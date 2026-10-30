#!/bin/bash
#SBATCH -J rapl-read
#SBATCH -N 1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=8G
#SBATCH -t 00:10:00
#SBATCH -o slurm-%j.out
#
# Measures RAPL energy on an ICE compute node:
#   1. idle baseline for IDLE_S seconds
#   2. a CPU workload for LOAD_S seconds
# Results land in results/job_<jobid>_<node>/.
set -euo pipefail
cd "${SLURM_SUBMIT_DIR:-$(dirname "$0")}"

IDLE_S=${IDLE_S:-15}
LOAD_S=${LOAD_S:-30}
INTERVAL=${INTERVAL:-1}

OUT=results/job_${SLURM_JOB_ID}_$(hostname -s)
mkdir -p "$OUT"

echo "node: $(hostname)  job: $SLURM_JOB_ID  cpus: $SLURM_CPUS_PER_TASK"
echo "kernel: $(uname -r)"
lscpu | grep -E 'Model name|^CPU\(s\)|Socket' | tee "$OUT/lscpu.txt"
echo
echo "RAPL domains:"
python3 rapl_reader.py --list | tee "$OUT/domains.txt"
echo

python3 rapl_reader.py --interval "$INTERVAL" --duration "$IDLE_S" --out "$OUT/idle" --label "idle baseline (${IDLE_S}s)"
python3 rapl_reader.py --interval "$INTERVAL" --out "$OUT/load" --label "cpu workload (${SLURM_CPUS_PER_TASK} procs, ${LOAD_S}s)" \
    -- python3 workload.py --seconds "$LOAD_S" --procs "$SLURM_CPUS_PER_TASK"

{
  echo "# RAPL results: job $SLURM_JOB_ID on $(hostname)"
  echo
  echo "Collected $(date -u +%Y-%m-%dT%H:%M:%SZ) with \`run_rapl.sbatch\`."
  echo
  echo '```'
  cat "$OUT/lscpu.txt"
  echo '```'
  echo
  cat "$OUT/idle.md"
  echo
  cat "$OUT/load.md"
} > "$OUT/summary.md"
echo "wrote $OUT/summary.md"
