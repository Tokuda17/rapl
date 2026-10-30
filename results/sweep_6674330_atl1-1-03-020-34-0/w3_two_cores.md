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
