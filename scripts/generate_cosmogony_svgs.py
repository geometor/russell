#!/usr/bin/env python3
"""Generate the flagship parametric SVG diagrams for GEOMETOR Russell.

Establishes the GEOMETOR Russell visual style (.russell-graphic):
- Dark-first cosmic chalkboard aesthetic with automatic light-mode adaptation
- Gold (#e8b85a) for Still Magnetic Light (0), Cube boundaries, and Zero-Curvature Equators
- Crimson/Coral (#f43f5e) for Centripetal / Genero-active / Male (+) compression spirals
- Cyan/Azure (#38bdf8) for Centrifugal / Radio-active / Female (-) expansion spirals
- Radiant White-Gold (#fef08a) for Wave Amplitude (4+ / 0 / 4-, Carbon / Sun)
- Signature double-ruled plate frame with 'W. R. • GEOMETOR' plate badge
"""

from __future__ import annotations

import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SVG_OUT_DIR = ROOT / "docsrc" / "_static" / "svg"

SHARED_STYLE = """
  <style>
    .russell-graphic {
      font-family: "Fira Sans Condensed", "Fira Sans", "DejaVu Sans", sans-serif;
      background-color: #0c0e14;
    }
    .plate-bg { fill: #0c0e14; }
    .panel-bg { fill: #121621; stroke: #262e42; stroke-width: 1.2; }
    .frame-outer { fill: none; stroke: #ebe6dc; stroke-width: 2; opacity: 0.85; }
    .frame-inner { fill: none; stroke: #e8b85a; stroke-width: 0.9; opacity: 0.6; }
    .rule-divider { stroke: #262e42; stroke-width: 1.4; }
    .zero-line { stroke: #e8b85a; stroke-width: 2.2; fill: none; stroke-linecap: round; }
    .zero-dashed { stroke: #e8b85a; stroke-width: 1.5; stroke-dasharray: 5, 4; fill: none; opacity: 0.85; }
    .zero-plane { fill: #e8b85a; fill-opacity: 0.16; stroke: #e8b85a; stroke-width: 1.3; }
    .pos-line { stroke: #fb7185; stroke-width: 2.2; fill: none; stroke-linecap: round; }
    .pos-fill { fill: #fb7185; fill-opacity: 0.16; stroke: #fb7185; stroke-width: 1.6; }
    .neg-line { stroke: #38bdf8; stroke-width: 2.2; fill: none; stroke-linecap: round; }
    .neg-fill { fill: #38bdf8; fill-opacity: 0.16; stroke: #38bdf8; stroke-width: 1.6; }
    .fg-line { stroke: #ebe6dc; stroke-width: 1.9; fill: none; stroke-linecap: round; }
    .fg-dashed { stroke: #949eb0; stroke-width: 1.3; stroke-dasharray: 4, 4; fill: none; }
    .node-zero { fill: #151924; stroke: #e8b85a; stroke-width: 2.2; }
    .node-pos { fill: #151924; stroke: #fb7185; stroke-width: 2.2; }
    .node-neg { fill: #151924; stroke: #38bdf8; stroke-width: 2.2; }
    .node-amp { fill: #e8b85a; stroke: #fef08a; stroke-width: 2.6; }
    .title-text { fill: #ebe6dc; font-size: 16px; font-weight: bold; letter-spacing: 1.4px; text-anchor: middle; }
    .subtitle-text { fill: #e8b85a; font-size: 11.5px; font-weight: bold; letter-spacing: 1.1px; text-anchor: middle; }
    .panel-title { fill: #e8b85a; font-size: 12px; font-weight: bold; letter-spacing: 1px; text-anchor: middle; }
    .label-text { fill: #ebe6dc; font-size: 11.5px; font-weight: bold; }
    .label-center { fill: #ebe6dc; font-size: 11.5px; font-weight: bold; text-anchor: middle; dominant-baseline: central; }
    .label-small { fill: #949eb0; font-size: 10px; font-weight: normal; }
    .caption-box { fill: #0c0e14; stroke: #262e42; stroke-width: 1; }
    .caption-text { fill: #ebe6dc; font-size: 10.5px; font-weight: normal; letter-spacing: 0.3px; text-anchor: middle; }
    .fig-tag { fill: #e8b85a; font-size: 12px; font-weight: bold; letter-spacing: 1.2px; }
    .sig-tag { fill: #949eb0; font-size: 10.5px; font-weight: bold; letter-spacing: 1.5px; text-anchor: end; }
  </style>
  <defs>
    <marker id="arrow-pos" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8.5 5 L 0 8.5 z" fill="#fb7185"/>
    </marker>
    <marker id="arrow-neg" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8.5 5 L 0 8.5 z" fill="#38bdf8"/>
    </marker>
    <marker id="arrow-zero" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8.5 5 L 0 8.5 z" fill="#e8b85a"/>
    </marker>
    <marker id="arrow-fg" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8.5 5 L 0 8.5 z" fill="#ebe6dc"/>
    </marker>
    <radialGradient id="sun-glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#fef08a" stop-opacity="0.95"/>
      <stop offset="35%" stop-color="#fb7185" stop-opacity="0.55"/>
      <stop offset="75%" stop-color="#e8b85a" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#0c0e14" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="lens-glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#fb7185" stop-opacity="0.40"/>
      <stop offset="55%" stop-color="#38bdf8" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#0c0e14" stop-opacity="0"/>
    </radialGradient>
  </defs>
"""


def plate_wrapper(width: int, height: int, title: str, subtitle: str, fig_label: str, body: str) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" class="russell-graphic">
{SHARED_STYLE}
  <rect x="0" y="0" width="{width}" height="{height}" class="plate-bg"/>
  <rect x="12" y="12" width="{width - 24}" height="{height - 24}" class="frame-outer"/>
  <rect x="16" y="16" width="{width - 32}" height="{height - 32}" class="frame-inner"/>
  <text x="{width / 2}" y="40" class="title-text">{title}</text>
  <text x="{width / 2}" y="58" class="subtitle-text">{subtitle}</text>
  <line x1="28" y1="68" x2="{width - 28}" y2="68" class="rule-divider"/>
{body}
  <text x="28" y="{height - 24}" class="fig-tag">{fig_label}</text>
  <text x="{width - 28}" y="{height - 24}" class="sig-tag">W. R. • GEOMETOR</text>
</svg>
"""


def build_01_mind_fulcrum_lever() -> str:
    """Figs. 7-16 & 28-33: The Still Magnetic Fulcrum (0) and Divided Electric Wave-Lever."""
    w, h = 860, 620
    # Top panel: Undivided Still Magnetic Light vs Divided Electric Pair
    # Bottom panel: The Wave Lever oscillating across the Fulcrum of Zero Rest
    wave_pts = []
    for i in range(181):
        x = 90 + (680 * i / 180)
        theta = i * 2 * math.pi / 90
        y = 435 - 75 * math.sin(theta)
        wave_pts.append(f"{x:.1f},{y:.1f}")
    wave_poly = " ".join(wave_pts)

    body = f"""
  <!-- Panel 1: Undivided Zero vs Divided Polarity -->
  <rect x="32" y="82" width="796" height="205" rx="4" class="panel-bg"/>
  <text x="430" y="104" class="panel-title">I. UNDIVIDED STILL MAGNETIC LIGHT (MIND) DIVIDED INTO MATED PAIRS OF OPPOSITE CONDITION</text>

  <!-- Left: One Whole Idea (Rest) -->
  <circle cx="155" cy="182" r="44" fill="url(#sun-glow)"/>
  <circle cx="155" cy="182" r="24" class="node-zero"/>
  <text x="155" y="182" class="label-center" style="font-size:15px;fill:#e8b85a;">0</text>
  <text x="155" y="242" class="label-center">STILL MAGNETIC LIGHT</text>
  <text x="155" y="257" class="label-center label-small">(Undivided Equilibrium • Knowing)</text>

  <!-- Arrow of Division (Thinking) -->
  <line x1="220" y1="174" x2="310" y2="174" class="zero-line" marker-end="url(#arrow-zero)"/>
  <line x1="310" y1="190" x2="220" y2="190" class="fg-dashed" marker-end="url(#arrow-fg)"/>
  <text x="265" y="164" class="label-center label-small" style="fill:#e8b85a;">CONCENTRATIVE THINKING</text>
  <text x="265" y="206" class="label-center label-small">DECENTRATIVE REST</text>

  <!-- Right: Divided Electric Polarity (+ / 0 / -) -->
  <line x1="395" y1="182" x2="735" y2="182" class="zero-dashed"/>
  <!-- Red Father Pole -->
  <path d="M 565 182 L 425 142 L 425 222 Z" class="pos-fill"/>
  <!-- Blue Mother Pole -->
  <path d="M 565 182 L 705 142 L 705 222 Z" class="neg-fill"/>

  <circle cx="405" cy="182" r="21" class="node-pos"/>
  <text x="405" y="182" class="label-center" style="fill:#fb7185;">+4</text>
  <text x="405" y="125" class="label-center" style="fill:#fb7185;">FATHER • RED</text>
  <text x="405" y="242" class="label-center label-small">Compression • Heat • Gravity</text>

  <circle cx="565" cy="182" r="20" class="node-zero"/>
  <text x="565" y="182" class="label-center" style="fill:#e8b85a;">0</text>
  <text x="565" y="125" class="label-center" style="fill:#e8b85a;">MAGNETIC FULCRUM</text>
  <text x="565" y="242" class="label-center label-small">Zero Rest • Balance Point</text>

  <circle cx="725" cy="182" r="21" class="node-neg"/>
  <text x="725" y="182" class="label-center" style="fill:#38bdf8;">-4</text>
  <text x="725" y="125" class="label-center" style="fill:#38bdf8;">MOTHER • BLUE</text>
  <text x="725" y="242" class="label-center label-small">Expansion • Cold • Radiation</text>

  <!-- Panel 2: The Fulcrum and the Wave Lever -->
  <rect x="32" y="302" width="796" height="270" rx="4" class="panel-bg"/>
  <text x="430" y="324" class="panel-title">II. THE WAVE-LEVER OSCILLATING UPON THE STILL FULCRUM OF ZERO CURVATURE (FIGS. 28–33)</text>

  <!-- Wave Axis -->
  <line x1="70" y1="435" x2="790" y2="435" class="zero-line"/>
  <text x="802" y="438" class="label-small" style="fill:#e8b85a;">0 AXIS</text>

  <!-- Sine Wave -->
  <polyline points="{wave_poly}" class="fg-line" style="stroke-width:2.4;"/>

  <!-- Lever Diagonal across First Wave Center -->
  <line x1="175" y1="360" x2="345" y2="510" class="pos-line" stroke-dasharray="6,3"/>
  <line x1="515" y1="360" x2="685" y2="510" class="neg-line" stroke-dasharray="6,3"/>

  <!-- Fulcrum Triangles at 0 Nodes -->
  <polygon points="90,435 80,455 100,455" class="zero-plane"/>
  <polygon points="260,435 250,455 270,455" class="zero-plane"/>
  <polygon points="430,435 420,455 440,455" class="zero-plane"/>
  <polygon points="600,435 590,455 610,455" class="zero-plane"/>
  <polygon points="770,435 760,455 780,455" class="zero-plane"/>

  <!-- Crest & Trough Nodes -->
  <circle cx="175" cy="360" r="14" class="node-pos"/>
  <text x="175" y="360" class="label-center" style="font-size:10px;fill:#fb7185;">+A</text>
  <text x="175" y="338" class="label-center label-small" style="fill:#fb7185;">HIGH PRESSURE (GRAVITY)</text>

  <circle cx="345" cy="510" r="14" class="node-neg"/>
  <text x="345" y="510" class="label-center" style="font-size:10px;fill:#38bdf8;">-A</text>
  <text x="345" y="534" class="label-center label-small" style="fill:#38bdf8;">LOW PRESSURE (VACUITY)</text>

  <circle cx="515" cy="360" r="14" class="node-pos"/>
  <text x="515" y="360" class="label-center" style="font-size:10px;fill:#fb7185;">+A</text>

  <circle cx="685" cy="510" r="14" class="node-neg"/>
  <text x="685" y="510" class="label-center" style="font-size:10px;fill:#38bdf8;">-A</text>

  <!-- Zero Fulcrum Labels -->
  <circle cx="260" cy="435" r="11" class="node-zero"/>
  <text x="260" y="435" class="label-center" style="font-size:10px;fill:#e8b85a;">0</text>
  <circle cx="430" cy="435" r="11" class="node-zero"/>
  <text x="430" y="435" class="label-center" style="font-size:10px;fill:#e8b85a;">0</text>
  <circle cx="600" cy="435" r="11" class="node-zero"/>
  <text x="600" y="435" class="label-center" style="font-size:10px;fill:#e8b85a;">0</text>

  <text x="430" y="556" class="caption-text">"POWER LIES IN THE STILL MAGNETIC FULCRUM ONLY — NEVER IN THE MOVING ELECTRIC LEVER."</text>
"""
    return plate_wrapper(
        w,
        h,
        "THE STILL MAGNETIC FULCRUM AND TWO-WAY ELECTRIC WAVE-LEVER",
        "LESSONS 9–17 • MIND AT REST DIVIDED INTO RECIPROCAL COMPRESSION AND EXPANSION",
        "FIGS. 7–16, 28–33",
        body,
    )


def _spiral_diamond_path(cx: float, cy: float, rx: float, ry: float, turns: int = 5) -> str:
    """Create a helical conical vortex path inside a diamond envelope."""
    pts = []
    steps = turns * 24
    for i in range(steps + 1):
        u = i / steps  # 0 (top pole) to 1 (bottom pole)
        y = (cy - ry) + 2 * ry * u
        env = 1.0 - abs(2 * u - 1.0)
        x = cx + rx * env * math.sin(u * turns * 2 * math.pi)
        pts.append(f"{'M' if i == 0 else 'L'} {x:.1f} {y:.1f}")
    return " ".join(pts)


def build_02_vitality_cycle_cones() -> str:
    """Figs. 38-47: Vitality increases as poles pull apart; decreases as poles depolarize."""
    w, h = 880, 740
    d43 = _spiral_diamond_path(440, 385, 78, 98, turns=6)
    d45 = _spiral_diamond_path(185, 614, 78, 50, turns=4)
    d46 = _spiral_diamond_path(440, 614, 78, 26, turns=3)

    body = f"""
  <!-- Top Row: Figs. 38, 39, 40 (Polarization Begins) -->
  <rect x="32" y="80" width="816" height="145" rx="4" class="panel-bg"/>
  <text x="440" y="100" class="panel-title">I. GENERATION: VITALITY INCREASES AS POLES PULL APART TOWARD MATURITY (FIGS. 38–40)</text>

  <!-- Fig 38: Seed at Zero Rest -->
  <line x1="65" y1="155" x2="225" y2="155" class="zero-dashed"/>
  <circle cx="145" cy="155" r="13" class="node-zero"/>
  <text x="145" y="155" class="label-center" style="fill:#e8b85a;">0</text>
  <text x="145" y="195" class="label-center">Fig. 38 • Seed in Rest</text>

  <!-- Fig 39: Equatorial Extension -->
  <line x1="325" y1="155" x2="515" y2="155" class="zero-line"/>
  <circle cx="325" cy="155" r="10" class="node-zero"/>
  <circle cx="420" cy="155" r="12" class="node-zero"/>
  <circle cx="515" cy="155" r="10" class="node-zero"/>
  <text x="420" y="155" class="label-center" style="font-size:10px;fill:#e8b85a;">0</text>
  <text x="420" y="195" class="label-center">Fig. 39 • Divided Equator</text>

  <!-- Fig 40: Cross of Polarity -->
  <line x1="620" y1="155" x2="780" y2="155" class="zero-line"/>
  <line x1="700" y1="122" x2="700" y2="188" class="pos-line" marker-start="url(#arrow-neg)" marker-end="url(#arrow-pos)"/>
  <circle cx="620" cy="155" r="9" class="node-zero"/>
  <circle cx="700" cy="155" r="11" class="node-zero"/>
  <circle cx="780" cy="155" r="9" class="node-zero"/>
  <text x="714" y="122" class="label-center" style="fill:#38bdf8;">-</text>
  <text x="714" y="188" class="label-center" style="fill:#fb7185;">+</text>
  <text x="700" y="206" class="label-center">Fig. 40 • Polarized Cross</text>

  <!-- Middle Row: Figs. 41-44 (Double-Cone Spiral Growth & Mature Tree) -->
  <rect x="32" y="238" width="816" height="278" rx="4" class="panel-bg"/>
  <text x="440" y="258" class="panel-title">II. FULL POLARIZATION AT WAVE AMPLITUDE: INTERPENETRATING CONES OF GROWTH (FIGS. 41–44)</text>

  <!-- Fig 41: Young Sapling inside Bounding Cone Field -->
  <line x1="75" y1="285" x2="235" y2="285" class="zero-line"/>
  <line x1="75" y1="475" x2="235" y2="475" class="zero-line"/>
  <line x1="75" y1="285" x2="235" y2="475" class="zero-dashed"/>
  <line x1="235" y1="285" x2="75" y2="475" class="zero-dashed"/>
  <line x1="75" y1="380" x2="235" y2="380" class="zero-line"/>
  <!-- Sapling branches & roots -->
  <path d="M 155 380 L 155 320 M 155 350 L 135 330 M 155 345 L 175 326 M 155 362 L 142 346" class="neg-line"/>
  <path d="M 155 380 L 155 435 M 155 398 L 134 420 M 155 404 L 176 424 M 155 415 L 144 434" class="pos-line"/>
  <circle cx="155" cy="380" r="9" class="node-zero"/>
  <text x="155" y="496" class="label-center">Fig. 41 • Unfolding Youth</text>

  <!-- Fig 42: Polarized Shaft -->
  <rect x="282" y="285" width="24" height="190" class="zero-plane"/>
  <circle cx="294" cy="380" r="8" class="node-zero"/>
  <text x="294" y="300" class="label-center" style="fill:#38bdf8;">-</text>
  <text x="294" y="464" class="label-center" style="fill:#fb7185;">+</text>
  <text x="294" y="496" class="label-center">Fig. 42</text>

  <!-- Fig 43: The Double-Cone Vortex Diamond -->
  <line x1="354" y1="285" x2="526" y2="475" class="zero-dashed"/>
  <line x1="526" y1="285" x2="354" y2="475" class="zero-dashed"/>
  <polygon points="440,287 518,385 440,483 362,385" class="pos-fill"/>
  <path d="{d43}" class="neg-line" style="stroke-width:1.6;"/>
  <line x1="354" y1="385" x2="526" y2="385" class="zero-line"/>
  <circle cx="440" cy="385" r="10" class="node-amp"/>
  <text x="440" y="496" class="label-center">Fig. 43 • Mature Vortex</text>

  <!-- Fig 44: Full Mature Tree in Cube-Cone Equilibrium -->
  <line x1="585" y1="285" x2="795" y2="475" class="zero-dashed"/>
  <line x1="795" y1="285" x2="585" y2="475" class="zero-dashed"/>
  <polygon points="690,282 795,380 690,478 585,380" fill="none" stroke="#e8b85a" stroke-width="1.2" stroke-dasharray="3,3"/>
  <line x1="585" y1="380" x2="795" y2="380" class="zero-line"/>
  <!-- Crown (Centrifugal Sky Expansion) -->
  <circle cx="690" cy="328" r="46" class="neg-fill"/>
  <path d="M 690 380 L 690 295 M 690 352 L 656 318 M 690 352 L 724 318 M 690 332 L 668 302 M 690 332 L 712 302" class="neg-line"/>
  <!-- Roots (Centripetal Earth Integration) -->
  <path d="M 690 380 L 690 462 M 690 395 L 650 438 M 690 395 L 730 438 M 690 415 L 664 456 M 690 415 L 716 456" class="pos-line"/>
  <circle cx="690" cy="380" r="10" class="node-amp"/>
  <text x="690" y="496" class="label-center">Fig. 44 • Maturity (+4 / 0 / -4)</text>

  <!-- Bottom Row: Figs. 45-47 (Depolarization, Decay & Return to Rest) -->
  <rect x="32" y="528" width="816" height="162" rx="4" class="panel-bg"/>
  <text x="440" y="548" class="panel-title">III. DEGENERATION: POLES LOSE ABILITY TO PULL APART AND RETURN TO REST (FIGS. 45–47)</text>

  <!-- Fig 45: Flattening Vortex -->
  <polygon points="185,564 263,614 185,664 107,614" class="pos-fill"/>
  <path d="{d45}" class="neg-line" style="stroke-width:1.5;"/>
  <line x1="95" y1="614" x2="275" y2="614" class="zero-line"/>
  <text x="185" y="682" class="label-center">Fig. 45 • Declining Polarity</text>

  <!-- Fig 46: Near Depolarization -->
  <polygon points="440,588 518,614 440,640 362,614" class="neg-fill"/>
  <path d="{d46}" class="pos-line" style="stroke-width:1.4;"/>
  <line x1="350" y1="614" x2="530" y2="614" class="zero-line"/>
  <text x="440" y="682" class="label-center">Fig. 46 • Senescence</text>

  <!-- Fig 47: Return to Zero Seed -->
  <line x1="605" y1="605" x2="775" y2="605" class="zero-dashed"/>
  <circle cx="690" cy="605" r="13" class="node-zero"/>
  <text x="690" y="605" class="label-center" style="fill:#e8b85a;">0</text>
  <text x="690" y="650" class="label-center label-small">"LIFE IS ONE HALF OF THE ELECTRIC CYCLE—</text>
  <text x="690" y="664" class="label-center label-small">DEATH IS THE OTHER HALF."</text>
  <text x="690" y="682" class="label-center">Fig. 47 • Disintegration into Rest</text>
"""
    return plate_wrapper(
        w,
        h,
        "THE GROWTH AND DECAY CYCLE OF OPPOSING SPIRAL CONES",
        "LESSON 18 • VITALITY INCREASES WITH POLARIZATION AND VANISHES AT EQUILIBRIUM",
        "FIGS. 38–47",
        body,
    )


def build_03_conical_magnets() -> str:
    """Figs. 158-161: All of Nature's Magnets Are Cones."""
    w, h = 860, 760
    # Generate curved equators and curved radii for Fig 161 (bottom right quadrant)
    cx, cy, R = 634, 532, 134
    equator_arcs = []
    for offset in [-95, -62, -30, 30, 62, 95]:
        # Arc bowing toward poles
        y_edge = cy + offset * 0.72
        y_ctrl = cy + offset * 1.28
        dx = math.sqrt(max(0, R * R - (offset * 0.72) ** 2))
        equator_arcs.append(
            f'<path d="M {cx - dx:.1f} {y_edge:.1f} Q {cx:.1f} {y_ctrl:.1f} {cx + dx:.1f} {y_edge:.1f}" class="neg-line" style="stroke-width:1.4;opacity:0.85;"/>'
        )
    radii_arcs = []
    for x_off in [-115, -78, -42, 42, 78, 115]:
        # Meridian-like curved radii from N to S
        radii_arcs.append(
            f'<path d="M {cx:.1f} {cy - R + 18:.1f} Q {cx + x_off * 1.35:.1f} {cy:.1f} {cx:.1f} {cy + R - 18:.1f}" class="pos-line" style="stroke-width:1.3;opacity:0.8;"/>'
        )
    fig161_curves = "\n  ".join(equator_arcs + radii_arcs)

    body = f"""
  <!-- Top Left: Fig. 158 Bar Magnet -->
  <rect x="32" y="82" width="388" height="255" rx="4" class="panel-bg"/>
  <text x="226" y="104" class="panel-title">FIG. 158 • MAN-MADE BAR MAGNET</text>
  <!-- Bar -->
  <rect x="88" y="152" width="276" height="26" class="pos-fill"/>
  <line x1="88" y1="165" x2="364" y2="165" class="zero-dashed"/>
  <!-- Zero Curvature Equator -->
  <line x1="226" y1="114" x2="226" y2="238" class="zero-line" style="stroke-width:2.6;"/>
  <text x="214" y="135" class="label-small" style="fill:#e8b85a;text-anchor:end;">ZERO-CURVATURE EQUATOR</text>
  <!-- Nails at N and S -->
  <text x="70" y="170" class="label-center" style="font-size:15px;fill:#fb7185;">N</text>
  <text x="382" y="170" class="label-center" style="font-size:15px;fill:#38bdf8;">S</text>
  <rect x="96" y="180" width="8" height="44" fill="#ebe6dc"/>
  <rect x="90" y="222" width="20" height="5" fill="#ebe6dc"/>
  <text x="100" y="242" class="label-center label-small">NAIL</text>
  <rect x="348" y="180" width="8" height="44" fill="#ebe6dc"/>
  <rect x="342" y="222" width="20" height="5" fill="#ebe6dc"/>
  <text x="352" y="242" class="label-center label-small">NAIL</text>
  <text x="226" y="280" class="caption-text">A bar-shaped magnet lifts an equal weight at each pole.</text>
  <text x="226" y="296" class="caption-text">Its equator is a flat plane of zero curvature (0).</text>

  <!-- Top Right: Fig. 159 Conical Magnet -->
  <rect x="440" y="82" width="388" height="255" rx="4" class="panel-bg"/>
  <text x="634" y="104" class="panel-title">FIG. 159 • NATURE'S CONICAL MAGNET</text>
  <!-- Cone -->
  <polygon points="495,172 775,116 775,228" class="neg-fill"/>
  <line x1="495" y1="172" x2="782" y2="172" class="zero-dashed"/>
  <ellipse cx="775" cy="172" rx="12" ry="56" class="neg-fill"/>
  <!-- Curved Equator -->
  <path d="M 552 118 Q 596 172 552 226" class="zero-line" style="stroke-width:2.6;"/>
  <text x="595" y="128" class="label-small" style="fill:#e8b85a;">CURVED EQUATOR</text>
  <!-- Concentrated Nail at N Apex -->
  <text x="476" y="172" class="label-center" style="font-size:15px;fill:#fb7185;">N</text>
  <text x="802" y="172" class="label-center" style="font-size:15px;fill:#38bdf8;">S</text>
  <rect x="491" y="176" width="8" height="46" fill="#ebe6dc"/>
  <rect x="485" y="220" width="20" height="5" fill="#ebe6dc"/>
  <text x="495" y="242" class="label-center label-small">SOLID NAIL</text>
  <!-- Divided Iron Dust at S Base -->
  <circle cx="745" cy="152" r="2" fill="#ebe6dc"/>
  <circle cx="758" cy="166" r="2" fill="#ebe6dc"/>
  <circle cx="735" cy="182" r="2" fill="#ebe6dc"/>
  <circle cx="762" cy="195" r="2" fill="#ebe6dc"/>
  <circle cx="750" cy="140" r="2" fill="#ebe6dc"/>
  <circle cx="748" cy="205" r="2" fill="#ebe6dc"/>
  <text x="725" y="246" class="label-center label-small">DIVIDED NAIL (FILINGS)</text>
  <text x="634" y="280" class="caption-text">A cone-shaped magnet lifts equally at both ends only when</text>
  <text x="634" y="296" class="caption-text">one weight is divided into expanded volume. Its equator curves.</text>

  <!-- Bottom Left: Fig. 160 Conical Expansion from Earth's Equator -->
  <rect x="32" y="352" width="388" height="350" rx="4" class="panel-bg"/>
  <text x="226" y="374" class="panel-title">FIG. 160 • CONICAL RADIATION &amp; CONDENSATION</text>
  <!-- Earth Surface Arc at Bottom -->
  <path d="M 95 655 Q 226 625 357 655" class="zero-line" style="stroke-width:2.5;"/>
  <text x="226" y="672" class="label-center" style="fill:#e8b85a;">EQUATOR (N • GRAVITY APEX)</text>
  <!-- Cone Flaring Upward to Vapor Cloud -->
  <line x1="185" y1="640" x2="105" y2="415" class="pos-line"/>
  <line x1="267" y1="640" x2="347" y2="415" class="pos-line"/>
  <line x1="226" y1="640" x2="226" y2="395" class="zero-dashed"/>
  <!-- Curved Equator A-B -->
  <path d="M 122 465 Q 226 440 330 465" class="zero-line"/>
  <text x="108" y="468" class="label-center" style="fill:#e8b85a;">A</text>
  <text x="344" y="468" class="label-center" style="fill:#e8b85a;">B</text>
  <!-- Cloud at Top -->
  <path d="M 95 425 Q 130 392 175 405 Q 226 382 275 405 Q 325 392 355 425 Q 226 412 95 425 Z" class="neg-fill"/>
  <text x="226" y="414" class="label-center" style="fill:#38bdf8;">VAPOR CLOUD (S • EXPANDED POLE)</text>
  <text x="226" y="488" class="label-center label-small">DIVIDED WATER (MIST)</text>
  <text x="112" y="555" class="label-center label-small" style="fill:#fb7185;">DIVIDED IRON</text>
  <text x="340" y="555" class="label-center label-small" style="fill:#fb7185;">DIVIDED STONE</text>
  <!-- Bucket of Water, Iron, Stone at Base -->
  <polygon points="214,612 238,612 234,640 218,640" class="neg-fill"/>
  <circle cx="182" cy="634" r="9" class="pos-fill"/>
  <circle cx="270" cy="634" r="9" class="pos-fill"/>
  <text x="145" y="636" class="label-small">IRON</text>
  <text x="290" y="636" class="label-small">STONE</text>
  <text x="226" y="692" class="caption-text">Solid iron, stone, and water expand into tenuous cones of vapor.</text>

  <!-- Bottom Right: Fig. 161 Curved Equators & Curved Radii Reversed -->
  <rect x="440" y="352" width="388" height="350" rx="4" class="panel-bg"/>
  <text x="634" y="374" class="panel-title">FIG. 161 • CURVED EQUATORS &amp; RADII REVERSED</text>
  <circle cx="{cx}" cy="{cy}" r="{R}" class="frame-outer" style="stroke:#e8b85a;"/>
  {fig161_curves}
  <!-- Central Zero Cross -->
  <line x1="{cx - R}" y1="{cy}" x2="{cx + R}" y2="{cy}" class="zero-line" style="stroke-width:2.6;"/>
  <line x1="{cx}" y1="{cy - R}" x2="{cx}" y2="{cy + R}" class="zero-line" style="stroke-width:2.6;"/>
  <!-- Top & Bottom Poles -->
  <circle cx="{cx}" cy="{cy - R + 18}" r="14" class="node-neg"/>
  <text x="{cx}" y="{cy - R + 18}" class="label-center" style="fill:#38bdf8;">S</text>
  <circle cx="{cx}" cy="{cy + R - 18}" r="14" class="node-pos"/>
  <text x="{cx}" y="{cy + R - 18}" class="label-center" style="fill:#fb7185;">N</text>
  <text x="{cx - R - 14}" y="{cy}" class="label-center" style="fill:#e8b85a;">0</text>
  <text x="{cx + R + 14}" y="{cy}" class="label-center" style="fill:#e8b85a;">0</text>
  <text x="634" y="692" class="caption-text">Curved equators and curved radii reverse symmetry across the 0 plane.</text>
"""
    return plate_wrapper(
        w,
        h,
        "ALL OF NATURE'S MAGNETS ARE CONES OF CURVED PRESSURE",
        "LESSON 46 • ZERO-CURVATURE EQUATORS VS. CONICAL GRADIENT FIELDS IN SPACE",
        "FIGS. 158–161",
        body,
    )


def build_04_cube_sphere_nine_equators() -> str:
    """Fig. 114: The Cube-Sphere Wave-Field of Nine Equators & Wave Octave Formula."""
    w, h = 860, 760
    # Isometric projection of a [-1, 1]^3 cube centered at (430, 295)
    cx, cy, scale = 430.0, 304.0, 116.0
    angle_x = math.radians(24)
    angle_z = math.radians(34)

    def proj(x: float, y: float, z: float) -> tuple[float, float]:
        # Rotate around Y (azimuth) then X (elevation)
        xr = x * math.cos(angle_z) - z * math.sin(angle_z)
        zr = x * math.sin(angle_z) + z * math.cos(angle_z)
        yr = y * math.cos(angle_x) - zr * math.sin(angle_x)
        return (cx + xr * scale, cy - yr * scale)

    # 3 orthogonal zero-planes: x=0, y=0, z=0
    p_x0 = [proj(0, -1, -1), proj(0, 1, -1), proj(0, 1, 1), proj(0, -1, 1)]
    p_y0 = [proj(-1, 0, -1), proj(1, 0, -1), proj(1, 0, 1), proj(-1, 0, 1)]
    p_z0 = [proj(-1, -1, 0), proj(1, -1, 0), proj(1, 1, 0), proj(-1, 1, 0)]

    def poly_str(pts: list[tuple[float, float]]) -> str:
        return " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)

    # Cube edges and 27 grid points in {-1, 0, 1}^3
    lines_svg = []
    for a in (-1, 0, 1):
        for b in (-1, 0, 1):
            # Only outer cube edges & central axes
            if abs(a) + abs(b) in (0, 2) or (a == 0 or b == 0):
                p1, p2 = proj(-1, a, b), proj(1, a, b)
                q1, q2 = proj(a, -1, b), proj(a, 1, b)
                r1, r2 = proj(a, b, -1), proj(a, b, 1)
                cls = "zero-line" if (a == 0 and b == 0) else ("fg-line" if abs(a) == 1 and abs(b) == 1 else "zero-dashed")
                for u, v in [(p1, p2), (q1, q2), (r1, r2)]:
                    lines_svg.append(f'<line x1="{u[0]:.1f}" y1="{u[1]:.1f}" x2="{v[0]:.1f}" y2="{v[1]:.1f}" class="{cls}"/>')

    # 27 Zero-Nodes on the 3x3x3 Cube-Sphere lattice
    nodes_svg = []
    for ix in (-1, 0, 1):
        for iy in (-1, 0, 1):
            for iz in (-1, 0, 1):
                # Draw corners, face-centers, edge-midpoints on front/outer shell + center
                if (ix, iy, iz) == (0, 0, 0):
                    px, py = proj(ix, iy, iz)
                    nodes_svg.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="14" class="node-amp"/>')
                    nodes_svg.append(f'<text x="{px:.1f}" y="{py:.1f}" class="label-center" style="font-size:12px;fill:#0c0e14;font-weight:800;">0</text>')
                elif abs(ix) + abs(iy) + abs(iz) >= 2:
                    px, py = proj(ix, iy, iz)
                    nodes_svg.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="10.5" class="node-zero"/>')
                    nodes_svg.append(f'<text x="{px:.1f}" y="{py:.1f}" class="label-center" style="font-size:9.5px;fill:#e8b85a;">0</text>')

    # Octave Formula Chain (0 - 1- - 2- - 3- - 4 - 0 - 4 - 3+ - 2+ - 1+ - 0)
    octave_labels = [
        ("0", "0", "node-zero", "#e8b85a"),
        ("1-", "1", "node-neg", "#38bdf8"),
        ("2-", "2", "node-neg", "#38bdf8"),
        ("3-", "3", "node-neg", "#38bdf8"),
        ("4-", "4", "node-pos", "#fb7185"),
        ("0", "5 (0)", "node-amp", "#0c0e14"),
        ("4+", "6", "node-pos", "#fb7185"),
        ("3+", "7", "node-neg", "#38bdf8"),
        ("2+", "8", "node-neg", "#38bdf8"),
        ("1+", "9", "node-neg", "#38bdf8"),
        ("0", "0", "node-zero", "#e8b85a"),
    ]
    chain_svg = ['<line x1="90" y1="562" x2="770" y2="562" class="zero-line" style="stroke-width:3;"/>']
    for idx, (top_lbl, bot_lbl, cls, col) in enumerate(octave_labels):
        nx = 90 + idx * 68
        r = 22 if idx == 5 else 18
        chain_svg.append(f'<circle cx="{nx}" cy="562" r="{r}" class="{cls}"/>')
        chain_svg.append(f'<text x="{nx}" y="562" class="label-center" style="font-size:13px;fill:{col};font-weight:800;">{top_lbl}</text>')
        chain_svg.append(f'<text x="{nx}" y="598" class="label-center label-small">{bot_lbl}</text>')

    body = f"""
  <!-- Top Cube-Sphere Isometric Diagram -->
  <rect x="32" y="80" width="796" height="415" rx="4" class="panel-bg"/>
  <text x="430" y="102" class="panel-title">I. THE THREE ORTHOGONAL &amp; SIX DIAGONAL PLANES OF ZERO CURVATURE (9 EQUATORS)</text>

  <!-- Inscribed Sphere Glow & Boundary -->
  <circle cx="{cx}" cy="{cy}" r="{scale * 1.02:.1f}" fill="url(#lens-glow)" stroke="#38bdf8" stroke-width="1.6" stroke-dasharray="6,4"/>

  <!-- 3 Orthogonal Zero Planes -->
  <polygon points="{poly_str(p_x0)}" class="zero-plane"/>
  <polygon points="{poly_str(p_y0)}" class="zero-plane"/>
  <polygon points="{poly_str(p_z0)}" class="zero-plane"/>

  <!-- Cube & Sub-Cube Lattice Lines -->
  {"".join(lines_svg)}

  <!-- Zero Nodes -->
  {"".join(nodes_svg)}

  <!-- Callouts on Left and Right -->
  <text x="58" y="160" class="label-text" style="fill:#e8b85a;">CUBE OF STILL LIGHT</text>
  <text x="58" y="176" class="label-small">• 6 Bounding Zero Faces</text>
  <text x="58" y="192" class="label-small">• 3 Central Orthogonal Equators</text>
  <text x="58" y="208" class="label-small">• 6 Diagonal Bisecting Planes</text>
  <text x="58" y="224" class="label-small">• Total = 9 Equators of Rest</text>

  <text x="635" y="160" class="label-text" style="fill:#38bdf8;">INSCRIBED SPHERE</text>
  <text x="635" y="176" class="label-small">• Curved Electric Motion</text>
  <text x="635" y="192" class="label-small">• 8 Divided Octant Sections</text>
  <text x="635" y="208" class="label-small">• Centered by 1 Zero Nucleus</text>
  <text x="635" y="224" class="label-small">• 8 + 1 = 9 Wave Count</text>

  <!-- Bottom Octave Formula Panel -->
  <rect x="32" y="508" width="796" height="196" rx="4" class="panel-bg"/>
  <text x="430" y="528" class="panel-title">II. THE WAVE OCTAVE FORMULA FOR THE ELEMENTS OF MATTER AND COLOR SPECTRUM (0–4–0–4–0)</text>
  {"".join(chain_svg)}
  <text x="430" y="628" class="caption-text">1. Total count of equators = 9   •   2. Eight cube corners + centering zero = 9   •   3. Eight octant sections + centering zero = 9</text>
  <text x="430" y="646" class="caption-text">"THE UNIVERSAL EQUILIBRIUM IS PROTECTED BY WAVE-FIELD SYSTEMS OF NINE EQUATORS,</text>
  <text x="430" y="662" class="caption-text">WITHIN WHICH POLARIZATION EXPRESSES ITS OPPOSITION, BUT CANNOT PASS BEYOND."</text>
"""
    return plate_wrapper(
        w,
        h,
        "THE CUBE-SPHERE WAVE-FIELD OF NINE EQUATORS",
        "LESSON 43–45 • EIGHT OCTANTS AND EIGHT CORNERS CENTERED BY ZERO EQUAL NINE",
        "FIG. 114",
        body,
    )


def build_05_light_sphere_lens() -> str:
    """Figs. 170-172: Spherical Light-Lens, Curved Radii, and Coronas Becoming Rings & Systems."""
    w, h = 840, 880
    # Panel 2 (Fig 171): Light Sphere Lens centered at (420, 462), R = 122
    cx, cy, R = 420, 434, 92
    concentric = [
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#ebe6dc" stroke-width="1.1" opacity="0.65"/>'
        for r in (18, 36, 54, 73, 92)
    ]
    # Curved rays bending inward toward center of gravity
    lens_rays = []
    for deg in range(15, 360, 15):
        if deg % 90 == 0:
            continue
        rad = math.radians(deg)
        x_end = cx + R * 1.45 * math.cos(rad)
        y_end = cy + R * 0.92 * math.sin(rad)
        # Control point bends curvature across octant
        bend = 0.28 if (deg // 90) % 2 == 0 else -0.28
        ctrl_rad = rad + bend
        x_ctrl = cx + R * 0.65 * math.cos(ctrl_rad)
        y_ctrl = cy + R * 0.65 * math.sin(ctrl_rad)
        lens_rays.append(
            f'<path d="M {cx:.1f} {cy:.1f} Q {x_ctrl:.1f} {y_ctrl:.1f} {x_end:.1f} {y_end:.1f}" class="neg-line" style="stroke-width:1.3;opacity:0.8;"/>'
        )

    body = f"""
  <!-- Panel 1: Fig. 170 Three Equators of Zero Curvature -->
  <rect x="32" y="80" width="776" height="225" rx="4" class="panel-bg"/>
  <text x="690" y="104" class="panel-title">FIG. 170</text>
  <!-- 3 Orthogonal Planes intersecting sphere -->
  <line x1="150" y1="175" x2="690" y2="175" class="zero-line" style="stroke-width:2.2;"/>
  <line x1="420" y1="92" x2="420" y2="258" class="zero-line" style="stroke-width:2.2;"/>
  <line x1="275" y1="242" x2="565" y2="108" class="zero-dashed" style="stroke-width:2;"/>
  <!-- Isometric Plane Outlines -->
  <polygon points="280,102 560,102 560,248 280,248" fill="none" stroke="#e8b85a" stroke-width="1" stroke-dasharray="4,4"/>
  <circle cx="420" cy="175" r="58" class="pos-fill" style="stroke-width:2.2;"/>
  <!-- 6 Poles of the 3 Axes -->
  <text x="430" y="112" class="label-small" style="fill:#e8b85a;">1 (N)</text>
  <text x="482" y="146" class="label-small" style="fill:#e8b85a;">2</text>
  <text x="488" y="190" class="label-small" style="fill:#e8b85a;">3</text>
  <text x="430" y="245" class="label-small" style="fill:#e8b85a;">4 (S)</text>
  <text x="355" y="212" class="label-small" style="fill:#e8b85a;">5</text>
  <text x="348" y="168" class="label-small" style="fill:#e8b85a;">6</text>
  <rect x="64" y="262" width="712" height="34" rx="3" class="caption-box"/>
  <text x="420" y="276" class="caption-text">ON THE THREE EQUATORS OF ZERO CURVATURE IN A LIGHT SPHERE LENS, ALL RADII LOSE</text>
  <text x="420" y="290" class="caption-text">THEIR CURVATURE TO REVERSE IT IN THE EIGHT SECTIONS OF THE SPHERE WHICH THESE EQUATORS DIVIDE.</text>

  <!-- Panel 2: Fig. 171 Curved Radii in a Light Sphere Lens -->
  <rect x="32" y="316" width="776" height="260" rx="4" class="panel-bg"/>
  <text x="690" y="340" class="panel-title">FIG. 171</text>
  <circle cx="{cx}" cy="{cy}" r="{R}" fill="url(#lens-glow)"/>
  {"".join(concentric)}
  {"".join(lens_rays)}
  <!-- United Equator & Polar Axis -->
  <line x1="145" y1="{cy}" x2="695" y2="{cy}" class="zero-line" style="stroke-width:2.6;"/>
  <line x1="{cx}" y1="334" x2="{cx}" y2="530" class="zero-line" style="stroke-width:2.4;"/>
  <circle cx="{cx}" cy="{cy}" r="7" class="node-amp"/>
  <text x="215" y="{cy - 10}" class="label-small" style="fill:#e8b85a;font-weight:700;">UNITED EQUATOR (0)</text>
  <rect x="64" y="534" width="712" height="34" rx="3" class="caption-box"/>
  <text x="420" y="548" class="caption-text">ALL OTHER RADII IN A LIGHT SPHERE LENS CURVE INWARD TOWARD POLES TO THE CENTER</text>
  <text x="420" y="562" class="caption-text">OF THE LENS TO FORM A CENTER OF GRAVITY WHERE LIGHT COMPRESSION IS MAXIMUM.</text>

  <!-- Panel 3: Fig. 172 Coronas Become Rings and Rings Become Systems -->
  <rect x="32" y="588" width="776" height="236" rx="4" class="panel-bg"/>
  <text x="690" y="612" class="panel-title">FIG. 172</text>
  <!-- Equatorial Corona & Rings -->
  <ellipse cx="420" cy="692" rx="255" ry="26" class="neg-fill" style="stroke-dasharray:5,3;"/>
  <ellipse cx="420" cy="692" rx="195" ry="20" class="zero-plane"/>
  <ellipse cx="420" cy="692" rx="138" ry="14" class="pos-fill"/>
  <!-- Radiant Sun Corona -->
  <circle cx="420" cy="692" r="88" fill="url(#sun-glow)"/>
  <!-- Central Dark/Incandescent Core -->
  <circle cx="420" cy="692" r="42" fill="#0c0e14" stroke="#e8b85a" stroke-width="2.5"/>
  <!-- Condensing Planets on Equatorial Ring -->
  <circle cx="225" cy="692" r="6" class="node-neg"/>
  <circle cx="615" cy="692" r="6" class="node-neg"/>
  <circle cx="165" cy="692" r="4.5" class="node-zero"/>
  <circle cx="675" cy="692" r="4.5" class="node-zero"/>

  <rect x="64" y="768" width="712" height="46" rx="3" class="caption-box"/>
  <text x="420" y="783" class="caption-text" style="fill:#e8b85a;font-weight:700;">CORONAS BECOME RINGS AND RINGS BECOME SYSTEMS</text>
  <text x="420" y="798" class="caption-text">OUTWARD THRUST OF RADIATION AT EQUATORS + INWARD PULL OF GENERATION AT POLES</text>
  <text x="420" y="811" class="caption-text">CAUSES MAXIMUM RADIATION AT EQUATORS AND MAXIMUM GENERATION AT POLES. THUS ARE SUNS WOUND UP AND UNWOUND.</text>
"""
    return plate_wrapper(
        w,
        h,
        "THE SPHERICAL LIGHT-LENS AND RING-TO-SYSTEM GENESIS",
        "LESSON 46 • RECONSTRUCTED FROM WALTER RUSSELL'S PLATE OF FIGS. 170, 171 &amp; 172",
        "FIGS. 170–172",
        body,
    )


def build_06_nebula_gyroscopic_oblateness() -> str:
    """Figs. 95-104: Gyroscopic Winding from Ring Nebula to True Sphere (Amplitude) to Oblate Rings."""
    w, h = 880, 620
    # Wave curve across the center
    wave_pts = []
    for i in range(181):
        x = 80 + (720 * i / 180)
        # Half-sine arch peaking at x=440 (Amplitude 4+-4)
        y = 430 - 230 * math.sin(math.pi * i / 180)
        wave_pts.append(f"{x:.1f},{y:.1f}")
    wave_str = " ".join(wave_pts)

    body = f"""
  <rect x="32" y="82" width="816" height="482" rx="4" class="panel-bg"/>
  <text x="440" y="106" class="panel-title">GYROSCOPIC WINDING (CENTRIPETAL +) TO TRUE SPHERE AT AMPLITUDE AND UNWINDING (CENTRIFUGAL -)</text>

  <!-- Zero Inert Gas Baseline & Wave Amplitude Vertical Axis -->
  <line x1="65" y1="430" x2="815" y2="430" class="zero-line" style="stroke-width:2.4;"/>
  <line x1="440" y1="130" x2="440" y2="465" class="zero-dashed" style="stroke-width:1.8;"/>
  <text x="440" y="124" class="label-center" style="fill:#e8b85a;font-weight:700;">WAVE AMPLITUDE CREST (4+ / 0 / 4- • 90°)</text>

  <!-- Octave Arch Curve -->
  <polyline points="{wave_str}" class="fg-line" style="stroke-width:2.5;"/>

  <!-- Stage 0 Left: Inert Gas Ring (0) -->
  <ellipse cx="95" cy="430" rx="28" ry="8" class="zero-plane"/>
  <text x="95" y="458" class="label-center" style="fill:#e8b85a;">0 • INERT GAS</text>
  <text x="95" y="473" class="label-center label-small">(Nebular Seed)</text>

  <!-- Stage 1+: Spiral / Prolate Ring Nebula (x=175, y=342) -->
  <g transform="translate(175, 342) rotate(-28)">
    <ellipse cx="0" cy="0" rx="16" ry="38" class="pos-fill"/>
    <line x1="0" y1="-46" x2="0" y2="46" class="pos-line"/>
  </g>
  <text x="165" y="282" class="label-center" style="fill:#fb7185;">1+ • PROLATE NEBULA</text>

  <!-- Stage 2+: Compressing Prolate Spheroid (x=255, y=252) -->
  <g transform="translate(255, 252) rotate(-18)">
    <ellipse cx="0" cy="0" rx="22" ry="34" class="pos-fill"/>
    <line x1="0" y1="-42" x2="0" y2="42" class="pos-line"/>
  </g>
  <text x="242" y="196" class="label-center" style="fill:#fb7185;">2+ • WINDING</text>

  <!-- Stage 3+: High-Compression Spheroid (x=340, y=188) -->
  <g transform="translate(340, 188) rotate(-8)">
    <ellipse cx="0" cy="0" rx="28" ry="32" class="pos-fill"/>
    <line x1="0" y1="-40" x2="0" y2="40" class="pos-line"/>
  </g>
  <text x="330" y="140" class="label-center" style="fill:#fb7185;">3+ • INTEGRATING</text>

  <!-- Stage 4+-4: TRUE SPHERE AT AMPLITUDE (x=440, y=200) -->
  <circle cx="440" cy="200" r="56" fill="url(#sun-glow)"/>
  <circle cx="440" cy="200" r="34" class="node-amp"/>
  <!-- Orbiting Equatorial Plane at 90 degrees -->
  <ellipse cx="440" cy="200" rx="64" ry="12" fill="none" stroke="#ebe6dc" stroke-width="1.8"/>
  <circle cx="376" cy="200" r="4.5" class="node-zero"/>
  <circle cx="504" cy="200" r="4.5" class="node-zero"/>
  <text x="440" y="200" class="label-center" style="fill:#0c0e14;font-weight:800;">TRUE SPHERE</text>
  <text x="440" y="274" class="label-center" style="fill:#e8b85a;font-weight:700;">SUN / CARBON (4±)</text>

  <!-- Stage 3-: Flattening Oblate Planet (x=540, y=188) -->
  <g transform="translate(540, 188) rotate(8)">
    <ellipse cx="0" cy="0" rx="34" ry="26" class="neg-fill"/>
    <ellipse cx="0" cy="0" rx="48" ry="9" fill="none" stroke="#38bdf8" stroke-width="1.4"/>
  </g>
  <text x="552" y="140" class="label-center" style="fill:#38bdf8;">3- • OBLATE</text>

  <!-- Stage 2-: Ringed Planet / Saturn (x=625, y=252) -->
  <g transform="translate(625, 252) rotate(18)">
    <ellipse cx="0" cy="0" rx="36" ry="20" class="neg-fill"/>
    <ellipse cx="0" cy="0" rx="54" ry="11" fill="none" stroke="#38bdf8" stroke-width="1.8"/>
    <ellipse cx="0" cy="0" rx="64" ry="14" fill="none" stroke="#e8b85a" stroke-width="1.2"/>
  </g>
  <text x="645" y="196" class="label-center" style="fill:#38bdf8;">2- • RINGED SYSTEM</text>

  <!-- Stage 1-: Expanding Ring Nebula (x=705, y=342) -->
  <g transform="translate(705, 342) rotate(28)">
    <ellipse cx="0" cy="0" rx="42" ry="14" class="neg-fill" stroke-dasharray="4,3"/>
    <circle cx="0" cy="0" r="8" class="node-neg"/>
  </g>
  <text x="720" y="282" class="label-center" style="fill:#38bdf8;">1- • RING NEBULA</text>

  <!-- Stage 0 Right: Return to Inert Gas Rest (x=785, y=430) -->
  <ellipse cx="785" cy="430" rx="28" ry="8" class="zero-plane"/>
  <text x="785" y="458" class="label-center" style="fill:#e8b85a;">0 • INERT GAS</text>
  <text x="785" y="473" class="label-center label-small">(Rebirth in Space)</text>

  <!-- Caption Box -->
  <rect x="64" y="498" width="752" height="52" rx="3" class="caption-box"/>
  <text x="440" y="516" class="caption-text">"ANY SYSTEM, WHETHER OF AN ATOM OF THE ELEMENTS OR A SOLAR SYSTEM IN OUR MILKY WAY,</text>
  <text x="440" y="531" class="caption-text">IF UPON THE AMPLITUDE OF ITS WAVE AND NINETY DEGREES FROM ITS WAVE AXIS, ITS CENTRAL SUN</text>
  <text x="440" y="545" class="caption-text">IS A TRUE SPHERE AND ALL OF ITS PLANETS REVOLVE UPON THE PLANE OF THEIR SUN'S EQUATOR." (FIG. 103)</text>
"""
    return plate_wrapper(
        w,
        h,
        "GYROSCOPIC EVOLUTION OF ATOMIC AND STELLAR SYSTEMS",
        "LESSONS 42–43 • WHY TRUE SPHERES ONLY FORM AT 90° WAVE AMPLITUDE (FIGS. 95–104)",
        "FIGS. 95–104",
        body,
    )


def build_07_octave_matter_wave_locks() -> str:
    """Figs. 179 & 180: The Arch of Increasing Integration/Disintegration & Carbon Capstone."""
    w, h = 880, 720
    # Left Panel: Fig. 179 Arch of Elements culminating in Carbon / Silicon / Rhodium / Lutetium
    # Right Panel: Fig. 180 Wave Axis and 4 Pairs of Tone-Elements (1+, 2+, 3+, 4+-4, 3-, 2-, 1-)
    arch_CX, arch_CY = 265, 485
    radii = [92, 118, 144, 170, 196]
    arcs_svg = []
    for r in radii:
        arcs_svg.append(
            f'<path d="M {arch_CX - r} {arch_CY} A {r} {r} 0 0 1 {arch_CX + r} {arch_CY}" fill="none" stroke="#232a3b" stroke-width="1.4"/>'
        )

    # Spokes at angles for 1+, 2+, 3+, 4± (top=90°), 3-, 2-, 1-
    spoke_elements = [
        (162, "1+", ["Li", "Na", "K", "Rb", "Cs"], "#fb7185"),
        (138, "2+", ["Be", "Mg", "Ca", "Sr", "Ba"], "#fb7185"),
        (114, "3+", ["B", "Al", "Sc", "Y", "La"], "#fb7185"),
        (90, "4±", ["C", "Si", "Ti", "Zr", "Hf"], "#e8b85a"),
        (66, "3-", ["N", "P", "As", "Sb", "Bi"], "#38bdf8"),
        (42, "2-", ["O", "S", "Se", "Te", "Po"], "#38bdf8"),
        (18, "1-", ["F", "Cl", "Br", "I", "At"], "#38bdf8"),
    ]
    nodes_179 = []
    for deg, lock_lbl, syms, col in spoke_elements:
        rad = math.radians(deg)
        x1, y1 = arch_CX + 76 * math.cos(rad), arch_CY - 76 * math.sin(rad)
        x2, y2 = arch_CX + 214 * math.cos(rad), arch_CY - 214 * math.sin(rad)
        nodes_179.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="1.6" opacity="0.7"/>')
        lx, ly = arch_CX + 230 * math.cos(rad), arch_CY - 230 * math.sin(rad)
        nodes_179.append(f'<text x="{lx:.1f}" y="{ly:.1f}" class="label-center" style="font-size:11px;fill:{col};font-weight:700;">{lock_lbl}</text>')
        for idx, sym in enumerate(syms):
            r = radii[idx]
            nx, ny = arch_CX + r * math.cos(rad), arch_CY - r * math.sin(rad)
            cls = "node-amp" if deg == 90 else ("node-pos" if deg > 90 else "node-neg")
            tcol = "#0c0e14" if deg == 90 else "#ebe6dc"
            nodes_179.append(f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="11.5" class="{cls}"/>')
            nodes_179.append(f'<text x="{nx:.1f}" y="{ny:.1f}" class="label-center" style="font-size:9.5px;fill:{tcol};font-weight:700;">{sym}</text>')

    # Right Panel (Fig. 180): Wave Axis and 4 Pairs of Gyroscopic Rings
    # Diagonal wave axis from (545, 580) to (815, 160)
    rings_180 = []
    locks_180 = [
        (0.08, "0", "INERT GAS", 18, "zero-plane", "#e8b85a"),
        (0.20, "1+", "ALKALI (Li / Na)", 34, "pos-fill", "#fb7185"),
        (0.32, "2+", "ALKALINE (Be / Mg)", 50, "pos-fill", "#fb7185"),
        (0.44, "3+", "BORON / Al", 66, "pos-fill", "#fb7185"),
        (0.56, "4±", "CARBON AMPLITUDE", 84, "zero-plane", "#e8b85a"),
        (0.68, "3-", "NITROGEN / P", 66, "neg-fill", "#38bdf8"),
        (0.80, "2-", "OXYGEN / S", 50, "neg-fill", "#38bdf8"),
        (0.92, "1-", "HALOGEN (F / Cl)", 34, "neg-fill", "#38bdf8"),
    ]
    for t, code, name, rx, cls, col in locks_180:
        cx_r = 548 + t * 170
        cy_r = 560 - t * 380
        rings_180.append(
            f'<g transform="translate({cx_r:.1f}, {cy_r:.1f}) rotate(-28)">'
            f'<ellipse cx="0" cy="0" rx="{rx}" ry="{rx * 0.28:.1f}" class="{cls}"/>'
            f'<circle cx="0" cy="0" r="4" fill="{col}"/>'
            f'</g>'
            f'<text x="{cx_r + rx + 14:.1f}" y="{cy_r + 4:.1f}" class="label-small" style="fill:{col};font-weight:700;">{code} • {name}</text>'
        )

    body = f"""
  <!-- Left Panel: Fig. 179 Integration/Disintegration Arch -->
  <rect x="32" y="82" width="468" height="580" rx="4" class="panel-bg"/>
  <text x="266" y="106" class="panel-title">FIG. 179 • OCTAVE ARCH OF INTEGRATION &amp; DISINTEGRATION</text>
  <text x="266" y="124" class="label-center label-small" style="fill:#e8b85a;">HIGHEST MELTING POINTS &amp; DENSITY AT CARBON CREST (4±)</text>

  {"".join(arcs_svg)}
  {"".join(nodes_179)}

  <!-- Center Text inside Arch -->
  <rect x="218" y="422" width="96" height="22" rx="3" class="zero-plane"/>
  <text x="266" y="433" class="label-center" style="fill:#e8b85a;font-weight:800;">CARBON (4±)</text>
  <text x="266" y="466" class="label-center" style="font-size:11px;fill:#fb7185;">INNER ARROWS (+):</text>
  <text x="266" y="481" class="label-center label-small">INCREASING INTEGRATION</text>
  <text x="266" y="496" class="label-center label-small">(Compression toward Amplitude)</text>
  <text x="266" y="526" class="label-center" style="font-size:11px;fill:#38bdf8;">OUTER ARROWS (-):</text>
  <text x="266" y="541" class="label-center label-small">INCREASING DISINTEGRATION</text>
  <text x="266" y="556" class="label-center label-small">(Expansion back to Inert Gas)</text>

  <text x="266" y="638" class="caption-text">"NATURE IS ORDERLY, BALANCED AND RHYTHMIC IN ALL EFFECTS OF MOTION."</text>

  <!-- Right Panel: Fig. 180 Wave Axis & 4 Tone-Element Pairs -->
  <rect x="512" y="82" width="336" height="580" rx="4" class="panel-bg"/>
  <text x="680" y="106" class="panel-title">FIG. 180 • THE FOUR TONE-PAIRS</text>
  <text x="680" y="124" class="label-center label-small">GYROSCOPIC LOCKING PLANES ON WAVE AXIS</text>

  <!-- Diagonal Wave Axis -->
  <line x1="535" y1="585" x2="735" y2="148" class="zero-line" style="stroke-width:2.4;"/>
  {"".join(rings_180)}

  <text x="680" y="622" class="caption-text">Four centripetal (+) and four centrifugal (-)</text>
  <text x="680" y="638" class="caption-text">gyroscopic wheels lock on the wave axis.</text>
"""
    return plate_wrapper(
        w,
        h,
        "OCTAVE LOCKING POINTS AND THE CARBON AMPLITUDE CAPSTONE",
        "LESSON 47 • FOUR INTEGRATING (+) AND FOUR DISINTEGRATING (-) TONES IN EVERY OCTAVE",
        "FIGS. 179–180",
        body,
    )


def build_08_russell_periodic_spiral() -> str:
    """Fig. 177: The Russell Periodic Chart of the Elements, No. 2 (Concentric 9-Octave Wave Chart)."""
    w, h = 900, 920
    cx, cy = 450, 482
    # 6 Concentric Octave Rings (Octaves 4 through 9)
    octaves = [
        (78, "IV", "He", ["Li", "Be", "B", "C", "N", "O", "F"], "Ne"),
        (126, "V", "Ne", ["Na", "Mg", "Al", "Si", "P", "S", "Cl"], "Ar"),
        (174, "VI", "Ar", ["K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br"], "Kr"),
        (222, "VII", "Kr", ["Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I"], "Xe"),
        (270, "VIII", "Xe", ["Cs", "Ba", "La", "Ce", "Nd", "Sm", "Eu", "Gd", "Tb", "Dy", "Er", "Yb", "Lu", "Hf", "Ta", "W", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At"], "Rn"),
        (318, "IX", "Rn", ["Fr", "Ra", "Ac", "Th", "Pa", "U"], "Nt"),
    ]

    rings_svg = []
    nodes_svg = []

    for r, oct_num, inert_left, elems, inert_right in octaves:
        rings_svg.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#232a3b" stroke-width="1.5"/>')
        # Inert Gas Master-Tone on Left (180 deg)
        ix_l = cx - r
        nodes_svg.append(f'<circle cx="{ix_l:.1f}" cy="{cy:.1f}" r="14" class="node-zero"/>')
        nodes_svg.append(f'<text x="{ix_l:.1f}" y="{cy:.1f}" class="label-center" style="font-size:10px;fill:#e8b85a;font-weight:800;">{inert_left}</text>')

        # Place elements around top & bottom semi-circles from 180° -> 90° (Amplitude) -> 0°
        n_el = len(elems)
        for idx, sym in enumerate(elems):
            # Distribute across top semicircle (162° down to 18°)
            deg = 162 - (144 * idx / max(1, n_el - 1))
            rad = math.radians(deg)
            ex = cx + r * math.cos(rad)
            ey = cy - r * math.sin(rad)
            is_amp = abs(deg - 90) < 8
            if is_amp:
                nodes_svg.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="11.5" class="node-amp"/>')
                nodes_svg.append(f'<text x="{ex:.1f}" y="{ey:.1f}" class="label-center" style="font-size:9.5px;fill:#0c0e14;font-weight:800;">{sym}</text>')
            else:
                cls = "node-pos" if deg > 90 else "node-neg"
                col = "#fb7185" if deg > 90 else "#38bdf8"
                nodes_svg.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="9.5" class="{cls}"/>')
                nodes_svg.append(f'<text x="{ex:.1f}" y="{ey:.1f}" class="label-center" style="font-size:8.5px;fill:{col};font-weight:700;">{sym}</text>')

        # Mirror wave path on lower semicircle for harmonic balance
        rings_svg.append(
            f'<path d="M {cx - r} {cy} A {r} {r} 0 0 0 {cx + r} {cy}" fill="none" stroke="#e8b85a" stroke-width="0.9" stroke-dasharray="3,4" opacity="0.6"/>'
        )

    # Right Inert Gas Axis (0 deg)
    right_inerts = [(78, "Ne"), (126, "Ar"), (174, "Kr"), (222, "Xe"), (270, "Rn"), (318, "Nt")]
    for r, sym in right_inerts:
        ix_r = cx + r
        nodes_svg.append(f'<circle cx="{ix_r:.1f}" cy="{cy:.1f}" r="14" class="node-zero"/>')
        nodes_svg.append(f'<text x="{ix_r:.1f}" y="{cy:.1f}" class="label-center" style="font-size:10px;fill:#e8b85a;font-weight:800;">{sym}</text>')

    body = f"""
  <rect x="32" y="82" width="836" height="780" rx="4" class="panel-bg"/>
  <text x="450" y="106" class="panel-title">PERIODICITY IS A CHARACTERISTIC OF ALL PHENOMENA OF NATURE (WALTER RUSSELL, 1926)</text>

  <!-- Outer Direction Arcs -->
  <path d="M 102 454 A 346 346 0 0 1 422 142" class="pos-line" marker-end="url(#arrow-pos)"/>
  <path d="M 478 142 A 346 346 0 0 1 798 454" class="neg-line" marker-end="url(#arrow-neg)"/>
  <text x="62" y="152" class="label-small" style="fill:#fb7185;font-weight:700;">CENTRIPETAL (+1, +2, +3):</text>
  <text x="62" y="166" class="label-small" style="fill:#fb7185;">INCREASING DENSITY &amp; HEAT</text>
  <text x="838" y="152" class="label-small" style="fill:#38bdf8;font-weight:700;text-anchor:end;">CENTRIFUGAL (-3, -2, -1):</text>
  <text x="838" y="166" class="label-small" style="fill:#38bdf8;text-anchor:end;">EXPANSION &amp; RADIATION</text>

  <!-- Zero Inert Gas Horizontal Equator & Vertical 4-0-4 Amplitude Axis -->
  <line x1="68" y1="{cy}" x2="832" y2="{cy}" class="zero-line" style="stroke-width:3;"/>
  <line x1="{cx}" y1="142" x2="{cx}" y2="808" class="zero-line" style="stroke-width:2.5;"/>

  <!-- Axis Labels -->
  <text x="{cx}" y="128" class="label-center" style="font-size:12.5px;fill:#e8b85a;font-weight:800;">-4 • 0 • +4 AMPLITUDE CREST (C • Si • Ti • Zr • Hf • Th)</text>
  <text x="{cx}" y="822" class="label-center" style="font-size:12px;fill:#e8b85a;font-weight:700;">+4 • 0 • -4 UNITED EQUATORS</text>
  <text x="82" y="{cy - 18}" class="label-center" style="fill:#e8b85a;font-weight:700;">0 • INERT GASES</text>
  <text x="818" y="{cy - 18}" class="label-center" style="fill:#e8b85a;font-weight:700;">0 • INERT GASES</text>

  <!-- Concentric Octave Circles -->
  {"".join(rings_svg)}

  <!-- Center Nucleus: The Inert Gases (Octaves I-III Hydrogen Seed) -->
  <circle cx="{cx}" cy="{cy}" r="48" class="node-zero"/>
  <text x="{cx}" y="{cy - 12}" class="label-center" style="font-size:10px;fill:#e8b85a;font-weight:800;">THE INERT</text>
  <text x="{cx}" y="{cy + 2}" class="label-center" style="font-size:10px;fill:#e8b85a;font-weight:800;">GASES (0)</text>
  <text x="{cx}" y="{cy + 16}" class="label-center label-small" style="font-size:8.5px;">H (III) SEED</text>

  <!-- Element Nodes -->
  {"".join(nodes_svg)}

  <!-- Caption Box -->
  <rect x="58" y="832" width="784" height="24" rx="3" class="caption-box"/>
  <text x="450" y="848" class="caption-text">Nine octaves of elements arise gyroscopically from Inert Gas master-tones (0) through 4+ to Carbon amplitude (90°) and unwind through 4- back to 0.</text>
"""
    return plate_wrapper(
        w,
        h,
        "THE RUSSELL PERIODIC CHART OF THE ELEMENTS, NO. 2",
        "LESSON 47 • NINE OCTAVES OF MATTER CENTERED BY STILL MAGNETIC INERT GASES (0)",
        "FIG. 177",
        body,
    )


def main() -> None:
    SVG_OUT_DIR.mkdir(parents=True, exist_ok=True)
    builders = {
        "01_mind_fulcrum_lever.svg": build_01_mind_fulcrum_lever,
        "02_vitality_cycle_cones.svg": build_02_vitality_cycle_cones,
        "03_conical_magnets.svg": build_03_conical_magnets,
        "04_cube_sphere_nine_equators.svg": build_04_cube_sphere_nine_equators,
        "05_light_sphere_lens.svg": build_05_light_sphere_lens,
        "06_nebula_gyroscopic_oblateness.svg": build_06_nebula_gyroscopic_oblateness,
        "07_octave_matter_wave_locks.svg": build_07_octave_matter_wave_locks,
        "08_russell_periodic_spiral.svg": build_08_russell_periodic_spiral,
    }
    for filename, fn in builders.items():
        out_path = SVG_OUT_DIR / filename
        out_path.write_text(fn(), encoding="utf-8")
        print(f"Wrote {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
