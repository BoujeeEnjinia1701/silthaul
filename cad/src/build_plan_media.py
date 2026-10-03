"""SiltHaul prototype build plan pictures (SLH-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps ...]
With no argument it draws everything. Every picture is drawn from cad/src/model.py, so the
pictures and the model never disagree:
    docs/05-build-plan/overview.png       every component pulled apart, numbered in build order
    cad/drawings/SLH-DWG-101 to 109       making sketches for the made components
    docs/05-build-plan/joint-NN.png       close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png        one picture per assembly step
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from build123d import Box, Pos, Rot  # noqa: E402
from model import (PARAMS as P, derived, capstan_parts, box_parts, tail_parts, ramp_parts,  # noqa: E402
                   build_components, anchor_bar_x, bx)

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-03"
D = derived(P)
CAP = capstan_parts(P)
BOX = box_parts(P)
TAIL = tail_parts(P)
RAMP = ramp_parts(P)

COL = {"frame": "#0F766E", "drum": "#C2410C", "drum_bearings": "#374151", "crank_bearings": "#4B5563",
       "crank_shaft": "#6B7280", "small_sprocket": "#B45309", "shear_pin": "#DC2626", "chain": "#78716C",
       "guard": "#CA8A04", "cranks": "#111827", "pawls": "#1D4ED8", "stakes": "#57534E", "box": "#2563EB",
       "tip_bar": "#1E3A8A", "bridles": "#475569", "tail_plate": "#0E7490", "tail_spacers": "#64748B",
       "sheaves": "#D4A017", "keeper": "#155E75", "anchors": "#111827", "cheeks": "#A16207",
       "decks": "#9CA3AF", "roller": "#15803D", "axle": "#374151", "ropes": "#E11D48", "sling": "#F97316"}


def part(name, shape, key, explode=(0, 0, 0)):
    return Part(name, shape, COL[key], None, tuple(explode))


def crop(shape, x0, x1, y0, y1, z0, z1):
    return shape & bx(x0, x1, y0, y1, z0, z1)


def stakes_above():
    s = CAP["stakes"]
    return s & bx(-2000, 2000, -2000, 2000, 0, 200)


# ----------------------------------------------------------------- overview
def overview():
    # groups laid side by side so every component shows; numbers follow the build order
    cap_dx, box_dy, tail_dy, ramp_dy = 0, -1700, -700, -2900
    items = [
        ("Capstan frame", CAP["frame"], "frame", (0, 0, 0)),
        ("Winding drum with ratchet wheels", CAP["drum"], "drum", (0, 0, 650)),
        ("Pawls (2)", CAP["pawls"], "pawls", (0, 450, 600)),
        ("Crank shaft", CAP["crank_shaft"], "crank_shaft", (0, 0, 900)),
        ("Small sprocket on its hub", CAP["small_sprocket"], "small_sprocket", (0, -350, 900)),
        ("Cranks with handles (2)", CAP["cranks"], "cranks", (0, 0, 1200)),
        ("Chain guard", CAP["guard"], "guard", (0, -700, 500)),
        ("Ground stakes (4)", stakes_above(), "stakes", (0, 0, -150)),
        ("Scraper box", BOX["box"], "box", (-300, box_dy, 0)),
        ("Tipping bar", BOX["tip_bar"], "tip_bar", (-300, box_dy, 350)),
        ("Tail plate with pins", TAIL["tail_plate"], "tail_plate", (-2800, tail_dy, 0)),
        ("Sheave spacers (2)", TAIL["tail_spacers"], "tail_spacers", (-2800, tail_dy, 200)),
        ("Keeper bar", TAIL["keeper"], "keeper", (-2800, tail_dy, 650)),
        ("Ramp cheeks (2)", RAMP["cheeks"], "cheeks", (-700, ramp_dy, 0)),
        ("Ramp decks (2)", RAMP["decks"], "decks", (-700, ramp_dy, 300)),
        ("Crest roller and axle", RAMP["roller"] + RAMP["axle"], "roller", (-700, ramp_dy, 600)),
        ("Drum bearings (2), bought", CAP["drum_bearings"], "drum_bearings", (0, 0, 350)),
        ("Crank bearings (2), bought", CAP["crank_bearings"], "crank_bearings", (0, 0, 650)),
        ("Roller chain, bought", CAP["chain"], "chain", (0, -500, 650)),
        ("Shear pin, bought", CAP["shear_pin"], "shear_pin", (0, -350, 1050)),
        ("Tail sheaves (2), bought", TAIL["sheaves"], "sheaves", (-2800, tail_dy, 420)),
        ("Floor anchors (4), bought", TAIL["anchors"], "anchors", (-2800, tail_dy, 900)),
        ("Bridles and shackles, bought", BOX["bridles"], "bridles", (-300, box_dy, 150)),
    ]
    parts = [part(n, s, k, e) for n, s, k, e in items]
    bv.overview(parts, OUT / "overview.png", "SiltHaul prototype: every component in build order",
                subtitle="Made parts first (1 to 16), then bought parts; ropes and sling not shown",
                key=True, size=(11, 7.5))


# ----------------------------------------------------------------- making sketches
def sheets():
    cap_all = [Part(k, v, "#D1D5DB") for k, v in CAP.items() if k != "stakes"]
    S = [
        ("SLH-DWG-101", "Capstan frame: making sketch", CAP["frame"], "frame",
         "40 x 40 x 2 SHS, 40 x 40 x 3 SHS anchor bar, 8 and 10 mm plate, 33.7 tube",
         ["Two side frames, each: rail 890 long, post 40 x 40 rising to 805, front and rear braces",
          "Bearing pad 180 x 50 x 8 on two short posts; top of pad 157 up",
          "Top plate 150 x 60 x 8 on the post; top 813 up, centre 150 behind the drum axis",
          f"Side frames {2 * D['yb']:.0f} apart, centre to centre; cross rails front and rear",
          "Top tie 700 up between the posts; anchor bar 40 x 40 x 3 at 180 to 220 up",
          "Anchor eye 10 mm plate, 22 mm hole 200 up, on the bar centre line",
          "Pawl brackets 6 mm on the +Y post and +Y front brace, 12 mm pins 300 up",
          "Four stake tubes 33.7 x 3.2 x 80 on the rail outsides",
          "Tack on a flat table, check diagonals within 3 mm, then weld all round",
          "Check: pads level and in line within 1 mm; top plates likewise"]),
        ("SLH-DWG-102", "Winding drum: making sketch", CAP["drum"], "drum",
         "219.1 x 3.0 tube; 4 mm rings and discs; 30 mm S355 shaft; 6 mm ratchet wheels",
         [f"Tube {D['drum_len']:.0f} long, ends square; rings 280 OD at both ends and the middle",
          f"Two winding halves of {D['half_len']:.0f}, each holds 21 turns of 10 mm rope",
          "End discs 4 mm inside the tube ends, six 50 mm lightening holes",
          f"Shaft 30, {D['drum_shaft_y'][1] - D['drum_shaft_y'][0]:.0f} long, through both discs; weld discs to tube and shaft",
          "48-tooth sprocket on a hub at the -Y end, outboard of the bearing",
          "Two ratchet wheels at the +Y end, teeth facing opposite ways, 4 mm apart",
          "Rope clamp block with a U-bolt on each end ring",
          "Weld in short stitches, turning the drum, to keep it straight",
          "Check: spins true in V-blocks within 2 mm at the rings"]),
        ("SLH-DWG-103", "Pawls: making sketch", CAP["pawls"], "pawls",
         "8 mm steel plate, profile cut",
         ["Two pawls, 12 mm pivot hole, nose 2.5 mm radius, thumb tab above the pivot",
          "Pawl 1 hangs from the front bracket; pawl 2 from the post bracket",
          "Each pawl lies in the plane of its own ratchet wheel",
          "Flip one up onto its stop to choose the direction that is held",
          "Check: the nose drops into every tooth gap by its own weight"]),
        ("SLH-DWG-104", "Crank shaft, hub and cranks: making sketch",
         CAP["crank_shaft"] + CAP["small_sprocket"] + CAP["cranks"], "crank_shaft",
         "25 mm S355 shaft; 36 mm tube hub; 40 x 10 flat; 32 mm handle tube",
         [f"Shaft 25, {D['crank_shaft_y'][1] - D['crank_shaft_y'][0]:.0f} long; 4 mm cross hole at the hub",
          "12-tooth sprocket welded to a 36 mm hub that turns freely on the shaft",
          "Drill hub and shaft together for the 4 mm shear pin",
          "Crank arms 250 between centres, 180 degrees apart, pinned to the shaft",
          "Handles 32 x 120 turn on M12 bolts",
          "Check: hub turns freely with the pin out, locks with it in"]),
        ("SLH-DWG-105", "Chain guard: making sketch", CAP["guard"], "guard",
         "1.5 mm steel sheet",
         ["Two side sheets cut to the outline round both sprockets, 22 clear",
          "Wrap band 20 deep, riveted or stitch welded to both sides",
          "Holes for the crank shaft (33) and both hubs (46, 60), 4 to 5 clear",
          "Two M6 screws to the guard tabs on the post",
          "Check: no finger can reach the chain with the guard on"]),
        ("SLH-DWG-106", "Ground stake: making sketch",
         CAP["stakes"] & bx(-1000, -200, -1000, 0, -600, 200), "stakes",
         "25 mm round bar, 32 mm washer",
         ["Four stakes, 25 bar 600 long, ground to a point",
          "32 mm washer welded on top as a head",
          "Driven through the stake tubes; the head rests on the tube",
          "They stop the frame skating; the sling is the anchor",
          "Check: straight within 3 mm"]),
        ("SLH-DWG-107", "Scraper box: making sketch", BOX["box"], "box",
         "2 mm sheet, 8 mm flat bar, 10 mm plate, 33.7 tube",
         ["Inside 446 wide, 600 long to the lip, sides 200 high",
          "Floor 520 long; back slopes 80 so it rides over mud going back",
          "Lip 8 x 50 bar set at 20 degrees, bevelled to the floor",
          "Two skids 8 x 25 under the floor, 340 apart, rear ends cut at 45 deg",
          "Four bridle lugs 10 mm, 19 mm holes 75 up: two at the front, two at the rear",
          "Tipping bar socket 33.7 x 150 at 45 deg on the back; bar 26.9 x 900 loose",
          "Check: 40 L of water to a 165 mm level fits; sits flat on its skids"]),
        ("SLH-DWG-108", "Tail plate, pins and keeper: making sketch",
         TAIL["tail_plate"] + TAIL["keeper"] + TAIL["tail_spacers"], "tail_plate",
         "10 mm plate, 25 mm S355 pins, 6 mm keeper bar",
         ["Plate 300 x 440 x 10; four 13 mm holes 220 x 340 apart",
          "Two 25 pins welded square to the plate, 175 apart",
          "Spacers 32 OD up to 45; sheave groove at 60 above the floor",
          "Keeper 40 x 6 across both pin tops, R-clips above",
          "Check: pins square within 1 deg; keeper drops over both"]),
        ("SLH-DWG-109", "Doorway ramp: making sketch",
         RAMP["cheeks"] + RAMP["decks"] + RAMP["roller"] + RAMP["axle"], "cheeks",
         "18 mm exterior plywood, 3 mm sheet, 60.3 tube, 20 mm bar",
         ["Cheeks 840 long, 330 high in the middle; notch 220 x 110 for the threshold",
          "Decks 3 mm, 610 wide, folded 30 flanges, crest 130 up",
          "Roller 60.3 x 600 on a 20 axle 110 up; stands 10 above the decks",
          "M8 bolts through cheeks and deck flanges",
          "Check: outside width 646; roller turns by hand"]),
    ]
    for dwg, title, shape, key, mat, notes in S:
        nb = cap_all if key in CAP else [Part(k, v, "#D1D5DB") for k, v in {**BOX, **TAIL, **RAMP}.items()]
        bv.component_sheet(Part(title, shape, COL[key]), [n for n in nb if n.name != key][:12], "SiltHaul", dwg,
                           title, mat, notes, DATE, out_dir=str(DWG))
        print("sheet", dwg)


# ----------------------------------------------------------------- joints
def joints():
    yb = D["yb"]
    hd, xc, hc = P["hd"], P["xc"], P["hc"]
    # 1 drum bearing on its pad
    r = (-120, 120, -yb - 60, -yb + 60, 40, 300)
    bv.joint([part("Bearing pad on the frame", crop(CAP["frame"], *r), "frame"),
              part("Drum bearing UCP206, 2 x M14", crop(CAP["drum_bearings"], *r), "drum_bearings"),
              part("Drum shaft and end ring", crop(CAP["drum"], *r), "drum")],
             OUT / "joint-01.png", "Joint 1: drum bearing on its pad", "Two M14 bolts through the pad; shaft locked by the bearing set screws")
    # 2 shear pin hub
    r2 = (xc - 60, xc + 60, D["y_spr"] - 30, -yb + 20, hc - 60, hc + 60)
    bv.joint([part("Crank shaft", crop(CAP["crank_shaft"], *r2), "crank_shaft"),
              part("Small sprocket and hub", crop(CAP["small_sprocket"], *r2), "small_sprocket"),
              part("4 mm shear pin", crop(CAP["shear_pin"], *r2), "shear_pin"),
              part("Crank bearing", crop(CAP["crank_bearings"], *r2), "crank_bearings")],
             OUT / "joint-02.png", "Joint 2: shear pin through the sprocket hub", "Cut through the shaft; the hub turns on the shaft and only the pin drives it", cut="+X")
    # 3 ratchet and pawls
    r3 = (-200, 200, yb - 30, D["drum_shaft_y"][1] + 10, 60, 360)
    bv.joint([part("Ratchet wheels on the drum shaft", crop(CAP["drum"], *r3), "drum"),
              part("Pawls: one engaged, one lifted", CAP["pawls"], "pawls"),
              part("Pawl brackets and pins", crop(CAP["frame"], *r3), "frame")],
             OUT / "joint-03.png", "Joint 3: ratchet wheels and pawls", "Seen from the +Y side; each pawl holds one direction", azim=60, elev=10)
    # 4 anchor eye and sling shackle
    xa = anchor_bar_x(P)
    C = build_components(P, short=True)
    ox = P["short"]["x_cap"]
    r4 = (ox + xa - 40, ox + xa + 250, P["cap_y"] - 150, P["cap_y"] + 150, 120, 280)
    bv.joint([part("Anchor bar and eye", crop(C["frame"].shape, *r4), "frame"),
              part("Bow shackle and round sling", crop(C["sling"].shape, *r4), "sling")],
             OUT / "joint-04.png", "Joint 4: sling on the anchor eye", "The sling pulls level with the drum axis, 200 mm up")
    # 5 box front lug and bridle
    Lb = P["box"][1]
    r5 = (Lb - 120, Lb + 340, -300, 20, 0, 230)
    bv.joint([part("Box side, lip and front lug", crop(BOX["box"], *r5), "box"),
              part("Shackle pin and chain leg", crop(BOX["bridles"], *r5), "bridles")],
             OUT / "joint-05.png", "Joint 5: front bridle on the box", "Shackle pin through the 19 mm lug hole; leg to the pear ring")
    # 6 tail sheave stack
    r6 = (-150, 150, -60, 150, -90, 120)
    bv.joint([part("Tail plate and pin", crop(TAIL["tail_plate"], *r6), "tail_plate"),
              part("Spacer", crop(TAIL["tail_spacers"], *r6), "tail_spacers"),
              part("Sheave", crop(TAIL["sheaves"], *r6), "sheaves"),
              part("Keeper bar", crop(TAIL["keeper"], *r6), "keeper"),
              part("M12 floor anchors", crop(TAIL["anchors"], *r6), "anchors")],
             OUT / "joint-06.png", "Joint 6: tail sheave on its pin", "Cut through the pin: plate, spacer, sheave, keeper, R-clip", cut="-X")
    # 7 ramp crest roller
    r7 = (-200, 200, -340, -150, 0, 340)
    bv.joint([part("Cheek", crop(RAMP["cheeks"], *r7), "cheeks"),
              part("Deck ends", crop(RAMP["decks"], *r7), "decks"),
              part("Crest roller", crop(RAMP["roller"], *r7), "roller"),
              part("Axle", crop(RAMP["axle"], *r7), "axle")],
             OUT / "joint-07.png", "Joint 7: crest roller between the cheeks", "The roller stands 10 mm above the deck ends so the rope rides on it")
    # 8 chain and sprockets with the guard cut away
    r8 = (-150, 250, D["y_spr"] - 40, -yb + 20, 60, 920)
    bv.joint([part("48-tooth sprocket on the drum", crop(CAP["drum"], *r8), "drum"),
              part("12-tooth sprocket", crop(CAP["small_sprocket"], *r8), "small_sprocket"),
              part("Roller chain", CAP["chain"], "chain"),
              part("Chain guard (cut away)", crop(CAP["guard"], -400, 400, D["y_guard"][0], (D["y_guard"][0] + D["y_guard"][1]) / 2, 0, 1100), "guard")],
             OUT / "joint-08.png", "Joint 8: chain drive inside its guard", "Outer half of the guard removed; 4:1 from crank to drum", azim=-120, elev=12)


# ----------------------------------------------------------------- steps
def steps():
    g = lambda n, k, s=None: part(n, CAP[k] if s is None else s, k)  # noqa: E731
    fr, dr = g("Frame", "frame"), g("Drum", "drum")
    db, cb = g("Drum bearings", "drum_bearings"), g("Crank bearings", "crank_bearings")
    cs, ss, sp = g("Crank shaft", "crank_shaft"), g("Small sprocket", "small_sprocket"), g("Shear pin", "shear_pin")
    ch, gd, ck, pw = g("Chain", "chain"), g("Guard", "guard"), g("Cranks", "cranks"), g("Pawls", "pawls")
    yb = D["yb"]

    def mv(p, e):
        return Part(p.name, p.shape, p.color, None, e)
    S = [
        ([dr], [mv(db, (0, 0, 0))], "Step 1: drum bearings onto the drum shaft",
         "Slide a UCP206 onto each end of the shaft, grease nipples up; set screws loose", [mv(db, (0, 0, 0))]),
        ([fr], [mv(dr, (0, 0, 500)), mv(db, (0, 0, 500))], "Step 2: lower the drum onto the pads",
         "Two people; bolt each bearing with two M14; tighten set screws", None),
        ([fr, dr, db], [mv(cb, (0, 0, 400)), mv(cs, (0, 0, 400)), mv(ss, (0, -150, 400))],
         "Step 3: crank shaft, hub and bearings onto the top plates", "Hub on the -Y end; M12 bolts; shaft turns by hand", None),
        ([fr, dr, db, cb, cs, ss], [mv(ch, (0, -250, 0))], "Step 4: fit the chain",
         "Over both sprockets; join with the connecting link, clip closed end leading", None),
        ([fr, dr, db, cb, cs, ss, ch], [mv(sp, (0, -250, 0))], "Step 5: fit the shear pin",
         "4 mm pin through hub and shaft, split pin; spares on the tag chain", None),
        ([fr, dr, db, cb, cs, ss, ch, sp], [mv(gd, (0, -350, 0))], "Step 6: chain guard on",
         "Two M6 screws to the tabs; never turn the cranks with it off", None),
        ([fr, dr, db, cb, cs, ss, ch, sp, gd], [mv(ck, (0, 0, 300))], "Step 7: cranks on",
         "180 degrees apart; pin each to the shaft", None),
        ([fr, dr, db, cb, cs, ss, ch, sp, gd, ck], [mv(pw, (0, 250, 0))], "Step 8: pawls on their pins",
         "Washer and R-clip each; flip one up onto its stop", None),
    ]
    n = 0
    for done, new, title, sub, _ in S:
        n += 1
        bv.step(done, new, OUT / f"step-{n:02d}.png", title, sub, label_done=False)
    # site steps in the shortened layout
    C = build_components(P, short=True)
    s = lambda k, nm=None, e=(0, 0, 0): Part(nm or C[k].name, C[k].shape, COL[k], None, e)  # noqa: E731
    capk = ["frame", "drum", "drum_bearings", "crank_bearings", "crank_shaft", "small_sprocket", "shear_pin", "chain", "guard", "cranks", "pawls"]
    cap_done = [s(k) for k in capk]
    stakes = Part("Ground stakes (4)", C["stakes"].shape & bx(0, 9000, -2000, 2000, 0, 300), COL["stakes"], None, (0, 0, 400))
    site = [
        ([], cap_done[:1] and [s(k) for k in capk] + [stakes, s("sling", e=(800, 0, 0))],
         "Step 9: set the capstan, stakes and sling", "At least 6 m from the door, in line; sling to a tree or vehicle"),
        (cap_done, [s("tail_plate", e=(0, 0, 400)), s("tail_spacers", e=(0, 0, 400)), s("sheaves", e=(0, 0, 400)),
                                            s("keeper", e=(0, 0, 600)), s("anchors", e=(0, 0, 800))],
         "Step 10: anchor the tail block", "Drill four 12 mm holes 80 deep in a sound slab; torque the anchors"),
        (cap_done + [s("tail_plate"), s("sheaves")],
         [s("cheeks", e=(0, 0, 500)), s("decks", e=(0, 0, 500)), s("roller", e=(0, 0, 500)), s("axle", e=(0, 0, 500))],
         "Step 11: ramp across the threshold", "Cheeks straddle the threshold; roller in line with the ropes"),
        (cap_done + [s("tail_plate"), s("sheaves"), s("cheeks"), s("decks"), s("roller")],
         [s("box", e=(0, -900, 0)), s("bridles", e=(0, -900, 0)), s("ropes", e=(0, 0, 300))],
         "Step 12: reeve the ropes and shackle the box", "Pull rope to the front bridle, return rope round the sheaves to the rear bridle"),
    ]
    for done, new, title, sub in site:
        n += 1
        bv.step(done, new, OUT / f"step-{n:02d}.png", title, sub, label_done=False, size=(9, 5.5))
    print("steps", n)


if __name__ == "__main__":
    what = sys.argv[1:] or ["overview", "sheets", "joints", "steps"]
    OUT.mkdir(parents=True, exist_ok=True)
    for w in what:
        globals()[w]()
