"""SiltHaul drawing sheets, Rev P3 (TRL 3, constructable design SLH-DDR-002, Amish's decisions SLH-DDR-003).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/SLH-DWG-001 (hand capstan, general arrangement) and SLH-DWG-002 (system
layout at the design case) as SVG, PDF and PNG from cad/src/model.py with .kit/drawing.py.
Overall sizes are dimensioned by the kit; main dimensions and interfaces are listed in the notes,
taken from PARAMS and derived(). The concept blueprint in media/ is SLH-DWG-010; the making
sketches for the build plan are SLH-DWG-101 onward (cad/src/build_plan_media.py).
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from build123d import Compound  # noqa: E402
from drawing import Sheet  # noqa: E402
from model import PARAMS as P, build_components, derived  # noqa: E402

DATE_P1 = "2026-10-03"
REVS = [("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", DATE_P1, "AC"),
        ("P2", "SLH-DDR-002: design for construction", DATE_P1, "AC"),
        ("P3", "SLH-DDR-003: flat-pack frame; second box on the return leg", DATE_P1, "AC")]


def safe_project_views(part, workdir, line_weight=0.35):
    """Front, top, right and iso views, edge by edge, so a degenerate edge is skipped."""
    from build123d import ExportSVG, LineType, Unit
    workdir = Path(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    bb = part.bounding_box()
    c = bb.center()
    d = max(bb.size.X, bb.size.Y, bb.size.Z) * 10
    setups = {"front": ((c.X, c.Y - d, c.Z), (0, 0, 1)), "top": ((c.X, c.Y, c.Z + d), (0, 1, 0)),
              "right": ((c.X + d, c.Y, c.Z), (0, 0, 1)), "iso": ((c.X + d, c.Y - d, c.Z + d * 0.8), (0, 0, 1))}
    out = {}
    for name, (origin, up) in setups.items():
        visible, hidden = part.project_to_viewport(origin, up, (c.X, c.Y, c.Z))
        ex = ExportSVG(unit=Unit.MM, line_weight=line_weight)
        ex.add_layer("Visible", line_color=0x111827)
        ex.add_layer("Hidden", line_color=0x6B7280, line_type=LineType.ISO_DASH, line_weight=line_weight / 2)
        for layer, edges in (("Visible", visible), ("Hidden", hidden if name != "iso" else [])):
            for e in edges:
                try:
                    ex.add_shape(e, layer=layer)
                except (AssertionError, ValueError, ZeroDivisionError):
                    pass
        p = workdir / f"{name}.svg"
        ex.write(str(p))
        out[name] = p
    return out


def capstan_sheet(C, D):
    keys = ["frame", "cross_members", "frame_bolts", "drum", "drum_bearings", "crank_bearings", "crank_shaft",
            "small_sprocket", "shear_pin", "chain", "guard", "cranks", "pawls"]
    fb = Compound([C[k].shape for k in ("frame", "cross_members")]).bounding_box()
    work = ROOT / "cad" / "drawings" / "_views1"
    views = safe_project_views(Compound([C[k].shape for k in keys]), work)
    s = Sheet(project="SiltHaul", title="Hand capstan: general arrangement", dwg_no="SLH-DWG-001", rev="P3",
              author="Amish Chadha", date=DATE_P1, scale=0.1, theme="technical",
              material="Steel weldments, bought bearings, sprockets and chain per bom/bom.csv. PRELIMINARY, NOT FOR FABRICATION",
              revisions=REVS)
    s.add_ortho(views)
    s.add_svg(views["iso"], 276, 32, 140, 92, label="Isometric view", sublabel="Not to scale; stakes and sling not shown")
    s.add_notes("Main dimensions and interfaces (mm)", [
        f"Frame {fb.size.X:.0f} x {fb.size.Y:.0f} x {fb.size.Z:.0f}, 40 x 40 x 2 SHS, flat-pack:",
        "two welded side frames 890 x 814 (9.2, 9.6 kg) and four bolted",
        "cross members with 8 mm end plates (8.0 kg): 8 M10, 4 M12 (21)",
        f"Drum 219.1 x 3.0 tube, {D['drum_len']:.0f} between rings; axis {P['hd']:.0f} above ground",
        f"Two halves of {D['half_len']:.0f}, {D['turns']} turns of 10 rope each at {P['pitch']:.0f} pitch",
        "Pull half underwound (rope leaves at 85 up), return half overwound (315 up)",
        f"Drum shaft 30 in UCP206 (3) at +/- {D['yb']:.0f}; crank shaft 25 in UCP205 (4)",
        f"Crank shaft {P['hc']:.0f} up, {P['xc']:.0f} behind the drum axis; cranks 250 radius (5)",
        "ISO 08B-1 chain (7), 12T on the crank shaft, 48T on the drum: 4:1",
        "4 mm S235 shear pin (10) in the small sprocket hub (6): about 2.5 kN rope",
        "Two 24-tooth ratchet wheels on the drum shaft, one pawl each (8)",
        "Closed chain guard (9) on the -Y side; anchor bar and eye 200 up at the rear",
        "Third-angle; front view from -Y; rope arrives from -X; (n) = BOM line",
    ], x=276, y=135, width=146)
    out = s.save(ROOT / "cad" / "drawings" / "SLH-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print("wrote", out)


def layout_sheet(C, D):
    keys = [k for k in C if k != "stakes"]
    work = ROOT / "cad" / "drawings" / "_views2"
    views = safe_project_views(Compound([C[k].shape for k in keys]), work, line_weight=0.25)
    s = Sheet(project="SiltHaul", title="Mud scraper system: layout at the design case", dwg_no="SLH-DWG-002", rev="P3",
              author="Amish Chadha", date=DATE_P1, scale=1 / 75, theme="technical",
              material="Layout only; parts per SLH-DWG-001 and SLH-DWG-101 to 109. PRELIMINARY, NOT FOR FABRICATION",
              revisions=REVS)
    s.add_ortho(views, names=("front", "top"))
    s.add_svg(views["iso"], 276, 32, 140, 92, label="Isometric view", sublabel="Not to scale")
    s.add_notes("Layout rules (mm)", [
        f"Tail sheave block at x = 0; door threshold at {P['x_door']:,.0f}; drum axis at {P['x_cap']:,.0f}",
        "Working length up to 15,000 tail sheave to capstan (R5)",
        "Capstan at least 6,000 from the ramp roller (fleet angle 1.4 deg or less)",
        "Each stroke hauls one full box out while the other goes back empty",
        "Box 1 on y = 0; box 2 on the return leg, y = 300; they pass 42 apart",
        "Ramp centred between the box lines; inner width 610 holds both boxes",
        "Box travel up to 12,000; tail rope 12.5 m here (6 and 9 m for shorter runs)",
        "Tail block: 4 M12 anchors in a sound slab of 100 or more (R7)",
        "Sling from the anchor eye, level or rising 10 deg at most",
        "Nobody in the rope lines or beside the sheaves while the cranks turn",
        "Third-angle; front view from -Y; X along the rope line",
    ], x=276, y=135, width=146)
    out = s.save(ROOT / "cad" / "drawings" / "SLH-DWG-002")
    shutil.rmtree(work, ignore_errors=True)
    print("wrote", out)


if __name__ == "__main__":
    C = build_components(P, short=False)
    D = derived(P)
    capstan_sheet(C, D)
    layout_sheet(C, D)
