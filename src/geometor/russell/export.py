"""Exporters for GEOMETOR Russell 3D Cosmogony scenes (.obj, .json, .svg).

Allows exact mathematical sharing between:
- Blender / MeshLab / CAD pipelines (Wavefront ``.obj``)
- Interactive WebGL / Canvas studios (``.json``)
- Print & Book Codex vector plates (depth-sorted 3D camera ``.svg``)
"""

from __future__ import annotations

import json
import math
from html import escape
from pathlib import Path

from geometor.russell.models3d import PALETTE, Scene3D, Vec3


def export_json(scene: Scene3D, out_path: Path | None = None, indent: int = 2) -> str:
    """Serialize ``scene`` to JSON and optionally write to ``out_path``."""
    payload = json.dumps(scene.to_dict(), indent=indent)
    if out_path is not None:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(payload, encoding="utf-8")
    return payload


def export_obj(scene: Scene3D, out_path: Path | None = None) -> str:
    """Export ``scene`` to Wavefront ``.obj`` format (polygons ``f``, polylines ``l``, nodes as octahedra)."""
    lines: list[str] = [
        f"# GEOMETOR Russell 3D Model: {scene.title}",
        f"# Figures: {scene.figures}",
        f"o {scene.name}",
        "",
    ]
    vert_idx = 1

    def emit_vertex(v: Vec3) -> int:
        nonlocal vert_idx
        lines.append(f"v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}")
        idx = vert_idx
        vert_idx += 1
        return idx

    if scene.polygons:
        lines.append("# Zero-Curvature Equator Planes")
        for pg_num, pg in enumerate(scene.polygons, start=1):
            lines.append(f"g {pg.group}_{pg_num}")
            idxs = [emit_vertex(v) for v in pg.vertices]
            lines.append("f " + " ".join(str(i) for i in idxs))
        lines.append("")

    if scene.polylines:
        lines.append("# Wave-Field Polylines & Trajectories")
        for pl_num, pl in enumerate(scene.polylines, start=1):
            lines.append(f"g {pl.group}_{pl_num}")
            idxs = [emit_vertex(v) for v in pl.points]
            if pl.closed and len(idxs) > 1 and idxs[0] != idxs[-1]:
                idxs.append(idxs[0])
            lines.append("l " + " ".join(str(i) for i in idxs))
        lines.append("")

    if scene.nodes:
        lines.append("# Discrete Locking & Zero Nodes (Octahedral Markers)")
        for nd_num, nd in enumerate(scene.nodes, start=1):
            cx, cy, cz = nd.position
            r = max(0.025, nd.radius * 0.006)
            safe_lbl = "".join(ch if ch.isalnum() else "_" for ch in nd.label).strip("_") or f"node_{nd_num}"
            lines.append(f"g node_{nd_num}_{safe_lbl}")
            top = emit_vertex((cx, cy + r, cz))
            bot = emit_vertex((cx, cy - r, cz))
            px = emit_vertex((cx + r, cy, cz))
            nx = emit_vertex((cx - r, cy, cz))
            pz = emit_vertex((cx, cy, cz + r))
            nz = emit_vertex((cx, cy, cz - r))
            for a, b, c in (
                (top, px, pz),
                (top, pz, nx),
                (top, nx, nz),
                (top, nz, px),
                (bot, pz, px),
                (bot, nx, pz),
                (bot, nz, nx),
                (bot, px, nz),
            ):
                lines.append(f"f {a} {b} {c}")

    text = "\n".join(lines) + "\n"
    if out_path is not None:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")
    return text


def project_point(
    pt: Vec3,
    yaw_deg: float = 34.0,
    pitch_deg: float = 22.0,
    width: int = 800,
    height: int = 640,
    scale: float = 185.0,
    perspective: float = 0.22,
) -> tuple[float, float, float]:
    """Project a 3D point ``(x, y, z)`` to ``(sx, sy, depth_z)``."""
    yaw = math.radians(yaw_deg)
    pitch = math.radians(pitch_deg)
    cy, sy_val = math.cos(yaw), math.sin(yaw)
    cp, sp = math.cos(pitch), math.sin(pitch)

    x1 = pt[0] * cy - pt[2] * sy_val
    z1 = pt[0] * sy_val + pt[2] * cy
    y2 = pt[1] * cp - z1 * sp
    z2 = pt[1] * sp + z1 * cp

    fov = 1.0 / max(0.25, 1.0 + perspective * z2 * 0.25)
    s = scale * fov
    return (width * 0.5 + x1 * s, height * 0.52 - y2 * s, z2)


def export_svg_projection(
    scene: Scene3D,
    out_path: Path | None = None,
    yaw_deg: float = 34.0,
    pitch_deg: float = 22.0,
    width: int = 800,
    height: int = 640,
    scale: float = 185.0,
    perspective: float = 0.22,
) -> str:
    """Render a depth-sorted 3D camera projection of ``scene`` to a standalone SVG."""
    drawables: list[tuple[float, str]] = []

    for pg in scene.polygons:
        proj_verts = [
            project_point(v, yaw_deg, pitch_deg, width, height, scale, perspective)
            for v in pg.vertices
        ]
        avg_z = sum(p[2] for p in proj_verts) / max(1, len(proj_verts))
        col = PALETTE.get(pg.role, PALETTE["zero"])
        pts_attr = " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in proj_verts)
        svg_el = (
            f'  <polygon points="{pts_attr}" fill="{col}" fill-opacity="{pg.opacity:.2f}" '
            f'stroke="{col}" stroke-opacity="0.55" stroke-width="1.1"/>'
        )
        drawables.append((avg_z, svg_el))

    for pl in scene.polylines:
        proj_pts = [
            project_point(v, yaw_deg, pitch_deg, width, height, scale, perspective)
            for v in pl.points
        ]
        avg_z = sum(p[2] for p in proj_pts) / max(1, len(proj_pts))
        col = PALETTE.get(pl.role, PALETTE["frame"])
        pts_attr = " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in proj_pts)
        dash = ' stroke-dasharray="5,4"' if pl.dashed else ""
        tag = "polygon" if pl.closed else "polyline"
        svg_el = (
            f'  <{tag} points="{pts_attr}" fill="none" stroke="{col}" '
            f'stroke-width="{pl.width:.2f}"{dash} stroke-linecap="round" stroke-linejoin="round"/>'
        )
        drawables.append((avg_z, svg_el))

    for nd in scene.nodes:
        sx, sy, sz = project_point(nd.position, yaw_deg, pitch_deg, width, height, scale, perspective)
        col = PALETTE.get(nd.role, PALETTE["zero"])
        fill_col = col if nd.role == "amplitude" else "#121621"
        txt_col = "#0c0e14" if nd.role == "amplitude" else col
        r = nd.radius
        lbl = escape(nd.label)
        node_svg = (
            f'  <g>\n'
            f'    <circle cx="{sx:.1f}" cy="{sy:.1f}" r="{r:.1f}" fill="{fill_col}" stroke="{col}" stroke-width="1.8"/>\n'
            f'    <text x="{sx:.1f}" y="{sy + r + 12:.1f}" text-anchor="middle" fill="{txt_col}" '
            f'font-family="Fira Sans Condensed, Inter, sans-serif" font-size="10" font-weight="700">{lbl}</text>\n'
            f'  </g>'
        )
        drawables.append((sz - 0.02, node_svg))

    # Painter's sort: draw farthest (+z2) first, nearest (-z2) last
    drawables.sort(key=lambda item: item[0], reverse=True)

    header = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">\n'
        f'  <rect width="{width}" height="{height}" fill="#0c0e14"/>\n'
        f'  <text x="{width / 2:.1f}" y="30" text-anchor="middle" fill="#e8b85a" '
        f'font-family="Fira Sans Condensed, Inter, sans-serif" font-size="16" font-weight="800" letter-spacing="1.2">'
        f'{escape(scene.title.upper())}</text>\n'
        f'  <text x="{width / 2:.1f}" y="48" text-anchor="middle" fill="#949eb0" '
        f'font-family="Fira Sans Condensed, Inter, sans-serif" font-size="11">{escape(scene.figures)}</text>'
    )
    svg_text = "\n".join([header, *(el for _, el in drawables), "</svg>\n"])
    if out_path is not None:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(svg_text, encoding="utf-8")
    return svg_text
