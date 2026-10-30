#!/usr/bin/env python3
"""Level 4: numpy matrix multiplies on half the allocated CPUs (4 of 8 by default)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import parse, run_procs, burn_numpy, allocated_cpus

if __name__ == "__main__":
    run_procs(max(1, allocated_cpus() // 2), burn_numpy, parse().seconds)
