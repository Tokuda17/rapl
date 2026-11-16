# RAPL + cgroup memory sweep: job 7123550 on atl1-1-03-007-25-2.pace.gatech.edu

Collected 2026-11-16T23:16:24Z with `run_memory_sweep.sbatch` (8 CPUs allocated).

```
CPU(s):                                  24
Model name:                              Intel(R) Xeon(R) Gold 6226 CPU @ 2.70GHz
Thread(s) per core:                      1
Socket(s):                               2
CPU(s) scaling MHz:                      72%
L2 cache:                                24 MiB (24 instances)
L3 cache:                                38.5 MiB (2 instances)
NUMA node(s):                            2
NUMA node0 CPU(s):                       0-11
NUMA node1 CPU(s):                       12-23
```
### w0_idle: idle baseline (20s)

- host: `atl1-1-03-007-25-2.pace.gatech.edu`  cpu: Intel(R) Xeon(R) Gold 6226 CPU @ 2.70GHz
- duration: 20.00 s, samples: 22, interval: 1.0 s
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM7KA0P7S00`  cpus: 0-23 on socket(s) [0, 1]
- attribution scope: package-0, package-1 (24 CPUs)

**Job (from cgroup and perf)**

| metric | value |
|---|---:|
| CPU time used (s) | 0.01 |
| avg cores busy | 0.00 |
| share of busy CPU time on its socket(s) | 0.5% |
| peak memory (MB) | 13.2 |
| page faults (major) | 9 (0) |
| peak anon memory by NUMA node (MB) | {'N0': 8.2, 'N1': 0.4} |
| attributed package energy (J) | 9.99 |
| attributed package power (W) | 0.50 |
| attributed DRAM energy by CPU share (J) | 0.44 |

**Node (from RAPL)**

avg cores busy, all users: 0.12 on job socket(s), 0.12 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 974.824 | 48.74 |
| package-0/dram | 59.739 | 2.99 |
| package-1 | 972.332 | 48.61 |
| package-1/dram | 25.540 | 1.28 |

### cpu8: 8 procs matmul, cache-resident (30s)

- host: `atl1-1-03-007-25-2.pace.gatech.edu`  cpu: Intel(R) Xeon(R) Gold 6226 CPU @ 2.70GHz
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/ncores.py --procs 8 --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM7KA0P7S00`  cpus: 0-23 on socket(s) [0, 1]
- attribution scope: package-0, package-1 (24 CPUs)
- perf counters: llc_load_misses, llc_misses, llc_store_misses (user mode, inherited by children)

**Job (from cgroup and perf)**

| metric | value |
|---|---:|
| CPU time used (s) | 240.00 |
| avg cores busy | 7.74 |
| share of busy CPU time on its socket(s) | 98.0% |
| peak memory (MB) | 330.0 |
| page faults (major) | 63701 (0) |
| peak anon memory by NUMA node (MB) | {'N0': 163.3, 'N1': 160.4} |
| LLC misses (perf) | 10,961,918,301 |
| est. DRAM traffic (misses x 64 B) | 701.56 GB, 22.63 GB/s |
| attributed package energy (J) | 4804.78 |
| attributed package power (W) | 154.98 |
| attributed DRAM energy by CPU share (J) | 299.73 |

**Node (from RAPL)**

avg cores busy, all users: 7.90 on job socket(s), 7.90 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 2458.660 | 79.31 |
| package-0/dram | 180.711 | 5.83 |
| package-1 | 2449.985 | 79.03 |
| package-1/dram | 125.418 | 4.04 |

### m1: 8 procs x 1 MB (30s)

- host: `atl1-1-03-007-25-2.pace.gatech.edu`  cpu: Intel(R) Xeon(R) Gold 6226 CPU @ 2.70GHz
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/memstream.py --procs 8 --mb 1 --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM7KA0P7S00`  cpus: 0-23 on socket(s) [0, 1]
- attribution scope: package-0, package-1 (24 CPUs)
- perf counters: llc_load_misses, llc_misses, llc_store_misses (user mode, inherited by children)

**Job (from cgroup and perf)**

| metric | value |
|---|---:|
| CPU time used (s) | 240.06 |
| avg cores busy | 7.74 |
| share of busy CPU time on its socket(s) | 98.3% |
| peak memory (MB) | 330.0 |
| page faults (major) | 41931 (0) |
| peak anon memory by NUMA node (MB) | {'N0': 75.1, 'N1': 72.0} |
| LLC misses (perf) | 2,509,720 |
| est. DRAM traffic (misses x 64 B) | 0.16 GB, 0.01 GB/s |
| attributed package energy (J) | 4171.95 |
| attributed package power (W) | 134.57 |
| attributed DRAM energy by CPU share (J) | 128.20 |

**Node (from RAPL)**

avg cores busy, all users: 7.88 on job socket(s), 7.88 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 2121.982 | 68.45 |
| package-0/dram | 92.298 | 2.98 |
| package-1 | 2129.560 | 68.69 |
| package-1/dram | 38.432 | 1.24 |

### m4: 8 procs x 4 MB (30s)

- host: `atl1-1-03-007-25-2.pace.gatech.edu`  cpu: Intel(R) Xeon(R) Gold 6226 CPU @ 2.70GHz
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/memstream.py --procs 8 --mb 4 --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM7KA0P7S00`  cpus: 0-23 on socket(s) [0, 1]
- attribution scope: package-0, package-1 (24 CPUs)
- perf counters: llc_load_misses, llc_misses, llc_store_misses (user mode, inherited by children)

**Job (from cgroup and perf)**

| metric | value |
|---|---:|
| CPU time used (s) | 239.60 |
| avg cores busy | 7.73 |
| share of busy CPU time on its socket(s) | 98.1% |
| peak memory (MB) | 330.0 |
| page faults (major) | 47831 (0) |
| peak anon memory by NUMA node (MB) | {'N0': 87.1, 'N1': 83.9} |
| LLC misses (perf) | 3,455,729,742 |
| est. DRAM traffic (misses x 64 B) | 221.17 GB, 7.13 GB/s |
| attributed package energy (J) | 4273.43 |
| attributed package power (W) | 137.84 |
| attributed DRAM energy by CPU share (J) | 200.11 |

**Node (from RAPL)**

avg cores busy, all users: 7.88 on job socket(s), 7.88 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 2169.735 | 69.99 |
| package-0/dram | 135.184 | 4.36 |
| package-1 | 2191.850 | 70.70 |
| package-1/dram | 69.051 | 2.23 |

### m16: 8 procs x 16 MB (30s)

- host: `atl1-1-03-007-25-2.pace.gatech.edu`  cpu: Intel(R) Xeon(R) Gold 6226 CPU @ 2.70GHz
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/memstream.py --procs 8 --mb 16 --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM7KA0P7S00`  cpus: 0-23 on socket(s) [0, 1]
- attribution scope: package-0, package-1 (24 CPUs)
- perf counters: llc_load_misses, llc_misses, llc_store_misses (user mode, inherited by children)

**Job (from cgroup and perf)**

| metric | value |
|---|---:|
| CPU time used (s) | 239.10 |
| avg cores busy | 7.71 |
| share of busy CPU time on its socket(s) | 97.8% |
| peak memory (MB) | 330.0 |
| page faults (major) | 50819 (0) |
| peak anon memory by NUMA node (MB) | {'N0': 135.1, 'N1': 132.0} |
| LLC misses (perf) | 33,891,693,559 |
| est. DRAM traffic (misses x 64 B) | 2169.07 GB, 69.97 GB/s |
| attributed package energy (J) | 4337.57 |
| attributed package power (W) | 139.91 |
| attributed DRAM energy by CPU share (J) | 556.90 |

**Node (from RAPL)**

avg cores busy, all users: 7.88 on job socket(s), 7.88 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 2219.304 | 71.59 |
| package-0/dram | 307.970 | 9.93 |
| package-1 | 2220.094 | 71.61 |
| package-1/dram | 261.613 | 8.44 |

### m64: 8 procs x 64 MB (30s)

- host: `atl1-1-03-007-25-2.pace.gatech.edu`  cpu: Intel(R) Xeon(R) Gold 6226 CPU @ 2.70GHz
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/memstream.py --procs 8 --mb 64 --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM7KA0P7S00`  cpus: 0-23 on socket(s) [0, 1]
- attribution scope: package-0, package-1 (24 CPUs)
- perf counters: llc_load_misses, llc_misses, llc_store_misses (user mode, inherited by children)

**Job (from cgroup and perf)**

| metric | value |
|---|---:|
| CPU time used (s) | 240.00 |
| avg cores busy | 7.74 |
| share of busy CPU time on its socket(s) | 98.2% |
| peak memory (MB) | 658.9 |
| page faults (major) | 50533 (0) |
| peak anon memory by NUMA node (MB) | {'N0': 316.9, 'N1': 334.2} |
| LLC misses (perf) | 38,778,796,909 |
| est. DRAM traffic (misses x 64 B) | 2481.84 GB, 80.06 GB/s |
| attributed package energy (J) | 4302.64 |
| attributed package power (W) | 138.79 |
| attributed DRAM energy by CPU share (J) | 592.00 |

**Node (from RAPL)**

avg cores busy, all users: 7.88 on job socket(s), 7.88 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 2196.178 | 70.84 |
| package-0/dram | 322.599 | 10.41 |
| package-1 | 2190.981 | 70.67 |
| package-1/dram | 280.456 | 9.05 |

### m256: 8 procs x 256 MB (30s)

- host: `atl1-1-03-007-25-2.pace.gatech.edu`  cpu: Intel(R) Xeon(R) Gold 6226 CPU @ 2.70GHz
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/memstream.py --procs 8 --mb 256 --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM7KA0P7S00`  cpus: 0-23 on socket(s) [0, 1]
- attribution scope: package-0, package-1 (24 CPUs)
- perf counters: llc_load_misses, llc_misses, llc_store_misses (user mode, inherited by children)

**Job (from cgroup and perf)**

| metric | value |
|---|---:|
| CPU time used (s) | 240.47 |
| avg cores busy | 7.76 |
| share of busy CPU time on its socket(s) | 97.2% |
| peak memory (MB) | 2197.8 |
| page faults (major) | 53439 (0) |
| peak anon memory by NUMA node (MB) | {'N0': 1095.1, 'N1': 1091.8} |
| LLC misses (perf) | 39,541,929,146 |
| est. DRAM traffic (misses x 64 B) | 2530.68 GB, 81.63 GB/s |
| attributed package energy (J) | 4292.63 |
| attributed package power (W) | 138.46 |
| attributed DRAM energy by CPU share (J) | 589.69 |

**Node (from RAPL)**

avg cores busy, all users: 7.98 on job socket(s), 7.98 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 2199.382 | 70.94 |
| package-0/dram | 323.428 | 10.43 |
| package-1 | 2231.681 | 71.99 |
| package-1/dram | 283.666 | 9.15 |

### m1024: 8 procs x 1024 MB (30s)

- host: `atl1-1-03-007-25-2.pace.gatech.edu`  cpu: Intel(R) Xeon(R) Gold 6226 CPU @ 2.70GHz
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/memstream.py --procs 8 --mb 1024 --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM7KA0P7S00`  cpus: 0-23 on socket(s) [0, 1]
- attribution scope: package-0, package-1 (24 CPUs)
- perf counters: llc_load_misses, llc_misses, llc_store_misses (user mode, inherited by children)

**Job (from cgroup and perf)**

| metric | value |
|---|---:|
| CPU time used (s) | 242.19 |
| avg cores busy | 7.81 |
| share of busy CPU time on its socket(s) | 93.3% |
| peak memory (MB) | 8353.3 |
| page faults (major) | 57229 (0) |
| peak anon memory by NUMA node (MB) | {'N0': 4166.8, 'N1': 4164.2} |
| LLC misses (perf) | 39,630,827,133 |
| est. DRAM traffic (misses x 64 B) | 2536.37 GB, 81.81 GB/s |
| attributed package energy (J) | 4161.82 |
| attributed package power (W) | 134.25 |
| attributed DRAM energy by CPU share (J) | 569.22 |

**Node (from RAPL)**

avg cores busy, all users: 8.38 on job socket(s), 8.38 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 2203.856 | 71.09 |
| package-0/dram | 325.637 | 10.50 |
| package-1 | 2262.234 | 72.97 |
| package-1/dram | 284.801 | 9.19 |

### p1: 1 procs x 1024 MB (30s)

- host: `atl1-1-03-007-25-2.pace.gatech.edu`  cpu: Intel(R) Xeon(R) Gold 6226 CPU @ 2.70GHz
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/memstream.py --procs 1 --mb 1024 --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM7KA0P7S00`  cpus: 0-23 on socket(s) [0, 1]
- attribution scope: package-0, package-1 (24 CPUs)
- perf counters: llc_load_misses, llc_misses, llc_store_misses (user mode, inherited by children)

**Job (from cgroup and perf)**

| metric | value |
|---|---:|
| CPU time used (s) | 30.30 |
| avg cores busy | 0.98 |
| share of busy CPU time on its socket(s) | 62.7% |
| peak memory (MB) | 8353.3 |
| page faults (major) | 10109 (0) |
| peak anon memory by NUMA node (MB) | {'N0': 7.0, 'N1': 1046.9} |
| LLC misses (perf) | 6,075,998,839 |
| est. DRAM traffic (misses x 64 B) | 388.86 GB, 12.54 GB/s |
| attributed package energy (J) | 2084.16 |
| attributed package power (W) | 67.23 |
| attributed DRAM energy by CPU share (J) | 144.90 |

**Node (from RAPL)**

avg cores busy, all users: 1.56 on job socket(s), 1.56 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 1550.256 | 50.01 |
| package-0/dram | 99.779 | 3.22 |
| package-1 | 1740.134 | 56.13 |
| package-1/dram | 128.582 | 4.15 |

### p2: 2 procs x 1024 MB (30s)

- host: `atl1-1-03-007-25-2.pace.gatech.edu`  cpu: Intel(R) Xeon(R) Gold 6226 CPU @ 2.70GHz
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/memstream.py --procs 2 --mb 1024 --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM7KA0P7S00`  cpus: 0-23 on socket(s) [0, 1]
- attribution scope: package-0, package-1 (24 CPUs)
- perf counters: llc_load_misses, llc_misses, llc_store_misses (user mode, inherited by children)

**Job (from cgroup and perf)**

| metric | value |
|---|---:|
| CPU time used (s) | 60.51 |
| avg cores busy | 1.95 |
| share of busy CPU time on its socket(s) | 70.2% |
| peak memory (MB) | 8353.3 |
| page faults (major) | 16838 (0) |
| peak anon memory by NUMA node (MB) | {'N0': 1039.8, 'N1': 1053.6} |
| LLC misses (perf) | 12,318,869,509 |
| est. DRAM traffic (misses x 64 B) | 788.41 GB, 25.43 GB/s |
| attributed package energy (J) | 2481.19 |
| attributed package power (W) | 80.03 |
| attributed DRAM energy by CPU share (J) | 225.87 |

**Node (from RAPL)**

avg cores busy, all users: 2.78 on job socket(s), 2.78 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 1737.541 | 56.05 |
| package-0/dram | 189.343 | 6.11 |
| package-1 | 1808.048 | 58.32 |
| package-1/dram | 132.507 | 4.27 |

### p4: 4 procs x 1024 MB (30s)

- host: `atl1-1-03-007-25-2.pace.gatech.edu`  cpu: Intel(R) Xeon(R) Gold 6226 CPU @ 2.70GHz
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/memstream.py --procs 4 --mb 1024 --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM7KA0P7S00`  cpus: 0-23 on socket(s) [0, 1]
- attribution scope: package-0, package-1 (24 CPUs)
- perf counters: llc_load_misses, llc_misses, llc_store_misses (user mode, inherited by children)

**Job (from cgroup and perf)**

| metric | value |
|---|---:|
| CPU time used (s) | 121.06 |
| avg cores busy | 3.90 |
| share of busy CPU time on its socket(s) | 82.9% |
| peak memory (MB) | 8353.3 |
| page faults (major) | 30280 (0) |
| peak anon memory by NUMA node (MB) | {'N0': 3125.1, 'N1': 1047.5} |
| LLC misses (perf) | 20,996,326,364 |
| est. DRAM traffic (misses x 64 B) | 1343.77 GB, 43.34 GB/s |
| attributed package energy (J) | 3233.44 |
| attributed package power (W) | 104.30 |
| attributed DRAM energy by CPU share (J) | 356.47 |

**Node (from RAPL)**

avg cores busy, all users: 4.71 on job socket(s), 4.71 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 2004.000 | 64.64 |
| package-0/dram | 301.360 | 9.72 |
| package-1 | 1901.571 | 61.34 |
| package-1/dram | 128.548 | 4.15 |

### p8: 8 procs x 1024 MB (30s)

- host: `atl1-1-03-007-25-2.pace.gatech.edu`  cpu: Intel(R) Xeon(R) Gold 6226 CPU @ 2.70GHz
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/memstream.py --procs 8 --mb 1024 --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM7KA0P7S00`  cpus: 0-23 on socket(s) [0, 1]
- attribution scope: package-0, package-1 (24 CPUs)
- perf counters: llc_load_misses, llc_misses, llc_store_misses (user mode, inherited by children)

**Job (from cgroup and perf)**

| metric | value |
|---|---:|
| CPU time used (s) | 242.21 |
| avg cores busy | 7.81 |
| share of busy CPU time on its socket(s) | 94.0% |
| peak memory (MB) | 8353.8 |
| page faults (major) | 57129 (0) |
| peak anon memory by NUMA node (MB) | {'N0': 4174.1, 'N1': 4156.8} |
| LLC misses (perf) | 39,671,840,212 |
| est. DRAM traffic (misses x 64 B) | 2539.00 GB, 81.90 GB/s |
| attributed package energy (J) | 4212.45 |
| attributed package power (W) | 135.88 |
| attributed DRAM energy by CPU share (J) | 575.81 |

**Node (from RAPL)**

avg cores busy, all users: 8.31 on job socket(s), 8.31 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 2229.923 | 71.93 |
| package-0/dram | 327.904 | 10.58 |
| package-1 | 2242.885 | 72.35 |
| package-1/dram | 283.260 | 9.14 |
