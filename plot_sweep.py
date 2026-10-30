#!/usr/bin/env python3
"""Plot energy vs CPU usage from a sweep results directory.

  python3 plot_sweep.py results/sweep_<jobid>_<node>

Writes energy_vs_cpu.png and sweep_table.md into that directory.
x axis: average cores the job kept busy (cgroup cpu.stat / wall time).
Left:  RAPL package power per socket. The job's cpuset pins it to one socket,
       so the other socket acts as a control.
Right: package power attributed to the job (its share of busy CPU time on its
       socket x that socket's package energy), against the idle baseline.
"""
import glob
import json
import os
import re
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e6e5e1"
BLUE, ORANGE = "#2a78d6", "#eb6834"   # categorical slots 1 and 2


def per_socket(domains, kind):
    out = {}
    for d in domains:
        m = re.match(r"package-(\d+)(/dram)?$", d["name"])
        if not m:
            continue
        if (kind == "dram") == bool(m.group(2)):
            out[int(m.group(1))] = d["avg_power_W"]
    return out


def load(d):
    rows = []
    for p in sorted(glob.glob(os.path.join(d, "w*.json"))):
        j = json.load(open(p))
        t = j["totals"]
        job_sockets = j["cgroup"].get("sockets") or []
        pkg = per_socket(t["domains"], "pkg")
        dram = per_socket(t["domains"], "dram")
        rows.append({
            "name": os.path.basename(p)[:-5],
            "label": j["meta"]["label"].split(":")[0].split(" ")[0],
            "cores": t["job_avg_cores_busy"],
            "scope_cores": t.get("scope_avg_cores_busy", t["node_avg_cores_busy"]),
            "share": t.get("job_share_of_scope_cpu", t.get("job_share_of_node_cpu")) or 0,
            "pkg": pkg, "dram": dram,
            "job_sockets": job_sockets,
            "attr_W": t["attributed_package_avg_W"],
            "attr_J": t["attributed_package_J"],
            "attr_dram_W": t["attributed_dram_avg_W"],
            "dur": t["duration_s"],
            "mem": t["job_mem_peak_MB"],
            "meta": j["meta"],
        })
    return rows


def label_points(ax, rows, ykey, first="left"):
    """Direct labels; the first two points sit close together at x~0, so push
    them apart instead of stacking them."""
    for i, r in enumerate(rows):
        if i == 0:
            kw = dict(xytext=(-7, -4), ha="right", va="top") if first == "left" else dict(xytext=(9, -2), ha="left", va="top")
        elif i == 1:
            kw = dict(xytext=(7, 4), ha="left", va="bottom")
        else:
            kw = dict(xytext=(0, 9), ha="center")
        ax.annotate(r["label"], (r["cores"], ykey(r)), textcoords="offset points", fontsize=8.5, color=INK2, **kw)


def style(ax):
    ax.set_facecolor(SURFACE)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(colors=INK2, labelsize=9, length=0)


def main(d):
    rows = load(d)
    if not rows:
        sys.exit(f"no w*.json in {d}")
    x = [r["cores"] for r in rows]
    sockets = sorted(rows[0]["pkg"])
    job_socks = rows[0]["job_sockets"]
    mk = dict(lw=2, marker="o", ms=7, mec=SURFACE, mew=1.5)

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.8), facecolor=SURFACE)
    fig.subplots_adjust(wspace=0.3, top=0.76, bottom=0.17, left=0.08, right=0.98)

    # Left: per-socket package power. Job socket(s) first so it takes slot 1 (blue).
    order = [s for s in sockets if s in job_socks] + [s for s in sockets if s not in job_socks]
    colors = [BLUE, ORANGE]
    for s, c in zip(order[:2], colors):
        tag = "job's CPUs here" if s in job_socks else "no job CPUs, control"
        a1.plot(x, [r["pkg"][s] for r in rows], color=c, label=f"package-{s} ({tag})", **mk)
    label_points(a1, rows, lambda r: r["pkg"][order[0]])
    a1.set_title("RAPL package power per socket", loc="left", fontsize=11, color=INK, pad=10)
    a1.set_ylabel("watts", color=INK2, fontsize=9)
    a1.legend(frameon=False, fontsize=8.5, loc="lower right", labelcolor=INK2)
    a1.set_ylim(bottom=0)

    # Right: attributed power vs idle baseline of the job's socket.
    idle_rows = [r for r in rows if "idle" in r["name"]]
    base = idle_rows[0]["pkg"][order[0]] if idle_rows else None
    a2.plot(x, [r["attr_W"] for r in rows], color=BLUE, **mk, label="attributed to job")
    if base is not None:
        a2.axhline(base, color=INK2, lw=1, ls=(0, (4, 3)))
        a2.annotate(f"socket idle power {base:.0f} W", (max(x), base), xytext=(0, -12), textcoords="offset points",
                    ha="right", fontsize=8.5, color=INK2)
    label_points(a2, rows, lambda r: r["attr_W"], first="right")
    a2.set_title("Package power attributed to this job", loc="left", fontsize=11, color=INK, pad=10)
    a2.set_ylabel("watts (job share of its socket's package energy)", color=INK2, fontsize=9)
    a2.set_ylim(bottom=0)

    for a in (a1, a2):
        style(a)
        a.set_xlabel("average cores kept busy by the job (cgroup cpu.stat / wall time)", color=INK2, fontsize=9)
        a.set_xlim(left=-0.4)
        a.margins(y=0.12)

    meta = rows[-1]["meta"]
    fig.suptitle("Energy vs CPU usage on an ICE node", x=0.08, ha="left", fontsize=14, color=INK, fontweight="bold")
    fig.text(0.08, 0.875, f"{meta['hostname'].split('.')[0]}, {meta['cpu']}, {rows[-1]['dur']:.0f}s per workload, "
             f"Slurm job {meta['slurm_job_id']}, {meta.get('slurm_cpus_per_task')} CPUs on socket {job_socks}.",
             fontsize=9, color=INK2)
    png = os.path.join(d, "energy_vs_cpu.png")
    fig.savefig(png, dpi=180, facecolor=SURFACE)

    hdr = ["workload", "job cores busy", "socket cores busy (all users)", "job share"] + \
          [f"package-{s} W" for s in sockets] + [f"dram-{s} W" for s in sockets] + \
          ["attributed package J", "attributed package W", "peak mem MB"]
    md = ["| " + " | ".join(hdr) + " |", "|---|" + "---:|" * (len(hdr) - 1)]
    for r in rows:
        cells = [r["label"], f"{r['cores']:.2f}", f"{r['scope_cores']:.2f}", f"{100*r['share']:.0f}%"] + \
                [f"{r['pkg'][s]:.1f}" for s in sockets] + [f"{r['dram'].get(s, float('nan')):.1f}" for s in sockets] + \
                [f"{r['attr_J']:.0f}", f"{r['attr_W']:.1f}", f"{r['mem']:.0f}"]
        md.append("| " + " | ".join(cells) + " |")
    table = "\n".join(md) + "\n"
    open(os.path.join(d, "sweep_table.md"), "w").write(table)
    print(table)
    print("wrote", png)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else sorted(glob.glob("results/sweep_*"))[-1])
