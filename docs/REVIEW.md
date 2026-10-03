# Review note: SiltHaul

## 2026-10-03: Amish's requirement decisions carried out

Amish, 2026-10-03, on every requirement decision put to him: "1A 2A 3A 4A 5A 6A 7A 8A 9A 10A 11A". For SiltHaul that is 2A (R1) and 7A (R9), recorded in `docs/decisions/0003-amish-requirement-decisions.md` (SLH-DDR-003) and in `docs/06-design-decisions.md` (SLH-DEC-001 v0.2). No commit or push in this session; Amish pushes.

**Changes made and their new results (SLH-CAL-001 v0.3).**

- **2A, second box on the return leg (R1).** Two identical boxes, 210 mm wide inside, 845 mm to the lip, 280 mm sides (40.3 L each at a 245 mm fill, R3 met by design); box 1 on the pull rope, box 2 on the return rope, joined by a tail rope round the tail sheaves (12.5, 9 and 6 m tail ropes, chosen for the room). Each stroke hauls one full box out (752 N) and drags the empty one back (218 N): 970 N, inside the unchanged 1,000 N working pull, so R2 stays 63 N each. A stroke is 3.54 min; 0.68 m³/h, **0.51 m³/h with rest against 0.90 for buckets, ratio 0.57 against the restated 0.5: R1 met on paper** (was 0.36, not met). R1 restated in `docs/03-requirements.md` (v0.4) in Amish's words. The boxes pass 42 mm apart and cross the recentred ramp 26 mm inside its cheeks (R4 met by design). Tail block 636 N on either stroke; at the limit unchanged (0.45 of anchor loads).
- **7A, flat-pack frame (R9).** Two welded side frames (890 x 814 x 83 mm, 9.2 and 9.6 kg) and four bolted cross members with 8 mm end plates (front and rear cross rails, top tie, anchor bar with eye; 8.0 kg), eight M10 and four M12 bolts; stake tubes moved to 280 mm front and 330 mm rear to clear the bolts. Heaviest lift 23.1 kg (drum with bearings), within 25 kg. Kit packs into about 454 L, 77 % of a 594 L small hatchback boot with the rear seats folded: **R9 met on paper (rear seats folded)** (was at risk). Capstan 65.7 kg; sling-tipping check still holds (145 N m against 271 N m at 10 degrees).
- **R8** moves to about 20 min with three people, at the limit (bolting the frame and a second box add 4 min); still not verifiable at TRL 3.
- **R10.** Value-engineering target: USD 2,000. Estimated cost of the constructable design: USD 1,055.60 (USD 944.40 under the target), up USD 168.10: second box USD 80, second bridle set USD 54, rope 62 m (+USD 9.10), frame end plates and drilling USD 10, frame bolts USD 8, paint USD 5. Kit about 154 kg (was 132).
- Counts: 7 met on paper, 4 met by design, 1 not verifiable at TRL 3; none not met.

**Files.** `cad/src/model.py` (box 2, tail rope, bolted frame; new checks: boxes pass at least 25 mm apart, both at least 15 mm inside the ramp cheeks, cross members and bolts touch the side frames, pack pieces listed; no overlaps, no floating parts), STEP and STL regenerated; `bom/bom.csv` (lines 1, 16, 17, 18, 20, 21, 23); `docs/04-calcs/sizing.py`, `01-sizing.md` (v0.3), `results.csv`; `docs/03-requirements.md` (v0.4); `cad/src/sheets.py`, SLH-DWG-001 and 002 Rev P3; `cad/src/concept_media.py` (hero, exploded, flow, blueprint, model.glb); `cad/src/build_plan_media.py`: overview, SLH-DWG-101 (now side frames), new SLH-DWG-110 (cross members), SLH-DWG-107 (box), joints 04, 05 and new 09, steps 01 to 13 (new step 1, bolting the frame; step 13 reeves both boxes); `docs/05-build-plan.md` (v0.2, figures renumbered); `cad/src/product_model.py` (box 2, cross members and bolts in the views; scenes exported to `/home/claude/renders/silthaul`); headline figures in `README.md` and `docs/02-concept.md`.

**Open decision for Amish (register item 1).** What "fits a small car boot" means. With the seats up the 890 x 814 mm side frames do not lie flat in a typical 950 x 650 mm small-car boot floor. Options: A, accept the rear seats folded as the reference (R9 met on paper); B, split each side frame into bolted tubes, about forty bolts, setup well past 20 min. Recommendation: A.

**Safety.** The boxes pass 42 mm apart: nobody between them while the cranks turn (stop 4). The crank crew leave the cranks to dump, so a pawl must be holding first (stop 5). Tipping a full box now takes about 236 N on the longer box, shared by two people. Frame bolts must be checked tight before each day's first haul; a missing anchor-bar bolt would put the sling load on one bolt.

**Recommended next step.** Amish to answer register item 1; then, when the phase allows, TRL 4 as already recommended, with the R1 trial run using both boxes.

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

## 2026-10-03: photoreal renders redone after Amish's requirement decisions

Rendered with Blender Cycles on Amish's Mac from `cad/src/product_model.py`; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` made with `.kit/cards.py`. Views: hero, exploded, detail. image_qc passes and `render.py --check` has no FAIL.
