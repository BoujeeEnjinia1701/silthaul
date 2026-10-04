---
doc_id: SLH-CAL-001
title: SiltHaul sizing calculations
project: SiltHaul
doc_type: Calculation
version: "0.4"
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
- version: "0.3"
  date: '2026-10-03'
  author: Amish Chadha
  change: Rerun for Amish's requirement decisions (SLH-DDR-003); second box on the return leg (two-box stroke, output against the restated R1); flat-pack frame and pack check (R9); tail block, setup, mass and cost updated
- version: "0.4"
  date: '2026-10-03'
  author: Amish Chadha
  change: "R9 restated per Amish's round-2 decision 2A (SLH-DDR-004); no numbers changed"
---

# SiltHaul sizing calculations

On paper SiltHaul now meets its output requirement as Amish restated it on 2026-10-03 (SLH-DDR-003, decision 2A): "no lifting or carrying of mud; output at least 0.5 times the same crew with shovels and buckets". A second box rides on the return leg of the rope loop, so every stroke hauls one full box out while the other goes back empty to be filled. A crew of four moves about 0.68 m³ an hour, 0.51 m³ an hour with a rest allowance, against about 0.90 m³ an hour for a bucket crew of the same four people: a ratio of 0.57 against the 0.5 asked. One box alone gave 0.43 m³ an hour. The two boxes are 210 mm wide inside so that they pass each other 42 mm apart in the room and both cross the doorway ramp in a 0.7 m door; each holds 40.3 L. Two people at the cranks need 63 N each at the 1,000 N working pull, the rope and every anchor keep a factor of at least 5 on the rope tension that the shear pin allows, and the frame now packs flat (decision 7A): two side frames of 9.2 and 9.6 kg and four bolted cross members, with the drum and its bearings the heaviest lift at 23.1 kg. The kit packs into about 454 L, 77 % of a small hatchback's boot with the rear seats folded. Value-engineering target: USD 2,000. Estimated cost of the constructable design: USD 1,055.60 (USD 944.40 under the target). Eleven of the twelve requirements are met on paper or by design, and one, R8 (setup time, now at its 20 min limit), can only be verified by a timed trial. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [B3], is the line of that script's output that carries it.

> **Safety:** SiltHaul is a rope-and-anchor system under tension with a hand-cranked chain drive. A failed anchor, rope or shackle can whip, and the chain, sprockets and cranks can trap fingers. These are first-principles estimates for a paper proof of concept; they do not show that any part is safe. Every anchor, the rope and the capstan must be proof-loaded before use (SLH-BLD-001, section 6), and nobody stands in the line of a rope or beside a sheave while the cranks turn. See SLH-PRC-001, Safety.

## Scope and method

The note checks every requirement in SLH-REQ-001 v0.4 against the design in SLH-PRC-001 v0.3 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS`, `derived()` and `masses()`, so the drum, frame, box and tail block used here are the ones in the STEP files and drawings SLH-DWG-001 and 002. It also reads `bom/bom.csv` and `budget_usd` in `project.yaml`, and writes `docs/04-calcs/results.csv`.

The design case is a ground-floor room 7 m long, with the tail sheave block at the far wall, the doorway threshold 7 m from it and the capstan drum 15 m from it (R5). Box 1, on the pull rope, is hauled 11 m from the far end of the room to a dump point outside, while box 2, on the return rope, comes back 11 m from its dump point to the far end of the room; the next stroke reverses them. A 12.5 m tail rope joins the two boxes round the tail sheaves.

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
| Trip | Loading 1.5 min, dumping 0.75 min plus 0.25 min for the crank crew to walk to the box and back; haul 11 m | Estimates |
| Boot | Small hatchback with the rear seats folded: 1,250 x 950 x 500 mm (594 L); boxed pieces may take 80 % of it | Assumed typical size; confirmed by a pack test |
| Buckets | Two shovellers each fill 10 L a minute of wet mud; carriers keep up | Estimate; no published rate found for flood mud |
| Rest | People work 75 % of the time in heat and wet | Estimate |
| Shear pin | S235 bar, ultimate shear strength 240 MPa, scatter ±20 % | 0.6 times 400 MPa tensile |
| Anchors | M12 wedge anchor in sound concrete: 4 kN tension and 6 kN shear recommended loads | Typical published values; to be confirmed on the product bought |

## A. Box capacity and load (R3)

There are now two identical boxes. Each is 210 mm wide inside and 845 mm long to the lip, with 280 mm sides and a back that slopes 110 mm. Filled level to 245 mm it holds 40.3 L, and 46.1 L to the brim [A1]. A box and its bridles weigh 17.2 kg; 40.3 L of mud weighs 68.5 kg, so a full box is 85.7 kg, or 841 N [A2]. The narrow, long box keeps the 40 L of R3 while leaving room for both boxes on lines 300 mm apart (section L).

## B. Haul force

Dragging a full box across the floor takes 589 N of friction plus 154 N for the narrower lip cutting through mud, 743 N in all [B1]. Over the 18.9 degree doorway ramp it takes 590 N, and the ropes add about 10 N of drag [B2]. The haul pull estimate for one box is 752 N; the design keeps a working pull of 1,000 N [B3]. Pulling an empty box back takes about 228 N with the rope drag [B4]. With two boxes on the loop each stroke does both at once: 752 N for the full box going out and 218 N for the empty one coming back, 970 N, still inside the 1,000 N working pull [B5].

## C. Crank force (R2)

The rope sits on the drum at a 114.5 mm radius; the chain gives 4:1 and the drive is about 91 % efficient [C1]. At the 1,000 N working pull each of two people pushes 63 N on a handle, or one person 126 N, both inside the 150 N of R2 [C2]. At the 970 N stroke estimate it is 61 N each, or 122 N for one person [C3].

## D. Speed, cycle and output (R1)

At 30 rpm on the cranks the rope moves 5.40 m a minute with a full box going out and the empty one coming back [D1]. A stroke works like this: at the end of each haul one box stands at the far end of the room and the other at the dump. The two loaders fill the box in the room (1.5 min) while the two people from the cranks walk to the other box, tip it with the tipping bar and walk back (0.75 min plus 0.25 min). Then the cranks turn the other way and haul for 2.04 min. A stroke takes 3.54 min and delivers one full box [D2]. That is 17.0 strokes and 0.68 m³ an hour with a crew of four, each person at the cranks putting in about 48 W; with one box the same crew managed 0.43 m³ an hour [D3].

*Table 2. Output against a bucket crew [D4, D5].*

| Crew of four | Output with rest | People lifting or carrying mud |
| --- | --- | --- |
| Shovels and buckets (two filling, two carrying) | 0.90 m³/h | All four; each cubic metre is 1.7 t lifted about 1 m and about 2.2 km walked carrying 10 L buckets |
| SiltHaul, two boxes (two cranking and dumping, two loading) | 0.51 m³/h | None; loaders push mud in over the lip at floor level |

The ratio is 0.57 against the 0.5 of R1 as Amish restated it, so **R1 is met on paper**, and nobody lifts or carries mud. The margin is small and rests on estimated loading, dumping and bucket rates; the timed trial of R1 at TRL 4 settles both numbers. Hand power still sets the haul speed: the second box doubles what each stroke delivers, not how fast the rope moves.

## E. Drum and rope storage (R5)

The drum has a 229.1 mm pitch diameter, 720 mm of rope a turn. Twelve metres of box travel is 16.7 turns, and each half stores 21 turns, which includes three dead turns and one spare [E1]. Each half is 236 mm long at an 11 mm winding pitch, and the drum is 484 mm between its outer faces [E2]. The drum is smooth, so the rope must reach it at no more than about 1.5 degrees from square. With the capstan 6 m from the ramp roller the worst fleet angle is 1.41 degrees, and 1.06 degrees at the design case of 8 m [E3, E4]. The capstan therefore stands at least 6 m beyond the door, which leaves rooms up to 9 m long within the 15 m of R5.

## F. Overload limit (R11)

A 4 mm S235 pin in double shear across the 25 mm crank shaft carries 75.4 N m, which is a rope tension of 2,451 N when it shears [F1]. With ±20 % scatter it releases between 1,961 and 2,941 N, so the design maximum rope tension is 3,000 N [F2]. Without the pin, two people heaving 400 N each on the cranks could put 6,372 N into a jammed rope [F3]; the pin is what lets every part below be sized on 3,000 N.

## G. Rope (R6)

An 18 kN rope, 16.2 kN through an eye splice, has a factor of 18 on the working pull and 5.4 on the overload limit [G1]. The rope bends round the drum at 22 times its diameter, round the tail sheaves at 12.5 and over the ramp roller at 6, where it turns only a few degrees [G2].

## H. Capstan anchor and stability

The capstan anchor carries 1,100 N while hauling and 3,250 N at the overload limit; the 2,000 kg round sling has 19.6 kN of working load, six times that, and each shackle 9.8 kN [H1]. The capstan, with its bolted frame, weighs 65.7 kg and its weight holds 271 N m about its front edge [H2]. The sling is shackled to an eye 200 mm up, level with the drum axis, so the rope pull and the sling pull nearly line up. With the sling level the frame is held back by 315 N m; with it rising 5.7 degrees by 54 N m; at 10 degrees the tipping moment is 145 N m, still inside the 271 N m [H3 to H5]. The anchor bar that carries the sling is now bolted between the rear braces with two M12 bolts at each end, each in shear at about 1.6 kN at the overload limit. The rule is therefore that the sling runs level or rises 10 degrees at most, for example a 3 m sling to a point no higher than 500 mm. The ground stakes stop the frame skating sideways and are not counted as the anchor.

## I. Tail sheave block (R7)

With two boxes the tail rope always drags the empty box back, so the tail block carries about 636 N on either stroke. If a box going back jammed and the crew cranked until the pin sheared, it would carry both legs at 3,000 N, 6,000 N in all [I1]. Each of the four M12 anchors then takes 1,500 N of shear and 818 N of tension, 0.45 of the typical recommended loads [I2]. Each 25 mm sheave pin takes 4,243 N at 50 mm above the plate, a bending stress of 138 MPa against 355 MPa yield [I3]. R7 is met on paper on a sound concrete slab; the anchors are only as good as the slab, which is checked on site (SLH-BLD-001, section 6).

## J. Shafts, chain and ratchet (R12)

At the overload limit the 30 mm drum shaft sees 44 MPa of bending and 65 MPa of torsion, 121 MPa combined [J1]. The chain pull is 3,539 N, a factor of 5.0 on the 17.8 kN breaking load of ISO 08B-1 chain [J2]. The 25 mm crank shaft sees 93 MPa combined before the cross hole; the hole roughly doubles the local stress, which stays below yield [J3]. A ratchet tooth carries 4,091 N, 57 MPa on its 12 x 6 mm face, and the pawl pin 36 MPa in shear [J4].

## K. Stability in the haul and tipping at the dump

A full box has its centre of mass 458 mm behind the lip, so its weight holds it level with 385 N m [K1]. The pull at the bridle ring, 75 mm up, tries to tip it nose-down with 75 N m at the working pull and 225 N m at the overload limit, both less [K2]. To dump, the end of the tipping bar is lifted 1,539 mm behind the lip: about 236 N to start a full box, falling as the mud slides out [K3]. That is more than one person should lift repeatedly, so the two people from the cranks share the bar, about 118 N each.

## L. Doorway fit, setup, mass, packing and cost (R4, R8, R9, R10)

Each box is 214 mm wide and 258 mm over its shackle pins. On lines 300 mm apart the two boxes pass each other 42 mm apart in the room, and the ramp, now centred between the two lines, carries both 26 mm inside its cheeks; it is 646 mm outside, inside a 700 mm opening [L1]. The model checks both clearances. Setting up takes about 27 min of tasks, about 20 min with three people working in parallel, at the R8 limit, because the frame is bolted together on site (3 min) and two boxes are shackled (4 min); only a timed trial can confirm it [L2]. The heaviest single lifts are the drum with its bearings at 23.1 kg, a box at 16.1 kg, the tail plate at 11.0 kg and a side frame at 9.6 kg [L3].

The flat-pack frame comes apart into two welded side frames, each 890 x 814 x 83 mm and 9.2 or 9.6 kg, and four cross members 516 mm long: the front and rear cross rails, the top tie and the anchor bar with its eye [L3a]. Each cross member has an 8 mm end plate at each end that bolts to the inside face of a side frame, with two M10 bolts for the rails and the tie and two M12 bolts for the anchor bar. Taking a small car boot as a small hatchback with the rear seats folded, 1,250 x 950 x 500 mm or 594 L, every piece fits and the boxed volume of the kit is about 454 L, 77 % of the space, with the rope bag, crank bearings and chain (30 L) carried inside the boxes and the ramp taken apart [L3b]. R9 is therefore met on paper with the seats folded. With the seats up the load floor is about 950 x 650 mm and the side frames do not lie flat in it [L3c]; whether that reading of "small car boot" is enough is put to Amish in the design decisions register.

Value-engineering target: USD 2,000. Estimated cost of the constructable design: USD 1,055.60 (USD 944.40 under the target) [L4]. The rise of USD 168.10 is the second box (USD 80), its bridles (USD 54), 7 m more rope, the frame's end plates and drilling (USD 10), twelve frame bolts (USD 8) and paint (USD 5). The whole kit weighs about 154 kg with rope and sling [L5].

## M. Results against every requirement

*Table 3. Requirement status from this note [M].*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R8 | Setup time | About 20 min with three people (estimate), at the limit | 20 min or less | Not verifiable at TRL 3 |
| R1 | Output | 0.51 m³/h against 0.90 m³/h for buckets (ratio 0.57); nobody lifts or carries mud | No lifting or carrying of mud; at least 0.5 times the bucket crew | Met on paper |
| R9 | Portability | Heaviest lift 23.1 kg; flat-pack frame, largest piece 890 x 814 x 83 mm; kit about 454 L in a 594 L small car boot | Restated R9: fits a small hatchback with the rear seats folded; heaviest part 25 kg or less | Met on paper (accepted by Amish, SLH-DDR-004) |
| R2 | Crank force | 63 N each with two at the cranks (126 N for one) at 1,000 N | 150 N or less | Met on paper |
| R6 | Rope and anchor strength | Rope factor 18 working, 5.4 at the 3,000 N limit; chain 5.0 | At least 5 times the working pull | Met on paper |
| R7 | Tail anchor independent of walls | Four M12 anchors in the slab, 0.45 of recommended loads at the limit | Holds on a bare concrete floor, no wall contact | Met on paper (sound slab assumed) |
| R10 | Cost | USD 1,055.60 | Value-engineering target USD 2,000 | Met on paper, within the target |
| R11 | Overload limit | Shear pin releases at 2,451 N (1,961 to 2,941 N) | Rope tension limited to 3,000 N | Met on paper |
| R3 | Box capacity | 40.3 L a box at a 245 mm fill (46 L to the brim) | About 40 L | Met by design |
| R4 | Fits a doorway | Boxes 258 mm over the shackles, pass 42 mm apart; ramp 646 mm; tail plate 440 mm | Pass a 0.7 m opening | Met by design |
| R5 | Working length | 21 turns a half store 12 m of travel; capstan at least 6 m from the door | Up to 15 m tail to capstan | Met by design |
| R12 | Holds when let go | Two ratchet wheels and pawls on the drum shaft, one each way | Holds the load when the cranks are let go | Met by design |

Counts: 1 not verifiable at TRL 3, 7 met on paper, 4 met by design; none not met or at risk.

## Checks against the TRL 2 figures

| TRL 2 claim (SLH-PRC-001 v0.2) | This note | Action |
| --- | --- | --- |
| Friction capstan with a rope loop | A loop on a friction drum needs a pretension of about half the pull and walks along the drum | Split winding drum (SLH-DDR-002) |
| Working pull about 1 kN | 917 N estimate; 1,000 N used | None |
| Twice the bucket output | 0.36 times with one box; 0.57 with two | R1 restated by Amish to 0.5 times and met with a second box (SLH-DDR-003) |
| Anchors sized on the working pull | A jammed box and two heaving people reach 6.4 kN | Shear pin limits rope tension to 3,000 N (R11) |
