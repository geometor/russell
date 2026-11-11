# GEOMETOR Russell

A digital reconstruction of Walter and Lao Russell's *Home Study Course* (1950–1952) and a new illustrated treatise on Russell's wave-field cosmogony, featuring revamped parametric SVG diagrams and interactive 3D animations.

## Overview

`geometor.russell` structures the 12 units (48 lessons) and 180 figures of the *Home Study Course in Universal Law, Natural Science and Philosophy* into a semantic Book Codex, while reconstructing Russell's chalkboard plates and periodic charts as precision vector graphics and parametric 3D models.

## Key Modules (`src/geometor/russell/` & `scripts/`)

- `src/geometor/russell/models3d.py`: Parametric 3D geometry generators for the five coupled Russellian primitives (`build_cube_sphere_lattice`, `build_conical_vortex_field`, `build_light_sphere_lens`, `build_gyroscopic_octave_system`, `build_periodic_helix_9_octave`).
- `src/geometor/russell/elements_data.py`: Structured 9-octave element dataset (`OCTAVE_SPECS`, `build_periodic_elements`) mapping locking tones (`0, 1+, 2+, 3+, 4±, 3-, 2-, 1-`) and gyroscopic angles across Octaves I–IX.
- `src/geometor/russell/export.py`: Exporters from `Scene3D` to Wavefront `.obj` (`export_obj`), `.json` (`export_json`), and depth-sorted 3D camera `.svg` (`export_svg_projection`).
- `src/geometor/russell/cli.py`: `geometor-russell` CLI (`list`, `export --model all --format obj|json|svg`).
- `docsrc/_static/js/russell_3d_codex.js`: Interactive 60fps 3D viewport engine mounted across Chapters II–VI of `docsrc/cosmogony/`.
- `scripts/generate_cosmogony_svgs.py`: Generator for the 8 dark-chalkboard parametric 2D SVG plates (`docsrc/_static/svg/`).
- `scripts/build_codices.py`: Compiler for both Book Codices (`docsrc/home_study_course/` and `docsrc/cosmogony/`) and the exported `.obj`/`.json` 3D assets (`docsrc/_static/models3d/`).

## Key Resources (`resources/home_study_course/`)

- `epub/OEBPS/Text/`: Clean XHTML source for `prelude.xhtml` and `lesson_01.xhtml` through `lesson_48.xhtml`.
- `epub/OEBPS/Images/`: 102 reference diagram plates (`image001.gif`–`image102.gif`) and `cover.png`.
- `docx_media/part_01/`–`part_12/`: 179 higher-resolution (`500px`–`1897px`) source images extracted prior to HTML/GIF downsampling.
- `pdfs/part_01.pdf`–`part_12.pdf`: Original 12 Unit PDFs (550 pages).
- `Fig_172_hires.png`: High-resolution (`2481 × 3508`) plate of `Figs. 170–172`.
