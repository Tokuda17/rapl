### w4_half_cores (30s)

- host: `atl1-1-03-020-34-0.pace.gatech.edu`  cpu: Intel(R) Xeon(R) 6740P
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/w4_half_cores.py --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM671ZWCK00`  cpus: 0-1,14-19 on socket(s) [0]
- attribution scope: package-0 (48 CPUs)

**Job (from cgroup)**

| metric | value |
|---|---:|
| CPU time used (s) | 119.78 |
| avg cores busy | 3.86 |
| share of busy CPU time on its socket(s) | 97.2% |
| peak memory (MB) | 174.4 |
| attributed package energy (J) | 3178.86 |
| attributed package power (W) | 102.54 |
| attributed DRAM energy (J) | 845.11 |

**Node (from RAPL)**

avg cores busy, all users: 3.98 on job socket(s), 4.06 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 3254.568 | 104.98 |
| package-0/dram | 865.170 | 27.91 |
| package-1 | 2627.172 | 84.74 |
| package-1/dram | 999.945 | 32.25 |
