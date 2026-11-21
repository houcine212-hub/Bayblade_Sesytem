"""Runs every analysis experiment quoted in DOC-BAL-001 and writes results/.
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
    summary = {"python": platform.python_version(), "numpy": np.__version__, "duels_per_cell": N}
    cand = Model(load("v0.3.1-candidate.json"))
    ref = Model(load("v0.2-reference.json"))

    # E1 advantage table
    sc = [("S1", 60, 60, 120, 80), ("S2", 60, 60, 100, 95), ("S3", 66, 60, 100, 100), ("S4", 66, 60, 80, 120),
          ("S5", 78, 60, 80, 120), ("S6", 78, 60, 60, 140), ("S7", 54, 66, 140, 60), ("S8", 66, 60, 70, 110), ("S9", 80, 50, 50, 150)]
    e1 = []
    for sid, ea, eb, wa, wb in sc:
        g = cand.rel(ea, eb); r = cand.rel(wa, wb); w = float(cand.w_rps(g))
        et = (1 - w) * math.tanh(3 * g); rt = w * math.tanh(2.5 * r)
        e1.append(dict(id=sid, E_A=ea, E_B=eb, ratio=round(ea / eb, 4), g=round(g, 4), omega_A=wa, omega_B=wb,
                       r=round(r, 4), w=round(w, 4), energy_term=round(et, 4), rps_term=round(rt, 4), S=round(et + rt, 4)))
    write_csv(os.path.join(OUT, "e1_advantage_table.csv"), e1)

    # E2 type matrices
    for tag, m, seed in (("v0.3.1", cand, 101), ("v0.2-reference", ref, 11)):
        rows, pairs, overall, shares, med = type_matrix(m, seed)
        write_csv(os.path.join(OUT, f"e2_type_matrix_{tag}.csv"), rows)
        write_csv(os.path.join(OUT, f"e2_type_pairs_{tag}.csv"), pairs)
        summary[f"e2_{tag}"] = {"overall_vs_other_types": overall, "finish_shares": shares, "median_of_pairing_medians_s": med,
                                "min_pairing_median_s": min(r["t_median_s"] for r in rows), "max_pairing_median_s": max(r["t_median_s"] for r in rows),
                                "max_draw": max(r["draw"] for r in rows)}

    # E3 RPS influence vs Energy gap (outcome level)
    e3 = []
    for arche in ("Attack", "Balance"):
        for f in (1.0, 1.05, 1.10, 1.15, 1.20, 1.30):
            a = scaled(cand.builds[arche], f); b = cand.builds[arche]
            p_eq = cand.duel(a, b, 120, 120, n=N, seed=3)["win_a"]
            p_lo = cand.duel(a, b, 120, 150, n=N, seed=4)["win_a"]
            p_hi = cand.duel(a, b, 150, 120, n=N, seed=5)["win_a"]
            ea, eb = cand.energy(a), cand.energy(b)
            e3.append(dict(mirror=arche, scale=f, E_A=round(ea, 2), E_B=round(eb, 2), g=round(cand.rel(ea, eb), 4),
                           p_equal_rps=p_eq, p_A120_B150=p_lo, p_A150_B120=p_hi, rps_swing_pp=round(100 * (p_hi - p_lo), 1)))
    write_csv(os.path.join(OUT, "e3_rps_vs_energy.csv"), e3)

    # E4 Magic weight (equal budget, skills NOT modelled)
    e4 = []
    base_b = cand.builds["Balance"]; shift = dict(base_b, atk=66, sta=66, mag=28); shift["def"] = 66
    base_a = cand.builds["Attack"]; himag = dict(base_a, atk=75, sta=35, mag=75); himag["def"] = 40
    for w in (0.0, 0.3, 0.5, 0.6, 0.7, 0.8, 1.0):
        cand.c["w_mag"] = w
        r1 = cand.duel(shift, base_b, n=N, seed=14)
        r2 = cand.duel(himag, base_a, n=N, seed=9)
        e4.append(dict(w_mag=w, p_physical_shift_beats_balance=r1["win_a"], p_high_magic_beats_attack=r2["win_a"]))
    cand.c["w_mag"] = 1.0
    write_csv(os.path.join(OUT, "e4_magic_weight.csv"), e4)

    # E5 launch: zero/low presses, capped presser, cap options
    e5 = []
    for p in (0, 1, 3, 5):
        ra = cand.duel(cand.builds["Attack"], cand.builds["Attack"], presses_a=p, presses_b=35, n=N, seed=31)
        rs = cand.duel(cand.builds["Stamina"], cand.builds["Stamina"], presses_a=p, presses_b=35, n=N, seed=32)
        e5.append(dict(case="low_press_vs_35", n_max=60, presses_a=p, presses_b=35, p_a_attack_mirror=ra["win_a"], p_a_stamina_mirror=rs["win_a"]))
    for nmax in (60, 50, 40, 35):
        cand.c["n_max"] = nmax
        for human in (25, 30, 35, 45):
            if human > nmax:
                continue
            ra = cand.duel(cand.builds["Attack"], cand.builds["Attack"], presses_a=nmax, presses_b=human, n=N, seed=12)
            rs = cand.duel(cand.builds["Stamina"], cand.builds["Stamina"], presses_a=nmax, presses_b=human, n=N, seed=13)
            e5.append(dict(case="capped_presser_vs_human", n_max=nmax, presses_a=nmax, presses_b=human,
                           p_a_attack_mirror=ra["win_a"], p_a_stamina_mirror=rs["win_a"]))
    cand.c["n_max"] = 60
    write_csv(os.path.join(OUT, "e5_launch.csv"), e5)

    # E6 TC-023: one contact from full lock, extreme inputs
    nvals = [1, 10, 1e3, 1e6]
    dmg = cand.single_contact_max_damage(nvals).tolist()
    summary["e6_tc023_single_contact_damage_cap"] = {"normalised_impacts": nvals, "max_damage": dmg,
                                                     "lock_after_one_contact_min": 100 - max(dmg), "crit_gate": cand.c["crit_gate"]}
    with open(os.path.join(OUT, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
