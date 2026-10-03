"""SiltHaul product appearance model (build123d), TRL 3, constructable design (SLH-DDR-002, SLH-DDR-003).

For photoreal renders only (.kit/export_views.py, then .kit/photoreal.py on Amish's Mac). Every
part is the model.py solid itself, placed in the shortened picture layout of model.py (tail
sheave, box, doorway ramp and capstan closer together than on site); colours and materials are
added for the look. Appearance additions not in model.py, recorded in docs/REVIEW.md: rope wound
on both drum halves, the above-ground part of the stakes only, and the context (a wall with a
doorway, a tree as the anchor, and a posed 1.75 m mannequin at the crank). CONCEPT, NOT FOR FABRICATION.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from build123d import Pos  # noqa: E402
from model import PARAMS as P, derived, build_components, context_shapes, bx, ytube  # noqa: E402

TITLE = "SiltHaul: hand-capstan scraper that drags flood mud out of homes"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 22, "az": -40,
     "note": "Product render from the front right and above (about 22 deg elevation); layout shortened. One scraper "
             "box and the tail sheaves inside the doorway, threshold ramp in the door, the second box outside at the "
             "dump, flat-pack hand capstan with a person at the crank, sling to a tree"},
    {"name": "exploded", "groups": ["shell"], "explode": True, "el": 26, "az": -50,
     "note": "Exploded hand capstan from the front right and above (about 26 deg elevation): side frames and bolted "
             "cross members, winding drum with ratchet wheels, bearings, crank shaft, sprockets and chain, chain guard, cranks and pawls"},
    {"name": "detail", "groups": ["internal"], "explode": False, "el": 28, "az": -35,
     "note": "Detail from the front right and above (about 28 deg elevation): the two scraper boxes with their "
             "bridles and tipping bar, tail sheave block, and the doorway ramp with its crest roller"},
]

LOOK = {  # key: (colour, material, group, exploded offset)
    "frame": ("#0F766E", "painted steel", "shell", (0, 0, 0)),
    "cross_members": ("#14B8A6", "painted steel", "shell", (0, 0, 250)),
    "frame_bolts": ("#9CA3AF", "zinc plated steel", "shell", (0, 0, 250)),
    "drum": ("#C2410C", "painted steel", "shell", (0, 0, 700)),
    "drum_bearings": ("#374151", "cast iron", "shell", (0, 0, 400)),
    "crank_bearings": ("#374151", "cast iron", "shell", (0, 0, 1350)),
    "crank_shaft": ("#9CA3AF", "bright steel", "shell", (0, 0, 1550)),
    "small_sprocket": ("#6B7280", "steel", "shell", (0, -350, 1550)),
    "shear_pin": ("#DC2626", "steel", "shell", (0, -350, 1650)),
    "chain": ("#4B5563", "steel", "shell", (0, -600, 900)),
    "guard": ("#FACC15", "painted steel", "shell", (0, -900, 900)),
    "cranks": ("#111827", "painted steel", "shell", (0, 0, 1850)),
    "pawls": ("#1D4ED8", "painted steel", "shell", (0, 450, 700)),
    "stakes": ("#57534E", "steel", "shell", (0, 0, 0)),
    "sling": ("#F97316", "polyester webbing", "internal", (0, 0, 0)),
    "tail_plate": ("#0E7490", "painted steel", "internal", (0, 0, 0)),
    "tail_spacers": ("#64748B", "steel", "internal", (0, 0, 0)),
    "sheaves": ("#D4A017", "zinc plated steel", "internal", (0, 0, 0)),
    "keeper": ("#155E75", "painted steel", "internal", (0, 0, 0)),
    "anchors": ("#9CA3AF", "zinc plated steel", "internal", (0, 0, 0)),
    "ropes": ("#E11D48", "polyester rope", "internal", (0, 0, 0)),
    "box": ("#2563EB", "painted steel", "internal", (0, 0, 0)),
    "box_2": ("#2563EB", "painted steel", "internal", (0, 0, 0)),
    "bridles_2": ("#475569", "galvanised steel", "internal", (0, 0, 0)),
    "tip_bar": ("#1E3A8A", "painted steel", "internal", (0, 0, 0)),
    "bridles": ("#475569", "galvanised steel", "internal", (0, 0, 0)),
    "cheeks": ("#A16207", "plywood", "internal", (0, 0, 0)),
    "decks": ("#9CA3AF", "galvanised steel", "internal", (0, 0, 0)),
    "roller": ("#15803D", "painted steel", "internal", (0, 0, 0)),
    "axle": ("#374151", "steel", "internal", (0, 0, 0)),
}


def product_parts(P=P):
    D = derived(P)
    C = build_components(P, short=True)
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    for k, c in C.items():
        color, mat, grp, ex = LOOK[k]
        shape = c.shape
        if k == "stakes":
            shape = shape & bx(0, 20000, -3000, 3000, 0, 400)
        add(c.name, shape, color, mat, c.bom, grp, ex)
    # rope wound on the drum: the pull half nearly empty (box 1 at the far end), the return half full (box 2 at the dump)
    L = P["short"]
    xd, yc, hd = L["x_cap"], P["cap_y"], P["hd"]
    r0, r1 = P["drum_tube"][0] / 2, P["drum_tube"][0] / 2 + P["rope_d"]
    h = D["half_len"]
    y_ret0 = yc + P["ring"][1] / 2
    y_pull1 = yc - P["ring"][1] / 2
    wound = (ytube(xd, hd, r1, r0, y_pull1 - 4 * P["pitch"], y_pull1)
             + ytube(xd, hd, r1, r0, y_ret0, y_ret0 + h * 0.85))
    add("Rope wound on the drum", wound, "#E11D48", "polyester rope", 16, "shell", (0, 0, 700))
    # context
    X = context_shapes(P, short=True)
    add("Wall, doorway and threshold (site)", X["wall"] + X["threshold"], "#D6D3D1", "plaster", None, "context", (0, 0, 0))
    add("Tree used as the anchor (site)", X["tree"], "#78716C", "bark", None, "context", (0, 0, 0))
    from context_parts import mannequin
    person = Pos(xd + P["xc"], yc + 900.0, 0) * mannequin(1750, "stand")
    add("Person, 1.75 m (scale)", person, "#D1D5DB", "clay", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:44s} {p['group']:9s} {p['material']:18s} vol={s.volume / 1000:9.1f} cm3")
