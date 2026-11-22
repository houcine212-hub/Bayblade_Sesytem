"""Runs every analysis experiment quoted in DOC-BAL-001 (v0.4.1) and writes results/.
Usage:  python3 run_all.py            (about 1-3 minutes)
NOT game code - design-phase analysis only."""
import csv, itertools, json, math, os, platform, copy
import numpy as np
from combat_model import Model, FINISHES

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results")
TYPES = ["Attack", "Defense", "Stamina", "Balance"]
N = 4000

def load(name):
    with open(os.path.join(HERE, "configs", name)) as f:
        return json.load(f)

def scaled(b, f):
    c = dict(b)
    for k in ("atk", "def", "sta", "mag"):
        c[k] = min(100, b[k] * f)
    return c

def type_matrix(m, seed0):
    rows = []
    for i, (x, y) in enumerate(itertools.product(TYPES, TYPES)):
        r = m.duel(m.builds[x], m.builds[y], n=N, seed=seed0 + i)
        rows.append(dict(row=x, col=y, p_row_wins=r["win_a"], p_col_wins=r["win_b"], draw=r["draw"],
                         t_median_s=r["t_median"], **{f"share_{f}": r["finish"][f] for f in FINISHES}))
    # seat-averaged: P(t beats u) = mean(row t vs col u, col t vs row u)
    cell = {(r["row"], r["col"]): r for r in rows}
    pairs = []
    for x, y in itertools.combinations_with_replacement(TYPES, 2):
        r1, r2 = cell[(x, y)], cell[(y, x)]
        px = (r1["p_row_wins"] + r2["p_col_wins"]) / 2
        py = (r1["p_col_wins"] + r2["p_row_wins"]) / 2
        pairs.append(dict(type_x=x, type_y=y, p_x_wins=px, p_y_wins=py, draw=(r1["draw"] + r2["draw"]) / 2,
                          t_median_s=(r1["t_median_s"] + r2["t_median_s"]) / 2,
                          **{f"share_{f}": (r1[f"share_{f}"] + r2[f"share_{f}"]) / 2 for f in FINISHES}))
    overall = {}
    for t in TYPES:
        vals = []
        for p in pairs:
            if p["type_x"] == p["type_y"]:
                continue
            if p["type_x"] == t: vals.append(p["p_x_wins"] + 0.5 * p["draw"])
            if p["type_y"] == t: vals.append(p["p_y_wins"] + 0.5 * p["draw"])
        overall[t] = sum(vals) / len(vals)
    shares = {f: sum(r[f"share_{f}"] for r in rows) / len(rows) for f in FINISHES}
    meds = sorted(r["t_median_s"] for r in rows)
    return rows, pairs, overall, shares, float(np.median(meds))

def write_csv(path, rows):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

def main():
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        os.remove(os.path.join(OUT, f))
    summary = {"python": platform.python_version(), "numpy": np.__version__, "duels_per_cell": N,
               "primary_config": "v0.4.1-candidate (RPS = max(20, 10n), cap 35, 120 s)"}
    cand = Model(load("v0.4.1-candidate.json"))
    old = Model(load("v0.3.1-candidate.json"))
    ref = Model(load("v0.2-reference.json"))

    # E1 advantage table (scale-free: depends only on g and r)
    sc = [("S1", 60, 60, 350, 250), ("S2", 60, 60, 350, 320), ("S3", 66, 60, 300, 300), ("S4", 66, 60, 250, 350),
          ("S5", 78, 60, 250, 350), ("S6", 78, 60, 150, 350), ("S7", 54, 66, 350, 150), ("S8", 66, 60, 220, 350), ("S9", 80, 50, 100, 350)]
    e1 = []
    for sid, ea, eb, wa, wb in sc:
        g = cand.rel(ea, eb); r = cand.rel(wa, wb); w = float(cand.w_rps(g))
        et = (1 - w) * math.tanh(3 * g); rt = w * math.tanh(2.5 * r)
        e1.append(dict(id=sid, E_A=ea, E_B=eb, ratio=round(ea / eb, 4), g=round(g, 4), omega_A=wa, omega_B=wb,
                       r=round(r, 4), w=round(w, 4), energy_term=round(et, 4), rps_term=round(rt, 4), S=round(et + rt, 4)))
    write_csv(os.path.join(OUT, "e1_advantage_table.csv"), e1)

    # E2 type matrices
    for tag, m, seed in (("v0.4.1", cand, 101), ("v0.3.1-superseded", old, 101), ("v0.2-reference", ref, 11)):
        rows, pairs, overall, shares, med = type_matrix(m, seed)
        write_csv(os.path.join(OUT, f"e2_type_matrix_{tag}.csv"), rows)
        write_csv(os.path.join(OUT, f"e2_type_pairs_{tag}.csv"), pairs)
        summary[f"e2_{tag}"] = {"overall_vs_other_types": overall, "finish_shares": shares, "median_of_pairing_medians_s": med,
                                "min_pairing_median_s": min(r["t_median_s"] for r in rows), "max_pairing_median_s": max(r["t_median_s"] for r in rows),
                                "max_draw": max(r["draw"] for r in rows)}

    # E3 superseded D-17 wording (30-RPS difference), kept for the record
    e3 = []
    for arche in ("Attack", "Balance", "Stamina"):
        for f in (1.0, 1.05, 1.10, 1.15, 1.20, 1.30):
            a = scaled(cand.builds[arche], f); b = cand.builds[arche]
            p_eq = cand.duel(a, b, 350, 350, n=N, seed=3)["win_a"]
            p_lo = cand.duel(a, b, 320, 350, n=N, seed=4)["win_a"]
            p_hi = cand.duel(a, b, 350, 320, n=N, seed=5)["win_a"]
            ea, eb = cand.energy(a), cand.energy(b)
            e3.append(dict(mirror=arche, scale=f, E_A=round(ea, 2), E_B=round(eb, 2), g=round(cand.rel(ea, eb), 4),
                           p_equal_350=p_eq, p_A320_B350=p_lo, p_A350_B320=p_hi, rps_swing_pp=round(100 * (p_hi - p_lo), 1)))
    write_csv(os.path.join(OUT, "e3_rps_vs_energy.csv"), e3)
    # E3b D-17 AS AMENDED (v0.4.1, OQ-CB-12): 7-press = 70-RPS difference (280 vs 350, r = 0.222); includes the exact g = 0.20 boundary
    def f_for_g(b, target):
        lo, hi = 1.0, 2.0
        for _ in range(60):
            mid = (lo + hi) / 2
            if cand.rel(cand.energy(scaled(b, mid)), cand.energy(b)) < target: lo = mid
            else: hi = mid
        return (lo + hi) / 2
    e3b = []
    for arche in ("Attack", "Balance", "Stamina"):
        for f in sorted((1.0, 1.10, 1.15, round(f_for_g(cand.builds[arche], 0.20), 6), 1.20, 1.30)):  # rows ordered by g
            a = scaled(cand.builds[arche], f); b = cand.builds[arche]
            p_lo = cand.duel(a, b, 280, 350, n=N, seed=6)["win_a"]
            p_hi = cand.duel(a, b, 350, 280, n=N, seed=7)["win_a"]
            ea, eb = cand.energy(a), cand.energy(b)
            e3b.append(dict(mirror=arche, scale=f, g=round(cand.rel(ea, eb), 4), p_A280_B350=p_lo, p_A350_B280=p_hi,
                            rps_swing_pp=round(100 * (p_hi - p_lo), 1)))
    write_csv(os.path.join(OUT, "e3b_rps_vs_energy_relative.csv"), e3b)

    # E4 Magic weight (equal budget, skills NOT modelled)
    e4 = []
    base_b = cand.builds["Balance"]; shift = dict(base_b, atk=66, sta=66, mag=28); shift["def"] = 66
    base_a = cand.builds["Attack"]; himag = dict(base_a, atk=75, sta=35, mag=75); himag["def"] = 40
    for w in (0.0, 0.5, 0.8, 1.0):
        cand.c["w_mag"] = w
        r1 = cand.duel(shift, base_b, n=N, seed=14)
        r2 = cand.duel(himag, base_a, n=N, seed=9)
        e4.append(dict(w_mag=w, p_physical_shift_beats_balance=r1["win_a"], p_high_magic_beats_attack=r2["win_a"]))
    cand.c["w_mag"] = 1.0
    write_csv(os.path.join(OUT, "e4_magic_weight.csv"), e4)

    # E5 launch: zero/one-press paradox, low presses, FC-1 at the cap, alternative caps
    e5 = []
    def add(case, nmax, pa, pb, seed_a=12, seed_s=13):
        ra = cand.duel(cand.builds["Attack"], cand.builds["Attack"], presses_a=pa, presses_b=pb, n=N, seed=seed_a)
        rs = cand.duel(cand.builds["Stamina"], cand.builds["Stamina"], presses_a=pa, presses_b=pb, n=N, seed=seed_s)
        e5.append(dict(case=case, n_max=nmax, presses_a=pa, rps_a=float(cand.launch_rps(pa)), presses_b=pb, rps_b=float(cand.launch_rps(pb)),
                       p_a_attack_mirror=ra["win_a"], p_a_stamina_mirror=rs["win_a"]))
    add("zero_vs_one_press", 35, 0, 1, 31, 32)
    for p in (0, 1, 2, 3, 4, 5):
        add("low_press_vs_median", 35, p, 35, 31, 32)
    for human in (20, 25, 28, 30, 32, 35):
        add("capped_presser_vs_human", 35, 35, human)
    for nmax in (40, 50, 60):
        cand.c["n_max"] = nmax
        add("higher_cap_vs_median35", nmax, nmax, 35)
    cand.c["n_max"] = 35
    write_csv(os.path.join(OUT, "e5_launch.csv"), e5)

    # E6 TC-023: one contact from full lock, extreme inputs
    nvals = [1, 10, 1e3, 1e6]
    dmg = cand.single_contact_max_damage(nvals).tolist()
    summary["e6_tc023_single_contact_damage_cap"] = {"normalised_impacts": nvals, "max_damage": dmg,
                                                     "lock_after_one_contact_min": 100 - max(dmg), "crit_gate": cand.c["crit_gate"]}
    with open(os.path.join(OUT, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps({k: v for k, v in summary.items() if k.startswith("e2")}, indent=1))

if __name__ == "__main__":
    main()
