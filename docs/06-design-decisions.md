---
doc_id: SLH-DEC-001
title: SiltHaul design decisions register
project: SiltHaul
doc_type: Design decisions register
version: "0.2"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: Register opened; every decision made under Amish's pre-approval of 2026-10-03
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: Amish's requirement decisions 2A and 7A recorded (SLH-DDR-003); boot reading for R9 opened for Amish
---

# SiltHaul design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list decisions.

> **Safety:** Several decisions below set SiltHaul's safety case (overload limit, holding, anchors, dumping). Each took the conservative option; the evidence that would relax it is in SLH-DDR-001, Table 1.

## Open decisions

| # | To decide | Options | Recommendation | What it affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | What "fits a small car boot" in R9 means. State: with the flat-pack frame the kit packs into about 454 L, 77 % of a small hatchback's load space with the rear seats folded (1,250 x 950 x 500 mm); with the seats up the 890 x 814 mm side frames do not lie flat in a typical 950 x 650 mm boot floor. | A: accept the rear seats folded as the reference and record R9 as met on paper. B: split each side frame into bolted tubes (rails, posts, braces) so everything fits with the seats up, at about forty bolts and well over 20 min of setup (R8). | A: the seats-folded space is what a volunteer's small car offers in practice, and B breaks R8. | B would replace the side frame making sketch and add about 28 bolts and their holes | SLH-DDR-003; SLH-CAL-001, L3b and L3c |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | Release load of the shear pins from the bar actually bought | The 4 mm pin is sized on 240 MPa shear; a stronger bar raises the overload limit above 3,000 N | SLH-CAL-001, F; R11 |
| 2 | Recommended loads of the M12 wedge anchor bought, in the concrete grade expected | The tail block check uses 4 kN tension and 6 kN shear | SLH-CAL-001, I; R7 |
| 3 | Rope breaking strength and splice efficiency of the rope bought | Factor 5.4 at the limit assumes 18 kN and 90 % at the splice | SLH-CAL-001, G; R6 |
| 4 | Sheave bore and rating | Pins are 25 mm; the sheaves must be rated at least 1,000 kg | BOM line 14 |
| 5 | Bearing centre heights and bolt pitches | The pads and top plates are drilled to UCP206 and UCP205 catalogue sizes | SLH-DWG-101 |
| 6 | Sprocket bores and the 12-tooth sprocket's fit on the 36 mm hub | Sets the hub and the line-up with the 48-tooth wheel | SLH-DWG-104 |

## Value engineering

Value-engineering target: USD 2,000 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 1,055.60 (USD 944.40 under the target). Main cost drivers and savings worth trying:

- The two boxes (USD 160) and the winding drum (USD 98) are the largest made parts; the rope (USD 80.60), the ramp (USD 73) and the frame (USD 72) follow.
- Bought lifting gear (sling, shackles, two bridle sets, USD 164) is kept at rated, traceable grades because it carries the safety case.
- Savings worth trying: a drum from a scrap gas cylinder or pipe offcut of the same diameter; a timber ramp with a steel wear strip; buying rope with factory eye splices in bulk.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-10-03 | Split winding drum in place of a friction capstan; 4:1 chain drive with two cranks | Amish: "I pre-approve the batch runs along with any recommendations you come up with." | SLH-DDR-001, items 1, 2 |
| 2026-10-03 | Shear pin limits rope tension to about 2.5 kN; all parts sized on 3,000 N; requirement R11 added | Amish: "I pre-approve the batch runs along with any recommendations you come up with." | SLH-DDR-001, item 3 |
| 2026-10-03 | Two opposite ratchet wheels and pawls on the drum shaft; requirement R12 added | Amish: "I pre-approve the batch runs along with any recommendations you come up with." | SLH-DDR-001, item 4 |
| 2026-10-03 | Tail block on four drilled floor anchors only, never walls or door frames | Amish: "I pre-approve the batch runs along with any recommendations you come up with." | SLH-DDR-001, item 5 |
| 2026-10-03 | Capstan anchored by a round sling to a tree or vehicle, level or rising 10 degrees at most; stakes only against skating | Amish: "I pre-approve the batch runs along with any recommendations you come up with." | SLH-DDR-001, item 6 |
| 2026-10-03 | 10 mm polyester double braid, 18 kN | Amish: "I pre-approve the batch runs along with any recommendations you come up with." | SLH-DDR-001, item 7 |
| 2026-10-03 | Box open toward the door, sloped back, forward tipping; two people on the tipping bar | Amish: "I pre-approve the batch runs along with any recommendations you come up with." | SLH-DDR-001, items 8, 9 |
| 2026-10-03 | Capstan at least 6 m beyond the door | Amish: "I pre-approve the batch runs along with any recommendations you come up with." | SLH-DDR-001, item 10 |
| 2026-10-03 | First co-design candidate to approach: Kerala State Disaster Management Authority (not agreed) | Amish: "I pre-approve the batch runs along with any recommendations you come up with." | SLH-DDR-001, item 11 |
| 2026-10-03 | SiltHaul capstan recorded as the candidate common block for SaltDrag; CalRig as the first candidate proof-load rig | Amish: "I pre-approve the batch runs along with any recommendations you come up with." | SLH-DDR-001, item 12 |
| 2026-10-03 | `budget_usd` kept at 2,000 as a value-engineering target | Amish: "I also accept any cost overruns or variations from the assumed scope cost." | SLH-DDR-001, item 13 |
| 2026-10-03 | R1 kept as the trial target and reported not met on paper (superseded by 2A below) | Amish: "I pre-approve the batch runs along with any recommendations you come up with." | SLH-DDR-001, Consequences |
| 2026-10-03 | Design for construction: the thirteen changes of SLH-DDR-002 | Amish: "I pre-approve the batch runs along with any recommendations you come up with." | SLH-DDR-002 |
| 2026-10-03 | Appearance model additions for renders: wound rope on the drum, stakes above ground only, context wall, tree and mannequin | Amish: "I pre-approve the batch runs along with any recommendations you come up with." | docs/REVIEW.md, TRL 3 |
| 2026-10-03 | 2A: second box on the return leg so the rope loop carries mud both ways; R1 restated as "no lifting or carrying of mud; output at least 0.5 times the same crew with shovels and buckets" (now 0.57, met on paper) | Amish: "1A 2A 3A 4A 5A 6A 7A 8A 9A 10A 11A" | SLH-DDR-003, items 1 to 5 |
| 2026-10-03 | 7A: bolted flat-pack frame (two welded side frames, four bolted cross members) that fits a small car boot, keeping the 25 kg heaviest-part limit (heaviest lift 23.1 kg) | Amish: "1A 2A 3A 4A 5A 6A 7A 8A 9A 10A 11A" | SLH-DDR-003, items 6 to 8 |
