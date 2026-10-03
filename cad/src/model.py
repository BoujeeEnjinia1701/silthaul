"""SiltHaul parametric model (build123d), TRL 3, constructable design (SLH-DDR-002).

Run from the repo root:  python cad/src/model.py          (exports and checks)
                         python cad/src/model.py --check  (constructability checks only)
Exports STEP and STL into cad/step and cad/stl:
    silthaul-capstan.step / .stl     hand capstan: flat-pack frame with its bolts, split winding drum, bearings, chain drive,
                                     guard, ratchet and pawls, cranks (stakes and sling not included)
    silthaul-box.step / .stl         scraper box with bridles and tipping bar (two boxes are made)
    silthaul-tail.step / .stl        tail sheave block with its four floor anchors
    silthaul-ramp.step / .stl        doorway rope guard (threshold ramp with crest roller)
    silthaul-assembly.step           the whole system at the design case: tail sheave 15 m from
                                     the capstan, room 7 m long, box 1 in the room, box 2 at the dump,
                                     ropes as straight legs

Axes (site): X runs along the rope line from the tail sheave (x = 0) toward the capstan (+X),
Y is across the line, Z is up with the floor at z = 0. Box 1 and its pull rope run along y = 0; the
return leg of the loop, with box 2 on it, runs beside it along y = +300 mm. The tail rope joins the
rear bridles of the two boxes round the tail sheaves.

Constructable design, 2026-10-03 (SLH-DDR-002, decided under Amish's pre-approval of 2026-10-03):
    the hand capstan is a split winding drum: one half winds the pull rope while the other half pays
    out the return rope, single layer, so the loop length stays constant and nothing can slip;
    a 4:1 roller-chain drive from a crank shaft 850 mm up, two cranks, a 4 mm shear pin in the small
    sprocket hub that limits rope tension to about 2.5 kN, and two opposite ratchet wheels on the
    drum shaft with two pawls (one holds each direction);
    the scraper box is 450 mm wide with its open front toward the capstan, a bevelled cutting lip,
    a sloped back that rides over mud on the return stroke and a socket for a loose tipping bar;
    the tail sheave block is two 125 mm sheaves on a 10 mm floor plate held by four M12 anchors;
    the doorway rope guard is a threshold ramp with a crest roller between plywood cheeks.
Amish's requirement decisions, 2026-10-03 (SLH-DDR-003): a second scraper box on the return leg, so
the loop carries mud out on both strokes (both boxes 210 mm wide inside so they pass each other and
go through a 0.7 m door on their own lines); and a flat-pack frame: two welded side frames joined by
four bolted cross members (front and rear cross rails, top tie, anchor bar), each with 8 mm end plates.
Main dimensions and interfaces only; tolerances are TRL 4 work. The same PARAMS feed
docs/04-calcs/sizing.py (SLH-CAL-001), the drawings (cad/src/sheets.py), the concept media
(cad/src/concept_media.py), the product model and the build plan pictures.
"""
import math
import sys
from dataclasses import dataclass
from pathlib import Path

from build123d import (Box, Compound, Cylinder, Plane, Polygon, Pos, Rot, Solid, Vector, extrude,
                       export_step, export_stl, mirror)

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # site layout, design case (R5): tail sheave at x = 0, door threshold, capstan drum axis
    "x_door": 7000.0, "x_cap": 15000.0, "box_x0": 900.0,      # box_x0: rear of box 1 at rest in the room
    "box2_x0": 11900.0,                 # rear of box 2 at the dump, 11 m of travel further on the loop
    "short": {"x_door": 2200.0, "x_cap": 5600.0, "box_x0": 600.0, "box2_x0": 3000.0},   # shortened layout for pictures
    "ret_y": 300.0,                     # return leg offset from the box line
    "cap_y": 150.0,                     # capstan centre line (midway between the legs)
    # rope (BOM 16): 10 mm polyester double braid, minimum breaking strength
    "rope_d": 10.0, "rope_mbs": 18000.0,
    # 2 drum: steel tube OD x wall; flange rings OD x thickness; end discs; shaft; winding pitch
    "drum_tube": (219.1, 3.0), "ring": (280.0, 4.0), "end_disc_t": 4.0, "disc_holes": (6, 50.0, 72.0), "drum_shaft": 30.0,
    "pitch": 11.0, "travel": 12000.0, "dead_turns": 3, "spare_turns": 1,
    "hd": 200.0,                        # drum axis height
    # 3 drum bearings UCP206: centre height, base L x W x t, housing dia x width, bolt pitch
    "ucp206": (42.9, 165.0, 48.0, 17.0, 82.0, 38.1, 121.0),
    # 4 crank bearings UCP205
    "ucp205": (36.5, 140.0, 38.0, 15.0, 70.0, 34.1, 105.0),
    # 1 frame: SHS size and wall; rail x extent; crank shaft x and height; pedestal plate; braces
    "shs": (40.0, 2.0), "rail_x": (-420.0, 470.0), "xc": 150.0, "hc": 850.0,
    "pad_plate": (180.0, 50.0, 8.0), "top_plate": (150.0, 60.0, 8.0),
    "stake_tube": (33.7, 3.2, 80.0), "stake_x": (-280.0, 330.0),
    # flat-pack frame (SLH-DDR-003): cross member centres (front, rear) along X; end plate thickness;
    # M10 bolts for the cross rails and top tie, M12 for the anchor bar (shank dia, head/nut dia, head/nut thickness)
    "x_cross": (-370.0, 420.0), "end_plate": 8.0, "bolt_pitch": 70.0,
    "m10": (10.0, 19.0, 8.0), "m12": (12.0, 22.0, 10.0),
    # 5 crank shaft dia; crank radius; crank arm bar (width x thickness); handle tube dia x length
    "crank_shaft": 25.0, "crank_r": 250.0, "crank_bar": (40.0, 10.0), "handle": (32.0, 120.0),
    # 6 sprockets ISO 08B-1: teeth, pitch; chain width and depth (pitch line +- depth / 2)
    "z_small": 12, "z_big": 48, "chain_p": 12.7, "chain_w": 11.3, "chain_h": 11.8,
    "sprocket_t": 7.2, "hub": (36.0, 25.0),   # small sprocket hub OD x length
    "shear_pin": 4.0,                       # 10 shear pin, mild steel
    # 8 ratchet wheels: OD, root dia, teeth, thickness; pawl pivot (x, z)
    "ratchet": (180.0, 156.0, 24, 6.0), "pawl_pivot": (115.0, 300.0), "pawl_t": 8.0,
    # 9 chain guard: sheet thickness, clearance round the sprockets, inside depth
    "guard": (1.5, 22.0, 17.0),
    # 11 stakes: dia, length, depth below ground
    "stake": (25.0, 600.0, 480.0),
    # 17 scraper boxes (two, SLH-DDR-003): inside width, length to the lip, side height, sheet; skids; lip
    "box": (210.0, 845.0, 280.0, 2.0), "skid": (8.0, 25.0, 80.0), "back_run": 110.0, "fill": 245.0,
    "lug_t": 10.0, "bridle_reach": (300.0, 300.0),   # front and rear bridle ring distance
    "lug_rear_x": 55.0,                 # rear lug hole, behind the sloped back's foot
    "socket_drop": 65.0,                # socket axis meets the back this far below the rim
    "socket": (33.7, 3.2, 150.0), "tip_bar": (26.9, 2.6, 900.0),
    # 13 tail sheave block: plate L x W x t; sheave pitch dia, OD, width; pin dia; rope height
    "tail_plate": (300.0, 440.0, 10.0), "sheave": (125.0, 140.0, 30.0), "tail_pin": 25.0,
    "rope_z": 60.0, "anchor": (12.0, 80.0),
    # 19 doorway ramp: half length, inner width, crest height, deck sheet, cheek ply, roller
    "ramp": (420.0, 610.0, 130.0, 3.0), "cheek_t": 18.0, "roller": (60.3, 3.6, 600.0), "axle": 20.0,
    "threshold_max": 110.0, "cheek_top": 330.0,
    # materials (kg per m^3)
    "rho_steel": 7850.0, "rho_ply": 550.0, "rho_poly": 1380.0,
}


# ----------------------------------------------------------------------------- helpers
def bx(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def ycyl(x, z, r, y0, y1):
    return Pos(x, (y0 + y1) / 2, z) * Rot(90, 0, 0) * Cylinder(r, y1 - y0)


def xcyl(y, z, r, x0, x1):
    return Pos((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, x1 - x0)


def zcyl(x, y, r, z0, z1):
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


def ytube(x, z, ro, ri, y0, y1):
    return ycyl(x, z, ro, y0, y1) - ycyl(x, z, ri, y0 - 1, y1 + 1)


def _ccw(points):
    a = sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(points, points[1:] + points[:1]))
    return list(points) if a > 0 else list(points)[::-1]


def prism_xz(points, y0, y1):
    """Polygon given as (x, z) points, extruded from y0 to y1."""
    f = Plane.XZ.offset(-y0) * Polygon(*_ccw(points), align=None)
    return extrude(f, amount=-(y1 - y0))


def prism_xy(points, z0, z1):
    f = Plane.XY.offset(z0) * Polygon(*_ccw(points), align=None)
    return extrude(f, amount=z1 - z0)


def rod(a, b, r):
    """Round bar from point a to point b."""
    a, b = Vector(*a), Vector(*b)
    d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def sq_bar(a, b, s, w=None):
    """Square tube (section s x s, wall w; solid if w is None) from a to b, sides square to Y."""
    a, b = Vector(*a), Vector(*b)
    d = b - a
    L = d.length
    pl = Plane(origin=a, x_dir=(0, 1, 0), z_dir=d.normalized())
    bar = pl * Pos(0, 0, L / 2) * Box(s, s, L)
    if w:
        bar = bar - pl * Pos(0, 0, L / 2) * Box(s - 2 * w, s - 2 * w, L + 2)
    return bar


def hull2d(pts):
    """Convex hull (monotone chain) of 2D points, counter-clockwise."""
    pts = sorted(set((round(x, 4), round(y, 4)) for x, y in pts))
    if len(pts) < 3:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def circle_pts(cx, cz, r, n=48):
    return [(cx + r * math.cos(2 * math.pi * k / n), cz + r * math.sin(2 * math.pi * k / n)) for k in range(n)]


def stadium_xz(c1, r1, c2, r2, y0, y1, n=48):
    return prism_xz(hull2d(circle_pts(*c1, r1, n) + circle_pts(*c2, r2, n)), y0, y1)


def fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out.fuse(s)
    return out.clean() if hasattr(out, "clean") else out


def rotate_about_y(shape, x, z, deg):
    return Pos(x, 0, z) * Rot(0, deg, 0) * Pos(-x, 0, -z) * shape


# ----------------------------------------------------------------------------- derived numbers
def derived(P=PARAMS):
    D = {}
    od, t = P["drum_tube"]
    D["pitch_d"] = od + P["rope_d"]                          # rope centre diameter on the drum
    D["circ"] = math.pi * D["pitch_d"]
    D["turns_travel"] = P["travel"] / D["circ"]
    D["turns"] = math.ceil(D["turns_travel"]) + P["dead_turns"] + P["spare_turns"]
    D["half_len"] = D["turns"] * P["pitch"] + 5.0             # winding length of each half
    D["drum_len"] = 2 * (D["half_len"] + P["ring"][1] * 1.5)  # rings: 5 at each end, 5 in the middle
    D["yb"] = D["drum_len"] / 2 + 12.0 + P["ucp206"][2] / 2   # bearing centre plane (frame side planes)
    s = P["shs"][0]
    D["rail_in"] = D["yb"] - s / 2
    # half centres
    D["y_pull"] = -(P["ring"][1] / 2 + D["half_len"] / 2)
    D["y_ret"] = +(P["ring"][1] / 2 + D["half_len"] / 2)
    D["z_under"] = P["hd"] - D["pitch_d"] / 2                # pull rope leaves the bottom of the drum
    D["z_over"] = P["hd"] + D["pitch_d"] / 2                 # return rope leaves the top
    # chain drive
    p = P["chain_p"]
    D["pd_small"] = p / math.sin(math.pi / P["z_small"])
    D["pd_big"] = p / math.sin(math.pi / P["z_big"])
    D["od_small"] = p * (0.6 + 1 / math.tan(math.pi / P["z_small"]))
    D["od_big"] = p * (0.6 + 1 / math.tan(math.pi / P["z_big"]))
    D["ratio"] = P["z_big"] / P["z_small"]
    D["centres"] = math.hypot(P["xc"], P["hc"] - P["hd"])
    # y positions outboard of the bearings (both shafts share the sprocket plane on -Y)
    yb, bw = D["yb"], P["ucp206"][5]
    D["y_spr"] = -(yb + bw / 2 + 30.0 + P["sprocket_t"] / 2)
    D["y_hub"] = (-(yb + bw / 2 + 30.0), -(yb + bw / 2 + 30.0) + P["hub"][1])   # (outer, inner) faces
    D["y_ratchet"] = yb + bw / 2 + 8.0                       # inner face of the first ratchet wheel
    D["y_guard"] = (-(yb + 70.0), -(yb + 44.0))
    D["y_crank_p"] = (yb + 32.0, yb + 42.0)                  # +Y crank arm
    D["y_crank_m"] = (-(yb + 84.0), -(yb + 74.0))            # -Y crank arm, outboard of the guard
    D["crank_shaft_y"] = (-(yb + 86.0), yb + 44.0)
    D["drum_shaft_y"] = (D["y_spr"] - P["sprocket_t"] / 2 - 3.0, D["y_ratchet"] + 2 * P["ratchet"][3] + 4.0 + 6.0)
    return D


# ----------------------------------------------------------------------------- capstan
def _bearing(P, kind, x, y, zc):
    h, L, W, t, hd, hw, _ = P[kind]
    shaft = P["drum_shaft"] if kind == "ucp206" else P["crank_shaft"]
    base = bx(x - L / 2, x + L / 2, y - W / 2, y + W / 2, zc - h, zc - h + t)
    web = bx(x - hd * 0.42, x + hd * 0.42, y - hw / 2, y + hw / 2, zc - h + t - 0.1, zc)
    housing = ycyl(x, zc, hd / 2, y - hw / 2, y + hw / 2)
    return (base + web + housing) - ycyl(x, zc, shaft / 2, y - hw, y + hw)


def _ratchet_wheel(P, y0, first_deg, forward=True):
    od, rd, n, t = P["ratchet"]
    R, r = od / 2, rd / 2
    pts = []
    for k in range(n):
        a = math.radians(first_deg + 360.0 * k / n)
        b = math.radians(first_deg + 360.0 * (k + 1) / n)
        if forward:     # radial face at a, slope up from the root at a to the tip at the next face
            pts += [(r * math.cos(a), r * math.sin(a))]
            pts += [(R * math.cos(b - 0.002), R * math.sin(b - 0.002))]
        else:           # radial face at a, slope down from the tip at a to the root at the next face
            pts += [(R * math.cos(a + 0.002), R * math.sin(a + 0.002))]
            pts += [(r * math.cos(b), r * math.sin(b))]
    # forward: root at a then tip just before b gives the radial face at b
    wheel = prism_xz([(x, z + P["hd"]) for x, z in pts], y0, y0 + t)
    return wheel - ycyl(0, P["hd"], P["drum_shaft"] / 2, y0 - 1, y0 + t + 1)


def _pawl(P, y0, lift_deg=0.0):
    px, pz = P["pawl_pivot"]
    hd = P["hd"]
    tip_r, tip_a = 85.0, math.radians(57.5)
    tx, tz = tip_r * math.cos(tip_a), hd + tip_r * math.sin(tip_a)
    pts = hull2d(circle_pts(px, pz, 14.0, 32) + circle_pts(tx, tz, 2.5, 16) +
                 circle_pts(px - 30, pz + 16, 6.0, 16))             # thumb tab above the pivot
    s = prism_xz(pts, y0, y0 + P["pawl_t"]) - ycyl(px, pz, 6.0, y0 - 1, y0 + P["pawl_t"] + 1)
    if lift_deg:
        s = rotate_about_y(s, px, pz, lift_deg)
    return s


def anchor_bar_x(P=PARAMS):
    """x of the anchor bar centre: where the rear braces' outer faces pass drum axis height."""
    s = P["shs"][0]
    x1, xc, hd = P["rail_x"][1], P["xc"], P["hd"]
    a = (x1 - 50, s - 6)
    b = (xc + s / 2 - 2, 560.0)
    t = (hd - a[1]) / (b[1] - a[1])
    return a[0] + t * (b[0] - a[0]) - s / 2 - 8.0


PAWL_LIFT = 24.0       # degrees pawl 2 is turned up onto its stop in the pictures


def capstan_parts(P=PARAMS):
    """Capstan in its own coordinates: drum axis along Y at x = 0, z = hd; rope arrives from -X."""
    D = derived(P)
    s, w = P["shs"]
    yb = D["yb"]
    x0, x1 = P["rail_x"]
    xc, hc, hd = P["xc"], P["hc"], P["hd"]
    h6 = P["ucp206"][0]
    h5 = P["ucp205"][0]
    pad_top = hd - h6
    top_top = hc - h5
    out = {}

    def shs_x(xa, xb, y, z0):           # square tube along X
        return bx(xa, xb, y - s / 2, y + s / 2, z0, z0 + s) - bx(xa - 1, xb + 1, y - s / 2 + w, y + s / 2 - w, z0 + w, z0 + s - w)

    def shs_y(x, ya, yb_, z0):
        return bx(x - s / 2, x + s / 2, ya, yb_, z0, z0 + s) - bx(x - s / 2 + w, x + s / 2 - w, ya - 1, yb_ + 1, z0 + w, z0 + s - w)

    def shs_z(x, y, z0, z1):
        return bx(x - s / 2, x + s / 2, y - s / 2, y + s / 2, z0, z1) - bx(x - s / 2 + w, x + s / 2 - w, y - s / 2 + w, y + s / 2 - w, z0 - 1, z1 + 1)

    # flat-pack frame (SLH-DDR-003): two welded side frames, one per side, and four bolted cross members
    sides = {-1: [], 1: []}
    for sg in (-1, 1):
        y = sg * yb
        side = sides[sg]
        side.append(shs_x(x0, x1, y, 0.0))                                    # side rail
        pl, pw, pt = P["pad_plate"]
        side.append(bx(-pl / 2, pl / 2, y - pw / 2, y + pw / 2, pad_top - pt, pad_top))   # drum bearing pad
        for xp in (-60.0, 60.0):
            side.append(shs_z(xp, y, s, pad_top - pt))                         # pad posts
        tl, tw, tt = P["top_plate"]
        side.append(shs_z(xc, y, s, top_top - tt))                            # upright post
        side.append(bx(xc - tl / 2, xc + tl / 2, y - tw / 2, y + tw / 2, top_top - tt, top_top))
        side.append(sq_bar((x0 + 60, y, s - 6), (xc - s / 2 + 2, y, 640.0), s, w))   # front brace
        side.append(sq_bar((x1 - 50, y, s - 6), (xc + s / 2 - 2, y, 560.0), s, w))   # rear brace
        so, st, sl = P["stake_tube"]
        for xs in P["stake_x"]:
            ys = y + sg * (s / 2 + so / 2 - 0.5)          # 0.5 mm into the rail: a welded line contact
            side.append(zcyl(xs, ys, so / 2, 0, sl) - zcyl(xs, ys, so / 2 - st, -1, sl + 1))
    # pawl brackets and pivot pins: pawl 2 on the +Y post's outer face, pawl 1 on the +Y front brace
    px, pz = P["pawl_pivot"]
    y_r = D["y_ratchet"]
    tr = P["ratchet"][3]
    sides[1].append(bx(px - 20, xc + s / 2, yb + s / 2, yb + s / 2 + 6, pz - 30, pz + 30))
    sides[1].append(ycyl(px, pz, 6.0, yb + s / 2 + 6, y_r + 2 * tr + 4.0 + 6.0))
    sides[1].append(bx(-px - 40, -px + 22, yb + s / 2, yb + s / 2 + 6, pz - 30, pz + 30))
    sides[1].append(ycyl(-px, pz, 6.0, yb + s / 2 + 6, y_r + tr + 2.0))
    # guard tabs on the -Y post's outer face
    for zt in (430.0, 700.0):
        sides[-1].append(bx(xc - 15, xc + 15, D["y_guard"][1], -yb - s / 2, zt, zt + 3))

    # cross members, each a tube with an 8 mm end plate at each end bolted to the inner face of a side frame
    ep = P["end_plate"]
    yi = yb - s / 2                       # inner face of the side frames
    yt = yi - ep                          # tube ends
    bolts = []                            # (x, z, kind)
    cross = []
    for xcm in P["x_cross"]:              # front and rear cross rails on the ground
        cross.append(shs_y(xcm, -yt, yt, 0.0))
        for sg in (-1, 1):
            ya, yz = sorted((sg * yt, sg * yi))
            cross.append(bx(xcm - 50, xcm + 50, ya, yz, 0.0, s))
        bp = P["bolt_pitch"] / 2
        bolts += [(xcm - bp, s / 2, "m10"), (xcm + bp, s / 2, "m10")]
    zt0 = 700.0                           # top tie between the posts
    cross.append(shs_y(xc, -yt, yt, zt0))
    for sg in (-1, 1):
        ya, yz = sorted((sg * yt, sg * yi))
        cross.append(bx(xc - s / 2, xc + s / 2, ya, yz, zt0 + s / 2 - 55, zt0 + s / 2 + 55))
    bolts += [(xc, zt0 + s / 2 - 37, "m10"), (xc, zt0 + s / 2 + 37, "m10")]
    # anchor bar (40 x 40 x 3) between the rear braces at drum axis height, with a 10 mm eye plate
    # and a 22 mm hole: the sling pulls in line with the ropes, so the frame does not tip
    xa = anchor_bar_x(P)
    za = hd - s / 2
    cross.append(bx(xa - s / 2, xa + s / 2, -yt, yt, za, za + s)
                 - bx(xa - s / 2 + 3, xa + s / 2 - 3, -yt - 1, yt + 1, za + 3, za + s - 3))
    ax_, az_ = x1 - 50, s - 6                       # rear brace centre line, from its foot ...
    bx_, bz_ = xc + s / 2 - 2, 560.0                # ... to its top
    L_b = math.hypot(bx_ - ax_, bz_ - az_)
    ux, uz = (bx_ - ax_) / L_b, (bz_ - az_) / L_b
    t0 = (hd - az_) / (bz_ - az_)
    xbc = ax_ + t0 * (bx_ - ax_)                    # brace centre line at drum axis height
    for k in (-1, 1):
        bolts.append((xbc + k * 40 * ux, hd + k * 40 * uz, "m12"))
    for sg in (-1, 1):
        ya, yz = sorted((sg * yt, sg * yi))
        cross.append(bx(xa - s / 2, xbc + 30, ya, yz, hd - 52, hd + 52))
    eye = prism_xz([(xa + s / 2, hd - 25), (xa + s / 2 + 70, hd - 15), (xa + s / 2 + 70, hd + 15), (xa + s / 2, hd + 25)], -5, 5)
    cross.append(eye - ycyl(xa + s / 2 + 45, hd, 11, -6, 6))

    # bolt holes through the end plates and the side frames; bolts with the head inside, nut outside
    side_f = {sg: fuse(v) for sg, v in sides.items()}
    cross_f = fuse(cross)
    bolt_parts = []
    for bxp, bzp, kind in bolts:
        d, dh, th = P[kind]
        for sg in (-1, 1):
            ya, yz = sorted((sg * (yt - 1), sg * (yb + s / 2 + 1)))
            hole = ycyl(bxp, bzp, d / 2 + 0.5, ya, yz)
            side_f[sg] = side_f[sg] - hole
            cross_f = cross_f - hole
            y_in, y_out = sg * yt, sg * (yb + s / 2)
            shank = ycyl(bxp, bzp, d / 2, *sorted((y_in, y_out + sg * (th + 3))))
            head = ycyl(bxp, bzp, dh / 2, *sorted((y_in, y_in - sg * th)))
            nut = ycyl(bxp, bzp, dh / 2, *sorted((y_out, y_out + sg * th)))
            bolt_parts.append(shank + head + nut)
    out["frame"] = side_f[-1].fuse(side_f[1])
    out["frame_side_m"] = side_f[-1]
    out["frame_side_p"] = side_f[1]
    out["cross_members"] = cross_f
    out["frame_bolts"] = fuse(bolt_parts)

    # drum bearings and crank bearings
    out["drum_bearings"] = fuse([_bearing(P, "ucp206", 0.0, sg * yb, hd) for sg in (-1, 1)])
    out["crank_bearings"] = fuse([_bearing(P, "ucp205", xc, sg * yb, hc) for sg in (-1, 1)])

    # drum weldment: tube, rings, end discs, shaft, big sprocket on its hub, two ratchet wheels
    od, t = P["drum_tube"]
    L = D["drum_len"]
    ro, rt = P["ring"]
    sh = P["drum_shaft"]
    drum = [ytube(0, hd, od / 2, od / 2 - t, -L / 2, L / 2)]
    for yr in (-L / 2, -rt / 2, L / 2 - rt):
        drum.append(ytube(0, hd, ro / 2, od / 2, yr, yr + rt))
    nh, dh, rh = P["disc_holes"]
    for yd in (-L / 2, L / 2 - P["end_disc_t"]):
        disc = ytube(0, hd, od / 2 - t, sh / 2, yd, yd + P["end_disc_t"])
        for k in range(nh):                      # lightening holes
            a = 2 * math.pi * (k + 0.5) / nh
            disc = disc - ycyl(rh * math.cos(a), hd + rh * math.sin(a), dh / 2, yd - 1, yd + P["end_disc_t"] + 1)
        drum.append(disc)
    drum.append(ycyl(0, hd, sh / 2, *D["drum_shaft_y"]))
    ys, st_ = D["y_spr"], P["sprocket_t"]
    rb = D["od_big"] / 2
    rb_m = D["pd_big"] / 2 - P["chain_h"] / 2          # modelled to the chain's inner edge (teeth not drawn)
    big = ycyl(0, hd, rb_m, ys - st_ / 2, ys + st_ / 2) - ycyl(0, hd, sh / 2, ys - 5, ys + 5)
    drum.append(big)
    drum.append(ytube(0, hd, 25.0, sh / 2, ys + st_ / 2, -(yb + P["ucp206"][5] / 2 + 6.0)))    # big sprocket hub
    y_r = D["y_ratchet"]
    tr = P["ratchet"][3]
    drum.append(mirror(_ratchet_wheel(P, y_r, 60.0, forward=False), Plane.YZ))     # wheel 1, pawl in front
    drum.append(ytube(0, hd, 22.0, sh / 2, y_r + tr, y_r + tr + 4.0))                   # spacer collar
    drum.append(_ratchet_wheel(P, y_r + tr + 4.0, 60.0, forward=False))
    drum.append(ytube(0, hd, 22.0, sh / 2, yb + P["ucp206"][5] / 2 + 2.0, y_r))          # inner collar
    # rope anchor clamps on the end rings (one per half): a block with a U-bolt, modelled as a block
    for sg in (-1, 1):
        yy = sg * (L / 2 - rt)
        drum.append(bx(-20, 20, min(yy, yy - sg * 18), max(yy, yy - sg * 18), hd + od / 2, hd + od / 2 + 14))
    out["drum"] = fuse(drum)

    # crank shaft (with the cross hole for the shear pin), small sprocket on its hub, shear pin
    cs = P["crank_shaft"]
    ya, yz = D["crank_shaft_y"]
    hub_o, hub_l = P["hub"]
    yh0, yh1 = D["y_hub"]
    ypin = (yh0 + yh1) / 2 + 4.0
    pin = xcyl(ypin, hc, P["shear_pin"] / 2, xc - hub_o / 2 - 1.5, xc + hub_o / 2 + 1.5)
    shaft = ycyl(xc, hc, cs / 2, ya, yz) - pin
    out["crank_shaft"] = shaft
    rs = D["od_small"] / 2
    rs_m = D["pd_small"] / 2 - P["chain_h"] / 2
    small = (ycyl(xc, hc, rs_m, ys - st_ / 2, ys + st_ / 2) + ytube(xc, hc, hub_o / 2, cs / 2, ys + st_ / 2, yh1)
             - ycyl(xc, hc, cs / 2, ys - 5, yh1 + 1)) - pin
    out["small_sprocket"] = small
    out["shear_pin"] = pin

    # chain: a band round the two pitch circles
    rps, rpb = D["pd_small"] / 2, D["pd_big"] / 2
    ch = P["chain_h"]
    cw = P["chain_w"]
    chain = (stadium_xz((xc, hc), rps + ch / 2, (0, hd), rpb + ch / 2, ys - cw / 2, ys + cw / 2, 96)
             - stadium_xz((xc, hc), rps - ch / 2 + 0.6, (0, hd), rpb - ch / 2 + 0.6, ys - cw, ys + cw, 96))
    out["chain"] = chain

    # chain guard: closed sheet box round the drive, holes for both shafts and the hubs
    gt, gc, _ = P["guard"]
    g0, g1 = D["y_guard"]
    outer = stadium_xz((xc, hc), rs + gc, (0, hd), rb + gc, g0, g1, 64)
    inner = stadium_xz((xc, hc), rs + gc - gt, (0, hd), rb + gc - gt, g0 + gt, g1 - gt, 64)
    guard = outer - inner
    guard = guard - ycyl(xc, hc, hub_o / 2 + 5, g1 - gt - 1, g1 + 1) - ycyl(0, hd, 25.0 + 5, g1 - gt - 1, g1 + 1)
    guard = guard - ycyl(xc, hc, cs / 2 + 4, g0 - 1, g0 + gt + 1)
    out["guard"] = guard

    # cranks: arm with a handle on each end of the crank shaft, 180 degrees apart
    cb, ct = P["crank_bar"]
    cr = P["crank_r"]
    hdia, hlen = P["handle"]
    cranks = []
    for (y0, y1), ang, out_sign in ((D["y_crank_p"], 180.0, 1), (D["y_crank_m"], 0.0, -1)):
        a = math.radians(ang)
        ex, ez = xc + cr * math.cos(a), hc + cr * math.sin(a)
        arm = prism_xz(hull2d(circle_pts(xc, hc, cb / 2 + 6, 32) + circle_pts(ex, ez, cb / 2, 32)), y0, y1)
        arm = arm - ycyl(xc, hc, cs / 2, y0 - 1, y1 + 1)
        hy0, hy1 = (y1, y1 + hlen) if out_sign > 0 else (y0 - hlen, y0)
        handle = ycyl(ex, ez, hdia / 2, hy0, hy1)
        cranks += [arm, handle]
    out["cranks"] = fuse(cranks)

    # pawls: pawl 1 engaged (holds the haul direction), pawl 2 lifted onto its stop
    y_r = D["y_ratchet"]
    out["pawls"] = fuse([mirror(_pawl(P, y_r, 0.0), Plane.YZ), _pawl(P, y_r + tr + 4.0, PAWL_LIFT)])

    # stakes (four) through the stake tubes
    sd, sl, sdep = P["stake"]
    so = P["stake_tube"][0]
    stakes = []
    for sg in (-1, 1):
        for xs in P["stake_x"]:
            ys_ = sg * (yb + s / 2 + so / 2 - 0.5)
            ztop = P["stake_tube"][2]          # the head rests on the top of the stake tube
            stakes.append(zcyl(xs, ys_, sd / 2, ztop - sl, ztop) + zcyl(xs, ys_, 16.0, ztop, ztop + 12))
    out["stakes"] = fuse(stakes)
    return out


# ----------------------------------------------------------------------------- scraper box
def box_parts(P=PARAMS):
    """Box in its own coordinates: rear at x = 0, open front toward +X, centred on y = 0."""
    W, Lb, H, t = P["box"]
    sk_t, sk_h, sk_y = P["skid"]
    br = P["back_run"]
    wy = W / 2
    z_f = sk_h                       # floor underside
    parts = []
    # skids with the rear end cut at 45 degrees
    for sg in (-1, 1):
        parts.append(prism_xz([(br - 20 + sk_h, 0), (Lb, 0), (Lb, sk_h), (br - 20, sk_h)], sg * sk_y - sk_t / 2, sg * sk_y + sk_t / 2))
    parts.append(bx(br, Lb, -wy, wy, z_f, z_f + t))                                    # floor
    parts.append(prism_xz([(br - 2, z_f), (br, z_f), (2, z_f + H), (0, z_f + H)], -wy, wy))   # sloped back
    for sg in (-1, 1):                                                                 # sides
        y0 = wy if sg > 0 else -wy - t
        parts.append(prism_xz([(br - 2, z_f), (Lb, z_f), (Lb, z_f + H), (0, z_f + H)], y0, y0 + t))
    # cutting lip, 8 mm bar set at about 20 degrees, bevelled to the floor
    parts.append(prism_xz([(Lb, z_f + t), (Lb, z_f - 7), (Lb + 50, 0), (Lb + 60, 0), (Lb + 60, 2.5), (Lb + 8, z_f + t)],
                          -wy - t, wy + t))
    # bridle lugs: 10 mm plates on the outside of each side, front and rear
    lt = P["lug_t"]
    for sg in (-1, 1):
        y0 = wy + t if sg > 0 else -wy - t - lt
        parts.append(prism_xz([(Lb - 60, 40), (Lb + 40, 40), (Lb + 40, 110), (Lb - 60, 110)], y0, y0 + lt)
                     - ycyl(Lb + 10, 75, 9.5, y0 - 1, y0 + lt + 1))
        xr_ = P["lug_rear_x"]
        parts.append(prism_xz([(xr_ - 30, 40), (xr_ + 85, 40), (xr_ + 85, 110), (xr_ - 30, 110)], y0, y0 + lt)
                     - ycyl(xr_, 75, 9.5, y0 - 1, y0 + lt + 1))
    # tipping bar socket on the back, 45 degrees up and back
    so, st, sl = P["socket"]
    zb = z_f + H - P["socket_drop"]
    xb = br * (z_f + H - zb) / H - 2 + 1.0         # on the back plate's outer face
    dvec = (-math.sqrt(0.5), 0, math.sqrt(0.5))
    a = (xb + 12.0, 0, zb - 12.0)
    b = (a[0] + dvec[0] * sl, 0, a[2] + dvec[2] * sl)
    sock = rod(a, b, so / 2) - rod((a[0] - dvec[0] * 5, 0, a[2] - dvec[2] * 5), (b[0] + dvec[0], 0, b[2] + dvec[2]), so / 2 - st)
    # trim the part of the socket that would sit inside the box
    sock = sock - prism_xz([(br - 2, z_f), (Lb, z_f), (Lb, z_f + H + 50), (2, z_f + H + 50), (2, z_f + H)], -wy, wy)
    parts.append(sock)
    out = {"box": fuse(parts)}
    # loose tipping bar in the socket (as stowed for dumping)
    tb_o, tb_t, tb_l = P["tip_bar"]
    a2 = (a[0] + dvec[0] * 48, 0, a[2] + dvec[2] * 48)
    b2 = (a2[0] + dvec[0] * tb_l, 0, a2[2] + dvec[2] * tb_l)
    out["tip_bar"] = rod(a2, b2, tb_o / 2) - rod(a2, b2, tb_o / 2 - tb_t)
    # bridles: a shackle pin through each lug, a leg of 8 mm chain (drawn as a bar) to a pear ring
    fr, rr = P["bridle_reach"]
    zr = 75.0
    br_parts = []
    for (xl, xr) in ((Lb + 10, Lb + fr), (P["lug_rear_x"], -rr)):
        sgx = 1 if xr > xl else -1
        br_parts.append(Pos(xr + sgx * 28, 0, zr) * Rot(90, 0, 0) * (Cylinder(28, 10) - Cylinder(18, 12)))
        for sg in (-1, 1):
            y_in, y_out = sg * (wy + t), sg * (wy + t + lt + 12)
            br_parts.append(ycyl(xl, zr, 9.5, min(y_in, y_out), max(y_in, y_out)))
            yo = sg * (wy + t + lt + 6)
            br_parts.append(rod((xl, yo, zr), (xr + sgx * 6, sg * 14, zr), 4.5))
    out["bridles"] = fuse(br_parts)
    return out


# ----------------------------------------------------------------------------- tail sheave block
def tail_parts(P=PARAMS):
    """Tail sheave block: sheave A centre at (0, r), sheave B at (0, ret_y - r); floor at z = 0."""
    pl, pw, pt = P["tail_plate"]
    pd, sod, sw = P["sheave"]
    r = pd / 2
    yA, yB = r, P["ret_y"] - r
    yc = P["ret_y"] / 2
    zr = P["rope_z"]
    pin = P["tail_pin"]
    an_d, an_l = P["anchor"]
    holes = [(-110.0, yc - 170.0), (-110.0, yc + 170.0), (110.0, yc - 170.0), (110.0, yc + 170.0)]
    plate = bx(-pl / 2, pl / 2, yc - pw / 2, yc + pw / 2, 0, pt)
    for hx, hy in holes:
        plate = plate - zcyl(hx, hy, an_d / 2 + 1, -1, pt + 1)
    z_sh0, z_sh1 = zr - sw / 2, zr + sw / 2
    zk0 = z_sh1 + 5.0
    pins, spacers, sheaves = [], [], []
    for y in (yA, yB):
        pins.append(zcyl(0, y, pin / 2, pt, zk0 + 6 + 10))
        spacers.append(zcyl(0, y, 16.0, pt, z_sh0) - zcyl(0, y, pin / 2, pt - 1, z_sh0 + 1))
        fl = 6.0
        sheave = (zcyl(0, y, sod / 2, z_sh0, z_sh0 + fl) + zcyl(0, y, r - 5.5, z_sh0 + fl - 0.1, z_sh1 - fl + 0.1)
                  + zcyl(0, y, sod / 2, z_sh1 - fl, z_sh1)) - zcyl(0, y, pin / 2, z_sh0 - 1, z_sh1 + 1)
        sheaves.append(sheave)
    out = {"tail_plate": fuse([plate] + pins)}
    out["tail_spacers"] = fuse(spacers)
    out["sheaves"] = fuse(sheaves)
    keeper = bx(-20, 20, yA - 30, yB + 30, zk0, zk0 + 6)
    for y in (yA, yB):
        keeper = keeper - zcyl(0, y, pin / 2, zk0 - 1, zk0 + 7)
    out["keeper"] = keeper
    anchors = []
    for hx, hy in holes:
        anchors.append(zcyl(hx, hy, an_d / 2, -an_l, pt + 14) + zcyl(hx, hy, 12.0, pt, pt + 3)
                       + Pos(hx, hy, pt + 3 + 5) * Cylinder(10.0, 10))
    out["anchors"] = fuse(anchors)
    return out


# ----------------------------------------------------------------------------- doorway ramp
def ramp_parts(P=PARAMS):
    """Threshold ramp centred on the threshold (x = 0) and on its own centre line (y = 0)."""
    hl, wi, hcst, dt = P["ramp"]
    ct = P["cheek_t"]
    ro, rt, rl = P["roller"]
    ax = P["axle"]
    th = P["threshold_max"]
    zt = P["cheek_top"]
    yi = wi / 2
    out = {}
    cheek_pts = [(-hl, 0), (-110, 0), (-110, th), (110, th), (110, 0), (hl, 0), (hl, 12), (150, zt), (-150, zt), (-hl, 12)]
    cheeks = []
    for sg in (-1, 1):
        y0 = yi if sg > 0 else -yi - ct
        cheeks.append(prism_xz(cheek_pts, y0, y0 + ct) - ycyl(0, hcst - 20, ax / 2 + 0.5, y0 - 1, y0 + ct + 1))
    out["cheeks"] = fuse(cheeks)
    # deck trays: 3 mm sheet, top from the floor to the crest, 30 mm flanges down each side
    xe = 40.0
    decks = []
    for sg in (-1, 1):
        xb_ = hl - dt * (hl - xe) / hcst            # where the underside meets the floor
        top = [(sg * hl, 0), (sg * xe, hcst), (sg * xe, hcst - dt), (sg * xb_, 0)]
        decks.append(prism_xz(top, -yi, yi))
        for yy in (-yi, yi - dt):                   # side flanges, bolted through the cheeks
            fl = [(sg * (xb_ - 60), 0.0), (sg * xe, hcst - dt - 30), (sg * xe, hcst - dt), (sg * xb_, 0.0)]
            decks.append(prism_xz(fl, yy, yy + dt))
    out["decks"] = fuse(decks)
    zr = hcst - 20
    out["roller"] = fuse([ytube(0, zr, ro / 2, ro / 2 - rt, -rl / 2, rl / 2),
                          ytube(0, zr, ro / 2 - rt, ax / 2, -rl / 2, -rl / 2 + 20),
                          ytube(0, zr, ro / 2 - rt, ax / 2, rl / 2 - 20, rl / 2)])
    out["axle"] = ycyl(0, zr, ax / 2, -yi - ct - 12, yi + ct + 12)
    return out


# ----------------------------------------------------------------------------- site assembly
@dataclass
class Comp:
    name: str
    shape: object
    bom: int
    group: str          # capstan, box, tail, ramp, rope, anchor
    material: str


BOM = {  # key: (BOM line, plain name)
    "frame": (1, "Capstan side frames (2)"),
    "cross_members": (1, "Frame cross members (4)"),
    "frame_bolts": (21, "Frame bolts (8 M10, 4 M12)"),
    "drum": (2, "Winding drum with sprocket and ratchet wheels"),
    "drum_bearings": (3, "Drum bearings (2)"),
    "crank_bearings": (4, "Crank shaft bearings (2)"),
    "crank_shaft": (5, "Crank shaft"),
    "cranks": (5, "Cranks with handles (2)"),
    "small_sprocket": (6, "Small sprocket on its hub"),
    "chain": (7, "Roller chain"),
    "pawls": (8, "Pawls (2)"),
    "guard": (9, "Chain guard"),
    "shear_pin": (10, "Shear pin"),
    "stakes": (11, "Ground stakes (4)"),
    "sling": (12, "Anchor sling and shackle"),
    "tail_plate": (13, "Tail plate with pins"),
    "tail_spacers": (13, "Sheave spacers (2)"),
    "keeper": (13, "Keeper bar"),
    "sheaves": (14, "Tail sheaves (2)"),
    "anchors": (15, "Floor anchors (4)"),
    "ropes": (16, "Pull rope, tail rope and return rope"),
    "box": (17, "Scraper box 1"),
    "box_2": (17, "Scraper box 2"),
    "tip_bar": (18, "Tipping bar"),
    "bridles": (20, "Bridles, shackles and rings, box 1"),
    "bridles_2": (20, "Bridles, shackles and rings, box 2"),
    "cheeks": (19, "Ramp cheeks (2)"),
    "decks": (19, "Ramp decks (2)"),
    "roller": (19, "Crest roller"),
    "axle": (19, "Roller axle"),
}
MATERIAL = {"frame": "steel", "cross_members": "steel", "frame_bolts": "steel", "box_2": "steel", "bridles_2": "steel", "drum": "steel", "drum_bearings": "cast iron", "crank_bearings": "cast iron",
            "crank_shaft": "steel", "cranks": "steel", "small_sprocket": "steel", "chain": "steel",
            "pawls": "steel", "guard": "steel", "shear_pin": "steel", "stakes": "steel", "sling": "polyester",
            "tail_plate": "steel", "tail_spacers": "steel", "keeper": "steel", "sheaves": "steel",
            "anchors": "steel", "ropes": "polyester", "box": "steel", "tip_bar": "steel", "bridles": "steel",
            "cheeks": "plywood", "decks": "steel", "roller": "steel", "axle": "steel"}


def ramp_y(P=PARAMS):
    """Ramp centre line: midway between the two box lines, so both boxes cross it inside the cheeks."""
    return P["ret_y"] / 2


def site(P=PARAMS, short=False):
    L = dict(P)
    if short:
        L.update(P["short"])
    return L


def build_components(P=PARAMS, short=False):
    """Every component placed on site. Returns {key: Comp}."""
    L = site(P, short)
    D = derived(P)
    comps = {}
    cap = capstan_parts(P)
    cap_loc = Pos(L["x_cap"], P["cap_y"], 0)
    for k, s in cap.items():
        if k.startswith("frame_side"):
            continue
        comps[k] = Comp(BOM[k][1], cap_loc * s, BOM[k][0], "capstan", MATERIAL[k])
    # box 1 on the box line in the room; box 2 on the return leg at the dump, carrying the tipping bar
    bp = box_parts(P)
    for k in ("box", "bridles"):
        comps[k] = Comp(BOM[k][1], Pos(L["box_x0"], 0, 0) * bp[k], BOM[k][0], "box", MATERIAL[k])
    for k in ("box", "bridles", "tip_bar"):
        k2 = k if k == "tip_bar" else k + "_2"
        comps[k2] = Comp(BOM[k2][1], Pos(L["box2_x0"], P["ret_y"], 0) * bp[k], BOM[k2][0], "box", MATERIAL[k2])
    for k, s in tail_parts(P).items():
        comps[k] = Comp(BOM[k][1], s, BOM[k][0], "tail", MATERIAL[k])
    for k, s in ramp_parts(P).items():
        comps[k] = Comp(BOM[k][1], Pos(L["x_door"], ramp_y(P), 0) * s, BOM[k][0], "ramp", MATERIAL[k])
    # ropes as straight legs, 10 mm
    rr = P["rope_d"] / 2
    Lb = P["box"][1]
    zr = 75.0
    x_front_ring = L["box_x0"] + Lb + P["bridle_reach"][0] + 28
    x_rear_ring = L["box_x0"] - P["bridle_reach"][1] - 28
    x_front_ring2 = L["box2_x0"] + Lb + P["bridle_reach"][0] + 28
    x_rear_ring2 = L["box2_x0"] - P["bridle_reach"][1] - 28
    hcst = P["ramp"][2]
    xr = L["x_door"]
    zroll = hcst - 20 + P["roller"][0] / 2 + rr
    xd = L["x_cap"]
    ypull = P["cap_y"] + D["y_pull"]
    yret = P["cap_y"] + D["y_ret"]
    rz = P["rope_z"]
    r = P["sheave"][0] / 2
    ry = P["ret_y"]
    legs = [((x_front_ring, 0, zr), (xr, 0, zroll)), ((xr, 0, zroll), (xd, ypull, D["z_under"])),     # pull rope
            ((x_rear_ring, 0, zr), (0, 0, rz)), ((-r, r, rz), (-r, ry - r, rz)),                       # tail rope
            ((0, ry, rz), (xr, ry, zroll)), ((xr, ry, zroll), (x_rear_ring2, ry, zr)),
            ((x_front_ring2, ry, zr), (xd, yret, D["z_over"]))]                                         # return rope
    ropes = [rod(a, b, rr) for a, b in legs]
    comps["ropes"] = Comp(BOM["ropes"][1], fuse(ropes), 16, "rope", "polyester")
    # sling from the anchor eye to the anchor point (vehicle or tree) 2 m behind
    ex = L["x_cap"] + anchor_bar_x(P) + P["shs"][0] / 2 + 45
    cy = P["cap_y"]
    zs = P["hd"]
    sling = bx(ex + 40, ex + 2900, cy - 25, cy + 25, zs - 3, zs + 3)
    shackle = (ycyl(ex, zs, 11.0, cy - 16, cy + 16) + bx(ex - 11, ex + 40, cy + 5, cy + 12, zs - 11, zs + 11)
               + bx(ex - 11, ex + 40, cy - 12, cy - 5, zs - 11, zs + 11) + bx(ex + 28, ex + 40, cy - 12, cy + 12, zs - 11, zs + 11))
    comps["sling"] = Comp(BOM["sling"][1], fuse([sling, shackle]), 12, "anchor", "polyester")
    return comps


def assembly(P=PARAMS, short=False, keys=None):
    C = build_components(P, short)
    return Compound([c.shape for k, c in C.items() if keys is None or k in keys])


def context_shapes(P=PARAMS, short=True):
    """Grey context: a wall with a doorway and threshold, and a tree as the outside anchor."""
    L = site(P, short)
    xd = L["x_door"]
    ry_ = ramp_y(P)
    w2 = 380.0               # door opening half width (0.76 m)
    wall = (bx(xd - 100, xd + 100, -700, ry_ - w2, 0, 2250) + bx(xd - 100, xd + 100, ry_ + w2, 1500, 0, 2250)
            + bx(xd - 100, xd + 100, ry_ - w2, ry_ + w2, 2050, 2250))
    thr = bx(xd - 60, xd + 60, ry_ - w2, ry_ + w2, 0, 60)
    tree = zcyl(L["x_cap"] + anchor_bar_x(P) + P["shs"][0] / 2 + 45 + 2900 + 160, P["cap_y"], 160, 0, 2600)
    return {"wall": wall, "threshold": thr, "tree": tree}


# ----------------------------------------------------------------------------- checks
def _dist(a, b):
    try:
        return a.distance_to(b)
    except Exception:
        return float("nan")


def checks(P=PARAMS, verbose=True):
    """Constructability checks: no two separate parts overlap; every part touches what holds it."""
    C = build_components(P, short=True)
    keys = list(C)
    res = {"overlaps": [], "floating": [], "volumes": {}}
    for k in keys:
        res["volumes"][k] = C[k].shape.volume
    # contact pairs: the part is held by the other (bolt, weld, pin, bearing, sits on)
    holds = [("drum_bearings", "frame"), ("crank_bearings", "frame"), ("drum", "drum_bearings"),
             ("crank_shaft", "crank_bearings"), ("small_sprocket", "crank_shaft"), ("shear_pin", "crank_shaft"),
             ("shear_pin", "small_sprocket"), ("cranks", "crank_shaft"), ("guard", "frame"), ("pawls", "frame"),
             ("stakes", "frame"), ("sling", "cross_members"), ("tail_spacers", "tail_plate"), ("sheaves", "tail_spacers"),
             ("keeper", "tail_plate"), ("anchors", "tail_plate"), ("tip_bar", "box_2"), ("bridles", "box"),
             ("bridles_2", "box_2"), ("cross_members", "frame"), ("frame_bolts", "frame"),
             ("frame_bolts", "cross_members"), ("decks", "cheeks"), ("axle", "cheeks"), ("roller", "axle")]
    for a, b in holds:
        d = _dist(C[a].shape, C[b].shape)
        if not d <= 0.6:
            res["floating"].append((a, b, d))
    pairs = [(a, b) for i, a in enumerate(keys) for b in keys[i + 1:]
             if C[a].group == C[b].group or {C[a].group, C[b].group} <= {"capstan", "anchor"}]
    for a, b in pairs:
        if {a, b} in ({"bridles", "box"}, {"ropes", "bridles"}, {"bridles_2", "box_2"}, {"ropes", "bridles_2"}):
            continue
        ba, bb_ = C[a].shape.bounding_box(), C[b].shape.bounding_box()
        if (ba.min.X > bb_.max.X or bb_.min.X > ba.max.X or ba.min.Y > bb_.max.Y or bb_.min.Y > ba.max.Y
                or ba.min.Z > bb_.max.Z or bb_.min.Z > ba.max.Z):
            continue
        try:
            i = C[a].shape & C[b].shape
            v = 0.0 if i is None else i.volume
        except Exception:
            v = float("nan")
        if not v < 1.0:
            res["overlaps"].append((a, b, v))
    # the two boxes pass each other in the room: clearance with both side by side at the same x
    bp = box_parts(P)
    b1 = fuse([bp["box"], bp["bridles"]])
    b2 = Pos(0, P["ret_y"], 0) * b1
    res["pass_gap"] = _dist(b1, b2)
    if not res["pass_gap"] >= 25.0:
        res["overlaps"].append(("box", "box_2 passing", res["pass_gap"]))
    # both boxes cross the ramp inside its cheeks
    wi = P["ramp"][1] / 2
    for k in ("box", "box_2"):
        bb = C[k].shape.bounding_box()
        lo, hi = bb.min.Y - ramp_y(P), bb.max.Y - ramp_y(P)
        res.setdefault("ramp_gap", []).append(min(lo + wi, wi - hi))
    if not min(res["ramp_gap"]) >= 15.0:
        res["overlaps"].append(("boxes", "ramp cheeks", min(res["ramp_gap"])))
    # flat pack: every piece of the frame is a separate solid of known size (SLH-DDR-003)
    res["pack"] = pack_pieces(P)
    if verbose:
        print("overlaps (should be none):", res["overlaps"] or "none")
        print("parts not touching what holds them (should be none):", res["floating"] or "none")
        print(f"boxes pass {res['pass_gap']:.1f} mm apart; least gap to a ramp cheek {min(res['ramp_gap']):.1f} mm")
        for n, d, m in res["pack"]:
            print(f"pack piece {n:34s} {d[0]:5.0f} x {d[1]:4.0f} x {d[2]:4.0f} mm  {m:5.1f} kg")
    return res


def pack_pieces(P=PARAMS):
    """The kit as carried: (name, sorted bounding box dims mm, kg) for each piece, largest first."""
    cap = capstan_parts(P)
    rho = P["rho_steel"] * 1e-9
    out = []

    def add(name, shape, kg=None, n=1):
        bb = shape.bounding_box()
        d = sorted((bb.size.X, bb.size.Y, bb.size.Z), reverse=True)
        m = shape.volume * rho if kg is None else kg
        for _ in range(n):
            out.append((name, tuple(d), m))
    add("Side frame, -Y (chain side)", cap["frame_side_m"])
    add("Side frame, +Y (pawl side)", cap["frame_side_p"])
    for i, sol in enumerate(sorted(cap["cross_members"].solids(), key=lambda q: q.bounding_box().center().Z)):
        add(["Front or rear cross rail", "Front or rear cross rail", "Anchor bar with eye", "Top tie"][i], sol)
    db = cap["drum_bearings"].volume * 7200e-9
    add("Drum with its bearings", cap["drum"] + cap["drum_bearings"], cap["drum"].volume * rho + db)
    bp = box_parts(P)
    add("Scraper box (bridles off)", bp["box"], bp["box"].volume * rho, n=2)
    t = tail_parts(P)
    add("Tail block", fuse(list(t.values())), sum(v.volume for v in t.values()) * rho)
    r = ramp_parts(P)
    # the ramp comes apart for carrying: cheeks stacked flat, the two deck trays nested, roller on its axle
    cheek = r["cheeks"] & bx(-1000, 1000, 0, 1000, -10, 1000)
    bb = cheek.bounding_box()
    d = sorted((bb.size.X, bb.size.Y, bb.size.Z), reverse=True)
    out.append(("Ramp cheeks (2), stacked", (d[0], d[1], 2 * d[2]), r["cheeks"].volume * P["rho_ply"] * 1e-9))
    tray = r["decks"] & bx(0, 1000, -1000, 1000, -10, 1000)
    bb = tray.bounding_box()
    d = sorted((bb.size.X, bb.size.Y, bb.size.Z), reverse=True)
    out.append(("Ramp deck trays (2), nested", (d[0], d[1], d[2] + 30.0), r["decks"].volume * rho))
    add("Crest roller on its axle", r["roller"] + r["axle"], (r["roller"].volume + r["axle"].volume) * rho)
    out.sort(key=lambda q: -q[1][0] * q[1][1])
    return out


def masses(P=PARAMS):
    """Mass of each component in kg from model volumes (steel parts) plus catalogue figures."""
    C = build_components(P, short=False)
    rho = {"steel": P["rho_steel"], "cast iron": 7200.0, "plywood": P["rho_ply"], "polyester": P["rho_poly"]}
    m = {}
    for k, c in C.items():
        if k in ("ropes", "sling"):
            continue
        m[k] = c.shape.volume * 1e-9 * rho[c.material]
    return m


def export(P=PARAMS):
    root = Path(__file__).resolve().parents[2]
    (root / "cad" / "step").mkdir(parents=True, exist_ok=True)
    (root / "cad" / "stl").mkdir(parents=True, exist_ok=True)
    groups = {"capstan": ["frame", "cross_members", "frame_bolts", "drum", "drum_bearings", "crank_bearings",
                          "crank_shaft", "small_sprocket", "shear_pin", "chain", "guard", "cranks", "pawls"],
              "box": ["box_2", "tip_bar", "bridles_2"],
              "tail": ["tail_plate", "tail_spacers", "sheaves", "keeper", "anchors"],
              "ramp": ["cheeks", "decks", "roller", "axle"]}
    C = build_components(P, short=False)
    for g, keys in groups.items():
        cmp = Compound([C[k].shape for k in keys])
        export_step(cmp, str(root / "cad" / "step" / f"silthaul-{g}.step"))
        export_stl(cmp, str(root / "cad" / "stl" / f"silthaul-{g}.stl"), tolerance=0.5, angular_tolerance=0.3)
    export_step(Compound([c.shape for c in C.values()]), str(root / "cad" / "step" / "silthaul-assembly.step"))
    print("exported STEP and STL to cad/step and cad/stl")


if __name__ == "__main__":
    D = derived()
    print({k: (round(v, 1) if isinstance(v, float) else v) for k, v in D.items()})
    r = checks()
    for k, v in sorted(masses().items()):
        print(f"{k:16s} {v:6.2f} kg")
    if "--check" not in sys.argv:
        export()
