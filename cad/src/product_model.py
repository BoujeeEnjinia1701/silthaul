"""SiltHaul product appearance model (build123d), TRL 3, kit 1.9 (STANDARDS sections 12 and 24).

Every product part is components(CHOSEN) from cad/src/model.py as it is, in the shortened picture layout (tail
sheave, box, doorway ramp and capstan closer together than on site): all 245 parts, every bolt, weld bead, pin,
bearing, chain roller and rope. Only the site is added, as context parts: a wall with a doorway and a threshold,
a tree as the anchor, both reaching below ground, and a 1.75 m mannequin standing on the ground at the crank.
Appearance additions not in model.py, recorded in docs/REVIEW.md: rope wound on both drum halves.
The hero is rendered by .kit/photoreal.py as an outdoor scene on wet mud, ground level at model z = 0.
APPEARANCE MODEL ONLY. CONCEPT, NOT FOR FABRICATION.

Groups: "shell" (the hand capstan), "internal" (boxes, tail block, ramp, ropes, sling), "context" (site, mannequin).

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from build123d import Pos  # noqa: E402
import model as M  # noqa: E402
from model import PARAMS as P, derived, context_shapes, ytube  # noqa: E402
from cad_parts import part  # noqa: E402

TITLE = "SiltHaul: hand-capstan scraper that drags flood mud out of homes"

_SITE = ["--scene=outdoor", "--ground=mud", "--ground-z=0", "--water=-8", "--sun=38,-75", "--lens=50"]
RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 22, "az": -40, "args": _SITE,
     "note": "Site render from the front right and above (about 22 deg elevation), layout shortened, on wet mud outside a "
             "flooded house: the hand capstan with a 1.75 m person standing on the ground at the crank, the sling to a tree, "
             "the second scraper box at the dump, the doorway ramp, and the first box and tail sheave block inside the door"},
    {"name": "studio", "groups": ["shell"], "explode": False, "el": 24, "az": -48,
     "note": "Studio render of the hand capstan from the front right and above (about 24 deg elevation): bolted side frames "
             "and cross members, rope on the winding drum, ratchet wheels and pawls, 4:1 chain drive in its guard, cranks"},
    {"name": "exploded", "groups": ["shell"], "explode": True, "el": 26, "az": -50,
     "note": "Exploded hand capstan from the front right and above (about 26 deg elevation): side frames and bolted "
             "cross members, winding drum with ratchet wheels, bearings, crank shaft, sprockets and chain, chain guard, cranks and pawls"},
    {"name": "detail", "groups": ["internal"], "explode": False, "el": 28, "az": -35,
     "note": "Detail from the front right and above (about 28 deg elevation): the two scraper boxes with their "
             "bridles and tipping bar, tail sheave block, and the doorway ramp with its crest roller"},
]


def product_parts(P=P):
    D = derived(P)
    out = [dict(p) for p in M.components(M.CHOSEN, True) if p["kind"] != "context"]
    # rope wound on the drum: the pull half nearly empty (box 1 at the far end), the return half full (box 2 at the dump)
    L = P["short"]
    xd, yc, hd = L["x_cap"], P["cap_y"], P["hd"]
    r0, r1 = P["drum_tube"][0] / 2, P["drum_tube"][0] / 2 + P["rope_d"]
    h = D["half_len"]
    y_ret0 = yc + P["ring"][1] / 2
    y_pull1 = yc - P["ring"][1] / 2
    wound = (ytube(xd, hd, r1, r0, y_pull1 - 4 * P["pitch"], y_pull1)
             + ytube(xd, hd, r1, r0, y_ret0, y_ret0 + h * 0.85))
    out.append(part("Rope wound on the drum", wound, "rope", kind="bought", group="shell", explode=(0, 0, 700)))
    # context
    X = context_shapes(P, short=True)
    out.append(part("Wall, doorway and threshold (site)", X["wall"] + X["threshold"], "concrete", kind="context", group="context"))
    out.append(part("Tree used as the anchor (site)", X["tree"], "timber", kind="context", group="context"))
    from context_parts import mannequin
    person = Pos(xd + P["xc"], yc + 900.0, 0) * mannequin(1750, "stand")
    out.append(part("Person, 1.75 m (scale)", person, "skin", kind="context", group="context"))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:44s} {p['group']:9s} {p['material']:18s} vol={s.volume / 1000:9.1f} cm3")
