---
doc_id: SLH-DDR-002
title: SiltHaul design for construction
project: SiltHaul
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: Constructability review and changes that make the design buildable, decided under Amish's pre-approval of 2026-10-03
---

# 0002: Design for construction

- **Date:** 2026-10-03
- **Status:** accepted

## Context

STANDARDS section 18 asks for every part to be makeable by its stated process and to fit and fasten to its neighbours (Amish, 2026-09-30: "fix the design assumptions to match and be physically feasible"). The TRL 2 concept (SLH-PRC-001 v0.2, SLH-DDR-001) was reviewed part by part in `cad/src/model.py`: how each part is made, how it joins each neighbour, and build123d checks for overlapping parts and for parts that do not touch what holds them. The checks now report no overlaps and no floating parts. Amish pre-approved every recommendation on 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." No change alters what SiltHaul does or its pitch; the safety-related changes all take the conservative side.

## Options considered

For each problem the simplest physically sound fix was chosen; the alternatives are noted in Table 1.

## Decision

*Table 1. Changes made for construction.*

| # | Part | Problem found | Change | Why |
| --- | --- | --- | --- | --- |
| 1 | Capstan frame | Over 25 kg in 40 x 40 x 3 tube with solid braces | 40 x 40 x 2 tube throughout, 8 mm bearing plates: 24.7 kg | R9 |
| 2 | Capstan frame | Sling eye at ground level let the capstan tip forward at the overload limit | Anchor bar 40 x 40 x 3 between the rear braces with an eye 200 mm up, level with the drum axis | The pulls line up; the frame is held back by 315 N m |
| 3 | Bearing pads | A 60 mm pad clashed with the first ratchet wheel | Pads 50 mm wide, 180 long | Clearance |
| 4 | Drum | Drum with its bearings was 26 kg, over R9 | 4 mm rings and end discs with six lightening holes; 6 mm ratchet wheels: 23.1 kg with bearings | R9 |
| 5 | Ratchet and pawls | Both pawls on one pivot could not each clear the tooth behind the one they hold | Wheel 1 and its pawl mirrored to the front, on a bracket on the front brace; wheel 2 and its pawl on the post | Each pawl's body clears the teeth; nose 1.3 mm off the face |
| 6 | Chain drive | Sprocket hub inside the chain line; guard wall in the chain's plane | Hub 36 mm; guard moved out to 44 to 70 mm beyond the bearing plane; cranks moved out to suit | Clearance |
| 7 | Shear pin | Not detailed | 4 mm S235 pin through a hub that turns freely on the crank shaft and the shaft itself | R11 |
| 8 | Stakes | Stakes hung free in their tubes | A 32 mm head welded on rests on the stake tube | Each part rests on what holds it |
| 9 | Tail block | One large sheave would have been 300 mm; 20 mm pins at 270 MPa at the limit | Two 125 mm sheaves 175 mm apart on 25 mm pins (138 MPa), spacers, a keeper bar and four anchors | Bought sheaves; strength |
| 10 | Scraper box | Return leg could not pass the box in a 0.7 m door | Box 450 mm wide; return leg 300 mm off the box line | R4 |
| 11 | Scraper box | Vertical back would bulldoze mud on the return | Back slopes 80 mm; skids cut at 45 degrees at the rear | Rides over mud |
| 12 | Bridles | Shackle and lug geometry not defined | 19 mm lug holes, shackle pins through them, chain legs to pear rings 300 mm out | Fixings |
| 13 | Ramp | Deck sheets were drawn self-intersecting and floated between the cheeks | Folded 3 mm trays the full inner width, flanges bolted through the cheeks; roller 10 mm proud of the deck ends | Fixings |

## Consequences

- `cad/src/model.py` holds the constructable design; STEP and STL, SLH-DWG-001 and 002 (Rev P2), the concept media and the build plan pictures are regenerated from it.
- SLH-CAL-001 is rerun on it; costs rise to USD 887.50, still USD 1,112.50 under the value-engineering target.
- `design_state: constructable` is set in `project.yaml`.
