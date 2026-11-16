### w0_idle: idle baseline (20s)

- host: `atl1-1-03-007-25-2.pace.gatech.edu`  cpu: Intel(R) Xeon(R) Gold 6226 CPU @ 2.70GHz
- duration: 20.00 s, samples: 22, interval: 1.0 s
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM7KA0P7S00`  cpus: 0-23 on socket(s) [0, 1]
- attribution scope: package-0, package-1 (24 CPUs)

**Job (from cgroup and perf)**

| metric | value |
|---|---:|
| CPU time used (s) | 0.01 |
| avg cores busy | 0.00 |
| share of busy CPU time on its socket(s) | 0.5% |
| peak memory (MB) | 13.2 |
| page faults (major) | 9 (0) |
| peak anon memory by NUMA node (MB) | {'N0': 8.2, 'N1': 0.4} |
| attributed package energy (J) | 9.99 |
| attributed package power (W) | 0.50 |
| attributed DRAM energy by CPU share (J) | 0.44 |

**Node (from RAPL)**

avg cores busy, all users: 0.12 on job socket(s), 0.12 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 974.824 | 48.74 |
| package-0/dram | 59.739 | 2.99 |
| package-1 | 972.332 | 48.61 |
| package-1/dram | 25.540 | 1.28 |
