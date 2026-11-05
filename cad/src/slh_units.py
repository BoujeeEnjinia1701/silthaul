"""SiltHaul units shared by the options: scraper box with bridles and tipping bar, tail sheave block, doorway
ramp, ropes and sling. Each returns a list of cad_parts.part() dicts (with a `key`) in the unit's own frame;
model.py places them. Millimetres.
"""
from __future__ import annotations

import math

from build123d import Box, Compound, Cylinder, Plane, Pos, Rot, Torus, mirror

from slh_parts import (bx, ycyl, xcyl, zcyl, ytube, prism_xz, rod, fuse, tube_between, weld_bead, ring_weld,
                       bolt_y, bolt_z, bow_shackle, pear_ring, be, mk, round_between, cp, hull2d, circle_pts)


# ----------------------------------------------------------------------------- scraper box
def box_unit(P, suffix="", bom=True, with_bar=False, group="internal", explode=(0, 0, 0)):
    """Box with rear at x = 0, open front toward +X, centred on y = 0. suffix is "" for box 1, "_2" for box 2."""
    W, Lb, H, t = P["box"]
    sk_t, sk_h, sk_y = P["skid"]
    br = P["back_run"]
    wy = W / 2
    z_f = sk_h
    out = []
    n = "2" if suffix else "1"
    parts = []
    for sg in (-1, 1):
        parts.append(prism_xz([(br - 20 + sk_h, 0), (Lb, 0), (Lb, sk_h), (br - 20, sk_h)], sg * sk_y - sk_t / 2, sg * sk_y + sk_t / 2))
    parts.append(bx(br, Lb, -wy, wy, z_f, z_f + t))
    parts.append(prism_xz([(br - 2, z_f), (br, z_f), (2, z_f + H), (0, z_f + H)], -wy, wy))
    for sg in (-1, 1):
        y0 = wy if sg > 0 else -wy - t
        parts.append(prism_xz([(br - 2, z_f), (Lb, z_f), (Lb, z_f + H), (0, z_f + H)], y0, y0 + t))
    parts.append(prism_xz([(Lb, z_f + t), (Lb, z_f - 7), (Lb + 50, 0), (Lb + 60, 0), (Lb + 60, 2.5), (Lb + 8, z_f + t)], -wy - t, wy + t))
    lt = P["lug_t"]
    xr_ = P["lug_rear_x"]
    for sg in (-1, 1):
        y0 = wy + t if sg > 0 else -wy - t - lt
        parts.append(be(prism_xz([(Lb - 60, 40), (Lb + 40, 40), (Lb + 40, 110), (Lb - 60, 110)], y0, y0 + lt)
                        - ycyl(Lb + 10, 75, 9.5, y0 - 1, y0 + lt + 1), 1.0))
        parts.append(be(prism_xz([(xr_ - 30, 40), (xr_ + 85, 40), (xr_ + 85, 110), (xr_ - 30, 110)], y0, y0 + lt)
                        - ycyl(xr_, 75, 9.5, y0 - 1, y0 + lt + 1), 1.0))
    so, st, sl = P["socket"]
    zb = z_f + H - P["socket_drop"]
    xb = br * (z_f + H - zb) / H - 2 + 1.0
    dv = (-math.sqrt(0.5), 0, math.sqrt(0.5))
    a = (xb + 12.0, 0, zb - 12.0)
    b = (a[0] + dv[0] * sl, 0, a[2] + dv[2] * sl)
    sock = rod(a, b, so / 2) - rod((a[0] - dv[0] * 5, 0, a[2] - dv[2] * 5), (b[0] + dv[0], 0, b[2] + dv[2]), so / 2 - st)
    sock = sock - prism_xz([(br - 2, z_f), (Lb, z_f), (Lb, z_f + H + 50), (2, z_f + H + 50), (2, z_f + H)], -wy, wy)
    parts.append(sock)
    out.append(mk(f"Scraper box {n}", fuse(parts), "painted_steel", "made", "box" + suffix, 17 if bom else None, explode, group))
    wl = []
    for sg in (-1, 1):
        wl.append(weld_bead((br + 5, sg * wy, z_f + t), (Lb - 5, sg * wy, z_f + t), (0, -sg, 0), (0, 0, 1), 3.0))
        for xl0, xl1 in ((Lb - 60, Lb + 40), (xr_ - 30, xr_ + 85)):
            ys = sg * (wy + t)
            wl.append(weld_bead((xl0, ys, 110), (xl1, ys, 110), (0, 0, 1), (0, sg, 0), 3.0))
    wl.append(weld_bead((Lb + 8, -wy, z_f + t), (Lb + 8, wy, z_f + t), (0, 0, 1), (-1, 0, 0), 3.0))
    out.append(mk(f"Welds, scraper box {n}", Compound(wl), "mild_steel", "weld", "box" + suffix, None, explode, group))
    # bridles: a pin through each lug hole with a bow shackle on it, chain legs to a pear ring at each end
    fr, rr = P["bridle_reach"]
    zr = 75.0
    pins, bows, legs, rings, splits = [], [], [], [], []
    for (xl, xr, sgx) in ((Lb + 10, Lb + fr, 1), (xr_, -rr, -1)):
        for sg in (-1, 1):
            yc = sg * (wy + t + lt / 2)
            pins.append(cp_pin(xl, zr, yc - 17, yc + 17))
            bw = bow_shackle(22.0, 50.0, 10.0)
            if sgx < 0:
                bw = Rot(0, 0, 180) * bw
            bows.append(Pos(xl, yc, zr) * bw)
            tip = xl + sgx * 50.0
            end = (xr - sgx * 4.0 if sgx > 0 else xr + 4.0, sg * 4.5, zr)
            legs.append(cp.rope([(tip + sgx * 6.0, yc, zr), (end[0] - sgx * 8.0, end[1], zr), end], 8.0))
            for ye in (yc - 17, yc + 17):
                splits.append(cp.at(cp.split_pin(19.0), (xl, ye + (1.5 if ye < yc else -1.5), zr), (0, 0, 90)))
        rings.append(Pos(xr + sgx * 28, 0, zr) * pear_ring(56.0, 8.0))
    k = "bridles" + suffix
    bm = 20 if bom else None
    out.append(mk(f"Shackle pins 19 mm, box {n}", Compound(pins), "zinc_plated", "bought", k, bm, explode, group))
    out.append(mk(f"Bow shackles, box {n}", Compound(bows), "galvanised", "bought", k, bm, explode, group))
    out.append(mk(f"Chain legs 8 mm, box {n}", Compound(legs), "galvanised", "bought", k, bm, explode, group))
    out.append(mk(f"Pear rings 56 mm, box {n}", Compound(rings), "galvanised", "bought", k, bm, explode, group))
    out.append(mk(f"Split pins, box {n}", Compound(splits), "zinc_plated", "fastener", k, bm, explode, group))
    if with_bar:
        tb_o, tb_t, tb_l = P["tip_bar"]
        a2 = (a[0] + dv[0] * 48, 0, a[2] + dv[2] * 48)
        b2 = (a2[0] + dv[0] * tb_l, 0, a2[2] + dv[2] * tb_l)
        out.append(mk("Tipping bar 26.9 x 2.6", round_between(a2, b2, tb_o, tb_t), "painted_steel", "made", "tip_bar", 18 if bom else None, explode, group))
        out.append(mk("Tipping bar end caps (2)", Compound([_cap(a2, b2, tb_o), _cap(b2, a2, tb_o)]), "hdpe_black", "made", "tip_bar", 18 if bom else None, explode, group))
    return out


def _cap(p, q, od):
    """Plastic end cap on the tube end at p, tube running toward q."""
    from build123d import Vector, Solid
    p, q = Vector(*p), Vector(*q)
    d = (q - p).normalized()
    pl = Plane(origin=p - d * 6.0, z_dir=d)
    return be(pl * (Cylinder(od / 2 + 1.5, 6.0).moved(__import__("build123d").Location((0, 0, 3.0)))), 1.0)


def cp_pin(x, z, y0, y1, d=19.0):
    return Pos(x, y0, z) * Rot(-90, 0, 0) * cp.round_bar(d, y1 - y0)


# ----------------------------------------------------------------------------- tail sheave block
def tail_unit(P, bom=True, group="internal"):
    """Sheave A centre at (0, r), sheave B at (0, ret_y - r); floor at z = 0."""
    pl, pw, pt = P["tail_plate"]
    pd, sod, sw = P["sheave"]
    r = pd / 2
    yA, yB = r, P["ret_y"] - r
    yc = P["ret_y"] / 2
    zr = P["rope_z"]
    pin = P["tail_pin"]
    an_d, an_l = P["anchor"]
    bm = (lambda n: n) if bom else (lambda n: None)
    holes = [(-110.0, yc - 170.0), (-110.0, yc + 170.0), (110.0, yc - 170.0), (110.0, yc + 170.0)]
    plate = Pos(0, yc, 0) * cp.sheet(pl, pw, pt, holes=[(hx, hy - yc, an_d + 1.0) for hx, hy in holes], r_corner=6.0)
    z_sh0, z_sh1 = zr - sw / 2, zr + sw / 2
    zk0 = z_sh1 + 5.0
    pins = [Pos(0, y, pt) * cp.round_bar(pin, zk0 + 6 + 10 - pt) for y in (yA, yB)]
    out = []
    out.append(mk("Tail plate with two pins", fuse([plate] + pins), "painted_steel", "made", "tail_plate", bm(13), (0, 0, 0), group))
    out.append(mk("Welds, tail pins to plate", Compound([ring_weld((0, y, pt), "z", pin / 2, 4.0, 1) for y in (yA, yB)]),
                  "mild_steel", "weld", "tail_plate", None, (0, 0, 0), group))
    for i, y in enumerate((yA, yB)):
        n = "A" if i == 0 else "B"
        spacer = Pos(0, y, pt) * cp.round_tube(32.0, 3.5, z_sh0 - pt)
        out.append(mk(f"Sheave spacer tube {n}", be(spacer, 0.5), "mild_steel", "made", "tail_spacers", bm(13), (0, 0, 250), group))
        fl = 6.0
        sheave = (zcyl(0, y, sod / 2, z_sh0, z_sh0 + fl) + zcyl(0, y, r - 5.5, z_sh0 + fl - 0.1, z_sh1 - fl + 0.1)
                  + zcyl(0, y, sod / 2, z_sh1 - fl, z_sh1)) - zcyl(0, y, 15.0, z_sh0 - 1, z_sh1 + 1)
        out.append(mk(f"Rope sheave 125 mm {n}", be(sheave, 1.0), "galvanised", "bought", "sheaves", bm(14), (0, 0, 450), group))
        out.append(mk(f"Sheave bush {n}", Pos(0, y, z_sh0) * cp.bush(30.0, pin, sw), "brass", "bought", "sheaves", bm(14), (0, 0, 450), group))
    keeper = Pos(0, (yA + yB) / 2, zk0) * cp.sheet(40.0, yB - yA + 60.0, 6.0,
                                                 holes=[(0, -(yB - yA) / 2, pin + 0.5), (0, (yB - yA) / 2, pin + 0.5)], r_corner=6.0)
    out.append(mk("Keeper bar 6 mm", keeper, "painted_steel", "made", "keeper", bm(13), (0, 0, 650), group))
    sp = [cp.at(cp.split_pin(pin * 0.5), (0, y, zk0 + 6 + 4.0), (0, 0, 0)) for y in (yA, yB)]
    out.append(mk("Split pins, tail pins", Compound(sp), "zinc_plated", "fastener", "keeper", bm(13), (0, 0, 650), group))
    anchors = [cp.at(cp.anchor_bolt(12, 80 + pt), (hx, hy, pt)) for hx, hy in holes]
    out.append(mk("M12 wedge anchors (4)", Compound(anchors), "zinc_plated", "bought", "anchors", bm(15), (0, 0, 850), group))
    return out


# ----------------------------------------------------------------------------- doorway ramp
def ramp_unit(P, bom=True, group="internal"):
    """Threshold ramp centred on the threshold (x = 0) and on its own centre line (y = 0)."""
    hl, wi, hcst, dt = P["ramp"]
    ct = P["cheek_t"]
    ro, rt, rl = P["roller"]
    ax = P["axle"]
    th = P["threshold_max"]
    zt = P["cheek_top"]
    yi = wi / 2
    bm = (lambda n: n) if bom else (lambda n: None)
    out = []
    cheek_pts = [(-hl, 0), (-110, 0), (-110, th), (110, th), (110, 0), (hl, 0), (hl, 12), (150, zt), (-150, zt), (-hl, 12)]
    # M8 bolts through each deck flange and cheek: three per flange, along the flange mid line
    xe = 40.0
    xb_ = hl - dt * (hl - xe) / hcst
    bolt_pts = []
    for sg in (-1, 1):
        lo = [(sg * (xb_ - 60), 0.0), (sg * xe, hcst - dt - 30)]
        up = [(sg * xb_, 0.0), (sg * xe, hcst - dt)]
        for f in (0.15, 0.5, 0.85):
            lx, lz = lo[0][0] + f * (lo[1][0] - lo[0][0]), lo[0][1] + f * (lo[1][1] - lo[0][1])
            ux_, uz_ = up[0][0] + f * (up[1][0] - up[0][0]), up[0][1] + f * (up[1][1] - up[0][1])
            bolt_pts.append(((lx + ux_) / 2, (lz + uz_) / 2 - 2.0))
    cheeks = []
    for sg in (-1, 1):
        y0 = yi if sg > 0 else -yi - ct
        c = prism_xz(cheek_pts, y0, y0 + ct) - ycyl(0, hcst - 20, ax / 2 + 0.5, y0 - 1, y0 + ct + 1)
        for bxp, bzp in bolt_pts:
            c = c - ycyl(bxp, bzp, 4.5, y0 - 1, y0 + ct + 1)
        cheeks.append(be(c, 1.5))
    out.append(mk("Ramp cheeks (2) 18 mm plywood", Compound(cheeks), "plywood", "made", "cheeks", bm(19), (0, 0, 500), group))
    decks = []
    for sg in (-1, 1):
        top = [(sg * hl, 0), (sg * xe, hcst), (sg * xe, hcst - dt), (sg * xb_, 0)]
        tray = [prism_xz(top, -yi, yi)]
        for yy in (-yi, yi - dt):
            fl = [(sg * (xb_ - 60), 0.0), (sg * xe, hcst - dt - 30), (sg * xe, hcst - dt), (sg * xb_, 0.0)]
            tray.append(prism_xz(fl, yy, yy + dt))
        decks.append(fuse(tray))
    # holes in the flanges only (not through the deck span)
    dk = []
    for tray in decks:
        for bxp, bzp in bolt_pts:
            for yy in (-yi, yi - dt):
                tray = tray - ycyl(bxp, bzp, 4.5, yy - 1, yy + dt + 1)
        dk.append(tray)
    out.append(mk("Ramp deck trays (2) 3 mm", Compound(dk), "galvanised", "made", "decks", bm(19), (0, 0, 350), group))
    zr = hcst - 20
    roller = ytube(0, zr, ro / 2, ro / 2 - rt, -rl / 2, rl / 2)
    out.append(mk("Crest roller 60.3 x 3.6", be(roller, 0.6), "safety_yellow", "made", "roller", bm(19), (0, 0, 600), group))
    bushes = [Pos(0, -rl / 2, zr) * Rot(-90, 0, 0) * cp.bush(ro - 2 * rt, ax, 20.0),
              Pos(0, rl / 2 - 20, zr) * Rot(-90, 0, 0) * cp.bush(ro - 2 * rt, ax, 20.0)]
    out.append(mk("Roller end bushes (2)", Compound(bushes), "hdpe_natural", "bought", "roller", bm(19), (0, 0, 600), group))
    out.append(mk("Roller axle 20 mm", Pos(0, -yi - ct - 12, zr) * Rot(-90, 0, 0) * cp.round_bar(ax, 2 * (yi + ct + 12)),
                  "mild_steel", "made", "axle", bm(19), (0, 0, 800), group))
    clips = [cp.at(cp.split_pin(ax), (0, sg * (yi + ct + 6), zr), (0, 0, 90)) for sg in (-1, 1)]
    out.append(mk("Split pins, roller axle", Compound(clips), "zinc_plated", "fastener", "axle", bm(19), (0, 0, 800), group))
    # M8 x 40 bolts: head on the cheek's outer face, nut inside against the deck flange
    for bxp, bzp in bolt_pts:
        for sg in (-1, 1):
            for n_, sh in bolt_y(8, ct + dt, bxp, bzp, sg * (yi + ct), -sg, L=40):
                out.append(mk(n_, sh, "zinc_plated", "fastener", "decks", bm(19), (0, 0, 500), group))
    return out


# ----------------------------------------------------------------------------- rope paths
def tail_arc_points(P):
    """Centre line of a rope that leaves the box line at the tail block, goes round sheave A and sheave B and
    returns along the second line: from (0, 0) via the A and B arcs to (0, ret_y)."""
    r = P["sheave"][0] / 2
    ry = P["ret_y"]
    rz = P["rope_z"]
    pts = [(0.0, 0.0, rz)]
    for k in range(1, 7):                       # round sheave A from -90 to -180 degrees
        a = math.radians(-90 - 15 * k)
        pts.append((r * math.cos(a), r + r * math.sin(a), rz))
    for k in range(0, 7):                       # round sheave B from 180 to 90 degrees
        a = math.radians(180 - 15 * k)
        pts.append((r * math.cos(a), (ry - r) + r * math.sin(a), rz))
    return pts


def ring_ends(P, L):
    """x of the rope ends beside the rings of box 1 and box 2 (the rope touches the pear ring's outer side)."""
    Lb = P["box"][1]
    fr, rr_ = P["bridle_reach"]
    rr = P["rope_d"] / 2
    out = {}
    for tag, x0 in (("1", L["box_x0"]), ("2", L["box2_x0"])):
        out["front" + tag] = x0 + Lb + fr + 28 + 28 + rr
        out["rear" + tag] = x0 - rr_ - 28 - 28 - rr
    out["zroll"] = P["ramp"][2] - 20 + P["roller"][0] / 2 + rr
    return out
