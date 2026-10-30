#!/bin/bash
#SBATCH -J rapl-mem
#SBATCH -N 1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=24G
#SBATCH -t 00:25:00
#SBATCH -o slurm-%j.out
#
# Memory access vs power. Part A: 8 streaming processes, working set per
# process swept from cache-resident to DRAM-resident. Part B: DRAM-resident
# working set, process count swept. RAPL + cgroup recorded for each.
# Results: results/mem_<jobid>_<node>/.
set -euo pipefail
cd "${SLURM_SUBMIT_DIR:-$(dirname "$0")}"

IDLE_S=${IDLE_S:-20}
LOAD_S=${LOAD_S:-30}
INTERVAL=${INTERVAL:-1}
PROCS=${SLURM_CPUS_PER_TASK:-8}
SIZES_MB=${SIZES_MB:-"1 4 16 64 256 1024"}
BIG_MB=${BIG_MB:-1024}
PROC_COUNTS=${PROC_COUNTS:-"1 2 4 8"}

OUT=results/mem_${SLURM_JOB_ID}_$(hostname -s)
mkdir -p "$OUT"

echo "node: $(hostname)  job: $SLURM_JOB_ID  cpus: $PROCS  kernel: $(uname -r)"
lscpu | grep -E 'Model name|^CPU\(s\)|Socket|Thread|L2|L3|NUMA' | tee "$OUT/lscpu.txt"
echo "cgroup: $(cat /proc/self/cgroup)"
python3 rapl_reader.py --list | tee "$OUT/domains.txt"
echo

python3 rapl_cgroup_reader.py --interval "$INTERVAL" --duration "$IDLE_S" --out "$OUT/w0_idle" --label "w0_idle: idle baseline (${IDLE_S}s)"
for mb in $SIZES_MB; do
  echo; echo "================ working set ${mb} MB x ${PROCS} procs"
  python3 rapl_cgroup_reader.py --interval "$INTERVAL" --out "$OUT/m${mb}" --label "m${mb}: ${PROCS} procs x ${mb} MB (${LOAD_S}s)" \
      -- python3 workloads/memstream.py --procs "$PROCS" --mb "$mb" --seconds "$LOAD_S"
done
for n in $PROC_COUNTS; do
  echo; echo "================ ${n} procs x ${BIG_MB} MB"
  python3 rapl_cgroup_reader.py --interval "$INTERVAL" --out "$OUT/p${n}" --label "p${n}: ${n} procs x ${BIG_MB} MB (${LOAD_S}s)" \
      -- python3 workloads/memstream.py --procs "$n" --mb "$BIG_MB" --seconds "$LOAD_S"
done

{
  echo "# RAPL + cgroup memory sweep: job $SLURM_JOB_ID on $(hostname)"
  echo
  echo "Collected $(date -u +%Y-%m-%dT%H:%M:%SZ) with \`run_memory_sweep.sbatch\` (${PROCS} CPUs allocated)."
  echo
  echo '```'; cat "$OUT/lscpu.txt"; echo '```'
  cat "$OUT/w0_idle.md"
  for mb in $SIZES_MB; do echo; cat "$OUT/m${mb}.md"; done
  for n in $PROC_COUNTS; do echo; cat "$OUT/p${n}.md"; done
} > "$OUT/summary.md"
echo "wrote $OUT/summary.md"
