"""SiltHaul concept media (TRL 3, constructable design SLH-DDR-002), generated from the parametric model.

Run from the repo root:  python cad/src/concept_media.py
Takes every component from cad/src/model.py in the shortened picture layout (tail sheave, box,
doorway ramp and capstan closer together than on site) and renders the media set with
.kit/concept.py: hero, exploded view with BOM callouts, concept blueprint, energy flow per trip,
and the web model (model.glb with viewer.html). Coloured parts carry the BOM line numbers of
bom/bom.csv; grey parts (wall and doorway, tree, person) are context only. Figures on the sheet and
in the flow diagram come from docs/04-calcs/sizing.py (SLH-CAL-001). CONCEPT, NOT FOR FABRICATION.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from build123d import Box, Pos, Compound, Color, export_gltf  # noqa: E402
import matplotlib.colors as mc  # noqa: E402
from concept import Part, render_all, human_figure  # noqa: E402
from model import PARAMS as P, build_components, context_shapes  # noqa: E402

C = build_components(P, short=True)
X = context_shapes(P, short=True)

STYLE = {  # key: (colour, exploded offset in mm)
    "frame": ("#0F766E", (0, 0, 0)),
    "cross_members": ("#14B8A6", (0, 0, 250)),
    "frame_bolts": ("#111827", (0, 0, 250)),
    "drum": ("#C2410C", (0, 0, 900)),
    "drum_bearings": ("#374151", (0, 0, 600)),
    "crank_bearings": ("#374151", (0, 0, 1500)),
    "crank_shaft": ("#6B7280", (0, 0, 1800)),
    "cranks": ("#111827", (0, 0, 2050)),
    "small_sprocket": ("#B45309", (0, -500, 1800)),
    "shear_pin": ("#DC2626", (0, -500, 1800)),
    "chain": ("#78716C", (0, -800, 1100)),
    "guard": ("#FACC15", (0, -1150, 1100)),
    "pawls": ("#1D4ED8", (0, 450, 900)),
    "stakes": ("#57534E", (0, 0, -0)),
    "sling": ("#F97316", (400, 0, 0)),
    "tail_plate": ("#0E7490", (0, 0, 0)),
    "tail_spacers": ("#64748B", (0, 0, 250)),
    "sheaves": ("#D4A017", (0, 0, 450)),
    "keeper": ("#0E7490", (0, 0, 650)),
    "anchors": ("#111827", (0, 0, 850)),
    "ropes": ("#E11D48", (0, 0, 0)),
    "box": ("#2563EB", (0, 0, 0)),
    "box_2": ("#2563EB", (0, 0, 0)),
    "bridles_2": ("#475569", (0, 0, 300)),
    "tip_bar": ("#1E3A8A", (0, 0, 500)),
    "bridles": ("#475569", (0, 0, 300)),
    "cheeks": ("#A16207", (0, 0, 0)),
    "decks": ("#9CA3AF", (0, 0, 350)),
    "roller": ("#15803D", (0, 0, 600)),
    "axle": ("#374151", (0, 0, 800)),
}
ABOVE = Pos(0, 0, 0)
parts = []
for key, comp in C.items():
    color, off = STYLE[key]
    shape = comp.shape
    if key == "stakes":                       # show only the parts above ground in the pictures
        bb = shape.bounding_box()
        shape = shape & Pos((bb.min.X + bb.max.X) / 2, (bb.min.Y + bb.max.Y) / 2, 500) * Box(bb.size.X + 10, bb.size.Y + 10, 1000)
    parts.append(Part(comp.name, shape, color, comp.bom, off))

L = P["short"]
person = human_figure(1750.0, x=L["x_cap"] + P["xc"], y=P["cap_y"] + 1000.0, z=0.0)
context = [Part("Wall, doorway and threshold (site)", X["wall"] + X["threshold"], "#D1D5DB"),
           Part("Tree used as the anchor (site)", X["tree"], "#A8A29E"), person]

flow = {"title": "energy per 11 m stroke: one full 40 L box out, the empty box back, kJ (SLH-CAL-001 estimates)", "unit": "kJ",
        "stages": [("Two people at the cranks", 11.7), ("Drum and rope", 10.7), ("Both boxes moved 11 m", 10.7),
                   ("Mud delivered to the dump", "40 L, 69 kg")],
        "losses": [(0, "Chain and bearings", 1.0), (1, "Floor friction, full box", 6.5), (2, "Lip cutting and empty box", 4.2)]}

outs = render_all(
    parts, project="SiltHaul", title="Hand-capstan mud scraper concept", dwg_no="SLH-DWG-010",
    key_figures=["Two boxes on the loop: every stroke hauls mud out",
                 "Boxes 210 mm wide, 40.3 L each; about 86 kg full",
                 "4:1 chain drive, two 250 mm cranks: 63 N each at 1.0 kN",
                 "About 17 strokes, 0.68 m3 an hour (0.51 with rest)",
                 "Flat-pack frame; heaviest lift 23.1 kg; parts USD 1,056",
                 "Layout shortened; on site up to 15 m tail to capstan"],
    scale_figure=False, context=context, cut=False, web_model=False, flow=flow)

# Web model at a coarse tessellation (a few MB), with the kit's viewer page
md = ROOT / "media"
kids = []
for p in parts:
    sh = p.shape
    sh.color = Color(*mc.to_rgb(p.color))
    sh.label = p.name
    kids.append(sh)
export_gltf(Compound(kids), str(md / "model.glb"), binary=True, linear_deflection=1.0, angular_deflection=0.35)
(md / "viewer.html").write_text("""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>SiltHaul: hand-capstan mud scraper concept</title>
<script type="module" src="https://cdn.jsdelivr.net/npm/@google/model-viewer@3/dist/model-viewer.min.js"></script>
<style>body{margin:0;font-family:system-ui,sans-serif;background:#F9FAFB}model-viewer{width:100vw;height:100vh}
.tag{position:fixed;left:12px;top:10px;font-size:12px;color:#B45309;letter-spacing:.06em}</style></head>
<body><div class="tag">CONCEPT, NOT FOR FABRICATION</div>
<model-viewer src="model.glb" poster="hero.png" alt="SiltHaul: hand-capstan mud scraper concept" camera-controls auto-rotate shadow-intensity="0.6"
  exposure="1.0" camera-orbit="-35deg 70deg auto" interaction-prompt="auto"></model-viewer></body></html>
""")
print({k: str(v) for k, v in outs.items()}, "model.glb", round((md / "model.glb").stat().st_size / 1e6, 2), "MB")
