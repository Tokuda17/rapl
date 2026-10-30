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
