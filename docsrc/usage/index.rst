:navigation: header
:order: 20
:nav_title: Usage

.. _usage:

Using This Edition
==================

.. rubric:: Reader's Guide to the Interactive Cosmogonic Codices & Parametric 3D Engine

The GEOMETOR edition of Walter and Lao Russell's cosmogony unites the 48 lessons of the *Home Study Course* (1950–1952) and the newly synthesized *Wave-Field Cosmogony* with interactive 3D WebGL models, parametric vector diagrams, and rich scholarly apparatus.

Interactive Codex Features
--------------------------

1. Synchronized Reading Tracks & Units
   The edition provides two complete codices accessible from the top header:
   
   * **Wave-Field Cosmogony:** A 7-chapter geometric treatise synthesizing the still magnetic light, conical vortices, cube-sphere equators, light-sphere lenses, gyroscopic precession, and 9-octave periodic table.
   * **Home Study Course:** The complete unabridged 12 Units (48 Lessons) with original student dialogues, meditations, and diagram plates.

2. Primary-Source Plate Milestones & Vector Reconstructions
   All 102 original diagram plates (`Figs. 1–180`) from the Russell Foundation printings are paired with clean, theme-adaptive GEOMETOR vector plates. Marginal references link directly to specific figures and plate numbers.

3. Interactive 3D WebGL Models & Parametric SVGs
   Explore Walter Russell's wave-field geometry in full 3D:
   
   * **Six-Axis Conical Vortices (`Plates II–III`):** Rotate and inspect centripetal generative cones and centrifugal radiative cones.
   * **Cube-Sphere of Nine Equators (`Plate IV`):** Interactive visualization of the 3 orthogonal and 6 diagonal zero-curvature boundary planes.
   * **Eight-Octant Light-Sphere Lens (`Plate V`):** Curvature reversal across orthogonal equators.
   * **Gyroscopic Precession (`Plate VI`):** Amplitude plane tilting from 0° to 90°.
   * **Unified 9-Octave Helix (`Plates VII–VIII`):** Interactive periodic element spiral.

4. Full-Text Search with In-Page Highlighting
   The sidebar search queries both treatises and all 48 lessons. Search query parameters automatically append ``?highlight=`` to highlight matched terms directly inside lessons and chapters.

5. Faceted Navigation & Collection Views
   Browse cosmogonic principles, element octaves, and historical figures via the sidebar index. Collection pages support switching between **Cards**, **Banners**, and **List** layout modes.

6. People, Bibliography & Glossary Tooltips
   Hovering over any thinker (:person:`Walter Russell <russell>`, :person:`Lao Russell <lao-russell>`, :person:`Nikola Tesla <tesla>`, :person:`Johannes Kepler <kepler>`, :person:`Dmitri Ivanovich Mendeleev <mendeleev>`), citation (:cite:`russell-1926`, :cite:`russell-1950`), or technical term (:term:`cube-sphere wave-field <cube-sphere-wave-field>`, :term:`still magnetic light <still-magnetic-light>`, :term:`nine equators of zero curvature <nine-equators-of-zero-curvature>`) displays an instant context card.

----

Command-Line & Python 3D Modeling API
-------------------------------------

In addition to the interactive web viewer, all five 3D wave-field scenes can be generated, inspected, and exported from the command line and Python.

Command-Line Interface
~~~~~~~~~~~~~~~~~~~~~~

List available 3D models and export them as Wavefront ``.obj``, JSON scene graphs, or orthographic SVGs:

.. code-block:: bash

   # List available parametric 3D Russell models
   geometor-russell list

   # Export all models to Wavefront .obj files
   geometor-russell export --model all --format obj --out ./build/models3d/

   # Export an orthographic SVG projection of the Cube-Sphere
   geometor-russell export --model cube_sphere --format svg --yaw 34 --pitch 22 --out ./build/svg/

Python API
~~~~~~~~~~

Import the procedural geometry engine directly in Python:

.. code-block:: python

   from geometor.russell.models3d import build_all_models, build_cube_sphere_model
   from geometor.russell.export import export_obj

   # Construct the parametric 9-equator cube-sphere scene
   scene = build_cube_sphere_model()
   print(f"Scene: {scene.title} with {len(scene.elements)} geometric primitives")

   # Export to Wavefront OBJ format
   obj_content = export_obj(scene)
