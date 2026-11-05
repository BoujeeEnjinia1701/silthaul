---
doc_id: SLH-PRS-001
title: SiltHaul product requirements and specifications
project: SiltHaul
doc_type: Product requirements and specifications
version: "0.6"
status: Draft
date: 2026-11-03
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: TRL 2 requirements with concept status; R11 overload limit and R12 load holding added (SLH-DDR-001)
- version: "0.3"
  date: '2026-10-03'
  author: Amish Chadha
  change: TRL 3 status from SLH-CAL-001 on the constructable design (SLH-DDR-002); R10 restated against the value-engineering target
- version: "0.4"
  date: '2026-10-03'
  author: Amish Chadha
  change: Amish's requirement decisions (SLH-DDR-003); R1 restated (no lifting or carrying of mud; at least 0.5 times the bucket crew) and met on paper with a second box on the return leg; R9 met on paper with a flat-pack frame; status rerun from SLH-CAL-001 v0.3
- version: "0.6"
  date: '2026-10-03'
  author: Amish Chadha
  change: "Amish's round-2 decision 2A (SLH-DDR-004): R9 restated as \"fits a small hatchback with the rear seats folded; heaviest part 25 kg or less\" and accepted as met on paper"
- version: "0.6"
  date: 2026-11-03
  author: Amish Chadha
  change: "Kit 1.9.1: migrated to the product requirements format (PR-001 to PR-012 are R1 to R12, wording unchanged), traced to the user requirements in SLH-URS-001; PR-013 to PR-018 added for the new user needs; status rerun on the detailed model (heaviest lift 22.2 kg, kit 407 L)"
---

# SiltHaul product requirements and specifications

Fourteen of the eighteen product requirements are met on paper or by design for option A, two are at risk (PR-001 by a hair and PR-006, the chain just under its factor of 5), two (PR-008, setup time, and PR-014, durability) can only be verified at TRL 4, and none is reported not met (SLH-CAL-001 v0.5, Table 3). PR-001 to PR-012 are the twelve requirements R1 to R12 that Amish accepted on 2026-10-03 and 2026-10-03 round 2 (SLH-DDR-003, SLH-DDR-004), with their wording unchanged; the "Was" column keeps the old numbers. PR-013 to PR-018 were added at the kit 1.9.1 upgrade so that every user need in SLH-URS-001 has a product requirement; they are proposals, awaiting Amish. "Met on paper" means shown by calculation, not by test. The statuses are for option A, the existing design; the other options are scored against the same needs in SLH-OPT-001.

> **Safety:** SiltHaul is a rope-and-anchor system under tension with a hand-cranked chain drive. PR-006, PR-007, PR-011, PR-012 and PR-016 are its safety requirements; they are checked on paper only and must be proved by proof-load tests before anyone uses the kit (SLH-BLD-001, section 6).

Table 1. Product requirements and specifications.

| ID | Traces to | Category | Title | Requirement | Target | Tolerance | Units | Verification | Status | Was |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR-001 | UR-001, UR-002 | Performance | Mud moved per hour by a crew of four | No lifting or carrying of mud; output at least 0.5 times that of the same crew with shovels and buckets (estimate) | 0.5 | min | ratio to a bucket crew | Side-by-side timed trial on a test bed of wet silt (TRL 4) | Met on paper, at risk: 0.51 against 0.90 m3/h (ratio 0.57) with a 1.5 min fill; 0.497 if the loaders fill at a shoveller's 10 L/min (SLH-CAL-001 D6); loaders push mud in over the lip; nobody lifts or carries it | R1 |
| PR-002 | UR-003 | Usability | Crank handle force at full box | 150 N (34 lbf) or less per person with two people at the cranks | 150 | max | N per person | Spring balance at the handle during trial (TRL 4) | Met on paper: 63 N each at 1,000 N (126 N for one person); 61 N each at the 977 N stroke estimate | R2 |
| PR-003 | UR-002 | Performance | Scraper box capacity | About 40 L (10 US gal) of wet mud per trip | 40 | nominal | L | Measured fill on test bed (TRL 4) | Met by design: 40.3 L in each of the two boxes at a 245 mm fill | R3 |
| PR-004 | UR-004 | Physical architecture | Fits through a doorway | Box, tail block and ramp pass a 0.7 m (28 in) opening, with the return leg beside the box | 700 | max | mm | Fit test (TRL 4) | Met by design: each box 258 mm over the shackles; the boxes pass 42 mm apart and cross the ramp 26 mm inside its cheeks; ramp 646 mm | R4 |
| PR-005 | UR-005 | Performance | Working length | Up to 15 m (49 ft) from tail sheave to capstan | 15 | min | m | Trial at full length (TRL 4) | Met by design: 12 m of travel on each drum half; capstan at least 6 m from the door | R5 |
| PR-006 | UR-006 | Safety | Rope and anchor strength | Minimum break strength at least 5 times the working pull, and at least 5 times the PR-011 limit for the rope and chain | 5 | min | factor | CalRig proof-load test of each anchor type (TRL 4) | At risk: rope 18 times working, 5.4 at the limit; chain 4.93 at the 3,000 N limit (5.03 at the 2,941 N the pin can release); fix proposed to Amish (SLH-STM-001 S5) | R6 |
| PR-007 | UR-006 | Safety | Tail anchor independent of walls | Holds the PR-011 limit on both legs on a bare concrete floor with no wall contact | 3000 | min | N rope tension | Pull test on the anchored tail block (TRL 4) | Met on paper on a sound slab: 0.45 of recommended anchor loads | R7 |
| PR-008 | UR-007 | Usability | Setup time | Three people set up in 20 min or less | 20 | max | min | Timed trial (TRL 4) | To verify at TRL 4: about 20 min estimated, at the limit (bolting the frame and shackling two boxes add 4 min) | R8 |
| PR-009 | UR-008 | Packaging and transport | Portability | Kit fits a small hatchback with the rear seats folded; heaviest part 25 kg or less (25 kg is 55 lb) | 25 | max | kg | Weigh and pack test (TRL 4) | Met on paper, as restated by Amish (2A, round 2): heaviest lift 22.2 kg (drum with bearings); flat-pack frame, largest piece 890 x 814 x 83 mm; kit about 407 L packed against a 594 L small car boot | R9 |
| PR-010 | UR-009 | Physical architecture | Cost | Prototype parts at or under the USD 2,000 value-engineering target (a hypothetical control target) | 2000 | max | USD | Costed bill of materials | Met on paper, within the target: USD 1,055.60 (USD 944.40 under) | R10 |
| PR-011 | UR-006 | Safety | Overload limit | Rope tension limited to 3,000 N whatever force the crew applies | 3000 | max | N | Shear pin release test on the capstan (TRL 4) | Met on paper: shear pin releases at 2,451 N (1,961 to 2,941 N) | R11 |
| PR-012 | UR-006 | Safety | Holds when let go | The drum holds the load in either direction when the cranks are released | 2 | min | ratchets and pawls | Release test at working pull (TRL 4) | Met by design: two ratchet wheels and pawls on the drum shaft | R12 |
| PR-013 | UR-010 | Materials | Made from stock | Every made part is cut, drilled, bent or welded from stock sections, sheet, bar and tube; bought parts are commercial catalogue items; no part needs machining beyond drilling and sawing | 1 | nominal | local workshop | Analysis of the BOM and the 245-part model (TRL 3); prototype build (TRL 4) | Met by design: 40 x 40 x 2 SHS, 219.1 x 3 tube, sheet and bar; UCP bearings, 08B-1 chain and sprockets, rope and fasteners bought | |
| PR-014 | UR-011 | Materials | Survives mud and wet | Steel parts painted or zinc plated; bearings sealed and greaseable; all surfaces that touch mud can be hosed clean with no closed pockets | 1 | nominal | coating and wash-down | Wash-down and inspection after a trial (TRL 4) | To verify at TRL 4: coatings and sealed UCP bearings in the BOM; coating life not assessed | |
| PR-015 | UR-012 | Safety | Crank crew clear of the mud | The capstan stands outside the door, at least 6 m from the ramp roller, so the crank crew is out of the mud; loaders push mud into the box at floor level | 6 | min | m | Layout drawing SLH-DWG-002; timed trial (TRL 4) | Met by design: capstan at least 6 m from the ramp roller (fleet angle 1.41 degrees); loaders push mud in at floor level | |
| PR-016 | UR-006 | Safety | Moving parts guarded | The chain and both sprockets are closed by a fixed guard; ratchet wheels and pawls are on the outer face of the frame, clear of the crank crew | 1 | min | closed guard | Inspection of the prototype (TRL 4) | Met by design: closed 1.5 mm sheet chain guard (BOM 9) held by two M6 screws | |
| PR-017 | UR-003 | Usability | Tipping a full box | Two people on the tipping bar start a full box tipping with 150 N or less each | 150 | max | N per person | Spring balance at the bar (TRL 4) | Met on paper: 237 N to start a full box, 119 N each with two people (SLH-CAL-001 K3) | |
| PR-018 | UR-013 | Performance | No added water | The kit moves the mud as it is and adds no water, so the wet waste leaving the room equals the mud removed | 1 | max | m3 delivered per m3 of mud | Analysis (TRL 3) | Met by design for option A (no flush water); option C would deliver 2.8 m3 per m3 (SLH-OPT-001) | |

Status words: met on paper, met by design, at risk, not met, over target, withdrawn, to verify at TRL 4.

## Requirements at risk or not met

None is reported not met for option A. Two are at risk and the rest wait for TRL 4:

- **PR-006 (R6).** Drum bearing friction raises the chain pull to 3,612 N at the 3,000 N limit, a factor of 4.93 on the 17.8 kN breaking load, just under 5; 5.03 at the 2,941 N the pin can release. The independent review found it. Three fixes are put to Amish (SLH-STM-001 S5): a 3.5 mm pin (limit about 2.25 kN), duplex 08B-2 chain, or accept it.
- **PR-001 (R1).** The ratio of 0.57 rests on estimated loading, dumping and bucket rates and on loaders filling 13.4 L/min each; at a shoveller's 10 L/min the ratio is 0.497 (SLH-CAL-001 D6). A timed trial settles it. The restatement is Amish's (2A, 2026-10-03): "no lifting or carrying of mud; output at least 0.5 times the same crew with shovels and buckets".
- **PR-008 (R8).** About 20 min with three people, at the limit, now that the frame is bolted together on site and two boxes are shackled.
- **PR-009 (R9).** Accepted by Amish with the rear seats folded (round 2, 2A, 2026-10-03: "i agree with all the 46 recommendations you provided. please proceed."). With the seats up the 890 x 814 mm side frames do not lie flat in a typical small boot; that is no longer an open question.
- **PR-011 (R11).** The release of 2,451 N rests on a shear strength of 240 MPa and 20 % scatter; the release test at TRL 4 settles it.

For the other options (SLH-OPT-001): option B does not meet PR-002 (189 N each with four people) and has no PR-011 or PR-012 equivalent; option C does not meet PR-001 (0.49), PR-002 (183 N each with two people) or PR-018 (2.8 m3 per m3).

## Assumptions

- Most flood mud is fluid enough to be scraped and dragged, not dug; very stiff or deep deposits may still need shovels first.
- The building has a sound concrete slab at least 100 mm thick for the tail block anchors; where it does not, SiltHaul is not used in that room.
- Volunteers accept a short briefing on rope safety.
- "A small hatchback with the rear seats folded" is taken as a small hatchback's load space with the rear seats folded: 1,250 mm long, 950 mm wide and 500 mm high (about 594 L).
- The detailed model of kit 1.9.1 (245 parts) changed the packed volume from 454 L to 407 L and the heaviest lift from 23.1 kg to 22.2 kg because the drum and fasteners are now modelled part by part; no design dimension changed.
