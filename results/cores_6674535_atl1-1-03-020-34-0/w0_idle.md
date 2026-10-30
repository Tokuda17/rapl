### w0_idle: idle baseline (20s)

- host: `atl1-1-03-020-34-0.pace.gatech.edu`  cpu: Intel(R) Xeon(R) 6740P
- duration: 20.00 s, samples: 22, interval: 1.0 s
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM673F56B00`  cpus: 20-27 on socket(s) [0]
- attribution scope: package-0 (48 CPUs)

**Job (from cgroup)**

| metric | value |
|---|---:|
| CPU time used (s) | 0.02 |
| avg cores busy | 0.00 |
| share of busy CPU time on its socket(s) | 0.0% |
| peak memory (MB) | 11.8 |
| attributed package energy (J) | 0.63 |
| attributed package power (W) | 0.03 |
| attributed DRAM energy (J) | 0.18 |

**Node (from RAPL)**

avg cores busy, all users: 3.06 on job socket(s), 5.10 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 1948.243 | 97.41 |
| package-0/dram | 557.438 | 27.87 |
| package-1 | 1849.770 | 92.48 |
| package-1/dram | 648.880 | 32.44 |
