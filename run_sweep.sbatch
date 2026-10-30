#!/bin/bash
#SBATCH -J rapl-sweep
#SBATCH -N 1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=8G
#SBATCH -t 00:15:00
#SBATCH -o slurm-%j.out
#
# Runs the 5-level CPU workload ladder, measuring RAPL energy and the job's
# cgroup CPU/memory accounting for each. Results: results/sweep_<jobid>_<node>/.
set -euo pipefail
cd "${SLURM_SUBMIT_DIR:-$(dirname "$0")}"

IDLE_S=${IDLE_S:-20}
LOAD_S=${LOAD_S:-30}
INTERVAL=${INTERVAL:-1}

OUT=results/sweep_${SLURM_JOB_ID}_$(hostname -s)
mkdir -p "$OUT"

echo "node: $(hostname)  job: $SLURM_JOB_ID  cpus: $SLURM_CPUS_PER_TASK  kernel: $(uname -r)"
lscpu | grep -E 'Model name|^CPU\(s\)|Socket|Thread' | tee "$OUT/lscpu.txt"
echo "cgroup: $(cat /proc/self/cgroup)"
python3 rapl_reader.py --list | tee "$OUT/domains.txt"
echo

python3 rapl_cgroup_reader.py --interval "$INTERVAL" --duration "$IDLE_S" --out "$OUT/w0_idle" --label "w0_idle: idle baseline (${IDLE_S}s)"
for w in w1_light w2_single_core w3_two_cores w4_half_cores w5_all_cores; do
  echo; echo "================ $w"
  python3 rapl_cgroup_reader.py --interval "$INTERVAL" --out "$OUT/$w" --label "$w (${LOAD_S}s)" \
      -- python3 "workloads/$w.py" --seconds "$LOAD_S"
done

{
  echo "# RAPL + cgroup sweep: job $SLURM_JOB_ID on $(hostname)"
  echo
  echo "Collected $(date -u +%Y-%m-%dT%H:%M:%SZ) with \`run_sweep.sbatch\` (${SLURM_CPUS_PER_TASK} CPUs allocated)."
  echo
  echo '```'; cat "$OUT/lscpu.txt"; echo '```'
  for f in "$OUT"/w*.md; do echo; cat "$f"; done
} > "$OUT/summary.md"
echo "wrote $OUT/summary.md"
