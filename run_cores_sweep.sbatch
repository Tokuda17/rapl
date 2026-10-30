#!/bin/bash
#SBATCH -J rapl-cores
#SBATCH -N 1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=8G
#SBATCH -t 00:20:00
#SBATCH -o slurm-%j.out
#
# Energy vs cores: idle baseline, then numpy on 1, 2, ..., SLURM_CPUS_PER_TASK
# processes, each measured with RAPL + cgroup. Results: results/cores_<jobid>_<node>/.
set -euo pipefail
cd "${SLURM_SUBMIT_DIR:-$(dirname "$0")}"

IDLE_S=${IDLE_S:-20}
LOAD_S=${LOAD_S:-30}
INTERVAL=${INTERVAL:-1}
MAXC=${SLURM_CPUS_PER_TASK:-8}

OUT=results/cores_${SLURM_JOB_ID}_$(hostname -s)
mkdir -p "$OUT"

echo "node: $(hostname)  job: $SLURM_JOB_ID  cpus: $MAXC  kernel: $(uname -r)"
lscpu | grep -E 'Model name|^CPU\(s\)|Socket|Thread' | tee "$OUT/lscpu.txt"
echo "cgroup: $(cat /proc/self/cgroup)"
python3 rapl_reader.py --list | tee "$OUT/domains.txt"
echo

python3 rapl_cgroup_reader.py --interval "$INTERVAL" --duration "$IDLE_S" --out "$OUT/w0_idle" --label "w0_idle: idle baseline (${IDLE_S}s)"
for n in $(seq 1 "$MAXC"); do
  echo; echo "================ $n core(s)"
  python3 rapl_cgroup_reader.py --interval "$INTERVAL" --out "$OUT/c${n}" --label "c${n}: ${n} core(s) numpy (${LOAD_S}s)" \
      -- python3 workloads/ncores.py --procs "$n" --seconds "$LOAD_S"
done

{
  echo "# RAPL + cgroup cores sweep: job $SLURM_JOB_ID on $(hostname)"
  echo
  echo "Collected $(date -u +%Y-%m-%dT%H:%M:%SZ) with \`run_cores_sweep.sbatch\` (${MAXC} CPUs allocated)."
  echo
  echo '```'; cat "$OUT/lscpu.txt"; echo '```'
  cat "$OUT/w0_idle.md"
  for n in $(seq 1 "$MAXC"); do echo; cat "$OUT/c${n}.md"; done
} > "$OUT/summary.md"
echo "wrote $OUT/summary.md"
