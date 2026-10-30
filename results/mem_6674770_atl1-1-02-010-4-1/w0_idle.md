### w0_idle: idle baseline (20s)

- host: `atl1-1-02-010-4-1.pace.gatech.edu`  cpu: Intel(R) Xeon(R) Gold 6226 CPU @ 2.70GHz
- duration: 20.00 s, samples: 22, interval: 1.0 s
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM674B5CX00`  cpus: 3-10 on socket(s) [0]
- attribution scope: package-0 (12 CPUs)

**Job (from cgroup)**

| metric | value |
|---|---:|
| CPU time used (s) | 0.01 |
| avg cores busy | 0.00 |
| share of busy CPU time on its socket(s) | 0.8% |
| peak memory (MB) | 9.9 |
| page faults (major) | 13 (0) |
| peak anon memory by NUMA node (MB) | {'N0': 7.7, 'N1': 0.1} |
| memory / cpu pressure, some (%) | None / None |
| attributed package energy (J) | 12.12 |
| attributed package power (W) | 0.61 |
| attributed DRAM energy (J) | 1.05 |

**Node (from RAPL)**

avg cores busy, all users: 0.06 on job socket(s), 0.07 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 1004.359 | 50.21 |
| package-0/dram | 86.593 | 4.33 |
| package-1 | 949.618 | 47.48 |
| package-1/dram | 72.394 | 3.62 |
