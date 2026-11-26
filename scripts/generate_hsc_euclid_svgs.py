"""Generate Phase B paired Ink-to-Vector .euclid-graphic SVGs for Home Study Course plates."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from pathlib import Path

HSC_DIR = Path(__file__).resolve().parent.parent / "docsrc" / "home_study_course"

STYLE_CSS = """\
    :root {
      --geom-fg: #18181b;
      --geom-bg: #ffffff;
      --geom-point-stroke: #ffffff;
      --geom-poly-fill: #000000;
      --geom-accent: #c88a1e;
      --geom-assert: #16a34a;
      --geom-pos: #e11d48;
      --geom-neg: #0284c7;
    }
    @media (prefers-color-scheme: dark) {
      :root {
        --geom-fg: #ebe6dc;
        --geom-bg: #0c0e14;
        --geom-point-stroke: #0c0e14;
        --geom-poly-fill: #ebe6dc;
        --geom-accent: #e8b85a;
        --geom-assert: #5ec27e;
        --geom-pos: #fb7185;
        --geom-neg: #38bdf8;
      }
    }
    .euclid-graphic {
      font-family: 'Fira Sans Condensed', 'Fira Sans', 'DejaVu Sans', sans-serif;
      font-style: normal;
      font-weight: 700;
      background-color: var(--geom-bg);
    }
    .geom-line {
      stroke: var(--geom-fg);
      stroke-width: 1.8;
      stroke-linecap: round;
      stroke-linejoin: round;
      fill: none;
      transition: stroke 0.15s, stroke-width 0.15s;
    }
    .geom-bold {
      stroke: var(--geom-fg);
      stroke-width: 2.3;
      stroke-linecap: round;
      stroke-linejoin: round;
      fill: none;
      transition: stroke 0.15s, stroke-width 0.15s;
    }
    .geom-circle, .geom-curve, .geom-ellipse {
      stroke: var(--geom-fg);
      stroke-width: 1.8;
      stroke-linecap: round;
      stroke-linejoin: round;
      fill: none;
      transition: stroke 0.15s, stroke-width 0.15s;
    }
    .geom-arc {
      stroke: var(--geom-fg);
      stroke-width: 1.6;
      stroke-linecap: round;
      fill: none;
      transition: stroke 0.15s, stroke-width 0.15s;
    }
    .geom-dashed, .geom-aux, .geom-construction {
      stroke: var(--geom-fg);
      stroke-width: 1.4;
      stroke-dasharray: 5, 3.5;
      stroke-linecap: round;
      stroke-linejoin: round;
      fill: none;
      opacity: 0.78;
      transition: stroke 0.15s, stroke-width 0.15s;
    }
    .geom-ray {
      stroke: var(--geom-fg);
      stroke-width: 1.3;
      stroke-linecap: round;
      fill: none;
      opacity: 0.82;
      transition: stroke 0.15s, stroke-width 0.15s;
    }
    .geom-zero {
      stroke: var(--geom-accent);
      stroke-width: 2.0;
      stroke-linecap: round;
      fill: none;
    }
    .geom-zero-dashed {
      stroke: var(--geom-accent);
      stroke-width: 1.5;
      stroke-dasharray: 5, 4;
      stroke-linecap: round;
      fill: none;
    }
    .geom-pos {
      stroke: var(--geom-pos);
      stroke-width: 2.0;
      stroke-linecap: round;
      fill: none;
    }
    .geom-neg {
      stroke: var(--geom-neg);
      stroke-width: 2.0;
      stroke-linecap: round;
      fill: none;
    }
    .geom-neg-dashed {
      stroke: var(--geom-neg);
      stroke-width: 1.6;
      stroke-dasharray: 5, 3.5;
      stroke-linecap: round;
      fill: none;
    }
    .geom-tick-mark {
      stroke: var(--geom-assert);
      stroke-width: 2;
      stroke-linecap: round;
      fill: none;
    }
    .geom-ang-arc {
      fill: none;
      stroke: var(--geom-assert);
      stroke-width: 2.2;
      stroke-linecap: round;
    }
    .geom-polygon {
      fill: var(--geom-poly-fill);
      fill-opacity: 0.05;
      stroke: none;
      transition: fill-opacity 0.15s, stroke 0.15s;
    }
    .geom-polygon-stroked {
      fill: var(--geom-poly-fill);
      fill-opacity: 0.06;
      stroke: var(--geom-fg);
      stroke-width: 1.7;
      stroke-linecap: round;
      stroke-linejoin: round;
      transition: fill-opacity 0.15s, stroke 0.15s;
    }
    .geom-zero-plane {
      fill: var(--geom-accent);
      fill-opacity: 0.12;
      stroke: var(--geom-accent);
      stroke-width: 1.5;
    }
    .geom-pos-fill {
      fill: var(--geom-pos);
      fill-opacity: 0.12;
      stroke: var(--geom-pos);
      stroke-width: 1.6;
    }
    .geom-neg-fill {
      fill: var(--geom-neg);
      fill-opacity: 0.12;
      stroke: var(--geom-neg);
      stroke-width: 1.6;
    }
    .wedge, .angle {
      fill: var(--geom-accent);
      fill-opacity: 0.24;
      stroke: var(--geom-accent);
      stroke-width: 2;
      stroke-linejoin: round;
    }
    .geom-point {
      fill: var(--geom-fg);
      stroke: var(--geom-point-stroke);
      stroke-width: 1.2;
      transition: fill 0.15s, r 0.15s;
    }
    .geom-dot {
      fill: var(--geom-fg);
      stroke: none;
    }
    .geom-point-zero {
      fill: var(--geom-bg);
      stroke: var(--geom-accent);
      stroke-width: 2.1;
    }
    .geom-point-pos {
      fill: var(--geom-bg);
      stroke: var(--geom-pos);
      stroke-width: 2.1;
    }
    .geom-point-neg {
      fill: var(--geom-bg);
      stroke: var(--geom-neg);
      stroke-width: 2.1;
    }
    .geom-label {
      font-family: 'Fira Sans Condensed', 'Fira Sans', 'DejaVu Sans', sans-serif;
      font-size: 13px;
      font-weight: 700;
      fill: var(--geom-fg);
      user-select: none;
    }
    .geom-label-sm {
      font-family: 'Fira Sans Condensed', 'Fira Sans', 'DejaVu Sans', sans-serif;
      font-size: 10.5px;
      font-weight: 700;
      fill: var(--geom-fg);
      user-select: none;
    }
    .geom-label-title {
      font-family: 'Fira Sans Condensed', 'Fira Sans', 'DejaVu Sans', sans-serif;
      font-size: 14px;
      font-weight: 700;
      letter-spacing: 0.8px;
      fill: var(--geom-accent);
      text-anchor: middle;
      user-select: none;
    }
    .geom-overlay {
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.12s ease;
    }
    [data-ref]:hover, .highlight, .geom-highlight-active {
      opacity: 1 !important;
      stroke: var(--geom-accent) !important;
      cursor: pointer;
    }
    text[data-ref]:hover, text.highlight, text.geom-highlight-active {
      opacity: 1 !important;
      fill: var(--geom-accent) !important;
      stroke: none !important;
    }
    .geom-polygon:hover, .geom-polygon-stroked:hover, polygon.geom-highlight-active {
      opacity: 1 !important;
      fill-opacity: 0.24 !important;
      fill: var(--geom-accent) !important;
      stroke: var(--geom-accent) !important;
    }
    .geom-point:hover, circle.geom-point.geom-highlight-active {
      opacity: 1 !important;
      fill: var(--geom-accent) !important;
      stroke: none !important;
    }
    .geom-assert-active {
      opacity: 1 !important;
      stroke: var(--geom-assert) !important;
    }
    text.geom-assert-active {
      opacity: 1 !important;
      fill: var(--geom-assert) !important;
      stroke: none !important;
    }
    path.geom-assert-active.geom-tick-1 { marker-mid: url(#geom-tick-1); }
    path.geom-assert-active.geom-tick-2 { marker-mid: url(#geom-tick-2); }
    path.geom-assert-active.geom-tick-3 { marker-mid: url(#geom-tick-3); }"""


def _esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _mid_d(x1: float, y1: float, x2: float, y2: float) -> str:
    mx = (x1 + x2) / 2.0
    my = (y1 + y2) / 2.0
    return f"M {x1:.2f} {y1:.2f} L {mx:.2f} {my:.2f} L {x2:.2f} {y2:.2f}"


@dataclass
class EuclidSvgBuilder:
    """Builder for .euclid-graphic compliant SVGs."""

    folio: str
    width: int
    height: int
    title: str
    desc: str
    elements: list[str] = field(default_factory=list)
    graphics: list[str] = field(default_factory=list)
    highlights: list[str] = field(default_factory=list)
    points: list[str] = field(default_factory=list)
    labels: list[str] = field(default_factory=list)

    def add_seg(
        self,
        group: list[str],
        el_id: str,
        ref: str,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        cls: str = "geom-line",
        extra: str = "",
    ) -> None:
        d = _mid_d(x1, y1, x2, y2)
        attr = f" {extra}" if extra else ""
        group.append(
            f'    <path id="{_esc(el_id)}" data-ref="{_esc(ref)}" class="{cls}" d="{d}"{attr} />'
        )
        if group is self.graphics:
            self.highlights.append(
                f'    <path id="hl-{_esc(el_id)}" data-ref="{_esc(ref)}" class="geom-line geom-overlay" d="{d}" />'
            )

    def add_path(
        self,
        group: list[str],
        el_id: str,
        ref: str,
        d: str,
        cls: str = "geom-curve",
        extra: str = "",
    ) -> None:
        attr = f" {extra}" if extra else ""
        group.append(
            f'    <path id="{_esc(el_id)}" data-ref="{_esc(ref)}" class="{cls}" d="{d}"{attr} />'
        )

    def add_circle(
        self,
        group: list[str],
        el_id: str,
        ref: str,
        cx: float,
        cy: float,
        r: float,
        cls: str = "geom-circle",
        extra: str = "",
    ) -> None:
        attr = f" {extra}" if extra else ""
        group.append(
            f'    <circle id="{_esc(el_id)}" data-ref="{_esc(ref)}" class="{cls}" cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}"{attr} />'
        )

    def add_ellipse(
        self,
        group: list[str],
        el_id: str,
        ref: str,
        cx: float,
        cy: float,
        rx: float,
        ry: float,
        cls: str = "geom-ellipse",
        extra: str = "",
    ) -> None:
        attr = f" {extra}" if extra else ""
        group.append(
            f'    <ellipse id="{_esc(el_id)}" data-ref="{_esc(ref)}" class="{cls}" cx="{cx:.2f}" cy="{cy:.2f}" rx="{rx:.2f}" ry="{ry:.2f}"{attr} />'
        )

    def add_polygon(
        self,
        group: list[str],
        el_id: str,
        ref: str,
        pts: list[tuple[float, float]],
        cls: str = "geom-polygon-stroked",
    ) -> None:
        pts_s = " ".join(f"{x:.2f},{y:.2f}" for x, y in pts)
        group.append(
            f'    <polygon id="{_esc(el_id)}" data-ref="{_esc(ref)}" class="{cls}" points="{pts_s}" />'
        )

    def add_point(
        self,
        pt_id: str,
        cx: float,
        cy: float,
        r: float = 3.5,
        cls: str = "geom-point",
    ) -> None:
        self.points.append(
            f'    <circle id="{_esc(pt_id)}" data-ref="{_esc(pt_id)}" class="{cls}" cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" />'
        )

    def add_label(
        self,
        lbl_id: str,
        ref: str,
        x: float,
        y: float,
        text: str,
        cls: str = "geom-label",
        anchor: str = "middle",
        extra: str = "",
    ) -> None:
        attr = f" {extra}" if extra else ""
        self.labels.append(
            f'    <text id="label-{_esc(lbl_id)}" data-ref="{_esc(ref)}" class="{cls}" x="{x:.2f}" y="{y:.2f}" text-anchor="{anchor}"{attr}>{_esc(text)}</text>'
        )

    def add_frame(self, title_text: str | None = None) -> None:
        w, h = self.width, self.height
        self.add_seg(self.elements, "frame-top", "[ F1 F2 ]", 10, 10, w - 10, 10, "geom-line")
        self.add_seg(self.elements, "frame-right", "[ F2 F3 ]", w - 10, 10, w - 10, h - 10, "geom-line")
        self.add_seg(self.elements, "frame-bottom", "[ F3 F4 ]", w - 10, h - 10, 10, h - 10, "geom-line")
        self.add_seg(self.elements, "frame-left", "[ F4 F1 ]", 10, h - 10, 10, 10, "geom-line")
        if title_text:
            self.add_label("title", "O", w / 2, 32, title_text, cls="geom-label-title")

    def render(self) -> str:
        return "\n".join(
            [
                '<?xml version="1.0" encoding="UTF-8"?>',
                f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" width="{self.width}" height="{self.height}" class="euclid-graphic" data-graphic-id="{self.folio}.g1" data-folio="{self.folio}" data-graphic="g1">',
                f"  <title>{_esc(self.title)}</title>",
                f"  <desc>{_esc(self.desc)}</desc>",
                "  <style>",
                STYLE_CSS,
                "  </style>",
                "  <defs>",
                '    <marker id="geom-tick-1" viewBox="-6 -6 12 12" refX="0" refY="0" markerWidth="12" markerHeight="12" markerUnits="userSpaceOnUse" orient="auto">',
                '      <line x1="0" y1="-4.5" x2="0" y2="4.5" class="geom-tick-mark" />',
                "    </marker>",
                '    <marker id="geom-tick-2" viewBox="-6 -6 12 12" refX="0" refY="0" markerWidth="12" markerHeight="12" markerUnits="userSpaceOnUse" orient="auto">',
                '      <line x1="-1.8" y1="-4.5" x2="-1.8" y2="4.5" class="geom-tick-mark" />',
                '      <line x1="1.8" y1="-4.5" x2="1.8" y2="4.5" class="geom-tick-mark" />',
                "    </marker>",
                '    <marker id="geom-tick-3" viewBox="-6 -6 12 12" refX="0" refY="0" markerWidth="12" markerHeight="12" markerUnits="userSpaceOnUse" orient="auto">',
                '      <line x1="-3.2" y1="-4.5" x2="-3.2" y2="4.5" class="geom-tick-mark" />',
                '      <line x1="0" y1="-4.5" x2="0" y2="4.5" class="geom-tick-mark" />',
                '      <line x1="3.2" y1="-4.5" x2="3.2" y2="4.5" class="geom-tick-mark" />',
                "    </marker>",
                '    <marker id="geom-arrow" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">',
                '      <path d="M 0 1.5 L 8.5 5 L 0 8.5 z" fill="var(--geom-fg)" />',
                "    </marker>",
                '    <marker id="geom-arrow-pos" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">',
                '      <path d="M 0 1.5 L 8.5 5 L 0 8.5 z" fill="var(--geom-pos)" />',
                "    </marker>",
                '    <marker id="geom-arrow-neg" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">',
                '      <path d="M 0 1.5 L 8.5 5 L 0 8.5 z" fill="var(--geom-neg)" />',
                "    </marker>",
                "  </defs>",
                '  <g id="elements">',
                *self.elements,
                "  </g>",
                '  <g id="graphics">',
                *self.graphics,
                "  </g>",
                '  <g id="highlights" style="pointer-events: none;">',
                *self.highlights,
                "  </g>",
                '  <g id="points">',
                *self.points,
                "  </g>",
                '  <g id="labels">',
                *self.labels,
                "  </g>",
                "</svg>",
                "",
            ]
        )


def _sine_d(
    x0: float, y0: float, width: float, amp: float, cycles: float = 1.0, steps: int = 80, phase: float = 0.0
) -> str:
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = x0 + t * width
        y = y0 - amp * math.sin(2.0 * math.pi * cycles * t + phase)
        pts.append(f"{'M' if i == 0 else 'L'} {x:.2f} {y:.2f}")
    return " ".join(pts)


def _spiral_d(
    cx: float, cy: float, r_start: float, r_end: float, turns: float, steps: int = 160, cw: bool = True, angle0: float = 0.0
) -> str:
    pts = []
    sign = 1.0 if cw else -1.0
    for i in range(steps + 1):
        t = i / steps
        ang = angle0 + sign * 2.0 * math.pi * turns * t
        r = r_start + (r_end - r_start) * t
        x = cx + r * math.cos(ang)
        y = cy + r * math.sin(ang)
        pts.append(f"{'M' if i == 0 else 'L'} {x:.2f} {y:.2f}")
    return " ".join(pts)


def _cone_helix_d(
    apex_x: float, apex_y: float, base_x: float, base_y: float, base_rx: float, base_ry: float, turns: float = 6.0, steps: int = 180
) -> str:
    pts = []
    for i in range(steps + 1):
        t = i / steps
        cx = apex_x + (base_x - apex_x) * t
        cy = apex_y + (base_y - apex_y) * t
        rx = base_rx * t
        ry = base_ry * t
        ang = 2.0 * math.pi * turns * t
        x = cx + rx * math.cos(ang)
        y = cy + ry * math.sin(ang)
        pts.append(f"{'M' if i == 0 else 'L'} {x:.2f} {y:.2f}")
    return " ".join(pts)


def build_0002() -> EuclidSvgBuilder:
    b = EuclidSvgBuilder(
        "0002", 620, 620,
        "The Cosmic Clock Emblem (Folio 0002)",
        "Circular octave dial showing 0-1-2-3-4-3-2-1-0 spectrum rings and 16 sunburst rays.",
    )
    cx, cy = 310.0, 310.0
    radii = [48, 86, 128, 174, 236]
    for idx, r in enumerate(radii):
        cls = "geom-zero" if idx in (1, 3) else "geom-circle"
        b.add_circle(b.graphics, f"ring-{idx}", f"( O R{idx} )", cx, cy, r, cls=cls)
    # 16 sunburst spikes & radial dividers
    for i in range(16):
        ang = math.radians(i * 22.5 - 90)
        x1, y1 = cx + 128 * math.cos(ang), cy + 128 * math.sin(ang)
        x2, y2 = cx + 236 * math.cos(ang), cy + 236 * math.sin(ang)
        b.add_seg(b.elements, f"ray-{i}", f"[ O S{i} ]", x1, y1, x2, y2, "geom-ray")
        a1, a2 = ang - 0.055, ang + 0.055
        sx, sy = cx + 278 * math.cos(ang), cy + 278 * math.sin(ang)
        bx1, by1 = cx + 236 * math.cos(a1), cy + 236 * math.sin(a1)
        bx2, by2 = cx + 236 * math.cos(a2), cy + 236 * math.sin(a2)
        b.add_polygon(b.graphics, f"spike-{i}", f"< S{i} B{i} C{i} >", [(bx1, by1), (sx, sy), (bx2, by2)], "geom-polygon-stroked")
    # Inner spiral & clock hands
    b.add_path(b.graphics, "inner-spiral", "( O S )", _spiral_d(cx, cy, 6, 40, 3.0, cw=True), "geom-curve")
    b.add_seg(b.graphics, "hand-1", "/ O H1 /", cx, cy, cx + 32, cy - 26, "geom-bold", 'marker-end="url(#geom-arrow)"')
    b.add_seg(b.graphics, "hand-2", "/ O H2 /", cx, cy, cx - 26, cy - 22, "geom-bold")
    # Octave digits 0-1-2-3-4-3-2-1-0 around inner ring
    nums = ["0", "1", "2", "3", "4", "3", "2", "1", "0", "1", "2", "3", "4", "3", "2", "1"]
    for i, num in enumerate(nums):
        ang = math.radians(i * 22.5 - 90)
        lx, ly = cx + 67 * math.cos(ang), cy + 67 * math.sin(ang) + 4
        b.add_label(f"n{i}", f"N{i}", lx, ly, num, "geom-label-sm")
    colors = [
        (0, "ULTRA-VIOLET"), (22.5, "BLUE"), (45, "GREEN"), (67.5, "YELLOW"),
        (90, "ORANGE"), (112.5, "RED"), (135, "INFRA-RED"), (180, "ULTRA-VIOLET"),
        (202.5, "VIOLET"), (225, "BLUE"), (247.5, "GREEN"), (270, "YELLOW"),
        (292.5, "ORANGE"), (315, "RED"), (337.5, "INFRA-RED"),
    ]
    for i, (deg, txt) in enumerate(colors):
        ang = math.radians(deg - 90)
        lx, ly = cx + 204 * math.cos(ang), cy + 204 * math.sin(ang) + 4
        b.add_label(f"col-{i}", f"C{i}", lx, ly, txt, "geom-label-sm")
    b.add_label("cosmic", "O", cx, cy - 102, "THE COSMIC CLOCK", "geom-label-title")
    b.add_point("O", cx, cy, 4.0, "geom-point-zero")
    return b


def build_0040() -> EuclidSvgBuilder:
    b = EuclidSvgBuilder(
        "0040", 520, 460,
        "Figure 5 — Concentration and Decentration",
        "Radial dashed cone diverging from concentration apex through two concentric pressure arcs.",
    )
    ox, oy = 260.0, 355.0
    b.add_point("O", ox, oy, 4.0, "geom-point-pos")
    for idx, deg in enumerate([-132, -116, -100, -90, -80, -64, -48]):
        rad = math.radians(deg)
        x2, y2 = ox + 300 * math.cos(rad), oy + 300 * math.sin(rad)
        b.add_seg(b.elements, f"ray-{idx}", f"[ O R{idx} ]", ox, oy, x2, y2, "geom-dashed")
    for idx, r in enumerate([165.0, 210.0]):
        a1, a2 = math.radians(-135), math.radians(-45)
        x1, y1 = ox + r * math.cos(a1), oy + r * math.sin(a1)
        x2, y2 = ox + r * math.cos(a2), oy + r * math.sin(a2)
        b.add_path(b.graphics, f"arc-{idx}", f"( O A{idx} )", f"M {x1:.2f} {y1:.2f} A {r:.2f} {r:.2f} 0 0 1 {x2:.2f} {y2:.2f}", "geom-bold")
        b.add_point(f"P{idx}L", x1, y1, 3.0)
        b.add_point(f"P{idx}R", x2, y2, 3.0)
    b.add_seg(b.graphics, "band-l", "/ P0L P1L /", ox + 165 * math.cos(math.radians(-135)), oy + 165 * math.sin(math.radians(-135)), ox + 210 * math.cos(math.radians(-135)), oy + 210 * math.sin(math.radians(-135)), "geom-bold")
    b.add_seg(b.graphics, "band-r", "/ P0R P1R /", ox + 165 * math.cos(math.radians(-45)), oy + 165 * math.sin(math.radians(-45)), ox + 210 * math.cos(math.radians(-45)), oy + 210 * math.sin(math.radians(-45)), "geom-bold")
    b.add_label("dec", "D", ox, 95, "DECENTRATION", "geom-label")
    b.add_label("conc", "O", ox, 395, "CONCENTRATION", "geom-label")
    b.add_label("fig", "O", ox, 435, "Fig. 5", "geom-label-title")
    return b


def build_0064() -> EuclidSvgBuilder:
    b = EuclidSvgBuilder(
        "0064", 680, 340,
        "Figure 6 — The Heartbeat of the Universe",
        "Symmetric octave heartbeat axis 0-1-2-3-4-0-4-3-2-1-0 dividing positive generation from negative disintegration.",
    )
    b.add_frame("THE HEARTBEAT OF THE UNIVERSE")
    b.add_seg(b.elements, "mid-div", "[ M1 M2 ]", 340, 56, 340, 275, "geom-zero-dashed")
    b.add_seg(b.graphics, "axis-pos", "/ Z0 Z4 /", 52, 165, 340, 165, "geom-pos")
    b.add_seg(b.graphics, "axis-neg", "/ Z4 Z8 /", 340, 165, 628, 165, "geom-neg")
    labels_seq = ["0", "1", "2", "3", "4", "0", "4", "3", "2", "1", "0"]
    for i, val in enumerate(labels_seq):
        x = 52 + i * 57.6
        cls = "geom-point-zero" if val == "0" else ("geom-point-pos" if i < 5 else "geom-point-neg")
        b.add_point(f"N{i}", x, 165, 9.0, cls)
        b.add_label(f"n{i}", f"N{i}", x, 169, val, "geom-label-sm")
    b.add_label("pos-h", "N2", 196, 108, "POSITIVE", "geom-label")
    b.add_label("neg-h", "N8", 484, 108, "NEGATIVE", "geom-label")
    b.add_label("pos-d1", "N2", 196, 215, "GENERATION OF ENERGY", "geom-label-sm")
    b.add_label("pos-d2", "N2", 196, 232, "TOWARD LIFE AND GROWTH", "geom-label-sm")
    b.add_label("neg-d1", "N8", 484, 215, "DISINTEGRATION OF ENERGY", "geom-label-sm")
    b.add_label("neg-d2", "N8", 484, 232, "TOWARD DECAY AND DEATH", "geom-label-sm")
    b.add_label("fig6", "N5", 340, 312, "Fig. 6", "geom-label-title")
    return b


def build_0103() -> EuclidSvgBuilder:
    b = EuclidSvgBuilder(
        "0103", 580, 580,
        "Radial North-South Equal Pressure Sphere (Folio 0103)",
        "Central North (+) hub radiating eight South (-) vectors surrounded by concentric East-West rings of equal pressure.",
    )
    b.add_frame()
    cx, cy = 290.0, 285.0
    b.add_circle(b.graphics, "ring-outer", "( O R3 )", cx, cy, 222, "geom-circle")
    b.add_circle(b.graphics, "ring-mid", "( O R2 )", cx, cy, 198, "geom-circle")
    b.add_circle(b.graphics, "ring-corona", "( O R1 )", cx, cy, 86, "geom-dashed")
    b.add_circle(b.graphics, "hub", "( O R0 )", cx, cy, 52, "geom-pos-fill")
    for i in range(8):
        ang = math.radians(i * 45 - 90)
        x1, y1 = cx + 52 * math.cos(ang), cy + 52 * math.sin(ang)
        x2, y2 = cx + 178 * math.cos(ang), cy + 178 * math.sin(ang)
        b.add_seg(b.graphics, f"vec-{i}", f"/ O S{i} /", x1, y1, x2, y2, "geom-neg", 'marker-end="url(#geom-arrow-neg)"')
        b.add_label(f"s-{i}", f"S{i}", cx + 190 * math.cos(ang), cy + 190 * math.sin(ang) + 4, "S", "geom-label-sm")
    b.add_point("O", cx, cy, 5.0, "geom-point-pos")
    b.add_label("N-hub", "O", cx, cy + 5, "N", "geom-label")
    b.add_label("bot-l", "O", 110, 540, "N MEANS NORTH +", "geom-label-sm")
    b.add_label("bot-r", "O", 470, 540, "S MEANS SOUTH -", "geom-label-sm")
    b.add_label("eq-lbl", "O", 290, 558, "THE CHANGELESS DIRECTION OF EQUAL PRESSURES", "geom-label-sm")
    return b


def build_0131() -> EuclidSvgBuilder:
    b = EuclidSvgBuilder(
        "0131", 560, 400,
        "Figure 18 — Undivided Equilibrium in a Closed Room",
        "Perspective box representing undivided stillness with zero thermal division.",
    )
    b.add_frame()
    # Outer rectangle F1-F4, inner back wall B1-B4
    f = [(60, 50), (500, 50), (500, 320), (60, 320)]
    bk = [(135, 100), (425, 100), (425, 270), (135, 270)]
    for i in range(4):
        j = (i + 1) % 4
        b.add_seg(b.graphics, f"front-{i}", f"/ F{i} F{j} /", *f[i], *f[j], "geom-bold")
        b.add_seg(b.graphics, f"back-{i}", f"/ B{i} B{j} /", *bk[i], *bk[j], "geom-line")
        b.add_seg(b.graphics, f"edge-{i}", f"/ F{i} B{i} /", *f[i], *bk[i], "geom-line")
        b.add_point(f"F{i}", *f[i], 3.0)
        b.add_point(f"B{i}", *bk[i], 3.0)
    # Windows on back wall
    for idx, wx in enumerate([175, 320]):
        pts = [(wx, 130), (wx + 55, 130), (wx + 55, 205), (wx, 205)]
        b.add_polygon(b.elements, f"win-{idx}", f"< W{idx} >", pts, "geom-polygon-stroked")
    # Door on left wall
    b.add_polygon(b.elements, "door", "< D0 >", [(82, 115), (112, 130), (112, 285), (82, 305)], "geom-polygon-stroked")
    b.add_label("undiv", "B0", 280, 362, "UNDIVIDED", "geom-label-title")
    return b


def build_0132() -> EuclidSvgBuilder:
    b = EuclidSvgBuilder(
        "0132", 560, 400,
        "Figure 19 — Divided Thermal Polarity Across an Equator",
        "Perspective room bisected by a vertical equator plane separating cold and hot poles.",
    )
    b.add_frame()
    f = [(60, 50), (500, 50), (500, 320), (60, 320)]
    bk = [(135, 100), (425, 100), (425, 270), (135, 270)]
    for i in range(4):
        j = (i + 1) % 4
        b.add_seg(b.graphics, f"front-{i}", f"/ F{i} F{j} /", *f[i], *f[j], "geom-bold")
        b.add_seg(b.graphics, f"back-{i}", f"/ B{i} B{j} /", *bk[i], *bk[j], "geom-line")
        b.add_seg(b.graphics, f"edge-{i}", f"/ F{i} B{i} /", *f[i], *bk[i], "geom-line")
        b.add_point(f"F{i}", *f[i], 3.0)
        b.add_point(f"B{i}", *bk[i], 3.0)
    # Central dividing EQUATOR line
    b.add_seg(b.graphics, "equator", "/ E1 E2 /", 280, 30, 280, 335, "geom-zero")
    b.add_point("E1", 280, 30, 3.5, "geom-point-zero")
    b.add_point("E2", 280, 335, 3.5, "geom-point-zero")
    b.add_circle(b.graphics, "cold-node", "( C0 R )", 125, 225, 14, "geom-neg-fill")
    b.add_circle(b.graphics, "hot-node", "( H0 R )", 435, 225, 18, "geom-pos-fill")
    b.add_point("C0", 125, 225, 3.5, "geom-point-neg")
    b.add_point("H0", 435, 225, 3.5, "geom-point-pos")
    b.add_label("eq-lbl", "E1", 268, 185, "EQUATOR", "geom-label-sm", extra='transform="rotate(-90 268 185)"')
    b.add_label("div", "E2", 280, 368, "DIVIDED", "geom-label-title")
    return b


def build_0136() -> EuclidSvgBuilder:
    b = EuclidSvgBuilder(
        "0136", 640, 400,
        "Figure 22 — Life and Death Exemplified in the Divine Trinity",
        "Catenary wave of expanding circles across a central sphere on the vertical equator.",
    )
    b.add_frame("LIFE AND DEATH MEET AS EQUALS AT THEIR EQUATOR")
    b.add_seg(b.elements, "eq-axis", "[ E1 E2 ]", 320, 48, 320, 365, "geom-zero-dashed")
    # Catenary curve y = 265 - 75 * ((x-320)/270)^2
    pts = []
    for i in range(61):
        t = -1.0 + 2.0 * i / 60.0
        x = 320.0 + 270.0 * t
        y = 260.0 - 78.0 * (t * t)
        pts.append(f"{'M' if i == 0 else 'L'} {x:.2f} {y:.2f}")
    b.add_path(b.graphics, "catenary", "/ L0 D0 /", " ".join(pts), "geom-bold")
    # Expanding circles along the catenary
    for i in range(17):
        t = -0.95 + 1.9 * i / 16.0
        x = 320.0 + 260.0 * t
        y = 260.0 - 78.0 * (t * t)
        r = 7.0 + (i * 3.8)
        cls = "geom-pos" if t < 0 else "geom-neg"
        b.add_circle(b.graphics, f"c-{i}", f"( P{i} R{i} )", x, y, r, cls)
    b.add_circle(b.graphics, "center-sphere", "( O R )", 320, 260, 26, "geom-zero-plane")
    b.add_point("O", 320, 260, 4.5, "geom-point-zero")
    b.add_label("life", "O", 85, 160, "+ LIFE", "geom-label")
    b.add_label("death", "O", 555, 160, "DEATH -", "geom-label")
    b.add_label("bot-l", "O", 165, 360, "LIFE CONCENTRATES", "geom-label-sm")
    b.add_label("bot-r", "O", 475, 360, "LIFE DECENTRATES", "geom-label-sm")
    return b


def build_0146() -> EuclidSvgBuilder:
    b = EuclidSvgBuilder(
        "0146", 580, 620,
        "Figure 25 — Pull of Gravitation and Thrust of Radiation",
        "Double logarithmic spiral showing inward centripetal gravitation and outward centrifugal radiation.",
    )
    b.add_frame()
    cx, cy = 290.0, 285.0
    b.add_circle(b.graphics, "core", "( O R0 )", cx, cy, 102, "geom-zero-plane")
    b.add_path(b.graphics, "grav-1", "( O G1 )", _spiral_d(cx, cy, 12, 248, 3.2, cw=True, angle0=0.0), "geom-pos", 'marker-end="url(#geom-arrow-pos)"')
    b.add_path(b.graphics, "rad-1", "( O D1 )", _spiral_d(cx, cy, 12, 248, 3.2, cw=False, angle0=math.pi), "geom-neg-dashed", 'marker-end="url(#geom-arrow-neg)"')
    b.add_point("O", cx, cy, 4.5, "geom-point-zero")
    b.add_label("grav", "O", 180, 445, "PULL OF GRAVITATION", "geom-label")
    b.add_label("rad", "O", 390, 455, "THRUST OF RADIATION", "geom-label")
    b.add_label("fig25", "O", 290, 568, "Fig. 25 — Doubly Charged Spiral", "geom-label-title")
    return b


def build_0162() -> EuclidSvgBuilder:
    b = EuclidSvgBuilder(
        "0162", 720, 640,
        "Figures 28–37 — Principle of the Divine Trinity",
        "Three-tier plate: wave-lever fulcrums (Figs. 28-31), calm/wave ships (32-33), and cube/trinity polarity (34-37).",
    )
    b.add_frame("PRINCIPLE OF THE DIVINE TRINITY (FIGS. 28–37)")
    # Tier 1: Figs 28-31 wave levers
    b.add_seg(b.elements, "t1-div", "[ T1A T1B ]", 20, 215, 700, 215, "geom-line")
    for idx, x0 in enumerate([55, 215, 375, 535]):
        b.add_seg(b.graphics, f"eq-{idx}", f"/ E{idx}A E{idx}B /", x0, 125, x0 + 130, 125, "geom-zero")
        phase = 0.0 if idx < 2 else math.pi
        b.add_path(b.graphics, f"lever-{idx}", f"/ L{idx}A L{idx}B /", _sine_d(x0 + 10, 125, 110, 48, 0.5, 40, phase), "geom-pos" if idx % 2 == 0 else "geom-neg")
        b.add_point(f"F{idx}", x0 + 65, 125, 4.5, "geom-point-zero")
        b.add_label(f"fig-{28 + idx}", f"F{idx}", x0 + 65, 200, f"Fig. {28 + idx}", "geom-label-sm")
    # Tier 2: Figs 32-33 calm vs wave horizon
    b.add_seg(b.elements, "t2-div", "[ T2A T2B ]", 20, 405, 700, 405, "geom-line")
    b.add_seg(b.graphics, "calm-sea", "/ C1 C2 /", 40, 275, 680, 275, "geom-zero")
    b.add_label("fig32", "F0", 360, 305, "Fig. 32 • Calm Zero Plane", "geom-label-sm")
    b.add_path(b.graphics, "wave-sea", "/ W1 W2 /", _sine_d(40, 355, 640, 18, 3.0, 90), "geom-neg")
    b.add_label("fig33", "F0", 360, 392, "Fig. 33 • Wave Oscillation", "geom-label-sm")
    # Tier 3: Figs 34-37 Cube & Trinity
    # Fig 34 Cube
    b.add_polygon(b.graphics, "cube34", "< C1 C2 C3 C4 >", [(75, 465), (135, 465), (135, 525), (75, 525)], "geom-polygon-stroked")
    b.add_label("fig34", "F0", 105, 585, "Fig. 34", "geom-label-sm")
    # Fig 35 Cross of Polarity
    b.add_seg(b.graphics, "c35-h", "/ P35 L35 /", 215, 505, 315, 505, "geom-zero")
    b.add_seg(b.graphics, "c35-v", "/ T35 B35 /", 265, 445, 265, 565, "geom-line")
    b.add_point("P35", 215, 505, 9.0, "geom-point-pos")
    b.add_point("L35", 315, 505, 9.0, "geom-point-neg")
    b.add_point("O35", 265, 505, 9.0, "geom-point-zero")
    b.add_label("fig35", "O35", 265, 585, "Fig. 35", "geom-label-sm")
    # Fig 36 Vertical Shaft
    b.add_seg(b.graphics, "s36", "/ S36A S36B /", 445, 445, 445, 565, "geom-bold")
    b.add_label("fig36", "O35", 445, 585, "Fig. 36", "geom-label-sm")
    # Fig 37 Polarized Lens
    b.add_ellipse(b.graphics, "l37", "( O37 R )", 605, 505, 16, 60, "geom-pos-fill")
    b.add_seg(b.graphics, "h37", "/ H37A H37B /", 565, 505, 645, 505, "geom-zero")
    b.add_label("fig37", "O35", 605, 585, "Fig. 37", "geom-label-sm")
    return b


def build_0175() -> EuclidSvgBuilder:
    b = EuclidSvgBuilder(
        "0175", 740, 620,
        "Figures 38–47 — Cycle of Polarity and Vitality",
        "Growth and decay cycle from seed at rest (Fig. 38) through full double-cone vortex (Fig. 43) back to rest (Fig. 47).",
    )
    b.add_frame("CYCLE OF POLARITY AND VITALITY (FIGS. 38–47)")
    # Top row: 38, 39, 40
    b.add_seg(b.elements, "f38-l", "/ A38 B38 /", 50, 105, 190, 105, "geom-zero-dashed")
    b.add_point("O38", 120, 105, 8.0, "geom-point-zero")
    b.add_label("l38", "O38", 120, 140, "Fig. 38", "geom-label-sm")

    b.add_seg(b.graphics, "f39-l", "/ A39 B39 /", 280, 105, 440, 105, "geom-zero")
    b.add_point("A39", 280, 105, 6.0, "geom-point-zero")
    b.add_point("O39", 360, 105, 8.0, "geom-point-zero")
    b.add_point("B39", 440, 105, 6.0, "geom-point-zero")
    b.add_label("l39", "O39", 360, 140, "Fig. 39", "geom-label-sm")

    b.add_seg(b.graphics, "f40-h", "/ A40 B40 /", 535, 105, 685, 105, "geom-zero")
    b.add_seg(b.graphics, "f40-v", "/ P40 N40 /", 610, 55, 610, 155, "geom-pos", 'marker-start="url(#geom-arrow-neg)" marker-end="url(#geom-arrow-pos)"')
    b.add_point("O40", 610, 105, 7.0, "geom-point-zero")
    b.add_label("l40", "O40", 610, 178, "Fig. 40", "geom-label-sm")

    # Middle row: 41-44
    for idx, cx in enumerate([125, 250, 395, 590]):
        if idx == 1:
            b.add_polygon(b.graphics, "f42-bar", "< B42 >", [(cx - 12, 225), (cx + 12, 225), (cx + 12, 395), (cx - 12, 395)], "geom-zero-plane")
            b.add_point("O42", cx, 310, 7.0, "geom-point-zero")
            b.add_label("l42", "O42", cx, 420, "Fig. 42", "geom-label-sm")
        else:
            b.add_seg(b.elements, f"d-{idx}-1", f"/ D{idx}A D{idx}B /", cx - 75, 225, cx + 75, 395, "geom-dashed")
            b.add_seg(b.elements, f"d-{idx}-2", f"/ D{idx}C D{idx}D /", cx + 75, 225, cx - 75, 395, "geom-dashed")
            b.add_seg(b.graphics, f"eq-{idx}", f"/ E{idx}A E{idx}B /", cx - 75, 310, cx + 75, 310, "geom-zero")
            if idx == 2:
                b.add_polygon(b.graphics, "vortex43", "< V1 V2 V3 V4 >", [(cx, 225), (cx + 72, 310), (cx, 395), (cx - 72, 310)], "geom-pos-fill")
                b.add_path(b.graphics, "spiral43", "( O43 S )", _cone_helix_d(cx, 225, cx, 310, 68, 14, 5.0, 120), "geom-neg")
            b.add_point(f"O{41 + idx}", cx, 310, 7.0, "geom-point-zero")
            b.add_label(f"l{41 + idx}", f"O{41 + idx}", cx, 420, f"Fig. {41 + idx}", "geom-label-sm")

    # Bottom row: 45, 46, 47
    b.add_polygon(b.graphics, "v45", "< V45 >", [(155, 475), (245, 520), (155, 565), (65, 520)], "geom-pos-fill")
    b.add_label("l45", "O38", 155, 590, "Fig. 45", "geom-label-sm")
    b.add_polygon(b.graphics, "v46", "< V46 >", [(370, 500), (465, 520), (370, 540), (275, 520)], "geom-neg-fill")
    b.add_label("l46", "O38", 370, 590, "Fig. 46", "geom-label-sm")
    b.add_seg(b.elements, "f47-l", "/ A47 B47 /", 515, 520, 665, 520, "geom-zero-dashed")
    b.add_point("O47", 590, 520, 8.0, "geom-point-zero")
    b.add_label("l47", "O47", 590, 590, "Fig. 47", "geom-label-sm")
    return b


def build_0249() -> EuclidSvgBuilder:
    b = EuclidSvgBuilder(
        "0249", 680, 640,
        "Figures 48–51 — Centripetal and Centrifugal Cones and Spheres",
        "Centripetal charge cone (Fig. 48), centrifugal discharge cone (Fig. 49), polarized sphere (Fig. 50), and oblate sphere (Fig. 51).",
    )
    b.add_frame()
    # Fig 48 top-left cone
    b.add_seg(b.elements, "c48-l", "/ A48 L48 /", 165, 230, 100, 65, "geom-line")
    b.add_seg(b.elements, "c48-r", "/ A48 R48 /", 165, 230, 230, 65, "geom-line")
    b.add_path(b.graphics, "h48", "( A48 H )", _cone_helix_d(165, 230, 165, 65, 62, 16, 5.5, 140), "geom-pos")
    b.add_circle(b.graphics, "b48", "( A48 B )", 165, 230, 32, "geom-circle")
    b.add_seg(b.graphics, "eq48", "/ E48A E48B /", 95, 230, 235, 230, "geom-zero")
    b.add_label("l48", "A48", 165, 285, "Fig. 48 • Centripetal Charge", "geom-label-sm")
    # Fig 49 bottom-left cone
    b.add_seg(b.elements, "c49-l", "/ A49 L49 /", 165, 535, 100, 360, "geom-line")
    b.add_seg(b.elements, "c49-r", "/ A49 R49 /", 165, 535, 230, 360, "geom-line")
    b.add_path(b.graphics, "h49", "( A49 H )", _cone_helix_d(165, 535, 165, 360, 62, 16, 5.5, 140), "geom-neg")
    b.add_circle(b.graphics, "b49", "( A49 B )", 165, 535, 32, "geom-circle")
    b.add_seg(b.graphics, "eq49", "/ E49A E49B /", 95, 535, 235, 535, "geom-zero")
    b.add_label("l49", "A49", 165, 592, "Fig. 49 • Centrifugal Discharge", "geom-label-sm")
    # Fig 50 top-right sphere
    b.add_circle(b.graphics, "sph50", "( S50 R )", 480, 160, 118, "geom-pos-fill")
    b.add_seg(b.graphics, "eq50", "/ E50A E50B /", 362, 160, 598, 160, "geom-zero")
    b.add_seg(b.elements, "ax50", "/ N50 S50 /", 480, 42, 480, 278, "geom-dashed")
    b.add_point("S50", 480, 160, 5.0, "geom-point-zero")
    b.add_label("l50", "S50", 480, 300, "Fig. 50 • Polarized Sphere", "geom-label-sm")
    # Fig 51 bottom-right oblate sphere
    b.add_ellipse(b.graphics, "sph51", "( S51 R )", 480, 455, 130, 92, "geom-neg-fill")
    b.add_seg(b.graphics, "eq51", "/ E51A E51B /", 350, 455, 610, 455, "geom-zero")
    b.add_seg(b.elements, "ax51", "/ N51 S51 /", 480, 363, 480, 547, "geom-dashed")
    b.add_point("S51", 480, 455, 5.0, "geom-point-zero")
    b.add_label("l51", "S51", 480, 578, "Fig. 51 • Oblate Sphere", "geom-label-sm")
    return b


def build_0273() -> EuclidSvgBuilder:
    b = EuclidSvgBuilder(
        "0273", 560, 580,
        "Figure 65 — The Universal Pulse",
        "Clockwise centripetal positive charge spiral paired with counter-clockwise centrifugal negative discharge spiral.",
    )
    b.add_frame("THE UNIVERSAL PULSE")
    cx, cy = 280.0, 290.0
    b.add_circle(b.graphics, "core", "( O R0 )", cx, cy, 28, "geom-zero-plane")
    b.add_path(b.graphics, "pos-spiral", "( O A )", _spiral_d(cx, cy, 28, 220, 2.75, cw=True, angle0=0.4), "geom-pos", 'marker-end="url(#geom-arrow-pos)"')
    b.add_path(b.graphics, "neg-spiral", "( O B )", _spiral_d(cx, cy, 28, 220, 2.75, cw=False, angle0=3.5), "geom-neg-dashed", 'marker-end="url(#geom-arrow-neg)"')
    b.add_point("O", cx, cy, 4.5, "geom-point-zero")
    b.add_label("lbl-a", "O", 492, 392, "A • POSITIVE CHARGE", "geom-label-sm")
    b.add_label("lbl-b", "O", 118, 120, "B • NEGATIVE DISCHARGE", "geom-label-sm")
    b.add_label("fig65", "O", 280, 552, "Fig. 65", "geom-label-title")
    return b


def build_0361() -> EuclidSvgBuilder:
    b = EuclidSvgBuilder(
        "0361", 560, 680,
        "Figures 101–102 — Gyroscopic Spin and Wave Amplitude",
        "Multi-cycle wave with radiant nodes (Fig. 101) and enlarged single wave amplitude crest (Fig. 102).",
    )
    b.add_frame()
    # Fig 101 top panel
    b.add_seg(b.graphics, "eq101", "/ E101A E101B /", 30, 125, 530, 125, "geom-zero")
    b.add_path(b.graphics, "wave101", "/ W101A W101B /", _sine_d(30, 125, 500, 52, 2.0, 120, math.pi / 2), "geom-bold")
    for idx, x in enumerate([155, 280, 405]):
        y = 177 if idx != 1 else 73
        cls = "geom-point-pos" if idx == 1 else "geom-point-neg"
        b.add_point(f"N101_{idx}", x, y, 6.0, cls)
    b.add_label("l101", "N101_1", 280, 232, "FIG. 101", "geom-label-title")
    b.add_seg(b.elements, "div", "[ D1 D2 ]", 20, 255, 540, 255, "geom-line")
    # Fig 102 bottom panel
    b.add_seg(b.graphics, "eq102", "/ E102A E102B /", 30, 470, 530, 470, "geom-zero")
    b.add_path(b.graphics, "wave102", "/ W102A W102B /", _sine_d(30, 470, 500, 130, 1.0, 120, -math.pi / 2), "geom-bold")
    b.add_point("N102", 280, 340, 9.0, "geom-point-pos")
    b.add_label("l102", "N102", 280, 650, "FIG. 102", "geom-label-title")
    return b


def build_0365() -> EuclidSvgBuilder:
    b = EuclidSvgBuilder(
        "0365", 560, 680,
        "Figure 103 — Solar and Atomic System Centered on Wave Amplitude",
        "Concentric elliptical orbits tilted across 1+-4+ / 4--1- planes resting on inert gas zero planes.",
    )
    b.add_frame()
    cx, cy = 280.0, 290.0
    b.add_seg(b.elements, "axis-0", "[ Z0 Z1 ]", cx, 45, cx, 575, "geom-zero-dashed")
    for k in range(1, 5):
        b.add_ellipse(b.graphics, f"orb-{k}", f"( O R{k} )", cx, cy, 18 * k, 155 + 15 * k, "geom-pos" if k % 2 == 1 else "geom-neg")
    b.add_ellipse(b.graphics, "inert-l", "( IL R )", 145, 565, 95, 22, "geom-zero-plane")
    b.add_ellipse(b.graphics, "inert-r", "( IR R )", 415, 565, 95, 22, "geom-zero-plane")
    b.add_circle(b.graphics, "sun", "( O S )", cx, 245, 18, "geom-pos-fill")
    b.add_point("O", cx, 245, 5.0, "geom-point-zero")
    b.add_label("inl", "O", 145, 570, "ZERO • INERT GAS", "geom-label-sm")
    b.add_label("inr", "O", 415, 570, "ZERO • INERT GAS", "geom-label-sm")
    b.add_label("fig103", "O", 280, 650, "FIG. 103", "geom-label-title")
    return b


def build_0399() -> EuclidSvgBuilder:
    b = EuclidSvgBuilder(
        "0399", 640, 580,
        "Figure 104 — Centripetal and Centrifugal Spiral Cones",
        "Clockwise centripetal cone (gravitation polarizes) vs. anti-clockwise centrifugal cone (radiation depolarizes).",
    )
    b.add_frame("CENTRIPETAL (CLOCKWISE) vs. CENTRIFUGAL (ANTI-CLOCKWISE)")
    # Left cone (clockwise)
    b.add_circle(b.graphics, "g1", "( G1 R )", 175, 430, 82, "geom-pos-fill")
    b.add_seg(b.elements, "c1-l", "/ G1 L1 /", 175, 455, 85, 120, "geom-line")
    b.add_seg(b.elements, "c1-r", "/ G1 R1 /", 175, 455, 265, 120, "geom-line")
    b.add_path(b.graphics, "h1", "( G1 H )", _cone_helix_d(175, 455, 175, 120, 86, 20, 6.5, 160), "geom-pos")
    # Right cone (anti-clockwise)
    b.add_circle(b.graphics, "g2", "( G2 R )", 465, 430, 82, "geom-neg-fill")
    b.add_seg(b.elements, "c2-l", "/ G2 L2 /", 465, 455, 375, 120, "geom-line")
    b.add_seg(b.elements, "c2-r", "/ G2 R2 /", 465, 455, 555, 120, "geom-line")
    b.add_path(b.graphics, "h2", "( G2 H )", _cone_helix_d(465, 455, 465, 120, 86, 20, -6.5, 160), "geom-neg")
    b.add_point("G1", 175, 455, 4.5, "geom-point-pos")
    b.add_point("G2", 465, 455, 4.5, "geom-point-neg")
    b.add_label("l-cw", "G1", 175, 80, "CLOCKWISE • GRAVITATION", "geom-label-sm")
    b.add_label("l-ccw", "G2", 465, 80, "ANTI-CLOCKWISE • RADIATION", "geom-label-sm")
    b.add_label("fig104", "G1", 320, 552, "FIG. 104", "geom-label-title")
    return b


def build_0400() -> EuclidSvgBuilder:
    b = EuclidSvgBuilder(
        "0400", 620, 660,
        "Figure 114 — Cube-Sphere Wave-Field of Nine Equators",
        "Isometric cube divided by three orthogonal zero-planes with 27 zero nodes and 0-1-2-3-4-0-4-3-2-1-0 octave formula.",
    )
    b.add_frame()
    # Isometric cube vertices: front face (70,130)-(390,130)-(390,410)-(70,410), back shifted (+150, -80)
    dx, dy = 150.0, -75.0
    x0, y0, s = 70.0, 125.0, 290.0
    for i in range(3):
        t = i * 0.5
        # horizontal & vertical grid lines on front and back
        b.add_seg(b.graphics, f"fh-{i}", f"/ FH{i}A FH{i}B /", x0, y0 + t * s, x0 + s, y0 + t * s, "geom-bold" if i != 1 else "geom-zero")
        b.add_seg(b.graphics, f"fv-{i}", f"/ FV{i}A FV{i}B /", x0 + t * s, y0, x0 + t * s, y0 + s, "geom-bold" if i != 1 else "geom-zero")
        b.add_seg(b.elements, f"bh-{i}", f"/ BH{i}A BH{i}B /", x0 + dx, y0 + dy + t * s, x0 + dx + s, y0 + dy + t * s, "geom-line")
        b.add_seg(b.elements, f"bv-{i}", f"/ BV{i}A BV{i}B /", x0 + dx + t * s, y0 + dy, x0 + dx + t * s, y0 + dy + s, "geom-line")
    for ix in range(3):
        for iy in range(3):
            fx, fy = x0 + ix * 0.5 * s, y0 + iy * 0.5 * s
            bx, by = fx + dx, fy + dy
            b.add_seg(b.elements, f"d-{ix}-{iy}", f"/ N{ix}{iy}0 N{ix}{iy}2 /", fx, fy, bx, by, "geom-line")
            for iz in range(3):
                px = fx + iz * 0.5 * dx
                py = fy + iz * 0.5 * dy
                b.add_point(f"Z{ix}{iy}{iz}", px, py, 7.5, "geom-point-zero")
    # Octave formula bar at bottom
    seq = ["0", "1+-", "2+-", "3+-", "4", "0", "4", "3+-", "2+-", "1+-", "0"]
    b.add_seg(b.graphics, "oct-axis", "/ OA OB /", 50, 560, 570, 560, "geom-zero")
    for i, lbl in enumerate(seq):
        ox = 50 + i * 52.0
        b.add_point(f"Q{i}", ox, 560, 12.0 if lbl == "0" else 10.0, "geom-point-zero")
        b.add_label(f"q-{i}", f"Q{i}", ox, 564, lbl, "geom-label-sm")
    b.add_label("fig114", "Z111", 310, 470, "Fig. 114 • Nine Equators & 27 Zero Nodes", "geom-label-title")
    return b


def build_0403() -> EuclidSvgBuilder:
    b = EuclidSvgBuilder(
        "0403", 580, 620,
        "Figure 115 — Sphere Inscribed Within the Cube of Zero Curvature",
        "Central radiant sphere centered at the intersection of three orthogonal zero-curvature equator planes.",
    )
    b.add_frame()
    cx, cy = 290.0, 295.0
    # 3 intersecting orthogonal planes
    b.add_polygon(b.graphics, "plane-xy", "< XY1 XY2 XY3 XY4 >", [(110, 85), (490, 85), (490, 485), (110, 485)], "geom-polygon-stroked")
    b.add_polygon(b.graphics, "plane-xz", "< XZ1 XZ2 XZ3 XZ4 >", [(60, 340), (420, 340), (520, 250), (160, 250)], "geom-zero-plane")
    b.add_polygon(b.graphics, "plane-yz", "< YZ1 YZ2 YZ3 YZ4 >", [(150, 130), (390, 35), (390, 435), (150, 535)], "geom-polygon-stroked")
    b.add_circle(b.graphics, "sphere", "( O R )", cx, cy, 108, "geom-pos-fill")
    b.add_point("O", cx, cy, 5.0, "geom-point-zero")
    b.add_label("cap", "O", 290, 585, "SPHERE CENTERED IN THREE ZERO EQUATORS", "geom-label-title")
    return b


def build_0412() -> EuclidSvgBuilder:
    b = EuclidSvgBuilder(
        "0412", 580, 680,
        "Figures 124–125 — Wave-Shaft Double Spiral Inside Cube",
        "Whirlpool double spiral along the diagonal wave-shaft of a cube (Fig. 124) and 3D cube-wave troughs/crests (Fig. 125).",
    )
    b.add_frame("THE WAVE-SHAFT IS THE STILL CENTER OF A WHIRLPOOL")
    # Cube outline
    x0, y0, s, dx, dy = 90.0, 135.0, 310.0, 105.0, -65.0
    b.add_polygon(b.elements, "c-front", "< F1 F2 F3 F4 >", [(x0, y0), (x0 + s, y0), (x0 + s, y0 + s), (x0, y0 + s)], "geom-polygon-stroked")
    b.add_polygon(b.elements, "c-back", "< B1 B2 B3 B4 >", [(x0 + dx, y0 + dy), (x0 + s + dx, y0 + dy), (x0 + s + dx, y0 + s + dy), (x0 + dx, y0 + s + dy)], "geom-dashed")
    # Diagonal wave shaft (top-left to bottom-right)
    b.add_seg(b.graphics, "shaft", "/ P4 B4 /", x0, y0, x0 + s, y0 + s, "geom-zero")
    b.add_path(b.graphics, "whirl-1", "( O W1 )", _cone_helix_d(x0, y0, x0 + s * 0.5, y0 + s * 0.5, 135, 38, 6.0, 140), "geom-pos")
    b.add_path(b.graphics, "whirl-2", "( O W2 )", _cone_helix_d(x0 + s, y0 + s, x0 + s * 0.5, y0 + s * 0.5, 135, 38, 6.0, 140), "geom-neg")
    b.add_point("O", x0 + s * 0.5, y0 + s * 0.5, 5.5, "geom-point-zero")
    b.add_label("fig124", "O", 290, 470, "FIG. 124", "geom-label-title")
    # Fig 125 wave-in-cubes
    b.add_path(b.graphics, "wave125", "/ W125A W125B /", _sine_d(60, 565, 460, 42, 3.5, 120), "geom-bold")
    b.add_seg(b.elements, "eq125", "/ E125A E125B /", 50, 565, 530, 565, "geom-zero-dashed")
    b.add_label("fig125", "O", 290, 645, "FIG. 125", "geom-label-title")
    return b


def build_0413() -> EuclidSvgBuilder:
    # Folio 0413 in Lesson 43: duplicate Fig. 103 in resources, keep faithful vectorization
    b = build_0365()
    b.folio = "0413"
    b.title = "Figure 115 / 103 — Atomic and Solar Wave-Field Loops"
    return b


def build_0434() -> EuclidSvgBuilder:
    b = EuclidSvgBuilder(
        "0434", 620, 680,
        "Figures 158–161 — All of Nature's Magnets Are Cones",
        "Bar magnet (Fig. 158), cone magnet (Fig. 159), Earth vapor cone (Fig. 160), and curved equators/radii sphere (Fig. 161).",
    )
    b.add_frame("ALL OF NATURE'S MAGNETS ARE CONES")
    b.add_seg(b.elements, "h-div", "[ H1 H2 ]", 20, 290, 600, 290, "geom-line")
    b.add_seg(b.elements, "v-div", "[ V1 V2 ]", 310, 45, 310, 660, "geom-line")
    # Fig 158 bar magnet
    b.add_polygon(b.graphics, "bar158", "< B1 B2 B3 B4 >", [(65, 130), (265, 130), (265, 152), (65, 152)], "geom-polygon-stroked")
    b.add_seg(b.graphics, "eq158", "/ E158A E158B /", 165, 85, 165, 200, "geom-zero")
    b.add_label("f158", "B1", 165, 72, "FIG. 158 • BAR MAGNET", "geom-label-sm")
    # Fig 159 cone magnet
    b.add_polygon(b.graphics, "cone159", "< C1 C2 C3 >", [(355, 145), (565, 80), (565, 210)], "geom-pos-fill")
    b.add_path(b.graphics, "eq159", "/ E159A E159B /", "M 385 100 A 55 55 0 0 1 385 190", "geom-zero")
    b.add_label("f159", "C1", 465, 72, "FIG. 159 • CONE MAGNET", "geom-label-sm")
    # Fig 160 Earth vapor cone
    b.add_polygon(b.graphics, "cone160", "< V1 V2 V3 >", [(165, 590), (75, 360), (255, 360)], "geom-neg-fill")
    b.add_label("f160", "V1", 165, 645, "FIG. 160 • VAPOR CONE", "geom-label-sm")
    # Fig 161 Curved equators & radii sphere
    b.add_circle(b.graphics, "sph161", "( S161 R )", 465, 465, 135, "geom-circle")
    b.add_seg(b.graphics, "eq161", "/ E161A E161B /", 330, 465, 600, 465, "geom-zero")
    b.add_seg(b.graphics, "ax161", "/ N161 S161 /", 465, 330, 465, 600, "geom-zero")
    for dy in [-65, -32, 32, 65]:
        b.add_path(b.elements, f"ceq-{dy}", f"/ CE{dy}A CE{dy}B /", f"M 345 {465 + dy} Q 465 {465 + dy * 0.55} 585 {465 + dy}", "geom-dashed")
    b.add_point("S161", 465, 465, 4.5, "geom-point-zero")
    b.add_label("f161", "S161", 465, 645, "FIG. 161 • CURVED EQUATORS", "geom-label-sm")
    return b


def build_0457() -> EuclidSvgBuilder:
    b = EuclidSvgBuilder(
        "0457", 640, 720,
        "Figures 162–169 — Light Pressure Lenses and Curvature Systems",
        "Eight-panel comparison of parallel, bent, inward, outward, dividing, uniting, spherical, and oblate light lenses.",
    )
    b.add_frame("LIGHT PRESSURE LENSES (FIGS. 162–169)")
    b.add_seg(b.elements, "v-mid", "[ VM1 VM2 ]", 320, 45, 320, 700, "geom-line")
    for r_idx, y_mid in enumerate([130, 290, 435, 595]):
        if r_idx < 3:
            b.add_seg(b.elements, f"h-{r_idx}", f"/ H{r_idx}A H{r_idx}B /", 20, y_mid + 85, 620, y_mid + 85, "geom-line")
        # Left & Right panel schematics
        for c_idx, cx in enumerate([170, 470]):
            fig_num = 162 + r_idx * 2 + c_idx
            b.add_seg(b.graphics, f"eq-{fig_num}", f"/ E{fig_num}A E{fig_num}B /", cx - 120, y_mid, cx + 120, y_mid, "geom-zero")
            if fig_num in (162, 163):
                for dx in [-80, -40, 0, 40, 80]:
                    b.add_seg(b.elements, f"ray-{fig_num}-{dx}", f"/ R{fig_num}_{dx}A R{fig_num}_{dx}B /", cx + dx, y_mid - 50, cx + dx + (dx * 0.25 if fig_num == 163 else 0), y_mid + 50, "geom-ray")
            elif fig_num in (164, 165, 166, 167):
                ry = 22 if fig_num % 2 == 1 else 36
                b.add_ellipse(b.graphics, f"lens-{fig_num}", f"( L{fig_num} R )", cx, y_mid, 105, ry, "geom-pos-fill" if fig_num % 2 == 0 else "geom-neg-fill")
            else:
                ry = 75 if fig_num == 168 else 52
                b.add_ellipse(b.graphics, f"sph-{fig_num}", f"( L{fig_num} R )", cx, y_mid, 95, ry, "geom-circle")
            b.add_label(f"lbl-{fig_num}", f"L{fig_num}", cx, y_mid + (76 if r_idx == 3 else 68), f"FIG. {fig_num}", "geom-label-sm")
    return b


def build_0465() -> EuclidSvgBuilder:
    b = EuclidSvgBuilder(
        "0465", 580, 680,
        "Figures 170–172 — Three Equators of Zero Curvature and Corona Rings",
        "Three orthogonal zero equators in a sphere (Fig. 170), united equator lens radii (Fig. 171), and corona ring (Fig. 172).",
    )
    b.add_frame()
    # Fig 170
    b.add_circle(b.graphics, "c170", "( O170 R )", 290, 125, 62, "geom-bold")
    b.add_seg(b.elements, "x170", "/ X170A X170B /", 75, 125, 505, 125, "geom-zero-dashed")
    b.add_seg(b.elements, "y170", "/ Y170A Y170B /", 290, 35, 290, 215, "geom-zero-dashed")
    b.add_seg(b.elements, "z170", "/ Z170A Z170B /", 110, 195, 470, 55, "geom-zero-dashed")
    b.add_point("O170", 290, 125, 4.5, "geom-point-zero")
    b.add_label("f170", "O170", 480, 205, "FIG. 170", "geom-label-sm")
    # Fig 171
    b.add_ellipse(b.graphics, "e171-o", "( O171 R2 )", 290, 355, 225, 102, "geom-circle")
    b.add_circle(b.graphics, "c171-i", "( O171 R1 )", 290, 355, 55, "geom-pos-fill")
    b.add_seg(b.graphics, "eq171", "/ E171A E171B /", 45, 355, 535, 355, "geom-zero")
    for i in range(12):
        ang = math.radians(i * 30)
        b.add_seg(b.elements, f"rad171-{i}", f"/ O171 R{i} /", 290, 355, 290 + 185 * math.cos(ang), 355 + 95 * math.sin(ang), "geom-ray")
    b.add_point("O171", 290, 355, 4.5, "geom-point-zero")
    b.add_label("f171", "O171", 480, 445, "FIG. 171", "geom-label-sm")
    # Fig 172
    b.add_circle(b.graphics, "c172-o", "( O172 R2 )", 290, 565, 78, "geom-dashed")
    b.add_circle(b.graphics, "c172-i", "( O172 R1 )", 290, 565, 36, "geom-point-zero")
    b.add_label("f172", "O172", 480, 625, "FIG. 172", "geom-label-sm")
    return b


def build_0466() -> EuclidSvgBuilder:
    b = EuclidSvgBuilder(
        "0466", 580, 720,
        "Figure 174 — Nature's Two Curvature Systems",
        "Two bar magnets separated by dividing equators and united at the central sphere equator with curved radii.",
    )
    b.add_frame("NATURE'S TWO CURVATURE SYSTEMS")
    cx, cy = 290.0, 360.0
    b.add_seg(b.graphics, "eq-top", "/ ET1 ET2 /", 35, 190, 545, 190, "geom-zero")
    b.add_seg(b.graphics, "eq-mid", "/ EM1 EM2 /", 35, 360, 545, 360, "geom-zero")
    b.add_seg(b.graphics, "eq-bot", "/ EB1 EB2 /", 35, 530, 545, 530, "geom-zero")
    b.add_polygon(b.graphics, "mag-top", "< MT1 MT2 MT3 MT4 >", [(278, 90), (302, 90), (302, 290), (278, 290)], "geom-polygon-stroked")
    b.add_polygon(b.graphics, "mag-bot", "< MB1 MB2 MB3 MB4 >", [(278, 430), (302, 430), (302, 630), (278, 630)], "geom-polygon-stroked")
    b.add_circle(b.graphics, "center-n", "( O R )", cx, cy, 56, "geom-pos-fill")
    for r in [95, 140, 185]:
        b.add_circle(b.elements, f"field-{r}", f"( O F{r} )", cx, cy, r, "geom-dashed")
    b.add_point("O", cx, cy, 5.0, "geom-point-zero")
    b.add_label("l-div1", "O", 455, 180, "EQUATOR WHICH DIVIDES", "geom-label-sm")
    b.add_label("l-uni", "O", 455, 350, "EQUATOR WHICH UNITES", "geom-label-sm")
    b.add_label("l-div2", "O", 455, 520, "EQUATOR WHICH DIVIDES", "geom-label-sm")
    b.add_label("fig174", "O", 290, 695, "FIG. 174", "geom-label-title")
    return b


def build_0470() -> EuclidSvgBuilder:
    b = EuclidSvgBuilder(
        "0470", 620, 680,
        "Figure 177 — Russell Periodic Chart of the Elements, No. 2",
        "Concentric octave rings centered on The Inert Gases with horizontal 0-axis and vertical +4-0-4- amplitude axis.",
    )
    b.add_frame("THE RUSSELL PERIODIC CHART OF THE ELEMENTS, NO. 2")
    cx, cy = 310.0, 340.0
    b.add_seg(b.graphics, "h-axis", "/ HL HR /", 45, cy, 575, cy, "geom-zero")
    b.add_seg(b.graphics, "v-axis", "/ VT VB /", cx, 65, cx, 615, "geom-zero")
    for k, r in enumerate([58, 95, 132, 168, 204, 240]):
        b.add_circle(b.graphics, f"oct-{k}", f"( O R{k} )", cx, cy, r, "geom-circle" if k < 4 else "geom-pos")
    # Radial octave spokes
    for deg in [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]:
        rad = math.radians(deg)
        b.add_seg(b.elements, f"spk-{deg}", f"/ O S{deg} /", cx + 58 * math.cos(rad), cy + 58 * math.sin(rad), cx + 240 * math.cos(rad), cy + 240 * math.sin(rad), "geom-ray")
    # Inert gas nodes along horizontal axis
    gases = [("XENON", 92), ("ARGON", 136), ("HELIUM", 180), ("NEON", 440), ("KRYPTON", 484), ("NITON", 528)]
    for name, gx in gases:
        b.add_point(name, gx, cy, 10.0, "geom-point-zero")
        b.add_label(f"g-{name}", name, gx, cy - 16, name, "geom-label-sm")
    b.add_point("O", cx, cy, 5.0, "geom-point-zero")
    b.add_label("inert", "O", cx, cy - 6, "THE INERT", "geom-label-sm")
    b.add_label("gases", "O", cx, cy + 12, "GASES", "geom-label-sm")
    b.add_label("fig177", "O", 310, 652, "Figure 177", "geom-label-title")
    return b


def build_0473() -> EuclidSvgBuilder:
    b = EuclidSvgBuilder(
        "0473", 620, 540,
        "Figure 179 — Octave Arch of Integration and Disintegration",
        "Symmetric periodic arch culminating in Carbon (C) with inner integration arrows and outer disintegration arrows.",
    )
    b.add_frame("OCTAVE ARCH OF INTEGRATION AND DISINTEGRATION")
    cx, cy = 310.0, 290.0
    for r in [115, 148, 182, 216]:
        b.add_path(b.graphics, f"arch-{r}", f"( O A{r} )", f"M {cx - r:.2f} {cy:.2f} A {r:.2f} {r:.2f} 0 0 1 {cx + r:.2f} {cy:.2f}", "geom-circle")
    # Left & right descending octave rungs
    for side, sx in [("L", -1), ("R", 1)]:
        for row, y in enumerate([330, 390, 450]):
            x1 = cx + sx * 120
            x2 = cx + sx * 225
            b.add_seg(b.graphics, f"rung-{side}-{row}", f"/ R{side}{row}A R{side}{row}B /", x1, y, x2, y + 28, "geom-bold")
        b.add_path(b.graphics, f"outer-{side}", f"/ O{side}A O{side}B /", f"M {cx + sx * 245:.2f} 290 L {cx + sx * 245:.2f} 475", "geom-neg", 'marker-end="url(#geom-arrow-neg)"')
        b.add_path(b.graphics, f"inner-{side}", f"/ I{side}A I{side}B /", f"M {cx + sx * 105:.2f} 475 L {cx + sx * 105:.2f} 290", "geom-pos", 'marker-end="url(#geom-arrow-pos)"')
    b.add_point("C", cx, 175, 11.0, "geom-point-zero")
    b.add_label("lbl-c", "C", cx, 179, "C", "geom-label-sm")
    b.add_label("carbon", "C", cx, 212, "CARBON", "geom-label")
    b.add_label("fig179", "C", cx, 515, "FIG. 179", "geom-label-title")
    return b


def build_0494() -> EuclidSvgBuilder:
    # Folio 0494 is Fig. 177 in Lesson 47
    b = build_0470()
    b.folio = "0494"
    return b


def build_0499() -> EuclidSvgBuilder:
    # Folio 0499 is Fig. 179 in Lesson 47
    b = build_0473()
    b.folio = "0499"
    return b


def build_0503() -> EuclidSvgBuilder:
    b = EuclidSvgBuilder(
        "0503", 580, 680,
        "Figures 180–182 — Gyroscopic Equators of the Elements",
        "Perspective base plane with semicircular 1-4-0-4-1 arc (Fig. 180), tilted element discs (Fig. 181), and unwinding rings (Fig. 182).",
    )
    b.add_frame()
    # Fig 180
    b.add_polygon(b.graphics, "base180", "< B1 B2 B3 B4 >", [(40, 195), (150, 115), (540, 115), (430, 195)], "geom-polygon-stroked")
    b.add_path(b.graphics, "arc180", "( O180 R )", "M 160 155 A 130 105 0 0 1 420 155", "geom-bold")
    for idx, deg in enumerate([150, 125, 105, 90, 75, 55, 30]):
        rad = math.radians(deg)
        b.add_seg(b.elements, f"r180-{idx}", f"/ O180 R{idx} /", 290, 155, 290 + 150 * math.cos(rad), 155 - 120 * math.sin(rad), "geom-ray")
    b.add_point("O180", 290, 155, 4.5, "geom-point-zero")
    b.add_label("f180", "O180", 290, 218, "Fig. 180 • Basis of Atomic/Solar Systems", "geom-label-sm")
    # Fig 181
    b.add_polygon(b.graphics, "base181", "< C1 C2 C3 C4 >", [(40, 465), (150, 385), (540, 385), (430, 465)], "geom-polygon-stroked")
    elems = ["FLUORINE", "OXYGEN", "NITROGEN", "CARBON", "BORON", "BERYLLIUM", "LITHIUM"]
    for i, name in enumerate(elems):
        ex = 140 + i * 50
        ey = 345 - 32 * math.sin(math.pi * i / 6.0)
        b.add_ellipse(b.graphics, f"disc-{i}", f"( E{i} R )", ex, ey, 48, 86, "geom-pos-fill" if i > 3 else ("geom-neg-fill" if i < 3 else "geom-zero-plane"))
    b.add_point("O181", 290, 425, 4.5, "geom-point-zero")
    b.add_label("f181", "O181", 290, 488, "Fig. 181 • Gyroscopic Equators", "geom-label-sm")
    # Fig 182
    b.add_path(b.graphics, "arc182", "( O182 R )", "M 130 615 A 160 95 0 0 1 450 615", "geom-zero")
    for i in range(7):
        ang = math.radians(160 - i * 23.3)
        px, py = 290 + 160 * math.cos(ang), 615 - 95 * math.sin(ang)
        b.add_ellipse(b.graphics, f"ring182-{i}", f"( R{i} S )", px, py, 22, 10, "geom-neg" if i < 3 else "geom-pos")
    b.add_point("O182", 290, 615, 4.5, "geom-point-zero")
    b.add_label("f182", "O182", 290, 655, "Fig. 182 • Unwinding Rings", "geom-label-sm")
    return b


BUILDERS = {
    "0002.g1.svg": build_0002,
    "part_01/0040.g1.svg": build_0040,
    "part_02/0064.g1.svg": build_0064,
    "part_03/0103.g1.svg": build_0103,
    "part_04/0131.g1.svg": build_0131,
    "part_04/0132.g1.svg": build_0132,
    "part_04/0136.g1.svg": build_0136,
    "part_04/0146.g1.svg": build_0146,
    "part_05/0162.g1.svg": build_0162,
    "part_05/0175.g1.svg": build_0175,
    "part_07/0249.g1.svg": build_0249,
    "part_08/0273.g1.svg": build_0273,
    "part_10/0361.g1.svg": build_0361,
    "part_10/0365.g1.svg": build_0365,
    "part_11/0399.g1.svg": build_0399,
    "part_11/0400.g1.svg": build_0400,
    "part_11/0403.g1.svg": build_0403,
    "part_11/0412.g1.svg": build_0412,
    "part_11/0413.g1.svg": build_0413,
    "part_12/0434.g1.svg": build_0434,
    "part_12/0457.g1.svg": build_0457,
    "part_12/0465.g1.svg": build_0465,
    "part_12/0466.g1.svg": build_0466,
    "part_12/0470.g1.svg": build_0470,
    "part_12/0473.g1.svg": build_0473,
    "part_12/0494.g1.svg": build_0494,
    "part_12/0499.g1.svg": build_0499,
    "part_12/0503.g1.svg": build_0503,
}


def main() -> None:
    for rel_path, fn in BUILDERS.items():
        out_path = HSC_DIR / rel_path
        svg_text = fn().render()
        out_path.write_text(svg_text, encoding="utf-8")
    print(f"Generated {len(BUILDERS)} .euclid-graphic SVGs in {HSC_DIR}")


if __name__ == "__main__":
    main()
