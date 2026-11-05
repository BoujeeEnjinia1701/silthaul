"""SiltHaul STEM check calculations (SLH-STM-001, STANDARDS section 20).

Run from the repo root:  python docs/04-calcs/stem_check.py
Writes docs/04-calcs/stem_results.csv. These are first-order screens of each claim of the three concept options
(A hand-capstan loop, the existing design; B crew-hauled box; C hand slurry pump). The sizing of option A is the
calculation note (SLH-CAL-001, sizing.py); the first-order numbers for B and C are in options_calc.py. Both are
imported here (about a minute: the model is built once) to close the claims on the TRL 3 design.
"""
import math
import sys

sys.path.insert(0, ".kit")
from stem_check import Check, limits, WITHIN, PLAUSIBLE, FIX  # noqa: E402
sys.path.insert(0, "docs/04-calcs")
import options_calc as OC  # noqa: E402  builds option A through sizing.py
CAL = OC.CAL
P = CAL.P
D = CAL.D
E_STEEL = 210e9

c = Check()

# ---------------------------------------------------------------- Option A: hand-capstan loop (SLH-CAL-001)
c.claim("S1", "Two people at the 250 mm cranks turn the drum against the 1,000 N working pull with 63 N each", "Physics", "Mechanics and statics",
        "Torque balance through a 4:1 roller chain at 0.91 efficiency; handle force = F r / (ratio eta R) per person",
        round(CAL.handle_force(CAL.F_w, 2), 1), 150.0, "N", closed_by="SLH-CAL-001 C2")
c.claim("S2", "A crank crew sustains the 5.4 m/min loaded stroke", "Physics", "Mechanics and statics",
        f"Power at the crank = pull x rope speed / efficiency; sustained hand-cranking {limits.HUMAN_SUSTAINED_W:.0f} W per person",
        round(CAL.P_person, 0), limits.HUMAN_SUSTAINED_W, "W each", closed_by="SLH-CAL-001 D3")
c.claim("S3", "The 10 mm polyester rope keeps a factor of 5 on the shear-pin limit through an eye splice", "Physics", "Strength of materials",
        "Rope minimum breaking strength 18 kN, 90 % at a splice, over the design maximum tension of 3,000 N",
        round(CAL.mbs_s / CAL.F_max_r, 2), 5.0, "x", rule="above", margin=0.1, closed_by="SLH-CAL-001 G1")
c.claim("S4", "The 4 mm S235 shear pin releases below the 3,000 N overload limit with its 20 % scatter", "Physics", "Strength of materials",
        "Double shear of a mild steel pin, tau = 0.6 x 400 MPa, torque to rope tension through the drive",
        round(CAL.F_max, 0), 3000.0, "N", margin=0.05, closed_by="SLH-CAL-001 F1 to F2; release test at TRL 4")
# S5: found by the independent review. Drum bearing friction adds to the chain's share of the torque, so the factor at the
# 3,000 N limit is 4.93 against the 5 that R6 asks. A smaller pin lowers the limit; the numbers for a 3.5 mm pin follow.
d_sh_ = CAL.P["crank_shaft"] / 1000
r_p_ = CAL.D["pitch_d"] / 2 / 1000


def release(d_mm, scatter=0.0):
    t = CAL.A["tau_pin"] * math.pi * (d_mm / 1000) ** 2 / 4 * d_sh_
    return t * CAL.ratio * CAL.A["eta_chain"] * CAL.A["eta_brg"] / r_p_ * (1 + scatter)


f35_max, f35_min = release(3.5, 0.2), release(3.5, -0.2)
chain_35 = 17800 / (f35_max * r_p_ / CAL.A["eta_brg"] / (CAL.D["pd_big"] / 2000))
c.cited("S5", "ISO 08B-1 chain keeps a factor of 5 on the overload limit", "Physics", "Strength of materials",
        f"Chain pull = drum torque / (drum bearing efficiency x big sprocket pitch radius) = {CAL.F_chain:.0f} N at 3,000 N; 08B-1 breaking load 17.8 kN (ISO 606:2015, maker's table): factor {17800 / CAL.F_chain:.2f}, below the 5 of R6 (5.03 at the 2,941 N the pin can release). Fix proposed to Amish, not implemented because it moves a safety limit (SLH-DDR-005, note): (a) a 3.5 mm pin, release {f35_min:.0f} to {f35_max:.0f} N, chain factor {chain_35:.1f}, still {f35_min / CAL.F_stroke:.1f} times the {CAL.F_stroke:.0f} N stroke pull; or (b) duplex 08B-2 chain and sprockets; or (c) accept 4.9",
        "Chain factor 4.93 at the 3,000 N limit", FIX, closed_by="")
c.claim("S6", "The 30 mm drum shaft stays below 0.6 of S355 yield at the overload limit", "Physics", "Strength of materials",
        "Combined bending (rope pull plus the chain overhang, added conservatively) and torsion, von Mises, at the bearing; yield S355 355 MPa (EN 10025-2)",
        round(CAL.vm, 0), 0.6 * 355.0, "MPa", closed_by="SLH-CAL-001 J1")
# New at kit 1.9: the thin drum tube under the pressure of the wound rope (not in SLH-CAL-001 v0.4)
t_tube, d_tube = P["drum_tube"][1] / 1000, P["drum_tube"][0] / 1000
l_ring = D["half_len"] / 1000
p_rope = CAL.F_max_r / ((d_tube / 2 - t_tube / 2) * P["pitch"] / 1000)
td = t_tube / d_tube
p_cr = 2.42 * E_STEEL * td ** 2.5 / ((1 - 0.3 ** 2) ** 0.75 * (l_ring / d_tube - 0.45 * math.sqrt(td)))
c.claim("S7", "The 219.1 x 3 mm drum tube does not buckle under the wound rope at the overload limit", "Physics", "Strength of materials",
        f"Radial pressure of a rope turn p = T / (r x pitch) = {p_rope / 1e6:.2f} MPa; critical external pressure of a short tube between rings, "
        f"p_cr = 2.42 E (t/D)^2.5 / ((1 - v^2)^0.75 (L/D - 0.45 sqrt(t/D))) = {p_cr / 1e6:.1f} MPa (Windenburg and Trilling); factor 2 required",
        round(p_cr / p_rope, 1), 2.0, "x", rule="above", closed_by="This script; add to SLH-CAL-001 at the next revision")
c.claim("S8", "The capstan does not tip forward with the sling rising 10 degrees at the overload limit", "Physics", "Mechanics and statics",
        "Moments about the front edge: rope pulls and sling pull against the weight of the frame (65.5 kg)",
        round(CAL.overturn(CAL.F_max_r, 250.0, 10.0), 0), round(CAL.restore, 0), "N m", margin=0.1, closed_by="SLH-CAL-001 H3 to H5; sling rule in SLH-PRC-001")
c.cited("S9", "Four M12 wedge anchors hold the tail block when a returning box jams at the overload limit", "Engineering and technology", "Standards practice",
        f"Shear and tension per anchor against typical recommended loads for M12 in C20/25 concrete: combined use {CAL.util:.2f} of recommended (SLH-CAL-001 I2). Maker's data not checked; wedge anchors need a minimum slab thickness (often more than 100 mm), four anchors 220 mm apart may overlap their concrete cones, a flood-damaged slab should be taken as cracked, and a snatch load is dynamic",
        "Maker's data, cracked-concrete and group factors to apply; pull test at TRL 4", PLAUSIBLE)
c.claim("S10", "The round sling carries the capstan anchor pull at the overload limit in a choke hitch round the tree", "Engineering and technology", "Standards practice",
        "Pull of 3.25 kN against the sling WLL of 2 t (EN 1492-2, which already holds 7:1 on break) times the choke hitch mode factor 0.8 = 15.7 kN; a ratio to WLL is not a factor on break",
        round(CAL.F_cap_max / 1000, 2), round(0.8 * CAL.wll_sling / 1000, 1), "kN", closed_by="SLH-CAL-001 H1 v0.5")
c.claim("S11", "The rope winds smoothly on the drum from 6 m away without climbing over the previous turn", "Physics", "Mechanics and statics",
        "Fleet angle = atan(offset / distance) with the capstan 6 m from the ramp roller; smooth drum limit 1.5 degrees",
        round(math.degrees(math.atan(CAL.off / 1000 / 6.0)), 2), 1.5, "deg", margin=0.1, closed_by="SLH-CAL-001 E3 to E4")
c.claim("S12", "A full box (40 L, 86 kg) drags out on the mud floor at 977 N on the loop", "Physics", "Mechanics and statics",
        "Coulomb friction mu 0.7 plus undrained cutting of the lip (s_u 3 kPa, N_c 6) and the ramp; pull of both boxes against the 1,000 N working pull",
        round(CAL.F_stroke, 0), 1000.0, "N", margin=0.05, closed_by="Estimate: floor friction and mud strength are assumptions; measured at TRL 4")
c.cited("S13", "Two loaders fill a 40 L box in 1.5 min, so the output is 0.51 m3/h with rest", "Mathematics", "Orders of magnitude",
        f"The 1.5 min fill needs {CAL.V_rated / CAL.A['fill_min'] / 2:.1f} L/min from each loader, above the 10 L/min of a bucket shoveller; at 10 L/min the fill takes 2.0 min, the output with rest is 0.45 m3/h and the ratio to the bucket crew 0.497, just under the 0.5 target (independent review, SLH-CAL-001 D6)",
        "Loading rate to measure on real mud; R1 at risk by a hair", PLAUSIBLE)
c.cited("S14", "Rope bends over the ramp roller (D/d 6), the tail sheaves (12.5) and the drum (22) do not cut the rope strength",
        "Engineering and technology", "Standards practice",
        "Fibre rope strength and life fall as the bend ratio D/d falls; usual guidance asks for about 8 or more on a sheave with more than a few degrees of wrap. The ramp roller has a few degrees of wrap only; confirm the supplier's figure for the chosen polyester double braid",
        "Ratio 6 at the roller, wrap a few degrees: to confirm with the rope supplier", PLAUSIBLE)
c.cited("S15", "Painted and zinc-plated mild steel and the bearings survive repeated use in muddy, possibly salty or sewage-contaminated water",
        "Chemistry", "Materials and polymer chemistry",
        "Mild steel corrodes in wet, aerated, chloride-bearing water; paint, zinc plating, sealed bearings (UCP) and a wash-down and drying routine are the controls. No corrosion rate is quoted here because none was checked against a source",
        "Coating life and wash-down routine to assess at TRL 4", PLAUSIBLE)
c.cited("S16", "Mechanising the haul reduces how long people stand in and touch flood mud",
        "Biology", "Ecology and agronomy",
        "Floodwater and mud can carry faecal material and chemicals, and tetanus bacteria can enter a break in the skin; boots, gloves and hand washing are advised (Better Health Channel, State of Victoria, reviewed 2024-05-20). Loaders still stand in the mud and push it into the box, so the exposure falls but does not vanish",
        "No exposure data; reduction is plausible, not quantified", PLAUSIBLE)
c.cited("S17", "A village fabricator can make the frame, drum, boxes and tail block from stock steel with hand tools and a small welder",
        "Engineering and technology", "Manufacturing tolerances",
        "All sections are 40 x 40 x 2 SHS, 219.1 x 3 tube, 2 to 10 mm sheet and bar; bought parts are UCP bearings, 08B-1 chain and sprockets, rope and bolts (bom/bom.csv); 245 parts of which 161 are fasteners (SLH-DDR-005)",
        "Weld quality and fit-up to prove in the prototype build at TRL 4", PLAUSIBLE)

# ---------------------------------------------------------------- Option B: crew-hauled box
c.claim("S18", "Four people hauling at 0.6 m/s need less than the peak human power", "Physics", "Mechanics and statics",
        f"Power each = pull x speed / people = {OC.F_haul:.0f} N x {OC.H_SPEED} m/s / {OC.N_HAUL}, hauling hand over hand from the foot boards; duty {OC.duty * 100:.0f} % of a {OC.t_cycle_b:.1f} min cycle",
        round(OC.P_haul_each, 0), limits.HUMAN_PEAK_W, "W each", closed_by="options_calc.py B2")
c.cited("S19", "Four people hold a 189 N pull each, about 20 times an hour, for a shift",
        "Physics", "Mechanics and statics",
        "ISO 11228-2:2007 (reviewed and confirmed 2021) sets recommended limits for whole-body pushing and pulling; its tables were not available to this check. 189 N each is a repeated hard pull. Boot traction on wet mud (mu about 0.25, estimate) is below the 0.28 the pull needs, so a plain boot slips: the fix, foot boards with heel cleats staked to the ground, is in the option B model (SLH-DDR-006, decided under the standing instruction); the stakes then carry 189 N each",
        "Check against ISO 11228-2 tables and measure at TRL 4", PLAUSIBLE)
c.claim("S20", "A jammed box does not break the rope when four people heave at 400 N each", "Physics", "Strength of materials",
        "1,600 N on an 18 kN rope with an eye splice at 90 %",
        round(0.9 * CAL.P["rope_mbs"] / OC.F_jam, 1), 5.0, "x", rule="above", closed_by="options_calc.py B4")

# ---------------------------------------------------------------- Option C: hand slurry pump
c.claim("S21", "The pump draws slurry up 0.4 m from the strainer", "Physics", "Fluid mechanics",
        f"Suction lift limit (atmosphere less vapour pressure at 25 C) for slurry of {OC.rho_slurry:.0f} kg/m3 is {OC.H_suction_max:.1f} m; practical limit taken as half",
        0.4, round(OC.H_suction_max / 2, 1), "m", closed_by="options_calc.py C1")
c.claim("S22", "One or two people can supply the hydraulic power for 0.46 L/s through 19 m of hose", "Physics", "Fluid mechanics",
        f"Power = pressure x flow / efficiency = {OC.dp / 1e3:.0f} kPa x {OC.Q_slurry * 1000:.2f} L/s / {OC.ETA_PUMP}",
        round(OC.P_hand, 0), limits.HUMAN_SUSTAINED_W, "W", closed_by="options_calc.py C3 to C4")
c.cited("S23", "A flat 3 mm EPDM diaphragm of 250 mm diameter lasts at the pump's stroke",
        "Chemistry", "Materials and polymer chemistry",
        f"The first draft assumed a 120 mm stroke: tangential strain {OC.strain_old * 100:.0f} % each way for a parabolic cap, and more than the 25 mm dish below the plane can take, so the diaphragm would bottom on the valves. Fix, kept inside the working principle and decided under the standing instruction (SLH-DDR-006): stroke 40 mm (plus or minus 20 mm), strain {OC.strain * 100:.1f} %, cover cavity cut to 49 mm in the model. Flex life of EPDM at that strain was not checked against a source",
        "Diaphragm flex life to confirm with a supplier", PLAUSIBLE)
c.cited("S24", "Flood mud thinned to 15 % solids by volume (yield stress about 30 Pa) can be pumped through a 75 mm hose at 0.1 m/s",
        "Physics", "Fluid mechanics",
        f"Bingham laminar flow in a pipe (Buckingham-Reiner), friction {OC.dp_fric / 1e3:.0f} kPa over 19 m with tau_y 30 Pa and mu_p 0.05 Pa s. Both are estimates; real flood silt, sand, sticks and rubbish may settle and block the hose and the flap valves",
        "Rheology and solids handling to measure on real mud at TRL 4", PLAUSIBLE)
c.balance("S25", "Flush water and mud together make the slurry the pump moves", "Mathematics", "Units and dimensional analysis",
          {"1 L mud": CAL.A["rho_mud"], "flush water": OC.water_per_L * 1.0},
          {"slurry": OC.slurry_per_L * OC.rho_slurry / 1000.0}, "kg", law="Conservation of mass (mud 1.7 kg/L, water 1 kg/L)", closed_by="options_calc.py C1")
c.claim("S26", "One 200 L flush drum thins two box loads (80 L) of mud", "Mathematics", "Orders of magnitude",
        f"Water per litre of mud {OC.water_per_L:.1f} L; drum thins {OC.drum_mud:.0f} L",
        80.0, round(OC.drum_mud, 0), "L of mud", closed_by="options_calc.py C6; a refill source of about 18 L/min is a site need (SLH-FEA-001)")

if __name__ == "__main__":
    print("Record of the fixes made at this check (SLH-DDR-006):")
    print(f"  B: boots on wet mud give mu {OC.MU_BOOT_MUD}, the pull needs {OC.mu_needed:.2f}: foot boards with heel cleats and four stakes added to option B")
    print(f"  C: stroke 120 mm gave {OC.strain_old * 100:.0f} % strain and did not fit the 25 mm dish: stroke cut to {OC.STROKE * 1000:.0f} mm, cover cavity cut to 49 mm")
    c.write()
