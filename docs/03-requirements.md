---
doc_id: SLH-REQ-001
title: SiltHaul requirements
project: SiltHaul
doc_type: Requirements
version: "0.4"
status: Draft
date: '2026-10-03'
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
---

# SiltHaul requirements

Eleven of the twelve requirements are met on paper or by design, one (R8, setup time, now estimated at the 20 min limit) can only be verified by a timed trial, and none is reported not met (SLH-CAL-001 v0.3, Table 3). On 2026-10-03 Amish chose option A on every requirement decision put to him ("1A 2A 3A 4A 5A 6A 7A 8A 9A 10A 11A"), which for SiltHaul meant two changes (SLH-DDR-003). Under 2A, R1 is restated as "no lifting or carrying of mud; output at least 0.5 times the same crew with shovels and buckets", and a second box rides on the return leg so the rope loop carries mud out on both strokes: about 0.51 m³ an hour with rest, a ratio of 0.57. Under 7A, the frame is a bolted flat-pack frame so the kit fits a small car boot, with the 25 kg heaviest-part limit kept. R11 and R12 were added at TRL 2 under Amish's pre-approval of 2026-10-03 (SLH-DDR-001), because the anchors and rope can only be sized on a known maximum rope tension, and a hand-cranked load must hold when the handles are let go. "Met on paper" means shown by calculation, not by test.

> **Safety:** SiltHaul is a rope-and-anchor system under tension with a hand-cranked chain drive. R6, R7, R11 and R12 are its safety requirements; they are checked on paper only and must be proved by proof-load tests before anyone uses the kit (SLH-BLD-001, section 6).

Table 1. Requirements and status at TRL 3

| ID | Requirement | Target | Verification (TRL 3 or later) | Status (SLH-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Mud moved per hour by a crew of four | No lifting or carrying of mud; output at least 0.5 times that of the same crew with shovels and buckets (estimate) | Side-by-side timed trial on a test bed of wet silt | Met on paper: 0.51 against 0.90 m³/h (ratio 0.57); loaders push mud in over the lip; nobody lifts or carries it |
| R2 | Crank handle force at full box | 150 N (34 lbf) or less per person with two people at the cranks | Spring balance at the handle during trial | Met on paper: 63 N each at 1,000 N (126 N for one person); 61 N each at the 970 N stroke estimate |
| R3 | Scraper box capacity | About 40 L (10 US gal) of wet mud per trip | Measured fill on test bed | Met by design: 40.3 L in each of the two boxes at a 245 mm fill |
| R4 | Fits through a doorway | Box, tail block and ramp pass a 0.7 m (28 in) opening, with the return leg beside the box | Fit test | Met by design: each box 258 mm over the shackles; the boxes pass 42 mm apart and cross the ramp 26 mm inside its cheeks; ramp 646 mm |
| R5 | Working length | Up to 15 m (49 ft) from tail sheave to capstan | Trial at full length | Met by design: 12 m of travel on each drum half; capstan at least 6 m from the door |
| R6 | Rope and anchor strength | Minimum break strength at least 5 times the working pull, and at least 5 times the R11 limit for the rope and chain | CalRig proof-load test of each anchor type | Met on paper: rope 18 times working, 5.4 at the limit; chain 5.0 |
| R7 | Tail anchor independent of walls | Holds the R11 limit on both legs on a bare concrete floor with no wall contact | Pull test on the anchored tail block | Met on paper on a sound slab: 0.45 of recommended anchor loads |
| R8 | Setup time | Three people set up in 20 min or less | Timed trial | Not verifiable at TRL 3: about 20 min estimated, at the limit (bolting the frame and shackling two boxes add 4 min) |
| R9 | Portability | Complete kit fits in a car boot; heaviest part 25 kg (55 lb) or less | Weigh and pack test | Met on paper with the rear seats folded: heaviest lift 23.1 kg (drum with bearings); flat-pack frame, largest piece 890 x 814 x 83 mm; kit about 454 L packed against a 594 L small car boot |
| R10 | Cost | Prototype parts at or under the USD 2,000 value-engineering target (a hypothetical control target) | Costed bill of materials | Met on paper, within the target: USD 1,055.60 (USD 944.40 under) |
| R11 | Overload limit | Rope tension limited to 3,000 N whatever force the crew applies | Shear pin release test on the capstan | Met on paper: shear pin releases at 2,451 N (1,961 to 2,941 N) |
| R12 | Holds when let go | The drum holds the load in either direction when the cranks are released | Release test at working pull | Met by design: two ratchet wheels and pawls on the drum shaft |

## Requirements at risk or not met

None is reported not met. Two results are close to their limits and are watched at TRL 4:

- **R1.** The ratio of 0.57 rests on estimated loading, dumping and bucket rates; a timed trial settles it. The restatement is Amish's (2A, 2026-10-03): "no lifting or carrying of mud; output at least 0.5 times the same crew with shovels and buckets".
- **R8.** About 20 min with three people, at the limit, now that the frame is bolted together on site and two boxes are shackled.
- **R9.** Met with the rear seats of a small hatchback folded. With the seats up the 890 x 814 mm side frames do not lie flat in a typical small boot; see the design decisions register.

## Assumptions

- Most flood mud is fluid enough to be scraped and dragged, not dug; very stiff or deep deposits may still need shovels first.
- The building has a sound concrete slab at least 100 mm thick for the tail block anchors; where it does not, SiltHaul is not used in that room.
- Volunteers accept a short briefing on rope safety.
- A small car boot is taken as a small hatchback's load space with the rear seats folded: 1,250 mm long, 950 mm wide and 500 mm high (about 594 L).
- Loaders push or rake mud into the box over its lip at floor level; the box is 305 mm tall, so shovelling over the side is possible but not needed.
- A safe dump point exists outside within rope reach, and an anchor point (a sound tree or a parked vehicle) exists behind the capstan.
