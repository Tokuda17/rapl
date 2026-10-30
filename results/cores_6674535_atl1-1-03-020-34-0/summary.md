# RAPL + cgroup cores sweep: job 6674535 on atl1-1-03-020-34-0.pace.gatech.edu

Collected 2026-10-30T19:13:32Z with `run_cores_sweep.sbatch` (8 CPUs allocated).

```
CPU(s):                                  96
Model name:                              Intel(R) Xeon(R) 6740P
Thread(s) per core:                      1
Socket(s):                               2
CPU(s) scaling MHz:                      53%
```
### w0_idle: idle baseline (20s)

- host: `atl1-1-03-020-34-0.pace.gatech.edu`  cpu: Intel(R) Xeon(R) 6740P
- duration: 20.00 s, samples: 22, interval: 1.0 s
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM673F56B00`  cpus: 20-27 on socket(s) [0]
- attribution scope: package-0 (48 CPUs)

**Job (from cgroup)**

| metric | value |
|---|---:|
| CPU time used (s) | 0.02 |
| avg cores busy | 0.00 |
| share of busy CPU time on its socket(s) | 0.0% |
| peak memory (MB) | 11.8 |
| attributed package energy (J) | 0.63 |
| attributed package power (W) | 0.03 |
| attributed DRAM energy (J) | 0.18 |

**Node (from RAPL)**

avg cores busy, all users: 3.06 on job socket(s), 5.10 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 1948.243 | 97.41 |
| package-0/dram | 557.438 | 27.87 |
| package-1 | 1849.770 | 92.48 |
| package-1/dram | 648.880 | 32.44 |

### c1: 1 core(s) numpy (30s)

- host: `atl1-1-03-020-34-0.pace.gatech.edu`  cpu: Intel(R) Xeon(R) 6740P
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/ncores.py --procs 1 --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM673F56B00`  cpus: 20-27 on socket(s) [0]
- attribution scope: package-0 (48 CPUs)

**Job (from cgroup)**

| metric | value |
|---|---:|
| CPU time used (s) | 29.99 |
| avg cores busy | 0.97 |
| share of busy CPU time on its socket(s) | 23.2% |
| peak memory (MB) | 56.3 |
| attributed package energy (J) | 737.03 |
| attributed package power (W) | 23.77 |
| attributed DRAM energy (J) | 200.92 |

**Node (from RAPL)**

avg cores busy, all users: 4.17 on job socket(s), 6.33 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 3171.973 | 102.31 |
| package-0/dram | 865.788 | 27.93 |
| package-1 | 2845.735 | 91.79 |
| package-1/dram | 1020.729 | 32.92 |

### c2: 2 core(s) numpy (30s)

- host: `atl1-1-03-020-34-0.pace.gatech.edu`  cpu: Intel(R) Xeon(R) 6740P
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/ncores.py --procs 2 --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM673F56B00`  cpus: 20-27 on socket(s) [0]
- attribution scope: package-0 (48 CPUs)

**Job (from cgroup)**

| metric | value |
|---|---:|
| CPU time used (s) | 59.79 |
| avg cores busy | 1.93 |
| share of busy CPU time on its socket(s) | 35.6% |
| peak memory (MB) | 95.6 |
| attributed package energy (J) | 1117.40 |
| attributed package power (W) | 36.04 |
| attributed DRAM energy (J) | 306.65 |

**Node (from RAPL)**

avg cores busy, all users: 5.42 on job socket(s), 6.27 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 3155.212 | 101.77 |
| package-0/dram | 866.570 | 27.95 |
| package-1 | 2725.549 | 87.92 |
| package-1/dram | 1010.386 | 32.59 |

### c3: 3 core(s) numpy (30s)

- host: `atl1-1-03-020-34-0.pace.gatech.edu`  cpu: Intel(R) Xeon(R) 6740P
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/ncores.py --procs 3 --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM673F56B00`  cpus: 20-27 on socket(s) [0]
- attribution scope: package-0 (48 CPUs)

**Job (from cgroup)**

| metric | value |
|---|---:|
| CPU time used (s) | 89.86 |
| avg cores busy | 2.90 |
| share of busy CPU time on its socket(s) | 47.9% |
| peak memory (MB) | 134.4 |
| attributed package energy (J) | 1535.84 |
| attributed package power (W) | 49.54 |
| attributed DRAM energy (J) | 412.05 |

**Node (from RAPL)**

avg cores busy, all users: 6.06 on job socket(s), 6.18 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 3225.853 | 104.05 |
| package-0/dram | 866.683 | 27.95 |
| package-1 | 2721.121 | 87.77 |
| package-1/dram | 1000.553 | 32.27 |

### c4: 4 core(s) numpy (30s)

- host: `atl1-1-03-020-34-0.pace.gatech.edu`  cpu: Intel(R) Xeon(R) 6740P
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/ncores.py --procs 4 --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM673F56B00`  cpus: 20-27 on socket(s) [0]
- attribution scope: package-0 (48 CPUs)

**Job (from cgroup)**

| metric | value |
|---|---:|
| CPU time used (s) | 119.67 |
| avg cores busy | 3.86 |
| share of busy CPU time on its socket(s) | 56.1% |
| peak memory (MB) | 174.0 |
| attributed package energy (J) | 1860.92 |
| attributed package power (W) | 60.02 |
| attributed DRAM energy (J) | 482.87 |

**Node (from RAPL)**

avg cores busy, all users: 6.88 on job socket(s), 6.92 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 3343.040 | 107.83 |
| package-0/dram | 869.082 | 28.03 |
| package-1 | 2672.776 | 86.21 |
| package-1/dram | 999.763 | 32.25 |

### c5: 5 core(s) numpy (30s)

- host: `atl1-1-03-020-34-0.pace.gatech.edu`  cpu: Intel(R) Xeon(R) 6740P
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/ncores.py --procs 5 --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM673F56B00`  cpus: 20-27 on socket(s) [0]
- attribution scope: package-0 (48 CPUs)

**Job (from cgroup)**

| metric | value |
|---|---:|
| CPU time used (s) | 149.70 |
| avg cores busy | 4.83 |
| share of busy CPU time on its socket(s) | 59.7% |
| peak memory (MB) | 213.2 |
| attributed package energy (J) | 2109.45 |
| attributed package power (W) | 68.04 |
| attributed DRAM energy (J) | 513.61 |

**Node (from RAPL)**

avg cores busy, all users: 8.09 on job socket(s), 8.73 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 3571.318 | 115.20 |
| package-0/dram | 869.426 | 28.04 |
| package-1 | 2709.515 | 87.40 |
| package-1/dram | 1006.252 | 32.46 |

### c6: 6 core(s) numpy (30s)

- host: `atl1-1-03-020-34-0.pace.gatech.edu`  cpu: Intel(R) Xeon(R) 6740P
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/ncores.py --procs 6 --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM673F56B00`  cpus: 20-27 on socket(s) [0]
- attribution scope: package-0 (48 CPUs)

**Job (from cgroup)**

| metric | value |
|---|---:|
| CPU time used (s) | 178.99 |
| avg cores busy | 5.77 |
| share of busy CPU time on its socket(s) | 63.9% |
| peak memory (MB) | 252.1 |
| attributed package energy (J) | 2390.63 |
| attributed package power (W) | 77.11 |
| attributed DRAM energy (J) | 549.73 |

**Node (from RAPL)**

avg cores busy, all users: 9.03 on job socket(s), 9.82 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 3777.783 | 121.86 |
| package-0/dram | 870.901 | 28.09 |
| package-1 | 2741.082 | 88.42 |
| package-1/dram | 1010.921 | 32.61 |

### c7: 7 core(s) numpy (30s)

- host: `atl1-1-03-020-34-0.pace.gatech.edu`  cpu: Intel(R) Xeon(R) 6740P
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/ncores.py --procs 7 --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM673F56B00`  cpus: 20-27 on socket(s) [0]
- attribution scope: package-0 (48 CPUs)

**Job (from cgroup)**

| metric | value |
|---|---:|
| CPU time used (s) | 209.38 |
| avg cores busy | 6.75 |
| share of busy CPU time on its socket(s) | 67.2% |
| peak memory (MB) | 291.9 |
| attributed package energy (J) | 2570.12 |
| attributed package power (W) | 82.90 |
| attributed DRAM energy (J) | 578.29 |

**Node (from RAPL)**

avg cores busy, all users: 10.05 on job socket(s), 10.78 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 3850.504 | 124.20 |
| package-0/dram | 869.630 | 28.05 |
| package-1 | 2710.968 | 87.44 |
| package-1/dram | 1006.193 | 32.45 |

### c8: 8 core(s) numpy (30s)

- host: `atl1-1-03-020-34-0.pace.gatech.edu`  cpu: Intel(R) Xeon(R) 6740P
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/ncores.py --procs 8 --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM673F56B00`  cpus: 20-27 on socket(s) [0]
- attribution scope: package-0 (48 CPUs)

**Job (from cgroup)**

| metric | value |
|---|---:|
| CPU time used (s) | 238.81 |
| avg cores busy | 7.70 |
| share of busy CPU time on its socket(s) | 71.2% |
| peak memory (MB) | 330.5 |
| attributed package energy (J) | 2837.60 |
| attributed package power (W) | 91.53 |
| attributed DRAM energy (J) | 612.65 |

**Node (from RAPL)**

avg cores busy, all users: 10.82 on job socket(s), 11.42 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 4021.423 | 129.71 |
| package-0/dram | 871.830 | 28.12 |
| package-1 | 2704.925 | 87.25 |
| package-1/dram | 1006.337 | 32.46 |
