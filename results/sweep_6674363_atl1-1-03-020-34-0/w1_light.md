### w1_light (30s)

- host: `atl1-1-03-020-34-0.pace.gatech.edu`  cpu: Intel(R) Xeon(R) 6740P
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/w1_light.py --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM671ZWCK00`  cpus: 0-1,14-19 on socket(s) [0]
- attribution scope: package-0 (48 CPUs)

**Job (from cgroup)**

| metric | value |
|---|---:|
| CPU time used (s) | 6.05 |
| avg cores busy | 0.20 |
| share of busy CPU time on its socket(s) | 89.4% |
| peak memory (MB) | 18.8 |
| attributed package energy (J) | 2451.45 |
| attributed package power (W) | 79.07 |
| attributed DRAM energy (J) | 761.28 |

**Node (from RAPL)**

avg cores busy, all users: 0.22 on job socket(s), 0.24 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 2777.410 | 89.59 |
| package-0/dram | 862.742 | 27.83 |
| package-1 | 2624.665 | 84.66 |
| package-1/dram | 997.858 | 32.19 |
