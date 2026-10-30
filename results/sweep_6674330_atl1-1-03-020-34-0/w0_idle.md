### w0_idle: idle baseline (20s)

- host: `atl1-1-03-020-34-0.pace.gatech.edu`  cpu: Intel(R) Xeon(R) 6740P
- duration: 20.00 s, samples: 22, interval: 1.0 s
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM671P7DM00`  cpus: 0-1,14-19 (sockets [0])

**Job (from cgroup)**

| metric | value |
|---|---:|
| CPU time used (s) | 0.01 |
| avg cores busy | 0.00 |
| share of node CPU time | 1.4% |
| peak memory (MB) | 12.0 |
| attributed package energy (J) | 64.38 |
| attributed package power (W) | 3.22 |
| attributed DRAM energy (J) | 22.32 |

**Node (from RAPL)**

node avg cores busy (all users): 0.04

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 1778.441 | 88.92 |
| package-0/dram | 556.563 | 27.83 |
| package-1 | 1691.016 | 84.54 |
| package-1/dram | 645.804 | 32.29 |
