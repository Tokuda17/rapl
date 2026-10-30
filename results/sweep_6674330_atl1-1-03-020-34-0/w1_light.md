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
