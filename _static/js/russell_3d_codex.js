/* GEOMETOR • russell — Interactive 3D Cosmogony Engine for Sphinx Book Codex
 * Automatically mounts onto any <div class="russell-3d-mount" data-russell-scene="...">
 * Supports: cube_sphere, conical_vortex, light_lens, gyroscopic, periodic_helix
 */
(function () {
  'use strict';

  const PAL = {
    bg: '#0c0e14',
    panel: '#121621',
    border: '#262e42',
    zero: '#e8b85a',
    zeroFill: 'rgba(232,184,90,0.14)',
    diagFill: 'rgba(56,189,248,0.08)',
    positive: '#fb7185',
    negative: '#38bdf8',
    amplitude: '#fef08a',
    ampText: '#0c0e14',
    frame: 'rgba(235,230,220,0.75)',
    muted: 'rgba(148,158,176,0.38)',
    text: '#ebe6dc',
    subtext: '#949eb0'
  };

  const OCTAVES = [
    { n: 1, rom: 'I', start: ['Al', 'Alphanon'], els: [['H₁', 'First Octave Crest', '4±']], end: ['Be', 'Betanon'] },
    { n: 2, rom: 'II', start: ['Be', 'Betanon'], els: [['H₂', 'Second Octave Crest', '4±']], end: ['Ga', 'Gammanon'] },
    { n: 3, rom: 'III', start: ['Ga', 'Gammanon'], els: [['H', 'Hydrogen', '4±']], end: ['He', 'Helium'] },
    { n: 4, rom: 'IV', start: ['He', 'Helium'], els: [['Li','Lithium','1+'],['Be','Beryllium','2+'],['B','Boron','3+'],['C','Carbon','4±'],['N','Nitrogen','3-'],['O','Oxygen','2-'],['F','Fluorine','1-']], end: ['Ne', 'Neon'] },
    { n: 5, rom: 'V', start: ['Ne', 'Neon'], els: [['Na','Sodium','1+'],['Mg','Magnesium','2+'],['Al','Aluminum','3+'],['Si','Silicon','4±'],['P','Phosphorus','3-'],['S','Sulfur','2-'],['Cl','Chlorine','1-']], end: ['Ar', 'Argon'] },
    { n: 6, rom: 'VI', start: ['Ar', 'Argon'], els: [['K','Potassium','1+'],['Ca','Calcium','2+'],['Sc','Scandium','3+'],['Ti','Titanium','4+'],['Cr','Chromium','4+'],['Fe','Iron','4±'],['Co','Cobalt','4±'],['Cu','Copper','4-'],['Zn','Zinc','4-'],['Ga','Gallium','3-'],['Ge','Germanium','3-'],['As','Arsenic','3-'],['Se','Selenium','2-'],['Br','Bromine','1-']], end: ['Kr', 'Krypton'] },
    { n: 7, rom: 'VII', start: ['Kr', 'Krypton'], els: [['Rb','Rubidium','1+'],['Sr','Strontium','2+'],['Y','Yttrium','3+'],['Zr','Zirconium','4+'],['Mo','Molybdenum','4+'],['Ru','Ruthenium','4±'],['Rh','Rhodium','4±'],['Ag','Silver','4-'],['Cd','Cadmium','4-'],['In','Indium','3-'],['Sn','Tin','3-'],['Sb','Antimony','3-'],['Te','Tellurium','2-'],['I','Iodine','1-']], end: ['Xe', 'Xenon'] },
    { n: 8, rom: 'VIII', start: ['Xe', 'Xenon'], els: [['Cs','Cesium','1+'],['Ba','Barium','2+'],['La','Lanthanum','3+'],['Nd','Neodymium','3+'],['Gd','Gadolinium','4+'],['Hf','Hafnium','4+'],['W','Tungsten','4±'],['Os','Osmium','4±'],['Pt','Platinum','4-'],['Au','Gold','4-'],['Hg','Mercury','4-'],['Pb','Lead','3-'],['Bi','Bismuth','3-'],['Po','Polonium','2-'],['At','Astatine','1-']], end: ['Rn', 'Radon'] },
    { n: 9, rom: 'IX', start: ['Rn', 'Radon'], els: [['Fr','Francium','1+'],['Ra','Radium','2+'],['Ac','Actinium','3+'],['Th','Thorium','4+'],['Pa','Protactinium','4+'],['U','Uranium','4±']], end: ['Ω', 'Omega Inert'] }
  ];

  const GYRO_DATA = [
    { t: '0', name: 'Inert Gas Seed', inc: 0, a: 0.30, c: 0.06, rings: 1, role: 'zero' },
    { t: '1+', name: 'Prolate Nebula', inc: 22.5, a: 0.15, c: 0.35, rings: 0, role: 'positive' },
    { t: '2+', name: 'Winding Spheroid', inc: 45, a: 0.21, c: 0.32, rings: 0, role: 'positive' },
    { t: '3+', name: 'Integrating Spheroid', inc: 67.5, a: 0.27, c: 0.31, rings: 0, role: 'positive' },
    { t: '4±', name: 'True Sphere (Carbon / Sun)', inc: 90, a: 0.33, c: 0.33, rings: 1, role: 'amplitude' },
    { t: '3-', name: 'Oblate Spheroid', inc: 112.5, a: 0.33, c: 0.23, rings: 1, role: 'negative' },
    { t: '2-', name: 'Ringed System (Saturn)', inc: 135, a: 0.32, c: 0.16, rings: 2, role: 'negative' },
    { t: '1-', name: 'Ring Nebula (Lyra)', inc: 157.5, a: 0.35, c: 0.10, rings: 2, role: 'negative' },
    { t: '0', name: 'Inert Gas Rebirth', inc: 180, a: 0.30, c: 0.06, rings: 1, role: 'zero' }
  ];

  const SCENE_CONFIGS = {
    cube_sphere: {
      title: 'INTERACTIVE 3D • CUBE-SPHERE LATTICE & ALL NINE EQUATORS',
      subtitle: 'Drag to orbit • Scroll to zoom • 3 Orthogonal + 6 Diagonal Zero-Curvature Planes & 27 Zero-Nodes',
      slider: ['Sphere Inscription', 82],
      presets: [
        ['Isometric', 0.62, 0.42, 1.0, 0.22],
        ['Front (Z=0)', 0.0, 0.0, 1.05, 0.0],
        ['Corner Triad', 0.7854, 0.6155, 1.05, 0.15],
        ['Polar Top', 0.0, 1.57, 1.05, 0.0]
      ],
      layers: { ortho: ['3 Ortho Planes', true], diag: ['6 Diag Planes', true], sphere: ['Unit Sphere', true], nodes: ['27 Zero-Nodes', true], cones: ['Spiral Cones', false] }
    },
    conical_vortex: {
      title: 'INTERACTIVE 3D • SIX-FACE CONICAL VORTEX & VITALITY ENGINE',
      subtitle: 'Drag to orbit • Scrub Vitality from Dormant Seed (0%) to Full Cube-Face Polarization (100%)',
      slider: ['Vitality / Polarization', 92],
      presets: [
        ['3D 6-Axis Vortex', 0.55, 0.35, 1.0, 0.24],
        ['Magnet Profile (Fig. 159)', 0.0, 0.0, 1.08, 0.05],
        ['Polar Throat', 0.0, 1.52, 1.1, 0.28]
      ],
      layers: { primary: ['Polar Y-Cones', true], allSix: ['All 6 Face Cones', true], equators: ['Curved Equators', true], cube: ['Bounding Cube', true] }
    },
    light_lens: {
      title: 'INTERACTIVE 3D • EIGHT-OCTANT LIGHT-SPHERE LENS & CORONAL RINGS',
      subtitle: 'Drag to orbit • Field curves lose curvature (κ=0) on all 3 zero equators & reverse concavity across octants',
      slider: ['Lens Inflection & Rings', 75],
      presets: [
        ['3D Optical Lens', 0.48, 0.34, 0.95, 0.22],
        ['Equatorial (Fig. 171)', 0.0, 0.0, 0.98, 0.0],
        ['Ring Genesis (Fig. 172)', 0.25, 0.20, 0.85, 0.22]
      ],
      layers: { equators: ['3 Zero Equators', true], octantRays: ['Inflecting Rays', true], gravityFocus: ['8 Octant Focus', true], rings: ['Coronal Rings', true] }
    },
    gyroscopic: {
      title: 'INTERACTIVE 3D • GYROSCOPIC PRECESSION & SPHEROID MORPHOGENESIS',
      subtitle: 'Scrub Octave Position: Prolate Winding (1+,2+,3+) → 90° True Sphere (4± Carbon/Sun) → Oblate Rings (3-,2-,1-)',
      slider: ['Octave Precession', 50],
      presets: [
        ['3D Wave Arch', -0.28, 0.28, 0.96, 0.20],
        ['Front Arch (Plate VI)', 0.0, 0.0, 0.98, 0.0],
        ['Top Precession', 0.0, 1.45, 0.96, 0.15]
      ],
      layers: { heroSpheroid: ['Live Scrub Spheroid', true], stageModels: ['9 Octave Stages', true], arch: ['Wave Arch', true], rings: ['Planetary Rings', true] }
    },
    periodic_helix: {
      title: 'INTERACTIVE 3D • UNIFIED NINE-OCTAVE PERIODIC HELIX (FIGS. 177 ↔ 180)',
      subtitle: 'Switch between Axial Chart (Fig. 177 Concentric Spiral) and Lateral Wave (Fig. 180 Corkscrew Vortex)!',
      slider: ['Axial Helix Stretch', 68],
      presets: [
        ['Axial Chart (Fig. 177)', 0.0, 0.0, 0.95, 0.0],
        ['3D Conical Vortex', -0.66, 0.36, 0.95, 0.22],
        ['Lateral Wave (Fig. 180)', -1.5708, 0.04, 0.92, 0.04]
      ],
      layers: { spiral: ['9-Octave Spiral', true], octaveRings: ['Octave Shells', true], axes: ['0 & 4± Axes', true], labels: ['Element Symbols', true] }
    }
  };

  function mountWidget(container) {
    const sceneKey = container.getAttribute('data-russell-scene') || 'cube_sphere';
    const cfg = SCENE_CONFIGS[sceneKey];
    if (!cfg) return;

    const state = {
      slider: cfg.slider[1],
      phase: 0,
      autoOrbit: sceneKey !== 'gyroscopic',
      cam: { yaw: cfg.presets[sceneKey === 'periodic_helix' ? 1 : 0][1], pitch: cfg.presets[sceneKey === 'periodic_helix' ? 1 : 0][2], zoom: cfg.presets[sceneKey === 'periodic_helix' ? 1 : 0][3], persp: cfg.presets[sceneKey === 'periodic_helix' ? 1 : 0][4] },
      target: { yaw: cfg.presets[sceneKey === 'periodic_helix' ? 1 : 0][1], pitch: cfg.presets[sceneKey === 'periodic_helix' ? 1 : 0][2], zoom: cfg.presets[sceneKey === 'periodic_helix' ? 1 : 0][3], persp: cfg.presets[sceneKey === 'periodic_helix' ? 1 : 0][4] },
      layers: {},
      hovered: null,
      screenNodes: []
    };
    Object.keys(cfg.layers).forEach(k => { state.layers[k] = cfg.layers[k][1]; });

    container.style.cssText = 'background:#0c0e14;border:1.5px solid #262e42;border-radius:10px;padding:16px;margin:24px 0;color:#ebe6dc;font-family:"Fira Sans Condensed","Inter",sans-serif;';
    container.innerHTML = `
      <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:10px;border-bottom:1px solid #262e42;padding-bottom:10px;margin-bottom:10px;">
        <div>
          <div style="color:#e8b85a;font-weight:800;letter-spacing:0.8px;font-size:14px;">${cfg.title}</div>
          <div style="color:#949eb0;font-size:12px;margin-top:2px;">${cfg.subtitle}</div>
        </div>
        <div class="r3d-presets" style="display:flex;gap:6px;flex-wrap:wrap;"></div>
      </div>
      <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;margin-bottom:10px;">
        <div class="r3d-toggles" style="display:flex;gap:6px;flex-wrap:wrap;"></div>
        <div style="display:flex;align-items:center;gap:8px;font-size:12px;color:#ebe6dc;">
          <span>${cfg.slider[0]}:</span>
          <input type="range" class="r3d-slider" min="0" max="100" value="${state.slider}" style="width:120px;accent-color:#e8b85a;cursor:pointer;" />
          <span class="r3d-sval" style="color:#e8b85a;font-weight:700;min-width:42px;">${state.slider}%</span>
        </div>
      </div>
      <canvas class="r3d-canvas" style="width:100%;height:440px;display:block;border-radius:6px;cursor:grab;touch-action:none;"></canvas>
      <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;margin-top:10px;padding-top:8px;border-top:1px solid #262e42;font-size:12px;color:#949eb0;">
        <span class="r3d-status">Hover any 3D node to inspect coordinates &amp; locking tone.</span>
        <span>
          <span style="color:#e8b85a;">●</span> 0 Equator &nbsp;
          <span style="color:#fb7185;">●</span> + Centripetal &nbsp;
          <span style="color:#fef08a;">●</span> 4± Amplitude &nbsp;
          <span style="color:#38bdf8;">●</span> - Centrifugal
        </span>
      </div>
    `;

    const presetsBar = container.querySelector('.r3d-presets');
    cfg.presets.forEach(([lbl, yw, pt, zm, pr]) => {
      const b = document.createElement('button');
      b.textContent = lbl;
      b.style.cssText = 'background:#182032;color:#e8b85a;border:1px solid #334155;padding:4px 9px;border-radius:5px;cursor:pointer;font-size:12px;font-weight:600;';
      b.addEventListener('click', () => {
        state.autoOrbit = false;
        state.target = { yaw: yw, pitch: pt, zoom: zm, persp: pr };
      });
      presetsBar.appendChild(b);
    });

    const togglesBar = container.querySelector('.r3d-toggles');
    Object.keys(cfg.layers).forEach(k => {
      const b = document.createElement('button');
      const sync = () => {
        const on = state.layers[k];
        b.textContent = `${cfg.layers[k][0]}: ${on ? 'ON' : 'OFF'}`;
        b.style.cssText = `background:${on ? '#1e2638' : '#121621'};color:${on ? '#ebe6dc' : '#949eb0'};border:1px solid ${on ? '#e8b85a' : '#262e42'};padding:3px 8px;border-radius:5px;cursor:pointer;font-size:12px;`;
      };
      sync();
      b.addEventListener('click', () => { state.layers[k] = !state.layers[k]; sync(); });
      togglesBar.appendChild(b);
    });

    const sliderEl = container.querySelector('.r3d-slider');
    const svalEl = container.querySelector('.r3d-sval');
    const statusEl = container.querySelector('.r3d-status');
    const updateSval = () => {
      if (sceneKey === 'gyroscopic') {
        const deg = (state.slider / 100) * 180;
        svalEl.textContent = `${deg.toFixed(0)}°`;
      } else {
        svalEl.textContent = `${state.slider}%`;
      }
    };
    updateSval();
    sliderEl.addEventListener('input', e => {
      state.slider = Number(e.target.value);
      updateSval();
    });

    const canvas = container.querySelector('.r3d-canvas');
    const ctx = canvas.getContext('2d');
    let dragging = false, lx = 0, ly = 0;

    canvas.addEventListener('pointerdown', e => {
      dragging = true; lx = e.clientX; ly = e.clientY;
      canvas.setPointerCapture(e.pointerId);
    });
    canvas.addEventListener('pointermove', e => {
      const rect = canvas.getBoundingClientRect();
      const mx = e.clientX - rect.left, my = e.clientY - rect.top;
      if (dragging) {
        state.autoOrbit = false;
        state.target.yaw += (e.clientX - lx) * 0.008;
        state.target.pitch = Math.max(-1.54, Math.min(1.54, state.target.pitch + (e.clientY - ly) * 0.008));
        state.cam.yaw = state.target.yaw;
        state.cam.pitch = state.target.pitch;
        lx = e.clientX; ly = e.clientY;
        return;
      }
      let best = null, bestD = Infinity;
      for (const nd of state.screenNodes) {
        const d = Math.hypot(mx - nd.x, my - nd.y);
        if (d <= nd.r && d < bestD) { best = nd; bestD = d; }
      }
      state.hovered = best;
      statusEl.textContent = best ? best.desc : 'Hover any 3D node to inspect coordinates & locking tone.';
    });
    canvas.addEventListener('pointerup', () => { dragging = false; });
    canvas.addEventListener('wheel', e => {
      e.preventDefault();
      state.target.zoom = Math.max(0.55, Math.min(2.2, state.target.zoom * (e.deltaY < 0 ? 1.08 : 0.92)));
    }, { passive: false });

    function proj(x, y, z, w, h, baseScale) {
      const cy = Math.cos(state.cam.yaw), sy = Math.sin(state.cam.yaw);
      const cp = Math.cos(state.cam.pitch), sp = Math.sin(state.cam.pitch);
      const x1 = x * cy - z * sy;
      const z1 = x * sy + z * cy;
      const y2 = y * cp - z1 * sp;
      const z2 = y * sp + z1 * cp;
      const fov = 1.0 / Math.max(0.28, 1.0 + state.cam.persp * z2 * 0.35);
      const s = baseScale * state.cam.zoom * fov;
      return [w * 0.5 + x1 * s, h * 0.51 - y2 * s, z2];
    }

    function addLine(q, pts, col, width, w, h, sc, dashed) {
      for (let i = 0; i < pts.length - 1; i++) {
        const p1 = proj(pts[i][0], pts[i][1], pts[i][2], w, h, sc);
        const p2 = proj(pts[i + 1][0], pts[i + 1][1], pts[i + 1][2], w, h, sc);
        q.push({
          z: 0.5 * (p1[2] + p2[2]),
          fn: () => {
            ctx.beginPath();
            if (dashed) ctx.setLineDash([5, 4]);
            ctx.moveTo(p1[0], p1[1]); ctx.lineTo(p2[0], p2[1]);
            ctx.strokeStyle = col; ctx.lineWidth = width; ctx.stroke();
            if (dashed) ctx.setLineDash([]);
          }
        });
      }
    }

    function addPoly(q, verts, fill, stroke, width, w, h, sc) {
      const pv = verts.map(v => proj(v[0], v[1], v[2], w, h, sc));
      const za = pv.reduce((s, p) => s + p[2], 0) / pv.length;
      q.push({
        z: za + 0.05,
        fn: () => {
          ctx.beginPath();
          pv.forEach((p, i) => i === 0 ? ctx.moveTo(p[0], p[1]) : ctx.lineTo(p[0], p[1]));
          ctx.closePath();
          if (fill) { ctx.fillStyle = fill; ctx.fill(); }
          if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = width; ctx.stroke(); }
        }
      });
    }

    function addNode(q, pos, r, role, lbl, desc, w, h, sc, showLbl) {
      const p = proj(pos[0], pos[1], pos[2], w, h, sc);
      const col = role === 'amplitude' ? PAL.amplitude : (role === 'positive' ? PAL.positive : (role === 'negative' ? PAL.negative : PAL.zero));
      const isHov = state.hovered && state.hovered.desc === desc;
      const rad = isHov ? r * 1.35 : r;
      state.screenNodes.push({ x: p[0], y: p[1], r: Math.max(10, rad + 4), desc });
      q.push({
        z: p[2] - 0.04,
        fn: () => {
          ctx.beginPath();
          ctx.arc(p[0], p[1], rad, 0, Math.PI * 2);
          ctx.fillStyle = role === 'amplitude' ? col : PAL.panel;
          ctx.fill();
          ctx.strokeStyle = col;
          ctx.lineWidth = isHov ? 2.5 : 1.7;
          ctx.stroke();
          if (showLbl && lbl) {
            ctx.font = '700 12px sans-serif';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            if (rad >= 7.5 && lbl.length <= 2) {
              ctx.fillStyle = role === 'amplitude' ? PAL.ampText : col;
              ctx.fillText(lbl, p[0], p[1] + 0.5);
            } else {
              ctx.fillStyle = col;
              ctx.fillText(lbl, p[0], p[1] - rad - 8);
            }
          }
        }
      });
    }

    function drawFrame() {
      const dpr = window.devicePixelRatio || 1;
      const rect = canvas.getBoundingClientRect();
      const w = Math.max(300, Math.floor(rect.width));
      const h = Math.max(300, Math.floor(rect.height));
      if (canvas.width !== w * dpr || canvas.height !== h * dpr) {
        canvas.width = w * dpr; canvas.height = h * dpr;
      }
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      state.phase += 0.018;
      if (state.autoOrbit && !dragging) state.target.yaw += 0.004;
      state.cam.yaw += (state.target.yaw - state.cam.yaw) * 0.14;
      state.cam.pitch += (state.target.pitch - state.cam.pitch) * 0.14;
      state.cam.zoom += (state.target.zoom - state.cam.zoom) * 0.14;
      state.cam.persp += (state.target.persp - state.cam.persp) * 0.14;

      ctx.fillStyle = PAL.bg;
      ctx.fillRect(0, 0, w, h);

      state.screenNodes = [];
      const q = [];
      const L = state.layers;

      if (sceneKey === 'cube_sphere') {
        const sc = Math.min(w, h) * 0.28;
        for (const a of [-1, 1]) for (const b of [-1, 1]) {
          addLine(q, [[-1,a,b],[1,a,b]], PAL.frame, 1.5, w, h, sc);
          addLine(q, [[a,-1,b],[a,1,b]], PAL.frame, 1.5, w, h, sc);
          addLine(q, [[a,b,-1],[a,b,1]], PAL.frame, 1.5, w, h, sc);
        }
        if (L.ortho) {
          [[[0,-1,-1],[0,1,-1],[0,1,1],[0,-1,1]],[[-1,0,-1],[1,0,-1],[1,0,1],[-1,0,1]],[[-1,-1,0],[1,-1,0],[1,1,0],[-1,1,0]]]
            .forEach(pl => addPoly(q, pl, PAL.zeroFill, PAL.zero, 1.3, w, h, sc));
        }
        if (L.diag) {
          [[[-1,-1,-1],[1,1,-1],[1,1,1],[-1,-1,1]],[[-1,1,-1],[1,-1,-1],[1,-1,1],[-1,1,1]],
           [[-1,-1,-1],[1,-1,-1],[1,1,1],[-1,1,1]],[[-1,1,-1],[1,1,-1],[1,-1,1],[-1,-1,1]],
           [[-1,-1,-1],[-1,1,-1],[1,1,1],[1,-1,1]],[[1,-1,-1],[1,1,-1],[-1,1,1],[-1,-1,1]]]
            .forEach(pl => addPoly(q, pl, PAL.diagFill, PAL.negative, 1.0, w, h, sc));
        }
        if (L.sphere) {
          const rs = (0.35 + 0.65 * (state.slider / 100)) * (0.94 + 0.06 * Math.sin(state.phase * 1.5));
          const c1 = [], c2 = [], c3 = [];
          for (let i = 0; i <= 48; i++) {
            const a = (i / 48) * Math.PI * 2;
            c1.push([rs * Math.cos(a), rs * Math.sin(a), 0]);
            c2.push([rs * Math.cos(a), 0, rs * Math.sin(a)]);
            c3.push([0, rs * Math.cos(a), rs * Math.sin(a)]);
          }
          addLine(q, c1, PAL.negative, 1.6, w, h, sc);
          addLine(q, c2, PAL.negative, 1.6, w, h, sc);
          addLine(q, c3, PAL.negative, 1.6, w, h, sc);
        }
        if (L.cones) {
          for (const dir of [-1, 1]) {
            const sp = [];
            for (let i = 0; i <= 64; i++) {
              const t = i / 64, r = 0.88 * (1 - t), ang = t * Math.PI * 7 + state.phase * dir * 2;
              sp.push([r * Math.cos(ang), dir * (1 - t), r * Math.sin(ang)]);
            }
            addLine(q, sp, dir > 0 ? PAL.positive : PAL.negative, 2.0, w, h, sc);
          }
        }
        if (L.nodes) {
          for (const ix of [-1, 0, 1]) for (const iy of [-1, 0, 1]) for (const iz of [-1, 0, 1]) {
            const m = Math.abs(ix) + Math.abs(iy) + Math.abs(iz);
            addNode(q, [ix, iy, iz], m === 0 ? 8.0 : 4.8, m === 0 ? 'amplitude' : 'zero', '0',
              `Zero-Node (${ix}, ${iy}, ${iz}) • ${m === 0 ? 'Central 4± / 0 Fulcrum of all 9 Equators' : 'Cube-Sphere Zero Lattice Locus'}`,
              w, h, sc, m === 0);
          }
        }
      } else if (sceneKey === 'conical_vortex') {
        const sc = Math.min(w, h) * 0.29;
        const vit = Math.max(0.08, state.slider / 100);
        if (L.cube) {
          for (const a of [-1, 1]) for (const b of [-1, 1]) {
            addLine(q, [[-1,a,b],[1,a,b]], PAL.muted, 1.0, w, h, sc);
            addLine(q, [[a,-1,b],[a,1,b]], PAL.muted, 1.0, w, h, sc);
            addLine(q, [[a,b,-1],[a,b,1]], PAL.muted, 1.0, w, h, sc);
          }
        }
        const mapAx = (u, v, wa, ax, sgn) => ax === 'Y' ? [u, sgn * wa, v] : (ax === 'X' ? [sgn * wa, u, v] : [u, v, sgn * wa]);
        const axes = [];
        if (L.primary) axes.push(['Y', 1], ['Y', -1]);
        if (L.allSix) axes.push(['X', 1], ['X', -1], ['Z', 1], ['Z', -1]);
        axes.forEach(([ax, sgn]) => {
          const isY = ax === 'Y';
          const inS = [], outS = [];
          const steps = isY ? 76 : 48;
          for (let i = 0; i <= steps; i++) {
            const t = i / steps, wa = 1 - t * vit, r = (0.86 * (1 - t) + 0.03) * vit;
            const aIn = t * Math.PI * 6.5 * sgn + state.phase * 2.1 * sgn;
            inS.push(mapAx(r * Math.cos(aIn), r * Math.sin(aIn), wa, ax, sgn));
            outS.push(mapAx(r * Math.cos(-aIn + Math.PI), r * Math.sin(-aIn + Math.PI), wa, ax, sgn));
          }
          addLine(q, inS, PAL.positive, isY ? 2.2 : 1.2, w, h, sc);
          addLine(q, outS, PAL.negative, isY ? 1.6 : 1.0, w, h, sc, !isY);
        });
        if (L.equators) {
          for (const yb of [-0.65, -0.32, 0.0, 0.32, 0.65]) {
            const eq = [];
            for (let k = 0; k <= 32; k++) {
              const p = -1 + (2 * k) / 32;
              eq.push([0.82 * (1 - 0.3 * Math.abs(yb)) * p, yb - 0.19 * yb * (1 - p * p) * vit, 0]);
            }
            addLine(q, eq, Math.abs(yb) < 1e-4 ? PAL.zero : PAL.frame, Math.abs(yb) < 1e-4 ? 2.3 : 1.1, w, h, sc, Math.abs(yb) > 1e-4);
          }
        }
        addNode(q, [0, 0, 0], 6.5 + 3 * vit, 'amplitude', '4±', `Central Gravitational Apex • Vitality ${(vit * 100).toFixed(0)}%`, w, h, sc, true);
      } else if (sceneKey === 'light_lens') {
        const sc = Math.min(w, h) * 0.23;
        const amp = 0.12 + 0.36 * (state.slider / 100);
        if (L.equators) {
          const c1 = [], c2 = [], c3 = [];
          for (let k = 0; k <= 56; k++) {
            const a = (k / 56) * Math.PI * 2;
            c1.push([Math.cos(a), 0, Math.sin(a)]); c2.push([Math.cos(a), Math.sin(a), 0]); c3.push([0, Math.cos(a), Math.sin(a)]);
          }
          addLine(q, c1, PAL.zero, 2.4, w, h, sc); addLine(q, c2, PAL.zero, 1.6, w, h, sc); addLine(q, c3, PAL.zero, 1.6, w, h, sc);
        }
        if (L.octantRays) {
          for (let m = 0; m < 8; m++) {
            const az = (m * Math.PI) / 4 + Math.PI / 8, pts = [];
            for (let i = 0; i <= 52; i++) {
              const s = -1 + (2 * i) / 52, lat = s * Math.PI * 0.5, defl = amp * Math.sin(Math.PI * s), rxz = Math.cos(lat);
              pts.push([rxz * Math.cos(az + defl), Math.sin(lat), rxz * Math.sin(az + defl)]);
            }
            addLine(q, pts, m % 2 === 0 ? PAL.positive : PAL.negative, 1.8, w, h, sc);
          }
        }
        if (L.gravityFocus) {
          const inv3 = 1 / Math.sqrt(3);
          for (const sx of [-1, 1]) for (const sy of [-1, 1]) for (const sz of [-1, 1]) {
            const ray = [];
            for (let i = 0; i <= 20; i++) {
              const t = i / 20, b = 0.18 * (state.slider / 100) * Math.sin(Math.PI * t);
              ray.push([sx * inv3 * t, sy * inv3 * t + sy * b, sz * inv3 * t - sz * b * 0.5]);
            }
            addLine(q, ray, PAL.positive, 1.3, w, h, sc);
          }
        }
        if (L.rings) {
          [1.22, 1.50, 1.78].forEach((rb, idx) => {
            const rr = 1 + (rb - 1) * (0.7 + 0.55 * (state.slider / 100)), ring = [];
            for (let k = 0; k <= 56; k++) { const a = (k / 56) * Math.PI * 2; ring.push([rr * Math.cos(a), 0, rr * Math.sin(a)]); }
            addLine(q, ring, idx === 0 ? PAL.zero : PAL.negative, 1.6 - idx * 0.2, w, h, sc, idx === 2);
            const pa = state.phase * (1.1 - idx * 0.2) + idx * 2.1;
            addNode(q, [rr * Math.cos(pa), 0, rr * Math.sin(pa)], 4.8, 'negative', '', `Equatorial Coronal Ring ${idx + 1} (Fig. 172)`, w, h, sc, false);
          });
        }
        addNode(q, [0, 0, 0], 8.0, 'amplitude', '0', 'Center of Gravity • Maximum Light Compression (Fig. 171)', w, h, sc, true);
      } else if (sceneKey === 'gyroscopic') {
        const sc = Math.min(w, h) * 0.095;
        addLine(q, [[-4.3, -1.2, 0], [4.3, -1.2, 0]], PAL.zero, 2.0, w, h, sc);
        addLine(q, [[0, -1.4, 0], [0, 1.5, 0]], PAL.zero, 1.4, w, h, sc, true);
        if (L.arch) {
          const arch = [];
          for (let i = 0; i <= 72; i++) { const u = i / 72; arch.push([-4 + 8 * u, -1.2 + 2.15 * Math.sin(Math.PI * u), 0.25 * Math.sin(2 * Math.PI * u)]); }
          addLine(q, arch, PAL.frame, 1.8, w, h, sc);
        }
        const drawSph = (ctr, aE, cP, inc, rCnt, col, det) => {
          const tl = ((inc - 90) * Math.PI) / 180, ct = Math.cos(tl), st = Math.sin(tl);
          const xf = (lx, ly, lz) => {
            const cs = Math.cos(state.phase * 1.5), ss = Math.sin(state.phase * 1.5);
            const rx = lx * cs - lz * ss, rz = lx * ss + lz * cs;
            return [ctr[0] + rx * ct - ly * st, ctr[1] + rx * st + ly * ct, ctr[2] + rz];
          };
          addLine(q, [xf(0, -cP - 0.16 * det, 0), xf(0, cP + 0.16 * det, 0)], col, 1.7, w, h, sc);
          for (const vf of [-0.55, 0, 0.55]) {
            const va = vf * Math.PI * 0.5, rp = aE * Math.cos(va), yp = cP * Math.sin(va), lat = [];
            for (let k = 0; k <= 24; k++) { const a = (k / 24) * Math.PI * 2; lat.push(xf(rp * Math.cos(a), yp, rp * Math.sin(a))); }
            addLine(q, lat, col, vf === 0 ? 1.5 : 1.0, w, h, sc);
          }
          for (let m = 0; m < 2; m++) {
            const az = (m * Math.PI) / 2, mer = [];
            for (let k = 0; k <= 24; k++) { const a = (k / 24) * Math.PI * 2; mer.push(xf(aE * Math.cos(a) * Math.cos(az), cP * Math.sin(a), aE * Math.cos(a) * Math.sin(az))); }
            addLine(q, mer, col, 1.0, w, h, sc);
          }
          if (rCnt > 0 && L.rings) {
            for (let rk = 0; rk < rCnt; rk++) {
              const rd = aE + (0.14 + rk * 0.10) * det, rg = [];
              for (let k = 0; k <= 28; k++) { const a = (k / 28) * Math.PI * 2; rg.push(xf(rd * Math.cos(a), 0, rd * Math.sin(a))); }
              addLine(q, rg, Math.abs(inc - 90) < 4 ? PAL.zero : col, 1.4, w, h, sc, rk > 0);
            }
          }
        };
        if (L.stageModels) {
          GYRO_DATA.forEach((g, idx) => {
            const u = idx / 8, ctr = [-4 + 8 * u, -1.2 + 2.15 * Math.sin(Math.PI * u), 0.25 * Math.sin(2 * Math.PI * u)];
            const col = g.role === 'amplitude' ? PAL.amplitude : (g.role === 'positive' ? PAL.positive : (g.role === 'negative' ? PAL.negative : PAL.zero));
            drawSph(ctr, g.a * 0.9, g.c * 0.9, g.inc, g.rings, col, 0.9);
            addNode(q, ctr, g.role === 'amplitude' ? 6.8 : 4.6, g.role, g.t, `${g.t} • ${g.name} (Inclination ${g.inc}°, c/a = ${(g.c / g.a).toFixed(2)})`, w, h, sc, true);
          });
        }
        if (L.heroSpheroid) {
          const u = state.slider / 100, inc = u * 180;
          let aH = 0.70, cH = 0.70, rH = 1, col = PAL.amplitude;
          if (Math.abs(u - 0.5) < 0.03) { aH = 0.70; cH = 0.70; rH = 1; col = PAL.amplitude; }
          else if (u < 0.5) { const k = u / 0.5; aH = 0.34 + 0.36 * k; cH = 0.80 - 0.10 * k; rH = u < 0.08 ? 1 : 0; col = u < 0.08 ? PAL.zero : PAL.positive; }
          else { const k = (u - 0.5) / 0.5; aH = 0.70 + 0.08 * Math.sin(Math.PI * k); cH = 0.70 - 0.54 * k; rH = k > 0.25 ? 2 : 1; col = u > 0.92 ? PAL.zero : PAL.negative; }
          drawSph([0, -0.35, 1.35], aH, cH, inc, rH, col, 1.55);
        }
      } else {
        const sc = Math.min(w, h) * 0.205;
        const zs = state.slider / 68;
        if (L.axes) {
          addLine(q, [[0, 0, -2.5 * zs], [0, 0, 2.7 * zs]], PAL.zero, 2.2, w, h, sc);
          addLine(q, [[-2.05, 0, 0], [2.05, 0, 0]], PAL.zero, 1.9, w, h, sc);
          addLine(q, [[0, -2.05, 0], [0, 2.05, 0]], PAL.amplitude, 1.5, w, h, sc, true);
        }
        if (L.spiral) {
          const sp = [], tot = 320;
          for (let i = 0; i <= tot; i++) {
            const u = 1 + 9 * (i / tot), fr = i === tot ? 1 : u - Math.floor(u), az = Math.PI - 2 * Math.PI * fr;
            const r = 0.20 + 0.19 * (u - 1), z = (u - 5.2) * 0.52 * zs;
            sp.push([r * Math.cos(az), r * Math.sin(az), z]);
          }
          addLine(q, sp, PAL.frame, 1.7, w, h, sc);
        }
        if (L.octaveRings) {
          for (let octN = 4; octN <= 9; octN++) {
            const r = 0.20 + 0.19 * (octN - 0.5), z = (octN + 0.5 - 5.2) * 0.52 * zs, rg = [];
            for (let k = 0; k <= 44; k++) { const a = (k / 44) * Math.PI * 2; rg.push([r * Math.cos(a), r * Math.sin(a), z]); }
            addLine(q, rg, PAL.muted, 1.0, w, h, sc, true);
          }
        }
        OCTAVES.forEach(oct => {
          const sR = 0.20 + 0.19 * (oct.n - 1), sZ = (oct.n - 5.2) * 0.52 * zs;
          addNode(q, [-sR, 0, sZ], oct.n >= 4 ? 7.2 : 5.2, 'zero', oct.start[0], `Octave ${oct.rom} • ${oct.start[1]} (${oct.start[0]}) • Tone 0 Inert Seed`, w, h, sc, L.labels);
          const m = oct.els.length;
          oct.els.forEach((el, idx) => {
            const deg = m === 1 ? 90 : 162 - (144 * idx / (m - 1)), u = oct.n + ((180 - deg) / 180) * 0.55;
            const r = 0.20 + 0.19 * (u - 1), z = (u - 5.2) * 0.52 * zs, rad = (deg * Math.PI) / 180;
            const role = el[2] === '4±' ? 'amplitude' : (el[2].includes('+') ? 'positive' : 'negative');
            addNode(q, [r * Math.cos(rad), r * Math.sin(rad), z], el[2] === '4±' ? 7.8 : 5.2, role, el[0],
              `Octave ${oct.rom} • ${el[1]} (${el[0]}) • Tone ${el[2]} (${deg.toFixed(0)}°)`, w, h, sc, L.labels);
          });
        });
      }

      q.sort((a, b) => b.z - a.z);
      for (const item of q) item.fn();
      requestAnimationFrame(drawFrame);
    }
    requestAnimationFrame(drawFrame);
  }

  function initAll() {
    document.querySelectorAll('.russell-3d-mount').forEach(mountWidget);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAll);
  } else {
    initAll();
  }
})();
