#!/usr/bin/env python3
"""Compile both Book Codices in docsrc/ for GEOMETOR Russell:

1. docsrc/home_study_course/:
   The complete 12-Unit, 48-Lesson Home Study Course (1950–1952) converted from
   the structured XHTML sources, with all 102 archival plates and side-by-side
   GEOMETOR parametric SVG reconstructions.

2. docsrc/cosmogony/:
   The Wave-Field Cosmogony of Walter Russell — a 7-chapter geometric and 3D
   interactive treatise distilling Russell's wave mechanics, Cube-Sphere geometry,
   conical vortices, spherical light-lenses, and 9-octave periodic chart.
"""

from __future__ import annotations

import html
import re
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EPUB_DIR = ROOT / "resources" / "home_study_course" / "epub" / "OEBPS"
PLATES_OUT = ROOT / "docsrc" / "_static" / "plates"
HSC_OUT = ROOT / "docsrc" / "home_study_course"
COS_OUT = ROOT / "docsrc" / "cosmogony"

NS = {"x": "http://www.w3.org/1999/xhtml"}

UNIT_TITLES = {
    1: "Unit I (Lessons 1–4): Meditation Scientifically Explained",
    2: "Unit II (Lessons 5–8): Prayer & The Story of My Illumining",
    3: "Unit III (Lessons 9–12): First Principles & This Sexed Electric Universe",
    4: "Unit IV (Lessons 13–16): Mind, Motion & Man Must Know Man",
    5: "Unit V (Lessons 17–20): The Fulcrum, The Lever & The Mystery of Life and Death",
    6: "Unit VI (Lessons 21–24): Deeper Thoughts of Life, Death & Spiritual-Physical Unity",
    7: "Unit VII (Lessons 25–28): Simplicity, Sound, Silence & Wave-Vibrations",
    8: "Unit VIII (Lessons 29–32): Electric Polarity & Reincarnation",
    9: "Unit IX (Lessons 33–36): Cosmic Knowledge & The Rise and Fall of Man",
    10: "Unit X (Lessons 37–40): Reincarnation Continued & Multiplication into Transcendent Beings",
    11: "Unit XI (Lessons 41–44): Building the Cube-Sphere Wave-Field of Curved Motion",
    12: "Unit XII (Lessons 45–48): As on Earth So in Heaven & The Making of Matter",
}

# Map lessons to revamped GEOMETOR SVG plates to display alongside archival scans
LESSON_SVG_UPGRADES = {
    9: [
        (
            "/_static/svg/01_mind_fulcrum_lever.svg",
            "GEOMETOR Vector Reconstruction (Figs. 7–16, 28–33): The Still Magnetic Fulcrum (0) and Divided Electric Wave-Lever.",
        )
    ],
    17: [
        (
            "/_static/svg/01_mind_fulcrum_lever.svg",
            "GEOMETOR Vector Reconstruction (Figs. 28–33): The Wave-Lever Oscillating upon the Still Fulcrum of Zero Curvature.",
        )
    ],
    18: [
        (
            "/_static/svg/02_vitality_cycle_cones.svg",
            "GEOMETOR Vector Reconstruction (Figs. 38–47): The Growth and Decay Cycle of Opposing Spiral Cones.",
        )
    ],
    42: [
        (
            "/_static/svg/06_nebula_gyroscopic_oblateness.svg",
            "GEOMETOR Vector Reconstruction (Figs. 95–104): Gyroscopic Winding to True Sphere at 90° Wave Amplitude and Unwinding.",
        )
    ],
    43: [
        (
            "/_static/svg/04_cube_sphere_nine_equators.svg",
            "GEOMETOR Vector Reconstruction (Fig. 114): The Cube-Sphere Wave-Field of Nine Equators and Wave Octave Formula.",
        )
    ],
    45: [
        (
            "/_static/svg/04_cube_sphere_nine_equators.svg",
            "GEOMETOR Vector Reconstruction (Fig. 114): The Cube-Sphere Wave-Field of Nine Equators (0–1–2–3–4–0–4–3–2–1–0).",
        )
    ],
    46: [
        (
            "/_static/svg/03_conical_magnets.svg",
            "GEOMETOR Vector Reconstruction (Figs. 158–161): All of Nature's Magnets Are Cones of Curved Pressure.",
        ),
        (
            "/_static/svg/05_light_sphere_lens.svg",
            "GEOMETOR Vector Reconstruction (Figs. 170–172): The Spherical Light-Lens, Curved Radii, and Ring-to-System Genesis.",
        ),
    ],
    47: [
        (
            "/_static/svg/08_russell_periodic_spiral.svg",
            "GEOMETOR Vector Reconstruction (Fig. 177): The Russell Nine-Octave Periodic Chart of the Elements, No. 2.",
        ),
        (
            "/_static/svg/07_octave_matter_wave_locks.svg",
            "GEOMETOR Vector Reconstruction (Figs. 179–180): Octave Arch of Integration/Disintegration and Four Tone-Element Pairs.",
        ),
    ],
}


def copy_plates() -> None:
    """Copy all 102 EPUB plates + cover.png + Fig_172_hires.png into docsrc/_static/plates/."""
    PLATES_OUT.mkdir(parents=True, exist_ok=True)
    img_dir = EPUB_DIR / "Images"
    for p in sorted(img_dir.glob("*")):
        if p.is_file():
            shutil.copy2(p, PLATES_OUT / p.name)
    hires_172 = ROOT / "resources" / "home_study_course" / "Fig_172_hires.png"
    if hires_172.exists():
        shutil.copy2(hires_172, PLATES_OUT / "Fig_172_hires.png")


def clean_inline_rst(elem: ET.Element) -> str:
    """Convert an XHTML paragraph or heading element into clean inline RST."""
    parts: list[str] = []

    def visit(node: ET.Element) -> None:
        tag = node.tag.split("}")[-1]
        if node.text:
            parts.append(node.text)
        for child in node:
            ctag = child.tag.split("}")[-1]
            inner = "".join(child.itertext()).strip()
            if ctag in ("b", "strong") and inner:
                parts.append(f"**{inner}**")
            elif ctag in ("i", "em") and inner:
                parts.append(f"*{inner}*")
            elif ctag == "br":
                parts.append(" ")
            else:
                visit(child)
            if child.tail:
                parts.append(child.tail)

    visit(elem)
    text = " ".join("".join(parts).split())
    # Fix adjacent emphasis markers like **foo****bar**
    text = re.sub(r"\*\*\s*\*\*", " ", text)
    text = re.sub(r"\*\*\*+", "**", text)
    return text.strip()


def convert_xhtml_to_rst(
    xhtml_path: Path,
    doc_ref: str,
    default_title: str,
    lesson_num: int | None = None,
) -> tuple[str, str, list[tuple[str, str]]]:
    """Convert a single EPUB XHTML file into a Book Codex RST file.

    Returns (rst_content, clean_title, list_of_(img_filename, context_caption)).
    """
    raw = xhtml_path.read_text(encoding="utf-8").replace("&nbsp;", " ")
    tree = ET.fromstring(raw)
    body = tree.find("x:body", NS)
    assert body is not None

    h1 = body.find("x:h1", NS)
    if h1 is not None:
        title = " ".join("".join(h1.itertext()).split())
    else:
        title = default_title

    lines: list[str] = [
        ":layout: book",
        "",
        f".. _{doc_ref}:",
        "",
        title,
        "=" * max(len(title), 4),
        "",
    ]

    if lesson_num in LESSON_SVG_UPGRADES:
        lines.extend(
            [
                ".. admonition:: GEOMETOR Revamped Cosmogony Plates",
                "   :class: note",
                "",
                "   This lesson's core geometric diagrams have been reconstructed as precision parametric vector plates:",
                "",
            ]
        )
        for svg_path, svg_cap in LESSON_SVG_UPGRADES[lesson_num]:
            lines.extend(
                [
                    f"   .. figure:: {svg_path}",
                    "      :align: center",
                    "      :width: 96%",
                    "",
                    f"      {svg_cap}",
                    "",
                ]
            )

    plate_records: list[tuple[str, str]] = []
    children = list(body)
    for idx, ch in enumerate(children):
        tag = ch.tag.split("}")[-1]
        if tag == "h1":
            continue
        if tag in ("h2", "h3"):
            htxt = " ".join("".join(ch.itertext()).split()).strip()
            if htxt:
                underline = "-" * max(len(htxt), 4) if tag == "h2" else "~" * max(len(htxt), 4)
                lines.extend([htxt, underline, ""])
            continue

        # Check for embedded images inside this element
        imgs = ch.findall(".//x:img", NS)
        if imgs:
            for img in imgs:
                src_name = Path(img.attrib.get("src", "")).name
                # Determine surrounding caption/context
                ctx = " ".join("".join(ch.itertext()).split()).strip()
                if not ctx and idx + 1 < len(children):
                    ctx = " ".join("".join(children[idx + 1].itertext()).split()).strip()[:160]
                if not ctx and idx > 0:
                    ctx = " ".join("".join(children[idx - 1].itertext()).split()).strip()[:160]
                plate_records.append((src_name, ctx))
                lines.extend(
                    [
                        f".. figure:: /_static/plates/{src_name}",
                        "   :align: center",
                        "",
                        f"   Archival Plate (``{src_name}``)",
                        "",
                    ]
                )
                if src_name == "image093.gif":
                    lines.extend(
                        [
                            ".. figure:: /_static/plates/Fig_172_hires.png",
                            "   :align: center",
                            "   :width: 85%",
                            "",
                            "   High-Resolution Archival Scan of Unit 12, Page 44 (``Figs. 170–172``)",
                            "",
                        ]
                    )

        txt = clean_inline_rst(ch)
        if txt:
            lines.extend([txt, ""])

    return ("\n".join(lines), title, plate_records)


def build_home_study_course() -> list[tuple[int, str, str, str]]:
    """Build docsrc/home_study_course/ across 12 Units and 48 Lessons.

    Returns list of (lesson_num, title, img_name, context) for the figure concordance.
    """
    HSC_OUT.mkdir(parents=True, exist_ok=True)
    text_dir = EPUB_DIR / "Text"

    # Build Prelude (combining title, copyright, and prelude)
    _, _, _ = convert_xhtml_to_rst(text_dir / "title.xhtml", "hsc-title", "Title")
    copy_rst, _, _ = convert_xhtml_to_rst(text_dir / "copyright.xhtml", "hsc-copyright", "Copyright")
    pre_rst, pre_title, _ = convert_xhtml_to_rst(
        text_dir / "prelude.xhtml",
        "hsc-prelude",
        "Prelude to Intimate Home Study Course",
    )
    (HSC_OUT / "prelude.rst").write_text(pre_rst + "\n\n----\n\n" + copy_rst.split("\n", 6)[-1], encoding="utf-8")

    concordance: list[tuple[int, str, str, str]] = []
    unit_lesson_titles: dict[int, list[tuple[int, str]]] = {u: [] for u in range(1, 13)}

    for lesson_num in range(1, 49):
        unit_num = (lesson_num - 1) // 4 + 1
        unit_dir = HSC_OUT / f"unit_{unit_num:02d}"
        unit_dir.mkdir(parents=True, exist_ok=True)

        xhtml_file = text_dir / f"lesson_{lesson_num:02d}.xhtml"
        rst_text, l_title, plates = convert_xhtml_to_rst(
            xhtml_file,
            f"hsc-lesson-{lesson_num:02d}",
            f"Lesson {lesson_num}",
            lesson_num=lesson_num,
        )
        (unit_dir / f"lesson_{lesson_num:02d}.rst").write_text(rst_text, encoding="utf-8")
        unit_lesson_titles[unit_num].append((lesson_num, l_title))
        for img_name, ctx in plates:
            concordance.append((lesson_num, l_title, img_name, ctx))

    # Write each Unit's index.rst
    for unit_num in range(1, 13):
        unit_dir = HSC_OUT / f"unit_{unit_num:02d}"
        utitle = UNIT_TITLES[unit_num]
        u_lines = [
            ":layout: book",
            "",
            f".. _hsc-unit-{unit_num:02d}:",
            "",
            utitle,
            "=" * len(utitle),
            "",
            ".. toctree::",
            "   :maxdepth: 2",
            "",
        ]
        for l_num, _ in unit_lesson_titles[unit_num]:
            u_lines.append(f"   lesson_{l_num:02d}")
        u_lines.append("")
        (unit_dir / "index.rst").write_text("\n".join(u_lines), encoding="utf-8")

    # Write top-level docsrc/home_study_course/index.rst
    idx_lines = [
        ":navigation: header",
        ":order: 2",
        ":layout: book",
        ":title: Home Study Course (1950–1952)",
        ":book_title: Home Study Course",
        ":book_subtitle: Universal Law, Natural Science and Philosophy (Lessons 1–48)",
        ":author: Walter and Lao Russell",
        ":publisher: Walter Russell Foundation • Swannanoa, Waynesboro, Virginia",
        ":year: 1950–1952",
        "",
        ".. _home-study-course-index:",
        "",
        "HOME STUDY COURSE",
        "=================",
        "",
        ".. rubric:: Universal Law, Natural Science and Philosophy — Third Edition (1950–1952) by Walter and Lao Russell",
        "",
        ".. figure:: /_static/plates/cover.png",
        "   :align: center",
        "   :width: 320px",
        "",
        "   Cover of the GEOMETOR Digital Edition featuring Walter Russell's *Cosmic Clock* emblem.",
        "",
        "Complete digital edition of the 12 Units (48 Lessons) and 102 diagram plates (`Figs. 1–180`) of **Walter and Lao Russell**'s *Home Study Course in Universal Law, Natural Science and Philosophy*, enhanced with **GEOMETOR** parametric vector reconstructions of the core cosmogonic plates.",
        "",
        "Conspectus of Units & Lessons",
        "-----------------------------",
        "",
        "* :ref:`Prelude to Intimate Home Study Course <hsc-prelude>`",
    ]
    for unit_num in range(1, 13):
        idx_lines.append(f"* :ref:`{UNIT_TITLES[unit_num]} <hsc-unit-{unit_num:02d}>`")
        for l_num, l_title in unit_lesson_titles[unit_num]:
            idx_lines.append(f"  - :ref:`{l_title} <hsc-lesson-{l_num:02d}>`")

    idx_lines.extend(
        [
            "",
            ".. toctree::",
            "   :maxdepth: 2",
            "   :caption: Units & Lessons",
            "   :hidden:",
            "",
            "   prelude",
        ]
    )
    for unit_num in range(1, 13):
        idx_lines.append(f"   unit_{unit_num:02d}/index")
    idx_lines.append("")
    (HSC_OUT / "index.rst").write_text("\n".join(idx_lines), encoding="utf-8")
    return concordance


INTERACTIVE_3D_CUBE_SPHERE_HTML = """
.. raw:: html

   <div style="background:#0c0e14;border:1.5px solid #262e42;border-radius:8px;padding:18px;margin:24px 0;color:#ebe6dc;font-family:'Fira Sans Condensed','Inter',sans-serif;">
     <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;margin-bottom:12px;border-bottom:1px solid #262e42;padding-bottom:10px;">
       <div>
         <strong style="color:#e8b85a;letter-spacing:1px;font-size:15px;">INTERACTIVE 3D MODEL • THE CUBE-SPHERE WAVE-FIELD &amp; NINE EQUATORS</strong>
         <div style="font-size:12px;color:#949eb0;">Drag to orbit in 3D • Toggle the 3 Orthogonal &amp; 6 Diagonal Zero-Curvature Planes, Opposing Spiral Cones, and Breathing Cycle</div>
       </div>
       <div style="display:flex;gap:8px;flex-wrap:wrap;">
         <button id="btn-ortho" style="background:#1e2638;color:#e8b85a;border:1px solid #e8b85a;padding:4px 10px;border-radius:4px;cursor:pointer;font-size:12px;">3 Ortho Planes: ON</button>
         <button id="btn-diag" style="background:#121621;color:#949eb0;border:1px solid #262e42;padding:4px 10px;border-radius:4px;cursor:pointer;font-size:12px;">6 Diag Planes: OFF</button>
         <button id="btn-cones" style="background:#1e2638;color:#fb7185;border:1px solid #fb7185;padding:4px 10px;border-radius:4px;cursor:pointer;font-size:12px;">Spiral Cones: ON</button>
         <button id="btn-nodes" style="background:#1e2638;color:#38bdf8;border:1px solid #38bdf8;padding:4px 10px;border-radius:4px;cursor:pointer;font-size:12px;">27 Zero Nodes: ON</button>
       </div>
     </div>
     <canvas id="russell-cube-sphere-canvas" width="780" height="480" style="width:100%;max-width:780px;height:auto;display:block;margin:0 auto;cursor:grab;"></canvas>
     <div style="display:flex;justify-content:space-between;align-items:center;margin-top:10px;font-size:12px;color:#949eb0;">
       <span><span style="color:#e8b85a;">●</span> Cube &amp; 9 Zero Equators (Still Magnetic Light)</span>
       <span><span style="color:#fb7185;">●</span> Centripetal Winding Cones (+1 → +4)</span>
       <span><span style="color:#38bdf8;">●</span> Inscribed Sphere &amp; Centrifugal Unwinding (-4 → 0)</span>
     </div>
   </div>
   <script>
   (function() {
     const canvas = document.getElementById('russell-cube-sphere-canvas');
     if (!canvas) return;
     const ctx = canvas.getContext('2d');
     let rotY = 0.62, rotX = 0.42;
     let dragging = false, lastX = 0, lastY = 0;
     let showOrtho = true, showDiag = false, showCones = true, showNodes = true;
     let phase = 0;

     function bindToggle(id, getter, setter, label, activeColor) {
       const btn = document.getElementById(id);
       if (!btn) return;
       btn.addEventListener('click', () => {
         const v = !getter();
         setter(v);
         btn.textContent = label + (v ? ': ON' : ': OFF');
         btn.style.color = v ? activeColor : '#949eb0';
         btn.style.borderColor = v ? activeColor : '#262e42';
         btn.style.background = v ? '#1e2638' : '#121621';
       });
     }
     bindToggle('btn-ortho', () => showOrtho, v => showOrtho = v, '3 Ortho Planes', '#e8b85a');
     bindToggle('btn-diag', () => showDiag, v => showDiag = v, '6 Diag Planes', '#e8b85a');
     bindToggle('btn-cones', () => showCones, v => showCones = v, 'Spiral Cones', '#fb7185');
     bindToggle('btn-nodes', () => showNodes, v => showNodes = v, '27 Zero Nodes', '#38bdf8');

     canvas.addEventListener('mousedown', e => { dragging = true; lastX = e.clientX; lastY = e.clientY; });
     window.addEventListener('mouseup', () => dragging = false);
     window.addEventListener('mousemove', e => {
       if (!dragging) return;
       rotY += (e.clientX - lastX) * 0.008;
       rotX = Math.max(-1.4, Math.min(1.4, rotX + (e.clientY - lastY) * 0.008));
       lastX = e.clientX; lastY = e.clientY;
     });

     function project(x, y, z) {
       const cy = Math.cos(rotY), sy = Math.sin(rotY);
       const cx = Math.cos(rotX), sx = Math.sin(rotX);
       const x1 = x * cy - z * sy;
       const z1 = x * sy + z * cy;
       const y2 = y * cx - z1 * sx;
       const z2 = y * sx + z1 * cx;
       const fov = 4.2 / (4.2 + z2 * 0.45);
       const scale = 148 * fov;
       return [canvas.width / 2 + x1 * scale, canvas.height / 2 - y2 * scale, z2, scale];
     }

     function drawPoly(pts3d, fillStyle, strokeStyle, width) {
       const pts = pts3d.map(p => project(p[0], p[1], p[2]));
       ctx.beginPath();
       pts.forEach((p, i) => i === 0 ? ctx.moveTo(p[0], p[1]) : ctx.lineTo(p[0], p[1]));
       ctx.closePath();
       if (fillStyle) { ctx.fillStyle = fillStyle; ctx.fill(); }
       if (strokeStyle) { ctx.strokeStyle = strokeStyle; ctx.lineWidth = width || 1; ctx.stroke(); }
     }

     function render() {
       phase += 0.018;
       if (!dragging) rotY += 0.0035;
       ctx.fillStyle = '#0c0e14';
       ctx.fillRect(0, 0, canvas.width, canvas.height);

       // 3 Orthogonal Planes of Zero Curvature
       if (showOrtho) {
         const ortho = [
           [[0,-1,-1],[0,1,-1],[0,1,1],[0,-1,1]],
           [[-1,0,-1],[1,0,-1],[1,0,1],[-1,0,1]],
           [[-1,-1,0],[1,-1,0],[1,1,0],[-1,1,0]]
         ];
         ortho.forEach(pl => drawPoly(pl, 'rgba(232,184,90,0.13)', 'rgba(232,184,90,0.65)', 1.3));
       }

       // 6 Diagonal Bisecting Planes of Zero Curvature
       if (showDiag) {
         const diag = [
           [[-1,-1,-1],[1,1,-1],[1,1,1],[-1,-1,1]],
           [[-1,1,-1],[1,-1,-1],[1,-1,1],[-1,1,1]],
           [[-1,-1,-1],[1,-1,1],[1,1,1],[-1,1,-1]],
           [[-1,1,-1],[1,1,1],[1,-1,1],[-1,-1,-1]]
         ];
         diag.forEach(pl => drawPoly(pl, 'rgba(56,189,248,0.08)', 'rgba(56,189,248,0.45)', 1.0));
       }

       // Outer Cube Wireframe
       const corners = [-1, 1];
       ctx.strokeStyle = 'rgba(235,230,220,0.75)';
       ctx.lineWidth = 1.6;
       for (let a of corners) {
         for (let b of corners) {
           const segs = [
             [[-1,a,b],[1,a,b]],
             [[a,-1,b],[a,1,b]],
             [[a,b,-1],[a,b,1]]
           ];
           segs.forEach(s => {
             const p1 = project(...s[0]), p2 = project(...s[1]);
             ctx.beginPath(); ctx.moveTo(p1[0], p1[1]); ctx.lineTo(p2[0], p2[1]); ctx.stroke();
           });
         }
       }

       // Opposing Double-Cone Spiral Vortex (from Y=-1 and Y=+1 faces to (0,0,0) center)
       if (showCones) {
         for (let dir of [-1, 1]) {
           ctx.beginPath();
           const steps = 110;
           for (let i = 0; i <= steps; i++) {
             const t = i / steps; // 0 at cube face, 1 at center
             const y = dir * (1 - t);
             const r = (1 - t) * 0.92;
             const ang = t * 5 * Math.PI * 2 + phase * dir * 2;
             const x = r * Math.cos(ang);
             const z = r * Math.sin(ang);
             const p = project(x, y, z);
             if (i === 0) ctx.moveTo(p[0], p[1]); else ctx.lineTo(p[0], p[1]);
           }
           ctx.strokeStyle = dir > 0 ? '#fb7185' : '#38bdf8';
           ctx.lineWidth = 2.0;
           ctx.stroke();
         }
       }

       // Breathing Inscribed Sphere at Center
       const centerP = project(0, 0, 0);
       const pulse = 0.85 + 0.15 * Math.sin(phase * 1.5);
       const sphereR = centerP[3] * pulse;
       const grad = ctx.createRadialGradient(centerP[0], centerP[1], 4, centerP[0], centerP[1], sphereR);
       grad.addColorStop(0, 'rgba(254,240,138,0.85)');
       grad.addColorStop(0.25, 'rgba(251,113,133,0.32)');
       grad.addColorStop(0.75, 'rgba(56,189,248,0.14)');
       grad.addColorStop(1, 'rgba(12,14,20,0)');
       ctx.fillStyle = grad;
       ctx.beginPath();
       ctx.arc(centerP[0], centerP[1], sphereR, 0, Math.PI * 2);
       ctx.fill();
       ctx.strokeStyle = 'rgba(56,189,248,0.65)';
       ctx.setLineDash([5, 4]);
       ctx.stroke();
       ctx.setLineDash([]);

       // 27 Zero-Nodes of the 3x3x3 Cube-Sphere Lattice
       if (showNodes) {
         for (let ix of [-1, 0, 1]) {
           for (let iy of [-1, 0, 1]) {
             for (let iz of [-1, 0, 1]) {
               const p = project(ix, iy, iz);
               const isCenter = (ix === 0 && iy === 0 && iz === 0);
               ctx.beginPath();
               ctx.arc(p[0], p[1], isCenter ? 8 : 4.5, 0, Math.PI * 2);
               ctx.fillStyle = isCenter ? '#fef08a' : '#151924';
               ctx.fill();
               ctx.strokeStyle = isCenter ? '#fb7185' : '#e8b85a';
               ctx.lineWidth = isCenter ? 2.2 : 1.5;
               ctx.stroke();
             }
           }
         }
       }

       requestAnimationFrame(render);
     }
     render();
   })();
   </script>
"""


INTERACTIVE_3D_HELIX_HTML = """
.. raw:: html

   <div style="background:#0c0e14;border:1.5px solid #262e42;border-radius:8px;padding:18px;margin:24px 0;color:#ebe6dc;font-family:'Fira Sans Condensed','Inter',sans-serif;">
     <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;margin-bottom:12px;border-bottom:1px solid #262e42;padding-bottom:10px;">
       <div>
         <strong style="color:#e8b85a;letter-spacing:1px;font-size:15px;">INTERACTIVE 3D MODEL • THE HELICAL OCTAVE WAVE OF MATTER (0 → 4± → 0)</strong>
         <div style="font-size:12px;color:#949eb0;">Drag to tilt &amp; rotate • Watch the 4 Pairs of Tone-Elements wind from Inert Gas (0) to Carbon Amplitude (4±) and unwind</div>
       </div>
     </div>
     <canvas id="russell-helix-canvas" width="780" height="400" style="width:100%;max-width:780px;height:auto;display:block;margin:0 auto;cursor:grab;"></canvas>
   </div>
   <script>
   (function() {
     const canvas = document.getElementById('russell-helix-canvas');
     if (!canvas) return;
     const ctx = canvas.getContext('2d');
     let pitch = 0.28, yaw = -0.35, tPhase = 0;
     let dragging = false, lx = 0, ly = 0;

     canvas.addEventListener('mousedown', e => { dragging = true; lx = e.clientX; ly = e.clientY; });
     window.addEventListener('mouseup', () => dragging = false);
     window.addEventListener('mousemove', e => {
       if (!dragging) return;
       yaw += (e.clientX - lx) * 0.007;
       pitch = Math.max(-1.1, Math.min(1.1, pitch + (e.clientY - ly) * 0.007));
       lx = e.clientX; ly = e.clientY;
     });

     const tones = [
       { u: -1.0, lbl: '0 • He (Inert Gas)', col: '#e8b85a', r: 0.15 },
       { u: -0.75, lbl: '1+ • Li', col: '#fb7185', r: 0.42 },
       { u: -0.50, lbl: '2+ • Be', col: '#fb7185', r: 0.68 },
       { u: -0.25, lbl: '3+ • B', col: '#fb7185', r: 0.90 },
       { u:  0.00, lbl: '4± • CARBON (Amplitude)', col: '#fef08a', r: 1.12 },
       { u:  0.25, lbl: '3- • N', col: '#38bdf8', r: 0.90 },
       { u:  0.50, lbl: '2- • O', col: '#38bdf8', r: 0.68 },
       { u:  0.75, lbl: '1- • F', col: '#38bdf8', r: 0.42 },
       { u:  1.00, lbl: '0 • Ne (Inert Gas)', col: '#e8b85a', r: 0.15 }
     ];

     function proj(x, y, z) {
       const cy = Math.cos(yaw), sy = Math.sin(yaw);
       const cp = Math.cos(pitch), sp = Math.sin(pitch);
       const x1 = x * cy - z * sy;
       const z1 = x * sy + z * cy;
       const y2 = y * cp - z1 * sp;
       const z2 = y * sp + z1 * cp;
       const s = 135 * (4.5 / (4.5 + z2 * 0.35));
       return [canvas.width / 2 + x1 * s, canvas.height / 2 - y2 * s];
     }

     function draw() {
       tPhase += 0.025;
       ctx.fillStyle = '#0c0e14';
       ctx.fillRect(0, 0, canvas.width, canvas.height);

       // Central Zero Wave Axis
       const a1 = proj(-2.2, 0, 0), a2 = proj(2.2, 0, 0);
       ctx.strokeStyle = '#e8b85a';
       ctx.lineWidth = 2;
       ctx.beginPath(); ctx.moveTo(a1[0], a1[1]); ctx.lineTo(a2[0], a2[1]); ctx.stroke();

       // Helical Double-Cone Wave Path
       ctx.beginPath();
       const steps = 160;
       for (let i = 0; i <= steps; i++) {
         const u = -1.0 + 2.0 * (i / steps);
         const env = 0.15 + 0.97 * Math.cos(u * Math.PI * 0.5);
         const ang = u * Math.PI * 4 - tPhase;
         const p = proj(u * 2.0, env * Math.sin(ang), env * Math.cos(ang));
         if (i === 0) ctx.moveTo(p[0], p[1]); else ctx.lineTo(p[0], p[1]);
       }
       ctx.strokeStyle = 'rgba(235,230,220,0.65)';
       ctx.lineWidth = 2;
       ctx.stroke();

       // Gyroscopic Locking Wheels & Element Nodes
       tones.forEach((t, idx) => {
         const x = t.u * 2.0;
         ctx.beginPath();
         for (let k = 0; k <= 36; k++) {
           const a = (k / 36) * Math.PI * 2;
           const p = proj(x, t.r * Math.sin(a), t.r * Math.cos(a));
           if (k === 0) ctx.moveTo(p[0], p[1]); else ctx.lineTo(p[0], p[1]);
         }
         ctx.strokeStyle = t.col;
         ctx.lineWidth = idx === 4 ? 2.4 : 1.3;
         ctx.stroke();

         const ang = t.u * Math.PI * 4 - tPhase;
         const np = proj(x, t.r * Math.sin(ang), t.r * Math.cos(ang));
         ctx.beginPath();
         ctx.arc(np[0], np[1], idx === 4 ? 8 : 5.5, 0, Math.PI * 2);
         ctx.fillStyle = t.col;
         ctx.fill();

         const lp = proj(x, -t.r - 0.25, 0);
         ctx.fillStyle = t.col;
         ctx.font = (idx === 4 ? 'bold 12px' : '11px') + ' sans-serif';
         ctx.textAlign = 'center';
         ctx.fillText(t.lbl, lp[0], lp[1]);
       });

       requestAnimationFrame(draw);
     }
     draw();
   })();
   </script>
"""


def build_cosmogony_book(concordance: list[tuple[int, str, str, str]]) -> None:
    """Build the new 7-chapter Cosmogony Book Codex in docsrc/cosmogony/."""
    COS_OUT.mkdir(parents=True, exist_ok=True)

    # Chapter 1: Mind, Fulcrum & Wave-Lever
    ch1 = """\
:layout: book

.. _cosmogony-ch1:

Chapter I: The Undivided Light of Mind & The Divided Electric Wave-Lever
========================================================================

.. rubric:: First Principles of the Russell Cosmogony (Lessons 1–17)

At the foundation of **Walter Russell**'s cosmogony stands a radical inversion of materialist physics: **Mind is the sole reality**, and its substance is **Still Magnetic Light**—an undivided, motionless, zero-point equilibrium of omnipotent Knowing.

The Divided Electric Universe of Motion
---------------------------------------

When Mind *thinks* what it *knows*, it divides its one whole idea at rest (``0``) into mated pairs of opposite electric pressure conditions:

1. **The Father / Centripetal / Red Pole (``+``)**:
   Concentrative thinking pulls inward from cold space toward a center of gravity, compressing large tenuous volumes into small incandescent spheres of high potential (`+1 -> +2 -> +3 -> +4`).
2. **The Mother / Centrifugal / Blue Pole (``-``)**:
   Decentrative rest thrusts outward from incandescent centers back toward the cold bounding planes of space, expanding dense spheres into tenuous radiation (`-4 -> -3 -> -2 -> -1 -> 0`).
3. **The Still Magnetic Fulcrum (``0``)**:
   Power never resides in the moving electric wave-lever; it resides exclusively in the motionless magnetic fulcrum upon which the wave-lever oscillates.

.. figure:: /_static/svg/01_mind_fulcrum_lever.svg
   :align: center
   :width: 98%

   **Plate I (Figs. 7–16, 28–33)**: Undivided Still Magnetic Light (`0`) divided by concentrative/decentrative thinking into Father (`+4` Red compression) and Mother (`-4` Blue expansion) poles oscillating across the Wave-Lever.

The Principle of Voidance
-------------------------

Every action in Nature occurs simultaneously with its equal and opposite reaction:

.. epigraph::

   *"Every action in Nature is voided as it occurs, is repeated as it is voided, and is recorded as it is repeated."*

   — **Walter Russell**, *Home Study Course*, Lesson 10
"""
    (COS_OUT / "01_mind_and_motion.rst").write_text(ch1, encoding="utf-8")

    # Chapter 2: Opposing Spiral Cones
    ch2 = """\
:layout: book

.. _cosmogony-ch2:

Chapter II: The Double-Cone Vortex — Centripetal Generation & Centrifugal Radiation
===================================================================================

.. rubric:: The Two-Way Spiral Engine of Life, Growth, and Magnetism (Lessons 18, 29 & 46)

In Russell's wave mechanics, there are no straight lines in the moving electric universe, nor do cylindrical bar magnets exist in Nature. Every wave-field is wound and unwound by **two opposing interpenetrating cones** operating between the flat planes of zero curvature and the central gravitational nucleus.

The Electric Cycle of Vitality (`Figs. 38–47`)
----------------------------------------------

Vitality in any system—whether an oak tree, a human body, or a stellar sun—is measured by the ability of its opposite poles to pull apart from its zero equator toward wave amplitude (``+4 / 0 / -4``):

* **Seed in Rest (`Fig. 38`)**: Polarity lies dormant at zero equilibrium (`0`).
* **Unfolding Youth (`Figs. 39–41`)**: Centripetal and centrifugal cones extend from the equator, drawing earthward roots (`+`) and skyward branches (`-`).
* **Full Maturity at Wave Amplitude (`Figs. 43–44`)**: The interpenetrating double-cone vortex reaches maximum axial extension and equatorial balance.
* **Declining Polarity & Return to Rest (`Figs. 45–47`)**: As the poles lose their ability to pull apart, the conical vortex flattens back into the plane of zero curvature.

.. figure:: /_static/svg/02_vitality_cycle_cones.svg
   :align: center
   :width: 98%

   **Plate II (Figs. 38–47)**: The ten-stage electric cycle of polarization (growth/life) and depolarization (decay/rest) governed by opposing spiral cones.

Why All of Nature's Magnets Are Cones (`Figs. 158–161`)
-------------------------------------------------------

A man-made cylindrical bar magnet (`Fig. 158`) artificially forces equal density at both poles, producing a flat equator of zero curvature. In free space, however, every pressure gradient expands conically from a dense gravitational apex (``N``) to a tenuous radiative base (``S``):

.. figure:: /_static/svg/03_conical_magnets.svg
   :align: center
   :width: 98%

   **Plate III (Figs. 158–161)**: Comparison of the cylindrical bar magnet (`Fig. 158`) with Nature's conical magnets (`Fig. 159`), conical evaporation of solid matter (`Fig. 160`), and the spherical reversal of curved equators and radii (`Fig. 161`).
"""
    (COS_OUT / "02_conical_vortices.rst").write_text(ch2, encoding="utf-8")

    # Chapter 3: The Cube-Sphere Wave-Field
    ch3 = (
        """\
:layout: book

.. _cosmogony-ch3:

Chapter III: The Cube-Sphere Wave-Field & The Nine Equators of Zero Curvature
=============================================================================

.. rubric:: The Crystal Geometry of Space and the ``0–4–0–4–0`` Wave Octave (Lessons 41–45)

The crown jewel of Russell's geometric cosmogony is the **Cube-Sphere Wave-Field** (`Figs. 105–124`). Space is not an unstructured void; it is a crystalline lattice of **bounding cubes of Still Magnetic Light** whose flat faces and internal bisecting planes are planes of **zero curvature (`0`)**.

The Nine Equators and the ``9`` Count of Creation
-------------------------------------------------

Within every cubic wave-field, electric motion curves inward to form an **inscribed sphere** divided into eight octants centered by a single zero nucleus:

1. **Three Orthogonal Planes of Zero Curvature**: Bisecting the cube along the $X, Y, Z$ axes, dividing the sphere into 8 octants.
2. **Six Diagonal Planes of Zero Curvature**: Bisecting the 12 edges of the cube at $45^\\circ$.
3. **Total Equators = 9**: Every polarized action-reaction cycle counts to **nine**—eight octants (or eight cube corners) centered by zero (`8 + 1 = 9`), expressed along the wave axis as the octave formula:

$$0 - 1^- - 2^- - 3^- - 4^- - \\mathbf{0} - 4^+ - 3^+ - 2^+ - 1^+ - 0$$

.. figure:: /_static/svg/04_cube_sphere_nine_equators.svg
   :align: center
   :width: 98%

   **Plate IV (Fig. 114)**: Isometric projection of the Cube-Sphere Wave-Field showing the 3 orthogonal planes of zero curvature, the 27 zero-nodes (`0`) of the $3 \\times 3 \\times 3$ lattice, the inscribed sphere of curved motion, and the 9-count wave octave formula.

Interactive 3D Cube-Sphere & Double-Cone Explorer
-------------------------------------------------

Use the interactive 3D visualizer below to orbit the Cube-Sphere Wave-Field, inspect the 27 zero-nodes, toggle the 3 orthogonal and 6 diagonal planes of zero curvature, and observe the opposing centripetal/centrifugal spiral cones winding into the central sphere:
"""
        + INTERACTIVE_3D_CUBE_SPHERE_HTML
    )
    (COS_OUT / "03_cube_sphere_wave_field.rst").write_text(ch3, encoding="utf-8")

    # Chapter 4: Spherical Light-Lenses
    ch4 = """\
:layout: book

.. _cosmogony-ch4:

Chapter IV: Spherical Light-Lenses, Octant Curvature Reversal & Gravity
=======================================================================

.. rubric:: How Curved Radii Focus Light into Centers of Gravity and Unwind into Rings (Lesson 46)

In Lesson 46 (`Figs. 170–172`), Russell demonstrates that every spherical wave-field acts as an optical **Light-Sphere Lens** divided into eight sections by the three orthogonal equators of zero curvature:

1. **Curvature Reversal across Zero Equators (`Fig. 170`)**:
   As light rays pass from one octant to the next across any of the three orthogonal zero-curvature equators, they lose their curvature at the plane of the equator and reverse it in the opposite octant.
2. **Gravity as Focused Light Compression (`Fig. 171`)**:
   All non-equatorial radii curve inward toward the poles to focus at the center of the lens, creating a **center of gravity** where light compression and heat reach their maximum.
3. **Coronas Become Rings and Rings Become Systems (`Fig. 172`)**:
   Maximum generation (inward winding) occurs at the poles, while maximum radiation (outward thrust) occurs along the united equator—casting off equatorial coronas that condense into nebulous rings and eventually into orbiting planets or electrons.

.. figure:: /_static/svg/05_light_sphere_lens.svg
   :align: center
   :width: 98%

   **Plate V (Figs. 170–172)**: GEOMETOR vector reconstruction of Walter Russell's Light-Sphere Lens plate (`Figs. 170, 171 & 172`).

Archival Comparison (`Fig_172_hires.png`)
-----------------------------------------

Compare the reconstructed vector plate above with Walter Russell's original white-on-black hand-lettered chalkboard plate from Unit 12, Page 44:

.. figure:: /_static/plates/Fig_172_hires.png
   :align: center
   :width: 72%

   **Archival Plate (Figs. 170–172)**: High-resolution (`2481 × 3508`) scan of Walter Russell's original drawing signed ``W. R.``.
"""
    (COS_OUT / "04_spherical_light_lenses.rst").write_text(ch4, encoding="utf-8")

    # Chapter 5: Gyroscopic Precession & Oblateness
    ch5 = """\
:layout: book

.. _cosmogony-ch5:

Chapter V: Gyroscopic Precession & The Evolution of Atomic and Stellar Systems
==============================================================================

.. rubric:: Why True Spheres Only Exist at $90^\\circ$ Wave Amplitude (Lessons 42–43, Figs. 95–104)

Both atomic systems and stellar/planetary systems evolve along the same gyroscopic wave path from stillness (`0`) to wave amplitude (`4±`) and back to stillness (`0`):

* **Centripetal Winding (`1+ -> 2+ -> 3+`)**:
  Beginning as an expanded inert-gas ring in space (`0`), centripetal compression winds the ring through **prolate** (polar-elongated) spheroids whose axes precess toward the wave amplitude perpendicular.
* **The True Sphere at Wave Amplitude (`4+ / 0 / 4-`)**:
  Only when a system locks squarely upon the $90^\\circ$ wave amplitude crest does its central nucleus become a **true incandescent sphere** (such as **Carbon** in the elements or a mature **Sun** in a solar system), with its planets revolving in its equatorial plane (`Fig. 103`).
* **Centrifugal Unwinding (`3- -> 2- -> 1- -> 0`)**:
  Past the amplitude crest, centrifugal radiation flattens the sphere at its poles and bulges its equator into **oblate spheroids**, **ringed planets** (like Saturn), and **ring nebulae** (like the Ring Nebula in Lyra or Hydra), unwinding back into the inert gases of space.

.. figure:: /_static/svg/06_nebula_gyroscopic_oblateness.svg
   :align: center
   :width: 98%

   **Plate VI (Figs. 95–104)**: Gyroscopic evolution from prolate winding (`1+, 2+, 3+`) to the True Sphere at $90^\\circ$ Wave Amplitude (`4±`) and oblate/ringed unwinding (`3-, 2-, 1-`).
"""
    (COS_OUT / "05_gyroscopic_systems.rst").write_text(ch5, encoding="utf-8")

    # Chapter 6: Making of Matter & 9-Octave Periodic Wave
    ch6 = (
        """\
:layout: book

.. _cosmogony-ch6:

Chapter VI: The Making of Matter — The Nine-Octave Periodic Wave of the Elements
================================================================================

.. rubric:: Inert Gas Master-Tones, Octave Locking Points, and Carbon at the Crest (Lesson 47, Figs. 175–180)

In Lesson 47 (*We Now Consider the Making of Matter*), Russell applies the Cube-Sphere wave-field directly to chemistry and atomic structure, contrasting the traditional Mendeleev table (`Fig. 175`) with his **Nine-Octave Periodic Chart of the Elements** (`Fig. 177`, copyrighted in 1926).

1. **Inert Gases as Still Magnetic Master-Tones (`0`)**:
   The inert gases (`Helium`, `Neon`, `Argon`, `Krypton`, `Xenon`, `Radon`) are not merely "unreactive elements"—they are the **zero-equator recording seeds** of Still Magnetic Light from which each octave of moving matter unfolds and into which it disappears.
2. **Four Pairs of Gyroscopic Locking Points (`1±, 2±, 3±, 4±`)**:
   In each octave, four centripetal (`+`) integrating pressure locks (`1+` Alkali metals, `2+` Alkaline earths, `3+` Boron/Aluminum group) wind upward in density and melting point toward the **`4±` Amplitude Crest** (**Carbon**, **Silicon**, **Titanium/Cobalt**, **Zirconium/Rhodium**, **Hafnium/Lutetium**), while four centrifugal (`-`) disintegrating locks (`3-` Pnictogens, `2-` Chalcogens, `1-` Halogens) unwind back to the next Inert Gas (`0`).

.. figure:: /_static/svg/07_octave_matter_wave_locks.svg
   :align: center
   :width: 98%

   **Plate VII (Figs. 179–180)**: The Octave Arch of Increasing Integration (`+`) and Disintegration (`-`) culminating in Carbon (`4±`), paired with the gyroscopic tone-wheels along the wave axis (`Fig. 180`).

The Russell Nine-Octave Periodic Chart (`Fig. 177`)
---------------------------------------------------

.. figure:: /_static/svg/08_russell_periodic_spiral.svg
   :align: center
   :width: 98%

   **Plate VIII (Fig. 177)**: GEOMETOR vector reconstruction of *The Russell Periodic Chart of the Elements, No. 2* (1926), showing the concentric octave waves centered on the horizontal Inert Gas zero-axis (`0 — 0`) and peaking along the vertical `-4 • 0 • +4` Amplitude axis.

Interactive 3D Helical Octave Wave of Matter
--------------------------------------------

Explore the 3D corkscrew geometry of a single Russell Octave (`He -> Li -> Be -> B -> C -> N -> O -> F -> Ne`) as gyroscopic wheels locking at discrete pressure planes along the wave axis:
"""
        + INTERACTIVE_3D_HELIX_HTML
    )
    (COS_OUT / "06_making_of_matter.rst").write_text(ch6, encoding="utf-8")

    # Chapter 7: Complete Concordance of the 102 Plates & 180 Figures
    ch7_lines = [
        ":layout: book",
        "",
        ".. _cosmogony-ch7:",
        "",
        "Chapter VII: Concordance of the 102 Plates & 180 Figures",
        "========================================================",
        "",
        ".. rubric:: Complete Index of Diagrams Across the 48 Lessons of the *Home Study Course*",
        "",
        "Every diagram plate from the 1950–1952 *Home Study Course* is indexed below with direct links to its lesson in the :ref:`Home Study Course Codex <home-study-course-index>`:",
        "",
        ".. list-table::",
        "   :header-rows: 1",
        "   :widths: 14 26 60",
        "",
        "   * - Plate",
        "     - Lesson",
        "     - Context & Figure References",
    ]
    for l_num, l_title, img_name, ctx in concordance:
        short_ctx = (ctx[:120] + "...") if len(ctx) > 120 else (ctx or "Diagram plate")
        short_ctx = short_ctx.replace("*", "").replace("`", "'")
        ch7_lines.extend(
            [
                f"   * - ``{img_name}``",
                f"     - :ref:`Lesson {l_num} <hsc-lesson-{l_num:02d}>`",
                f"     - {short_ctx}",
            ]
        )
    ch7_lines.append("")
    (COS_OUT / "07_figure_concordance.rst").write_text("\n".join(ch7_lines), encoding="utf-8")

    # Scholarly Apparatus: Glossary, Persons, Bibliography
    glossary_rst = """\
:title: Technical Glossary of Russell's Wave-Field Cosmogony
:layout: book

.. _glossary:

Technical Glossary
==================

.. rubric:: *Lexicon of Walter Russell's Wave-Field Cosmogony*

* **Cube-Sphere Wave-Field**: The fundamental geometric unit of creation consisting of an outer bounding Cube of Still Magnetic Light (zero curvature) and an inscribed Sphere of curved electric motion divided into eight octants by nine planes of zero curvature.
* **Centripetal / Genero-active (`+`)**: The male/father polarizing thrust that winds light inward from the cold planes of the cube toward a gravitational focal center, compressing volume into dense, incandescent spheres.
* **Centrifugal / Radio-active (`-`)**: The female/mother depolarizing thrust that unwinds dense spheres outward from the gravitational center back into the flat zero-planes of space.
* **Inert Gas Master-Tones (`0`)**: The noble gases (`He`, `Ne`, `Ar`, `Kr`, `Xe`, `Rn`) situated on the zero-curvature amplitude equators, serving as the motionless magnetic recording seeds of each octave of matter.
* **Light-Sphere Lens**: A spherical wave-field across whose three orthogonal zero-curvature equators light rays reverse curvature in all eight octants (`Figs. 170–172`).
* **Nine Equators of Zero Curvature**: The 3 orthogonal coordinate planes plus 6 diagonal bisecting planes of the Cube-Sphere where opposed electric pressures balance at `0`.
* **Octave Wave Formula (`0–1–2–3–4–0–4–3–2–1–0`)**: The nine-count rhythmic heartbeat of every wave cycle, consisting of four centripetal locking points (`1+, 2+, 3+, 4+`) and four centrifugal locking points (`4-, 3-, 2-, 1-`) centered by zero.
* **Still Magnetic Light (`0`)**: The undivided, motionless, omnipotent Mind-equilibrium out of which the divided electric universe of motion is simulated by thinking.
* **Voidance Principle**: The universal law that every electric action is simultaneously balanced by its equal and opposite reaction, sequentially repeated, and magnetically recorded in the seed (`0`).
"""
    (COS_OUT / "glossary.rst").write_text(glossary_rst, encoding="utf-8")

    persons_rst = """\
:title: Biographical Register
:layout: book

.. _persons:

Biographical Register
=====================

.. rubric:: *Key Figures in the Home Study Course and Cosmogony*

* **Walter Russell (1871–1963)**: American polymath, sculptor, painter, architect, musician, and natural philosopher; author of *The Universal One* (1926), *The Secret of Light* (1947), and co-author with Lao Russell of the *Home Study Course* (1950–1952).
* **Lao Russell (1904–1988)**: Philosopher, author, and co-founder with Walter Russell of the University of Science and Philosophy at Swannanoa Palace, Waynesboro, Virginia.
* **Nikola Tesla (1856–1943)**: Electrical pioneer and contemporary admirer of Walter Russell's wave-field cosmology.
* **Dmitri Ivanovich Mendeleev (1834–1907)**: Russian chemist whose 1904 periodic table is critiqued and contrasted with Russell's 9-octave spiral chart in Lesson 47 (`Figs. 175–177`).
* **Robert Kennedy Duncan (1868–1914)**: Author of *The New Knowledge* (1905), cited by Russell in `Fig. 175` on the Periodic Law as "God's alphabet of the universe."
"""
    (COS_OUT / "persons.rst").write_text(persons_rst, encoding="utf-8")

    bib_rst = """\
:title: Bibliography of Works by Walter and Lao Russell
:layout: book

.. _bibliography:

Bibliography & Primary Sources
==============================

.. rubric:: *Chronological Register of Primary Works*

* **1926** — **Walter Russell**, *The Universal One: An Exact Science of the One Visible and Invisible Universe of Mind and the Registration of All Idea of Thinking Mind in Light, Which Is Matter and Also Energy*. New York: Brieger Press.
* **1926** — **Walter Russell**, *The Russell Periodic Chart of the Elements, No. 1 & No. 2* (`Fig. 177`).
* **1930** — **Walter Russell**, *The Russell Genero-Radiative Concept, or The Cyclic Theory of Continuous Motion*. New York: L. Middleditch Co.
* **1947** — **Walter Russell**, *The Secret of Light*. Waynesboro, VA: University of Science and Philosophy.
* **1948–1949** — **Walter Russell**, *The Message of the Divine Iliad*, Vols. I–II. Waynesboro, VA: University of Science and Philosophy.
* **1950–1952** — **Walter and Lao Russell**, *Home Study Course in Universal Law, Natural Science and Philosophy* (Units 1–12, Lessons 1–48, 3rd Edition). Waynesboro, VA: Walter Russell Foundation.
* **1953** — **Walter Russell**, *A New Concept of the Universe*. Waynesboro, VA: University of Science and Philosophy.
* **1957** — **Walter and Lao Russell**, *Atomic Suicide?* Waynesboro, VA: University of Science and Philosophy.
"""
    (COS_OUT / "bibliography.rst").write_text(bib_rst, encoding="utf-8")

    # Write docsrc/cosmogony/index.rst
    cos_index = """\
:navigation: header
:order: 1
:layout: book
:title: The Wave-Field Cosmogony of Walter Russell
:book_title: The Wave-Field Cosmogony of Walter Russell
:book_subtitle: From Still Magnetic Light to the Cube-Sphere and Nine-Octave Periodic Universe
:author: Walter & Lao Russell • Reconstructed by GEOMETOR
:publisher: GEOMETOR Digital Scriptorium
:year: 2026

.. _cosmogony-index:

THE WAVE-FIELD COSMOGONY OF WALTER RUSSELL
==========================================

.. rubric:: A Geometric, Parametric Vector & Interactive 3D Treatise

A new illustrated treatise distilling the wave-field physics, projective crystal geometry, and periodic element mechanics of **Walter and Lao Russell**'s 48-lesson *Home Study Course* into a unified geometric synthesis—featuring **8 revamped parametric SVG plates** and **interactive 3D WebGL/Canvas models**.

.. figure:: /_static/svg/04_cube_sphere_nine_equators.svg
   :align: center
   :width: 92%

   **The Cube-Sphere Wave-Field of Nine Equators (`Fig. 114`)** — Eight corners and eight octants centered by zero (`8 + 1 = 9`).

----

Conspectus of Chapters
----------------------

* :ref:`Chapter I: The Undivided Light of Mind & The Divided Electric Wave-Lever <cosmogony-ch1>` (`Plate I`, `Figs. 7–16, 28–33`)
* :ref:`Chapter II: The Double-Cone Vortex — Centripetal Generation & Centrifugal Radiation <cosmogony-ch2>` (`Plates II–III`, `Figs. 38–47, 158–161`)
* :ref:`Chapter III: The Cube-Sphere Wave-Field & The Nine Equators of Zero Curvature <cosmogony-ch3>` (`Plate IV`, `Fig. 114` + **Interactive 3D Cube-Sphere Explorer**)
* :ref:`Chapter IV: Spherical Light-Lenses, Octant Curvature Reversal & Gravity <cosmogony-ch4>` (`Plate V`, `Figs. 170–172` + Archival Comparison)
* :ref:`Chapter V: Gyroscopic Precession & The Evolution of Atomic and Stellar Systems <cosmogony-ch5>` (`Plate VI`, `Figs. 95–104`)
* :ref:`Chapter VI: The Making of Matter — The Nine-Octave Periodic Wave of the Elements <cosmogony-ch6>` (`Plates VII–VIII`, `Figs. 177, 179–180` + **Interactive 3D Helical Octave Animator**)
* :ref:`Chapter VII: Complete Concordance of the 102 Plates & 180 Figures <cosmogony-ch7>` (`Figs. 1–180`)
* **Scholarly Apparatus**: :ref:`Technical Glossary <glossary>` · :ref:`Biographical Register <persons>` · :ref:`Bibliography & Primary Sources <bibliography>`

.. toctree::
   :maxdepth: 2
   :caption: Chapters
   :hidden:

   01_mind_and_motion
   02_conical_vortices
   03_cube_sphere_wave_field
   04_spherical_light_lenses
   05_gyroscopic_systems
   06_making_of_matter
   07_figure_concordance

.. toctree::
   :maxdepth: 1
   :caption: Scholarly Apparatus
   :hidden:

   glossary
   persons
   bibliography
"""
    (COS_OUT / "index.rst").write_text(cos_index, encoding="utf-8")


def update_root_index() -> None:
    """Update docsrc/index.rst to link both Book Codices."""
    root_idx = """\
:title: GEOMETOR • russell

GEOMETOR • russell
==================

.. rubric:: The Wave-Field Cosmogony & Home Study Course of Walter and Lao Russell

Digital critical edition, reconstructed parametric vector diagrams, interactive 3D wave-field animations, and scholarly apparatus for the works of **Walter Russell (1871–1963)** and **Lao Russell (1904–1988)**, published with the **Book Codex** engine of ``photon-platform/publish``.

.. figure:: /_static/svg/08_russell_periodic_spiral.svg
   :align: center
   :width: 88%

   **The Russell Nine-Octave Periodic Chart of the Elements (`Fig. 177`)** — Reconstructed in the GEOMETOR parametric vector style.

----

Book Codices (*Opera*)
----------------------

:doc:`The Wave-Field Cosmogony of Walter Russell <cosmogony/index>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A new 7-chapter geometric and 3D visual treatise synthesizing Walter Russell's wave mechanics—from the **Still Magnetic Fulcrum (`0`)** and **Opposing Spiral Cones (`+` / `-`)** to the **Cube-Sphere Wave-Field of Nine Equators (`Fig. 114`)**, **Spherical Light-Lenses (`Figs. 170–172`)**, and the **Nine-Octave Periodic Wave of Matter (`Figs. 177–180`)**—equipped with interactive 3D Canvas models and apparatus (:ref:`Glossary <glossary>` · :ref:`Persons <persons>` · :ref:`Bibliography <bibliography>`).

:doc:`Home Study Course in Universal Law, Natural Science and Philosophy (1950–1952) <home_study_course/index>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The complete 3rd Edition of **Walter and Lao Russell**'s 12-Unit, 48-Lesson *Home Study Course*, featuring the Prelude, all 48 Lessons (`Lessons 1–48`), all 102 original diagram plates (`Figs. 1–180`), and side-by-side GEOMETOR vector reconstructions.

.. toctree::
   :maxdepth: 2
   :hidden:

   cosmogony/index
   home_study_course/index
   changelog
   connect
"""
    (ROOT / "docsrc" / "index.rst").write_text(root_idx, encoding="utf-8")


def main() -> None:
    copy_plates()
    concordance = build_home_study_course()
    build_cosmogony_book(concordance)
    update_root_index()
    print(f"Built Home Study Course Codex (48 lessons, {len(concordance)} plate entries) and Cosmogony Book Codex (7 chapters).")


if __name__ == "__main__":
    main()
