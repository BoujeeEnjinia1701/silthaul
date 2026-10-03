---
doc_id: SLH-DDR-003
title: SiltHaul second box on the return leg and flat-pack frame
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
  change: Amish's requirement decisions 2A (R1) and 7A (R9) carried into the constructable design
---

# 0003: Second box on the return leg and flat-pack frame

- **Date:** 2026-10-03
- **Status:** accepted

## Context

At TRL 3 (SLH-CAL-001 v0.2) SiltHaul missed R1, output, by a wide margin (0.32 m³ an hour, a ratio of 0.36 to a bucket crew against a target of 2), and R9, portability, was at risk because the welded frame, 890 x 663 x 814 mm, needed an estate car or small pickup. Both fixes change what the product is, so they were put to Amish as requirement decisions. On 2026-10-03 Amish chose option A on every decision put to him: "1A 2A 3A 4A 5A 6A 7A 8A 9A 10A 11A". For SiltHaul:

- **2A (R1).** Add a second box on the return run so the rope loop carries mud both ways; restate R1 as "no lifting or carrying of mud; output at least 0.5 times the same crew with shovels and buckets".
- **7A (R9).** Redesign the frame as a bolted flat-pack frame that fits a small car boot, keeping the 25 kg heaviest-part limit.

## Options considered

For 2A the open question was how two boxes fit through a 0.7 m door (R4) with their rope lines 300 mm apart, the spacing the drum and ramp already set.

| Option | Result | Chosen |
| --- | --- | --- |
| Two 446 mm boxes, lines moved about 540 mm apart | Ramp and door about 1.1 m wide; breaks R4 | No |
| Two narrow boxes on the existing 300 mm lines | 210 mm inside, 845 mm long, 280 mm sides: 40.3 L each; they pass 42 mm apart and cross the ramp 26 mm inside its cheeks | Yes |

For 7A the frame could come apart into two welded side frames joined by bolted cross members, or into loose tubes (rails, posts and braces each bolted). The side frames need only twelve bolts and keep every welded joint that carries the drum and crank bearings; loose tubes would fit a boot with the seats up but need about forty bolts and would push setup well past 20 min (R8).

## Decision

*Table 1. Changes made.*

| # | Part | Change | Result (SLH-CAL-001 v0.3) |
| --- | --- | --- | --- |
| 1 | Scraper boxes | Two identical boxes, 210 mm wide inside, 845 mm to the lip, 280 mm sides, back sloping 110 mm; box 1 on the pull rope, box 2 on the return rope, both open toward the door | 40.3 L each at a 245 mm fill (R3); 16.1 kg each |
| 2 | Ropes | Pull rope 17 m to box 1; return rope 17 m to box 2; a tail rope joins the two boxes' rear bridles round the tail sheaves, chosen for the room from 12.5, 9 and 6 m | 62 m of rope in all |
| 3 | Operation | Each stroke hauls one full box out while the other goes back empty; loaders fill one box while the crank crew dump the other | 3.54 min a stroke; 0.68 m³/h, 0.51 with rest; ratio 0.57 (R1 met on paper) |
| 4 | Ramp | Centred midway between the two box lines | Both boxes 26 mm inside the cheeks (R4) |
| 5 | R1 | Restated in Amish's words above | Met on paper |
| 6 | Capstan frame | Two welded side frames (rail, posts, braces, pads, top plate, stake tubes) and four bolted cross members (front and rear cross rails, top tie, anchor bar with eye), each with 8 mm end plates; eight M10 and four M12 bolts | Side frames 9.2 and 9.6 kg; cross members 8.0 kg in all |
| 7 | Stake tubes | Moved to 280 mm in front of and 330 mm behind the drum axis to clear the bolts | Stakes unchanged |
| 8 | R9 | Requirement unchanged; small car boot taken as a small hatchback with the rear seats folded (1,250 x 950 x 500 mm) | Heaviest lift 23.1 kg; kit about 454 L, 77 % of the boot (R9 met on paper) |

## Consequences

- `cad/src/model.py` adds box 2, its bridles, the tail rope and the bolted frame, with checks that the boxes pass with at least 25 mm between them, that both cross the ramp at least 15 mm inside the cheeks, and that every cross member and bolt touches the side frames. STEP and STL, SLH-DWG-001 and 002 (Rev P3), the concept media and the build plan pictures are regenerated.
- The working pull stays 1,000 N: the narrower lip cuts less mud, so a full box out and an empty box back need about 970 N. Handle force, rope, chain, shear pin and anchors are unchanged.
- Setup rises to about 20 min with three people, at the R8 limit.
- Value-engineering target: USD 2,000. Estimated cost of the constructable design: USD 1,055.60 (USD 944.40 under the target), up USD 168.10.
- Boxes pass 42 mm apart in the room: loaders keep hands and feet out from between them while the cranks turn.
- New open decision for Amish: whether "fits a small car boot" may assume the rear seats are folded (design decisions register).
