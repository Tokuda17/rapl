# rapl

Read Intel RAPL (Running Average Power Limit) energy counters on a Linux node
and record them for a Slurm job on Georgia Tech's ICE cluster.

## Files

- `rapl_reader.py` - samples every RAPL domain in `/sys/class/powercap`
  (package, dram, ...) at a fixed interval, for a fixed duration or while a
  command runs. Handles counter wraparound. Writes `.csv`, `.json`, `.md`.
- `workload.py` - small CPU-bound workload so there is something to measure.
- `run_rapl.sbatch` - Slurm script: idle baseline, then the workload, both
  measured. Results go to `results/job_<jobid>_<node>/`.
- `results/` - collected data from real ICE runs.

## Usage on ICE

```bash
ssh mtokuda3@login-ice.pace.gatech.edu
git clone https://github.com/Tokuda17/rapl.git && cd rapl
sbatch run_rapl.sbatch          # defaults: 8 cpus, 15s idle, 30s load
squeue -u $USER
cat results/job_*/summary.md
```

Tunables are environment variables: `IDLE_S`, `LOAD_S`, `INTERVAL`, for example
`LOAD_S=120 sbatch --cpus-per-task=32 run_rapl.sbatch`.

## Standalone use

```bash
python3 rapl_reader.py --list                                  # show domains
python3 rapl_reader.py --duration 10 --interval 1 --out idle   # sample 10s
python3 rapl_reader.py --interval 0.5 --out run -- ./my_prog   # measure a command
```

## Notes

- RAPL counters are per socket. The job's node is shared unless you request
  `--exclusive`, so other users' jobs on the same node contribute to the numbers.
- Reading `energy_uj` needs read permission on the sysfs files. On ICE (RHEL 9,
  kernel 5.14) they are world-readable. On many desktop kernels they are root-only.

## Collected data: job 6673551 (2026-10-30)

Run on ICE node `atl1-1-02-003-19-1` (2x Intel Xeon Gold 6226, 24 cores, kernel 5.14, RHEL 9), partition coc-cpu, 8 CPUs allocated. Full data in [`results/job_6673551_atl1-1-02-003-19-1/`](results/job_6673551_atl1-1-02-003-19-1/).

RAPL domains found:

```
intel-rapl:0     package-0            max_energy_range_uj=262143328850  /sys/class/powercap/intel-rapl:0/energy_uj
intel-rapl:0:0   package-0/dram       max_energy_range_uj=65712999613  /sys/class/powercap/intel-rapl:0:0/energy_uj
intel-rapl:1     package-1            max_energy_range_uj=262143328850  /sys/class/powercap/intel-rapl:1/energy_uj
intel-rapl:1:0   package-1/dram       max_energy_range_uj=65712999613  /sys/class/powercap/intel-rapl:1:0/energy_uj
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
Per-second cumulative energy is in `results/job_6673551_atl1-1-02-003-19-1/idle.csv` and `results/job_6673551_atl1-1-02-003-19-1/load.csv`; the JSON files carry the same samples plus metadata. Note the node was shared with other jobs, so the baseline is not a true idle socket.

## Energy vs CPU usage sweep: job 6674363 (2026-10-30)

`run_sweep.sbatch` runs five workloads of increasing CPU intensity on one node, each for 30 s, with `rapl_cgroup_reader.py` recording RAPL energy and the job's cgroup accounting side by side. Slurm pinned the 8 allocated CPUs to socket 0, so package-1 is an untouched control. Node `atl1-1-03-020-34-0` (2x Intel Xeon 6740P, 96 cores) was otherwise nearly idle. Full data in [`results/sweep_6674363_atl1-1-03-020-34-0/`](results/sweep_6674363_atl1-1-03-020-34-0/); an earlier identical run is in [`results/sweep_6674330_atl1-1-03-020-34-0/`](results/sweep_6674330_atl1-1-03-020-34-0/) (its attribution columns use the older whole-node formula).

![Energy vs CPU usage](results/sweep_6674363_atl1-1-03-020-34-0/energy_vs_cpu.png)

| level | script | what it does |
|---|---|---|
| w0 | (none) | idle baseline, 20 s |
| w1 | `workloads/w1_light.py` | 1 process at a 20% duty cycle |
| w2 | `workloads/w2_single_core.py` | 1 process, pure-Python arithmetic loop |
| w3 | `workloads/w3_two_cores.py` | 2 processes, numpy matrix multiplies |
| w4 | `workloads/w4_half_cores.py` | 4 processes (half the allocation), numpy |
| w5 | `workloads/w5_all_cores.py` | 8 processes (full allocation), numpy |

| workload | job cores busy | socket cores busy (all users) | job share | package-0 W | package-1 W | dram-0 W | dram-1 W | attributed package J | attributed package W | peak mem MB |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| w0_idle | 0.00 | 0.27 | 0% | 89.3 | 84.6 | 27.9 | 32.2 | 61 | 3.0 | 11 |
| w1_light | 0.20 | 0.22 | 89% | 89.6 | 84.7 | 27.8 | 32.2 | 2451 | 79.1 | 19 |
| w2_single_core | 0.97 | 1.10 | 88% | 92.7 | 84.7 | 27.8 | 32.2 | 2690 | 86.8 | 19 |
| w3_two_cores | 1.93 | 1.98 | 98% | 96.9 | 84.7 | 27.8 | 32.2 | 2939 | 94.8 | 95 |
| w4_half_cores | 3.86 | 3.98 | 97% | 105.0 | 84.7 | 27.9 | 32.3 | 3179 | 102.5 | 174 |
| w5_all_cores | 7.72 | 7.80 | 99% | 117.5 | 84.9 | 28.2 | 32.3 | 3607 | 116.3 | 331 |

Reading the data:

- `job cores busy` comes from the cgroup's `cpu.stat` usage divided by wall time, and lands within a few percent of the intended 0.2, 1, 2, 4, 8 cores.
- Package-0 power rose from 89 W idle to 117 W with all 8 cores busy, about 3.6 W per busy core, while package-1 stayed at 85 W throughout.
- `attributed package W` is the job's share of busy CPU time on socket 0 times that socket's package power. The share model hands the job most of the socket's idle power as soon as it uses any CPU, which is why w1 jumps to 79 W for 0.2 cores of work. The marginal cost of the work itself is the rise above the 89 W idle line.
- DRAM power barely moved (27.8 to 28.2 W on socket 0): these workloads fit in cache.

To regenerate the plot and table locally (needs matplotlib): `python3 plot_sweep.py results/sweep_6674363_atl1-1-03-020-34-0`.
