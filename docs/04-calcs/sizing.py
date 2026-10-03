"""SiltHaul sizing calculations (SLH-CAL-001), TRL 3.

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every figure quoted in docs/04-calcs/01-sizing.md, tagged [A1], [B2] and so on, and
writes docs/04-calcs/results.csv (one row per requirement). Geometry comes from cad/src/model.py
(PARAMS, derived(), masses()); costs from bom/bom.csv; the value-engineering target from
project.yaml. First-principles estimates for a paper proof of concept, not test results.
"""
import csv
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "cad" / "src")]
from model import PARAMS as P, derived, masses  # noqa: E402

D = derived(P)
g = 9.81
OUT = []


def say(tag, text):
    line = f"[{tag}] {text}"
    print(line)
    OUT.append(line)


# ------------------------------------------------------------------ assumptions
A = dict(
    rho_mud=1.70,            # kg/L wet flood silt and mud (range 1.5 to 1.8)
    mu_floor=0.70,           # steel skids on a mud-covered tiled or concrete floor
    mu_ramp=0.40,            # steel skids on the wet steel ramp deck
    s_u=3000.0,              # Pa, undrained shear strength of soft flood mud (1 to 5 kPa)
    cut_depth=0.040,         # m, mud layer the lip cuts while hauling
    n_c=6.0,                 # bearing factor for the lip pushing through mud
    rope_ret=100.0,          # N, return rope tension while hauling (slack side)
    empty_extra=100.0,       # N, plough resistance of the sloped back riding over mud
    eta_chain=0.95, eta_brg=0.98,
    crank_rpm_loaded=30.0, crank_rpm_empty=45.0,
    fill_min=1.5, dump_min=0.75,     # min per trip, loading the box and dumping it
    haul_m=11.0,             # design-case haul from the far end of a 7 m room to the dump point
    tau_pin=240e6,           # Pa, ultimate shear strength of S235 bar (0.6 x 400 MPa)
    pin_scatter=0.20,
    heave_N=400.0,           # N, short heave by one person on a crank
    bucket_fill_lpm=10.0,    # L/min sustained per shoveller filling buckets in wet mud
    work_rest=0.75,          # fraction of time working in heat and wet
    anchor_t=4.0e3, anchor_v=6.0e3,  # N, recommended tension and shear for one M12 wedge anchor (typical)
)

# ------------------------------------------------------------------ A. box capacity and load
W_in, Lb, H, t = P["box"]
br = P["back_run"]


def box_volume_L(h):
    """Inside volume below a level fill h (mm above the floor): floor from the sloped back to the lip."""
    area = (Lb - br) * h + (br / H) * h * h / 2
    return area * W_in * 1e-6


h_fill = 165.0
V_rated = box_volume_L(h_fill)
V_gross = box_volume_L(H - t)
M = masses()
m_box = M["box"] + M["bridles"]
m_mud = V_rated * A["rho_mud"]
W_full = (m_box + m_mud) * g
say("A1", f"Box inside 446 x 600 x 200 mm: {V_rated:.1f} L at a {h_fill:.0f} mm level fill (R3 target 40 L); {V_gross:.1f} L to the brim")
say("A2", f"Box and bridles {m_box:.1f} kg; mud {m_mud:.1f} kg at {A['rho_mud']} kg/L; full box {m_box + m_mud:.1f} kg ({W_full:.0f} N)")

# ------------------------------------------------------------------ B. haul force
F_fric = A["mu_floor"] * W_full
F_cut = A["s_u"] * (W_in + 2 * t) * 1e-3 * A["cut_depth"] * A["n_c"]
th = math.atan(P["ramp"][2] / (P["ramp"][0] - 40.0))
F_ramp = W_full * (math.sin(th) + A["mu_ramp"] * math.cos(th))
rope_w = 0.065 * g                      # N/m, 10 mm polyester
F_rope = 0.5 * rope_w * 30
F_haul = max(F_fric + F_cut, F_ramp) + F_rope
F_w = 1000.0
say("B1", f"Floor friction {F_fric:.0f} N (mu {A['mu_floor']}) plus lip cutting {F_cut:.0f} N = {F_fric + F_cut:.0f} N")
say("B2", f"Over the ramp ({math.degrees(th):.1f} deg, mu {A['mu_ramp']}): {F_ramp:.0f} N; rope drag {F_rope:.0f} N")
say("B3", f"Haul pull estimate {F_haul:.0f} N; design working pull {F_w:.0f} N")
F_empty = A["mu_floor"] * m_box * g + A["empty_extra"] + F_rope
say("B4", f"Empty return pull {F_empty:.0f} N")

# ------------------------------------------------------------------ C. crank force
r_p = D["pitch_d"] / 2 / 1000
eta = A["eta_chain"] * A["eta_brg"] ** 2
ratio = D["ratio"]
crank_r = P["crank_r"] / 1000


def handle_force(F, people):
    return F * r_p / (ratio * eta) / crank_r / people


say("C1", f"Drum pitch radius {r_p * 1000:.1f} mm; reduction {ratio:.0f}:1; efficiency {eta:.2f}; crank radius {P['crank_r']:.0f} mm")
say("C2", f"Handle force at {F_w:.0f} N: {handle_force(F_w, 2):.0f} N each with two people, {handle_force(F_w, 1):.0f} N for one (R2: 150 N)")
say("C3", f"Handle force at the haul estimate {F_haul:.0f} N: {handle_force(F_haul, 2):.0f} N each with two people; empty return {handle_force(F_empty, 1):.0f} N for one")

# ------------------------------------------------------------------ D. speed, cycle and output
circ = D["circ"] / 1000
v_load = A["crank_rpm_loaded"] / ratio * circ
v_empty = A["crank_rpm_empty"] / ratio * circ
t_haul = A["haul_m"] / v_load
t_ret = A["haul_m"] / v_empty
t_cycle = A["fill_min"] + t_haul + A["dump_min"] + t_ret
trips = 60 / t_cycle
q_silt = trips * V_rated / 1000
P_person = F_w * v_load / 60 / eta / 2
say("D1", f"Rope speed {v_load:.2f} m/min loaded (crank {A['crank_rpm_loaded']:.0f} rpm), {v_empty:.2f} m/min empty ({A['crank_rpm_empty']:.0f} rpm)")
say("D2", f"Trip over {A['haul_m']:.0f} m: fill {A['fill_min']} + haul {t_haul:.2f} + dump {A['dump_min']} + return {t_ret:.2f} = {t_cycle:.2f} min")
say("D3", f"{trips:.1f} trips an hour, {q_silt:.2f} m3/h with a crew of four (two at the crank, two loading); {P_person:.0f} W each at the crank")
q_bucket = 2 * A["bucket_fill_lpm"] * 60 / 1000 * A["work_rest"]
q_silt_rest = q_silt * A["work_rest"]
ratio_out = q_silt_rest / q_bucket
say("D4", f"Bucket crew of four (two shovelling, two carrying): {q_bucket:.2f} m3/h; SiltHaul with the same rest allowance {q_silt_rest:.2f} m3/h; ratio {ratio_out:.2f} (R1 target 2.0)")
lift_bucket = 1000 * A["rho_mud"] * g * 1.0 * 1e-3      # kJ per m3 to lift mud 1.0 m into and out of buckets
carry_bucket = A["haul_m"] * 2                         # m walked per bucket trip
say("D5", f"Per cubic metre the bucket crew lifts {A['rho_mud']:.1f} t through about 1 m ({lift_bucket:.0f} kJ) and walks about {1000 / 10 * carry_bucket / 1000:.1f} km carrying 10 L buckets; with SiltHaul nobody carries mud")

# ------------------------------------------------------------------ E. drum and rope storage
say("E1", f"Drum pitch diameter {D['pitch_d']:.1f} mm, {D['circ']:.0f} mm a turn; travel {P['travel'] / 1000:.0f} m = {D['turns_travel']:.1f} turns; {D['turns']} turns stored on each half")
say("E2", f"Each half {D['half_len']:.0f} mm long at {P['pitch']:.0f} mm pitch; drum {D['drum_len']:.0f} mm between outer faces")
half = D["half_len"] / 2
off = max(abs(P["cap_y"] + D["y_pull"]) + half, abs(P["cap_y"] + D["y_ret"] - P["ret_y"]) + half)
for dist in (6.0, 8.0):
    say("E3" if dist == 6.0 else "E4", f"Fleet angle with the capstan {dist:.0f} m from the ramp roller: {math.degrees(math.atan(off / 1000 / dist)):.2f} deg (smooth drum limit 1.5 deg)")

# ------------------------------------------------------------------ F. overload limit (shear pin)
d_pin, d_sh = P["shear_pin"] / 1000, P["crank_shaft"] / 1000
T_pin = A["tau_pin"] * math.pi * d_pin ** 2 / 4 * d_sh
F_rel = T_pin * ratio * A["eta_chain"] * A["eta_brg"] / r_p
F_max = F_rel * (1 + A["pin_scatter"])
F_max_r = math.ceil(F_max / 100) * 100
F_stall = 2 * A["heave_N"] * crank_r * ratio * eta / r_p
say("F1", f"Shear pin {P['shear_pin']:.0f} mm in double shear across a {P['crank_shaft']:.0f} mm shaft: {T_pin:.1f} N m; rope tension at release {F_rel:.0f} N")
say("F2", f"With {A['pin_scatter'] * 100:.0f} % scatter the release is {F_rel * (1 - A['pin_scatter']):.0f} to {F_max:.0f} N; design maximum rope tension {F_max_r:.0f} N")
say("F3", f"Without the pin two people heaving {A['heave_N']:.0f} N each could reach {F_stall:.0f} N")

# ------------------------------------------------------------------ G. rope
mbs = P["rope_mbs"]
mbs_s = 0.9 * mbs
say("G1", f"Rope MBS {mbs / 1000:.0f} kN, {mbs_s / 1000:.1f} kN at an eye splice: factor {mbs / F_w:.0f} on the working pull, {mbs_s / F_max_r:.1f} on the overload limit (R6: 5)")
say("G2", f"Bend ratios D/d: drum {P['drum_tube'][0] / P['rope_d']:.0f}, tail sheaves {P['sheave'][0] / P['rope_d']:.1f}, ramp roller {P['roller'][0] / P['rope_d']:.0f} (a few degrees of wrap)")

# ------------------------------------------------------------------ H. capstan anchor and frame stability
F_cap_w = F_w + A["rope_ret"]
F_cap_max = F_max_r + 250.0
wll_sling = 2000 * g
say("H1", f"Capstan anchor pull {F_cap_w:.0f} N working, {F_cap_max:.0f} N at the overload limit; sling WLL {wll_sling / 1000:.1f} kN ({wll_sling / F_cap_max:.1f} times); shackle WLL 9.8 kN")
m_cap = sum(M[k] for k in ("frame", "drum", "drum_bearings", "crank_bearings", "crank_shaft", "cranks",
                           "small_sprocket", "chain", "guard", "pawls"))
x_front = abs(P["rail_x"][0])
restore = m_cap * g * x_front / 1000
z_eye = P["hd"] / 1000


def overturn(F, Tret, alpha_deg):
    a = math.radians(alpha_deg)
    Fs = F + Tret
    from model import anchor_bar_x
    x_eye = (anchor_bar_x(P) + P["shs"][0] / 2 + 45 + x_front) / 1000
    return F * D["z_under"] / 1000 + Tret * D["z_over"] / 1000 - Fs * math.cos(a) * z_eye + Fs * math.sin(a) * x_eye


say("H2", f"Capstan {m_cap:.1f} kg; weight holds {restore:.0f} N m about the front edge")
for tag, al in (("H3", 0.0), ("H4", 5.7), ("H5", 10.0)):
    say(tag, f"Tipping moment at the overload limit with the sling rising {al:.1f} deg: {overturn(F_max_r, 250.0, al):.0f} N m (holds if below {restore:.0f})")

# ------------------------------------------------------------------ I. tail sheave block
F_tail_haul = 2 * A["rope_ret"]
F_tail_ret = 2 * F_empty
F_tail_max = 2 * F_max_r
M_tail = F_tail_max * P["rope_z"] / 1000
T_anchor = M_tail / 0.220 / 2
V_anchor = F_tail_max / 4
util = T_anchor / A["anchor_t"] + V_anchor / A["anchor_v"]
say("I1", f"Tail block load {F_tail_haul:.0f} N while hauling, {F_tail_ret:.0f} N on the return stroke, {F_tail_max:.0f} N if the box jams on the return at the overload limit")
say("I2", f"Each of four M12 anchors at that limit: shear {V_anchor:.0f} N, tension {T_anchor:.0f} N; combined use {util:.2f} of typical recommended loads")
F_pin = math.sqrt(2) * F_max_r
M_pin = F_pin * (P["rope_z"] - P["tail_plate"][2]) / 1000
sig_pin = M_pin / (math.pi * (P["tail_pin"] / 1000) ** 3 / 32) / 1e6
say("I3", f"Sheave pin {P['tail_pin']:.0f} mm: {F_pin:.0f} N at {P['rope_z'] - P['tail_plate'][2]:.0f} mm above the plate, bending {sig_pin:.0f} MPa (S355 yield 355 MPa)")

# ------------------------------------------------------------------ J. shafts, chain, ratchet
T_drum_max = F_max_r * r_p
yb = D["yb"]
arm = (yb - D["drum_len"] / 2) / 1000
sig_b = F_cap_max * arm / (math.pi * 0.030 ** 3 / 32) / 1e6
tau_t = T_drum_max / (math.pi * 0.030 ** 3 / 16) / 1e6
vm = math.sqrt(sig_b ** 2 + 3 * tau_t ** 2)
say("J1", f"Drum shaft 30 mm at the bearing: bending {sig_b:.0f} MPa, torsion {tau_t:.0f} MPa, combined {vm:.0f} MPa at the overload limit")
F_chain = T_drum_max / (D["pd_big"] / 2000)
say("J2", f"Chain pull {F_chain:.0f} N at the overload limit; 08B-1 breaking load 17.8 kN, factor {17800 / F_chain:.1f}")
ov = abs(D["y_spr"]) - (yb + P["ucp205"][5] / 2)
sig_cs = F_chain * ov / 1000 / (math.pi * 0.025 ** 3 / 32) / 1e6
tau_cs = T_pin / (math.pi * 0.025 ** 3 / 16) / 1e6
say("J3", f"Crank shaft 25 mm: bending {sig_cs:.0f} MPa, torsion {tau_cs:.0f} MPa, combined {math.sqrt(sig_cs ** 2 + 3 * tau_cs ** 2):.0f} MPa (nominal, before the cross hole)")
r_t = (P["ratchet"][0] + P["ratchet"][1]) / 4 / 1000
F_tooth = T_drum_max / r_t
say("J4", f"Ratchet tooth force {F_tooth:.0f} N; bearing stress {F_tooth / (12 * P['ratchet'][3]):.0f} MPa on a 12 x {P['ratchet'][3]:.0f} mm face; pawl pin shear {F_tooth / (math.pi * 36):.0f} MPa")

# ------------------------------------------------------------------ K. stability in the haul and tipping at the dump
x_lip = Lb + 60.0
x_cg_mud = ((Lb - br) * h_fill * (br + (Lb - br) / 2) + (br / H) * h_fill ** 2 / 2 * (br - br * h_fill / H / 3)) / ((Lb - br) * h_fill + (br / H) * h_fill ** 2 / 2)
x_cg = (m_mud * x_cg_mud + m_box * 300.0) / (m_mud + m_box)
M_rest = W_full * (x_lip - x_cg) / 1000
say("K1", f"Full box: centre of mass {x_lip - x_cg:.0f} mm behind the lip; {M_rest:.0f} N m holds it level")
say("K2", f"Pull at the bridle ring 75 mm up tips it forward by {F_w * 0.075:.0f} N m at the working pull and {F_max_r * 0.075:.0f} N m at the overload limit")
so = P["socket"]
xb = br * (P["skid"][1] + H - 160.0) / H - 1.0
lever = (x_lip - (xb + 12.0 - math.sqrt(0.5) * (48 + P["tip_bar"][2]))) / 1000
F_tip = (M_rest - 300.0 * 0.075) / lever
say("K3", f"Tipping at the dump: lever {lever * 1000:.0f} mm from the lip to the bar end; lift {F_tip:.0f} N to start a full box, falling as the mud slides out")

# ------------------------------------------------------------------ L. doorway fit, setup, mass, cost
w_box = W_in + 2 * t + 2 * P["lug_t"] + 2 * 12
w_ramp = P["ramp"][1] + 2 * P["cheek_t"]
say("L1", f"Box {W_in + 2 * t:.0f} mm wide, {w_box:.0f} mm over the shackle pins; ramp {w_ramp:.0f} mm outside; return leg {P['ret_y'] - w_box / 2:.0f} mm clear of the box (R4: 700 mm opening)")
setup = [("Unload and carry the kit, three people", 5), ("Set the capstan, drive four stakes", 4),
         ("Sling to a tree or vehicle, shackle", 2), ("Drill four holes, fit the tail block", 6),
         ("Place the ramp", 1), ("Lay out the ropes, shackle the box", 3), ("Take up slack, brief the crew", 2)]
serial = sum(m for _, m in setup)
par = 5 + max(4 + 2, 6 + 1) + 3 + 2
say("L2", f"Setup tasks {serial} min end to end; with three people working in parallel about {par} min (R8: 20 min)")
heavy = sorted(((v, k) for k, v in M.items()), reverse=True)[:4]
drum_lift = M["drum"] + M["drum_bearings"]
say("L3", "Heaviest single lifts: capstan frame {:.1f} kg; drum with its bearings {:.1f} kg; box {:.1f} kg; tail plate {:.1f} kg (R9: 25 kg)".format(
    M["frame"], drum_lift, M["box"], M["tail_plate"]))
rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
cost = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows)
budget = float(re.search(r"^budget_usd:\s*([0-9.]+)", (ROOT / "project.yaml").read_text(), re.M).group(1))
say("L4", f"Parts cost {cost:,.2f} USD; value-engineering target {budget:,.0f} USD; {budget - cost:,.2f} USD under")
total_mass = sum(M.values()) + 55 * 0.065 + 1.0
say("L5", f"Kit mass about {total_mass:.0f} kg including rope and sling")

# ------------------------------------------------------------------ results against the requirements
R = [
    ("R1", f"{q_silt_rest:.2f} m3/h against {q_bucket:.2f} m3/h for buckets (ratio {ratio_out:.2f}); nobody carries mud", "At least 2 times the bucket crew", "Not met on paper"),
    ("R2", f"{handle_force(F_w, 2):.0f} N each with two at the crank ({handle_force(F_w, 1):.0f} N for one) at 1,000 N", "150 N or less", "Met on paper"),
    ("R3", f"{V_rated:.1f} L at a 165 mm fill ({V_gross:.0f} L to the brim)", "About 40 L", "Met by design"),
    ("R4", f"Box {w_box:.0f} mm over the shackles, ramp {w_ramp:.0f} mm, tail plate 440 mm", "Pass a 0.7 m opening", "Met by design"),
    ("R5", f"{D['turns']} turns a half store {P['travel'] / 1000:.0f} m of travel; capstan at least 6 m from the door", "Up to 15 m tail to capstan", "Met by design"),
    ("R6", f"Rope factor {mbs / F_w:.0f} working, {mbs_s / F_max_r:.1f} at the {F_max_r:.0f} N overload limit; chain {17800 / F_chain:.1f}", "At least 5 times the working pull", "Met on paper"),
    ("R7", f"Four M12 anchors in the slab, {util:.2f} of typical recommended loads at the overload limit", "Holds on a bare concrete floor, no wall contact", "Met on paper (sound slab assumed)"),
    ("R8", f"About {par} min with three people (estimate)", "20 min or less", "Not verifiable at TRL 3"),
    ("R9", f"Heaviest lift {max(M['frame'], drum_lift):.1f} kg; capstan frame 890 x 663 x 814 mm", "Car boot; heaviest part 25 kg or less", "At risk (boot size)"),
    ("R10", f"{cost:,.2f} USD", f"Value-engineering target {budget:,.0f} USD", "Met on paper, within the target"),
    ("R11", f"Shear pin releases at {F_rel:.0f} N ({F_rel * 0.8:.0f} to {F_max:.0f} N)", "Rope tension limited to 3,000 N", "Met on paper"),
    ("R12", "Two ratchet wheels and pawls on the drum shaft, one for each direction", "Holds the load when the cranks are let go", "Met by design"),
]
with (ROOT / "docs" / "04-calcs" / "results.csv").open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "value", "target", "status"])
    w.writerows(R)
for r in R:
    say("M", " | ".join(r))
