"""Unit tests verifying geometric invariants of Walter Russell's 3D Cosmogony models."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from geometor.russell import (
    GYRO_STAGES,
    build_all_models,
    build_conical_vortex_field,
    build_cube_sphere_lattice,
    build_gyroscopic_octave_system,
    build_light_sphere_lens,
    build_periodic_elements,
    build_periodic_helix_9_octave,
    export_json,
    export_obj,
    export_svg_projection,
)
from geometor.russell.cli import main as cli_main
from geometor.russell.models3d import lens_inflection_curve, vec_dot, vec_length


def test_cube_sphere_nine_equators_and_27_zero_nodes() -> None:
    scene = build_cube_sphere_lattice(include_diagonal_planes=True)

    # Exactly 9 Equators of Zero Curvature: 3 orthogonal + 6 diagonal bisecting planes
    ortho = [p for p in scene.polygons if p.group == "ortho_planes"]
    diag = [p for p in scene.polygons if p.group == "diag_planes"]
    assert len(ortho) == 3
    assert len(diag) == 6
    assert len(scene.polygons) == 9

    # Every plane must pass through the central zero fulcrum (0, 0, 0) and stay inside [-1, 1]^3
    for poly in scene.polygons:
        assert math.isclose(vec_length(poly.normal), 1.0, rel_tol=1e-9)
        for v in poly.vertices:
            assert math.isclose(vec_dot(v, poly.normal), 0.0, abs_tol=1e-9)
            assert all(-1.0 - 1e-9 <= c <= 1.0 + 1e-9 for c in v)

    # Exactly 27 Zero-Nodes {-1, 0, 1}^3 = 1 center + 6 faces + 12 edges + 8 corners
    assert len(scene.nodes) == 27
    kinds = [n.metadata["kind"] for n in scene.nodes]
    assert kinds.count("center") == 1
    assert kinds.count("face_center") == 6
    assert kinds.count("edge_midpoint") == 12
    assert kinds.count("cube_corner") == 8


def test_conical_vortex_six_face_axes_and_apex_convergence() -> None:
    scene = build_conical_vortex_field(vitality=1.0, all_six_axes=True)
    centripetal = [pl for pl in scene.polylines if pl.role == "positive"]
    centrifugal = [pl for pl in scene.polylines if pl.role == "negative"]

    # 6 cube faces -> 6 centripetal (+) cones and 6 centrifugal (-) cones
    assert len(centripetal) == 6
    assert len(centrifugal) == 6

    # At t=1 (final point), every centripetal spiral converges onto the central focal sphere near (0,0,0)
    for cone in centripetal:
        end_pt = cone.points[-1]
        assert vec_length(end_pt) < 0.05

    # Flat zero pressure equator at y=0 must have strictly zero y-coordinate across its span
    zero_eq = [pl for pl in scene.polylines if pl.group == "pressure_equators" and pl.role == "zero"]
    assert len(zero_eq) == 1
    assert all(abs(pt[1]) < 1e-9 for pt in zero_eq[0].points)


def test_light_sphere_lens_octant_curvature_reversal() -> None:
    # Inflection curve must vanish in value AND second derivative at s=0, reversing concavity across s=0
    assert math.isclose(lens_inflection_curve(0.0), 0.0, abs_tol=1e-12)
    h = 1e-4
    d2_zero = (lens_inflection_curve(h) - 2 * lens_inflection_curve(0.0) + lens_inflection_curve(-h)) / (h * h)
    d2_pos = (lens_inflection_curve(0.5 + h) - 2 * lens_inflection_curve(0.5) + lens_inflection_curve(0.5 - h)) / (h * h)
    d2_neg = (lens_inflection_curve(-0.5 + h) - 2 * lens_inflection_curve(-0.5) + lens_inflection_curve(-0.5 - h)) / (h * h)
    assert abs(d2_zero) < 1e-8
    assert d2_pos < 0.0 < d2_neg  # Strict concavity sign reversal across the zero equator!

    scene = build_light_sphere_lens(rays_per_meridian=8, coronal_rings=3)
    equators = [pl for pl in scene.polylines if pl.group == "equators"]
    assert len(equators) == 3
    gravity_rays = [pl for pl in scene.polylines if pl.group == "gravity_focus"]
    assert len(gravity_rays) == 8  # One per spherical octant


def test_gyroscopic_octave_true_sphere_exclusively_at_90_deg_amplitude() -> None:
    scene = build_gyroscopic_octave_system()
    assert len(scene.nodes) == 9
    assert len(GYRO_STAGES) == 9

    for node in scene.nodes:
        tone = node.metadata["tone"]
        inc = node.metadata["inclination_deg"]
        shape = node.metadata["shape"]
        if tone == "4±":
            assert math.isclose(inc, 90.0)
            assert shape == "sphere"
        elif tone in ("1+", "2+", "3+"):
            assert 0.0 < inc < 90.0
            assert shape == "prolate"
        elif tone in ("3-", "2-", "1-"):
            assert 90.0 < inc < 180.0
            assert shape == "oblate"


def test_periodic_helix_unifies_axial_fig177_and_lateral_fig180() -> None:
    elements = build_periodic_elements()
    assert any(el.symbol == "C" and el.octave == 4 and el.tone == "4±" for el in elements)

    scene = build_periodic_helix_9_octave()
    carbon_nodes = [n for n in scene.nodes if n.label == "C" and n.metadata["octave"] == 4]
    assert len(carbon_nodes) == 1
    cx, cy, _ = carbon_nodes[0].position
    # In Axial View (X, Y), Carbon (4±, 90°) sits directly on the vertical X=0 Wave Amplitude Crest (Y > 0)!
    assert abs(cx) < 1e-9
    assert cy > 0.5

    # All Inert Gases (tone "0") sit strictly on the horizontal Y=0 Zero-Equator in Axial View!
    inert_nodes = [n for n in scene.nodes if n.metadata["tone"] == "0"]
    assert len(inert_nodes) >= 9
    for nd in inert_nodes:
        assert abs(nd.position[1]) < 1e-9

    # Along the Z Wave Axis (Lateral View, Fig. 180), octave Z increases strictly monotonically across Octaves 1..9
    octave_z_means = []
    for oct_n in range(1, 10):
        zs = [n.position[2] for n in scene.nodes if n.metadata["octave"] == oct_n]
        octave_z_means.append(sum(zs) / len(zs))
    assert all(octave_z_means[i] < octave_z_means[i + 1] for i in range(len(octave_z_means) - 1))


def test_exporters_and_cli(tmp_path: Path) -> None:
    models = build_all_models()
    assert len(models) == 5

    cube = models["cube_sphere"]
    obj_str = export_obj(cube, tmp_path / "cube.obj")
    assert "o cube_sphere_lattice" in obj_str
    assert "\nf " in obj_str and "\nl " in obj_str

    json_str = export_json(cube, tmp_path / "cube.json")
    parsed = json.loads(json_str)
    assert len(parsed["polygons"]) == 9
    assert len(parsed["nodes"]) == 27

    svg_str = export_svg_projection(cube, tmp_path / "cube.svg")
    assert svg_str.startswith("<svg ") and svg_str.strip().endswith("</svg>")

    rc = cli_main(["export", "--model", "periodic_helix", "--format", "obj", "--out", str(tmp_path / "cli_out")])
    assert rc == 0
    assert (tmp_path / "cli_out" / "periodic_helix.obj").exists()
