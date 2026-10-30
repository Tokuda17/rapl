#!/usr/bin/env python3
"""Plot energy vs CPU usage from a sweep results directory.

  python3 plot_sweep.py results/sweep_<jobid>_<node>

Writes energy_vs_cpu.png and sweep_table.md into that directory.
x axis: average cores the job kept busy (cgroup cpu.stat / wall time).
Left:  node average power from RAPL (package total, DRAM total).
Right: energy attributed to the job (package), job share x node package energy.
"""
import glob
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e6e5e1"
BLUE, ORANGE = "#2a78d6", "#eb6834"   # categorical slots 1 and 2


def load(d):
    rows = []
    for p in sorted(glob.glob(os.path.join(d, "w*.json"))):
        j = json.load(open(p))
        t = j["totals"]
        rows.append({
            "name": os.path.basename(p)[:-5],
            "label": j["meta"]["label"].split(":")[0].split(" ")[0],
            "cores": t["job_avg_cores_busy"],
            "node_cores": t["node_avg_cores_busy"],
            "pkg_W": t["node_package_avg_W"],
            "dram_W": t["node_dram_avg_W"],
            "pkg_J": t["node_package_J"],
            "attr_J": t["attributed_package_J"],
            "attr_W": t["attributed_package_avg_W"],
            "share": t["job_share_of_node_cpu"] or 0,
            "dur": t["duration_s"],
            "mem": t["job_mem_peak_MB"],
        })
    return rows


def style(ax):
    ax.set_facecolor(SURFACE)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(colors=INK2, labelsize=9, length=0)
    for lbl in ax.get_xticklabels() + ax.get_yticklabels():
        lbl.set_color(INK2)


def main(d):
    rows = load(d)
    if not rows:
        sys.exit(f"no w*.json in {d}")
    x = [r["cores"] for r in rows]

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.6), facecolor=SURFACE)
    fig.subplots_adjust(wspace=0.3, top=0.8, bottom=0.17, left=0.08, right=0.98)

    a1.plot(x, [r["pkg_W"] for r in rows], color=BLUE, lw=2, marker="o", ms=7, mec=SURFACE, mew=1.5, label="CPU packages (both sockets)")
    a1.plot(x, [r["dram_W"] for r in rows], color=ORANGE, lw=2, marker="o", ms=7, mec=SURFACE, mew=1.5, label="DRAM (both sockets)")
    for r in rows:
        a1.annotate(r["label"], (r["cores"], r["pkg_W"]), xytext=(0, 9), textcoords="offset points", ha="center", fontsize=8.5, color=INK2)
    a1.set_title("Node average power from RAPL", loc="left", fontsize=11, color=INK, pad=10)
    a1.set_ylabel("watts", color=INK2, fontsize=9)
    a1.legend(frameon=False, fontsize=8.5, loc="upper left", labelcolor=INK2)
    a1.set_ylim(bottom=0)

    a2.plot(x, [r["attr_W"] for r in rows], color=BLUE, lw=2, marker="o", ms=7, mec=SURFACE, mew=1.5)
    for r in rows:
        a2.annotate(r["label"], (r["cores"], r["attr_W"]), xytext=(0, 9), textcoords="offset points", ha="center", fontsize=8.5, color=INK2)
    a2.set_title("Package power attributed to this job", loc="left", fontsize=11, color=INK, pad=10)
    a2.set_ylabel("watts (job share of socket energy)", color=INK2, fontsize=9)
    a2.set_ylim(bottom=0)

    for a in (a1, a2):
        style(a)
        a.set_xlabel("average cores kept busy by the job (cgroup cpu.stat)", color=INK2, fontsize=9)
        a.set_xlim(left=-0.3)

    meta = json.load(open(os.path.join(d, rows[-1]["name"] + ".json")))["meta"]
    fig.suptitle("Energy vs CPU usage on an ICE node", x=0.08, ha="left", fontsize=14, color=INK, fontweight="bold")
    fig.text(0.08, 0.86, f"{meta['hostname'].split('.')[0]}, {meta['cpu']}, {rows[0]['dur']:.0f}s per workload, Slurm job {meta['slurm_job_id']}. "
             "Node is shared, so node power includes other users' jobs.", fontsize=9, color=INK2)
    png = os.path.join(d, "energy_vs_cpu.png")
    fig.savefig(png, dpi=180, facecolor=SURFACE)

    md = ["| workload | job cores busy | node cores busy (all users) | job share of CPU | node package W | node DRAM W | attributed package J | attributed package W | peak mem MB |",
          "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for r in rows:
        md.append(f"| {r['label']} | {r['cores']:.2f} | {r['node_cores']:.2f} | {100*r['share']:.1f}% | {r['pkg_W']:.1f} | {r['dram_W']:.1f} | {r['attr_J']:.1f} | {r['attr_W']:.2f} | {r['mem']:.0f} |")
    table = "\n".join(md) + "\n"
    open(os.path.join(d, "sweep_table.md"), "w").write(table)
    print(table)
    print("wrote", png)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else sorted(glob.glob("results/sweep_*"))[-1])
