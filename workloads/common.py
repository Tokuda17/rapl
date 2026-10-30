"""Shared helpers for the workload ladder. Pins BLAS to one thread per process
so the number of busy cores equals the number of processes."""
import argparse
import multiprocessing as mp
import os
import time

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")


def parse(default_seconds=30):
    ap = argparse.ArgumentParser()
    ap.add_argument("--seconds", type=float, default=default_seconds)
    return ap.parse_args()


def burn_python(seconds):
    """Pure-Python floating point loop, one core at 100%."""
    end = time.monotonic() + seconds
    x = 1.0001
    while time.monotonic() < end:
        for _ in range(50000):
            x = x * 1.0000001 + 1e-9
    return x


def burn_numpy(seconds, n=768):
    """Dense matrix multiply loop, one core at 100% with heavy FP/vector use."""
    import numpy as np
    a = np.random.rand(n, n)
    b = np.random.rand(n, n)
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        c = a @ b
        a = c / c.max()
    return a


def burn_duty_cycle(seconds, duty=0.2, period=1.0):
    """Busy for `duty` of each period, sleeping the rest. Light load."""
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        t_busy_end = time.monotonic() + duty * period
        x = 1.0001
        while time.monotonic() < t_busy_end:
            x = x * 1.0000001 + 1e-9
        time.sleep(max(0.0, (1 - duty) * period))


def run_procs(n, target, seconds):
    print(f"workload: {n} process(es) x {seconds}s of {target.__name__}", flush=True)
    ps = [mp.Process(target=target, args=(seconds,)) for _ in range(n)]
    for p in ps:
        p.start()
    for p in ps:
        p.join()


def allocated_cpus():
    return int(os.environ.get("SLURM_CPUS_PER_TASK", os.cpu_count() or 1))
