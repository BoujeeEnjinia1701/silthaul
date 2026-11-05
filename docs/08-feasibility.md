---
doc_id: SLH-FEA-001
title: SiltHaul feasibility assessment
project: SiltHaul
doc_type: Feasibility
version: "0.1"
status: Draft
date: 2026-11-03
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-11-03
    author: Amish Chadha
    change: First feasibility assessment, written for the kit 1.9.1 upgrade
---

# SiltHaul feasibility assessment

SiltHaul is feasible on paper as option A (the existing design) and as option B, and the case for either rests on three things only a trial can settle: the output ratio, the shear pin release and a local fabricator's welds. Option C is not feasible with village tools. Method: STANDARDS section 23.

Table 1. Feasibility by aspect.

| Aspect | Assessment | Rating | Risks and notes | Evidence |
| --- | --- | --- | --- | --- |
| Design | Option A is fully calculated: 63 N each at the cranks, rope factor 5.4 and chain 4.9 (just under the 5 asked, a fix is proposed) at the 3 kN overload limit, 0.45 of recommended anchor loads, tipping margin at 10 degrees; modelled at D3 with 245 parts and no interference | High | Output ratio 0.57 against the 0.5 target rests on assumed mud and loading rates; floor friction and mud strength are estimates | SLH-STM-001, SLH-CAL-001, `cad/fidelity.json` |
| Materials | Stock 40 x 40 x 2 SHS, 219.1 x 3 tube, sheet and bar; polyester rope; bought UCP bearings, 08B-1 chain, rope sheaves and shackles | High | Coating life in wet, salty or contaminated mud not assessed (S15); rope bend ratio 6 at the ramp roller (S14) | SLH-STM-001, BOM |
| Manufacturing and assembly | A village workshop with a small welder makes the two side frames, drum, boxes and tail plate; the kit bolts together with twelve frame bolts; the build plan has making sketches and joint pictures | Medium | 245 parts and 161 fasteners; weld quality and fit-up of the drum and frame are unproven; setup is at the 20 min limit | SLH-BLD-001, SLH-DWG-101 to 109 |
| Power and controls | Hand power only: 48 W each at the crank against 75 W sustained; no electrics | High | A crank crew tires over a shift; rest allowance of 25 % assumed | SLH-CAL-001 D3, SLH-STM-001 S2 |
| Supply of parts | Every bought part is a catalogue item from a bearing, rigging, fastener or hardware supplier; indicative prices in the BOM | Medium | Prices are indicative and not region-specific; rated shackles and a 2 t sling are needed (SLH-REG-001 G4, G5) | BOM, SLH-MKT-001 |
| Safety and certification | No certification route identified; rope, anchor and chain are sized on a 3 kN limit with proof-load tests planned | Medium | Rope under tension near people; contaminated mud; machinery rules of the country of use to assess | SLH-REG-001, SLH-RSK-001 |
| Option B (crew-hauled box) | Half the mass and under half the cost; no frame; but 189 N each repeated, no overload limit | Medium | Footing on wet mud (foot boards fix it on paper); ISO 11228-2 limits unchecked | SLH-OPT-001, SLH-STM-001 S18 to S20 |
| Option C (hand slurry pump) | Flow and power work on paper at 40 mm stroke; the made pump is not buildable with village tools and needs 18 L/min of flush water | Low | HDPE manifold block, diaphragms, flap valves and debris blocking; 2.8 times the wet waste | SLH-OPT-001, SLH-STM-001 S23 to S26 |

Ratings: High, Medium, Low.

## What would change the verdict

A timed trial on real wet silt (PR-001), a shear pin release test (PR-011) and a first build by a local fabricator would each move a Medium to High or expose a Low. All three are TRL 4 work and are not started here.
