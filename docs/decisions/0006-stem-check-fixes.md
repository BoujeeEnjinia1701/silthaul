---
doc_id: SLH-DDR-006
title: SiltHaul STEM check fixes
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
    change: Two STEM fixes decided under Amish's standing instruction of 2026-10-23
---

# 0006: STEM check fixes

- **Date:** 2026-11-03
- **Status:** Decided under Amish's standing instruction of 2026-10-23: when a STEM check row fails, propose and implement the best fix for the design and its constructability in the same session; a fix that changes the working principle, pitch or scope goes to Amish instead. Neither fix below changes the working principle, the pitch or the scope.

## Context

The STEM check (SLH-STM-001) of options A, B and C found two details that failed their first screen. Option A had no failing row.

## Options considered

Table 1. Fixes considered.

| # | Option | Failure | Fixes considered | Chosen |
| --- | --- | --- | --- | --- |
| 1 | B | Boots on wet mud give a friction coefficient of about 0.25 (estimate); a 189 N pull needs 0.28 | (a) staked foot boards with heel cleats; (b) a longer rope and more haulers; (c) a post to lean on | (a): keeps the principle, uses stock timber and four 25 mm stakes |
| 2 | C | A 120 mm stroke on a 250 mm flat EPDM diaphragm is 15 % strain each way and does not fit the 25 mm dish below the plane | (a) stroke 40 mm; (b) a convoluted diaphragm; (c) a bigger dish | (a): strain 1.7 %; the cover cavity is cut to 49 mm. Output falls to 0.44 m3/h with rest |

## Decision

Both fixes are made in the models (`cad/src/opt_b.py`, `cad/src/opt_c.py`, `PARAMS["pump"]["stroke_chamber"]` is 40 mm) and the checks rerun (`docs/04-calcs/stem_check.py`).

## Consequences

- Option B's foot boards (two 40 x 200 x 1200 mm boards, heel cleats, coach screws, four stakes) are in its D3 model; they are not priced.
- Option C's R1 ratio falls to 0.49, which is part of why it scores lowest (SLH-OPT-001).
- Option A is not touched.
