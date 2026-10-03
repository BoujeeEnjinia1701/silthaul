---
doc_id: SLH-CAL-001
title: SiltHaul sizing calculations
project: SiltHaul
doc_type: Calculation
version: "0.2"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: First issue for TRL 3 (haul force, crank force, speed and output, drum storage, overload limit, rope, anchors, shafts and chain, stability, doorway fit, setup, mass, cost)
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: Rerun on the constructable design (SLH-DDR-002); anchor bar at drum axis height, 25 mm sheave pins, lighter drum
---

# SiltHaul sizing calculations

On paper SiltHaul does the job it was drawn for, but not at the output its first requirement asks for. Two people at the cranks haul a full 40 L box (about 85 kg) with 63 N each on the handles, the rope and every anchor keep a factor of at least 5 on the rope tension that the shear pin allows, the heaviest lift is 24.7 kg, and the parts cost USD 887.50 against a value-engineering target of USD 2,000. The miss is output: about 0.32 m³ an hour with a rest allowance, against about 0.90 m³ an hour for a bucket crew of the same four people, a ratio of 0.36 where R1 asks for 2. Hand power sets the limit: two people at about 50 W each can drag 1 kN at about 5.4 m a minute, and no gearing changes that. What SiltHaul does change is who carries the weight: nobody lifts or carries mud out of the building. Nine of the twelve requirements are met on paper or by design, one is at risk (R9, boot size), one cannot be verified before a trial (R8, setup time) and one is not met (R1, output). Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [B3], is the line of that script's output that carries it.

> **Safety:** SiltHaul is a rope-and-anchor system under tension with a hand-cranked chain drive. A failed anchor, rope or shackle can whip, and the chain, sprockets and cranks can trap fingers. These are first-principles estimates for a paper proof of concept; they do not show that any part is safe. Every anchor, the rope and the capstan must be proof-loaded before use (SLH-BLD-001, section 6), and nobody stands in the line of a rope or beside a sheave while the cranks turn. See SLH-PRC-001, Safety.

## Scope and method

The note checks every requirement in SLH-REQ-001 v0.3 against the design in SLH-PRC-001 v0.3 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS`, `derived()` and `masses()`, so the drum, frame, box and tail block used here are the ones in the STEP files and drawings SLH-DWG-001 and 002. It also reads `bom/bom.csv` and `budget_usd` in `project.yaml`, and writes `docs/04-calcs/results.csv`.

The design case is a ground-floor room 7 m long, with the tail sheave block at the far wall, the doorway threshold 7 m from it and the capstan drum 15 m from it (R5). The box is hauled 11 m from the far end of the room to a dump point outside.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Mud | Density 1.70 kg/L (range 1.5 to 1.8); undrained shear strength 3 kPa (soft mud is 1 to 5 kPa) | Handbook ranges for soft silt and clay |
| Friction | Steel skids on a mud-covered floor 0.70; on the wet steel ramp 0.40 | Conservative screening values |
| Lip | Cuts a 40 mm layer of mud with a bearing factor of 6 | Assumed |
| Rope | 10 mm polyester double braid, MBS 18 kN, 0.065 kg/m; eye splices keep 90 % | Typical catalogue figures |
| Drive | Chain 95 %, each bearing 98 %; cranks 250 mm | Typical figures |
| People | 30 rpm at the cranks with a full box, 45 rpm empty; a short heave of 400 N on a crank | Ergonomic ranges for sustained cranking |
| Trip | Loading 1.5 min, dumping 0.75 min; haul 11 m | Estimates |
| Buckets | Two shovellers each fill 10 L a minute of wet mud; carriers keep up | Estimate; no published rate found for flood mud |
| Rest | People work 75 % of the time in heat and wet | Estimate |
| Shear pin | S235 bar, ultimate shear strength 240 MPa, scatter ±20 % | 0.6 times 400 MPa tensile |
| Anchors | M12 wedge anchor in sound concrete: 4 kN tension and 6 kN shear recommended loads | Typical published values; to be confirmed on the product bought |

## A. Box capacity and load (R3)

The box is 446 mm wide inside and 600 mm long to the lip, with 200 mm sides and a back that slopes 80 mm. Filled level to 165 mm it holds 40.7 L, and 49.4 L to the brim [A1]. The box and its bridles weigh 15.8 kg; 40.7 L of mud weighs 69.2 kg, so a full box is 85.0 kg, or 834 N [A2].

## B. Haul force

Dragging the full box across the floor takes 584 N of friction plus 324 N for the lip cutting through mud, 908 N in all [B1]. Over the 18.9 degree doorway ramp it takes 586 N, and the ropes add about 10 N of drag [B2]. The haul pull estimate is 917 N; the design uses a working pull of 1,000 N [B3]. Pulling the empty box back takes about 218 N [B4].

## C. Crank force (R2)

The rope sits on the drum at a 114.5 mm radius; the chain gives 4:1 and the drive is about 91 % efficient [C1]. At the 1,000 N working pull each of two people pushes 63 N on a handle, or one person 126 N, both inside the 150 N of R2 [C2]. At the haul estimate it is 58 N each, and the empty return takes 27 N for one person [C3].

## D. Speed, cycle and output (R1)

At 30 rpm on the cranks the rope moves 5.40 m a minute, and 8.10 m a minute empty at 45 rpm [D1]. A trip over 11 m takes 1.5 min to load, 2.04 min to haul, 0.75 min to dump and 1.36 min to return, 5.65 min in all [D2]. That is 10.6 trips and 0.43 m³ an hour with a crew of four, with each person at the cranks putting in about 49 W [D3].

*Table 2. Output against a bucket crew [D4, D5].*

| Crew of four | Output with rest | People carrying mud |
| --- | --- | --- |
| Shovels and buckets (two filling, two carrying) | 0.90 m³/h | Two; each cubic metre is 1.7 t lifted about 1 m and about 2.2 km walked carrying 10 L buckets |
| SiltHaul (two cranking, two loading) | 0.32 m³/h | None |

The ratio is 0.36 against the 2.0 of R1, so **R1 is not met on paper**. The limit is the power two people can give at a crank: dragging 1 kN at 5.4 m a minute already takes about 50 W each, so a faster haul needs more people or a smaller load, not a different gear. The bucket figure is an estimate; the timed trial of R1 at TRL 4 settles both numbers.

## E. Drum and rope storage (R5)

The drum has a 229.1 mm pitch diameter, 720 mm of rope a turn. Twelve metres of box travel is 16.7 turns, and each half stores 21 turns, which includes three dead turns and one spare [E1]. Each half is 236 mm long at an 11 mm winding pitch, and the drum is 484 mm between its outer faces [E2]. The drum is smooth, so the rope must reach it at no more than about 1.5 degrees from square. With the capstan 6 m from the ramp roller the worst fleet angle is 1.41 degrees, and 1.06 degrees at the design case of 8 m [E3, E4]. The capstan therefore stands at least 6 m beyond the door, which leaves rooms up to 9 m long within the 15 m of R5.

## F. Overload limit (R11)

A 4 mm S235 pin in double shear across the 25 mm crank shaft carries 75.4 N m, which is a rope tension of 2,451 N when it shears [F1]. With ±20 % scatter it releases between 1,961 and 2,941 N, so the design maximum rope tension is 3,000 N [F2]. Without the pin, two people heaving 400 N each on the cranks could put 6,372 N into a jammed rope [F3]; the pin is what lets every part below be sized on 3,000 N.

## G. Rope (R6)

An 18 kN rope, 16.2 kN through an eye splice, has a factor of 18 on the working pull and 5.4 on the overload limit [G1]. The rope bends round the drum at 22 times its diameter, round the tail sheaves at 12.5 and over the ramp roller at 6, where it turns only a few degrees [G2].

## H. Capstan anchor and stability

The capstan anchor carries 1,100 N while hauling and 3,250 N at the overload limit; the 2,000 kg round sling has 19.6 kN of working load, six times that, and each shackle 9.8 kN [H1]. The capstan weighs 62.4 kg and its weight holds 257 N m about its front edge [H2]. The sling is shackled to an eye 200 mm up, level with the drum axis, so the rope pull and the sling pull nearly line up. With the sling level the frame is held back by 315 N m; with it rising 5.7 degrees by 54 N m; at 10 degrees the tipping moment is 145 N m, still inside the 257 N m [H3 to H5]. The rule is therefore that the sling runs level or rises 10 degrees at most, for example a 3 m sling to a point no higher than 500 mm. The ground stakes stop the frame skating sideways and are not counted as the anchor.

## I. Tail sheave block (R7)

The tail block carries only 200 N while the box is hauled out, because the return leg is slack, and 436 N on the return stroke. If the box jammed on the return stroke and the crew cranked until the pin sheared, it would carry both legs at 3,000 N, 6,000 N in all [I1]. Each of the four M12 anchors then takes 1,500 N of shear and 818 N of tension, 0.45 of the typical recommended loads [I2]. Each 25 mm sheave pin takes 4,243 N at 50 mm above the plate, a bending stress of 138 MPa against 355 MPa yield [I3]. R7 is met on paper on a sound concrete slab; the anchors are only as good as the slab, which is checked on site (SLH-BLD-001, section 6).

## J. Shafts, chain and ratchet (R12)

At the overload limit the 30 mm drum shaft sees 44 MPa of bending and 65 MPa of torsion, 121 MPa combined [J1]. The chain pull is 3,539 N, a factor of 5.0 on the 17.8 kN breaking load of ISO 08B-1 chain [J2]. The 25 mm crank shaft sees 93 MPa combined before the cross hole; the hole roughly doubles the local stress, which stays below yield [J3]. A ratchet tooth carries 4,091 N, 57 MPa on its 12 x 6 mm face, and the pawl pin 36 MPa in shear [J4].

## K. Stability in the haul and tipping at the dump

A full box has its centre of mass 341 mm behind the lip, so its weight holds it level with 284 N m [K1]. The pull at the bridle ring, 75 mm up, tries to tip it nose-down with 75 N m at the working pull and 225 N m at the overload limit, both less [K2]. To dump, a person lifts the end of the tipping bar 1,293 mm behind the lip: about 203 N to start a full box, falling as the mud slides out [K3]. That is more than one person should lift repeatedly, so two people share the bar.

## L. Doorway fit, setup, mass and cost (R4, R8, R9, R10)

The box is 450 mm wide and 494 mm over its shackle pins; the ramp is 646 mm outside, and the return leg runs 53 mm clear of the box, all inside a 700 mm opening [L1]. Setting up takes about 23 min of tasks, about 17 min with three people working in parallel, which can only be confirmed in a timed trial [L2]. The heaviest single lifts are the capstan frame at 24.7 kg and the drum with its bearings at 23.1 kg; the box is 14.6 kg and the tail plate 11.0 kg [L3]. The frame is 890 x 663 x 814 mm, which fits an estate car or small pickup but not every small hatchback boot, so R9 is at risk on boot size. Value-engineering target: USD 2,000. Estimated cost of the constructable design: USD 887.50 (USD 1,112.50 under the target) [L4]. The whole kit weighs about 132 kg with rope and sling [L5].

## M. Results against every requirement

*Table 3. Requirement status from this note [M].*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R1 | Output | 0.32 m³/h against 0.90 m³/h for buckets (ratio 0.36); nobody carries mud | At least 2 times the bucket crew | **Not met on paper** |
| R9 | Portability | Heaviest lift 24.7 kg; capstan frame 890 x 663 x 814 mm | Car boot; heaviest part 25 kg or less | **At risk** (boot size) |
| R8 | Setup time | About 17 min with three people (estimate) | 20 min or less | Not verifiable at TRL 3 |
| R2 | Crank force | 63 N each with two at the cranks (126 N for one) at 1,000 N | 150 N or less | Met on paper |
| R6 | Rope and anchor strength | Rope factor 18 working, 5.4 at the 3,000 N limit; chain 5.0 | At least 5 times the working pull | Met on paper |
| R7 | Tail anchor independent of walls | Four M12 anchors in the slab, 0.45 of recommended loads at the limit | Holds on a bare concrete floor, no wall contact | Met on paper (sound slab assumed) |
| R10 | Cost | USD 887.50 | Value-engineering target USD 2,000 | Met on paper, within the target |
| R11 | Overload limit | Shear pin releases at 2,451 N (1,961 to 2,941 N) | Rope tension limited to 3,000 N | Met on paper |
| R3 | Box capacity | 40.7 L at a 165 mm fill (49 L to the brim) | About 40 L | Met by design |
| R4 | Fits a doorway | Box 494 mm over the shackles, ramp 646 mm, tail plate 440 mm | Pass a 0.7 m opening | Met by design |
| R5 | Working length | 21 turns a half store 12 m of travel; capstan at least 6 m from the door | Up to 15 m tail to capstan | Met by design |
| R12 | Holds when let go | Two ratchet wheels and pawls on the drum shaft, one each way | Holds the load when the cranks are let go | Met by design |

Counts: 1 not met, 1 at risk, 1 not verifiable at TRL 3, 5 met on paper, 4 met by design.

## Checks against the TRL 2 figures

| TRL 2 claim (SLH-PRC-001 v0.2) | This note | Action |
| --- | --- | --- |
| Friction capstan with a rope loop | A loop on a friction drum needs a pretension of about half the pull and walks along the drum | Split winding drum (SLH-DDR-002) |
| Working pull about 1 kN | 917 N estimate; 1,000 N used | None |
| Twice the bucket output | 0.36 times | R1 reported not met |
| Anchors sized on the working pull | A jammed box and two heaving people reach 6.4 kN | Shear pin limits rope tension to 3,000 N (R11) |
