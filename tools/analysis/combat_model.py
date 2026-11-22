"""Design-analysis model for the Bayblade combat specifications (v0.4).

NOT game code. This script is a simplified 1-v-1 Monte Carlo model used only to
screen balance hypotheses during the design phase. It implements the canonical
equations of DOC-CMB-001 / DOC-BURST-001 / DOC-STAT-001 / DOC-LAUNCH-001 with
the analysis-only proxies listed in tools/analysis/README.md.

Requires: Python >= 3.10, numpy >= 2.0.
"""
from __future__ import annotations
import copy
import math
import numpy as np

FINISHES = ("BURST", "OVER", "SPIN", "TIME_LIMIT", "DRAW", "TIMEOUT")

# Profile matrix: (attacker, defender) -> (Pk knockback factor, Pb burst factor)
PROFILE = {
    ("SMASH", "SMASH"): (1.0, 1.0), ("SMASH", "UPPER"): (1.0, 1.0), ("SMASH", "ABSORB"): (0.85, 0.85), ("SMASH", "ROUND"): (1.1, 0.95),
    ("UPPER", "SMASH"): (0.85, 1.2), ("UPPER", "UPPER"): (0.9, 1.1), ("UPPER", "ABSORB"): (0.8, 1.0), ("UPPER", "ROUND"): (0.9, 1.25),
    ("ABSORB", "SMASH"): (0.8, 0.8), ("ABSORB", "UPPER"): (0.8, 0.8), ("ABSORB", "ABSORB"): (0.7, 0.7), ("ABSORB", "ROUND"): (0.8, 0.8),
    ("ROUND", "SMASH"): (0.9, 0.9), ("ROUND", "UPPER"): (0.9, 0.9), ("ROUND", "ABSORB"): (0.8, 0.8), ("ROUND", "ROUND"): (0.85, 0.85),
}
HEIGHT = {"LOW": 0, "MID": 1, "HIGH": 2}


class Model:
    def __init__(self, cfg: dict):
        self.c = dict(cfg["coefficients"])
        self.builds = copy.deepcopy(cfg["builds"])
        c = self.c
        c.setdefault("launch_model", "saturating")
        c.setdefault("omega_ref", c.get("rps_max", 150.0))
        c.setdefault("time_limit_rank", False)
        if c["launch_model"] == "saturating":
            c["k"] = -c["n_ref"] / math.log(1 - (c["rps_ref"] - c["rps_min"]) / (c["rps_max"] - c["rps_min"]))

    # ---------- launch / energy / advantage ----------
    def launch_rps(self, presses):
        """D-01/D-03 (v0.4): linear 10 RPS per counted press for n >= 1, zero presses = 20 RPS (exception).
        The v0.3.1 saturating curve is kept only to reproduce superseded comparison runs."""
        c = self.c
        n = np.minimum(np.asarray(presses, float), c["n_max"])
        if c["launch_model"] == "linear":
            return np.where(n <= 0, c["zero_press_rps"], c["rps_per_press"] * n)
        return c["rps_min"] + (c["rps_max"] - c["rps_min"]) * (1 - np.exp(-n / c["k"]))

    def energy(self, b, w_mag=None):
        w = self.c["w_mag"] if w_mag is None else w_mag
        return (b["atk"] + b["def"] + b["sta"] + w * b["mag"]) / (3 + w)

    @staticmethod
    def rel(a, b):
        return (a - b) / ((a + b) / 2)

    def w_rps(self, g):
        c = self.c
        return c["w_min"] + (c["w_max"] - c["w_min"]) * np.exp(-(np.asarray(g) / c["sigma"]) ** 2)

    def advantage(self, ea, eb, wa, wb):
        c = self.c
        g = self.rel(ea, eb)
        r = self.rel(np.maximum(wa, 1e-6), np.maximum(wb, 1e-6))
        w = self.w_rps(g)
        return (1 - w) * np.tanh(c["k_e"] * g) + w * np.tanh(c["k_r"] * r)

    def stab(self, w):
        return np.minimum(1.0, 0.45 + 0.55 * np.maximum(w, 0) / self.c["wobble"])

    # ---------- duel ----------
    def duel(self, a, b, rps_a=None, rps_b=None, n=4000, seed=1, presses_a=None, presses_b=None):
        c = self.c
        rng = np.random.default_rng(seed)

        def draw_launch(fixed_rps, fixed_presses):
            if fixed_rps is not None:
                return np.full(n, float(fixed_rps))
            if fixed_presses is not None:
                return np.full(n, float(self.launch_rps(fixed_presses)))
            p = np.clip(np.round(rng.normal(c["press_mu"], c["press_sd"], n)), 0, c["n_max"])
            return self.launch_rps(p)

        wa = draw_launch(rps_a, presses_a)
        wb = draw_launch(rps_b, presses_b)
        ea, eb = self.energy(a), self.energy(b)
        la = np.full(n, 100.0)
        lb = np.full(n, 100.0)
        alive = np.ones(n, bool)
        res = np.zeros(n, int)
        fin = np.full(n, "TIMEOUT", dtype=object)
        tend = np.full(n, c["t_max"])

        pk_ab, pb_ab = PROFILE[(a["prof"], b["prof"])]
        pk_ba, pb_ba = PROFILE[(b["prof"], a["prof"])]
        if a["prof"] == "UPPER" and HEIGHT[a["h"]] > HEIGHT[b["h"]]:
            pk_ab, pb_ab = PROFILE[("SMASH", b["prof"])]
        if b["prof"] == "UPPER" and HEIGHT[b["h"]] > HEIGHT[a["h"]]:
            pk_ba, pb_ba = PROFILE[("SMASH", a["prof"])]
        abs_a = 1.15 if a["prof"] == "ABSORB" else 1.0
        abs_b = 1.15 if b["prof"] == "ABSORB" else 1.0
        h = c["h0"] * (0.25 + 0.75 * (a["mob"] + b["mob"]) / 2)
        skill_a = np.clip(rng.normal(1.0, c["skill_sd"], n), 0.5, 1.5)
        skill_b = np.clip(rng.normal(1.0, c["skill_sd"], n), 0.5, 1.5)
        dt = c["dt"]
        t = 0.0
        while t < c["t_max"] - 1e-9 and alive.any():
            t += dt
            # contact events: debounce => at most one damaging event per pair per 100 ms step
            k = np.minimum(rng.poisson(h * dt, n), 1)
            u = rng.lognormal(-c["v_sig"] ** 2 / 2, c["v_sig"], n)
            # analysis proxy for normalised contact speed v_norm (in game: v_norm = clamp(v_n / v_ref, 0, v_norm_max) from physics)
            vna = np.clip(skill_a * u * (0.4 + 0.6 * a["mob"]), 0, c["v_norm_max"])
            vnb = np.clip(skill_b * u * (0.4 + 0.6 * b["mob"]), 0, c["v_norm_max"])
            s = self.advantage(ea, eb, wa, wb)
            ia = vna * (0.5 + a["atk"] / 100) * math.sqrt(a["mass"]) * pk_ab * (1 + c["alpha"] * s)
            ib = vnb * (0.5 + b["atk"] / 100) * math.sqrt(b["mass"]) * pk_ba * (1 - c["alpha"] * s)
            ra = (0.5 + a["def"] / 100) * math.sqrt(a["mass"]) * self.stab(wa) * abs_a
            rb = (0.5 + b["def"] / 100) * math.sqrt(b["mass"]) * self.stab(wb) * abs_b
            n_ab = ia / rb
            n_ba = ib / ra
            dec_a = c["c_d"] * (1.25 - a["sta"] / 100) * a.get("fric", 1.0) * (1 + c["c_move"] * a["mob"]) * dt
            dec_b = c["c_d"] * (1.25 - b["sta"] / 100) * b.get("fric", 1.0) * (1 + c["c_move"] * b["mob"]) * dt
            wa = np.where(alive, wa - (c["c_s"] * n_ba * (1 - a["sta"] / 250) * k + dec_a), wa)
            wb = np.where(alive, wb - (c["c_s"] * n_ab * (1 - b["sta"] / 250) * k + dec_b), wb)
            ta = c["t0"] * a["lock"] * (1 + c["beta"] * np.maximum(wa, 0) / c["omega_ref"])
            tb = c["t0"] * b["lock"] * (1 + c["beta"] * np.maximum(wb, 0) / c["omega_ref"])
            eps_a = 1 + rng.uniform(-c["eps"], c["eps"], n)
            eps_b = 1 + rng.uniform(-c["eps"], c["eps"], n)
            bload_a = n_ba * pb_ba          # burst load on A (A(theta) = 1 on average in this proxy)
            bload_b = n_ab * pb_ab
            la_start, lb_start = la.copy(), lb.copy()
            d_a = np.minimum(c["c_b"] * np.maximum(0, bload_a - ta) * eps_a, c["d_cap"]) * k
            d_b = np.minimum(c["c_b"] * np.maximum(0, bload_b - tb) * eps_b, c["d_cap"]) * k
            la = np.where(alive, la - d_a, la)
            lb = np.where(alive, lb - d_b, lb)
            crit_a = (k > 0) & (bload_a >= c["crit"] * ta) & (la_start <= c["crit_gate"])
            crit_b = (k > 0) & (bload_b >= c["crit"] * tb) & (lb_start <= c["crit_gate"])
            # ring-out hazard proxy incl. recoil (in game: OVER emerges from physics position)
            ka = a["mass"] * (0.6 + a["def"] / 100) * (1.3 - 0.5 * a["mob"]) * self.stab(wa)
            kb = b["mass"] * (0.6 + b["def"] / 100) * (1.3 - 0.5 * b["mob"]) * self.stab(wb)
            rec_a = c["rho_rec"] * (2.5 if b["prof"] == "ABSORB" else 1.0)
            rec_b = c["rho_rec"] * (2.5 if a["prof"] == "ABSORB" else 1.0)
            kn_a = n_ba + rec_a * n_ab * a["mob"]
            kn_b = n_ab + rec_b * n_ba * b["mob"]
            p_a = c["p_ko"] / (1 + np.exp(-(kn_a * c["ko_k"] - 1.6 * ka) / c["ko_s"]))
            p_b = c["p_ko"] / (1 + np.exp(-(kn_b * c["ko_k"] - 1.6 * kb) / c["ko_s"]))
            ko_a = rng.random(n) < p_a * k
            ko_b = rng.random(n) < p_b * k
            out_a = np.where((la <= 0) | crit_a, "BURST", np.where(ko_a, "OVER", np.where(wa < c["stop"], "SPIN", "")))
            out_b = np.where((lb <= 0) | crit_b, "BURST", np.where(ko_b, "OVER", np.where(wb < c["stop"], "SPIN", "")))
            da = alive & (out_a != "")
            db = alive & (out_b != "")
            both, only_a, only_b = da & db, da & ~db, db & ~da
            res[only_b], fin[only_b] = 1, out_b[only_b]
            res[only_a], fin[only_a] = -1, out_a[only_a]
            res[both], fin[both] = 0, "DRAW"
            tend[da | db] = t
            alive &= ~(da | db)
        if c["time_limit_rank"]:
            # D-16: at the time limit survivors are ranked by current spin; exact ties share placement (draw)
            hi_a = alive & (wa > wb); hi_b = alive & (wb > wa); tie = alive & (wa == wb)
            res[hi_a], fin[hi_a] = 1, "TIME_LIMIT"
            res[hi_b], fin[hi_b] = -1, "TIME_LIMIT"
            res[tie], fin[tie] = 0, "DRAW"
            alive[:] = False
        return {
            "win_a": float((res == 1).mean()), "win_b": float((res == -1).mean()), "draw": float((res == 0).mean()),
            "finish": {f: float((fin == f).mean()) for f in FINISHES},
            "t_median": float(np.median(tend)), "energy_a": float(ea), "energy_b": float(eb),
        }

    def single_contact_max_damage(self, n_values, lock=1.0, spin=None):
        """TC-023 helper: damage of one contact event for extreme normalised impacts."""
        c = self.c
        spin = c["omega_ref"] if spin is None else spin
        t = c["t0"] * lock * (1 + c["beta"] * spin / c["omega_ref"])
        d = np.minimum(c["c_b"] * np.maximum(0, np.asarray(n_values) * 1.25 * 1.5 - t) * (1 + c["eps"]), c["d_cap"])
        return d
