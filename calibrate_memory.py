#!/usr/bin/env python3
"""Fit the energy cost of a byte of DRAM traffic from a memory sweep that was
run on an EXCLUSIVE node with perf cache-miss counters enabled.

  python3 calibrate_memory.py results/mem_<jobid>_<node>

For every run with perf data:   x = LLC misses x 64 bytes
                                y = DRAM energy of the job's sockets above idle
                                    (idle power taken from the w0_idle run)
Fits y = e_byte * x through the origin and writes calibration.json,
calibration.png and calibration_table.md into the directory.
"""
import glob
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e6e5e1"
BLUE, ORANGE = "#2a78d6", "#eb6834"
CACHE_LINE = 64


def main(d):
    runs = {os.path.basename(p)[:-5]: json.load(open(p)) for p in glob.glob(os.path.join(d, "*.json"))
            if not os.path.basename(p).startswith("calibration")}
    idle = runs.get("w0_idle")
    if idle is None:
        sys.exit("need a w0_idle run for the idle DRAM baseline")
    idle_w = idle["totals"]["scope_dram_avg_W"]
    rows = []
    for name, j in sorted(runs.items()):
        t = j["totals"]
        m = t.get("job_llc_misses")
        if name == "w0_idle" or m is None:
            continue
        x = m * CACHE_LINE
        y = t["scope_dram_J"] - idle_w * t["duration_s"]
        rows.append({"name": name, "label": j["meta"]["label"].split(":")[0], "bytes": x, "GB": x / 1e9,
                     "dram_above_idle_J": y, "cores": t["job_avg_cores_busy"], "GBps": x / 1e9 / t["duration_s"],
                     "nJ_per_line": (y / m * 1e9) if m else None})
    if not rows:
        sys.exit("no runs with perf cache-miss data; rerun the sweep with perf available")
    fit = [r for r in rows if r["GB"] > 1.0]           # ignore cache-resident runs for the slope
    sxx = sum(r["bytes"] ** 2 for r in fit)
    sxy = sum(r["bytes"] * r["dram_above_idle_J"] for r in fit)
    e_byte = sxy / sxx if sxx else float("nan")
    resid = [r["dram_above_idle_J"] - e_byte * r["bytes"] for r in fit]
    rmse = (sum(v * v for v in resid) / len(resid)) ** 0.5 if resid else float("nan")

    meta = rows[-1] and runs[rows[-1]["name"]]["meta"]
    out = {"node": meta["hostname"], "cpu": meta["cpu"], "slurm_job_id": meta["slurm_job_id"],
           "idle_dram_W": idle_w, "e_byte_J": e_byte, "nJ_per_byte": e_byte * 1e9, "nJ_per_cache_line": e_byte * CACHE_LINE * 1e9,
           "fit_runs": [r["name"] for r in fit], "rmse_J": rmse, "runs": rows}
    json.dump(out, open(os.path.join(d, "calibration.json"), "w"), indent=2)

    fig, ax = plt.subplots(figsize=(6.5, 4.6), facecolor=SURFACE)
    fig.subplots_adjust(top=0.8, bottom=0.15, left=0.13, right=0.97)
    ax.set_facecolor(SURFACE)
    xs = [r["GB"] for r in rows]
    ax.plot([0, max(xs) * 1.05], [0, e_byte * max(xs) * 1.05 * 1e9], color=INK2, lw=1, ls=(0, (4, 3)),
            label=f"fit: {e_byte * 1e9:.3f} nJ/byte ({e_byte * CACHE_LINE * 1e9:.1f} nJ per 64 B line)")
    ax.scatter(xs, [r["dram_above_idle_J"] for r in rows], s=55, color=BLUE, edgecolor=SURFACE, linewidth=1.5, zorder=3)
    for r in rows:
        ax.annotate(r["label"], (r["GB"], r["dram_above_idle_J"]), xytext=(6, 4), textcoords="offset points", fontsize=8.5, color=INK2)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
    ax.grid(axis="y", color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(colors=INK2, labelsize=9, length=0)
    ax.set_xlabel("DRAM traffic from LLC misses x 64 B (GB)", color=INK2, fontsize=9)
    ax.set_ylabel("DRAM energy above idle (J)", color=INK2, fontsize=9)
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=min(0, min(r["dram_above_idle_J"] for r in rows) * 1.1))
    ax.legend(frameon=False, fontsize=8.5, loc="upper left", labelcolor=INK2)
    fig.suptitle("DRAM energy per byte (calibration)", x=0.13, ha="left", fontsize=13, color=INK, fontweight="bold")
    fig.text(0.13, 0.86, f"{meta['hostname'].split('.')[0]}, {meta['cpu']}, job {meta['slurm_job_id']}, exclusive node, idle DRAM {idle_w:.1f} W",
             fontsize=9, color=INK2)
    fig.savefig(os.path.join(d, "calibration.png"), dpi=180, facecolor=SURFACE)

    md = ["| run | job cores busy | DRAM traffic (GB) | GB/s | DRAM energy above idle (J) | nJ per 64 B line |",
          "|---|---:|---:|---:|---:|---:|"]
    for r in rows:
        md.append(f"| {r['label']} | {r['cores']:.2f} | {r['GB']:.2f} | {r['GBps']:.2f} | {r['dram_above_idle_J']:.1f} | "
                  + (f"{r['nJ_per_line']:.1f}" if r["nJ_per_line"] is not None else "") + " |")
    md.append("")
    md.append(f"Fit over runs with more than 1 GB of traffic: **{e_byte * 1e9:.3f} nJ/byte**, {e_byte * CACHE_LINE * 1e9:.1f} nJ per cache line, rmse {rmse:.1f} J. "
              f"Use `--e-byte {e_byte:.4e}` with rapl_cgroup_reader.py.")
    table = "\n".join(md) + "\n"
    open(os.path.join(d, "calibration_table.md"), "w").write(table)
    print(table)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else sorted(glob.glob("results/mem_*"), key=os.path.getmtime)[-1])
