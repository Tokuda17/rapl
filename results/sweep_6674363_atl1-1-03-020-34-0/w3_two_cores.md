### w3_two_cores (30s)

- host: `atl1-1-03-020-34-0.pace.gatech.edu`  cpu: Intel(R) Xeon(R) 6740P
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/w3_two_cores.py --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM671ZWCK00`  cpus: 0-1,14-19 on socket(s) [0]
- attribution scope: package-0 (48 CPUs)

**Job (from cgroup)**

| metric | value |
|---|---:|
| CPU time used (s) | 59.93 |
| avg cores busy | 1.93 |
| share of busy CPU time on its socket(s) | 97.9% |
| peak memory (MB) | 95.4 |
| attributed package energy (J) | 2938.65 |
| attributed package power (W) | 94.79 |
| attributed DRAM energy (J) | 843.15 |

**Node (from RAPL)**

avg cores busy, all users: 1.98 on job socket(s), 2.00 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 3004.574 | 96.92 |
| package-0/dram | 862.150 | 27.81 |
| package-1 | 2625.583 | 84.69 |
| package-1/dram | 999.345 | 32.23 |
