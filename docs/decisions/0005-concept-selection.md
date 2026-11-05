---
doc_id: SLH-DDR-005
title: SiltHaul concept selection
project: SiltHaul
doc_type: Design decision record
version: "0.1"
status: Draft
date: 2026-11-03
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-11-03
    author: Amish Chadha
    change: Concept options compared for the kit 1.9.1 upgrade; the choice is proposed and awaits Amish
---

# 0005: Concept selection

- **Date:** 2026-11-03
- **Status:** Proposed, awaiting Amish. Nothing is decided: the two leading options are within 10 % of each other, so both go to Amish without a pick (STANDARDS section 21).

## Context

SiltHaul was designed as option A, the hand-capstan loop (SLH-DDR-001 to SLH-DDR-004). The kit 1.8 pipeline asks every design for at least two options with different working principles, scored against the user requirements (SLH-URS-001) and modelled to the stage's detail level (D3 at P3). Options B and C were added; option A is unchanged. Amish's earlier choices (friction capstan, 540 mm line spacing, loose-tube frame, single box on the loop) were not re-proposed.

## Options considered

Table 1. Options and weighted scores (SLH-OPT-001, Table 2; maximum 160).

| Option | Working principle | Score | Share | Main strength | Main weakness |
| --- | --- | --- | --- | --- | --- |
| A | Hand-cranked drum on a 4:1 chain drive hauls two boxes round a rope loop; shear pin, ratchets, guard | 126 | 79 % | 63 N each at the cranks; overload limit and load holding | 153.9 kg, USD 1,055.60, a rope and chain system under tension |
| B | Up to four people haul one box on a rope with fixed grips; tag line returns it; staked foot boards | 133 | 83 % | 80.5 kg, about USD 454 carried over, quickest trip (0.62 m3/h) | 189 N each, repeated, on wet footing; no overload limit or brake |
| C | Hand diaphragm pump on a skid sucks mud thinned with flush water and delivers it by hose | 96 | 60 % | No rope under tension; 39 W | Misses R1 (0.49); needs 18 L/min of water; 2.8 times the wet waste; not buildable with village tools |

## Decision

Proposed, awaiting Amish: B (133) and A (126) are within 10 % (5.3 %), so no pick is made. Option C is not recommended. Amish chooses A, B or a hybrid (for example A with B's staked foot boards at the dump, or B with a snubbing post on the tag line). Until then the repo keeps option A as the chosen design for the drawings, BOM and build plan (`CHOSEN = "A"` in `cad/src/model.py`), and `concept_chosen` in `project.yaml` is "A (proposed)", which is not a decision.

## Note: chain factor of option A

The independent review of the STEM check found that the 08B-1 chain of option A has a factor of 4.93 on its breaking load at the 3,000 N limit (drum bearing friction adds to its share), just under the 5 that R6 asks. Three fixes are proposed, all awaiting Amish because they move a safety limit: (a) a 3.5 mm shear pin, limit about 2.25 kN, chain factor 6.6, 1.5 times the stroke pull of 977 N, which narrows the margin before the pin shears in normal use; (b) duplex 08B-2 chain and sprockets (BOM and guard change); (c) accept 4.9. Recommended: (a), after a release test. Nothing is changed in the model, BOM or drawings.

## Consequences

- If Amish chooses A: nothing changes.
- If Amish chooses B: the BOM, drawings, build plan and product renders are redone for B, whose D3 model already exists; R2 (PR-002) would be restated for four haulers or a longer rope on a pulley.
- Option C stays in the record as the option that was modelled and scored, not as a candidate.

> **Safety:** Option B has no overload limit and no brake; a jammed box lets four people heave 1.6 kN on the rope. If B is chosen, SLH-RSK-001 gets new hazards before any trial.
