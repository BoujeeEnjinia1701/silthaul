# Review note: SiltHaul

## Session 2026-10-03: TRL 3 (kit 1.7.0, /to-trl3 under Amish's pre-approval)

Amish, 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." Every recommendation in this session is therefore recorded as decided, dated 2026-10-03, in `docs/06-design-decisions.md`. Kit 1.7.0 was installed from the kit source; `.kit/PHASE.yaml` kept as installed.

### TRL 2

**What was done.**

- `docs/01-problem.md` (SLH-PRB-001 v0.2): first co-design candidate, safety note, questions for the first trials.
- `docs/03-requirements.md` (SLH-REQ-001 v0.2): measurable targets; R11 (overload limit) and R12 (holds when let go) added.
- `docs/02-concept.md` (SLH-PRC-001 v0.2): how it works, components, first-order numbers, key design choices, safety.
- `docs/decisions/0001-trl2-review-decisions.md` (SLH-DDR-001): thirteen TRL 2 review items decided.

**Results.** First-order working pull about 1 kN; crank force well inside 150 N with a 4:1 drive; output limited by hand power to well below a bucket crew.

**Requirements not met.** R1 (output) was already short at TRL 2 and is kept as the trial target.

**Decisions made under the pre-approval.** SLH-DDR-001, items 1 to 13: split winding drum; 4:1 chain drive; shear pin (R11); two ratchet wheels on the drum shaft (R12); tail block on floor anchors only; sling anchor with stakes only against skating; 10 mm rope; box open toward the door with forward tipping; two people to tip; capstan 6 m or more from the door; Kerala State Disaster Management Authority as first co-design candidate (not agreed); capstan as candidate common block for SaltDrag and CalRig as first proof-load rig; budget kept.

**Safety concerns.** Rope whip from a failed anchor or rope; entrapment at the chain, drum and cranks; uncontrolled stall loads without an overload limit; weak walls as anchors.

### TRL 3

**What was done.**

- `docs/04-calcs/01-sizing.md` and `docs/04-calcs/sizing.py` (SLH-CAL-001 v0.2), `docs/04-calcs/results.csv`.
- `cad/src/model.py`: parametric build123d model with constructability checks (no overlaps, no floating parts); STEP and STL in `cad/step` and `cad/stl` (capstan, box, tail, ramp; assembly STEP at the design case).
- `cad/src/sheets.py`: SLH-DWG-001 (hand capstan GA) and SLH-DWG-002 (system layout), Rev P2.
- `bom/bom.csv`: 23 lines, all priced, with suppliers by type.
- `cad/src/concept_media.py`: `media/hero.png`, `exploded.png`, `flow.png`, `concept-blueprint.png` and `.pdf` (SLH-DWG-010), `model.glb` (1.6 MB, coarse tessellation) and `viewer.html`. No cutaway (the inside does not matter).
- `docs/decisions/0002-design-for-construction.md` (SLH-DDR-002); `design_state: constructable`.
- `cad/src/build_plan_media.py`: overview, nine making sketches (SLH-DWG-101 to 109), eight joint close-ups and twelve step pictures; `docs/05-build-plan.md` (SLH-BLD-001) and `docs/06-design-decisions.md` (SLH-DEC-001).
- `cad/src/product_model.py` (`product_parts()`, `TITLE`, `RENDER_VIEWS` hero, exploded, detail); scenes exported to `/home/claude/renders/silthaul` (three .npz and .json, `silthaul__jobs.json`). Photoreal renders, captions and cards are made on Amish's Mac; the README already leads with `media/render-hero.png`.
- `README.md`, `project.yaml` (trl 3, trl_target 3).

**Results (SLH-CAL-001).** Working pull 1,000 N (917 N estimated); 63 N per person with two at the cranks; 5.4 m/min loaded; 5.65 min a trip over 11 m; 0.43 m³/h (0.32 with rest); shear pin releases at about 2,450 N, all parts sized on 3,000 N; rope factor 18 working and 5.4 at the limit; chain factor 5.0; tail anchors at 0.45 of recommended loads at the limit; heaviest lift 24.7 kg (frame) and 23.1 kg (drum with bearings); kit about 132 kg. Value-engineering target: USD 2,000. Estimated cost of the constructable design: USD 887.50 (USD 1,112.50 under the target).

**Requirements not met.**

- **R1, not met on paper:** 0.32 against about 0.90 m³/h for a bucket crew (ratio 0.36, target 2). Two people at a crank give about 50 W each; dragging 1 kN uses it all.
- **R9, at risk:** mass is met (24.7 kg) but the 890 x 663 x 814 mm frame needs an estate car or small pickup.
- **R8, not verifiable at TRL 3:** about 17 min estimated.

**Decisions made under the pre-approval.** SLH-DDR-002, the thirteen design-for-construction changes (listed below); keeping R1 as the trial target; the appearance model additions (below). All in `docs/06-design-decisions.md`; open decisions: none.

**Build plan findings (design changes made for construction, SLH-DDR-002).**

1. Frame in 40 x 40 x 2 tube with 8 mm plates: 24.7 kg (was over 25 kg).
2. Anchor bar and eye 200 mm up, level with the drum axis; at ground level the capstan could tip at the overload limit.
3. Bearing pads narrowed to 50 mm to clear the first ratchet wheel.
4. Lighter drum (4 mm rings and discs with lightening holes, 6 mm ratchet wheels): 23.1 kg with bearings.
5. Ratchet wheel 1 and its pawl mirrored to the front so each pawl clears the teeth behind its nose.
6. Sprocket hub 36 mm; guard and cranks moved outboard to clear the chain.
7. Shear pin detailed through a free-running hub.
8. Stake heads that rest on the stake tubes.
9. Tail block of two 125 mm sheaves on 25 mm pins with spacers, keeper and four anchors.
10. Box 450 mm wide so the return rope passes beside it in a 0.7 m door.
11. Sloped back and cut skids so the box rides over mud on the return.
12. Bridle lugs, shackle pins and chain legs defined.
13. Ramp decks as folded trays bolted through the cheeks; roller 10 mm proud.

**Appearance model.** `product_model.py` uses the `model.py` solids in the shortened picture layout. Additions not in `model.py`: rope wound on both drum halves, stakes shown above ground only, a wall with a doorway, a tree as the anchor and a 1.75 m mannequin (`mannequin()`, standing at the +Y crank facing the capstan). Decided under the pre-approval.

**Safety concerns.**

- Rope whip: the shear pin bounds rope tension, but a pin replaced by a bolt removes the bound; the briefing card and stop 6 say so.
- The tail block depends on a sound slab; stop 2 forbids use without one. A door-frame option needs pull tests first.
- Tipping the full box takes about 203 N; two people, and only with a pawl holding.
- Sling geometry: a sling rising more than 10 degrees can tip the capstan at the overload limit.
- Entrapment at the drum where the rope winds on is not guarded (the drum must stay open for the rope); people stay out of the rope area while cranking.
- Clean-up hazards (structure, electricity, contamination) remain with users.

**Recommended next step.** The design is ready for TRL 4 when the phase allows: build the capstan and tail block, run the R11 shear pin release test and the proof loads on CalRig, then the timed R1 trial against a bucket crew with the first co-design candidate. Suggestions not added to the repo: a second box on the return leg so both strokes carry mud (would roughly double output; changes the product); a bolted, flat-packing frame for R9.

## Session 2026-09-30: scaffolded

### What was done

- Repository created from kit 1.6.0 at TRL 1, target TRL 2.
- `docs/01-problem.md` (SLH-PRB-001 v0.1): problem with cited evidence, users, environment, constraints, prior work, open questions.
- `docs/02-concept.md` (SLH-PRC-001 v0.1): how it works, components, patent design-arounds, shared blocks, safety.
- `docs/03-requirements.md` (SLH-REQ-001 v0.1): 10 proposed requirements.
- `README.md` with concept rationale, burning platform, where it could be used, and what sparked the idea.

## 2026-10-03: photoreal renders

Rendered with Blender Cycles on Amish's Mac from `cad/src/product_model.py`; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` made with `.kit/cards.py`. Views: hero, exploded, detail. image_qc passes and `render.py --check` has no FAIL.
