### cpu8: 8 procs matmul, cache-resident (30s)

- host: `atl1-1-03-007-25-2.pace.gatech.edu`  cpu: Intel(R) Xeon(R) Gold 6226 CPU @ 2.70GHz
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workloads/ncores.py --procs 8 --seconds 30` (exit 0)
- cgroup: `/sys/fs/cgroup/system.slice/slurmstepd.scope/s8FXM7KA0P7S00`  cpus: 0-23 on socket(s) [0, 1]
- attribution scope: package-0, package-1 (24 CPUs)
- perf counters: llc_load_misses, llc_misses, llc_store_misses (user mode, inherited by children)

**Job (from cgroup and perf)**

| metric | value |
|---|---:|
| CPU time used (s) | 240.00 |
| avg cores busy | 7.74 |
| share of busy CPU time on its socket(s) | 98.0% |
| peak memory (MB) | 330.0 |
| page faults (major) | 63701 (0) |
| peak anon memory by NUMA node (MB) | {'N0': 163.3, 'N1': 160.4} |
| LLC misses (perf) | 10,961,918,301 |
| est. DRAM traffic (misses x 64 B) | 701.56 GB, 22.63 GB/s |
| attributed package energy (J) | 4804.78 |
| attributed package power (W) | 154.98 |
| attributed DRAM energy by CPU share (J) | 299.73 |

**Node (from RAPL)**

avg cores busy, all users: 7.90 on job socket(s), 7.90 whole node

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 2458.660 | 79.31 |
| package-0/dram | 180.711 | 5.83 |
| package-1 | 2449.985 | 79.03 |
| package-1/dram | 125.418 | 4.04 |
