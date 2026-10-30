# RAPL + cgroup sweep: job 6674330 on atl1-1-03-020-34-0.pace.gatech.edu

Collected 2026-10-30T18:40:45Z with `run_sweep.sbatch` (8 CPUs allocated).

```
CPU(s):                                  96
Model name:                              Intel(R) Xeon(R) 6740P
Thread(s) per core:                      1
Socket(s):                               2
CPU(s) scaling MHz:                      48%
```

### w0_idle: idle baseline (20s)

- host: `atl1-1-03-020-34-0.pace.gatech.edu`  cpu: Intel(R) Xeon(R) 6740P
- duration: 20.00 s, samples: 22, interval: 1.0 s
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM671P7DM00`  cpus: 0-1,14-19 (sockets [0])

**Job (from cgroup)**

| metric | value |
|---|---:|
| CPU time used (s) | 0.01 |
| avg cores busy | 0.00 |
| share of node CPU time | 1.4% |
| peak memory (MB) | 12.0 |
| attributed package energy (J) | 64.38 |
| attributed package power (W) | 3.22 |
| attributed DRAM energy (J) | 22.32 |

**Node (from RAPL)**

node avg cores busy (all users): 0.04

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 1778.441 | 88.92 |
| package-0/dram | 556.563 | 27.83 |
| package-1 | 1691.016 | 84.54 |
| package-1/dram | 645.804 | 32.29 |

### w1_light (30s)

- host: `atl1-1-03-020-34-0.pace.gatech.edu`  cpu: Intel(R) Xeon(R) 6740P
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/w1_light.py --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM671P7DM00`  cpus: 0-1,14-19 (sockets [0])

**Job (from cgroup)**

| metric | value |
|---|---:|
| CPU time used (s) | 6.04 |
| avg cores busy | 0.20 |
| share of node CPU time | 81.9% |
| peak memory (MB) | 19.9 |
| attributed package energy (J) | 4360.63 |
| attributed package power (W) | 140.66 |
| attributed DRAM energy (J) | 1503.54 |

**Node (from RAPL)**

node avg cores busy (all users): 0.24

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 2778.006 | 89.61 |
| package-0/dram | 862.026 | 27.81 |
| package-1 | 2626.155 | 84.71 |
| package-1/dram | 1001.469 | 32.30 |

### w2_single_core (30s)

- host: `atl1-1-03-020-34-0.pace.gatech.edu`  cpu: Intel(R) Xeon(R) 6740P
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/w2_single_core.py --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM671P7DM00`  cpus: 0-1,14-19 (sockets [0])

**Job (from cgroup)**

| metric | value |
|---|---:|
| CPU time used (s) | 29.97 |
| avg cores busy | 0.97 |
| share of node CPU time | 77.5% |
| peak memory (MB) | 19.9 |
| attributed package energy (J) | 4970.72 |
| attributed package power (W) | 160.34 |
| attributed DRAM energy (J) | 1683.88 |

**Node (from RAPL)**

node avg cores busy (all users): 1.25

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 2875.442 | 92.75 |
| package-0/dram | 863.029 | 27.84 |
| package-1 | 2627.628 | 84.76 |
| package-1/dram | 1001.068 | 32.29 |

### w3_two_cores (30s)

- host: `atl1-1-03-020-34-0.pace.gatech.edu`  cpu: Intel(R) Xeon(R) 6740P
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/w3_two_cores.py --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM671P7DM00`  cpus: 0-1,14-19 (sockets [0])

**Job (from cgroup)**

| metric | value |
|---|---:|
| CPU time used (s) | 59.92 |
| avg cores busy | 1.93 |
| share of node CPU time | 87.7% |
| peak memory (MB) | 95.4 |
| attributed package energy (J) | 5226.42 |
| attributed package power (W) | 168.59 |
| attributed DRAM energy (J) | 1727.81 |

**Node (from RAPL)**

node avg cores busy (all users): 2.20

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 3012.687 | 97.18 |
| package-0/dram | 862.711 | 27.83 |
| package-1 | 2627.963 | 84.77 |
| package-1/dram | 1001.813 | 32.31 |

### w4_half_cores (30s)

- host: `atl1-1-03-020-34-0.pace.gatech.edu`  cpu: Intel(R) Xeon(R) 6740P
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/w4_half_cores.py --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM671P7DM00`  cpus: 0-1,14-19 (sockets [0])

**Job (from cgroup)**

| metric | value |
|---|---:|
| CPU time used (s) | 119.78 |
| avg cores busy | 3.86 |
| share of node CPU time | 97.6% |
| peak memory (MB) | 174.2 |
| attributed package energy (J) | 5741.20 |
| attributed package power (W) | 185.19 |
| attributed DRAM energy (J) | 1820.76 |

**Node (from RAPL)**

node avg cores busy (all users): 3.96

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 3256.031 | 105.03 |
| package-0/dram | 865.654 | 27.92 |
| package-1 | 2628.317 | 84.78 |
| package-1/dram | 1000.684 | 32.28 |

### w5_all_cores (30s)

- host: `atl1-1-03-020-34-0.pace.gatech.edu`  cpu: Intel(R) Xeon(R) 6740P
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/w5_all_cores.py --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM671P7DM00`  cpus: 0-1,14-19 (sockets [0])

**Job (from cgroup)**

| metric | value |
|---|---:|
| CPU time used (s) | 239.41 |
| avg cores busy | 7.72 |
| share of node CPU time | 97.0% |
| peak memory (MB) | 330.9 |
| attributed package energy (J) | 6134.96 |
| attributed package power (W) | 197.89 |
| attributed DRAM energy (J) | 1832.14 |

**Node (from RAPL)**

node avg cores busy (all users): 7.96

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 3657.305 | 117.97 |
| package-0/dram | 879.678 | 28.38 |
| package-1 | 2634.490 | 84.98 |
| package-1/dram | 998.995 | 32.22 |
