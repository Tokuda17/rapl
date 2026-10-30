### w5_all_cores (30s)

- host: `atl1-1-03-020-34-0.pace.gatech.edu`  cpu: Intel(R) Xeon(R) 6740P
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/w5_all_cores.py --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM671ZWCK00`  cpus: 0-1,14-19 on socket(s) [0]
- attribution scope: package-0 (48 CPUs)

**Job (from cgroup)**

| metric | value |
|---|---:|
| CPU time used (s) | 239.42 |
| avg cores busy | 7.72 |
| share of busy CPU time on its socket(s) | 99.1% |
| peak memory (MB) | 331.2 |
| attributed package energy (J) | 3607.07 |
| attributed package power (W) | 116.35 |
| attributed DRAM energy (J) | 864.55 |

**Node (from RAPL)**

avg cores busy, all users: 7.80 on job socket(s), 7.82 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 3642.503 | 117.49 |
| package-0/dram | 873.140 | 28.16 |
| package-1 | 2630.923 | 84.86 |
| package-1/dram | 1000.222 | 32.26 |
