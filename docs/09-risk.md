---
doc_id: SLH-RSK-001
title: SiltHaul risk register and hazard analysis
project: SiltHaul
doc_type: Risk register and hazard analysis
version: "0.1"
status: Draft
date: 2026-11-03
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-11-03
    author: Amish Chadha
    change: First risk register, preliminary hazard analysis and design FMEA, written for the kit 1.9.1 upgrade
---

# SiltHaul risk register and hazard analysis

The top risks are a rope or anchor that lets go under tension, a load that runs back if a pawl, pin or chain fails, and contamination of the crew by flood mud; the design answers them with a 3 kN shear pin limit, two ratchets, a closed guard and a sound-slab anchor rule, all checked on paper only. The highest RPN items are F1 (shear pin, 60) and F4 (tail anchors, 40), then F5, F10 and F14 at 36; each has a proof-load, checklist or site-test action for TRL 4. Method: STANDARDS section 23. Likelihood, impact, severity and occurrence are scored 1 (low) to 5 (high).

## Project risk register

Table 1. Project risks.

| # | Risk | Cause | Effect | Likelihood | Impact | Owner (role) | Response |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | The output ratio of 0.57 is below 0.5 in a real trial | Assumed mud strength, floor friction and loading rates | R1 not met; option B or a longer crew needed | 3 | 4 | Design lead | Timed side-by-side trial at TRL 4; B is the fallback (SLH-OPT-001) |
| P2 | No co-design partner is found | No agreement yet with a disaster authority or NGO | No realistic mud, room or crew to test | 4 | 4 | Project lead | Approach the first candidate named in SLH-PRB-001 (not agreed); Amish decides |
| P3 | A local fabricator cannot reproduce the welds and fit-up | 245 parts and tight cross-member fit | Frame or drum out of true; setup slips | 3 | 3 | Fabricator | Build plan with joint pictures; first build at TRL 4 (not started) |
| P4 | The shear pin scatter is wider than 20 % | Pin steel varies by supplier | Overload limit not reliable (PR-011) | 3 | 5 | Design lead | Release test on a batch; buy pin bar from one supplier |
| P5 | Rated shackles and a 2 t sling are not available or priced as assumed | Indicative BOM prices | Cost above the USD 2,000 target | 2 | 3 | Project lead | Quote at TRL 4; current cost USD 1,055.60 |
| P6 | Amish chooses B, A or neither and the repo must follow | Options within 10 % (SLH-OPT-001) | Re-plan of BOM, drawings and build plan for B | 3 | 2 | Project lead | Option B is modelled at D3 already; BOM and drawings follow the choice |
| P7 | Safety claims outrun the evidence | Proof loads untested | Harm to a volunteer | 2 | 5 | Design lead | "Met on paper" only; proof-load tests before any use (SLH-BLD-001 section 6) |

## Preliminary hazard analysis

Table 2. Hazards.

| # | Hazard | Cause | Harm | Severity | Likelihood | Control | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | Rope or splice parts under tension | Wear, overload, cut | Whiplash injury to a person in the line | 5 | 2 | Overload limit 3 kN; rope factor 5.4; nobody in the rope lines while the cranks turn; stop signals (BOM 22) | Medium |
| H2 | Anchor or sling fails | Weak slab, wall used as anchor, sling over an edge | Frame or tail block flies toward the crew | 5 | 2 | Floor anchors only in a sound slab; walls never used; sling level or rising 10 degrees | Medium |
| H3 | Load runs back when cranks are let go | Pawl missed, pin or chain fails | Spinning cranks strike a hand | 4 | 2 | Two ratchets and pawls; hands off the cranks on a stop signal | Low |
| H4 | Crushing at the chain, sprockets or between boxes | Guard removed; fingers between boxes passing 42 mm apart | Crushed or cut finger | 3 | 3 | Closed guard; loaders keep hands and feet out from between the boxes | Medium |
| H5 | Contaminated mud, sewage, tetanus | Cuts and wet skin in floodwater | Infection | 4 | 4 | Boots, gloves, hand washing, wound cover (Better Health Channel); the kit reduces time in the mud, not the exposure | Medium |
| H6 | Manual handling of the kit | 22.2 kg drum and bearings, 16.2 kg box | Back or shoulder strain | 3 | 3 | Heaviest part under 25 kg; two people share the drum | Low |
| H7 | Damaged building | Weakened walls, floors, live electrics | Collapse, electric shock | 5 | 2 | Outside the design; the crew follows local advice; no wall contact (PR-007) | Medium |
| H8 | Capstan tips or skids | Sling rising more than 10 degrees; soft ground | Frame moves toward the crew | 4 | 2 | Tipping margin 145 against 270 N m at 10 degrees; four stakes | Low |
| H9 | Dumping a full box | Box tips forward onto feet | Foot injury | 3 | 3 | Two people on the 900 mm tipping bar; 119 N each; feet clear | Low |
| H10 | Heat, fatigue and slips on wet mud | Hot humid work, wet footing | Collapse, falls | 3 | 4 | Rest allowance (25 % of time); staked foot boards for option B | Medium |

## Design FMEA (first pass, P3)

Table 3. Failure modes. RPN = severity x occurrence x detection.

| # | Item | Function | Failure mode | Effect | Cause | S | O | D | RPN | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | Shear pin (BOM 10) | Limit rope tension to 3,000 N | Releases late (above 3 kN) or early | Rope, chain, anchors or shaft overloaded; or the crew loses the pull | Pin steel stronger than S235 or 20 % scatter; wrong pin substituted | 5 | 3 | 4 | 60 | Pins in a labelled bag, cut from S235 bar only; release test on a batch (PR-011) |
| F2 | Ratchet wheels and pawls (BOM 8) | Hold the drum when the cranks are let go | Pawl does not engage, tooth shears | Drum runs back; cranks spin; load runs to the box | Spring lost, mud in teeth, tooth overload 4.1 kN | 5 | 2 | 3 | 30 | Two opposite ratchets; tooth bearing stress 57 MPa; release test at working pull (PR-012) |
| F3 | Rope (BOM 16) | Carry the pull between drum and boxes | Rope parts or splice fails | Rope whips; box runs back | Abrasion on the ramp roller, cuts, UV, bend ratio 6 at the roller | 5 | 2 | 3 | 30 | Factor 5.4 at the limit; inspect before each use; replace on cut or fray |
| F4 | Tail anchors (BOM 15) | Hold the tail block against 6 kN if a returning box jams | Wedge anchor pulls out or the slab spalls | Tail block flies toward the crew | Cracked or thin slab, drilling too close to an edge | 5 | 2 | 4 | 40 | Sound slab 100 mm or more; 0.45 of recommended loads; pull test on the anchored block (PR-007) |
| F5 | Anchor sling (BOM 12) | Hold the capstan against the pull | Sling cut or the tree or vehicle moves | Capstan skids or tips toward the crew | Sling over a sharp edge; rising more than 10 degrees | 4 | 3 | 3 | 36 | Tree protector strap; sling level or rising 10 degrees at most; stakes stop skating |
| F6 | Drum shaft and bearings (BOM 2, 3) | Carry the rope load into the frame | Shaft bends or a bearing seizes | Drum jams; crew loses control of the load | Mud and water in the bearing; overload at the pin limit | 4 | 2 | 3 | 24 | Shaft 144 MPa combined against 213 allowed; sealed UCP bearings with grease nipples |
| F7 | Drum tube (BOM 2) | Carry wound rope without collapse | Tube buckles under rope pressure | Rope slackens and tangles | 3 mm wall under 2.5 MPa rope pressure | 4 | 1 | 4 | 16 | Buckling factor 4.6 between rings (SLH-STM-001 S7); rings at both ends of each half |
| F8 | Chain, sprockets (BOM 6, 7) | Transmit torque at 4:1 | Chain breaks or jumps a tooth | Cranks spin free; ratchets then hold the drum | Misalignment, no lubrication, shock | 3 | 3 | 3 | 27 | Factor 4.9 at the limit (fix proposed, SLH-STM-001 S5); guard (BOM 9) keeps the chain in view and hands out |
| F9 | Chain guard (BOM 9) | Keep fingers away from chain and sprockets | Guard removed or bent | Crushed finger at the chain | Removed for lubrication and not refitted | 3 | 3 | 2 | 18 | Two M6 screws only; briefing card; guard in the packing list |
| F10 | Frame cross-member bolts (BOM 1, 21) | Hold the flat-pack frame together | Bolt loosens or is left out | Frame racks; drum shaft misaligns | Twelve bolts to fit on site in 3 min | 4 | 3 | 3 | 36 | Nyloc nuts; checklist in the build plan section 5; look before the first stroke |
| F11 | Scraper box and bridles (BOM 17, 20) | Carry 86 kg of mud and its pull | Shackle pin works out, chain or lug fails | Box runs free in the room | Split pin missing, lug weld cracks | 3 | 3 | 3 | 27 | Split pin on every shackle pin; 10 mm lugs; inspect welds |
| F12 | Tail sheave pins (BOM 13, 14) | Turn the tail rope through 180 degrees | Pin bends under a jam load | Sheave drops; rope jumps out | Jam at the limit: 138 MPa bending | 3 | 2 | 3 | 18 | 25 mm S355 pins, keeper bar over both; inspect after a jam |
| F13 | Doorway ramp (BOM 19) | Carry the boxes over the threshold | Cheek ply splits or the roller seizes | Box catches; rope snatches | Wet ply, mud in the roller bushes | 2 | 3 | 2 | 12 | Exterior plywood, nylon bushes, clean after use |
| F14 | Option B foot boards and stakes | Give the haulers a staked foothold | Stake pulls out of soft mud | Haulers slip while pulling 756 N | Saturated soil; 189 N each on 25 mm stakes | 3 | 3 | 4 | 36 | Stakes 480 mm deep; test the pull on site before the first haul; heel cleats |
| F15 | Option C diaphragms and valves | Pump slurry at 0.46 L/s | Valve blocked by debris; diaphragm tears | Pump stops; slurry spills | Sticks and stones in the strainer; flex fatigue at 1.7 % strain | 2 | 4 | 3 | 24 | Strainer cage; clear and test valves before each shift; supplier flex life to confirm |

Actions are paper actions or TRL 4 tests; none is carried out here. Scores are the author's first pass and are to be reviewed with a co-design partner and a fabricator.
