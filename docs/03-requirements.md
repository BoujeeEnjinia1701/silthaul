---
doc_id: SLH-REQ-001
title: SiltHaul requirements
project: SiltHaul
doc_type: Requirements
version: "0.3"
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
---

# SiltHaul requirements

Nine of the twelve requirements are met on paper or by design, one is at risk, one can only be verified by a timed trial and one is not met (SLH-CAL-001, Table 3). The miss is R1, output: about 0.32 m³ an hour against about 0.90 m³ an hour for a bucket crew of the same size, because two people at a crank can only give about 50 W each. SiltHaul's gain is that nobody lifts or carries mud out of the building. R11 and R12 were added at TRL 2 under Amish's pre-approval of 2026-10-03 (SLH-DDR-001), because the anchors and rope can only be sized on a known maximum rope tension, and a hand-cranked load must hold when the handles are let go. "Met on paper" means shown by calculation, not by test.

> **Safety:** SiltHaul is a rope-and-anchor system under tension with a hand-cranked chain drive. R6, R7, R11 and R12 are its safety requirements; they are checked on paper only and must be proved by proof-load tests before anyone uses the kit (SLH-BLD-001, section 6).

Table 1. Requirements and status at TRL 3

| ID | Requirement | Target | Verification (TRL 3 or later) | Status (SLH-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Mud moved per hour by a crew of four | At least twice the volume moved by the same crew with shovels and buckets (estimate) | Side-by-side timed trial on a test bed of wet silt | **Not met on paper:** 0.32 against 0.90 m³/h (ratio 0.36); nobody carries mud |
| R2 | Crank handle force at full box | 150 N (34 lbf) or less per person with two people at the cranks | Spring balance at the handle during trial | Met on paper: 63 N each at 1,000 N (126 N for one person) |
| R3 | Scraper box capacity | About 40 L (10 US gal) of wet mud per trip | Measured fill on test bed | Met by design: 40.7 L at a 165 mm fill |
| R4 | Fits through a doorway | Box, tail block and ramp pass a 0.7 m (28 in) opening, with the return leg beside the box | Fit test | Met by design: 494 mm over the shackles; ramp 646 mm |
| R5 | Working length | Up to 15 m (49 ft) from tail sheave to capstan | Trial at full length | Met by design: 12 m of travel on each drum half; capstan at least 6 m from the door |
| R6 | Rope and anchor strength | Minimum break strength at least 5 times the working pull, and at least 5 times the R11 limit for the rope and chain | CalRig proof-load test of each anchor type | Met on paper: rope 18 times working, 5.4 at the limit; chain 5.0 |
| R7 | Tail anchor independent of walls | Holds the R11 limit on both legs on a bare concrete floor with no wall contact | Pull test on the anchored tail block | Met on paper on a sound slab: 0.45 of recommended anchor loads |
| R8 | Setup time | Three people set up in 20 min or less | Timed trial | Not verifiable at TRL 3: about 17 min estimated |
| R9 | Portability | Complete kit fits in a car boot; heaviest part 25 kg (55 lb) or less | Weigh and pack test | **At risk:** heaviest lift 24.7 kg; frame 890 x 663 x 814 mm needs an estate car or small pickup |
| R10 | Cost | Prototype parts at or under the USD 2,000 value-engineering target (a hypothetical control target) | Costed bill of materials | Met on paper, within the target: USD 887.50 (USD 1,112.50 under) |
| R11 | Overload limit | Rope tension limited to 3,000 N whatever force the crew applies | Shear pin release test on the capstan | Met on paper: shear pin releases at 2,451 N (1,961 to 2,941 N) |
| R12 | Holds when let go | The drum holds the load in either direction when the cranks are released | Release test at working pull | Met by design: two ratchet wheels and pawls on the drum shaft |

## Requirements at risk or not met

- **R1 (not met).** Hand power sets the haul speed. Ways to close the gap belong to TRL 4 trials: a second box on the return leg so both strokes carry mud, or a crew of six with two at the cranks and four loading. Both change what the product is, so they are not made here.
- **R9 (at risk).** The frame is 25 mm inside the mass limit and too tall for some small hatchbacks. A bolted frame that packs flat is a later option.

## Assumptions

- Most flood mud is fluid enough to be scraped and dragged, not dug; very stiff or deep deposits may still need shovels first.
- The building has a sound concrete slab at least 100 mm thick for the tail block anchors; where it does not, SiltHaul is not used in that room.
- Volunteers accept a short briefing on rope safety.
- A safe dump point exists outside within rope reach, and an anchor point (a sound tree or a parked vehicle) exists behind the capstan.
