---
doc_id: SLH-PLN-001
title: SiltHaul project plan
project: SiltHaul
doc_type: Project plan
version: "0.1"
status: Draft
date: 2026-11-03
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-11-03
    author: Amish Chadha
    change: First project plan, written for the kit 1.9.1 upgrade
---

# SiltHaul project plan

SiltHaul is at stage P3 (design outputs, TRL 3) with three modelled concept options; the next gate is Amish's choice between option B and option A (SLH-OPT-001, SLH-DDR-005), and TRL 4 work stays on hold while the portfolio cap is TRL 3. Method: STANDARDS sections 19 and 23.

## Workstreams

Table 1. Workstreams.

| Workstream | Owner (role) | Deliverable | Status |
| --- | --- | --- | --- |
| Problem, users and stakeholders | Project lead | SLH-PRB-001 with user and stakeholder tables | Done (P3) |
| STEM check | Design lead | SLH-STM-001, `stem_check.py`; independent review recorded | Done; 12 plausible rows open to TRL 4 |
| Concept options | Design lead | SLH-OPT-001 and the options picture | Done; choice awaiting Amish |
| Requirements and traceability | Design lead | SLH-URS-001, SLH-PRS-001, SLH-RTM-001 | Done; to review with a co-design partner |
| Calculations | Design lead | SLH-CAL-001, `sizing.py`, `options_calc.py` | Done for A; first-order for B and C |
| CAD at D3, every option | Design lead | `cad/src/model.py`, STEP per part and per assembly, `cad/fidelity.json` | Done |
| Drawings, BOM, build plan | Design lead | SLH-DWG-001 and 002, BOM, SLH-BLD-001 | Done for option A; B follows only if Amish chooses it |
| Regulatory, feasibility, risk, market | Project lead | SLH-REG-001, FEA-001, RSK-001, MKT-001 | Done (first pass) |
| Co-design partner | Project lead | Agreement with a disaster authority, NGO or volunteer group | Not started; Amish decides |
| Prototype build, tests and trials (P4) | Fabricator, test lead | TST plans and reports | On hold: TRL 4 |
| Field validation (P5) | Co-design partner | Validation and human factors reports | On hold |
| Launch (P6) | Project lead | Instructions for use, training | On hold |

## Resources needed

Table 2. Resources.

| Resource | Deliverable | Effort | Estimated cost (USD) |
| --- | --- | --- | --- |
| Local fabricator | First build of the chosen option | To assess | Parts 1,055.60 for option A (BOM); labour to assess |
| Test lead and a test bed of wet silt | Timed trial against a bucket crew (PR-001), release and anchor tests | To assess | To assess |
| Proof-load rig (CalRig, shared block) | Anchor, rope and sling proof loads (PR-006, PR-007) | To assess | To assess |
| Regulatory consultant | Machinery rules of the country of use (SLH-REG-001 G9) | To assess | To assess |

No cost is invented here: the only priced item is the BOM, at the indicative prices in `bom/bom.csv`.

## Stage gates

Table 3. Stages (P4 to P6 on hold while the stage cap is P3).

| Stage | Gate criteria | Status |
| --- | --- | --- |
| P0 Proposal | Problem, STEM check, options, first REG, FEA, PLN | Done |
| P1 Definition | URS, PRS, RSK, MKT, REG complete | Done |
| P2 Design inputs | PRS with targets, CAL, RTM, concept selection DDR, STEM check closed | Done except the selection: awaiting Amish; STEM check open (12 plausible rows) |
| P3 Design outputs | Model, STEP, drawings, priced BOM, build plan, decisions register, design FMEA, traceability complete | Reached 2026-11-03 |
| P4 Verification | Test plans, lab reports, verification report | On hold (TRL 4) |
| P5 Validation | Field trials with a partner | On hold |
| P6 Commercialization | Launch plan, training | On hold; needs a named partner |

## Next steps and decision requested

1. Amish chooses between option B and option A, or asks for a hybrid (SLH-DDR-005, SLH-OPT-001). Nothing is chosen here.
2. If Amish chooses B, the BOM, drawings and build plan are redone for B; if A, nothing changes.
3. Amish decides whether to approach a co-design partner and whether to move to TRL 4 when the portfolio cap is lifted. The review note recommends it only after the choice.

## References

- Better Health Channel, State of Victoria. "After a Flood: Returning Home Safely." Reviewed May 20, 2024. https://www.betterhealth.vic.gov.au/health/healthyliving/after-a-flood-returning-home-safely.
- Gulf News. "Kerala Floods: 70,000 People Participate in Massive Post-Flood Clean-Up Drive in Kuttanad." 2018. https://gulfnews.com/world/asia/india/kerala-flood-70000-people-participate-in-massive-post-flood-clean-up-drive-in-kuttanad-1.2271770.
- ISO. ISO 606:2015, ISO 11228-2:2007 and ISO 12100:2010; SIS, ISO 14120:2015, EN 1492-2:2000+A1:2008 and EN 13889:2003+A1:2008 (pages in SLH-REG-001, checked November 3, 2026).
- Mining History Association. Journal of mining history, 2015, on slusher scrapers. https://www.mininghistoryassociation.org/Journal/MHJ-v22-2015-Reynolds.pdf.
- Mongabay India. "Leptospirosis Outbreak Causes Concern in Kerala after the Floods." 2018. https://india.mongabay.com/2018/09/leptospirosis-outbreak-causes-concern-in-kerala-after-the-floods/.
- OSHA. "Flood Response." https://www.osha.gov/flood/response.
- Paul B Hardware. "Maasdam Powr-Pull 2 Ton 6 ft Cable Puller MP144SB6." Checked November 3, 2026.
- Quartz. "After Kerala Floods, Leptospirosis Has Killed Nearly 70 in India." 2018. https://qz.com/india/1377755/after-kerala-floods-leptospirosis-has-killed-nearly-70-in-india.
- USA Blue Book. "AMT Hand Diaphragm Pump HP01-99." Checked November 3, 2026.
- Patents US2588657A, US3532170A and WO2017216731A1 (slusher and scraper winch prior art), cited in SLH-PRB-001.
