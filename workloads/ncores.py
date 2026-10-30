#!/usr/bin/env python3
"""Parametric level: N processes doing dense numpy matrix multiplies, ~N cores.
    python3 workloads/ncores.py --procs 3 --seconds 30
"""
import argparse, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import run_procs, burn_numpy

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--procs", type=int, required=True)
    ap.add_argument("--seconds", type=float, default=30)
    a = ap.parse_args()
    run_procs(a.procs, burn_numpy, a.seconds)
