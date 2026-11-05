"""SiltHaul option C, hand slurry pump (SLH-OPT-001): a double-acting diaphragm pump on a welded skid, worked by a
long rocker handle, sucks mud thinned with flush water through a strainer and delivers it by hose; a flush lance
fed from a 200 L drum loosens and thins the mud. Built in the pump frame (skid centre at the origin, rocker along X,
suction toward -Y, delivery toward +Y) and placed so the suction hose runs toward the door."""
from __future__ import annotations

import math

from build123d import Box, Compound, Cylinder, Location, Pos, Rot

import slh_units as U
from slh_parts import rod, bx, ycyl, xcyl, zcyl, ytube, tube_between, round_between, bolt_z, bolt_y, weld_bead, ring_weld, be, mk, cp, fuse

BASE_Z0 = 48.0                    # top of the base plate
BLOCK = (700.0, 220.0, 90.0)      # manifold block x, y, z
POT_X = 220.0                     # chamber centres at +- POT_X
Z_BLK = BASE_Z0 + BLOCK[2]        # block top = diaphragm plane
Z_P = 700.0                       # rocker pivot height
LINK = 150.0                      # pin to pin
G = "internal"
SPX = 90.0                        # x of the hose and spigot axes, clear of the rocker posts at x = 0


def _hose(points, od, t):
    segs = [round_between(a, b, od, t) for a, b in zip(points, points[1:])]
    return Compound([s for sg in segs for s in sg.solids()])


def pump_frame(P):
    out = []
    M = lambda name, shape, mat, kind, key: out.append(mk(name, shape, mat, kind, key, None, (0, 0, 0), G))  # noqa: E731
    # ---- skid: two runners, four cross members, 8 mm base plate, two rocker posts
    holes = [(0.0, -85.0, 11.0), (0.0, 85.0, 11.0)]
    sk = [tube_between((-500, sy, 20), (500, sy, 20), 40, 3) for sy in (-200.0, 200.0)]
    sk += [tube_between((cx, -180, 20), (cx, 180, 20), 40, 3) for cx in (-350.0, -170.0, 170.0, 350.0)]
    sk.append(Pos(0, 0, 40) * cp.sheet(760.0, 340.0, 8.0, holes=holes, r_corner=8.0))
    for sy in (-145.0, 145.0):
        sk.append(tube_between((0, sy, BASE_Z0), (0, sy, Z_P + 30), 40, 3))
        sk.append(ycyl(0, Z_P, 11.0, sy - 20, sy + 20))              # crush sleeve for the pivot bolt
    skid = fuse(sk)
    for sy in (-145.0, 145.0):
        skid = skid - ycyl(0, Z_P, 8.75, sy - 21, sy + 21)
    M("Pump skid with base plate and rocker posts", skid, "painted_steel", "made", "skid")
    wl = []
    for sy in (-145.0, 145.0):
        for ex in (-1, 1):
            wl.append(weld_bead((ex * 20, sy - 20, BASE_Z0), (ex * 20, sy + 20, BASE_Z0), (ex, 0, 0), (0, 0, 1), 3.0))
    M("Welds, rocker posts to base plate", Compound(wl), "mild_steel", "weld", "skid")
    # ---- manifold block (HDPE): dish under each diaphragm, valve pockets, blind bolt holes, base bolt holes
    block = bx(-BLOCK[0] / 2, BLOCK[0] / 2, -BLOCK[1] / 2, BLOCK[1] / 2, BASE_Z0, Z_BLK)
    for hx, hy, _ in holes:
        block = block - zcyl(hx, hy, 5.5, BASE_Z0 - 1, Z_BLK + 1)
    for sg in (-1, 1):
        cx = sg * POT_X
        block = block - zcyl(cx, 0, 135.0, Z_BLK - 25.0, Z_BLK + 1)
        for vy in (-60.0, 60.0):
            block = block - zcyl(cx, vy, 32.0, Z_BLK - 33.0, Z_BLK - 24.0)
        for k in range(6):
            a = math.radians(60 * k + 30)
            block = block - zcyl(cx + 150 * math.cos(a), 150 * math.sin(a), 5.0, Z_BLK - 34.0, Z_BLK + 1)
    M("Manifold block 700 x 220 x 90 (HDPE)", be(block, 1.5), "hdpe_recycled", "made", "pump_body")
    zs = BASE_Z0 + 45.0
    M("Suction spigot 75 mm (butt fused)", be(Pos(SPX, -BLOCK[1] / 2, zs) * Rot(90, 0, 0) * cp.round_tube(75.0, 6.0, 160.0), 0.5), "hdpe_recycled", "made", "pump_body")
    M("Delivery spigot 75 mm (butt fused)", be(Pos(SPX, BLOCK[1] / 2, zs) * Rot(-90, 0, 0) * cp.round_tube(75.0, 6.0, 160.0), 0.5), "hdpe_recycled", "made", "pump_body")
    for hx, hy, _ in holes:     # M10 x 120, head on the block, nut under the plate between the skid tubes
        for n_, sh in bolt_z(10, BLOCK[2] + 8.0, hx, hy, Z_BLK, -1, L=120):
            M(n_ + " (base)", sh, "zinc_plated", "fastener", "pump_body")
    # ---- two chambers
    z_rt = Z_P - LINK                          # rod pin height
    for sg, nm in ((-1, "left"), (1, "right")):
        cx = sg * POT_X
        zd = Z_BLK
        dia = zcyl(cx, 0, 165.0, zd, zd + 3.0) - zcyl(cx, 0, 8.2, zd - 1, zd + 4)
        for k in range(6):
            a = math.radians(60 * k + 30)
            dia = dia - zcyl(cx + 150 * math.cos(a), 150 * math.sin(a), 5.5, zd - 1, zd + 4)
        M(f"Diaphragm {nm} (EPDM)", dia, "epdm", "bought", "pump_body")
        zc0 = zd + 3.0
        # cavity 49 mm deep above the diaphragm plane: the stroke is +-20 mm (SLH-STM-001 S20), 25 mm dish below
        cover = zcyl(cx, 0, 165.0, zc0, zc0 + 25.0) + zcyl(cx, 0, 135.0, zc0 + 25.0, zc0 + 50.0) + zcyl(cx, 0, 30.0, zc0 + 50.0, zc0 + 80.0)
        cover = cover - zcyl(cx, 0, 125.0, zc0 - 1, zc0 + 49.0) - zcyl(cx, 0, 11.0, zc0 + 48.0, zc0 + 81.0)
        for k in range(6):
            a = math.radians(60 * k + 30)
            cover = cover - zcyl(cx + 150 * math.cos(a), 150 * math.sin(a), 5.5, zc0 - 1, zc0 + 26.0)
        M(f"Pump cover {nm} (HDPE)", be(cover, 1.5), "hdpe_recycled", "made", "pump_body")
        bs = []
        for k in range(6):
            a = math.radians(60 * k + 30)
            hx, hy = cx + 150 * math.cos(a), 150 * math.sin(a)
            bs.append(Pos(hx, hy, zc0 + 25.0) * cp.washer(10))
            bs.append(Pos(hx, hy, zc0 + 25.0 + cp.ISO[10][4]) * cp.hex_bolt(10, 60))
        M(f"Cover bolts M10 x 60 with washers, {nm} (6)", Compound([s for b in bs for s in b.solids()]), "zinc_plated", "fastener", "pump_body")
        lo = zcyl(cx, 0, 60.0, zd - 8.0, zd) - zcyl(cx, 0, 8.0, zd - 9, zd + 1)
        up = zcyl(cx, 0, 60.0, zd + 3.0, zd + 11.0) - zcyl(cx, 0, 8.0, zd + 2, zd + 12)
        M(f"Diaphragm clamp discs {nm} (2)", Compound([be(lo, 0.8), be(up, 0.8)]), "mild_steel", "made", "pump_body")
        rod_bot = zd - 8.0 - cp.ISO[16][2] + 2.0
        prod = Pos(cx, 0, rod_bot) * cp.round_bar(16.0, z_rt + 25.0 - rod_bot)
        prod = prod - Pos(cx, 0, z_rt) * Rot(90, 0, 0) * Cylinder(5.2, 30.0)
        M(f"Pump rod 16 mm {nm}", prod, "mild_steel", "made", "pump_rod")
        M(f"Rod nut M16 {nm}", Pos(cx, 0, zd - 8.0 - cp.ISO[16][2]) * cp.hex_nut(16), "zinc_plated", "fastener", "pump_rod")
        M(f"Rod guide bush {nm}", Pos(cx, 0, zc0 + 65.0) * cp.bush(22.0, 16.2, 30.0), "hdpe_natural", "bought", "pump_rod")
        for vy, vn in ((-60.0, "inlet"), (60.0, "outlet")):
            M(f"Valve seat ring, {vn} {nm}", Pos(cx, vy, Z_BLK - 33.0) * cp.bush(60.0, 40.0, 4.0), "brass", "bought", "pump_valves")
            M(f"Valve flap, {vn} {nm}", be(Pos(cx, vy, Z_BLK - 29.0) * Cylinder(28.0, 4.0).moved(Location((0, 0, 2.0))), 0.5), "epdm", "bought", "pump_valves")
        lks = []
        for ys in (-11.5, 11.5):
            lk = be(Pos(cx, ys, (z_rt + Z_P) / 2) * Box(30.0, 6.0, Z_P - z_rt + 30.0), 1.0)
            lk = lk - Pos(cx, ys, z_rt) * Rot(90, 0, 0) * Cylinder(5.2, 10.0) - Pos(cx, ys, Z_P) * Rot(90, 0, 0) * Cylinder(5.2, 10.0)
            lks.append(lk)
        M(f"Link bars {nm} (2)", Compound(lks), "mild_steel", "made", "rocker")
        pins = [U.cp_pin(cx, z, -17.0, 17.0, 10.0) for z in (z_rt, Z_P)]
        sp = [cp.at(cp.split_pin(10.0), (cx, ye + (-1.5 if ye > 0 else 1.5), z), (0, 0, 90)) for z in (z_rt, Z_P) for ye in (-17.0, 17.0)]
        M(f"Pins 10 mm {nm} (2)", Compound(pins), "zinc_plated", "bought", "rocker")
        M(f"Split pins {nm} (4)", Compound(sp), "zinc_plated", "fastener", "rocker")
    # ---- rocker, handle, grip, pivot bolt and spacers
    rock = Pos(-280.0, 0, Z_P) * Rot(0, 90, 0) * cp.flat_bar(60.0, 10.0, 560.0)
    rock = rock - Pos(0, 0, Z_P) * Rot(90, 0, 0) * Cylinder(11.0, 20.0)
    for xe in (-POT_X, POT_X):
        rock = rock - Pos(xe, 0, Z_P) * Rot(90, 0, 0) * Cylinder(5.2, 20.0)
    ht = Pos(280.0, 0, Z_P) * Rot(0, 90, 0) * cp.round_tube(33.7, 3.2, 1400.0)
    gus = [bx(280.0, 380.0, ys0, ys0 + 4.0, Z_P - 27.0, Z_P + 27.0) for ys0 in (-9.0, 5.0)]
    M("Rocker arm with handle tube", be(fuse([rock, ht] + gus), 0.6), "painted_steel", "made", "rocker")
    M("Welds, handle tube to rocker", ring_weld((280.0, 0, Z_P), "x", 16.85, 3.0, 1), "mild_steel", "weld", "rocker")
    M("Handle grip (rubber)", Pos(1560.0, 0, Z_P) * Rot(0, 90, 0) * be(cp.round_tube(39.7, 3.0, 120.0), 2.0), "epdm", "bought", "rocker")
    M("Rocker pivot bush", Pos(0, -5.0, Z_P) * Rot(-90, 0, 0) * cp.bush(22.0, 16.2, 10.0), "brass", "bought", "rocker")
    for n_, sh in bolt_y(16, 330.0, 0, Z_P, -165.0, 1, L=350):
        M(n_ + " (pivot)", sh, "zinc_plated", "fastener", "rocker")
    sp = [ytube(0, Z_P, 14.0, 8.9, -125.0, -5.5), ytube(0, Z_P, 14.0, 8.9, 5.5, 125.0)]
    M("Pivot spacer tubes (2)", Compound([be(s, 0.4) for s in sp]), "mild_steel", "made", "rocker")
    # ---- suction side: hose over the spigot, strainer on the far end, band clamps
    y_far = -3700.0
    suction = [(SPX, -150.0, zs), (SPX, -420.0, zs), (SPX, -1400.0, 45.0), (SPX, y_far + 280.0, 45.0)]
    M("Suction hose 75 mm ID", _hose(suction, 90.0, 7.5), "rubber_belt", "bought", "hoses")
    cage = Pos(SPX, y_far, 45.0) * Rot(-90, 0, 0) * cp.round_tube(110.0, 3.0, 280.0)
    for k in range(10):
        for j in range(5):
            ang = math.radians(36 * k + (18 if j % 2 else 0))
            yy = y_far + 30 + 55 * j
            cage = cage - rod((SPX + 40.0 * math.cos(ang), yy, 45.0 + 40.0 * math.sin(ang)), (SPX + 65.0 * math.cos(ang), yy, 45.0 + 65.0 * math.sin(ang)), 5.0)
    plate = Pos(SPX, y_far + 280.0, 45.0) * Rot(-90, 0, 0) * (Cylinder(55.0, 4.0).moved(Location((0, 0, 2.0))) - Cylinder(31.5, 6.0))
    stub = Pos(SPX, y_far + 284.0, 45.0) * Rot(-90, 0, 0) * cp.round_tube(75.0, 6.0, 140.0)
    cap = Pos(SPX, y_far, 45.0) * Rot(-90, 0, 0) * (Cylinder(55.0, 4.0).moved(Location((0, 0, 2.0))))
    M("Strainer cage 110 mm with inlet stub", be(fuse([cage, plate, stub, cap]), 0.6), "galvanised", "made", "hoses")
    # ---- delivery hose
    deliv = [(SPX, 150.0, zs), (SPX, 420.0, zs), (SPX, 1400.0, 45.0), (SPX, 4200.0, 45.0)]
    M("Delivery hose 75 mm ID", _hose(deliv, 90.0, 7.5), "rubber_belt", "bought", "hoses")
    cl = []
    for yc_, zc_ in ((-185.0, zs), (185.0, zs), (y_far + 330.0, 45.0)):
        cl.append(Pos(SPX, yc_ - 6.0, zc_) * Rot(-90, 0, 0) * cp.round_tube(100.0, 5.0, 12.0))
    M("Hose clamps (3)", Compound(cl), "stainless", "bought", "hoses")
    # ---- flush water: 200 L drum on timber battens, tap, 25 mm hose, lance
    dx = -800.0
    for yy in (-150.0, 150.0):
        M(f"Drum batten {'front' if yy < 0 else 'rear'} 100 x 100", be(bx(dx - 250, dx + 250, yy - 50, yy + 50, 0, 100), 2.0), "timber", "made", "flush")
    M("Water drum 200 L", Pos(dx, 0, 100.0) * _drum(), "painted_steel", "bought", "flush")
    tap = [Pos(dx, -292.5 - 20.0, 160.0) * Rot(90, 0, 0) * Cylinder(18.0, 40.0),
           Pos(dx, -292.5 - 55.0, 160.0) * Rot(90, 0, 0) * Cylinder(9.0, 30.0)]
    M("Drum tap (ball valve)", Compound(tap), "brass", "bought", "flush")
    fh = [(dx, -292.5 - 70.0, 160.0), (dx, -420.0, 160.0), (dx, -700.0, 16.5), (dx, -3300.0, 16.5)]
    M("Flush hose 25 mm", _hose(fh, 33.0, 4.0), "rubber_belt", "bought", "flush")
    M("Flush lance 26.9 x 2.6", round_between((dx, -3302.0, 16.5), (dx, -4300.0, 16.5), 26.9, 2.6), "galvanised", "made", "flush")
    M("Lance grip (rubber)", Pos(dx, -3500.0, 16.5) * Rot(-90, 0, 0) * be(cp.round_tube(32.9, 3.0, 140.0), 1.5), "epdm", "bought", "flush")
    nozzle = Cylinder(13.45, 30.0).moved(Location((0, 0, 15.0))) - Cylinder(4.0, 32.0).moved(Location((0, 0, 16.0)))
    M("Lance nozzle (brass)", Pos(dx, -4300.0, 16.5) * Rot(90, 0, 0) * be(nozzle, 1.0), "brass", "bought", "flush")
    return out


def _drum():
    """200 L steel drum with a 1.2 mm shell: the kit's hoops, chimes and bung round a hollow shell."""
    solids = cp.drum_200l().solids()
    r, h = 292.5, 880.0
    shell = cp.round_tube(2 * r, 1.2, h) + Cylinder(r, 1.2).moved(Location((0, 0, 0.6))) + Cylinder(r, 1.2).moved(Location((0, 0, h - 0.6)))
    return Compound([shell] + list(solids[1:]))
