### w0_idle: idle baseline (20s)

- host: `atl1-1-03-020-34-0.pace.gatech.edu`  cpu: Intel(R) Xeon(R) 6740P
- duration: 20.00 s, samples: 22, interval: 1.0 s
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM671ZWCK00`  cpus: 0-1,14-19 on socket(s) [0]
- attribution scope: package-0 (48 CPUs)

**Job (from cgroup)**

| metric | value |
|---|---:|
| CPU time used (s) | 0.02 |
| avg cores busy | 0.00 |
| share of busy CPU time on its socket(s) | 0.4% |
| peak memory (MB) | 11.1 |
| attributed package energy (J) | 60.74 |
| attributed package power (W) | 3.04 |
| attributed DRAM energy (J) | 18.98 |

**Node (from RAPL)**

avg cores busy, all users: 0.27 on job socket(s), 0.45 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 1786.953 | 89.34 |
| package-0/dram | 557.202 | 27.86 |
| package-1 | 1692.039 | 84.59 |
| package-1/dram | 644.082 | 32.20 |
