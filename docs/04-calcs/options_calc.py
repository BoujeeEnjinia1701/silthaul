"""SiltHaul first-order numbers for the concept options (SLH-OPT-001, SLH-STM-001).

Run from the repo root:  python docs/04-calcs/options_calc.py
Option A is the existing design and its numbers come from sizing.py (SLH-CAL-001). Options B (crew-hauled box)
and C (hand slurry pump) are first-order screens with the assumptions listed below; they are estimates to be
measured at TRL 4, not calculation notes. Importing this file builds the model once (about a minute).
"""
import io
import math
import contextlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "docs" / "04-calcs"), str(ROOT / "cad" / "src"), str(ROOT / ".kit")]
with contextlib.redirect_stdout(io.StringIO()):
    import sizing as CAL  # noqa: E402  SLH-CAL-001, builds option A
import model as M  # noqa: E402
import cad_parts as cp  # noqa: E402

g = 9.81
A = CAL.A
P = M.PARAMS
OUT = []


def say(tag, text):
    OUT.append(f"[{tag}] {text}")


# ------------------------------------------------------------------ assumptions (estimates)
H_SPEED = 0.4          # m/s, rope speed hauling hand over hand from the staked foot boards (range 0.3 to 0.5)
RET_SPEED = 0.9        # m/s, one or two people pulling the empty box back on the tag line
N_HAUL = 4             # people on the pull rope
MU_BOOT_MUD = 0.25     # boot on wet mud, no foot board (estimate, to measure at TRL 4)
M_PERSON = 70.0        # kg
PHI_MUD = (A["rho_mud"] - 1.0) / 1.65       # solid volume fraction of flood mud, solids 2650 kg/m3
PHI_SLURRY = 0.15      # solid volume fraction the pump can move (estimate, to measure on real mud)
TAU_Y = 30.0           # Pa, yield stress of the slurry at that fraction (estimate)
MU_P = 0.05            # Pa s, plastic viscosity (estimate)
HOSE_D = P["pump"]["hose_d"] / 1000.0
HOSE_L = 4.0 + 15.0    # m, suction plus delivery hose in the design case
STATIC_H = 1.0         # m, delivery lift to the dump point
ETA_PUMP = 0.6
D_EFF = 0.25           # m, effective diaphragm diameter (clamp discs inside the 250 mm cavity bore)
STROKE = P["pump"]["stroke_chamber"] / 1000.0      # m, diaphragm centre travel peak to peak
EL_RATIO = 1.4 / 0.22  # rocker handle length over chamber offset: handle travel per metre of diaphragm travel
SPM = 40.0             # strokes a minute (one stroke is one half cycle of the rocker)
VOL_EFF = 0.7          # valve slip and air in the suction

# ------------------------------------------------------------------ option B: crew-hauled box
F_haul, F_back = CAL.F_haul, CAL.F_back
F_each = F_haul / N_HAUL
t_haul = A["haul_m"] / H_SPEED / 60
t_ret = A["haul_m"] / RET_SPEED / 60
t_cycle_b = A["fill_min"] + t_haul + A["dump_min"] + t_ret
q_b = 60 / t_cycle_b * CAL.V_rated / 1000 * A["work_rest"]
P_haul_each = F_haul * H_SPEED / N_HAUL
duty = t_haul / t_cycle_b
mu_needed = F_each / (M_PERSON * g)
F_jam = N_HAUL * 400.0
say("B1", f"Full box haul {F_haul:.0f} N over {A['haul_m']:.0f} m: {F_each:.0f} N each with {N_HAUL} people at {H_SPEED} m/s")
say("B2", f"Mechanical power {P_haul_each:.0f} W each while hauling, duty {duty * 100:.0f} %; boot traction needed mu {mu_needed:.2f} against {MU_BOOT_MUD} on wet mud")
say("B3", f"Cycle {t_cycle_b:.2f} min (fill {A['fill_min']}, haul {t_haul:.2f}, dump {A['dump_min']}, return {t_ret:.2f}); output {q_b:.2f} m3/h with rest, ratio {q_b / CAL.q_bucket:.2f} to the bucket crew")
say("B4", f"If the box jams, {N_HAUL} people heaving 400 N each reach {F_jam:.0f} N on a {P['rope_mbs'] / 1000:.0f} kN rope: factor {0.9 * P['rope_mbs'] / F_jam:.1f} through a splice; no overload limit, no brake")

# ------------------------------------------------------------------ option C: hand slurry pump
water_per_L = PHI_MUD / PHI_SLURRY - 1.0
slurry_per_L = PHI_MUD / PHI_SLURRY
rho_slurry = 1000.0 + PHI_SLURRY * 1650.0
A_d = math.pi / 4 * D_EFF ** 2
V_stroke = 0.5 * A_d * STROKE * VOL_EFF                 # parabolic profile sweeps half the cylinder
Q_slurry = V_stroke * SPM / 60                           # m3/s
Q_mud = Q_slurry / slurry_per_L                          # m3/s of mud
q_c = Q_mud * 3600 * A["work_rest"]
v_hose = Q_slurry / (math.pi / 4 * HOSE_D ** 2)


def bingham_dp(Q, D, L, ty, mu):
    """Pressure drop of a Bingham fluid in a laminar pipe flow (Buckingham-Reiner), solved for the wall shear."""
    v = Q / (math.pi / 4 * D ** 2)
    lo, hi = ty * 1.0000001, ty + 8 * mu * v / D * 50 + ty * 4
    for _ in range(200):
        tw = (lo + hi) / 2
        x = ty / tw
        vv = tw * D / (8 * mu) * (1 - 4 / 3 * x + x ** 4 / 3)
        lo, hi = (tw, hi) if vv < v else (lo, tw)
    return 4 * tw / D * L


dp_fric = bingham_dp(Q_slurry, HOSE_D, HOSE_L, TAU_Y, MU_P)
dp_stat = rho_slurry * g * STATIC_H
dp_valve = 5e3
dp = dp_fric + dp_stat + dp_valve
W_stroke = dp * V_stroke / ETA_PUMP
F_handle_avg = W_stroke / (STROKE * EL_RATIO)
F_handle_peak = 1.6 * F_handle_avg
P_hand = dp * Q_slurry / ETA_PUMP
H_suction_max = (101325 - 3169) / (rho_slurry * g)       # m, at sea level, water at 25 C vapour pressure
strain = (2 / 3) * (STROKE / 2 / (D_EFF / 2)) ** 2       # parabolic cap, tangential strain at the amplitude
strain_old = (2 / 3) * (0.120 / 2 / (D_EFF / 2)) ** 2    # the 120 mm stroke the first draft assumed
flush_per_h = water_per_L * Q_mud * 3600 * 1000 / 60     # L/min of flush water at full pumping rate
drum_mud = P["pump"]["drum_water"] / water_per_L         # L of mud one 200 L drum thins
say("C1", f"Flood mud {PHI_MUD * 100:.0f} % solids by volume; thinned to {PHI_SLURRY * 100:.0f} % it needs {water_per_L:.1f} L of flush water a litre of mud and makes {slurry_per_L:.1f} L of slurry ({rho_slurry:.0f} kg/m3)")
say("C2", f"Stroke {STROKE * 1000:.0f} mm on a {D_EFF * 1000:.0f} mm diaphragm: {V_stroke * 1000:.2f} L a stroke at {SPM:.0f} strokes a minute = {Q_slurry * 1000:.2f} L/s slurry, {Q_mud * 3600:.2f} m3/h of mud ({q_c:.2f} with rest, ratio {q_c / CAL.q_bucket:.2f})")
say("C3", f"Hose {HOSE_D * 1000:.0f} mm, {HOSE_L:.0f} m, {v_hose:.2f} m/s: Bingham friction {dp_fric / 1e3:.1f} kPa, static {dp_stat / 1e3:.1f} kPa, valves {dp_valve / 1e3:.0f} kPa = {dp / 1e3:.1f} kPa")
say("C4", f"Handle force {F_handle_avg:.0f} N mean, {F_handle_peak:.0f} N peak ({F_handle_peak / 2:.0f} N each with two people); hand power {P_hand:.0f} W")
say("C5", f"Diaphragm strain at the stroke amplitude {strain * 100:.1f} % (the 120 mm stroke of the first draft: {strain_old * 100:.0f} % and more than the 25 mm dish below the plane allows)")
say("C6", f"Full pumping rate needs {flush_per_h:.1f} L/min of flush water; one {P['pump']['drum_water']:.0f} L drum thins {drum_mud:.0f} L of mud ({drum_mud / CAL.V_rated:.1f} box loads)")
say("C7", f"Slurry delivered per m3 of mud {slurry_per_L:.1f} m3: {slurry_per_L:.1f} times the wet waste to dispose of")

# ------------------------------------------------------------------ parts, mass and cost by option (from the models)
INFO = {}
for opt in M.OPTIONS:
    parts = [p for p in M.components(opt) if p["kind"] != "context"]
    INFO[opt] = dict(parts=len(parts), mass=round(sum(cp.mass_kg(p) for p in parts), 1))

if __name__ == "__main__":
    print("\n".join(OUT))
    print(INFO)
