#!/usr/bin/env python3
"""
rapl_cgroup_reader.py - sample Intel RAPL energy AND the job's cgroup v2
accounting together, so socket energy can be attributed to the job.

Each interval records, for the whole node, the RAPL energy of every domain,
and for the job's cgroup, CPU time (cpu.stat), memory (memory.current), plus
node-wide busy CPU time from /proc/stat. The job's share of each interval's
package energy is  job_cpu_time / node_busy_cpu_time  (capped at 1).

Outputs (for --out PREFIX):
  PREFIX.csv   t_s, per-domain cumulative energy_J, job_cpu_s, node_busy_cpu_s,
               job_mem_MB, attributed_package_J, attributed_dram_J
  PREFIX.json  metadata, cgroup info, totals, samples
  PREFIX.md    summary table

Examples:
  python3 rapl_cgroup_reader.py --duration 15 --out idle
  python3 rapl_cgroup_reader.py --out w3 -- python3 workloads/w3_two_cores.py --seconds 30
"""
import argparse
import csv
import json
import os
import platform
import socket
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rapl_reader import discover_domains, read_all, delta_uj, cpu_model  # noqa: E402

CGROUP_ROOT = "/sys/fs/cgroup"
CLK_TCK = os.sysconf("SC_CLK_TCK")


def _read(path):
    with open(path) as f:
        return f.read().strip()


def find_job_cgroup():
    """Return the job-level cgroup directory for this process.

    Under Slurm the process sits in .../slurmstepd.scope/<job>/step_X/user/task_0;
    we walk up to the <job> node so every step and task of the job is counted.
    Outside Slurm, the process's own cgroup is used."""
    rel = _read("/proc/self/cgroup").split("::", 1)[-1]
    parts = [p for p in rel.split("/") if p]
    if "slurmstepd.scope" in parts:
        i = parts.index("slurmstepd.scope")
        parts = parts[: i + 2]
    return os.path.join(CGROUP_ROOT, *parts)


def read_cpu_stat(cg):
    d = {}
    for line in _read(os.path.join(cg, "cpu.stat")).splitlines():
        k, v = line.split()
        d[k] = int(v)
    return d


def read_int(path, default=None):
    try:
        v = _read(path)
        return int(v) if v != "max" else None
    except (OSError, ValueError):
        return default


def node_busy_jiffies():
    """Sum of non-idle jiffies across all CPUs (first 'cpu' line of /proc/stat)."""
    with open("/proc/stat") as f:
        f0 = f.readline().split()
    user, nice, system, idle, iowait, irq, softirq, steal = map(int, f0[1:9])
    return user + nice + system + irq + softirq + steal


def parse_cpulist(s):
    cpus = []
    for part in s.split(","):
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-")
            cpus.extend(range(int(a), int(b) + 1))
        else:
            cpus.append(int(part))
    return cpus


def sockets_for_cpus(cpus):
    socks = set()
    for c in cpus:
        p = f"/sys/devices/system/cpu/cpu{c}/topology/physical_package_id"
        try:
            socks.add(int(_read(p)))
        except OSError:
            pass
    return sorted(socks)


def cgroup_info(cg):
    info = {"path": cg}
    try:
        info["cpuset_cpus_effective"] = _read(os.path.join(cg, "cpuset.cpus.effective"))
        cpus = parse_cpulist(info["cpuset_cpus_effective"])
        info["n_cpus"] = len(cpus)
        info["sockets"] = sockets_for_cpus(cpus)
    except OSError:
        pass
    info["memory_max_bytes"] = read_int(os.path.join(cg, "memory.max"))
    try:
        info["cpu_max"] = _read(os.path.join(cg, "cpu.max"))
    except OSError:
        pass
    return info


def is_dram(name):
    return "dram" in name.lower()


def is_package(name):
    return name.lower().startswith("package") and "/" not in name


def sample_loop(domains, cg, interval, duration=None, proc=None):
    pkg_idx = [i for i, d in enumerate(domains) if is_package(d["name"])]
    dram_idx = [i for i, d in enumerate(domains) if is_dram(d["name"])]

    t0 = time.monotonic()
    prev_e = read_all(domains)
    prev_cpu = read_cpu_stat(cg)["usage_usec"]
    prev_busy = node_busy_jiffies()
    cum_uj = [0] * len(domains)
    cum_job_cpu = 0.0
    cum_node_busy = 0.0
    attr_pkg = 0.0
    attr_dram = 0.0
    mem_peak = 0

    def row(t):
        return {
            "t_s": t,
            "energy_J": [x / 1e6 for x in cum_uj],
            "job_cpu_s": cum_job_cpu,
            "node_busy_cpu_s": cum_node_busy,
            "job_mem_MB": read_int(os.path.join(cg, "memory.current"), 0) / 1e6,
            "attributed_package_J": attr_pkg,
            "attributed_dram_J": attr_dram,
        }

    samples = [row(0.0)]
    next_t = t0 + interval
    while True:
        now = time.monotonic()
        done = (proc is not None and proc.poll() is not None) or (duration is not None and now - t0 >= duration)
        if not done:
            time.sleep(max(0.0, next_t - now))
            next_t += interval
        now = time.monotonic()
        cur_e = read_all(domains)
        cur_cpu = read_cpu_stat(cg)["usage_usec"]
        cur_busy = node_busy_jiffies()

        d_uj = [delta_uj(prev_e[i], cur_e[i], domains[i]["max_uj"]) for i in range(len(domains))]
        d_job = (cur_cpu - prev_cpu) / 1e6
        d_busy = (cur_busy - prev_busy) / CLK_TCK
        share = min(1.0, d_job / d_busy) if d_busy > 0 else 0.0
        attr_pkg += share * sum(d_uj[i] for i in pkg_idx) / 1e6
        attr_dram += share * sum(d_uj[i] for i in dram_idx) / 1e6
        for i in range(len(domains)):
            cum_uj[i] += d_uj[i]
        cum_job_cpu += d_job
        cum_node_busy += d_busy
        mem_peak = max(mem_peak, read_int(os.path.join(cg, "memory.peak"), 0))
        prev_e, prev_cpu, prev_busy = cur_e, cur_cpu, cur_busy
        samples.append(row(now - t0))
        if done:
            break
    return samples, mem_peak


def summarize(domains, samples, mem_peak):
    last = samples[-1]
    T = last["t_s"]
    per_domain = []
    for i, d in enumerate(domains):
        e = last["energy_J"][i]
        per_domain.append({"name": d["name"], "energy_J": round(e, 6), "avg_power_W": round(e / T, 3) if T else None})
    pkg_J = sum(x["energy_J"] for x in per_domain if is_package(x["name"]))
    dram_J = sum(x["energy_J"] for x in per_domain if is_dram(x["name"]))
    return {
        "duration_s": T,
        "domains": per_domain,
        "node_package_J": round(pkg_J, 6),
        "node_dram_J": round(dram_J, 6),
        "node_package_avg_W": round(pkg_J / T, 3) if T else None,
        "node_dram_avg_W": round(dram_J / T, 3) if T else None,
        "job_cpu_s": round(last["job_cpu_s"], 3),
        "job_avg_cores_busy": round(last["job_cpu_s"] / T, 3) if T else None,
        "node_busy_cpu_s": round(last["node_busy_cpu_s"], 3),
        "node_avg_cores_busy": round(last["node_busy_cpu_s"] / T, 3) if T else None,
        "job_share_of_node_cpu": round(last["job_cpu_s"] / last["node_busy_cpu_s"], 4) if last["node_busy_cpu_s"] else None,
        "job_mem_peak_MB": round(mem_peak / 1e6, 1),
        "attributed_package_J": round(last["attributed_package_J"], 6),
        "attributed_dram_J": round(last["attributed_dram_J"], 6),
        "attributed_package_avg_W": round(last["attributed_package_J"] / T, 3) if T else None,
        "attributed_dram_avg_W": round(last["attributed_dram_J"] / T, 3) if T else None,
    }


def render_md(meta, cg, tot):
    L = [f"### {meta['label']}", "",
         f"- host: `{meta['hostname']}`  cpu: {meta['cpu']}",
         f"- duration: {tot['duration_s']:.2f} s, samples: {meta['n_samples']}, interval: {meta['interval_s']} s"]
    if meta.get("command"):
        L.append(f"- command: `{' '.join(meta['command'])}` (exit {meta.get('exit_code')})")
    L.append(f"- cgroup: `{cg['path']}`  cpus: {cg.get('cpuset_cpus_effective', '?')} (sockets {cg.get('sockets', '?')})")
    L += ["", "**Job (from cgroup)**", "",
          "| metric | value |", "|---|---:|",
          f"| CPU time used (s) | {tot['job_cpu_s']:.2f} |",
          f"| avg cores busy | {tot['job_avg_cores_busy']:.2f} |",
          f"| share of node CPU time | {100 * (tot['job_share_of_node_cpu'] or 0):.1f}% |",
          f"| peak memory (MB) | {tot['job_mem_peak_MB']:.1f} |",
          f"| attributed package energy (J) | {tot['attributed_package_J']:.2f} |",
          f"| attributed package power (W) | {tot['attributed_package_avg_W']:.2f} |",
          f"| attributed DRAM energy (J) | {tot['attributed_dram_J']:.2f} |",
          "", "**Node (from RAPL)**", "",
          f"node avg cores busy (all users): {tot['node_avg_cores_busy']:.2f}", "",
          "| domain | energy (J) | avg power (W) |", "|---|---:|---:|"]
    for d in tot["domains"]:
        L.append(f"| {d['name']} | {d['energy_J']:.3f} | {d['avg_power_W']:.2f} |")
    L.append("")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--interval", type=float, default=1.0)
    ap.add_argument("--duration", type=float)
    ap.add_argument("--out", default="rapl_cgroup")
    ap.add_argument("--label")
    ap.add_argument("--cgroup", help="cgroup directory to account (default: this job's)")
    ap.add_argument("command", nargs=argparse.REMAINDER)
    args = ap.parse_args()

    domains = discover_domains()
    if not domains:
        print("error: no readable RAPL domains", file=sys.stderr)
        return 2
    cg = args.cgroup or find_job_cgroup()
    if not os.path.exists(os.path.join(cg, "cpu.stat")):
        print(f"error: {cg}/cpu.stat not found (cgroup v2 required)", file=sys.stderr)
        return 2

    cmd = args.command[1:] if args.command and args.command[0] == "--" else args.command
    if not cmd and args.duration is None:
        ap.error("give --duration SECONDS or a command after --")

    cg_info = cgroup_info(cg)
    proc = subprocess.Popen(cmd) if cmd else None
    samples, mem_peak = sample_loop(domains, cg, args.interval, None if cmd else args.duration, proc)
    exit_code = proc.wait() if proc else None
    tot = summarize(domains, samples, mem_peak)

    meta = {
        "label": args.label or os.path.basename(args.out),
        "hostname": socket.gethostname(), "cpu": cpu_model(), "kernel": platform.release(),
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "interval_s": args.interval, "n_samples": len(samples),
        "command": cmd or None, "exit_code": exit_code,
        "slurm_job_id": os.environ.get("SLURM_JOB_ID"),
        "slurm_cpus_per_task": os.environ.get("SLURM_CPUS_PER_TASK"),
    }

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out + ".csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["t_s"] + [f"{d['name']}_J" for d in domains] +
                   ["job_cpu_s", "node_busy_cpu_s", "job_mem_MB", "attributed_package_J", "attributed_dram_J"])
        for s in samples:
            w.writerow([f"{s['t_s']:.3f}"] + [f"{v:.6f}" for v in s["energy_J"]] +
                       [f"{s['job_cpu_s']:.4f}", f"{s['node_busy_cpu_s']:.4f}", f"{s['job_mem_MB']:.2f}",
                        f"{s['attributed_package_J']:.6f}", f"{s['attributed_dram_J']:.6f}"])
    with open(args.out + ".json", "w") as f:
        json.dump({"meta": meta, "cgroup": cg_info, "rapl_domains": domains, "totals": tot, "samples": samples}, f, indent=2)
    md = render_md(meta, cg_info, tot)
    with open(args.out + ".md", "w") as f:
        f.write(md)
    print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
