#!/usr/bin/env python3
"""Simple CPU-bound workload used to produce a measurable RAPL load.

Spawns N processes that each run floating-point loops for the given number of
seconds. Uses numpy matrix multiplies when numpy is available, otherwise a
pure-Python arithmetic loop.
"""
import argparse
import multiprocessing as mp
import os
import time


def burn(seconds):
    end = time.monotonic() + seconds
    try:
        import numpy as np
        a = np.random.rand(512, 512)
        while time.monotonic() < end:
            a = a @ a
            a /= a.max()
    except ImportError:
        x = 1.0001
        while time.monotonic() < end:
            for _ in range(100000):
                x = x * 1.0000001 + 1e-9


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seconds", type=float, default=30)
    ap.add_argument("--procs", type=int, default=int(os.environ.get("SLURM_CPUS_PER_TASK", os.cpu_count() or 1)))
    args = ap.parse_args()
    print(f"workload: {args.procs} processes x {args.seconds}s", flush=True)
    ps = [mp.Process(target=burn, args=(args.seconds,)) for _ in range(args.procs)]
    for p in ps:
        p.start()
    for p in ps:
        p.join()


if __name__ == "__main__":
    main()
