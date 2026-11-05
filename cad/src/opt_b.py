"""SiltHaul option B, crew-hauled box (SLH-OPT-001): one scraper box on a pull rope with fixed toggle handles for up
to four people, a tag line through the tail sheave block for the loaders, the threshold ramp, and two foot boards
staked to the ground. No machine and no overload limit: the crew's own pull is the only force."""
from __future__ import annotations

from build123d import Compound, Cylinder, Pos, Rot

import slh_units as U
from slh_parts import bx, xcyl, zcyl, be, mk, cp, fuse


def _place(parts, loc):
    return [dict(p, shape=loc * p["shape"]) for p in parts]


def _grip_z(x, y, z):
    """Toggle grip, rope entering from below: HDPE tube 40 x 220 along Y with a rope hole through its lower wall."""
    ln = 220.0
    tube = Pos(x, y - ln / 2, z) * Rot(-90, 0, 0) * cp.round_tube(40.0, 8.0, ln)
    return be(tube - zcyl(x, y, 5.6, z - 21, z - 10), 1.5)


def _grip_x(x, y, z):
    """Toggle grip, rope entering from the -X side."""
    ln = 220.0
    tube = Pos(x, y - ln / 2, z) * Rot(-90, 0, 0) * cp.round_tube(40.0, 8.0, ln)
    return be(tube - xcyl(y, z, 5.6, x - 21, x - 10), 1.5)


def option_b(P, L, D, ends):
    H = P["haul"]
    rr = P["rope_d"] / 2
    zr = 75.0
    parts = []
    parts += _place(U.box_unit(P, "", bom=False, with_bar=True), Pos(L["box_x0"], 0, 0))
    parts += U.tail_unit(P, bom=False)
    parts += _place(U.ramp_unit(P, bom=False), Pos(L["x_door"], P["ret_y"] / 2, 0))
    xh = L["x_cap"]
    xfl = xh - 2500.0                              # the pull rope lies on the floor from here to the crew
    zroll = ends["zroll"]
    pull = [(ends["front1"], 0, zr), (L["x_door"], 0, zroll), (xfl, 0, rr), (xh, 0, rr)]
    parts.append(mk("Pull rope 10 mm with eye splices", cp.rope(pull, P["rope_d"]), "rope", "bought", "ropes", None, (0, 0, 0), "internal"))
    tail = [(ends["rear1"], 0, zr)] + U.tail_arc_points(P) + [(1494.0, P["ret_y"], P["rope_z"])]
    parts.append(mk("Tag line 10 mm with eye splices", cp.rope(tail, P["rope_d"]), "rope", "bought", "ropes", None, (0, 0, 0), "internal"))
    for i in range(H["n_handles"]):
        x = xh - 500.0 - i * H["handle_pitch"]
        z0 = rr if x >= xfl else rr + (zroll - rr) * (xfl - x) / (xfl - L["x_door"])
        parts.append(mk(f"Pull toggle grip {i + 1}", _grip_z(x, 0.0, 700.0), "hdpe_black", "made", "grips", None, (0, 0, 0), "internal"))
        parts.append(mk(f"Pull toggle strap {i + 1}", cp.rope([(x, 0, z0 + 2 * rr + 0.2), (x, 0, 694.0)], P["rope_d"]),
                        "rope", "bought", "grips", None, (0, 0, 0), "internal"))
    parts.append(mk("Tag line toggle grip", _grip_x(1500.0, P["ret_y"], P["rope_z"]), "hdpe_black", "made", "grips", None, (0, 0, 0), "internal"))
    sd, sl, _ = P["stake"]
    for i, ysg in enumerate((-1, 1)):
        yc = ysg * 600.0
        xc0 = xh - 1800.0
        screws = [(xc0 - 590.0 + 20.0, yc - 70.0), (xc0 - 590.0 + 20.0, yc + 70.0)]
        board = Pos(xc0, yc, 0) * cp.sheet(1200.0, 200.0, 40.0, holes=[(-450.0, 0, sd + 1.0), (450.0, 0, sd + 1.0)], r_corner=6.0)
        for sx, sy in screws:
            board = board - Pos(sx, sy, 24.0) * Cylinder(4.0, 33.0)
        parts.append(mk(f"Foot board {i + 1} 40 x 200 x 1200", board, "timber", "made", "foot_boards", None, (0, 0, 0), "internal"))
        ang = cp.angle(40.0, 40.0, 4.0, 200.0)
        ang = Pos(xc0 - 590.0, yc + 100.0, 40.0) * Rot(90, 0, 0) * ang
        for sx, sy in screws:
            ang = ang - Pos(sx, sy, 42.0) * Cylinder(4.5, 6.0)
        parts.append(mk(f"Heel cleat {i + 1} angle 40 x 4", ang, "mild_steel", "made", "foot_boards", None, (0, 0, 0), "internal"))
        for k, (sx, sy) in enumerate(screws):
            parts.append(mk(f"Coach screw M8 x 36 ({i + 1}{'ab'[k]})", Pos(sx, sy, 44.0) * cp.coach_screw(8, 36), "zinc_plated", "fastener", "foot_boards", None, (0, 0, 0), "internal"))
        for k, xs in enumerate((xc0 - 450.0, xc0 + 450.0)):
            stake = cp.round_bar(sd, sl) + Pos(0, 0, sl + 3.0) * Cylinder(16.0, 6.0)
            parts.append(mk(f"Foot board stake {i + 1}{'ab'[k]}", be(Pos(xs, yc, 40.0 - sl) * stake, 0.6), "mild_steel", "made", "stakes", None, (0, 0, 0), "internal"))
    return parts
