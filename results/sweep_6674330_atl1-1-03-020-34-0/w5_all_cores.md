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
