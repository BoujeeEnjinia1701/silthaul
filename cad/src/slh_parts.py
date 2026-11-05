"""SiltHaul repo helpers for the kit 1.9 model (cad/src/model.py): plain geometry builders, weld beads,
bolted joints along Y, bow shackles and pear rings. Repo-specific; the shared parts library is .kit/cad_parts.py.
All dimensions in millimetres.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import (Box, Compound, Cylinder, Plane, Polygon, Pos, Rot, Solid, Torus, Vector, extrude,  # noqa: E402
                       mirror)
import cad_parts as cp  # noqa: E402


# ----------------------------------------------------------------------------- plain geometry
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


def rod(a, b, r):
    a, b = Vector(*a), Vector(*b)
    d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def hull2d(pts):
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


def be(shape, r=0.8):
    """Break the edges of a made part (cad_parts.break_edges), keeping the shape if that fails."""
    return cp.break_edges(shape, r)


# ----------------------------------------------------------------------------- stock along a line
def tube_between(a, b, s=40.0, w=2.0):
    """Square hollow section s x s x w (EN 10219, rounded corners) from point a to point b, sides square to Y
    (or to X for a tube along Y)."""
    a, b = Vector(*a), Vector(*b)
    d = b - a
    L = d.length
    dn = d.normalized()
    xd = (0, 1, 0) if abs(dn.Y) < 0.99 else (1, 0, 0)
    pl = Plane(origin=a, x_dir=xd, z_dir=dn)
    return pl * cp.shs(s, w, L)


def bar_between(a, b, d):
    """Round bar (chamfered ends) from a to b."""
    a, b = Vector(*a), Vector(*b)
    v = b - a
    pl = Plane(origin=a, z_dir=v.normalized())
    return pl * cp.round_bar(d, v.length)


# ----------------------------------------------------------------------------- welds
def weld_bead(a, b, n1, n2, leg=4.0):
    """Fillet weld bead from a to b with legs along n1 and n2 (unit vectors square to the line, pointing away
    from the joint corner along each face)."""
    a, b = Vector(*a), Vector(*b)
    d = b - a
    L = d.length
    dn = d.normalized()
    n1, n2 = Vector(*n1), Vector(*n2)
    pl = Plane(origin=a, x_dir=n1, z_dir=dn)
    sgn = 1.0 if pl.y_dir.dot(n2) > 0 else -1.0
    # counter-clockwise in the plane so that the extrusion runs from a toward b for either side of the joint
    prof = Polygon((0, 0), (leg, 0), (0, leg), align=None) if sgn > 0 else Polygon((0, 0), (0, -leg), (leg, 0), align=None)
    return extrude(pl * prof, L)


def ring_weld(center, axis, r, leg=4.0, face=1):
    """Fillet weld round a cylinder of radius r (axis 'x','y' or 'z') against a plate face that lies at the
    given centre; the bead grows from the plate face toward +axis if face = 1, else toward -axis."""
    dirs = {"x": (1, 0, 0), "y": (0, 1, 0), "z": (0, 0, 1)}[axis]
    dv = Vector(*dirs) * face
    pl = Plane(origin=Vector(*center), z_dir=dv)
    cone = Solid.make_cone(r + leg, r, leg, pl)
    core = Solid.make_cylinder(r - 0.01, leg + 2, Plane(origin=Vector(*center) - dv * 1.0, z_dir=dv))
    return cone - core


# ----------------------------------------------------------------------------- bolted joints
def bolt_y(d, grip, x, z, y_head, toward, L=None):
    """Bolt, two washers and nut as (name, shape) pairs, axis along Y through (x, z). The joint face under the
    head washer is at y_head; the shank runs toward +Y (toward = 1) or -Y (toward = -1). L fixes the bolt length
    to the BOM figure."""
    s, k, m, d2, h, p = cp.ISO[d]
    extra = None if L is None else (L - (grip + 2 * h + m))
    rot = (90, 0, 0) if toward > 0 else (-90, 0, 0)
    return [(n, cp.at(sh, (x, y_head, z), rot)) for n, sh in cp.hex_bolt_set(d, grip, extra)]


def bolt_z(d, grip, x, y, z_head, toward, L=None):
    """Same along Z: head side at z_head, shank toward +Z (1) or -Z (-1)."""
    s, k, m, d2, h, p = cp.ISO[d]
    extra = None if L is None else (L - (grip + 2 * h + m))
    rot = (180, 0, 0) if toward > 0 else (0, 0, 0)
    return [(n, cp.at(sh, (x, y, z_head), rot)) for n, sh in cp.hex_bolt_set(d, grip, extra)]


# ----------------------------------------------------------------------------- part constructor
def mk(name, shape, material, kind, key, bom=None, explode=(0, 0, 0), group="shell", note=""):
    """cad_parts.part() plus a `key` naming the legacy component group the calculations and drawings use."""
    if isinstance(shape, Compound):          # flatten nested compounds so volume and booleans behave
        shape = Compound(list(shape.solids()))
    p = cp.part(name, shape, material, kind=kind, bom=bom, group=group, explode=explode, note=note)
    p["key"] = key
    return p


# ----------------------------------------------------------------------------- rigging
def bow_shackle(width=22.0, length=50.0, bow_d=10.0):
    """Bow of a bow shackle with its two legs along X at y = +-width / 2 and the bow toward +X (pin axis along Y
    through the origin)."""
    r = width / 2
    pts = [(0.0, -r, 0.0), (length - r, -r, 0.0)]
    n = 14
    for k in range(1, n):
        a = -math.pi / 2 + math.pi * k / n
        pts.append((length - r + r * math.cos(a), r * math.sin(a), 0.0))
    pts += [(length - r, r, 0.0), (0.0, r, 0.0)]
    return cp.rope(pts, bow_d)


def pear_ring(od=56.0, d=8.0):
    """Pear link approximated as a ring of round bar in the XZ plane, centre at the origin."""
    return Rot(90, 0, 0) * Torus(od / 2 - d / 2, d / 2)


def chain_leg(a, b, d=8.0):
    """A leg of chain drawn as a round bar with spherical ends."""
    return cp.rope([a, b], d)


def round_between(a, b, od, t):
    """Round tube od x t from point a to point b (chamfered edges)."""
    a, b = Vector(*a), Vector(*b)
    v = b - a
    pl = Plane(origin=a, z_dir=v.normalized())
    return be(pl * cp.round_tube(od, t, v.length), 0.4)
