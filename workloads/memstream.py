#!/usr/bin/env python3
"""Memory-streaming workload: N processes, each sweeping a = b + c over arrays
sized to a given working set, STREAM-style. CPU usage is ~N cores whatever the
size; what changes is whether the data lives in cache or in DRAM.

    python3 workloads/memstream.py --procs 8 --mb 256 --seconds 30
--mb is the working set PER PROCESS (three arrays of mb/3 each).
"""
import argparse, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: F401  (pins BLAS threads to 1)
import multiprocessing as mp


def stream(seconds, mb):
    import numpy as np
    n = int(mb * 1e6 / 3 / 8)          # three float64 arrays totalling mb MB
    a = np.ones(n); b = np.full(n, 1.5); c = np.full(n, 2.5)
    end = time.monotonic() + seconds
    sweeps = 0
    while time.monotonic() < end:
        np.add(b, c, out=a)             # read b, read c, write a
        a, b, c = b, c, a               # rotate so nothing is dead
        sweeps += 1
    bytes_moved = sweeps * 3 * n * 8
    print(f"  pid {os.getpid()}: {sweeps} sweeps, {bytes_moved / seconds / 1e9:.2f} GB/s", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--procs", type=int, default=common.allocated_cpus())
    ap.add_argument("--mb", type=float, required=True, help="working set per process, MB")
    ap.add_argument("--seconds", type=float, default=30)
    a = ap.parse_args()
    print(f"workload: {a.procs} process(es) x {a.seconds}s streaming {a.mb:g} MB each ({a.procs * a.mb / 1e3:.2f} GB total)", flush=True)
    ps = [mp.Process(target=stream, args=(a.seconds, a.mb)) for _ in range(a.procs)]
    for p in ps: p.start()
    for p in ps: p.join()
