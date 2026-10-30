#!/usr/bin/env python3
"""Plot memory access vs power from a memory sweep results directory.

  python3 plot_memory.py results/mem_<jobid>_<node>

Left:  power vs working set per process (log x), 8 streaming processes.
Right: DRAM power vs number of streaming processes at the largest working set.
Writes memory_vs_power.png and memory_table.md.
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
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"   # categorical slots 1-3


def per_socket(domains, kind):
    out = {}
    for d in domains:
        m = re.match(r"package-(\d+)(/dram)?$", d["name"])
        if m and (kind == "dram") == bool(m.group(2)):
            out[int(m.group(1))] = d["avg_power_W"]
    return out


def load(d):
    rows = []
    for p in glob.glob(os.path.join(d, "*.json")):
        j = json.load(open(p))
        name = os.path.basename(p)[:-5]
        m = re.match(r"(m|p)(\d+)$", name)
        if not m and name != "w0_idle":
            continue
        t = j["totals"]
        rows.append({
            "name": name, "kind": m.group(1) if m else "idle", "val": int(m.group(2)) if m else 0,
            "cores": t["job_avg_cores_busy"], "pkg": per_socket(t["domains"], "pkg"), "dram": per_socket(t["domains"], "dram"),
            "mem": t["job_mem_peak_MB"], "stats": j.get("cgroup_stats", {}), "sockets": j["cgroup"].get("sockets", []),
            "attr_dram_W": t["attributed_dram_avg_W"], "meta": j["meta"],
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


def main(d):
    rows = load(d)
    idle = next((r for r in rows if r["kind"] == "idle"), None)
    A = sorted((r for r in rows if r["kind"] == "m"), key=lambda r: r["val"])
    B = sorted((r for r in rows if r["kind"] == "p"), key=lambda r: r["val"])
    if not A:
        sys.exit(f"no m*.json in {d}")
    js = A[0]["sockets"][0] if A[0]["sockets"] else 0
    ctl = next((s for s in A[0]["pkg"] if s != js), None)
    mk = dict(lw=2, marker="o", ms=7, mec=SURFACE, mew=1.5)

    fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(14, 4.8), facecolor=SURFACE)
    fig.subplots_adjust(wspace=0.3, top=0.76, bottom=0.17, left=0.06, right=0.985)

    xa = [r["val"] for r in A]
    xlabels = [f"{v} MB" if v < 1024 else f"{v // 1024} GB" for v in xa]
    n_procs = A[0]["meta"].get("slurm_cpus_per_task", 8)

    # Panel 1: DRAM power vs working set
    a1.plot(xa, [r["dram"][js] for r in A], color=ORANGE, label=f"DRAM-{js} (job's socket)", **mk)
    if ctl is not None:
        a1.plot(xa, [r["dram"][ctl] for r in A], color=AQUA, label=f"DRAM-{ctl} (control)", **mk)
    if idle:
        a1.axhline(idle["dram"][js], color=INK2, lw=1, ls=(0, (4, 3)))
        a1.annotate(f"idle {idle['dram'][js]:.1f} W", (xa[-1], idle["dram"][js]), xytext=(0, 5),
                    textcoords="offset points", fontsize=8.5, color=INK2, ha="right", va="bottom")
    for i, r in enumerate(A):
        if i in (0, 1, 2, len(A) - 1):
            a1.annotate(f"{r['dram'][js]:.1f} W", (r["val"], r["dram"][js]), xytext=(0, 9), textcoords="offset points",
                        ha="center", fontsize=8.5, color=INK2)
    a1.set_title(f"DRAM power vs working set, {n_procs} streaming processes", loc="left", fontsize=10.5, color=INK, pad=10)
    a1.legend(frameon=False, fontsize=8.5, loc="center right", labelcolor=INK2)

    # Panel 2: package power vs working set (CPU usage constant)
    a2.plot(xa, [r["pkg"][js] for r in A], color=BLUE, label=f"package-{js} (job's socket)", **mk)
    if ctl is not None:
        a2.plot(xa, [r["pkg"][ctl] for r in A], color=AQUA, label=f"package-{ctl} (control)", **mk)
    if idle:
        a2.axhline(idle["pkg"][js], color=INK2, lw=1, ls=(0, (4, 3)))
        a2.annotate(f"idle {idle['pkg'][js]:.0f} W", (xa[-1], idle["pkg"][js]), xytext=(0, 5),
                    textcoords="offset points", fontsize=8.5, color=INK2, ha="right", va="bottom")
    a2.set_title(f"Package power vs working set, {n_procs} streaming processes", loc="left", fontsize=10.5, color=INK, pad=10)
    a2.legend(frameon=False, fontsize=8.5, loc="lower left", labelcolor=INK2)

    for a in (a1, a2):
        a.set_xscale("log", base=2)
        a.set_xticks(xa)
        a.set_xticklabels(xlabels)
        a.set_xlabel("working set per process (arrays swept a = b + c)", color=INK2, fontsize=9)
        a.set_ylabel("watts", color=INK2, fontsize=9)
        a.set_ylim(bottom=0)

    # Panel 3: DRAM power vs number of streaming processes at the largest working set
    if B:
        xb = [r["cores"] for r in B]
        a3.plot(xb, [r["dram"][js] for r in B], color=ORANGE, label=f"DRAM-{js} (job's socket)", **mk)
        if ctl is not None:
            a3.plot(xb, [r["dram"][ctl] for r in B], color=AQUA, label=f"DRAM-{ctl} (control)", **mk)
        for r in B:
            a3.annotate(f"p{r['val']}", (r["cores"], r["dram"][js]), xytext=(0, 9), textcoords="offset points",
                        ha="center", fontsize=8.5, color=INK2)
        big = B[0]["val"]
        a3.set_title(f"DRAM power vs streaming processes, {xlabels[-1]} each", loc="left", fontsize=10.5, color=INK, pad=10)
        a3.set_xlabel("average cores kept busy by the job (cgroup cpu.stat)", color=INK2, fontsize=9)
        a3.set_ylabel("watts", color=INK2, fontsize=9)
        a3.set_ylim(bottom=0)
        a3.set_xlim(left=0)
        a3.legend(frameon=False, fontsize=8.5, loc="lower right", labelcolor=INK2)
    for a in (a1, a2, a3):
        style(a)
        a.margins(y=0.15)

    meta = A[-1]["meta"]
    fig.suptitle("Memory access vs power on an ICE node", x=0.06, ha="left", fontsize=14, color=INK, fontweight="bold")
    fig.text(0.06, 0.895, f"{meta['hostname'].split('.')[0]}, {meta['cpu']}, Slurm job {meta['slurm_job_id']}, job CPUs on socket {js}, "
             f"{A[0]['meta']['interval_s']:g}s samples.", fontsize=9, color=INK2)
    fig.text(0.06, 0.855, f"Left and middle hold CPU usage at about {n_procs} cores; only the data's distance from the cores changes.",
             fontsize=9, color=INK2)
    png = os.path.join(d, "memory_vs_power.png")
    fig.savefig(png, dpi=180, facecolor=SURFACE)

    hdr = ["run", "job cores busy", f"package-{js} W"] + ([f"package-{ctl} W"] if ctl is not None else []) + \
          [f"DRAM-{js} W"] + ([f"DRAM-{ctl} W"] if ctl is not None else []) + \
          ["peak mem MB", "page faults", "peak anon by NUMA node (MB)", "mem pressure %"]
    md = ["| " + " | ".join(hdr) + " |", "|---|" + "---:|" * (len(hdr) - 1)]
    for r in ([idle] if idle else []) + A + B:
        st = r["stats"]
        cells = [r["name"], f"{r['cores']:.2f}", f"{r['pkg'][js]:.1f}"] + ([f"{r['pkg'][ctl]:.1f}"] if ctl is not None else []) + \
                [f"{r['dram'][js]:.1f}"] + ([f"{r['dram'][ctl]:.1f}"] if ctl is not None else []) + \
                [f"{r['mem']:.0f}", str(st.get("pgfault", "")), str(st.get("numa_anon_MB_peak", st.get("numa_anon_MB_end", ""))), str(st.get("memory_pressure_some_pct", ""))]
        md.append("| " + " | ".join(cells) + " |")
    table = "\n".join(md) + "\n"
    open(os.path.join(d, "memory_table.md"), "w").write(table)
    print(table)
    print("wrote", png)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else sorted(glob.glob("results/mem_*"), key=os.path.getmtime)[-1])
