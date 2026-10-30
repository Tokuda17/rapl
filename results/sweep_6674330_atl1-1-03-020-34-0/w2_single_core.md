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
