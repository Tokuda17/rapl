### w2_single_core (30s)

- host: `atl1-1-03-020-34-0.pace.gatech.edu`  cpu: Intel(R) Xeon(R) 6740P
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/w2_single_core.py --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM671ZWCK00`  cpus: 0-1,14-19 on socket(s) [0]
- attribution scope: package-0 (48 CPUs)

**Job (from cgroup)**

| metric | value |
|---|---:|
| CPU time used (s) | 29.98 |
| avg cores busy | 0.97 |
| share of busy CPU time on its socket(s) | 87.9% |
| peak memory (MB) | 18.8 |
| attributed package energy (J) | 2689.86 |
| attributed package power (W) | 86.76 |
| attributed DRAM energy (J) | 807.95 |

**Node (from RAPL)**

avg cores busy, all users: 1.10 on job socket(s), 1.22 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 2872.969 | 92.67 |
| package-0/dram | 862.936 | 27.84 |
| package-1 | 2626.896 | 84.73 |
| package-1/dram | 998.581 | 32.21 |
