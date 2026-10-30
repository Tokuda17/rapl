# RAPL results: job 6673551 on atl1-1-02-003-19-1.pace.gatech.edu

Collected 2026-10-30T16:18:24Z with `run_rapl.sbatch`.

```
CPU(s):                                  24
Model name:                              Intel(R) Xeon(R) Gold 6226 CPU @ 2.70GHz
Socket(s):                               2
CPU(s) scaling MHz:                      68%
```

### RAPL summary: idle baseline (15s)

- host: `atl1-1-02-003-19-1.pace.gatech.edu`  cpu: Intel(R) Xeon(R) Gold 6226 CPU @ 2.70GHz
- duration: 15.00 s, samples: 17, interval: 1.0 s

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 708.397 | 47.22 |
| package-0/dram | 331.045 | 22.07 |
| package-1 | 777.245 | 51.81 |
| package-1/dram | 308.386 | 20.56 |

### RAPL summary: cpu workload (8 procs, 30s)

- host: `atl1-1-02-003-19-1.pace.gatech.edu`  cpu: Intel(R) Xeon(R) Gold 6226 CPU @ 2.70GHz
- duration: 31.00 s, samples: 33, interval: 1.0 s
- command: `python3 workload.py --seconds 30 --procs 8` (exit 0)

| domain | energy (J) | avg power (W) |
|---|---:|---:|
| package-0 | 1838.373 | 59.30 |
| package-0/dram | 697.724 | 22.51 |
| package-1 | 1740.829 | 56.15 |
| package-1/dram | 645.827 | 20.83 |
