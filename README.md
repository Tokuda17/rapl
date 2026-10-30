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
