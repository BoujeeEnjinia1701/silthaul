---
doc_id: SLH-STM-001
title: SiltHaul STEM check
project: SiltHaul
doc_type: STEM check
version: "0.1"
status: Draft
date: 2026-11-03
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-11-03
    author: Amish Chadha
    change: First STEM check, written for the kit 1.9.1 upgrade; covers options A, B and C; two fixes made under the standing instruction (SLH-DDR-006)
---

# SiltHaul STEM check

Of 26 claims across the three concept options, 12 sit within known science, 13 are plausible and open to confirmation at TRL 4, one (S5, the chain factor of option A, found by the independent review) fails by 1.4 % with a fix proposed to Amish, and none fails outright. Two other details failed their first screen and were fixed under Amish's standing instruction of 2026-10-23 (SLH-DDR-006): foot boards for option B and a 40 mm stroke for option C. Method and rules: STANDARDS section 20. Calculations: `docs/04-calcs/stem_check.py`, which reads the calculation note (SLH-CAL-001, `sizing.py`) for option A and `options_calc.py` for options B and C. Rows marked (A), (B) or (C) belong to that option; option A is the existing design.

## Claims checked

Table 1. Claims, governing science and verdicts.

| # | Claim (number and unit) | Field | Branch | Governing law or source | First-order check | Verdict | Closed by |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1 (A) | Two people at the 250 mm cranks turn the drum against the 1,000 N working pull with 63 N each | Physics | Mechanics and statics | Torque balance through a 4:1 roller chain at 0.91 efficiency; handle force = F r / (ratio eta R) per person | 62.8 N <= 150 N | Within known science | SLH-CAL-001 C2 |
| S2 (A) | A crank crew sustains the 5.4 m/min loaded stroke | Physics | Mechanics and statics | Power at the crank = pull x rope speed / efficiency; sustained hand-cranking 75 W per person | 48 W each <= 75 W each | Within known science | SLH-CAL-001 D3 |
| S3 (A) | The 10 mm polyester rope keeps a factor of 5 on the shear-pin limit through an eye splice | Physics | Strength of materials | Rope minimum breaking strength 18 kN, 90 % at a splice, over the design maximum tension of 3,000 N | 5.4 x >= 5 x | Plausible, to confirm at TRL 3 | SLH-CAL-001 G1 |
| S4 (A) | The 4 mm S235 shear pin releases below the 3,000 N overload limit with its 20 % scatter | Physics | Strength of materials | Double shear of a mild steel pin, tau = 0.6 x 400 MPa, torque to rope tension through the drive | 2941 N <= 3000 N | Plausible, to confirm at TRL 3 | SLH-CAL-001 F1 to F2; release test at TRL 4 |
| S5 (A) | ISO 08B-1 chain keeps a factor of 5 on the overload limit | Physics | Strength of materials | Chain pull = drum torque / (drum bearing efficiency x big sprocket pitch radius) = 3612 N at 3,000 N; 08B-1 breaking load 17.8 kN (ISO 606:2015, maker's table): factor 4.93, below the 5 of R6 (5.03 at the 2,941 N the pin can release). Fix proposed to Amish, not implemented because it moves a safety limit (SLH-DDR-005, note): (a) a 3.5 mm pin, release 1501 to 2252 N, chain factor 6.6, still 1.5 times the 977 N stroke pull; or (b) duplex 08B-2 chain and sprockets; or (c) accept 4.9 | Chain factor 4.93 at the 3,000 N limit | Fails, fix proposed | Open |
| S6 (A) | The 30 mm drum shaft stays below 0.6 of S355 yield at the overload limit | Physics | Strength of materials | Combined bending (rope pull plus the chain overhang, added conservatively) and torsion, von Mises, at the bearing; yield S355 355 MPa (EN 10025-2) | 144 MPa <= 213 MPa | Within known science | SLH-CAL-001 J1 |
| S7 (A) | The 219.1 x 3 mm drum tube does not buckle under the wound rope at the overload limit | Physics | Strength of materials | Radial pressure of a rope turn p = T / (r x pitch) = 2.52 MPa; critical external pressure of a short tube between rings, p_cr = 2.42 E (t/D)^2.5 / ((1 - v^2)^0.75 (L/D - 0.45 sqrt(t/D))) = 11.7 MPa (Windenburg and Trilling); factor 2 required | 4.6 x >= 2 x | Within known science | This script; add to SLH-CAL-001 at the next revision |
| S8 (A) | The capstan does not tip forward with the sling rising 10 degrees at the overload limit | Physics | Mechanics and statics | Moments about the front edge: rope pulls and sling pull against the weight of the frame (65.5 kg) | 145 N m <= 270 N m | Within known science | SLH-CAL-001 H3 to H5; sling rule in SLH-PRC-001 |
| S9 (A) | Four M12 wedge anchors hold the tail block when a returning box jams at the overload limit | Engineering and technology | Standards practice | Shear and tension per anchor against typical recommended loads for M12 in C20/25 concrete: combined use 0.45 of recommended (SLH-CAL-001 I2). Maker's data not checked; wedge anchors need a minimum slab thickness (often more than 100 mm), four anchors 220 mm apart may overlap their concrete cones, a flood-damaged slab should be taken as cracked, and a snatch load is dynamic | Maker's data, cracked-concrete and group factors to apply; pull test at TRL 4 | Plausible, to confirm at TRL 3 | Open |
| S10 (A) | The round sling carries the capstan anchor pull at the overload limit in a choke hitch round the tree | Engineering and technology | Standards practice | Pull of 3.25 kN against the sling WLL of 2 t (EN 1492-2, which already holds 7:1 on break) times the choke hitch mode factor 0.8 = 15.7 kN; a ratio to WLL is not a factor on break | 3.25 kN <= 15.7 kN | Within known science | SLH-CAL-001 H1 v0.5 |
| S11 (A) | The rope winds smoothly on the drum from 6 m away without climbing over the previous turn | Physics | Mechanics and statics | Fleet angle = atan(offset / distance) with the capstan 6 m from the ramp roller; smooth drum limit 1.5 degrees | 1.41 deg <= 1.5 deg | Plausible, to confirm at TRL 3 | SLH-CAL-001 E3 to E4 |
| S12 (A) | A full box (40 L, 86 kg) drags out on the mud floor at 977 N on the loop | Physics | Mechanics and statics | Coulomb friction mu 0.7 plus undrained cutting of the lip (s_u 3 kPa, N_c 6) and the ramp; pull of both boxes against the 1,000 N working pull | 977 N <= 1000 N | Plausible, to confirm at TRL 3 | Estimate: floor friction and mud strength are assumptions; measured at TRL 4 |
| S13 (A) | Two loaders fill a 40 L box in 1.5 min, so the output is 0.51 m3/h with rest | Mathematics | Orders of magnitude | The 1.5 min fill needs 13.4 L/min from each loader, above the 10 L/min of a bucket shoveller; at 10 L/min the fill takes 2.0 min, the output with rest is 0.45 m3/h and the ratio to the bucket crew 0.497, just under the 0.5 target (independent review, SLH-CAL-001 D6) | Loading rate to measure on real mud; R1 at risk by a hair | Plausible, to confirm at TRL 3 | Open |
| S14 (A) | Rope bends over the ramp roller (D/d 6), the tail sheaves (12.5) and the drum (22) do not cut the rope strength | Engineering and technology | Standards practice | Fibre rope strength and life fall as the bend ratio D/d falls; usual guidance asks for about 8 or more on a sheave with more than a few degrees of wrap. The ramp roller has a few degrees of wrap only; confirm the supplier's figure for the chosen polyester double braid | Ratio 6 at the roller, wrap a few degrees: to confirm with the rope supplier | Plausible, to confirm at TRL 3 | Open |
| S15 (A) | Painted and zinc-plated mild steel and the bearings survive repeated use in muddy, possibly salty or sewage-contaminated water | Chemistry | Materials and polymer chemistry | Mild steel corrodes in wet, aerated, chloride-bearing water; paint, zinc plating, sealed bearings (UCP) and a wash-down and drying routine are the controls. No corrosion rate is quoted here because none was checked against a source | Coating life and wash-down routine to assess at TRL 4 | Plausible, to confirm at TRL 3 | Open |
| S16 (A) | Mechanising the haul reduces how long people stand in and touch flood mud | Biology | Ecology and agronomy | Floodwater and mud can carry faecal material and chemicals, and tetanus bacteria can enter a break in the skin; boots, gloves and hand washing are advised (Better Health Channel, State of Victoria, reviewed 2024-05-20). Loaders still stand in the mud and push it into the box, so the exposure falls but does not vanish | No exposure data; reduction is plausible, not quantified | Plausible, to confirm at TRL 3 | Open |
| S17 (A) | A village fabricator can make the frame, drum, boxes and tail block from stock steel with hand tools and a small welder | Engineering and technology | Manufacturing tolerances | All sections are 40 x 40 x 2 SHS, 219.1 x 3 tube, 2 to 10 mm sheet and bar; bought parts are UCP bearings, 08B-1 chain and sprockets, rope and bolts (bom/bom.csv); 245 parts of which 161 are fasteners (SLH-DDR-005) | Weld quality and fit-up to prove in the prototype build at TRL 4 | Plausible, to confirm at TRL 3 | Open |
| S18 (B) | Four people hauling at 0.6 m/s need less than the peak human power | Physics | Mechanics and statics | Power each = pull x speed / people = 756 N x 0.4 m/s / 4, hauling hand over hand from the foot boards; duty 16 % of a 2.9 min cycle | 76 W each <= 300 W each | Within known science | options_calc.py B2 |
| S19 (B) | Four people hold a 189 N pull each, about 20 times an hour, for a shift | Physics | Mechanics and statics | ISO 11228-2:2007 (reviewed and confirmed 2021) sets recommended limits for whole-body pushing and pulling; its tables were not available to this check. 189 N each is a repeated hard pull. Boot traction on wet mud (mu about 0.25, estimate) is below the 0.28 the pull needs, so a plain boot slips: the fix, foot boards with heel cleats staked to the ground, is in the option B model (SLH-DDR-006, decided under the standing instruction); the stakes then carry 189 N each | Check against ISO 11228-2 tables and measure at TRL 4 | Plausible, to confirm at TRL 3 | Open |
| S20 (B) | A jammed box does not break the rope when four people heave at 400 N each | Physics | Strength of materials | 1,600 N on an 18 kN rope with an eye splice at 90 % | 10.1 x >= 5 x | Within known science | options_calc.py B4 |
| S21 (C) | The pump draws slurry up 0.4 m from the strainer | Physics | Fluid mechanics | Suction lift limit (atmosphere less vapour pressure at 25 C) for slurry of 1248 kg/m3 is 8.0 m; practical limit taken as half | 0.4 m <= 4 m | Within known science | options_calc.py C1 |
| S22 (C) | One or two people can supply the hydraulic power for 0.46 L/s through 19 m of hose | Physics | Fluid mechanics | Power = pressure x flow / efficiency = 51 kPa x 0.46 L/s / 0.6 | 39 W <= 75 W | Within known science | options_calc.py C3 to C4 |
| S23 (C) | A flat 3 mm EPDM diaphragm of 250 mm diameter lasts at the pump's stroke | Chemistry | Materials and polymer chemistry | The first draft assumed a 120 mm stroke: tangential strain 15 % each way for a parabolic cap, and more than the 25 mm dish below the plane can take, so the diaphragm would bottom on the valves. Fix, kept inside the working principle and decided under the standing instruction (SLH-DDR-006): stroke 40 mm (plus or minus 20 mm), strain 1.7 %, cover cavity cut to 49 mm in the model. Flex life of EPDM at that strain was not checked against a source | Diaphragm flex life to confirm with a supplier | Plausible, to confirm at TRL 3 | Open |
| S24 (C) | Flood mud thinned to 15 % solids by volume (yield stress about 30 Pa) can be pumped through a 75 mm hose at 0.1 m/s | Physics | Fluid mechanics | Bingham laminar flow in a pipe (Buckingham-Reiner), friction 34 kPa over 19 m with tau_y 30 Pa and mu_p 0.05 Pa s. Both are estimates; real flood silt, sand, sticks and rubbish may settle and block the hose and the flap valves | Rheology and solids handling to measure on real mud at TRL 4 | Plausible, to confirm at TRL 3 | Open |
| S25 (C) | Flush water and mud together make the slurry the pump moves | Mathematics | Units and dimensional analysis | Conservation of mass (mud 1.7 kg/L, water 1 kg/L) | in 3.528 kg, out 3.528 kg | Within known science | options_calc.py C1 |
| S26 (C) | One 200 L flush drum thins two box loads (80 L) of mud | Mathematics | Orders of magnitude | Water per litre of mud 1.8 L; drum thins 109 L | 80 L of mud <= 109 L of mud | Within known science | options_calc.py C6; a refill source of about 18 L/min is a site need (SLH-FEA-001) |

Verdicts: **Within known science**, **Plausible, to confirm at TRL 3**, **Fails, fix proposed**, **Fails**. The thirteen plausible rows are not failures: S3, S4, S11 and S12 are within 10 % of their limits or rest on assumed mud and friction values (SLH-CAL-001); S13 rests on an assumed loading rate; S9 and S14 to S17, S19, S23 and S24 rest on a standard, supplier figure or material property that was not checked against a source. "Open" in the last column means no calculation note closes the row at TRL 3; each is a TRL 4 measurement or an answer from Amish.

## Fixes made at this check

Two details failed their first screen. Neither changes the working principle, the pitch or the scope, so both were fixed and rerun in the same session (standing instruction, 2026-10-23) and are recorded in SLH-DDR-006. A third failure, S5, found by the independent review, moves a safety limit and goes to Amish instead (below).

Table 2. Fixes made under the standing instruction.

| Option | What failed | Fix | Result |
| --- | --- | --- | --- |
| B | Boots on wet mud give a friction coefficient of about 0.25 (estimate); a 189 N pull each needs 0.28, so the haulers slip | Two foot boards, each 40 x 200 x 1200 mm with a heel cleat and two stakes, give the haulers a staked reaction that does not rely on boot friction | In the option B model; S19 now rests on the stakes (189 N each) and on ISO 11228-2, both to check at TRL 4 |
| C | The first draft assumed a 120 mm diaphragm stroke on a 250 mm flat EPDM diaphragm: 15 % tangential strain each way, and more than the 25 mm dish under the plane allows, so the diaphragm bottoms on the valves | Stroke cut to 40 mm (plus or minus 20 mm); strain 1.7 %; cover cavity cut to 49 mm in the model | In the option C model; output falls to 0.58 m3/h of mud (0.44 with rest), which puts R1 at risk for option C (SLH-OPT-001) |

Table 3. Fix proposed to Amish (not implemented: it moves a safety limit).

| Option | What failed | Fixes proposed | Recommendation |
| --- | --- | --- | --- |
| A | S5: with drum bearing friction the chain pull at the 3,000 N limit is 3,612 N, a factor of 4.93 on 17.8 kN; R6 asks for 5 (5.03 at the 2,941 N the pin can release) | (a) a 3.5 mm shear pin: release 1,501 to 2,252 N, chain factor 6.6, still 1.5 times the 977 N stroke pull; (b) duplex 08B-2 chain and sprockets, which changes the BOM and the guard; (c) accept 4.9 | (a), awaiting Amish (SLH-DDR-005, note); it also lowers every load on the rope, anchors and frame, but it narrows the margin before the pin shears in normal use, which only the release test can settle |

## Fields not relevant

None. All five fields are touched: physics (mechanics, fluids), chemistry (corrosion, elastomer), biology (flood contamination of people), mathematics (balances and bounds) and engineering (fabrication, anchors).

## Concept options

STEM verdict for each option in SLH-OPT-001.

- **Option A, hand-capstan loop:** 17 claims; 6 within known science, 10 plausible (S3, S4, S9, S11, S12, S13 near limits or assumed; S14 to S17 open) and 1 fail with a fix proposed (S5). The new check S7 (drum tube buckling under the wound rope, factor 4.6) passes.
- **Option B, crew-hauled box:** 3 claims; 2 within known science and 1 plausible (S19, the hauling effort and footing). No fail after the foot boards were added.
- **Option C, hand slurry pump:** 6 claims; 4 within known science and 2 plausible (S23, S24). No fail after the stroke was cut. Handle force is a requirement matter, not a science one: 183 N each with two people at 19 m of hose against R2's 150 N (SLH-OPT-001).

## Independent review

A second reviewer (headless `claude -p --model claude-opus-5-5`, as Amish fixed on 2026-10-28) was given only this note, the calculation note (SLH-CAL-001), the product requirements (SLH-PRS-001) and `sizing.py`, none of my reasoning, and asked to refute the headline results and every "Within known science" verdict. It raised 13 findings. What it found and what changed:

Table 4. Independent review.

| # | Finding | Severity (reviewer) | What changed |
| --- | --- | --- | --- |
| 1 | S4 shear pin: S235 ultimate shear may be 0.6 x 510 MPa or more, releasing at 3.1 to 3.9 kN; the 3,000 N limit is not bounded; F1 uses one bearing efficiency | Blocking | Not refuted as a hazard, already Plausible: S4 stays Plausible and the release test (PR-011) and a certified pin bar (SLH-DEC-001) are the answer. The single efficiency is deliberate: only the chain and the drum bearings lie between the pin and the rope, whereas the handle force also passes the crank bearings. Wording kept; the upper-range release is recorded here |
| 2 | S13 output: the 1.5 min fill needs 13.4 L/min each, above the 10 L/min of a bucket shoveller; at 10 L/min the ratio is 0.497 | Blocking | Accepted. S13 was a weak check and is now Plausible; SLH-CAL-001 D6 added; PR-001 now "Met on paper, at risk" |
| 3 | B5 stroke pull ignores sheave and roller friction (about 1,004 N); the stroke pull is quoted three ways | Should fix | Recorded; S12 stays Plausible. The 970 N and 917 N figures belong to earlier revisions (TRL 2 and v0.3) and are history |
| 4 | S10 sling: choke hitch mode factor 0.8; a ratio to WLL is not a factor on break | Should fix | Accepted. S10 rewritten (3.25 kN against 15.7 kN WLL in a choke hitch); H1 now prints both |
| 5 | S9 anchors are Plausible, not Within known science; cone overlap, cracked concrete, minimum slab thickness | Should fix | Accepted. S9 is now Plausible with those factors listed |
| 6 | S6 drum shaft omits the chain overhang | Should fix | Accepted. J1 adds it conservatively: 144 MPa against 213 MPa allowed; S6 stays Within known science |
| 7 | S5 chain: drum bearing friction gives 3,612 N and a factor of 4.93, below 5 | Should fix | Accepted. J2 corrected; S5 is "Fails, fix proposed": the fix moves a safety limit, so it goes to Amish (Table 3) |
| 8 | K3 tipping lift subtracts a 300 N x 75 mm rope moment; mud suction not covered | Minor | Recorded; 250 N (125 N each) without the rope moment is still inside 150 N each (PR-017) |
| 9 | G1 rope factor of 18 uses the unspliced strength; no abrasion allowance | Minor | Recorded; the 5.4 at the limit already uses 90 % at a splice |
| 10 | S18 power assumes walking at 0.6 m/s but the foot boards hold the haulers still | Should fix | Accepted. Option B now hauls hand over hand at 0.4 m/s: 76 W each, 16 % duty, 0.62 m3/h with rest (ratio 0.69); SLH-OPT-001 and SLH-DDR-005 updated |
| 11 | H3 to H5 tipping uses F + Tret where the sling force is that divided by cos a (about 9 N m at 10 degrees) | Minor | Recorded; 145 + 9 N m is still inside 270 N m. The script is not changed at this revision |
| 12 | L3b packing is not a packing proof (layers, wheel arches) | Minor | Recorded; left to the TRL 4 pack test (PR-009) |
| 13 | S25 marked Open although the check holds | Minor | closed_by filled in |

The reviewer could not refute S1, S2, S6, S7, S8, S18 (power figure), S20, S21, S22, S25 and S26. It did refute S5 (now Fails, fix proposed), S9 (now Plausible), S10 (rewritten) and S13 (now Plausible). Two of its numbers were not adopted: the 0.6 x 510 MPa pin strength is a bound, not the S235 value in the note, and the choke-hitch factor applies only when the sling is choked round the tree.


## Sources

- Better Health Channel, State of Victoria, "After a flood: returning home safely", reviewed 2024-05-20, <https://www.betterhealth.vic.gov.au/health/healthyliving/after-a-flood-returning-home-safely> (checked 2026-11-03): contamination of floodwater, boots, gloves, hand washing, tetanus (S16).
- ISO 11228-2:2007 Ergonomics, Manual handling, Part 2: Pushing and pulling, confirmed 2021, <https://www.iso.org/standard/26521.html> (checked 2026-11-03): recommended limits for whole-body pushing and pulling; the tables were not read (S19).
- ISO 606:2015 Short-pitch transmission precision roller and bush chains, confirmed 2021, <https://www.iso.org/standard/61232.html> (checked 2026-11-03); the 17.8 kN breaking load of 08B-1 chain is the maker's table (S5).
- EN 1492-2:2000+A1:2008 Textile slings, roundslings made of man-made fibres, <https://genorma.com/en/standards/en-1492-2-2000-a1-2008/amp> (checked 2026-11-03): sling WLL (S10).
- EN 10025-2 non-alloy structural steels (S355 yield, S235 shear pin); Windenburg and Trilling, collapse by instability of thin cylindrical shells under external pressure (S7); Buckingham-Reiner equation for laminar Bingham pipe flow (S24).
- SiltHaul calculation note SLH-CAL-001 (`docs/04-calcs/01-sizing.md`) and `docs/04-calcs/options_calc.py` for the numbers.
