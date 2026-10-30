#!/usr/bin/env python3
"""
rapl_reader.py - read Intel RAPL energy counters from Linux sysfs (powercap).

Samples every RAPL domain found under /sys/class/powercap (package, dram,
core, uncore, psys, ...) at a fixed interval, either for a fixed duration or
for as long as a wrapped command runs. Handles counter wraparound.

Outputs (for --out PREFIX):
  PREFIX.csv   time series: t_s, then one energy_J column per domain
  PREFIX.json  metadata, per-domain totals (energy J, avg power W), samples
  PREFIX.md    human-readable summary table

Examples:
  python3 rapl_reader.py --duration 10 --interval 1 --out idle
  python3 rapl_reader.py --interval 0.5 --out load -- ./my_program arg1
"""
import argparse
import csv
import glob
import json
import os
import platform
import socket
import subprocess
import sys
import time

POWERCAP = "/sys/class/powercap"


def _read(path):
    with open(path) as f:
        return f.read().strip()


def discover_domains():
    """Return list of dicts {id, path, name, max_uj} for readable RAPL domains."""
    domains = []
    for path in sorted(glob.glob(os.path.join(POWERCAP, "intel-rapl*:*"))):
        energy = os.path.join(path, "energy_uj")
        if not os.path.exists(energy):
            continue
        try:
            _read(energy)
        except PermissionError:
            print(f"warning: no permission to read {energy}", file=sys.stderr)
            continue
        dom_id = os.path.basename(path)
        name = _read(os.path.join(path, "name")) if os.path.exists(os.path.join(path, "name")) else dom_id
        max_path = os.path.join(path, "max_energy_range_uj")
        max_uj = int(_read(max_path)) if os.path.exists(max_path) else None
        # Label sub-domains with their parent so "dram" becomes "package-0/dram".
        parent = os.path.dirname(os.path.realpath(path))
        parent_name_file = os.path.join(parent, "name")
        if ":" in dom_id and dom_id.count(":") == 2 and os.path.exists(parent_name_file):
            name = f"{_read(parent_name_file)}/{name}"
        domains.append({"id": dom_id, "path": energy, "name": name, "max_uj": max_uj})
    return domains


def read_all(domains):
    return [int(_read(d["path"])) for d in domains]


def delta_uj(prev, cur, max_uj):
    d = cur - prev
    if d < 0 and max_uj:
        d += max_uj + 1
    return d


def sample_loop(domains, interval, duration=None, proc=None):
    """Collect samples until duration elapses or proc exits. Returns list of
    (t_seconds, [cumulative_energy_J per domain])."""
    t0 = time.monotonic()
    raw0 = read_all(domains)
    prev = list(raw0)
    cum_uj = [0] * len(domains)
    samples = [(0.0, [0.0] * len(domains))]
    next_t = t0 + interval
    while True:
        now = time.monotonic()
        done = False
        if proc is not None and proc.poll() is not None:
            done = True
        if duration is not None and now - t0 >= duration:
            done = True
        if not done:
            time.sleep(max(0.0, next_t - now))
            next_t += interval
        now = time.monotonic()
        cur = read_all(domains)
        for i, d in enumerate(domains):
            cum_uj[i] += delta_uj(prev[i], cur[i], d["max_uj"])
        prev = cur
        samples.append((now - t0, [x / 1e6 for x in cum_uj]))
        if done:
            break
    return samples


def summarize(domains, samples):
    total_t = samples[-1][0]
    out = []
    for i, d in enumerate(domains):
        e = samples[-1][1][i]
        out.append({
            "id": d["id"],
            "name": d["name"],
            "energy_J": round(e, 6),
            "avg_power_W": round(e / total_t, 3) if total_t > 0 else None,
        })
    return total_t, out


def write_outputs(prefix, meta, domains, samples, totals):
    os.makedirs(os.path.dirname(os.path.abspath(prefix)), exist_ok=True)
    with open(prefix + ".csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["t_s"] + [f"{d['name']}_J" for d in domains])
        for t, vals in samples:
            w.writerow([f"{t:.3f}"] + [f"{v:.6f}" for v in vals])
    with open(prefix + ".json", "w") as f:
        json.dump({
            "meta": meta,
            "domains": domains,
            "totals": totals,
            "samples": [{"t_s": round(t, 3), "energy_J": [round(v, 6) for v in vals]} for t, vals in samples],
        }, f, indent=2)
    md = render_md(meta, totals)
    with open(prefix + ".md", "w") as f:
        f.write(md)
    return md


def render_md(meta, totals):
    lines = [
        f"### RAPL summary: {meta['label']}",
        "",
        f"- host: `{meta['hostname']}`  cpu: {meta['cpu']}",
        f"- duration: {meta['duration_s']:.2f} s, samples: {meta['n_samples']}, interval: {meta['interval_s']} s",
    ]
    if meta.get("command"):
        lines.append(f"- command: `{' '.join(meta['command'])}` (exit {meta.get('exit_code')})")
    lines += ["", "| domain | energy (J) | avg power (W) |", "|---|---:|---:|"]
    for t in totals:
        lines.append(f"| {t['name']} | {t['energy_J']:.3f} | {t['avg_power_W']:.2f} |")
    lines.append("")
    return "\n".join(lines)


def cpu_model():
    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if line.startswith("model name"):
                    return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return platform.processor()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--interval", type=float, default=1.0, help="sampling interval in seconds (default 1)")
    ap.add_argument("--duration", type=float, help="sample for this many seconds (if no command given)")
    ap.add_argument("--out", default="rapl", help="output prefix, writes PREFIX.csv/.json/.md (default rapl)")
    ap.add_argument("--label", help="label stored in the output (default: basename of --out)")
    ap.add_argument("--list", action="store_true", help="list readable RAPL domains and exit")
    ap.add_argument("command", nargs=argparse.REMAINDER, help="command to run and measure (after --)")
    args = ap.parse_args()

    domains = discover_domains()
    if not domains:
        print(f"error: no readable RAPL domains under {POWERCAP}", file=sys.stderr)
        return 2
    if args.list:
        for d in domains:
            print(f"{d['id']:<16} {d['name']:<20} max_energy_range_uj={d['max_uj']}  {d['path']}")
        return 0

    cmd = args.command
    if cmd and cmd[0] == "--":
        cmd = cmd[1:]
    if not cmd and args.duration is None:
        ap.error("give --duration SECONDS or a command to run after --")

    proc = None
    if cmd:
        proc = subprocess.Popen(cmd)
    samples = sample_loop(domains, args.interval, duration=None if cmd else args.duration, proc=proc)
    exit_code = proc.wait() if proc else None

    total_t, totals = summarize(domains, samples)
    meta = {
        "label": args.label or os.path.basename(args.out),
        "hostname": socket.gethostname(),
        "cpu": cpu_model(),
        "kernel": platform.release(),
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "interval_s": args.interval,
        "duration_s": total_t,
        "n_samples": len(samples),
        "command": cmd or None,
        "exit_code": exit_code,
        "slurm_job_id": os.environ.get("SLURM_JOB_ID"),
    }
    md = write_outputs(args.out, meta, domains, samples, totals)
    print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
