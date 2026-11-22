"""S-5 summarizer (DOC-M1-001 steps 5.2-5.3). Design-analysis tool, not game code.

Reads the per-trial CSVs written by game/spikes/s5_launch_input (user://s5/*.csv),
recomputes accepted presses from the raw edges with the DOC-LAUNCH-001 rules
(independently of the Godot counter, as a cross-check), and prints median and
spread of accepted presses per input class plus NFR-073 (median launch RPS per
input class within 5%).

Usage: python3 tools/spikes/s5_summarize.py <dir-with-csvs>
"""
import csv, glob, os, statistics, sys

WINDOW_US, MIN_INTERVAL_US, CAP = 5_000_000, 142_857, 35


def rps(n):
    return max(20, 10 * min(max(n, 0), CAP))


def recount(rows):
    """Re-apply the counting rules to the down edges the client marked as valid edges in the zone."""
    n, last = 0, None
    for r in rows:
        if r["edge"] != "down" or r["verdict"] in ("NOT_EDGE", "OUTSIDE_ZONE"):
            continue
        t = int(r["t_us_from_w0"])
        if t < 0 or t >= WINDOW_US or n >= CAP or (last is not None and t - last < MIN_INTERVAL_US):
            continue
        n, last = n + 1, t
    return n


def main(d):
    trials = {}
    for f in sorted(glob.glob(os.path.join(d, "*.csv"))):
        with open(f, newline="") as fh:
            rows = list(csv.DictReader(fh))
        if not rows:
            continue
        n = recount(rows)
        client = max(int(r["accepted_count"]) for r in rows)
        if n != client:
            print(f"MISMATCH {os.path.basename(f)}: client {client}, recount {n}")
        trials.setdefault(rows[0]["input_class"], []).append((rows[0]["participant"], n))
    if not trials:
        print("no trial CSVs found"); return 1
    medians = {}
    print("input_class,trials,participants,median_presses,p10,p90,median_rps,share_at_cap")
    for cls, v in sorted(trials.items()):
        ns = sorted(n for _, n in v)
        q = statistics.quantiles(ns, n=10) if len(ns) >= 2 else [ns[0]] * 9
        medians[cls] = statistics.median(ns)
        print(f"{cls},{len(ns)},{len({p for p, _ in v})},{medians[cls]},{q[0]:.1f},{q[-1]:.1f},"
              f"{rps(int(medians[cls]))},{sum(n == CAP for n in ns) / len(ns):.2f}")
    r = [rps(int(m)) for m in medians.values()]
    spread = (max(r) - min(r)) / max(r) if max(r) else 0
    print(f"NFR-073 median launch RPS spread across input classes: {spread:.1%} -> {'PASS' if spread <= 0.05 else 'FAIL'}"
          " (valid only with >= 30 participants per class)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
