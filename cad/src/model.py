"""SiltHaul parametric model, kit 1.9 interface (STANDARDS section 24), detail level D3 for every option.

Run from the repo root:
    python .kit/cad_check.py --export     fidelity check, STEP per part and per assembly (cad/step/)
    python cad/src/model.py               part list with masses, constructability checks and STL (cad/stl/)

Axes (site): X runs along the rope line from the tail sheave (x = 0) toward the capstan (+X), Y is across
the line, Z is up with the floor at z = 0. Box 1 and its pull rope run along y = 0; the return leg of the
loop, with box 2 on it, runs beside it along y = +300 mm. Pictures use the shortened layout (`short=True`,
the default of `components()`); the drawing of the design case uses `short=False`.

Options (SLH-OPT-001; option A is the existing design and is carried to the drawings, BOM and build plan):
    A  hand-capstan loop: a split winding drum on a 4:1 chain drive with a shear pin and two ratchet
       wheels pulls two scraper boxes round a rope loop; a flat-pack frame; tail sheave block on four
       floor anchors; threshold ramp (SLH-DDR-001 to SLH-DDR-004)
    B  crew-hauled box: no machine; up to four people haul one box out by hand on a rope with fixed
       toggle handles, and the loaders pull it back on a tag line through the same tail block
    C  hand slurry pump: a double-acting diaphragm pump on a skid, worked by a long rocker handle, sucks
       thinned mud through a strainer inlet and delivers it by hose through the door; a flush lance fed
       from a 200 L drum loosens and thins the mud

Every part is a cad_parts.part() dict: made, bought, fastener, weld or context, with a `key` that names
the legacy component group the calculations, drawings and build-plan pictures use. BOM line numbers are
given for option A only. Main dimensions and interfaces only; tolerances are TRL 4 work.
"""
from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Box, Compound, Cylinder, Plane, Pos, Rot, Sketch, Circle, Torus, Vector, export_stl, mirror, extrude  # noqa: E402
import cad_parts as cp  # noqa: E402
from cad_parts import part, at, break_edges  # noqa: E402
import slh_units as U  # noqa: E402
from slh_parts import (bx, ycyl, xcyl, zcyl, ytube, prism_xz, rod, hull2d, circle_pts, stadium_xz, fuse,  # noqa: E402
                       rotate_about_y, tube_between, bar_between, weld_bead, ring_weld, bolt_y, bolt_z,
                       bow_shackle, pear_ring, chain_leg, be, mk)

TITLE = "SiltHaul"

# M14 is not in the kit's fastener table (ISO 4014 / 4032 / 7089 sizes); added here for the UCP206 bearing bolts.
cp.ISO.setdefault(14, (21, 8.8, 12.8, 28, 2.5, 2.0))

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
    # option B: crew-hauled box (SLH-OPT-001)
    "haul": {"rope_len": 17000.0, "n_handles": 4, "handle_pitch": 700.0, "grip": (40.0, 220.0), "brace_plate": (300.0, 400.0, 8.0)},
    # option C: hand diaphragm slurry pump on a skid (SLH-OPT-001)
    "pump": {"skid": (900.0, 500.0), "body_d": 330.0, "stroke_chamber": 40.0, "hose_d": 75.0, "lever": 1400.0, "drum_water": 200.0},
}

OPTIONS = {"A": "Hand-capstan loop", "B": "Crew-hauled box", "C": "Hand slurry pump"}
PRINCIPLES = {
    "A": "A hand-cranked split winding drum on a 4:1 chain drive pulls two scraper boxes round a rope loop, "
         "a shear pin limits the pull and two ratchets hold the load: the mechanism multiplies the crew's force.",
    "B": "No machine: up to four people haul one scraper box out on a rope with fixed toggle handles and the "
         "loaders pull it back on a tag line, so the crew's own pull is the only force.",
    "C": "A double-acting diaphragm pump worked by a long rocker handle sucks mud thinned with flush water through "
         "a strainer and delivers it by hose: the mud is moved as a slurry instead of being scraped.",
}
CHOSEN = "A"
OPTION_VIEWS = {k: {"el": 24, "az": -48, "scale": "person", "ground_z": 0.0} for k in OPTIONS}
# welds are fused metal: a bead may meet the parts it joins; the pins sit in their own sleeves and bores
ALLOWED_CONTACTS = [
    ("Welds", ""), ("Weld ring", ""), ("Pin through", ""),
    # pins carried through drilled eyes and cross-holes: the pin is the part that fills the hole
    ("Shackle pins", "Bow shackles"), ("Shackle pins", "Split pins"), ("Bow shackles", "Split pins"),
    ("Tail plate", "Split pins"), ("Roller axle", "Split pins"), ("Pins 10 mm", "Split pins"),
    # press fits and push-on fits
    ("Scraper box", "end caps"), ("Tipping bar", "end caps"), ("spigot", "hose"), ("Suction hose", "Strainer"),
    ("hose", "Hose clamps"), ("Crest roller", "rope"),
    # rope laid on the drum and clamped by its U-bolts, chain on the sprocket seats, rope threaded through the bow
    ("Winding drum", "U-bolt"), ("Winding drum", "rope"), ("sprocket", "Roller chain"),
    ("Pawl pin", "Split pin"), ("Pawl", "Pawl spring"),
    ("anchor eye", "anchor eye"), ("anchor eye", "Split pins, anchor"), ("anchor eye", "Round sling"),
]


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
    D["y_pull"] = -(P["ring"][1] / 2 + D["half_len"] / 2)
    D["y_ret"] = +(P["ring"][1] / 2 + D["half_len"] / 2)
    D["z_under"] = P["hd"] - D["pitch_d"] / 2                # pull rope leaves the bottom of the drum
    D["z_over"] = P["hd"] + D["pitch_d"] / 2                 # return rope leaves the top
    p = P["chain_p"]
    D["pd_small"] = p / math.sin(math.pi / P["z_small"])
    D["pd_big"] = p / math.sin(math.pi / P["z_big"])
    D["od_small"] = p * (0.6 + 1 / math.tan(math.pi / P["z_small"]))
    D["od_big"] = p * (0.6 + 1 / math.tan(math.pi / P["z_big"]))
    D["ratio"] = P["z_big"] / P["z_small"]
    D["centres"] = math.hypot(P["xc"], P["hc"] - P["hd"])
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


def anchor_bar_x(P=PARAMS):
    """x of the anchor bar centre: where the rear braces' outer faces pass drum axis height."""
    s = P["shs"][0]
    x1, xc, hd = P["rail_x"][1], P["xc"], P["hd"]
    a = (x1 - 50, s - 6)
    b = (xc + s / 2 - 2, 560.0)
    t = (hd - a[1]) / (b[1] - a[1])
    return a[0] + t * (b[0] - a[0]) - s / 2 - 8.0


def site(P=PARAMS, short=False):
    L = dict(P)
    if short:
        L.update(P["short"])
    return L


def ramp_y(P=PARAMS):
    """Ramp centre line: midway between the two box lines, so both boxes cross it inside the cheeks."""
    return P["ret_y"] / 2


def context_shapes(P=PARAMS, short=True):
    """Site context (not part of any option): a wall with a doorway and threshold, and a tree as the outside anchor.
    Every piece reaches 300 mm or more below the floor (z = 0) so that a ground plane at z = 0 never shows a gap."""
    L = site(P, short)
    xd = L["x_door"]
    ry_ = ramp_y(P)
    w2 = 380.0               # door opening half width (0.76 m)
    zb = -300.0
    wall = (bx(xd - 100, xd + 100, -700, ry_ - w2, zb, 2250) + bx(xd - 100, xd + 100, ry_ + w2, 1500, zb, 2250)
            + bx(xd - 100, xd + 100, ry_ - w2, ry_ + w2, 2050, 2250))
    thr = bx(xd - 60, xd + 60, ry_ - w2, ry_ + w2, zb, 60)
    tree = zcyl(L["x_cap"] + anchor_bar_x(P) + P["shs"][0] / 2 + 45 + 2900 + 160, P["cap_y"], 160, -500, 2600)
    return {"wall": wall, "threshold": thr, "tree": tree}


def _bolts(parts, items, key, bom, explode=(0, 0, 0), group="shell", tag=""):
    """Add bolt-set items [(name, shape)] as fastener parts."""
    for n, sh in items:
        parts.append(mk(n + tag, sh, "zinc_plated", "fastener", key, bom, explode, group))


# ----------------------------------------------------------------------------- capstan (option A)
def _bearing(P, kind, x, y, zc, sg):
    h, L, W, t, hd_, hw, pitch = P[kind]
    shaft = P["drum_shaft"] if kind == "ucp206" else P["crank_shaft"]
    md = 14.0 if kind == "ucp206" else 12.0
    base = bx(x - L / 2, x + L / 2, y - W / 2, y + W / 2, zc - h, zc - h + t)
    web = bx(x - hd_ * 0.42, x + hd_ * 0.42, y - hw / 2, y + hw / 2, zc - h + t - 0.1, zc)
    housing = ycyl(x, zc, hd_ / 2, y - hw / 2, y + hw / 2)
    body = base + web + housing
    for hx in (-pitch / 2, pitch / 2):
        body = body - zcyl(x + hx, y, md / 2 + 0.5, zc - h - 1, zc - h + t + 1)
    nipple = zcyl(x - 8, y, 3.0, zc + hd_ / 2 - 3, zc + hd_ / 2 + 9) + zcyl(x - 8, y, 4.2, zc + hd_ / 2 + 9, zc + hd_ / 2 + 12)
    body = body + nipple - ycyl(x, zc, shaft / 2, y - hw, y + hw)
    return body


def _sprocket(teeth, pd, t, y0, cx, cz, hub=None, bore=None):
    """Plate sprocket in the XZ plane at (cx, cz), thickness t from y0: disc to just outside the pitch circle
    with a roller seat cut at every pitch point (so the chain rollers sit in the gaps)."""
    p = 12.7
    rr = 8.51 / 2 + 0.15
    disc = ycyl(cx, cz, pd / 2 + 2.0, y0, y0 + t)
    for k in range(teeth):
        a = 2 * math.pi * k / teeth
        disc = disc - ycyl(cx + pd / 2 * math.cos(a), cz + pd / 2 * math.sin(a), rr, y0 - 1, y0 + t + 1)
    return disc


def _ratchet_wheel(P, y0, first_deg, forward=True):
    od, rd, n, t = P["ratchet"]
    R, r = od / 2, rd / 2
    pts = []
    for k in range(n):
        a = math.radians(first_deg + 360.0 * k / n)
        b = math.radians(first_deg + 360.0 * (k + 1) / n)
        if forward:
            pts += [(r * math.cos(a), r * math.sin(a))]
            pts += [(R * math.cos(b - 0.002), R * math.sin(b - 0.002))]
        else:
            pts += [(R * math.cos(a + 0.002), R * math.sin(a + 0.002))]
            pts += [(r * math.cos(b), r * math.sin(b))]
    wheel = prism_xz([(x, z + P["hd"]) for x, z in pts], y0, y0 + t)
    return wheel - ycyl(0, P["hd"], P["drum_shaft"] / 2, y0 - 1, y0 + t + 1)


def _pawl(P, y0, lift_deg=0.0):
    px, pz = P["pawl_pivot"]
    hd = P["hd"]
    tip_r, tip_a = 85.0, math.radians(57.5)
    tx, tz = tip_r * math.cos(tip_a), hd + tip_r * math.sin(tip_a)
    pts = hull2d(circle_pts(px, pz, 14.0, 32) + circle_pts(tx, tz, 2.5, 16) +
                 circle_pts(px - 30, pz + 16, 6.0, 16))
    s = prism_xz(pts, y0, y0 + P["pawl_t"]) - ycyl(px, pz, 6.0, y0 - 1, y0 + P["pawl_t"] + 1)
    if lift_deg:
        s = rotate_about_y(s, px, pz, lift_deg)
    return s


PAWL_LIFT = 24.0       # degrees pawl 2 is turned up onto its stop in the pictures


def _chain_geometry(P, D):
    """Roller centres (x, z) of the 08B-1 chain round the two sprockets (open belt) and the closed path."""
    xc, hc, hd = P["xc"], P["hc"], P["hd"]
    r1, r2 = D["pd_small"] / 2, D["pd_big"] / 2
    C1, C2 = (xc, hc), (0.0, hd)
    ux, uz = C2[0] - C1[0], C2[1] - C1[1]
    dc = math.hypot(ux, uz)
    th = math.atan2(uz, ux)
    off = math.acos((r1 - r2) / dc)
    na, nb = th - off, th + off                # outward normals of the two tangent lines
    z1, z2 = P["z_small"], P["z_big"]
    pts = []

    def arc(c, r, z, a_from, a_to):             # rollers at the sprocket's tooth angles, going ccw from a_from to a_to
        out = []
        step = 2 * math.pi / z
        k0 = math.ceil((a_from - 1e-6) / step)
        a = k0 * step
        while a <= a_to + 1e-6:
            out.append((c[0] + r * math.cos(a), c[1] + r * math.sin(a)))
            a += step
        return out
    # wrap on the big sprocket, from normal na to normal nb going the long way round the far side (away from C1)
    def norm(a, lo):
        while a < lo:
            a += 2 * math.pi
        return a
    big_from = norm(nb, 0.0)
    big_to = norm(na, big_from)
    if big_to - big_from > math.pi * 1.5:       # choose the side that wraps the far side of the big sprocket
        pass
    # which pair of normals wraps the side facing away from the other sprocket: it contains the direction th
    def contains(a0, a1, a):
        a = norm(a, a0)
        return a <= a1
    if not contains(norm(na, 0.0), norm(nb, norm(na, 0.0)), th):
        na, nb = nb, na
    # big sprocket wraps from na to nb (ccw) around direction th; small sprocket wraps from nb to na around th + pi
    a0 = norm(na, 0.0)
    a1 = norm(nb, a0)
    big = arc(C2, r2, z2, a0, a1)
    b0 = norm(nb, 0.0)
    b1 = norm(na, b0)
    small = arc(C1, r1, z1, b0, b1)
    return big, small


def capstan(P=PARAMS):
    """The capstan in its own coordinates: drum axis along Y at x = 0, z = hd; the rope arrives from -X."""
    D = derived(P)
    s, w = P["shs"]
    yb = D["yb"]
    x0, x1 = P["rail_x"]
    xc, hc, hd = P["xc"], P["hc"], P["hd"]
    h6, h5 = P["ucp206"][0], P["ucp205"][0]
    pad_top, top_top = hd - h6, hc - h5
    ep = P["end_plate"]
    yi = yb - s / 2
    yt = yi - ep
    out = []
    A = lambda *a, **k: out.append(mk(*a, **k))  # noqa: E731
    pl, pw, pt = P["pad_plate"]
    tl, tw, tt = P["top_plate"]
    p206, p205 = P["ucp206"][6], P["ucp205"][6]

    # ---- cross-member geometry first: the bolt positions drive the holes in the side frames
    bolts_cm = []          # (x, z, d, member)
    for xcm in P["x_cross"]:
        bp = P["bolt_pitch"] / 2
        bolts_cm += [(xcm - bp, s / 2, 10, f"rail{xcm:.0f}"), (xcm + bp, s / 2, 10, f"rail{xcm:.0f}")]
    zt0 = 700.0
    bolts_cm += [(xc, zt0 + s / 2 - 37, 10, "tie"), (xc, zt0 + s / 2 + 37, 10, "tie")]
    xa = anchor_bar_x(P)
    ax_, az_ = x1 - 50, s - 6
    bx_, bz_ = xc + s / 2 - 2, 560.0
    L_b = math.hypot(bx_ - ax_, bz_ - az_)
    ux, uz = (bx_ - ax_) / L_b, (bz_ - az_) / L_b
    t0 = (hd - az_) / (bz_ - az_)
    xbc = ax_ + t0 * (bx_ - ax_)
    bolts_cm += [(xbc - 40 * ux, hd - 40 * uz, 12, "anchor"), (xbc + 40 * ux, hd + 40 * uz, 12, "anchor")]

    # ---- side frames (welded weldments): rail, pad posts and plate, post and top plate, braces, stake tubes
    sides = {}
    for sg in (-1, 1):
        y = sg * yb
        sp = []
        sp.append(tube_between((x0, y, s / 2), (x1, y, s / 2), s, w))                          # side rail
        sp.append(Pos(0, y, pad_top - pt) * cp.sheet(pl, pw, pt, holes=[(-p206 / 2, 0, 15.0), (p206 / 2, 0, 15.0)]))
        for xp in (-60.0, 60.0):
            sp.append(tube_between((xp, y, s), (xp, y, pad_top - pt), s, w))                   # pad posts
        for hx in (-p206 / 2, p206 / 2):                                                       # M14 weld nuts under the pad
            sp.append(Pos(hx, y, pad_top - pt - cp.ISO[14][2]) * cp.hex_nut(14))
        sp.append(tube_between((xc, y, s), (xc, y, top_top - tt), s, w))                       # upright post
        sp.append(Pos(xc, y, top_top - tt) * cp.sheet(tl, tw, tt, holes=[(-p205 / 2, 0, 13.0), (p205 / 2, 0, 13.0)]))
        sp.append(tube_between((x0 + 60, y, s - 6), (xc - s / 2 + 2, y, 640.0), s, w))         # front brace
        sp.append(tube_between((x1 - 50, y, s - 6), (xc + s / 2 - 2, y, 560.0), s, w))         # rear brace
        so, st, sl = P["stake_tube"]
        for xs in P["stake_x"]:
            ys = y + sg * (s / 2 + so / 2 - 0.5)
            sp.append(Pos(xs, ys, 0) * cp.round_tube(so, st, sl))
        # crush sleeves for the cross member bolts (the bolts clamp through the hollow section)
        for bxp, bzp, d, _ in bolts_cm:
            sp.append(ycyl(bxp, bzp, 8.5, y - s / 2, y + s / 2))
        sides[sg] = sp
    # pawl brackets and pins: pawl 2 on the +Y post's outer face, pawl 1 on the +Y front brace
    px, pz = P["pawl_pivot"]
    y_r = D["y_ratchet"]
    tr = P["ratchet"][3]
    y_pin_end2 = y_r + 2 * tr + 4.0 + 6.0
    y_pin_end1 = y_r + tr + 2.0
    sides[1].append(bx(px - 20, xc + s / 2, yb + s / 2, yb + s / 2 + 6, pz - 30, pz + 30))
    sides[1].append(bx(-px - 40, -px + 22, yb + s / 2, yb + s / 2 + 6, pz - 30, pz + 30))
    # guard flanges on the -Y post's outer face
    gt, gc, _ = P["guard"]
    g0, g1 = D["y_guard"]
    for zt in (430.0, 700.0):
        sides[-1].append(bx(xc - 15, xc + 15, g1, -yb - s / 2, zt, zt + 3))                    # web welded to the post
        sides[-1].append(bx(xc - 15, xc + 15, g1, g1 + 3, zt - 13.5, zt + 16.5))               # flange against the guard
    # bolt holes through the side frames
    for sg in (-1, 1):
        shp = fuse(sides[sg])
        for bxp, bzp, d, _ in bolts_cm:
            shp = shp - ycyl(bxp, bzp, d / 2 + 0.5, sg * yb - s / 2 - 1, sg * yb + s / 2 + 1)
        for zt in (430.0, 700.0):
            shp = shp - ycyl(xc - 6.0, zt + 10.0, 3.3, g1 - 1, g1 + 4)
        # pawl bracket pin holes (+Y only)
        if sg == 1:
            shp = shp - ycyl(px, pz, 6.0, yb + s / 2 - 1, yb + s / 2 + 7) - ycyl(-px, pz, 6.0, yb + s / 2 - 1, yb + s / 2 + 7)
        sides[sg] = shp
    A("Side frame -Y (chain side)", sides[-1], "painted_steel", "made", "frame", 1, (0, 0, 0))
    A("Side frame +Y (pawl side)", sides[1], "painted_steel", "made", "frame", 1, (0, 0, 0))

    # ---- welds on the side frames: plates onto their posts
    for sg in (-1, 1):
        y = sg * yb
        wl = []
        for xp in (-60.0, 60.0):
            for e in (-1, 1):
                wl.append(weld_bead((xp - 20, y + e * 20, pad_top - pt), (xp + 20, y + e * 20, pad_top - pt), (0, e, 0), (0, 0, -1), 4.0))
        for e in (-1, 1):
            wl.append(weld_bead((xc - 20, y + e * 20, top_top - tt), (xc + 20, y + e * 20, top_top - tt), (0, e, 0), (0, 0, -1), 4.0))
        A(f"Welds, side frame {'+Y' if sg > 0 else '-Y'} (plates to posts)", Compound(wl), "mild_steel", "weld", "frame", None, (0, 0, 0))

    # ---- cross members: tube with an end plate welded on each end
    def end_plate(ycen_in, sg, wd, ht, xcen, zcen, holes):
        """8 mm plate between the tube end (at |y| = yt) and the side frame (|y| = yi)."""
        y_hi = max(sg * yt, sg * yi)
        shp = cp.sheet(wd, ht, ep, holes=holes, r_corner=4.0)
        return at(shp, (xcen, y_hi, zcen), (90, 0, 0))

    cms = {}
    for i, xcm in enumerate(P["x_cross"]):
        name = "Front cross rail" if i == 0 else "Rear cross rail"
        bp = P["bolt_pitch"] / 2
        parts_ = [tube_between((xcm, -yt, s / 2), (xcm, yt, s / 2), s, w)]
        for sg in (-1, 1):
            parts_.append(end_plate(0, sg, 100.0, s, xcm, s / 2, [(-bp, 0, 11.0), (bp, 0, 11.0)]))
        cms[name] = (fuse(parts_), "rail")
    parts_ = [tube_between((xc, -yt, zt0 + s / 2), (xc, yt, zt0 + s / 2), s, w)]
    for sg in (-1, 1):
        parts_.append(end_plate(0, sg, 40.0, 110.0, xc, zt0 + s / 2, [(0, -37.0, 11.0), (0, 37.0, 11.0)]))
    cms["Top tie"] = (fuse(parts_), "tie")
    za = hd - s / 2
    xa_lo, xa_hi = xa - s / 2, xbc + 30
    abar = tube_between((xa, -yt, hd), (xa, yt, hd), s, 3.0)
    parts_ = [abar]
    for sg in (-1, 1):
        pcx = (xa_lo + xa_hi) / 2
        parts_.append(end_plate(0, sg, xa_hi - xa_lo, 104.0, pcx, hd,
                                [(xbc - 40 * ux - pcx, -40 * uz, 13.0), (xbc + 40 * ux - pcx, 40 * uz, 13.0)]))
    eye = prism_xz([(xa + s / 2, hd - 25), (xa + s / 2 + 70, hd - 15), (xa + s / 2 + 70, hd + 15), (xa + s / 2, hd + 25)], -5, 5)
    eye = be(eye - ycyl(xa + s / 2 + 45, hd, 11, -6, 6), 1.0)
    parts_.append(eye)
    cms["Anchor bar with eye"] = (fuse(parts_), "anchor")
    for n, (shp, kind) in cms.items():
        A(n, shp, "painted_steel", "made", "cross_members", 1, (0, 0, 250))
    # end plate welds: four short beads where each tube meets its plates (all four members)
    for n, (shp, kind) in cms.items():
        wl = []
        for sg in (-1, 1):
            yy = sg * yt
            cx_, cz_ = {"Front cross rail": (P["x_cross"][0], s / 2), "Rear cross rail": (P["x_cross"][1], s / 2),
                        "Top tie": (xc, zt0 + s / 2), "Anchor bar with eye": (xa, hd)}[n]
            hh = s / 2
            wl += [weld_bead((cx_ - hh, yy, cz_ + hh), (cx_ + hh, yy, cz_ + hh), (0, 0, 1), (0, -sg, 0), 3.0),
                   weld_bead((cx_ - hh, yy, cz_ - hh), (cx_ + hh, yy, cz_ - hh), (0, 0, -1), (0, -sg, 0), 3.0)]
        A(f"Welds, {n.lower()} (end plates)", Compound(wl), "mild_steel", "weld", "cross_members", None, (0, 0, 250))

    # ---- frame bolts: eight M10 and four M12 with nyloc-style nuts (hex nuts drawn), heads inside
    fb = []
    for bxp, bzp, d, mem in bolts_cm:
        for sg in (-1, 1):
            items = bolt_y(d, ep + s, bxp, bzp, sg * yt, sg, L=70)
            _bolts(fb, items, "frame_bolts", 21, (0, 0, 250))
    out += fb

    # ---- bearings (bought) and their bolts
    for sg in (-1, 1):
        y = sg * yb
        A(f"Pillow block bearing UCP206 {'+Y' if sg > 0 else '-Y'}", _bearing(P, "ucp206", 0.0, y, hd, sg), "mild_steel", "bought",
          "drum_bearings", 3, (0, 0, 400))
        A(f"Pillow block bearing UCP205 {'+Y' if sg > 0 else '-Y'}", _bearing(P, "ucp205", xc, y, hc, sg), "mild_steel", "bought",
          "crank_bearings", 4, (0, 0, 1350))
        for hx in (-p206 / 2, p206 / 2):    # M14 x 50 into the weld nut under the pad
            zb = pad_top + P["ucp206"][3]
            wsh = Pos(hx, y, zb) * cp.washer(14)
            bolt = Pos(hx, y, zb + cp.ISO[14][4]) * cp.hex_bolt(14, 50)
            out.append(mk("M14 washer (ISO 7089)", wsh, "zinc_plated", "fastener", "frame_bolts", 21, (0, 0, 400)))
            out.append(mk("M14x50 hex bolt (ISO 4017)", bolt, "zinc_plated", "fastener", "frame_bolts", 21, (0, 0, 400)))
        for hx in (-p205 / 2, p205 / 2):    # M12 x 45 through the top plate, nut underneath
            zb = top_top + P["ucp205"][3]
            items = bolt_z(12, P["ucp205"][3] + tt, xc + hx, y, zb, -1, L=45)
            _bolts(out, items, "frame_bolts", 21, (0, 0, 1350))

    # ---- drum: tube, three rings, two end discs with lightening holes, all welded
    od, t = P["drum_tube"]
    L = D["drum_len"]
    ro, rt = P["ring"]
    sh = P["drum_shaft"]
    dr = [ytube(0, hd, od / 2, od / 2 - t, -L / 2, L / 2)]
    ring_y = (-L / 2, -rt / 2, L / 2 - rt)
    for yr in ring_y:
        dr.append(ytube(0, hd, ro / 2, od / 2, yr, yr + rt))
    nh, dh, rh = P["disc_holes"]
    for yd in (-L / 2, L / 2 - P["end_disc_t"]):
        disc = ytube(0, hd, od / 2 - t, sh / 2, yd, yd + P["end_disc_t"])
        for k in range(nh):
            a = 2 * math.pi * (k + 0.5) / nh
            disc = disc - ycyl(rh * math.cos(a), hd + rh * math.sin(a), dh / 2, yd - 1, yd + P["end_disc_t"] + 1)
        dr.append(disc)
    # rope clamp blocks, one per end ring, with a U-bolt each
    clamp_y = {}
    for sg in (-1, 1):
        yy = sg * (L / 2 - rt)
        ya, yb2 = sorted((yy, yy - sg * 18))
        clamp_y[sg] = (ya, yb2)
        blk = bx(-20, 20, ya, yb2, hd + od / 2, hd + od / 2 + 14)
        for hx in (-12.0, 12.0):
            blk = blk - zcyl(hx, (ya + yb2) / 2, 4.5, hd + od / 2 - 1, hd + od / 2 + 15)
        dr.append(be(blk, 1.0))
    A("Winding drum weldment", fuse(dr), "painted_steel", "made", "drum", 2, (0, 0, 700))
    wl = []
    for yr in ring_y:
        for e, face in ((0, 1), (rt, -1)):
            wl.append(ring_weld((0, yr + e, hd), "y", od / 2, 3.0, face))
    A("Weld rings, drum rings to tube", Compound(wl), "mild_steel", "weld", "drum", None, (0, 0, 700))
    for sg in (-1, 1):
        ya, yb2 = clamp_y[sg]
        yc_ = (ya + yb2) / 2
        zb = hd + od / 2 + 14
        u = cp.rope([(-12, yc_, zb + 30), (-12, yc_, zb - 20), (12, yc_, zb - 20), (12, yc_, zb + 30)], 8.0)
        A("Rope clamp U-bolt M8", u, "zinc_plated", "fastener", "drum", 2, (0, 0, 700))
    # drum shaft (S355, 30 mm) and what sits on it
    ya, yz = D["drum_shaft_y"]
    A("Drum shaft 30 mm", _y_bar(0.0, hd, sh, ya, yz), "mild_steel", "made", "drum", 2, (0, 0, 700))
    ys, st_ = D["y_spr"], P["sprocket_t"]
    big_pl = _sprocket(P["z_big"], D["pd_big"], st_, ys - st_ / 2, 0.0, hd) - ycyl(0, hd, sh / 2, ys - 5, ys + 5)
    A("48-tooth sprocket ISO 08B-1", be(big_pl, 0.4), "zinc_plated", "bought", "small_sprocket", 6, (0, -350, 700))
    hub_y1 = -(yb + P["ucp206"][5] / 2 + 6.0)
    hub = ytube(0, hd, 25.0, sh / 2, ys + st_ / 2, hub_y1)
    A("Sprocket hub collar", be(hub, 1.0), "mild_steel", "made", "drum", 2, (0, -350, 700))
    A("Weld rings, sprocket hub", Compound([ring_weld((0, ys + st_ / 2, hd), "y", 25.0, 3.0, 1),
                                           ring_weld((0, hub_y1, hd), "y", sh / 2, 3.0, -1)]), "mild_steel", "weld", "drum", None, (0, -350, 700))
    # ratchet wheels, each with a 4 mm collar between; inner collar against the bearing
    y_r = D["y_ratchet"]
    A("Ratchet wheel 1 (pawl in front)", be(mirror(_ratchet_wheel(P, y_r, 60.0, forward=False), Plane.YZ), 0.5),
      "mild_steel", "made", "drum", 2, (0, 450, 700))
    A("Ratchet wheel 2", be(_ratchet_wheel(P, y_r + tr + 4.0, 60.0, forward=False), 0.5), "mild_steel", "made", "drum", 2, (0, 450, 700))
    A("Collar between the ratchet wheels", be(ytube(0, hd, 22.0, sh / 2, y_r + tr, y_r + tr + 4.0), 0.5), "mild_steel", "made", "drum", 2, (0, 450, 700))
    A("Inner collar at the bearing", be(ytube(0, hd, 22.0, sh / 2, yb + P["ucp206"][5] / 2 + 2.0, y_r), 0.5), "mild_steel", "made", "drum", 2, (0, 450, 700))
    A("Weld rings, ratchet wheels", Compound([ring_weld((0, y_r + 2 * tr + 4.0, hd), "y", sh / 2, 3.0, 1)]), "mild_steel", "weld", "drum", None, (0, 450, 700))

    # ---- crank shaft (S355, 25 mm) with the shear pin cross hole, small sprocket on its hub, shear pin
    cs = P["crank_shaft"]
    ya_, yz_ = D["crank_shaft_y"]
    hub_o, hub_l = P["hub"]
    yh0, yh1 = D["y_hub"]
    ypin = (yh0 + yh1) / 2 + 4.0
    pin_len = 44.0
    pin = at(cp.round_bar(P["shear_pin"], pin_len), (xc - pin_len / 2, ypin, hc), (0, 90, 0))
    shaft = _y_bar(xc, hc, cs, ya_, yz_) - xcyl(ypin, hc, P["shear_pin"] / 2, xc - 30, xc + 30)
    A("Crank shaft 25 mm", shaft, "mild_steel", "made", "crank_shaft", 5, (0, 0, 1550))
    sm = _sprocket(P["z_small"], D["pd_small"], st_, ys - st_ / 2, xc, hc)
    sm = sm + ytube(xc, hc, hub_o / 2, cs / 2 + 0.5, ys + st_ / 2 - 0.5, yh1)
    sm = sm - ycyl(xc, hc, cs / 2 + 0.5, ys - 5, yh1 + 1) - xcyl(ypin, hc, P["shear_pin"] / 2, xc - 30, xc + 30)
    A("12-tooth sprocket on its hub", be(sm, 0.4), "zinc_plated", "bought", "small_sprocket", 6, (0, -350, 1550))
    A("Shear pin 4 mm S235", pin, "mild_steel", "bought", "shear_pin", 10, (0, -350, 1650))
    # chain: rollers in the sprocket seats and the two side plates
    big, small = _chain_geometry(P, D)
    rl_y0, rl_y1 = ys - 7.75 / 2, ys + 7.75 / 2
    rollers = [ycyl(x, z, 8.51 / 2, rl_y0, rl_y1) for x, z in big + small]
    # straight spans: equally spaced rollers between the last and the first roller of each wrap
    def span(a, b):
        L_ = math.dist(a, b)
        n = max(1, round(L_ / P["chain_p"]))
        return [(a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n) for k in range(1, n)]
    ends = [(big[0], small[-1]), (big[-1], small[0])]
    for a, b in ends:
        for x, z in span(a, b):
            rollers.append(ycyl(x, z, 8.51 / 2, rl_y0, rl_y1))
    ch = P["chain_h"]
    rps, rpb = D["pd_small"] / 2, D["pd_big"] / 2
    plates = []
    for yy0 in (ys + 7.75 / 2, ys - 7.75 / 2 - 1.6):
        plates.append(stadium_xz((xc, hc), rps + ch / 2, (0, hd), rpb + ch / 2, yy0, yy0 + 1.6, 96)
                      - stadium_xz((xc, hc), rps - ch / 2 + 0.6, (0, hd), rpb - ch / 2 + 0.6, yy0 - 1, yy0 + 2.6, 96))
    A("Roller chain ISO 08B-1", Compound(rollers + plates), "zinc_plated", "bought", "chain", 7, (0, -600, 900))

    # ---- chain guard: closed sheet box round the drive, holes for both shafts and the hubs; two M6 screws
    rs = D["od_small"] / 2
    rb = D["od_big"] / 2
    outer = stadium_xz((xc, hc), rs + gc, (0, hd), rb + gc, g0, g1, 64)
    inner = stadium_xz((xc, hc), rs + gc - gt, (0, hd), rb + gc - gt, g0 + gt, g1 - gt, 64)
    guard = outer - inner
    guard = guard - ycyl(xc, hc, hub_o / 2 + 5, g1 - gt - 1, g1 + 1) - ycyl(0, hd, 25.0 + 5, g1 - gt - 1, g1 + 1)
    guard = guard - ycyl(xc, hc, cs / 2 + 4, g0 - 1, g0 + gt + 1)
    for zt in (430.0, 700.0):
        guard = guard - ycyl(xc - 6.0, zt + 10.0, 3.3, g0 - 1, g1 + 1)
    A("Chain guard", guard, "galvanised", "made", "guard", 9, (0, -900, 900))
    for zt in (430.0, 700.0):
        A("Guard spacer tube", _y_tube(xc - 6.0, zt + 10.0, 4.0, 3.3, g0 + gt, g1 - gt), "galvanised", "made", "guard", 9, (0, -900, 900))
        items = bolt_y(6, 2 * gt + (g1 - g0 - 2 * gt) + 3.0, xc - 6.0, zt + 10.0, g0, 1, L=35)
        _bolts(out, items, "frame_bolts", 21, (0, -900, 900))

    # ---- cranks: arm with a handle tube on each end of the crank shaft, 180 degrees apart; collars
    cb, ct = P["crank_bar"]
    cr = P["crank_r"]
    hdia, hlen = P["handle"]
    for (y0, y1), ang, out_sign, nm in ((D["y_crank_p"], 180.0, 1, "+Y"), (D["y_crank_m"], 0.0, -1, "-Y")):
        a = math.radians(ang)
        ex, ez = xc + cr * math.cos(a), hc + cr * math.sin(a)
        arm = prism_xz(hull2d(circle_pts(xc, hc, cb / 2 + 6, 32) + circle_pts(ex, ez, cb / 2, 32)), y0, y1)
        arm = arm - ycyl(xc, hc, cs / 2, y0 - 1, y1 + 1) - ycyl(ex, ez, 6.5, y0 - 1, y1 + 1)
        A(f"Crank arm {nm}", be(arm, 0.8), "painted_steel", "made", "cranks", 5, (0, 0, 1850))
        hy0, hy1 = (y1 + 2.0, y1 + 2.0 + hlen) if out_sign > 0 else (y0 - 2.0 - hlen, y0 - 2.0)
        A(f"Crank handle tube {nm}", _y_tube(ex, ez, hdia / 2, hdia / 2 - 3.0, hy0, hy1), "matte_black", "made", "cranks", 5, (0, 0, 1850))
        # M12 bolt through the arm and the handle tube, nut and washer at the end of the handle
        grip = (y1 - y0) + 2.0 + hlen
        yh = (y0 if out_sign > 0 else y1)
        items = bolt_y(12, grip, ex, ez, yh, out_sign, L=int(math.ceil((grip + 2 * cp.ISO[12][4] + cp.ISO[12][2] + 3) / 5) * 5))
        _bolts(out, items, "cranks", 5, (0, 0, 1850))
        # shaft collar next to the arm (retained by a set screw, not drawn)
        cy0, cy1 = (y1, y1 + 4.0) if out_sign > 0 else (y0 - 4.0, y0)
    for nm, (cy0, cy1) in (("+Y", (D["y_crank_p"][1], D["y_crank_p"][1] + 6.0)), ("-Y", (D["y_crank_m"][0] - 6.0, D["y_crank_m"][0]))):
        A(f"Crank shaft collar {nm}", be(_y_tube(xc, hc, 22.0, cs / 2, cy0, cy1), 0.5), "mild_steel", "made", "crank_shaft", 5, (0, 0, 1850))

    # ---- pawls on 12 mm pins, split pins
    pw1 = mirror(_pawl(P, y_r, 0.0), Plane.YZ)
    pw2 = _pawl(P, y_r + tr + 4.0, PAWL_LIFT)
    A("Pawl 1 (engaged)", be(pw1, 0.5), "painted_steel", "made", "pawls", 8, (0, 450, 700))
    A("Pawl 2 (lifted onto its stop)", be(pw2, 0.5), "painted_steel", "made", "pawls", 8, (0, 450, 700))
    for nm, xp_, y_end in (("1", -px, y_pin_end1), ("2", px, y_pin_end2)):
        A(f"Pawl pin {nm} 12 mm", _y_bar(xp_, pz, 12.0, yb + s / 2 + 6, y_end), "mild_steel", "made", "frame", 1, (0, 450, 700))
        out.append(mk(f"Split pin, pawl pin {nm}", at(cp.split_pin(12.0), (xp_, y_end - 3.0, pz), (0, 0, 90)), "zinc_plated", "fastener", "pawls", 8, (0, 450, 700)))
    spr_rest = cp.rope([(px - 14, y_r + tr + 4.0 + 4, pz + 20), (px - 6, y_r + tr + 4.0 + 4, pz + 30), (px + 2, y_r + tr + 4.0 + 4, pz + 20)], 1.5)
    A("Pawl spring", spr_rest, "zinc_plated", "bought", "pawls", 8, (0, 450, 700))

    # ---- stakes (four), heads resting on the stake tubes
    sd, sl, sdep = P["stake"]
    so = P["stake_tube"][0]
    ztop = P["stake_tube"][2]
    for sg in (-1, 1):
        for xs in P["stake_x"]:
            ys_ = sg * (yb + s / 2 + so / 2 - 0.5)
            stk = cp.round_bar(sd, sl)
            shp = Pos(xs, ys_, ztop - sl) * (stk + Pos(0, 0, sl + 3) * Cylinder(16.0, 6.0))
            shp = be(shp, 0.6)
            A(f"Ground stake {'+Y' if sg > 0 else '-Y'} {'front' if xs < 0 else 'rear'}", shp, "mild_steel", "made", "stakes", 11, (0, 0, 0))
    return out


def _y_bar(x, z, d, y0, y1):
    """Round bar along Y between y0 and y1 (chamfered ends)."""
    return Pos(x, y0, z) * Rot(-90, 0, 0) * cp.round_bar(d, y1 - y0)


def _y_tube(x, z, ro, ri, y0, y1):
    return be(Pos(x, y0, z) * Rot(-90, 0, 0) * cp.round_tube(2 * ro, ro - ri, y1 - y0), 0.4)


# ----------------------------------------------------------------------------- placing and rigging
_CACHE = {}


def _cached(name, fn, *a):
    if name not in _CACHE:
        _CACHE[name] = fn(*a)
    return _CACHE[name]


def _place(parts, loc, group=None):
    out = []
    for p in parts:
        q = dict(p, shape=loc * p["shape"])
        if group:
            q["group"] = group
        out.append(q)
    return out


def sling_parts(P, L):
    """Round sling from the anchor eye to the tree, with the bow shackle on the eye (BOM 12)."""
    xa = anchor_bar_x(P)
    ex = L["x_cap"] + xa + P["shs"][0] / 2 + 45
    cy, zs = P["cap_y"], P["hd"]
    out = []
    ys = (cy - 11.0, cy + 11.0)
    bow = Pos(ex, cy, zs) * bow_shackle(22.0, 50.0, 10.0)
    pin = U.cp_pin(ex, zs, cy - 17.0, cy + 17.0, 19.0)
    out.append(mk("Bow shackle on the anchor eye", bow, "galvanised", "bought", "sling", 12, (400, 0, 0), "internal"))
    out.append(mk("Shackle pin 19 mm on the anchor eye", pin, "zinc_plated", "bought", "sling", 12, (400, 0, 0), "internal"))
    sp = [cp.at(cp.split_pin(19.0), (ex, ye + (-1.5 if ye > cy else 1.5), zs), (0, 0, 90)) for ye in (cy - 17.0, cy + 17.0)]
    out.append(mk("Split pins, anchor shackle", Compound(sp), "zinc_plated", "fastener", "sling", 12, (400, 0, 0), "internal"))
    x0 = ex + 55.0
    x1 = ex + 2900.0
    r = 14.0
    pts = [(x0 + r, cy - r, zs)]
    pts += [(x0 + r - r * math.sin(math.radians(a)), cy - r * math.cos(math.radians(a)), zs) for a in range(15, 181, 15)]
    pts += [(x1 - r + r * math.sin(math.radians(a)), cy + r * math.cos(math.radians(a)), zs) for a in range(15, 181, 15)]
    loop = [(x0 + r, cy - r, zs), (x1 - r, cy - r, zs)]
    for a in range(15, 181, 15):
        loop.append((x1 - r + r * math.sin(math.radians(a)), cy - r * math.cos(math.radians(a)), zs))
    loop += [(x0 + r, cy + r, zs)]
    for a in range(15, 181, 15):
        loop.append((x0 + r - r * math.sin(math.radians(a)), cy + r * math.cos(math.radians(a)), zs))
    out.append(mk("Round sling WLL 2 t, 3 m", cp.rope(loop, 25.0), "rope", "bought", "sling", 12, (400, 0, 0), "internal"))
    return out


def ropes_a(P, L, D, ends):
    zr = 75.0
    ry = P["ret_y"]
    xd = L["x_cap"]
    ypull = P["cap_y"] + D["y_pull"]
    yret = P["cap_y"] + D["y_ret"]
    zroll = ends["zroll"]
    pull = [(ends["front1"], 0, zr), (L["x_door"], 0, zroll), (xd, ypull, D["z_under"])]
    tail = [(ends["rear1"], 0, zr)] + U.tail_arc_points(P) + [(L["x_door"], ry, zroll), (ends["rear2"], ry, zr)]
    ret = [(ends["front2"], ry, zr), (xd, yret, D["z_over"])]
    out = []
    for nm, pts in (("Pull rope (box 1 to the drum)", pull), ("Tail rope (box 1 round the tail sheaves to box 2)", tail), ("Return rope (box 2 to the drum)", ret)):
        out.append(mk(nm, cp.rope(pts, P["rope_d"]), "rope", "bought", "ropes", 16, (0, 0, 300), "internal"))
    return out


def option_a(P, L, D, ends):
    parts = _place(_cached("cap", capstan, P), Pos(L["x_cap"], P["cap_y"], 0), "shell")
    parts += _place(U.box_unit(P, "", bom=True, with_bar=False), Pos(L["box_x0"], 0, 0))
    parts += _place(U.box_unit(P, "_2", bom=True, with_bar=True), Pos(L["box2_x0"], P["ret_y"], 0))
    parts += U.tail_unit(P, bom=True)
    parts += _place(U.ramp_unit(P, bom=True), Pos(L["x_door"], ramp_y(P), 0))
    parts += ropes_a(P, L, D, ends)
    parts += sling_parts(P, L)
    return parts


def option_b(P, L, D, ends):
    import opt_b
    return opt_b.option_b(P, L, D, ends)


def option_c(P, L, D, ends):
    import opt_c
    xp = L["x_door"] + 2000.0
    parts = _cached("pump", opt_c.pump_frame, P)
    return _place(parts, Pos(xp, P["cap_y"], 0) * Rot(0, 0, -90))


def components(option=CHOSEN, short=True):
    """Parts of one option as cad_parts.part() dicts. short=True is the shortened picture layout (default);
    short=False is the design case of the drawing (tail sheave 15 m from the capstan)."""
    L = site(PARAMS, short)
    D = derived(PARAMS)
    ends = U.ring_ends(PARAMS, L)
    return {"A": option_a, "B": option_b, "C": option_c}[option](PARAMS, L, D, ends)


# ----------------------------------------------------------------------------- views for the calculations, drawings and pictures
def by_key(parts):
    """Group parts by their legacy component key: {key: Compound}."""
    d = {}
    for p in parts:
        d.setdefault(p["key"], []).extend(p["shape"].solids())
    return {k: Compound(v) for k, v in d.items()}


@dataclass
class Comp:
    name: str
    shape: object
    bom: object
    group: str
    material: str


def build_components(P=PARAMS, short=False):
    """Option A as {key: Comp} with one fused-by-key shape per legacy component (for drawings and pictures)."""
    parts = components("A", short)
    names, bom, grp, mat = {}, {}, {}, {}
    for p in parts:
        names.setdefault(p["key"], p["name"])
        bom.setdefault(p["key"], p["bom"])
        grp.setdefault(p["key"], p["group"])
        mat.setdefault(p["key"], p["material_name"])
    return {k: Comp(names[k], sh, bom[k], grp[k], mat[k]) for k, sh in by_key(parts).items()}


def legacy_parts(P=PARAMS):
    """Option A as four groups, each {key: Compound} in its own frame (capstan about its drum axis, box 1 at the origin,
    tail block and ramp as built): what the building-plan pictures draw."""
    cap = by_key(_cached("cap", capstan, P))
    box = by_key(U.box_unit(P, "", True, True))
    tail = by_key(U.tail_unit(P, True))
    ramp = by_key(U.ramp_unit(P, True))
    return cap, box, tail, ramp


def masses(P=PARAMS):
    """Mass in kg of option A by legacy component key (model volume times material density; rope and sling left out)."""
    m = {}
    for p in components("A", True):
        if p["key"] in ("ropes", "sling"):
            continue
        m[p["key"]] = m.get(p["key"], 0.0) + cp.mass_kg(p)
    return m


def _dims(shape):
    bb = shape.bounding_box()
    return tuple(sorted((bb.size.X, bb.size.Y, bb.size.Z), reverse=True))


def pack_pieces(P=PARAMS):
    """The kit as carried: (name, sorted bounding box dims mm, kg) for each piece, largest first (SLH-DDR-003)."""
    parts = components("A", True)
    byname = {p["name"]: p for p in parts}
    kg = cp.mass_kg
    out = []

    def add(name, shapes, mass, dims=None):
        sh = Compound([s for x in shapes for s in x.solids()])
        out.append((name, dims or _dims(sh), mass))
    for nm, lab in (("Side frame -Y (chain side)", "Side frame, -Y (chain side)"), ("Side frame +Y (pawl side)", "Side frame, +Y (pawl side)")):
        add(lab, [byname[nm]["shape"]], kg(byname[nm]))
    for nm, lab in (("Front cross rail", "Front or rear cross rail"), ("Rear cross rail", "Front or rear cross rail"),
                    ("Anchor bar with eye", "Anchor bar with eye"), ("Top tie", "Top tie")):
        wn = f"Welds, {nm.lower()} (end plates)"
        add(lab, [byname[nm]["shape"]], kg(byname[nm]) + kg(byname[wn]))
    drum_keys = [p for p in parts if p["key"] in ("drum", "drum_bearings") and p["kind"] != "fastener"]
    add("Drum with its bearings", [p["shape"] for p in drum_keys], sum(kg(p) for p in drum_keys))
    for n in ("1", "2"):
        b = byname[f"Scraper box {n}"]
        add("Scraper box (bridles off)", [b["shape"]], kg(b) + kg(byname[f"Welds, scraper box {n}"]))
    tail = [p for p in parts if p["key"] in ("tail_plate", "tail_spacers", "sheaves", "keeper", "anchors")]
    add("Tail block", [p["shape"] for p in tail], sum(kg(p) for p in tail))
    ch = byname["Ramp cheeks (2) 18 mm plywood"]
    d1 = _dims(ch["shape"] & bx(-1000, 1000, 0, 1000, -10, 1000))
    out.append(("Ramp cheeks (2), stacked", (d1[0], d1[1], 2 * d1[2]), kg(ch)))
    dk = byname["Ramp deck trays (2) 3 mm"]
    d2 = _dims(dk["shape"] & bx(0, 1000, -1000, 1000, -10, 1000))
    out.append(("Ramp deck trays (2), nested", (d2[0], d2[1], d2[2] + 30.0), kg(dk)))
    rl = [byname[n] for n in ("Crest roller 60.3 x 3.6", "Roller axle 20 mm", "Roller end bushes (2)")]
    add("Crest roller on its axle", [p["shape"] for p in rl], sum(kg(p) for p in rl))
    out.sort(key=lambda q: -q[1][0] * q[1][1])
    return out


def side_frame_masses(P=PARAMS):
    byname = {p["name"]: p for p in _cached("cap", capstan, P)}
    return {"m": cp.mass_kg(byname["Side frame -Y (chain side)"]), "p": cp.mass_kg(byname["Side frame +Y (pawl side)"])}


# ----------------------------------------------------------------------------- constructability checks beyond the kit's
def _dist(a, b):
    try:
        return a.distance_to(b)
    except Exception:
        return float("nan")


def checks(P=PARAMS, verbose=True):
    """Two boxes pass each other in the room and cross the ramp inside its cheeks (SLH-DDR-003)."""
    res = {}
    bu = [p for p in U.box_unit(P, "", True, False) if p["key"] in ("box", "bridles")]
    b1 = Compound([s for p in bu for s in p["shape"].solids()])
    b2 = Pos(0, P["ret_y"], 0) * b1
    res["pass_gap"] = _dist(b1, b2)
    wi = P["ramp"][1] / 2
    bb = b1.bounding_box()
    lo, hi = bb.min.Y - (ramp_y(P) - 0.0), bb.max.Y - ramp_y(P)
    res["ramp_gap"] = [min(lo + wi, wi - hi), min(lo + P["ret_y"] + wi, wi - (hi + P["ret_y"]))]
    if verbose:
        print(f"boxes pass {res['pass_gap']:.1f} mm apart; least gap to a ramp cheek {min(res['ramp_gap']):.1f} mm")
    return res


def export_stl(P=PARAMS):
    """STL of the chosen design by group, 0.2 mm chord tolerance."""
    root = HERE.parents[1]
    (root / "cad" / "stl").mkdir(parents=True, exist_ok=True)
    parts = components(CHOSEN, True)
    groups = {"capstan": lambda p: p["group"] == "shell",
              "box": lambda p: p["key"] in ("box", "bridles", "box_2", "bridles_2", "tip_bar"),
              "tail": lambda p: p["key"] in ("tail_plate", "tail_spacers", "sheaves", "keeper", "anchors"),
              "ramp": lambda p: p["key"] in ("cheeks", "decks", "roller", "axle")}
    for g, f in groups.items():
        sel = [s for p in parts if f(p) for s in p["shape"].solids()]
        from build123d import export_stl as ex
        ex(Compound(sel), str(root / "cad" / "stl" / f"silthaul-{g}.stl"), tolerance=0.2, angular_tolerance=0.3)
    print("exported STL to cad/stl")


if __name__ == "__main__":
    D = derived()
    checks()
    for k, v in sorted(masses().items()):
        print(f"{k:16s} {v:6.2f} kg")
    if "--check" not in sys.argv:
        export_stl()
