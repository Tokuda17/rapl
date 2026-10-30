# RAPL + cgroup memory sweep: job 6674770 on atl1-1-02-010-4-1.pace.gatech.edu

Collected 2026-10-30T19:30:06Z with `run_memory_sweep.sbatch` (8 CPUs allocated).

```
CPU(s):                                  24
Model name:                              Intel(R) Xeon(R) Gold 6226 CPU @ 2.70GHz
Thread(s) per core:                      1
Socket(s):                               2
CPU(s) scaling MHz:                      70%
L2 cache:                                24 MiB (24 instances)
L3 cache:                                38.5 MiB (2 instances)
NUMA node(s):                            2
NUMA node0 CPU(s):                       0-11
NUMA node1 CPU(s):                       12-23
```
### w0_idle: idle baseline (20s)

- host: `atl1-1-02-010-4-1.pace.gatech.edu`  cpu: Intel(R) Xeon(R) Gold 6226 CPU @ 2.70GHz
- duration: 20.00 s, samples: 22, interval: 1.0 s
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM674B5CX00`  cpus: 3-10 on socket(s) [0]
- attribution scope: package-0 (12 CPUs)

**Job (from cgroup)**

| metric | value |
|---|---:|
| CPU time used (s) | 0.01 |
| avg cores busy | 0.00 |
| share of busy CPU time on its socket(s) | 0.8% |
| peak memory (MB) | 9.9 |
| page faults (major) | 13 (0) |
| peak anon memory by NUMA node (MB) | {'N0': 7.7, 'N1': 0.1} |
| memory / cpu pressure, some (%) | None / None |
| attributed package energy (J) | 12.12 |
| attributed package power (W) | 0.61 |
| attributed DRAM energy (J) | 1.05 |

**Node (from RAPL)**

avg cores busy, all users: 0.06 on job socket(s), 0.07 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 1004.359 | 50.21 |
| package-0/dram | 86.593 | 4.33 |
| package-1 | 949.618 | 47.48 |
| package-1/dram | 72.394 | 3.62 |

### m1: 8 procs x 1 MB (30s)

- host: `atl1-1-02-010-4-1.pace.gatech.edu`  cpu: Intel(R) Xeon(R) Gold 6226 CPU @ 2.70GHz
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/memstream.py --procs 8 --mb 1 --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM674B5CX00`  cpus: 3-10 on socket(s) [0]
- attribution scope: package-0 (12 CPUs)

**Job (from cgroup)**

| metric | value |
|---|---:|
| CPU time used (s) | 240.12 |
| avg cores busy | 7.75 |
| share of busy CPU time on its socket(s) | 99.6% |
| peak memory (MB) | 151.7 |
| page faults (major) | 41636 (0) |
| peak anon memory by NUMA node (MB) | {'N0': 146.4, 'N1': 0.1} |
| memory / cpu pressure, some (%) | None / None |
| attributed package energy (J) | 2763.33 |
| attributed package power (W) | 89.14 |
| attributed DRAM energy (J) | 134.23 |

**Node (from RAPL)**

avg cores busy, all users: 7.78 on job socket(s), 7.79 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 2774.936 | 89.51 |
| package-0/dram | 134.811 | 4.35 |
| package-1 | 1473.795 | 47.54 |
| package-1/dram | 111.327 | 3.59 |

### m4: 8 procs x 4 MB (30s)

- host: `atl1-1-02-010-4-1.pace.gatech.edu`  cpu: Intel(R) Xeon(R) Gold 6226 CPU @ 2.70GHz
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/memstream.py --procs 8 --mb 4 --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM674B5CX00`  cpus: 3-10 on socket(s) [0]
- attribution scope: package-0 (12 CPUs)

**Job (from cgroup)**

| metric | value |
|---|---:|
| CPU time used (s) | 239.00 |
| avg cores busy | 7.71 |
| share of busy CPU time on its socket(s) | 99.2% |
| peak memory (MB) | 176.4 |
| page faults (major) | 47442 (0) |
| peak anon memory by NUMA node (MB) | {'N0': 170.5, 'N1': 0.1} |
| memory / cpu pressure, some (%) | None / None |
| attributed package energy (J) | 2931.00 |
| attributed package power (W) | 94.54 |
| attributed DRAM energy (J) | 436.74 |

**Node (from RAPL)**

avg cores busy, all users: 7.77 on job socket(s), 7.77 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 2956.771 | 95.38 |
| package-0/dram | 440.436 | 14.21 |
| package-1 | 1450.987 | 46.80 |
| package-1/dram | 110.844 | 3.58 |

### m16: 8 procs x 16 MB (30s)

- host: `atl1-1-02-010-4-1.pace.gatech.edu`  cpu: Intel(R) Xeon(R) Gold 6226 CPU @ 2.70GHz
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/memstream.py --procs 8 --mb 16 --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM674B5CX00`  cpus: 3-10 on socket(s) [0]
- attribution scope: package-0 (12 CPUs)

**Job (from cgroup)**

| metric | value |
|---|---:|
| CPU time used (s) | 239.66 |
| avg cores busy | 7.73 |
| share of busy CPU time on its socket(s) | 99.5% |
| peak memory (MB) | 272.6 |
| page faults (major) | 50380 (0) |
| peak anon memory by NUMA node (MB) | {'N0': 266.5, 'N1': 0.1} |
| memory / cpu pressure, some (%) | None / None |
| attributed package energy (J) | 2814.62 |
| attributed package power (W) | 90.79 |
| attributed DRAM energy (J) | 514.97 |

**Node (from RAPL)**

avg cores busy, all users: 7.77 on job socket(s), 7.78 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 2831.254 | 91.33 |
| package-0/dram | 517.917 | 16.71 |
| package-1 | 1448.979 | 46.74 |
| package-1/dram | 111.631 | 3.60 |

### m64: 8 procs x 64 MB (30s)

- host: `atl1-1-02-010-4-1.pace.gatech.edu`  cpu: Intel(R) Xeon(R) Gold 6226 CPU @ 2.70GHz
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/memstream.py --procs 8 --mb 64 --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM674B5CX00`  cpus: 3-10 on socket(s) [0]
- attribution scope: package-0 (12 CPUs)

**Job (from cgroup)**

| metric | value |
|---|---:|
| CPU time used (s) | 240.08 |
| avg cores busy | 7.74 |
| share of busy CPU time on its socket(s) | 99.6% |
| peak memory (MB) | 657.5 |
| page faults (major) | 50229 (0) |
| peak anon memory by NUMA node (MB) | {'N0': 650.6, 'N1': 0.1} |
| memory / cpu pressure, some (%) | None / None |
| attributed package energy (J) | 2781.09 |
| attributed package power (W) | 89.71 |
| attributed DRAM energy (J) | 515.22 |

**Node (from RAPL)**

avg cores busy, all users: 7.78 on job socket(s), 7.80 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 2793.502 | 90.11 |
| package-0/dram | 517.470 | 16.69 |
| package-1 | 1448.410 | 46.72 |
| package-1/dram | 111.563 | 3.60 |

### m256: 8 procs x 256 MB (30s)

- host: `atl1-1-02-010-4-1.pace.gatech.edu`  cpu: Intel(R) Xeon(R) Gold 6226 CPU @ 2.70GHz
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/memstream.py --procs 8 --mb 256 --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM674B5CX00`  cpus: 3-10 on socket(s) [0]
- attribution scope: package-0 (12 CPUs)

**Job (from cgroup)**

| metric | value |
|---|---:|
| CPU time used (s) | 240.37 |
| avg cores busy | 7.75 |
| share of busy CPU time on its socket(s) | 95.5% |
| peak memory (MB) | 2196.0 |
| page faults (major) | 53024 (0) |
| peak anon memory by NUMA node (MB) | {'N0': 2186.2, 'N1': 0.1} |
| memory / cpu pressure, some (%) | None / None |
| attributed package energy (J) | 2734.93 |
| attributed package power (W) | 88.22 |
| attributed DRAM energy (J) | 497.77 |

**Node (from RAPL)**

avg cores busy, all users: 8.12 on job socket(s), 8.15 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 2854.744 | 92.08 |
| package-0/dram | 519.094 | 16.74 |
| package-1 | 1450.418 | 46.78 |
| package-1/dram | 111.562 | 3.60 |

### m1024: 8 procs x 1024 MB (30s)

- host: `atl1-1-02-010-4-1.pace.gatech.edu`  cpu: Intel(R) Xeon(R) Gold 6226 CPU @ 2.70GHz
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/memstream.py --procs 8 --mb 1024 --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM674B5CX00`  cpus: 3-10 on socket(s) [0]
- attribution scope: package-0 (12 CPUs)

**Job (from cgroup)**

| metric | value |
|---|---:|
| CPU time used (s) | 242.39 |
| avg cores busy | 7.82 |
| share of busy CPU time on its socket(s) | 99.5% |
| peak memory (MB) | 8351.6 |
| page faults (major) | 56845 (0) |
| peak anon memory by NUMA node (MB) | {'N0': 8330.3, 'N1': 0.1} |
| memory / cpu pressure, some (%) | None / None |
| attributed package energy (J) | 2810.74 |
| attributed package power (W) | 90.66 |
| attributed DRAM energy (J) | 518.69 |

**Node (from RAPL)**

avg cores busy, all users: 7.86 on job socket(s), 7.86 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 2824.274 | 91.10 |
| package-0/dram | 521.192 | 16.81 |
| package-1 | 1446.827 | 46.67 |
| package-1/dram | 111.634 | 3.60 |

### p1: 1 procs x 1024 MB (30s)

- host: `atl1-1-02-010-4-1.pace.gatech.edu`  cpu: Intel(R) Xeon(R) Gold 6226 CPU @ 2.70GHz
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/memstream.py --procs 1 --mb 1024 --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM674B5CX00`  cpus: 3-10 on socket(s) [0]
- attribution scope: package-0 (12 CPUs)

**Job (from cgroup)**

| metric | value |
|---|---:|
| CPU time used (s) | 30.30 |
| avg cores busy | 0.98 |
| share of busy CPU time on its socket(s) | 98.4% |
| peak memory (MB) | 8351.6 |
| page faults (major) | 9845 (0) |
| peak anon memory by NUMA node (MB) | {'N0': 1053.3, 'N1': 0.1} |
| memory / cpu pressure, some (%) | None / None |
| attributed package energy (J) | 1766.48 |
| attributed package power (W) | 56.98 |
| attributed DRAM energy (J) | 223.01 |

**Node (from RAPL)**

avg cores busy, all users: 0.99 on job socket(s), 1.22 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 1797.617 | 57.98 |
| package-0/dram | 226.856 | 7.32 |
| package-1 | 1463.014 | 47.19 |
| package-1/dram | 111.804 | 3.61 |

### p2: 2 procs x 1024 MB (30s)

- host: `atl1-1-02-010-4-1.pace.gatech.edu`  cpu: Intel(R) Xeon(R) Gold 6226 CPU @ 2.70GHz
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/memstream.py --procs 2 --mb 1024 --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM674B5CX00`  cpus: 3-10 on socket(s) [0]
- attribution scope: package-0 (12 CPUs)

**Job (from cgroup)**

| metric | value |
|---|---:|
| CPU time used (s) | 60.60 |
| avg cores busy | 1.96 |
| share of busy CPU time on its socket(s) | 99.3% |
| peak memory (MB) | 8351.6 |
| page faults (major) | 16571 (0) |
| peak anon memory by NUMA node (MB) | {'N0': 2092.9, 'N1': 0.1} |
| memory / cpu pressure, some (%) | None / None |
| attributed package energy (J) | 1966.39 |
| attributed package power (W) | 63.43 |
| attributed DRAM energy (J) | 293.24 |

**Node (from RAPL)**

avg cores busy, all users: 1.97 on job socket(s), 1.97 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 1979.945 | 63.87 |
| package-0/dram | 295.264 | 9.52 |
| package-1 | 1445.106 | 46.61 |
| package-1/dram | 111.578 | 3.60 |

### p4: 4 procs x 1024 MB (30s)

- host: `atl1-1-02-010-4-1.pace.gatech.edu`  cpu: Intel(R) Xeon(R) Gold 6226 CPU @ 2.70GHz
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/memstream.py --procs 4 --mb 1024 --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM674B5CX00`  cpus: 3-10 on socket(s) [0]
- attribution scope: package-0 (12 CPUs)

**Job (from cgroup)**

| metric | value |
|---|---:|
| CPU time used (s) | 121.31 |
| avg cores busy | 3.91 |
| share of busy CPU time on its socket(s) | 99.3% |
| peak memory (MB) | 8351.6 |
| page faults (major) | 30008 (0) |
| peak anon memory by NUMA node (MB) | {'N0': 4172.0, 'N1': 0.1} |
| memory / cpu pressure, some (%) | None / None |
| attributed package energy (J) | 2336.05 |
| attributed package power (W) | 75.35 |
| attributed DRAM energy (J) | 431.88 |

**Node (from RAPL)**

avg cores busy, all users: 3.94 on job socket(s), 3.95 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 2352.848 | 75.89 |
| package-0/dram | 434.972 | 14.03 |
| package-1 | 1445.329 | 46.62 |
| package-1/dram | 111.129 | 3.58 |

### p8: 8 procs x 1024 MB (30s)

- host: `atl1-1-02-010-4-1.pace.gatech.edu`  cpu: Intel(R) Xeon(R) Gold 6226 CPU @ 2.70GHz
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/memstream.py --procs 8 --mb 1024 --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM674B5CX00`  cpus: 3-10 on socket(s) [0]
- attribution scope: package-0 (12 CPUs)

**Job (from cgroup)**

| metric | value |
|---|---:|
| CPU time used (s) | 242.37 |
| avg cores busy | 7.82 |
| share of busy CPU time on its socket(s) | 99.4% |
| peak memory (MB) | 8352.2 |
| page faults (major) | 56849 (0) |
| peak anon memory by NUMA node (MB) | {'N0': 8330.3, 'N1': 0.1} |
| memory / cpu pressure, some (%) | None / None |
| attributed package energy (J) | 2816.45 |
| attributed package power (W) | 90.85 |
| attributed DRAM energy (J) | 516.85 |

**Node (from RAPL)**

avg cores busy, all users: 7.87 on job socket(s), 7.99 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 2833.395 | 91.39 |
| package-0/dram | 519.964 | 16.77 |
| package-1 | 1459.523 | 47.08 |
| package-1/dram | 111.500 | 3.60 |
