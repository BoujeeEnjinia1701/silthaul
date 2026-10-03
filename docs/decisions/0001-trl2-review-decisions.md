---
doc_id: SLH-DDR-001
title: SiltHaul TRL 2 review decisions
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
  change: TRL 2 review items decided under Amish's pre-approval of 2026-10-03
---

# 0001: TRL 2 review decisions

- **Date:** 2026-10-03
- **Status:** accepted

## Context

The TRL 2 review (`docs/REVIEW.md`, TRL 2 section) raised the items below. On 2026-10-03 Amish wrote: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." Every recommendation is therefore decided as recommended. Choices that touch safety take the conservative option, with the evidence that would relax them stated. Partners and regions are the first candidates to approach, not agreements.

## Options considered

Table 1 lists the options for each item and the one chosen.

## Decision

*Table 1. Items decided on 2026-10-03 under Amish's pre-approval.*

| # | Item | Options | Decision | What would relax a safety choice |
| --- | --- | --- | --- | --- |
| 1 | Capstan type | (a) friction capstan with the rope loop wrapped round it; (b) split winding drum, one half winding while the other pays out | (b). A friction loop needs a pretension of about half the pull and its turns walk along the drum; a winding drum cannot slip | Not a safety choice |
| 2 | Drive | (a) direct crank; (b) 4:1 roller chain to a crank shaft at standing height, two cranks | (b): 63 N per person at 1 kN | Not a safety choice |
| 3 | Overload | (a) size everything on what two people can heave (6.4 kN); (b) a shear pin that limits rope tension to about 2.5 kN | (b), conservative: R11 added. Every part is sized on 3,000 N | Release tests on a batch of pins showing a tighter scatter could raise the working pull, never the limit |
| 4 | Holding | (a) one pawl on the crank shaft; (b) two opposite ratchet wheels and pawls on the drum shaft | (b), conservative: R12 added. The drum holds either way even if the chain or pin fails | None proposed |
| 5 | Tail anchor | (a) floor plate on drilled anchors; (b) door-frame spanning bar; (c) strut | (a) only, conservative. Walls and door frames are never used | Pull tests to 5 times the R11 limit on representative flood-damaged frames would allow (b) as an option |
| 6 | Capstan anchor | (a) ground stakes; (b) round sling to a tree or parked vehicle, stakes against skating | (b), conservative; the sling runs level or rises 10 degrees at most | Pull tests of stakes in wet soil to 5 times the anchor load would allow stakes alone |
| 7 | Rope | 8 mm or 10 mm polyester double braid | 10 mm, 18 kN: factor 5.4 on the limit through a splice | Not relaxed |
| 8 | Box | (a) open front facing the room, filled by hand; (b) open front facing the door, scooping on the way out and tipping forward at the dump | (b), with a sloped back that rides over mud on the return | Not a safety choice |
| 9 | Dumping | One person or two on the tipping bar | Two people, conservative: about 203 N to start a full box | A lift under 150 N measured at TRL 4 would allow one person |
| 10 | Capstan distance from the door | 4 m, 6 m or more | At least 6 m, for a fleet angle of 1.41 degrees or less on the smooth drum | Not a safety choice |
| 11 | Co-design partner | NGO, municipal unit or volunteer fire service | First candidate to approach: the Kerala State Disaster Management Authority and its civil defence volunteers (not agreed) | |
| 12 | Shared blocks | Hand capstan common block with SaltDrag; CalRig for proof loads | SiltHaul's capstan is recorded as the candidate common block; SaltDrag is checked against it at its own TRL 3 (not edited here). CalRig is the first candidate rig for proof loads | |
| 13 | Budget | Keep `budget_usd` at 2,000 | Kept; it is a value-engineering target, not a limit | |

## Consequences

- R11 (overload limit) and R12 (holds when let go) are added to SLH-REQ-001.
- The design for construction (SLH-DDR-002) works from these choices.
- R1 is reported not met on paper; Amish's pre-approval covers the recommendation to keep R1 as the trial target rather than lower it, so the TRL 4 timed trial settles it.
