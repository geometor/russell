"""Parametric 3D geometry generators for Walter Russell's Wave-Field Cosmogony.

Almost all 180 chalkboard figures in Russell's *Home Study Course* (1950–1952)
are orthographic slices or camera projections of five coupled 3D structures:

1. ``CubeSphereLattice`` (Figs. 105–124):
   Bounding Cube ``[-1, 1]^3`` of Still Magnetic Light, inscribed unit Sphere,
   27 zero-nodes ``{-1, 0, 1}^3``, 3 orthogonal zero-curvature planes, and
   6 diagonal bisecting zero-curvature planes (total = 9 Equators).
2. ``ConicalVortexField`` (Figs. 38–47, 117–124, 158–161):
   Six centripetal (``+``) cones projecting inward from the 6 cube faces to the
   common gravitational apex ``(0, 0, 0)``, paired with centrifugal (``-``)
   unwinding spirals and curved pressure equators.
3. ``LightSphereLens`` (Figs. 170–172):
   3D octant-divided optical wave-field whose field trajectories pass through
   zero curvature (``kappa = 0``) on the 3 orthogonal equators and reverse
   concavity across adjacent octants while ejecting equatorial rings.
4. ``GyroscopicOctaveSystem`` (Figs. 95–104):
   Nine gyroscopic precession stages (``0 -> 1+ -> 2+ -> 3+ -> 4± -> 3- -> 2- -> 1- -> 0``)
   precessing from ``0°`` to ``90°`` (True Sphere at Wave Amplitude ``4±``) to ``180°``
   while morphing from prolate spheroids to a true sphere to oblate ringed systems.
5. ``PeriodicHelix9Octave`` (Figs. 177, 179–180):
   Unified 3D 9-octave conical helical wave of the elements whose axial camera
   projection reproduces Russell's concentric chart (Fig. 177) and whose lateral
   camera projection reproduces the corkscrew octave wave (Fig. 180).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

from geometor.russell.elements_data import OCTAVE_SPECS, build_periodic_elements

Vec3 = tuple[float, float, float]

PALETTE: dict[str, str] = {
    "zero": "#e8b85a",       # Still Magnetic Light / 9 Equators / Inert Gases
    "positive": "#fb7185",   # Centripetal / Genero-active (+) / Compression
    "negative": "#38bdf8",   # Centrifugal / Radio-active (-) / Expansion
    "amplitude": "#fef08a",  # 4± Wave Crest / Carbon / True Sphere
    "frame": "#ebe6dc",      # Outer structural cube / neutral reference
    "muted": "#64748b",      # Secondary coordinate guides
}


def vec_add(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def vec_sub(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def vec_scale(v: Vec3, s: float) -> Vec3:
    return (v[0] * s, v[1] * s, v[2] * s)


def vec_dot(a: Vec3, b: Vec3) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def vec_cross(a: Vec3, b: Vec3) -> Vec3:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def vec_length(v: Vec3) -> float:
    return math.sqrt(vec_dot(v, v))


def vec_normalize(v: Vec3) -> Vec3:
    length = vec_length(v)
    if length < 1e-12:
        return (0.0, 0.0, 0.0)
    return (v[0] / length, v[1] / length, v[2] / length)


def rotate_z(v: Vec3, rad: float) -> Vec3:
    c, s = math.cos(rad), math.sin(rad)
    return (v[0] * c - v[1] * s, v[0] * s + v[1] * c, v[2])


def rotate_x(v: Vec3, rad: float) -> Vec3:
    c, s = math.cos(rad), math.sin(rad)
    return (v[0], v[1] * c - v[2] * s, v[1] * s + v[2] * c)


def rotate_y(v: Vec3, rad: float) -> Vec3:
    c, s = math.cos(rad), math.sin(rad)
    return (v[0] * c + v[2] * s, v[1], -v[0] * s + v[2] * c)


@dataclass(frozen=True)
class Polyline3D:
    """A 3D curve or wireframe edge sequence."""

    points: tuple[Vec3, ...]
    role: str = "frame"
    group: str = "default"
    closed: bool = False
    width: float = 1.6
    dashed: bool = False
    label: str = ""


@dataclass(frozen=True)
class Polygon3D:
    """A planar 3D face (such as one of the 9 zero-curvature equators)."""

    vertices: tuple[Vec3, ...]
    normal: Vec3
    role: str = "zero"
    group: str = "planes"
    opacity: float = 0.14
    label: str = ""


@dataclass(frozen=True)
class Node3D:
    """A discrete 3D locus (zero-node, focal apex, or locked element)."""

    position: Vec3
    label: str
    role: str = "zero"
    group: str = "nodes"
    radius: float = 5.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Scene3D:
    """Complete parametric 3D model ready for .obj, .json, or SVG projection."""

    name: str
    title: str
    figures: str
    description: str
    polylines: list[Polyline3D] = field(default_factory=list)
    polygons: list[Polygon3D] = field(default_factory=list)
    nodes: list[Node3D] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the 3D scene to a JSON-compatible dictionary."""
        return {
            "name": self.name,
            "title": self.title,
            "figures": self.figures,
            "description": self.description,
            "palette": PALETTE,
            "polylines": [
                {
                    "points": [list(p) for p in pl.points],
                    "role": pl.role,
                    "group": pl.group,
                    "closed": pl.closed,
                    "width": pl.width,
                    "dashed": pl.dashed,
                    "label": pl.label,
                }
                for pl in self.polylines
            ],
            "polygons": [
                {
                    "vertices": [list(v) for v in pg.vertices],
                    "normal": list(pg.normal),
                    "role": pg.role,
                    "group": pg.group,
                    "opacity": pg.opacity,
                    "label": pg.label,
                }
                for pg in self.polygons
            ],
            "nodes": [
                {
                    "position": list(nd.position),
                    "label": nd.label,
                    "role": nd.role,
                    "group": nd.group,
                    "radius": nd.radius,
                    "metadata": nd.metadata,
                }
                for nd in self.nodes
            ],
        }


# ---------------------------------------------------------------------------
# 1. Cube-Sphere Lattice & Nine Equators (Figs. 105–124)
# ---------------------------------------------------------------------------


def build_cube_sphere_lattice(
    include_diagonal_planes: bool = True,
    circle_segments: int = 64,
) -> Scene3D:
    """Build the Cube-Sphere Wave-Field of Nine Equators (Fig. 114).

    Contains:
    - Outer bounding Cube ``[-1, 1]^3`` (12 edges)
    - 3 Orthogonal Zero-Curvature Planes (``x=0``, ``y=0``, ``z=0``)
    - 6 Diagonal Bisecting Zero-Curvature Planes (``x±y=0``, ``y±z=0``, ``z±x=0``)
    - Inscribed Unit Sphere (3 great circles + latitude parallels)
    - All 27 Zero-Nodes ``{-1, 0, 1}^3``
    """
    scene = Scene3D(
        name="cube_sphere_lattice",
        title="The Cube-Sphere Wave-Field & Nine Equators",
        figures="Figs. 105–124 (Plate IV • Fig. 114)",
        description=(
            "Bounding Cube of Still Magnetic Light [-1,1]^3 enclosing the inscribed "
            "unit Sphere of curved motion, divided into 8 octants by 3 orthogonal "
            "and 6 diagonal planes of zero curvature (9 Equators) with 27 zero-nodes."
        ),
    )

    # 12 Outer Cube Edges
    for a in (-1.0, 1.0):
        for b in (-1.0, 1.0):
            scene.polylines.append(
                Polyline3D(((-1.0, a, b), (1.0, a, b)), role="frame", group="cube", width=1.8)
            )
            scene.polylines.append(
                Polyline3D(((a, -1.0, b), (a, 1.0, b)), role="frame", group="cube", width=1.8)
            )
            scene.polylines.append(
                Polyline3D(((a, b, -1.0), (a, b, 1.0)), role="frame", group="cube", width=1.8)
            )

    # 3 Central Orthogonal Axes
    scene.polylines.append(
        Polyline3D(((-1.0, 0.0, 0.0), (1.0, 0.0, 0.0)), role="zero", group="axes", width=2.0)
    )
    scene.polylines.append(
        Polyline3D(((0.0, -1.0, 0.0), (0.0, 1.0, 0.0)), role="zero", group="axes", width=2.0)
    )
    scene.polylines.append(
        Polyline3D(((0.0, 0.0, -1.0), (0.0, 0.0, 1.0)), role="zero", group="axes", width=2.0)
    )

    # 3 Orthogonal Zero-Curvature Planes
    ortho_specs: list[tuple[str, tuple[Vec3, ...], Vec3]] = [
        ("X = 0", ((0.0, -1.0, -1.0), (0.0, 1.0, -1.0), (0.0, 1.0, 1.0), (0.0, -1.0, 1.0)), (1.0, 0.0, 0.0)),
        ("Y = 0", ((-1.0, 0.0, -1.0), (1.0, 0.0, -1.0), (1.0, 0.0, 1.0), (-1.0, 0.0, 1.0)), (0.0, 1.0, 0.0)),
        ("Z = 0", ((-1.0, -1.0, 0.0), (1.0, -1.0, 0.0), (1.0, 1.0, 0.0), (-1.0, 1.0, 0.0)), (0.0, 0.0, 1.0)),
    ]
    for lbl, verts, nrm in ortho_specs:
        scene.polygons.append(
            Polygon3D(vertices=verts, normal=nrm, role="zero", group="ortho_planes", opacity=0.14, label=lbl)
        )

    # 6 Diagonal Bisecting Zero-Curvature Planes
    if include_diagonal_planes:
        inv_s2 = 1.0 / math.sqrt(2.0)
        diag_specs: list[tuple[str, tuple[Vec3, ...], Vec3]] = [
            ("X - Y = 0", ((-1.0, -1.0, -1.0), (1.0, 1.0, -1.0), (1.0, 1.0, 1.0), (-1.0, -1.0, 1.0)), (inv_s2, -inv_s2, 0.0)),
            ("X + Y = 0", ((-1.0, 1.0, -1.0), (1.0, -1.0, -1.0), (1.0, -1.0, 1.0), (-1.0, 1.0, 1.0)), (inv_s2, inv_s2, 0.0)),
            ("Y - Z = 0", ((-1.0, -1.0, -1.0), (1.0, -1.0, -1.0), (1.0, 1.0, 1.0), (-1.0, 1.0, 1.0)), (0.0, inv_s2, -inv_s2)),
            ("Y + Z = 0", ((-1.0, 1.0, -1.0), (1.0, 1.0, -1.0), (1.0, -1.0, 1.0), (-1.0, -1.0, 1.0)), (0.0, inv_s2, inv_s2)),
            ("Z - X = 0", ((-1.0, -1.0, -1.0), (-1.0, 1.0, -1.0), (1.0, 1.0, 1.0), (1.0, -1.0, 1.0)), (-inv_s2, 0.0, inv_s2)),
            ("Z + X = 0", ((1.0, -1.0, -1.0), (1.0, 1.0, -1.0), (-1.0, 1.0, 1.0), (-1.0, -1.0, 1.0)), (inv_s2, 0.0, inv_s2)),
        ]
        for lbl, verts, nrm in diag_specs:
            scene.polygons.append(
                Polygon3D(vertices=verts, normal=nrm, role="negative", group="diag_planes", opacity=0.07, label=lbl)
            )

    # Inscribed Unit Sphere (3 Great Equator Circles + 2 Latitude Parallels)
    angles = [2.0 * math.pi * k / circle_segments for k in range(circle_segments + 1)]
    scene.polylines.append(
        Polyline3D(
            tuple((math.cos(a), math.sin(a), 0.0) for a in angles),
            role="negative",
            group="sphere",
            closed=True,
            width=1.6,
            label="Sphere Equator XY",
        )
    )
    scene.polylines.append(
        Polyline3D(
            tuple((math.cos(a), 0.0, math.sin(a)) for a in angles),
            role="negative",
            group="sphere",
            closed=True,
            width=1.6,
            label="Sphere Equator XZ",
        )
    )
    scene.polylines.append(
        Polyline3D(
            tuple((0.0, math.cos(a), math.sin(a)) for a in angles),
            role="negative",
            group="sphere",
            closed=True,
            width=1.6,
            label="Sphere Equator YZ",
        )
    )
    for lat_y in (-0.5, 0.5):
        r_lat = math.sqrt(1.0 - lat_y * lat_y)
        scene.polylines.append(
            Polyline3D(
                tuple((r_lat * math.cos(a), lat_y, r_lat * math.sin(a)) for a in angles),
                role="negative",
                group="sphere",
                closed=True,
                width=1.0,
                dashed=True,
            )
        )

    # 27 Zero-Nodes {-1, 0, 1}^3
    for ix in (-1, 0, 1):
        for iy in (-1, 0, 1):
            for iz in (-1, 0, 1):
                manhattan = abs(ix) + abs(iy) + abs(iz)
                if manhattan == 0:
                    kind, role, rad = "center", "amplitude", 8.0
                elif manhattan == 1:
                    kind, role, rad = "face_center", "zero", 5.5
                elif manhattan == 2:
                    kind, role, rad = "edge_midpoint", "zero", 4.5
                else:
                    kind, role, rad = "cube_corner", "zero", 5.0
                scene.nodes.append(
                    Node3D(
                        position=(float(ix), float(iy), float(iz)),
                        label="0",
                        role=role,
                        group="zero_nodes",
                        radius=rad,
                        metadata={"kind": kind, "ijk": [ix, iy, iz]},
                    )
                )

    return scene


# ---------------------------------------------------------------------------
# 2. Six-Face Conical Vortex Field (Figs. 38–47, 117–124, 158–161)
# ---------------------------------------------------------------------------


def _map_local_axis(u: float, v: float, w_ax: float, axis: str, sign: float) -> Vec3:
    """Map local cone coordinates (u, v, w_ax) where w_ax in [0, 1] runs from center to cube face."""
    val = sign * w_ax
    if axis == "Y":
        return (u, val, v)
    if axis == "X":
        return (val, u, v)
    return (u, v, val)


def build_conical_vortex_field(
    vitality: float = 1.0,
    turns: float = 3.5,
    all_six_axes: bool = True,
    steps: int = 120,
) -> Scene3D:
    """Build the 3D Interpenetrating Conical Vortex Field (Figs. 38–47, 119, 158–161).

    In 3D, each of the 6 square zero-curvature faces of the bounding Cube projects
    a centripetal (``+``) spiral cone inward to the common gravitational center
    ``(0, 0, 0)``, while centrifugal (``-``) spirals unwind back toward the cube faces.
    """
    v_clamped = max(0.05, min(1.0, vitality))
    scene = Scene3D(
        name="conical_vortex_field",
        title="Six-Face Cube-to-Apex Conical Vortex Field",
        figures="Figs. 38–47, 117–124, 158–161",
        description=(
            "Six centripetal (+) spiral cones projecting inward from the 6 cube faces "
            "to the central gravitational nucleus (0,0,0), paired with centrifugal (-) "
            "unwinding cones and curved pressure equators."
        ),
    )

    # Subtle Cube Wireframe Reference
    for a in (-1.0, 1.0):
        for b in (-1.0, 1.0):
            scene.polylines.append(Polyline3D(((-1.0, a, b), (1.0, a, b)), role="muted", group="cube", width=1.0))
            scene.polylines.append(Polyline3D(((a, -1.0, b), (a, 1.0, b)), role="muted", group="cube", width=1.0))
            scene.polylines.append(Polyline3D(((a, b, -1.0), (a, b, 1.0)), role="muted", group="cube", width=1.0))

    axes = [("Y", 1.0), ("Y", -1.0)]
    if all_six_axes:
        axes.extend([("X", 1.0), ("X", -1.0), ("Z", 1.0), ("Z", -1.0)])

    for axis_name, sign in axes:
        is_primary = axis_name == "Y"
        grp = "primary_cones" if is_primary else "secondary_cones"
        # Base circle on cube face
        ring_pts: list[Vec3] = []
        for k in range(49):
            ang = 2.0 * math.pi * k / 48
            r_face = 0.88 * v_clamped
            ring_pts.append(_map_local_axis(r_face * math.cos(ang), r_face * math.sin(ang), 1.0, axis_name, sign))
        scene.polylines.append(
            Polyline3D(tuple(ring_pts), role="zero", group=grp, closed=True, width=1.4 if is_primary else 1.0)
        )

        # Centripetal (+) inward spiral: Cube face (t=0) -> Focal apex (t=1)
        in_pts: list[Vec3] = []
        out_pts: list[Vec3] = []
        for i in range(steps + 1):
            t = i / steps
            # Conical radius tapers linearly from cube face to incandescent focal sphere
            r = (0.88 * (1.0 - t) + 0.03) * v_clamped
            theta_in = 2.0 * math.pi * turns * t * sign
            theta_out = -theta_in + math.pi
            in_pts.append(_map_local_axis(r * math.cos(theta_in), r * math.sin(theta_in), 1.0 - t * v_clamped, axis_name, sign))
            out_pts.append(_map_local_axis(r * math.cos(theta_out), r * math.sin(theta_out), 1.0 - t * v_clamped, axis_name, sign))

        scene.polylines.append(
            Polyline3D(
                tuple(in_pts),
                role="positive",
                group=grp,
                width=2.2 if is_primary else 1.3,
                label=f"Centripetal +{axis_name}" if sign > 0 else f"Centripetal -{axis_name}",
            )
        )
        scene.polylines.append(
            Polyline3D(
                tuple(out_pts),
                role="negative",
                group=grp,
                width=1.8 if is_primary else 1.1,
                dashed=not is_primary,
                label=f"Centrifugal +{axis_name}" if sign > 0 else f"Centrifugal -{axis_name}",
            )
        )

    # Curved Pressure Equators along primary Y axis (Fig. 159: curved away from center, flat at y=0)
    for y_base in (-0.65, -0.32, 0.0, 0.32, 0.65):
        eq_pts: list[Vec3] = []
        for k in range(49):
            phi = -1.0 + 2.0 * k / 48
            # At y_base = 0, curvature is strictly 0 (flat plane); away from 0, arcs curve!
            arch = -0.18 * y_base * (1.0 - phi * phi)
            r_eq = 0.78 * (1.0 - 0.35 * abs(y_base))
            eq_pts.append((r_eq * phi, y_base + arch, 0.0))
        scene.polylines.append(
            Polyline3D(
                tuple(eq_pts),
                role="zero" if abs(y_base) < 1e-6 else "muted",
                group="pressure_equators",
                width=2.2 if abs(y_base) < 1e-6 else 1.2,
                dashed=abs(y_base) >= 1e-6,
            )
        )

    # Central Incandescent Nucleus Node
    scene.nodes.append(
        Node3D(
            position=(0.0, 0.0, 0.0),
            label="4± APEX",
            role="amplitude",
            group="apex",
            radius=8.5,
            metadata={"vitality": v_clamped},
        )
    )
    return scene


# ---------------------------------------------------------------------------
# 3. Eight-Octant Light-Sphere Lens (Figs. 170–172)
# ---------------------------------------------------------------------------


def lens_inflection_curve(s: float, amplitude: float = 0.24) -> float:
    """Odd-symmetric octant deflection ``d(s) = A * sin(pi * s)`` for ``s in [-1, 1]``.

    Guarantees exact zero value ``d(0) = 0`` and exact zero curvature ``d''(0) = 0``
    on the orthogonal zero-curvature equator ``s = 0``, with opposite concavity
    (``d''(s) < 0`` vs ``d''(s) > 0``) across adjacent octants!
    """
    return amplitude * math.sin(math.pi * s)


def build_light_sphere_lens(
    rays_per_meridian: int = 8,
    coronal_rings: int = 3,
    steps: int = 80,
) -> Scene3D:
    """Build the 3D 8-Octant Curvature-Reversing Light-Sphere Lens (Figs. 170–172).

    Contains:
    - 3 Circular Zero-Curvature Equators dividing the unit sphere into 8 octants
    - Inflecting 3D light-ray trajectories whose curvature vanishes on the equators
      and reverses sign in opposite octants (Fig. 170–171)
    - Equatorial coronal rings & condensing planetary nodes (Fig. 172)
    """
    scene = Scene3D(
        name="light_sphere_lens",
        title="Eight-Octant Spherical Light-Lens & Coronal Ring Genesis",
        figures="Figs. 170–172",
        description=(
            "Spherical optical wave-field divided into 8 octants by 3 zero-curvature "
            "equators; field trajectories lose curvature at every zero plane and reverse "
            "concavity across octants while casting off equatorial rings."
        ),
    )

    angles = [2.0 * math.pi * k / 72 for k in range(73)]
    # 3 Orthogonal Circular Zero-Equators of the Lens (Fig. 170)
    scene.polylines.append(
        Polyline3D(tuple((math.cos(a), 0.0, math.sin(a)) for a in angles), role="zero", group="equators", closed=True, width=2.4, label="United Equator (Y=0)")
    )
    scene.polylines.append(
        Polyline3D(tuple((math.cos(a), math.sin(a), 0.0) for a in angles), role="zero", group="equators", closed=True, width=1.8, label="Polar Equator (Z=0)")
    )
    scene.polylines.append(
        Polyline3D(tuple((0.0, math.cos(a), math.sin(a)) for a in angles), role="zero", group="equators", closed=True, width=1.8, label="Polar Equator (X=0)")
    )

    # Curvature-Reversing Light Trajectories passing through the 8 octants across Y=0
    for m in range(rays_per_meridian):
        az = 2.0 * math.pi * m / rays_per_meridian + math.pi / rays_per_meridian
        pts: list[Vec3] = []
        for i in range(steps + 1):
            s = -1.0 + 2.0 * i / steps  # s=-1 (South pole) -> s=0 (United Equator) -> s=+1 (North pole)
            # Radial envelope inside the unit sphere focusing toward polar/central compression
            lat = s * (math.pi * 0.5)
            defl = lens_inflection_curve(s, amplitude=0.34)
            r_xz = math.cos(lat) * 0.98
            y = math.sin(lat) * 0.98
            x = r_xz * math.cos(az + defl)
            z = r_xz * math.sin(az + defl)
            pts.append((x, y, z))
        scene.polylines.append(
            Polyline3D(
                tuple(pts),
                role="positive" if m % 2 == 0 else "negative",
                group="octant_rays",
                width=1.7,
                label=f"Octant Ray {m + 1}",
            )
        )

    # Inward-Focusing Gravity Rays from Sphere Boundary to Center (Fig. 171)
    for sign_x in (-1.0, 1.0):
        for sign_y in (-1.0, 1.0):
            for sign_z in (-1.0, 1.0):
                oct_pts: list[Vec3] = []
                inv_s3 = 1.0 / math.sqrt(3.0)
                for i in range(33):
                    t = i / 32  # 0 at center, 1 at octant midpoint on unit sphere
                    bend = 0.16 * math.sin(math.pi * t)
                    bx = sign_x * inv_s3 * t
                    by = sign_y * inv_s3 * t + sign_y * bend
                    bz = sign_z * inv_s3 * t - sign_z * bend * 0.5
                    oct_pts.append((bx, by, bz))
                scene.polylines.append(
                    Polyline3D(tuple(oct_pts), role="positive", group="gravity_focus", width=1.4)
                )

    # Equatorial Coronas Becoming Rings & Orbiting Planets (Fig. 172)
    ring_radii = [1.22 + 0.28 * k for k in range(coronal_rings)]
    for idx, r_ring in enumerate(ring_radii):
        scene.polylines.append(
            Polyline3D(
                tuple((r_ring * math.cos(a), 0.0, r_ring * math.sin(a)) for a in angles),
                role="negative" if idx > 0 else "zero",
                group="coronal_rings",
                closed=True,
                width=1.6 - 0.25 * idx,
                dashed=idx == coronal_rings - 1,
                label=f"Coronal Ring {idx + 1}",
            )
        )
        planet_ang = idx * 2.1 + 0.4
        scene.nodes.append(
            Node3D(
                position=(r_ring * math.cos(planet_ang), 0.0, r_ring * math.sin(planet_ang)),
                label=f"Ring {idx + 1}",
                role="negative",
                group="planets",
                radius=4.5,
            )
        )

    # 6 Pole Markers + Central Gravity Focus
    pole_coords = [
        ((0.0, 1.0, 0.0), "1 (N)"),
        ((0.0, -1.0, 0.0), "4 (S)"),
        ((1.0, 0.0, 0.0), "2"),
        ((-1.0, 0.0, 0.0), "5"),
        ((0.0, 0.0, 1.0), "3"),
        ((0.0, 0.0, -1.0), "6"),
    ]
    for pos, lbl in pole_coords:
        scene.nodes.append(Node3D(position=pos, label=lbl, role="zero", group="poles", radius=4.5))

    scene.nodes.append(
        Node3D(
            position=(0.0, 0.0, 0.0),
            label="GRAVITY CENTER",
            role="amplitude",
            group="center",
            radius=8.5,
        )
    )
    return scene


# ---------------------------------------------------------------------------
# 4. Gyroscopic Precession & Spheroid Morphing (Figs. 95–104)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class GyroStage:
    """Parameters of one locking stage along the 0 -> 4± -> 0 gyroscopic arch."""

    tone: str
    title: str
    inclination_deg: float  # 0° at Inert Gas -> 90° at Wave Amplitude -> 180° at Inert Gas
    eq_radius: float        # Equatorial semi-axis a
    polar_radius: float     # Polar semi-axis c (c > a: prolate; c == a: sphere; c < a: oblate)
    rings: int              # Detached equatorial rings (Saturn / Ring Nebula stages)
    role: str


GYRO_STAGES: tuple[GyroStage, ...] = (
    GyroStage("0", "Inert Gas Seed", 0.0, 0.34, 0.06, 1, "zero"),
    GyroStage("1+", "Prolate Spiral", 22.5, 0.16, 0.38, 0, "positive"),
    GyroStage("2+", "Compressing Prolate", 45.0, 0.23, 0.35, 0, "positive"),
    GyroStage("3+", "Integrating Spheroid", 67.5, 0.29, 0.33, 0, "positive"),
    GyroStage("4±", "True Sphere (Carbon / Sun)", 90.0, 0.36, 0.36, 1, "amplitude"),
    GyroStage("3-", "Oblate Spheroid", 112.5, 0.36, 0.26, 1, "negative"),
    GyroStage("2-", "Ringed System (Saturn)", 135.0, 0.34, 0.19, 2, "negative"),
    GyroStage("1-", "Ring Nebula (Lyra)", 157.5, 0.38, 0.11, 2, "negative"),
    GyroStage("0", "Inert Gas Rebirth", 180.0, 0.34, 0.06, 1, "zero"),
)


def build_gyroscopic_octave_system(
    parallels: int = 5,
    meridians: int = 8,
) -> Scene3D:
    """Build the 3D Gyroscopic Precession & Spheroid Morphing Wave (Figs. 95–104).

    Demonstrates why ONLY the ``90°`` Wave Amplitude crest (``4±``) produces a
    **True Sphere** (``eq_radius == polar_radius``), flanked by prolate centripetal
    winding stages (``1+, 2+, 3+``) and oblate/ringed centrifugal unwinding stages
    (``3-, 2-, 1-``).
    """
    scene = Scene3D(
        name="gyroscopic_octave_system",
        title="Gyroscopic Precession & Prolate-to-Sphere-to-Oblate Evolution",
        figures="Figs. 95–104, 180",
        description=(
            "Nine gyroscopic locking stages along the octave wave arch showing axis "
            "precession from 0° through 90° (True Sphere at Wave Amplitude 4±) to 180° "
            "and spheroid morphogenesis from prolate winding to oblate ring ejection."
        ),
    )

    # Baseline Zero Wave Axis & Octave Arch Trajectory
    scene.polylines.append(
        Polyline3D(((-4.4, -0.9, 0.0), (4.4, -0.9, 0.0)), role="zero", group="wave_axis", width=2.2, label="Zero Wave Axis")
    )
    arch_pts: list[Vec3] = []
    for i in range(121):
        u = i / 120  # 0 to 1
        x = -4.0 + 8.0 * u
        y = -0.9 + 1.85 * math.sin(math.pi * u)
        z = 0.22 * math.sin(2.0 * math.pi * u)
        arch_pts.append((x, y, z))
    scene.polylines.append(
        Polyline3D(tuple(arch_pts), role="frame", group="wave_arch", width=2.0, label="Octave Wave Arch")
    )

    # 9 Precessing 3D Spheroids + Equatorial Rings
    ring_segs = 36
    for idx, st in enumerate(GYRO_STAGES):
        u = idx / (len(GYRO_STAGES) - 1)
        cx = -4.0 + 8.0 * u
        cy = -0.9 + 1.85 * math.sin(math.pi * u)
        cz = 0.22 * math.sin(2.0 * math.pi * u)
        center = (cx, cy, cz)

        # Tilt spin axis from horizontal wave axis (0°) -> vertical perpendicular (90°) -> (-180°)
        tilt_rad = math.radians(st.inclination_deg - 90.0)

        def transform_local(pt: Vec3, tr: float = tilt_rad, ctr: Vec3 = center) -> Vec3:
            return vec_add(ctr, rotate_z(pt, tr))

        # Spin Axis Segment
        ax_len = st.polar_radius + 0.16
        scene.polylines.append(
            Polyline3D(
                (transform_local((0.0, -ax_len, 0.0)), transform_local((0.0, ax_len, 0.0))),
                role=st.role,
                group="spin_axes",
                width=1.6,
            )
        )

        # Latitude Parallels of the Spheroid
        for p_idx in range(1, parallels + 1):
            v_ang = -0.5 * math.pi + math.pi * p_idx / (parallels + 1)
            r_p = st.eq_radius * math.cos(v_ang)
            y_p = st.polar_radius * math.sin(v_ang)
            pts_lat = tuple(
                transform_local((r_p * math.cos(2.0 * math.pi * k / ring_segs), y_p, r_p * math.sin(2.0 * math.pi * k / ring_segs)))
                for k in range(ring_segs + 1)
            )
            scene.polylines.append(Polyline3D(pts_lat, role=st.role, group="spheroids", closed=True, width=1.2))

        # Longitude Meridians of the Spheroid
        for m_idx in range(meridians // 2):
            az = math.pi * m_idx / (meridians // 2)
            pts_mer = tuple(
                transform_local(
                    (
                        st.eq_radius * math.cos(2.0 * math.pi * k / ring_segs) * math.cos(az),
                        st.polar_radius * math.sin(2.0 * math.pi * k / ring_segs),
                        st.eq_radius * math.cos(2.0 * math.pi * k / ring_segs) * math.sin(az),
                    )
                )
                for k in range(ring_segs + 1)
            )
            scene.polylines.append(Polyline3D(pts_mer, role=st.role, group="spheroids", closed=True, width=1.0))

        # Detached Equatorial Rings (Amplitude Planetary Plane / Saturn / Lyra Rings)
        for r_k in range(st.rings):
            r_det = st.eq_radius + 0.14 + 0.10 * r_k
            pts_ring = tuple(
                transform_local((r_det * math.cos(2.0 * math.pi * k / ring_segs), 0.0, r_det * math.sin(2.0 * math.pi * k / ring_segs)))
                for k in range(ring_segs + 1)
            )
            scene.polylines.append(
                Polyline3D(pts_ring, role="zero" if st.tone == "4±" else st.role, group="rings", closed=True, width=1.5, dashed=r_k > 0)
            )

        aspect_ratio = st.polar_radius / st.eq_radius
        shape_kind = (
            "sphere"
            if abs(aspect_ratio - 1.0) < 1e-6
            else ("prolate" if aspect_ratio > 1.0 else "oblate")
        )
        scene.nodes.append(
            Node3D(
                position=center,
                label=f"{st.tone} • {st.title}",
                role=st.role,
                group="stages",
                radius=7.5 if st.tone == "4±" else 5.0,
                metadata={
                    "tone": st.tone,
                    "inclination_deg": st.inclination_deg,
                    "eq_radius": st.eq_radius,
                    "polar_radius": st.polar_radius,
                    "aspect_ratio": round(aspect_ratio, 4),
                    "shape": shape_kind,
                },
            )
        )

    return scene


# ---------------------------------------------------------------------------
# 5. Unified 3D Nine-Octave Periodic Helix (Unifying Fig. 177 & Fig. 180!)
# ---------------------------------------------------------------------------


def build_periodic_helix_9_octave(
    points_per_octave: int = 64,
) -> Scene3D:
    """Build the Unified 3D Nine-Octave Conical Spiral of the Elements (Figs. 177 & 180).

    Coordinate design unifies Russell's two periodic charts into ONE 3D geometry:
    - **Axial Projection ``(X, Y)``** looking down the ``Z`` wave axis reproduces
      *The Russell Periodic Chart of the Elements, No. 2* (``Fig. 177``, 1926):
      concentric expanding spiral turns with Inert Gases on the horizontal ``Y = 0``
      Zero-Equator and Carbon/Silicon/etc. on the vertical ``X = 0, Y > 0`` ``4±`` Crest.
    - **Lateral Projection ``(Z, Y)``** looking perpendicular to the ``Z`` wave axis
      reproduces the 9-Octave Wave Arch & Corkscrew Vortex (``Figs. 179–180``)!
    """
    scene = Scene3D(
        name="periodic_helix_9_octave",
        title="Unified 3D Nine-Octave Periodic Helix of the Elements",
        figures="Figs. 177, 179–180",
        description=(
            "Single 3D 9-octave conical helical wave of the elements whose axial "
            "projection (X, Y) yields Russell's 1926 concentric periodic chart (Fig. 177) "
            "and whose lateral projection (Z, Y) yields the corkscrew octave wave (Fig. 180)."
        ),
    )

    def octave_radius(oct_continuous: float) -> float:
        """Monotonically expanding conical radius across Octaves 1..9 (in [0.22, 1.85])."""
        return 0.22 + 0.18 * (oct_continuous - 1.0)

    def octave_z(oct_continuous: float) -> float:
        """Axial position along the Z wave axis centered at Octave 5 (in [-2.4, +2.4])."""
        return (oct_continuous - 5.2) * 0.56

    # Central Z Wave Axis & Orthogonal Zero-Equatorial / Amplitude Reference Planes
    z_min, z_max = octave_z(1.0) - 0.25, octave_z(10.0) + 0.25
    scene.polylines.append(
        Polyline3D(((0.0, 0.0, z_min), (0.0, 0.0, z_max)), role="zero", group="axes", width=2.4, label="Still Magnetic Wave Axis (0)")
    )
    scene.polylines.append(
        Polyline3D(((-2.05, 0.0, 0.0), (2.05, 0.0, 0.0)), role="zero", group="axes", width=2.0, label="Inert Gas Zero Equator (0—0)")
    )
    scene.polylines.append(
        Polyline3D(((0.0, -2.05, 0.0), (0.0, 2.05, 0.0)), role="amplitude", group="axes", width=1.8, dashed=True, label="Wave Amplitude Crest (4±)")
    )

    # Continuous 9-Octave 3D Spiral Wave Trajectory
    helix_pts: list[Vec3] = []
    total_steps = 9 * points_per_octave
    for i in range(total_steps + 1):
        u_oct = 1.0 + 9.0 * (i / total_steps)  # 1.0 at start of Octave I -> 10.0 at end of Octave IX
        frac = u_oct - math.floor(u_oct)
        if i == total_steps:
            frac = 1.0
        # Azimuth sweeps 180° -> 90° (Amplitude Crest) -> 0° (Inert Gas) -> -90° -> -180° per full cycle,
        # or across the upper semi-wave (pi -> 0) paired with harmonic return wave (0 -> -pi):
        az = math.pi - 2.0 * math.pi * frac
        r = octave_radius(u_oct)
        z = octave_z(u_oct)
        helix_pts.append((r * math.cos(az), r * math.sin(az), z))

    scene.polylines.append(
        Polyline3D(tuple(helix_pts), role="frame", group="helix_wave", width=1.9, label="9-Octave Conical Spiral")
    )

    # Concentric Octave Guide Rings (Octaves IV–IX)
    ring_angles = [2.0 * math.pi * k / 64 for k in range(65)]
    for spec in OCTAVE_SPECS:
        if spec.number >= 4:
            r_mid = octave_radius(spec.number + 0.5)
            z_mid = octave_z(spec.number + 0.5)
            scene.polylines.append(
                Polyline3D(
                    tuple((r_mid * math.cos(a), r_mid * math.sin(a), z_mid) for a in ring_angles),
                    role="muted",
                    group="octave_rings",
                    closed=True,
                    width=1.0,
                    dashed=True,
                    label=f"Octave {spec.roman}",
                )
            )

    # Discrete Element Locking Nodes across Octaves I–IX
    for el in build_periodic_elements():
        # Map azimuth_deg in [180°, 0°] across the active half-cycle of its octave
        progress = (180.0 - el.azimuth_deg) / 180.0  # 0.0 at Inert Start -> 0.5 at 4± Crest -> 1.0 at Inert End
        u_pos = float(el.octave) + progress * 0.5
        if el.tone == "0" and el.azimuth_deg == 0.0:
            u_pos = float(el.octave) + 1.0
        r = octave_radius(u_pos)
        z = octave_z(u_pos)
        az = math.radians(el.azimuth_deg)
        pos = (r * math.cos(az), r * math.sin(az), z)
        rad = 7.2 if el.polarity in ("amplitude", "zero") else 5.2
        scene.nodes.append(
            Node3D(
                position=pos,
                label=el.symbol,
                role=el.polarity,
                group=f"octave_{el.octave}",
                radius=rad,
                metadata={
                    "name": el.name,
                    "octave": el.octave,
                    "tone": el.tone,
                    "atomic_number": el.atomic_number,
                    "azimuth_deg": round(el.azimuth_deg, 2),
                },
            )
        )

    return scene


MODEL_REGISTRY: dict[str, Any] = {
    "cube_sphere": build_cube_sphere_lattice,
    "conical_vortex": build_conical_vortex_field,
    "light_lens": build_light_sphere_lens,
    "gyroscopic_octave": build_gyroscopic_octave_system,
    "periodic_helix": build_periodic_helix_9_octave,
}


def build_all_models() -> dict[str, Scene3D]:
    """Instantiate all five canonical 3D Russell cosmogony models."""
    return {key: builder() for key, builder in MODEL_REGISTRY.items()}
