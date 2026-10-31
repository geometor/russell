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
2. **Six Diagonal Planes of Zero Curvature**: Bisecting the 12 edges of the cube at $45^\circ$.
3. **Total Equators = 9**: Every polarized action-reaction cycle counts to **nine**—eight octants (or eight cube corners) centered by zero (`8 + 1 = 9`), expressed along the wave axis as the octave formula:

$$0 - 1^- - 2^- - 3^- - 4^- - \mathbf{0} - 4^+ - 3^+ - 2^+ - 1^+ - 0$$

.. figure:: /_static/svg/04_cube_sphere_nine_equators.svg
   :align: center
   :width: 98%

   **Plate IV (Fig. 114)**: Isometric projection of the Cube-Sphere Wave-Field showing the 3 orthogonal planes of zero curvature, the 27 zero-nodes (`0`) of the $3 \times 3 \times 3$ lattice, the inscribed sphere of curved motion, and the 9-count wave octave formula.

Interactive 3D Cube-Sphere & Double-Cone Explorer
-------------------------------------------------

Use the interactive 3D visualizer below to orbit the Cube-Sphere Wave-Field, inspect the 27 zero-nodes, toggle the 3 orthogonal and 6 diagonal planes of zero curvature, and observe the opposing centripetal/centrifugal spiral cones winding into the central sphere:

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
