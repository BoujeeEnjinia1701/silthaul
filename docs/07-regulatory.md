---
doc_id: SLH-REG-001
title: SiltHaul regulatory and standards register
project: SiltHaul
doc_type: Regulatory register
version: "0.1"
status: Draft
date: 2026-11-03
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-11-03
    author: Amish Chadha
    change: First register, written for the kit 1.9.1 upgrade; standards checked on their issuing pages on 2026-11-03
---

# SiltHaul regulatory and standards register

SiltHaul is a hand-powered rope and chain machine for flood clean-up; no product regulation was found that certifies it as a whole, and the design leans on lifting-accessory and machinery-safety standards for its rope, sling, shackle and guard choices. This is not legal advice; anything marked "to assess" needs a qualified reviewer before any product claim. Method: STANDARDS section 23.

Table 1. Regulatory and standards register.

| # | Standard or regulation | Jurisdiction | What it covers | Applicability to this design | Owner (role) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| G1 | ISO 12100:2010 Safety of machinery, general principles for design, risk assessment and risk reduction (confirmed 2022) | International | Method for hazard identification, risk estimation and risk reduction in machine design | The preliminary hazard analysis and design FMEA in SLH-RSK-001 follow its order: remove by design, guard, then inform | Design lead | Applies; used as method (SLH-RSK-001) |
| G2 | ISO 14120:2015 Safety of machinery, guards, general requirements for the design and construction of fixed and movable guards | International | Fixed and movable guards against mechanical hazards | The closed chain guard (BOM 9, PR-016); the ratchet wheels and pawls stay on the outer face of the frame | Design lead | Met by design for the chain guard; guard openings and fixings to assess at TRL 4 |
| G3 | ISO 11228-2:2007 Ergonomics, manual handling, Part 2: pushing and pulling (confirmed 2021, amendment 2022) | International | Recommended limits for whole-body pushing and pulling | Crank force (PR-002), tipping bar (PR-017) and, for option B, the 189 N each hauling pull (SLH-STM-001 S19) | Design lead | To assess: tables not read; check at TRL 4 |
| G4 | EN 1492-2:2000+A1:2008 Textile slings, safety, roundslings made of man-made fibres | EU, widely used elsewhere | Rating and testing of polyester roundslings up to 40 t; excludes lifting of people | The 2 t round sling that anchors the capstan to a tree or vehicle (BOM 12); used here as a pulling anchor, not for lifting | Design lead | Applies to the bought sling; use as an anchor to assess |
| G5 | EN 13889:2003+A1:2008 Forged steel shackles for general lifting purposes, dee shackles and bow shackles, grade 6 | EU, widely used elsewhere | Dimensions and working load limits of grade 6 shackles with threaded pins, 0.5 t and above | Bow shackles on the sling and the box bridles (BOM 12, 20); the bought shackles have 19 mm pins and cotter or split pins in the model | Design lead | To assess: the model's split-pin shackles are not threaded-pin grade 6 shackles; buy rated shackles at TRL 4 |
| G6 | ISO 606:2015 Short-pitch transmission precision roller and bush chains, attachments and sprockets (confirmed 2021) | International | Dimensions, strength and sprockets of 08B-1 chain | The 4:1 chain drive (BOM 6, 7); breaking load 17.8 kN from the maker's table | Design lead | Applies; met by design (SLH-CAL-001 J2) |
| G7 | ISO 4017, ISO 4032 and ISO 7089 hex bolts, nuts and washers, as named by the CAD parts library | International | Dimensions of the bolts, nuts and washers in the model | The 161 fasteners in the 245-part model of option A; numbers as named in `.kit/cad_parts.py`, not checked against the standards this session | Design lead | Applies; to check at TRL 4 |
| G8 | Flood clean-up health advice, for example Better Health Channel, State of Victoria (reviewed 2024-05-20) and OSHA flood response | Victoria, Australia; United States | Boots, gloves, hand washing, tetanus and contamination; manual lifting injuries | The safety notes and the briefing card (BOM 22); user behaviour, not a product requirement | Project lead | Applies as guidance; local health advice governs |
| G9 | Machinery or equipment safety regulation of the country of use | To assess | Whether a hand-powered kit lent to volunteers is "machinery" in law | None identified; no CE-style marking is claimed | Regulatory consultant | To assess |
| G10 | Rules for anchoring into floors of damaged or rented buildings, and for working in a flooded building | Local | Permission to drill the slab, structural safety, electricity | The tail block needs four drilled anchors in a sound slab (PR-007); the capstan stands on the ground | Co-design partner | To assess locally |
| G11 | Disposal of flood mud and wastewater | Local | Where mud may be dumped | Out of scope of the design (SLH-PRB-001); option C would add 2.8 times the volume | Co-design partner | Does not apply to the design; to assess locally |
| G12 | CERN-OHL-S-2.0 and MIT licences; REUSE | International | Licensing of the hardware and calculators | `REUSE.toml`, `LICENSES/` | Project lead | Met by design |

Status: to assess, applies, does not apply, met by design, certification needed later.

## Sources

- ISO, ISO 11228-2:2007, <https://www.iso.org/standard/26521.html>, checked 2026-11-03.
- ISO, ISO 12100:2010, <https://www.iso.org/standard/51528.html>, checked 2026-11-03.
- ISO, ISO 606:2015, <https://www.iso.org/standard/61232.html>, checked 2026-11-03.
- SIS (Swedish Standards Institute), ISO 14120:2015, <https://www.sis.se/en/produkter/environment-health-protection-safety/safety-of-machinery/iso141202015>, checked 2026-11-03.
- Genorma, EN 1492-2:2000+A1:2008, <https://genorma.com/en/standards/en-1492-2-2000-a1-2008/amp>, checked 2026-11-03.
- SIS, SS-EN 13889+A1:2008, <https://online.sis.se/en/produkter/maskinsakerhet-357f77b1/chains-ropes-webbing-slings-and-accessories/ssen13889a12008>, checked 2026-11-03.
- Better Health Channel, "After a flood: returning home safely", <https://www.betterhealth.vic.gov.au/health/healthyliving/after-a-flood-returning-home-safely>, reviewed 2024-05-20, checked 2026-11-03.
- OSHA, flood response, <https://www.osha.gov/flood/response> (cited in SLH-PRB-001).
