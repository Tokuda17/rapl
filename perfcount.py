#!/usr/bin/env python3
"""
perfcount.py - count hardware cache misses for a process tree with
perf_event_open, no perf binary required.

Opens last-level-cache miss counters on a pid with the inherit flag, so every
child the process spawns is counted too. Works for an unprivileged user on
kernels with perf_event_paranoid <= 2 as long as kernel mode is excluded.

    from perfcount import PerfCounters
    pc = PerfCounters(pid)         # pid should not have forked workers yet
    ...
    pc.read()  -> {"llc_misses": n, "llc_load_misses": n, "llc_store_misses": n}

`start_stopped(cmd)` launches a command that stops itself before exec, so the
counters can be attached before it runs anything; `cont(proc)` resumes it.

Standalone:  python3 perfcount.py -- ./my_prog args
"""
import ctypes
import os
import signal
import subprocess
import sys
import time

SYS_perf_event_open = 298            # x86_64
PERF_TYPE_HARDWARE = 0
PERF_TYPE_HW_CACHE = 3
PERF_COUNT_HW_CACHE_MISSES = 3       # architectural LLC misses (incl. core prefetch)
PERF_COUNT_HW_CACHE_LL = 2
PERF_COUNT_HW_CACHE_OP_READ = 0
PERF_COUNT_HW_CACHE_OP_WRITE = 1
PERF_COUNT_HW_CACHE_RESULT_MISS = 1
CACHE_LINE = 64

# attr flag bits
F_DISABLED, F_INHERIT, F_EXCLUDE_USER, F_EXCLUDE_KERNEL, F_EXCLUDE_HV = 1 << 0, 1 << 1, 1 << 4, 1 << 5, 1 << 6

EVENTS = {
    "llc_misses": (PERF_TYPE_HARDWARE, PERF_COUNT_HW_CACHE_MISSES),
    "llc_load_misses": (PERF_TYPE_HW_CACHE, PERF_COUNT_HW_CACHE_LL | (PERF_COUNT_HW_CACHE_OP_READ << 8) | (PERF_COUNT_HW_CACHE_RESULT_MISS << 16)),
    "llc_store_misses": (PERF_TYPE_HW_CACHE, PERF_COUNT_HW_CACHE_LL | (PERF_COUNT_HW_CACHE_OP_WRITE << 8) | (PERF_COUNT_HW_CACHE_RESULT_MISS << 16)),
}


class PerfEventAttr(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_uint32), ("size", ctypes.c_uint32), ("config", ctypes.c_uint64),
        ("sample_period", ctypes.c_uint64), ("sample_type", ctypes.c_uint64), ("read_format", ctypes.c_uint64),
        ("flags", ctypes.c_uint64), ("wakeup_events", ctypes.c_uint32), ("bp_type", ctypes.c_uint32),
        ("config1", ctypes.c_uint64), ("config2", ctypes.c_uint64), ("branch_sample_type", ctypes.c_uint64),
        ("sample_regs_user", ctypes.c_uint64), ("sample_stack_user", ctypes.c_uint32), ("clockid", ctypes.c_int32),
        ("sample_regs_intr", ctypes.c_uint64), ("aux_watermark", ctypes.c_uint32), ("sample_max_stack", ctypes.c_uint16),
        ("_r2", ctypes.c_uint16), ("aux_sample_size", ctypes.c_uint32), ("_r3", ctypes.c_uint32),
        ("sig_data", ctypes.c_uint64), ("config3", ctypes.c_uint64),
    ]


def perf_event_open(ev_type, config, pid, cpu=-1, inherit=True, exclude_kernel=True):
    libc = ctypes.CDLL(None, use_errno=True)
    attr = PerfEventAttr()
    attr.type = ev_type
    attr.size = ctypes.sizeof(PerfEventAttr)
    attr.config = config
    attr.flags = (F_INHERIT if inherit else 0) | (F_EXCLUDE_KERNEL | F_EXCLUDE_HV if exclude_kernel else 0)
    fd = libc.syscall(SYS_perf_event_open, ctypes.byref(attr), ctypes.c_int(pid), ctypes.c_int(cpu), ctypes.c_int(-1), ctypes.c_ulong(0))
    if fd < 0:
        err = ctypes.get_errno()
        raise OSError(err, f"perf_event_open({ev_type}, {config:#x}, pid={pid}): {os.strerror(err)}")
    return fd


class PerfCounters:
    """LLC miss counters on a process tree. Missing/unsupported events are skipped."""

    def __init__(self, pid, events=EVENTS):
        self.fds = {}
        self.errors = {}
        if sys.platform != "linux":
            self.errors["all"] = "not linux"
            return
        for name, (t, c) in events.items():
            try:
                self.fds[name] = perf_event_open(t, c, pid)
            except OSError as e:
                self.errors[name] = str(e)

    @property
    def ok(self):
        return "llc_misses" in self.fds

    def read(self):
        out = {}
        for name, fd in self.fds.items():
            try:
                out[name] = int.from_bytes(os.read(fd, 8), "little")
            except OSError:
                out[name] = None
        return out

    def close(self):
        for fd in self.fds.values():
            os.close(fd)
        self.fds = {}


def start_stopped(cmd, **popen_kw):
    """Launch cmd through a shell that stops itself before exec'ing cmd, so
    counters can be attached before the program runs. Call cont(proc) after.
    (Stopping inside Popen's preexec_fn would deadlock the parent, which waits
    for the exec to happen.) Without /proc, falls back to a plain Popen."""
    if not os.path.exists("/proc/self/stat"):
        return subprocess.Popen(cmd, **popen_kw)
    proc = subprocess.Popen(["/bin/sh", "-c", 'kill -STOP $$; exec "$@"', "sh", *cmd], **popen_kw)
    for _ in range(5000):                      # wait until the shell is stopped
        try:
            with open(f"/proc/{proc.pid}/stat") as f:
                state = f.read().rsplit(")", 1)[1].split()[0]
        except OSError:
            break
        if state in ("T", "t"):
            break
        time.sleep(0.001)
    return proc


def cont(proc):
    os.kill(proc.pid, signal.SIGCONT)


def main():
    args = sys.argv[1:]
    if args and args[0] == "--":
        args = args[1:]
    if not args:
        print(__doc__)
        return 2
    proc = start_stopped(args)
    pc = PerfCounters(proc.pid)
    if pc.errors:
        print("perfcount warnings:", pc.errors, file=sys.stderr)
    t0 = time.monotonic()
    cont(proc)
    rc = proc.wait()
    dt = time.monotonic() - t0
    c = pc.read()
    pc.close()
    m = c.get("llc_misses")
    print(f"exit {rc}, {dt:.2f}s, counters: {c}")
    if m is not None:
        print(f"LLC misses {m:,}  ->  {m * CACHE_LINE / 1e9:.3f} GB from DRAM (est.), {m * CACHE_LINE / 1e9 / dt:.2f} GB/s")
    return rc


if __name__ == "__main__":
    sys.exit(main())
