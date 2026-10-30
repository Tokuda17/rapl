#!/usr/bin/env python3
"""
rapl_cgroup_reader.py - sample Intel RAPL energy AND the job's cgroup v2
accounting together, so socket energy can be attributed to the job.

Each interval records, for the whole node, the RAPL energy of every domain,
and for the job's cgroup, CPU time (cpu.stat) and memory (memory.current).
From the cgroup's cpuset it works out which socket(s) the job may run on, and
reads busy CPU time for just those sockets' CPUs from /proc/stat. The job's
share of each interval's energy on those sockets is

    job_cpu_time / busy_cpu_time_on_job_sockets   (capped at 1)

and "attributed" energy is that share applied to the package (and DRAM)
domains of those sockets only. Sockets the job cannot touch are excluded.

Outputs (for --out PREFIX):
  PREFIX.csv   t_s, per-domain cumulative energy_J, job_cpu_s, scope_busy_cpu_s,
               job_mem_MB, attributed_package_J, attributed_dram_J
  PREFIX.json  metadata, cgroup info, attribution scope, totals, samples
  PREFIX.md    summary table

Examples:
  python3 rapl_cgroup_reader.py --duration 15 --out idle
  python3 rapl_cgroup_reader.py --out w3 -- python3 workloads/w3_two_cores.py --seconds 30
"""
import argparse
import csv
import glob
import json
import os
import platform
import re
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


def read_kv(path):
    """'key value' lines -> {key: int}. Missing file -> {}."""
    try:
        return {k: int(v) for k, v in (ln.split() for ln in _read(path).splitlines())}
    except (OSError, ValueError):
        return {}


def read_pressure(path):
    """PSI file -> {'some_total_us': .., 'full_total_us': ..} (missing -> {})."""
    out = {}
    try:
        for ln in _read(path).splitlines():
            parts = ln.split()
            kind = parts[0]
            for kv in parts[1:]:
                k, v = kv.split("=")
                if k == "total":
                    out[f"{kind}_total_us"] = int(v)
    except (OSError, ValueError):
        pass
    return out


def read_numa_anon(cg):
    """memory.numa_stat 'anon N0=.. N1=..' -> {'N0': bytes, ...}."""
    try:
        for ln in _read(os.path.join(cg, "memory.numa_stat")).splitlines():
            parts = ln.split()
            if parts[0] == "anon":
                return {kv.split("=")[0]: int(kv.split("=")[1]) for kv in parts[1:]}
    except (OSError, ValueError):
        pass
    return {}


def cgroup_stats_snapshot(cg):
    return {"memory_stat": read_kv(os.path.join(cg, "memory.stat")),
            "memory_pressure": read_pressure(os.path.join(cg, "memory.pressure")),
            "cpu_pressure": read_pressure(os.path.join(cg, "cpu.pressure")),
            "io_pressure": read_pressure(os.path.join(cg, "io.pressure"))}


def cgroup_stats_delta(before, after, cg, T):
    ms0, ms1 = before["memory_stat"], after["memory_stat"]
    def pct(key):
        a, b = before[key].get("some_total_us"), after[key].get("some_total_us")
        return round(100 * (b - a) / (T * 1e6), 3) if a is not None and b is not None and T else None
    return {
        "pgfault": ms1.get("pgfault", 0) - ms0.get("pgfault", 0),
        "pgmajfault": ms1.get("pgmajfault", 0) - ms0.get("pgmajfault", 0),
        "anon_MB_end": round(ms1.get("anon", 0) / 1e6, 1),
        "file_MB_end": round(ms1.get("file", 0) / 1e6, 1),
        "numa_anon_MB_end": {k: round(v / 1e6, 1) for k, v in read_numa_anon(cg).items()},
        "memory_pressure_some_pct": pct("memory_pressure"),
        "cpu_pressure_some_pct": pct("cpu_pressure"),
        "io_pressure_some_pct": pct("io_pressure"),
    }


def busy_jiffies(cpus=None):
    """Non-idle jiffies summed over `cpus` (set of ids), or all CPUs if None."""
    total = 0
    with open("/proc/stat") as f:
        for line in f:
            if not line.startswith("cpu"):
                break
            f0 = line.split()
            if cpus is None:
                if f0[0] != "cpu":
                    continue
            else:
                if f0[0] == "cpu" or int(f0[0][3:]) not in cpus:
                    continue
            user, nice, system, idle, iowait, irq, softirq, steal = map(int, f0[1:9])
            total += user + nice + system + irq + softirq + steal
            if cpus is None:
                break
    return total


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


def cpu_socket_map():
    """{cpu_id: physical_package_id} for every online CPU."""
    m = {}
    for p in glob.glob("/sys/devices/system/cpu/cpu[0-9]*/topology/physical_package_id"):
        cid = int(re.search(r"cpu(\d+)/", p).group(1))
        try:
            m[cid] = int(_read(p))
        except OSError:
            pass
    return m


def cgroup_info(cg):
    info = {"path": cg}
    try:
        info["cpuset_cpus_effective"] = _read(os.path.join(cg, "cpuset.cpus.effective"))
        cpus = parse_cpulist(info["cpuset_cpus_effective"])
        info["n_cpus"] = len(cpus)
        smap = cpu_socket_map()
        info["sockets"] = sorted({smap[c] for c in cpus if c in smap})
    except OSError:
        pass
    info["memory_max_bytes"] = read_int(os.path.join(cg, "memory.max"))
    try:
        info["cpu_max"] = _read(os.path.join(cg, "cpu.max"))
    except OSError:
        pass
    return info


def domain_socket(name):
    """'package-1' -> 1, 'package-1/dram' -> 1, else None."""
    m = re.match(r"package-(\d+)", name)
    return int(m.group(1)) if m else None


def is_dram(name):
    return "dram" in name.lower()


def is_package(name):
    return name.lower().startswith("package") and "/" not in name


def attribution_scope(domains, cg_info):
    """Decide which sockets/CPUs/domains the job's energy is attributed against."""
    smap = cpu_socket_map()
    sockets = cg_info.get("sockets") or sorted(set(smap.values()))
    cpus = {c for c, s in smap.items() if s in sockets} or None
    pkg_idx = [i for i, d in enumerate(domains) if is_package(d["name"]) and domain_socket(d["name"]) in sockets]
    dram_idx = [i for i, d in enumerate(domains) if is_dram(d["name"]) and domain_socket(d["name"]) in sockets]
    if not pkg_idx:  # names did not parse; fall back to everything
        pkg_idx = [i for i, d in enumerate(domains) if is_package(d["name"])]
        dram_idx = [i for i, d in enumerate(domains) if is_dram(d["name"])]
    return {
        "sockets": sockets,
        "n_cpus_in_scope": len(cpus) if cpus else len(smap),
        "package_domains": [domains[i]["name"] for i in pkg_idx],
        "dram_domains": [domains[i]["name"] for i in dram_idx],
        "_cpus": cpus, "_pkg_idx": pkg_idx, "_dram_idx": dram_idx,
    }


def sample_loop(domains, cg, scope, interval, duration=None, proc=None):
    cpus, pkg_idx, dram_idx = scope["_cpus"], scope["_pkg_idx"], scope["_dram_idx"]
    t0 = time.monotonic()
    prev_e = read_all(domains)
    prev_cpu = read_cpu_stat(cg)["usage_usec"]
    prev_busy = busy_jiffies(cpus)
    prev_node_busy = busy_jiffies(None)
    cum_uj = [0] * len(domains)
    cum_job_cpu = cum_scope_busy = cum_node_busy = 0.0
    attr_pkg = attr_dram = 0.0
    mem_peak = 0
    numa_peak = {}

    def row(t):
        return {
            "t_s": t,
            "energy_J": [x / 1e6 for x in cum_uj],
            "job_cpu_s": cum_job_cpu,
            "scope_busy_cpu_s": cum_scope_busy,
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
        cur_busy = busy_jiffies(cpus)
        cur_node_busy = busy_jiffies(None)

        d_uj = [delta_uj(prev_e[i], cur_e[i], domains[i]["max_uj"]) for i in range(len(domains))]
        d_job = (cur_cpu - prev_cpu) / 1e6
        d_busy = (cur_busy - prev_busy) / CLK_TCK
        share = min(1.0, d_job / d_busy) if d_busy > 0 else 0.0
        attr_pkg += share * sum(d_uj[i] for i in pkg_idx) / 1e6
        attr_dram += share * sum(d_uj[i] for i in dram_idx) / 1e6
        for i in range(len(domains)):
            cum_uj[i] += d_uj[i]
        cum_job_cpu += d_job
        cum_scope_busy += d_busy
        cum_node_busy += (cur_node_busy - prev_node_busy) / CLK_TCK
        mem_peak = max(mem_peak, read_int(os.path.join(cg, "memory.peak"), 0))
        for k, v in read_numa_anon(cg).items():
            numa_peak[k] = max(numa_peak.get(k, 0), v)
        prev_e, prev_cpu, prev_busy, prev_node_busy = cur_e, cur_cpu, cur_busy, cur_node_busy
        samples.append(row(now - t0))
        if done:
            break
    return samples, mem_peak, numa_peak


def summarize(domains, samples, mem_peak, scope):
    last = samples[-1]
    T = last["t_s"]
    per_domain = []
    for i, d in enumerate(domains):
        e = last["energy_J"][i]
        per_domain.append({"name": d["name"], "energy_J": round(e, 6), "avg_power_W": round(e / T, 3) if T else None})
    pkg_J = sum(x["energy_J"] for x in per_domain if is_package(x["name"]))
    dram_J = sum(x["energy_J"] for x in per_domain if is_dram(x["name"]))
    scope_pkg_J = sum(last["energy_J"][i] for i in scope["_pkg_idx"])
    scope_dram_J = sum(last["energy_J"][i] for i in scope["_dram_idx"])
    r = lambda v: round(v, 3) if v is not None else None
    return {
        "duration_s": T,
        "domains": per_domain,
        "node_package_J": r(pkg_J), "node_dram_J": r(dram_J),
        "node_package_avg_W": r(pkg_J / T) if T else None, "node_dram_avg_W": r(dram_J / T) if T else None,
        "scope_package_J": r(scope_pkg_J), "scope_dram_J": r(scope_dram_J),
        "scope_package_avg_W": r(scope_pkg_J / T) if T else None, "scope_dram_avg_W": r(scope_dram_J / T) if T else None,
        "job_cpu_s": r(last["job_cpu_s"]),
        "job_avg_cores_busy": r(last["job_cpu_s"] / T) if T else None,
        "scope_busy_cpu_s": r(last["scope_busy_cpu_s"]),
        "scope_avg_cores_busy": r(last["scope_busy_cpu_s"] / T) if T else None,
        "node_busy_cpu_s": r(last["node_busy_cpu_s"]),
        "node_avg_cores_busy": r(last["node_busy_cpu_s"] / T) if T else None,
        "job_share_of_scope_cpu": round(last["job_cpu_s"] / last["scope_busy_cpu_s"], 4) if last["scope_busy_cpu_s"] else None,
        "job_mem_peak_MB": round(mem_peak / 1e6, 1),
        "attributed_package_J": r(last["attributed_package_J"]),
        "attributed_dram_J": r(last["attributed_dram_J"]),
        "attributed_package_avg_W": r(last["attributed_package_J"] / T) if T else None,
        "attributed_dram_avg_W": r(last["attributed_dram_J"] / T) if T else None,
    }


def render_md(meta, cg, scope, tot, cgs=None):
    L = [f"### {meta['label']}", "",
         f"- host: `{meta['hostname']}`  cpu: {meta['cpu']}",
         f"- duration: {tot['duration_s']:.2f} s, samples: {meta['n_samples']}, interval: {meta['interval_s']} s"]
    if meta.get("command"):
        L.append(f"- command: `{' '.join(meta['command'])}` (exit {meta.get('exit_code')})")
    L.append(f"- cgroup: `{cg['path']}`  cpus: {cg.get('cpuset_cpus_effective', '?')} on socket(s) {scope['sockets']}")
    L.append(f"- attribution scope: {', '.join(scope['package_domains'])} ({scope['n_cpus_in_scope']} CPUs)")
    L += ["", "**Job (from cgroup)**", "",
          "| metric | value |", "|---|---:|",
          f"| CPU time used (s) | {tot['job_cpu_s']:.2f} |",
          f"| avg cores busy | {tot['job_avg_cores_busy']:.2f} |",
          f"| share of busy CPU time on its socket(s) | {100 * (tot['job_share_of_scope_cpu'] or 0):.1f}% |",
          f"| peak memory (MB) | {tot['job_mem_peak_MB']:.1f} |"]
    if cgs:
        L += [f"| page faults (major) | {cgs['pgfault']} ({cgs['pgmajfault']}) |",
              f"| peak anon memory by NUMA node (MB) | {cgs.get('numa_anon_MB_peak', cgs['numa_anon_MB_end'])} |",
              f"| memory / cpu pressure, some (%) | {cgs['memory_pressure_some_pct']} / {cgs['cpu_pressure_some_pct']} |"]
    L += [
          f"| attributed package energy (J) | {tot['attributed_package_J']:.2f} |",
          f"| attributed package power (W) | {tot['attributed_package_avg_W']:.2f} |",
          f"| attributed DRAM energy (J) | {tot['attributed_dram_J']:.2f} |",
          "", "**Node (from RAPL)**", "",
          f"avg cores busy, all users: {tot['scope_avg_cores_busy']:.2f} on job socket(s), {tot['node_avg_cores_busy']:.2f} whole node", "",
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
    scope = attribution_scope(domains, cg_info)
    snap0 = cgroup_stats_snapshot(cg)
    proc = subprocess.Popen(cmd) if cmd else None
    samples, mem_peak, numa_peak = sample_loop(domains, cg, scope, args.interval, None if cmd else args.duration, proc)
    exit_code = proc.wait() if proc else None
    snap1 = cgroup_stats_snapshot(cg)
    tot = summarize(domains, samples, mem_peak, scope)
    cg_stats = cgroup_stats_delta(snap0, snap1, cg, tot["duration_s"])
    cg_stats["numa_anon_MB_peak"] = {k: round(v / 1e6, 1) for k, v in numa_peak.items()}

    meta = {
        "label": args.label or os.path.basename(args.out),
        "hostname": socket.gethostname(), "cpu": cpu_model(), "kernel": platform.release(),
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "interval_s": args.interval, "n_samples": len(samples),
        "command": cmd or None, "exit_code": exit_code,
        "slurm_job_id": os.environ.get("SLURM_JOB_ID"),
        "slurm_cpus_per_task": os.environ.get("SLURM_CPUS_PER_TASK"),
    }
    scope_pub = {k: v for k, v in scope.items() if not k.startswith("_")}

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out + ".csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["t_s"] + [f"{d['name']}_J" for d in domains] +
                   ["job_cpu_s", "scope_busy_cpu_s", "node_busy_cpu_s", "job_mem_MB", "attributed_package_J", "attributed_dram_J"])
        for s in samples:
            w.writerow([f"{s['t_s']:.3f}"] + [f"{v:.6f}" for v in s["energy_J"]] +
                       [f"{s['job_cpu_s']:.4f}", f"{s['scope_busy_cpu_s']:.4f}", f"{s['node_busy_cpu_s']:.4f}", f"{s['job_mem_MB']:.2f}",
                        f"{s['attributed_package_J']:.6f}", f"{s['attributed_dram_J']:.6f}"])
    with open(args.out + ".json", "w") as f:
        json.dump({"meta": meta, "cgroup": cg_info, "cgroup_stats": cg_stats, "attribution_scope": scope_pub,
                   "rapl_domains": domains, "totals": tot, "samples": samples}, f, indent=2)
    md = render_md(meta, cg_info, scope_pub, tot, cg_stats)
    with open(args.out + ".md", "w") as f:
        f.write(md)
    print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
