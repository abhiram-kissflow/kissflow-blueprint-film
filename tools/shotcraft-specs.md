# Shotcraft specs for the HTML + GSAP port (8 cards)

Source library: `/Users/abhiram/.claude/skills/video-shotcraft` (read-only). Card = `references/shots/<cat>/<name>.md`; demo = `demos/<cat>/<name>/*.tsx`.
All demos: 1920x1080, **30 fps** (Remotion). Seconds = frames / 30. Every card carries the caveat "demo was tuned on greyscale/placeholder content; the numbers are a starting point, re-verify on real assets".

## Resolution (library.json)

| Requested | Resolved to | Style keys |
|---|---|---|
| text-as-mask | exact | text-as-mask |
| word-relay-geometry | exact | word-relay-geometry |
| steep-tilt-glide | exact | steep-tilt-glide |
| transition-travel | exact | shared-element-morph (A), letterform-zoom (C) - both covered |
| timeline-travel | exact | timeline-travel |
| beat-step-list-theme-cycle | exact | beat-step-list-theme-cycle |
| wall-reveal-moves . bento-light-up | exact | bento-light-up (siblings not covered: grid-wave-flip, wireframe-draw-on) |
| theme-switch-moves . theme-sweep-toggle | exact | theme-sweep-toggle (sibling not covered: palette-theme-ripple) |

## Shared GSAP toolkit (use for every card)

Principle: GSAP has no Remotion `interpolate`/`Easing.bezier`/`spring`. Two deterministic patterns:

- **Pattern P (pure render function)** - one linear proxy tween drives `frame`; a pure `render(frame)` writes all styles. Use for anything multi-parameter (word-relay, steep-tilt, beat-step, bento, timeline-travel). Seek-safe because `onUpdate` fires on every seek.
- **Pattern N (native tweens)** - plain `tl.to(..., {ease})` for simple single-property moves.

```js
const FPS = 30, F = n => n / FPS;                       // frames -> seconds
const clamp01 = x => Math.min(1, Math.max(0, x));
const lerp = (t, a, b) => a + (b - a) * t;
// Remotion interpolate(f,[a,b],[y0,y1],{easing, clamp})
const itp = (f, a, b, y0, y1, ease = x => x) => y0 + (y1 - y0) * ease(clamp01((f - a) / (b - a)));
// multi-breakpoint interpolate, easing applied PER SEGMENT (Remotion semantics)
const itpN = (x, xs, ys, ease = t => t) => { for (let i = 0; i < xs.length - 1; i++) if (x <= xs[i+1]) return ys[i] + (ys[i+1]-ys[i]) * ease(clamp01((x-xs[i])/(xs[i+1]-xs[i]))); return ys[ys.length-1]; };
// Easing.bezier(x1,y1,x2,y2): exact, inline, deterministic (bisection; y may overshoot 1)
const bz = (x1,y1,x2,y2) => x => { let lo=0, hi=1, t=0; for (let i=0;i<40;i++){ t=(lo+hi)/2; const xt=3*(1-t)**2*t*x1+3*(1-t)*t*t*x2+t**3; xt<x? lo=t: hi=t; } return 3*(1-t)**2*t*y1+3*(1-t)*t*t*y2+t**3; };
// Remotion/E easings -> GSAP strings when a string ease is enough
// Easing.out(cubic)=E.outCubic=Easing.out(poly(3)) -> "power2.out" ; quad out -> "power1.out"; inQuad -> "power1.in"
// inOutCubic -> "power2.inOut" ; Easing.inOut(quad) -> "power1.inOut"   (GSAP powerN = t^(N+1))
const E = { outCubic:t=>1-(1-t)**3, outQuad:t=>t*(2-t), inQuad:t=>t*t, inOutCubic:t=>t<.5?4*t**3:1-(-2*t+2)**3/2, inOutQuad:t=>t<.5?2*t*t:-1+(4-2*t)*t };
// Pattern P driver (shot starts at S seconds on the master timeline, length N frames)
const proxy = { f: 0 };
tl.fromTo(proxy, { f: 0 }, { f: N, duration: F(N), ease: 'none', onUpdate: () => render(proxy.f) }, S);
```
Rules: no `Math.random`/`Date.now`; every "random" is a sine hash (see bento / particles). Set initial state by calling `render(0)` once at build. Pass a function directly as `ease:` when a custom curve is needed (GSAP accepts `ease: t => y`).

Remotion `spring({damping,stiffness,mass})` -> analytic damped spring (underdamped):
```js
// zeta = c/(2*sqrt(k*m)); w0 = sqrt(k/m); wd = w0*sqrt(1-zeta^2);  s(tau)=1-e^(-zeta*w0*tau)*(cos(wd*tau)+(zeta*w0/wd)*sin(wd*tau))
const spring = (tau, c, k, m) => { const z=c/(2*Math.sqrt(k*m)), w0=Math.sqrt(k/m), wd=w0*Math.sqrt(1-z*z); return 1-Math.exp(-z*w0*tau)*(Math.cos(wd*tau)+(z*w0/wd)*Math.sin(wd*tau)); };
```

---

## 1. text-as-mask  (opening/text-as-mask.md; demo `demos/opening/text-as-mask/TextAsMask.tsx`)

**Visual / meaning.** Dark field, a huge bold word ("SCALE") whose letterforms are windows onto a slowly drifting product screenshot; at the end the glyph mask scales 26x so the product takes over the full frame. "The word is the door, the product is inside it." Use for brand-word/slogan + product opener or a chapter card that doubles as a transition into product. Camera-static, the door moves (contrast: transition-travel C moves the camera into the letter).

**Demo parameters (30 fps, 150f = 5.0 s).**
| Segment | Frames | Seconds | Detail |
|---|---|---|---|
| hold | 0-20 | 0-0.667 | dashboard at translateX(+110), scale 1.15 |
| drift | 20-100 | 0.667-3.333 | translateX 110 -> -110, **linear** (2.75 px/f = 82.5 px/s), scale constant 1.15, origin 50% 50% |
| takeover | 100-130 | 3.333-4.333 | one bezier(0.4,0,0.2,1) progress `endT` 0->1 |
| still | 130-150 | 4.333-5.0 | locked |
- Takeover channels (all from `endT`): `maskS = 1 -> 26`; drift x `-110 -> 0` (linear in endT); content scale `1.15 -> 1`; unmasked cover layer opacity `interpolate(endT,[0.25,0.9],[0,1])` linear, clamped; caption "TEXT AS MASK" (30px/700, letter-spacing 10, bottom 90, colour #8f8f8d) fades 1->0 over f100-114 (3.333-3.8 s).
- Mask: SVG 1920x1080, `<text x=960 y=666 font-size=360 font-weight=900 letter-spacing=-8 text-anchor=middle fill=white>SCALE</text>`, Helvetica/Arial, as a data-URI on CSS `mask-image` (+ `-webkit-`), `no-repeat`, `mask-size:1920px 1080px`. Background #2f2f2f.
- **Mask transform-origin `61.5% 50%`** (= 1180.8, 540: the vertical stem of the letter L - a solid stroke).
- Structure: wrapper (mask + `scale(maskS)`, origin 61.5% 50%) > counter layer (`scale(1/maskS)`, same origin) > motion layer (`translateX(dx) scale(dashS)`, origin 50% 50%) > screenshot. A second full-screen **unmasked** motion layer (same dx/dashS) sits on top at opacity `cover`.

**Pitfalls (translated).**
- Params tuned on greyscale/placeholder; re-verify with real footage.
- The product image shows in close-up inside the strokes for the entire shot: rasterize real material at high resolution; low-res screenshots turn to mush in the strokes.
- Changing the word or font invalidates the hand-picked origin; render and check that the zoom centres on a solid stroke, adjust origin (origin inside a counter/hole reveals only the background colour on scale-up).
- Do not use together with transition-travel C in one film (same "world grows out of letters" move reads as the same trick twice).
- Mask layer and content layer transforms must be driven separately (wrapper scales, content counter-scales); merged, the product also inflates 26x.
- Min glyph size >= 360 px at weight 900 (thin strokes = product through a door crack). Scale 26x is tuned to word/frame ratio; too little leaves glyph-edge remnants. Seam safety: the unmasked cover layer fades in over endT 0.25-0.9.
- Hold >= 20 f of true stillness at end; product ends in standard composition.

**GSAP port.**
```html
<div id="tam" style="position:absolute;inset:0;background:#2f2f2f;overflow:hidden">
  <div id="maskWrap" style="position:absolute;inset:0;transform-origin:61.5% 50%;
       -webkit-mask-image:var(--maskUrl);mask-image:var(--maskUrl);-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;
       -webkit-mask-size:1920px 1080px;mask-size:1920px 1080px">
    <div id="counter" style="position:absolute;inset:0;transform-origin:61.5% 50%">
      <div class="motion" style="position:absolute;inset:0;transform-origin:50% 50%"><img src="product.png" style="width:1920px;height:1080px"></div>
    </div>
  </div>
  <div id="cover" style="position:absolute;inset:0;opacity:0">
    <div class="motion" style="position:absolute;inset:0;transform-origin:50% 50%"><img src="product.png" style="width:1920px;height:1080px"></div>
  </div>
  <div id="cap" style="position:absolute;bottom:90px;width:100%;text-align:center;font:700 30px Helvetica;letter-spacing:10px;color:#8f8f8d">TEXT AS MASK</div>
</div>
```
`--maskUrl: url("data:image/svg+xml,"+encodeURIComponent(svgString))` (set from JS). Timeline (shot start S):
```js
const motions = gsap.utils.toArray('#tam .motion');
const setMotion = (dx, s) => motions.forEach(m => m.style.transform = `translateX(${dx}px) scale(${s})`);
setMotion(110, 1.15);
tl.to({}, { duration: F(80), ease: 'none',                       // drift 0.667 -> 3.333 s
  onUpdate() { setMotion(110 - 220 * this.progress(), 1.15); } }, S + F(20));
const st = { e: 0 }, bz1 = bz(.4,0,.2,1);
tl.to(st, { e: 1, duration: F(30), ease: bz1,                    // takeover 3.333 -> 4.333 s (ease applied by GSAP; st.e is already eased)
  onUpdate() { const e = st.e, ms = 1 + 25 * e;
    gsap.set('#maskWrap', { scale: ms }); gsap.set('#counter', { scale: 1 / ms });
    setMotion(-110 * (1 - e), lerp(e, 1.15, 1));
    gsap.set('#cover', { opacity: clamp01((e - .25) / .65) }); } }, S + F(100));
tl.to('#cap', { opacity: 0, duration: F(14), ease: 'none' }, S + F(100));
```
(Because `st.e` is the eased value, linear mappings of `e` match the demo exactly.) Hidden risk: Chromium rasterizing a data-URI SVG mask under a 26x transform may soften edges; check the frame at ~3.7 s - the cover layer takes over by endT 0.9 anyway.

**Inputs.** One 1920x1080 hi-res product screenshot (or short loop); the headline word (<= ~6 letters, bold; re-tune origin if changed); font stack Helvetica/Arial 900.

---

## 2. word-relay-geometry  (typography/word-relay-geometry.md; demo `demos/typography/word-relay-geometry/WordRelayGeometry.tsx`)

**Visual / meaning.** Three benefit words (Faster / Better / Stronger) on near-black; each owns a bespoke geometry: word 1 a rotating dashed circle that grows 0.4->1; word 2 three interlocking solid circles that "trim-draw" in sequence; word 3 a metal sheen sweep then resolve to pure white with glow (the "conclusion"). Old word shrinks to 0.86 and fades; new word goes outline -> fill reveal; 20 drifting dust motes stitch the three beats into one space. Use for 3-point benefit statements, value sections, "one word, one world" mid-film progressions. Energy medium-high, no still frames.

**Coordinate system.** Designed on a **480x270** stage scaled **x4** to 1920x1080 (all numbers below are design px; text 56 px = 224 px final). Port as a 480x270 div with `transform:scale(4);transform-origin:0 0`.

**Timing.** 180f = 6.0 s; normalised `t = frame/179` (t=1 at last frame). 1 t-unit = 179/30 = **5.967 s**. Slots (t -> seconds):
| Word | t0 | t1 | start s | end s |
|---|---|---|---|---|
| Faster | 0.00 | 0.36 | 0 | 2.148 |
| Better | 0.32 | 0.68 | 1.909 | 4.057 |
| Stronger | 0.64 | 1.00 | 3.819 | 5.967 |
Overlap 0.04 t (0.239 s). Windows (all `seg(t,a,b,ease)` = clamp-normalise then ease):
- `tin = seg(t0, t0+0.07, outCubic)` (0.418 s); `tout = seg(t1-0.05, t1, inQuad)` (0.298 s; last word: 0). Layer opacity `alive ? tin*(1-tout) : 0`; word scale `lerp(tout,1,0.86)`, `translate(-50%,-52%)`.
- Faster/Better fill reveal: `fillp = seg(t0+0.06, t0+0.18, inOutCubic)` (0.358-1.074 s after t0); fill layer `clip-path: inset(-20% ${(1-fillp)*100}% -20% 0)`; outline opacity `1 - fillp*0.75`.
- Stronger: `sh = seg(t0+0.05, t0+0.20, outQuad)`; `sweep = seg(t0+0.08, t0+0.26, inOutCubic)` (0.477-1.551 s); `white = seg(t0+0.27, t0+0.34, outQuad)` (1.611-2.029 s). Outline opacity `1-sh`; sheen layer opacity `sh*(1-white)`, `background-position: lerp(sweep,100,0)% 0`; white layer opacity `white`, `text-shadow:0 0 ${white*18}px rgba(255,255,255,.3)`.
- Dashed circle: cx0 cy0 r=100 (`CIRC_R 78 + 22`), stroke #565e78 width 1.1, `stroke-dasharray:5 7`, `grow = seg(t0+0.01, t0+0.14, outCubic)`, opacity `grow*(1-tout)`, `transform: rotate(${-90 + t*30}deg) scale(${lerp(grow,0.4,1)})` (**global t**: slow continuous spin, 30 deg over the film, ~5 deg/s).
- Solid circles: r=62, cx -110/0/110, same stroke; `pathLength=1; stroke-dasharray=1; stroke-dashoffset = 1 - max(0, trim)`, `trim = seg(t0+0.02+d, t0+0.14+d, outCubic) - seg(t1-0.06, t1, inQuad)`, d = 0 / 0.06 (0.358 s) / 0.12 (0.716 s); `transform: rotate(-90)`.
- Text: font `-apple-system,"Helvetica Neue",sans-serif` 56/800, line-height 1; outline layer `color:transparent; -webkit-text-stroke:1px #6a7186`; fill layer `#fff` absolutely overlaid. Sheen: `linear-gradient(100deg,#585f72 0%,#8d95aa 38%,#ffffff 50%,#8d95aa 62%,#585f72 100%)`, `background-size:280% 100%`, `background-clip:text`. Stage bg #07080c.
- Dust (20): `rand(s)=frac(sin(s*127.1+311.7)*43758.5453)`; `size=1+rand(3i)*1.4`, `x=rand(i)*100 %`, `ph=rand(i+40)`, `sp=0.5+rand(i+80)*0.8`; `top = ((1-((t*sp+ph)%1))*110-5)%`; opacity `0.12+0.18*sin((t*3+ph)*2π)^2`; white, round.
- SVG viewBox `-240 -135 480 270` (origin at centre).

**Pitfalls (translated).**
- Tuned on placeholder; verify with real assets.
- The three words must be the same grammatical form (demo: comparative adjectives, 6-8 letters): slots are equal-length and geometry (radii, spacing) is hard-coded; a long word overflows the dashed ring or collides with the interlocking circles - retune `CIRC_R` and x offsets with the word list.
- `-webkit-text-stroke` exists only in Chromium/WebKit; Firefox shows transparent text (word vanishes). (HyperFrames renders in Chromium, fine; check preview browser.)
- SVG `pathLength=1` normalisation on `<circle>` is flaky in old browsers (circle draws fully, trim lost) - verify one frame on the target renderer.
- Exit trim = entry trim minus exit seg; if slot is shorter than 0.2 t the circles start retracting before fully drawn.
- Sheen and white layers cross-fade; if `white` and `sh` windows overlap too little there are 1-2 frames where both are half transparent (grey word).
- The promotion treatment (sheen + white) is for the last word only; applying to all kills the "conclusion" feel. Give the third entrance its own sound accent.
- Overlap 0.04: <0.02 reads as hard cut, >0.08 two words fight. Exit is shorter than entry and uses `inQuad` (exit with an out-curve reads reluctant). Shrink on exit, never grow. Dust > 40 reads as snow; geometry colour slightly darker than the outline (hierarchy).

**GSAP port (Pattern P).**
```html
<div id="wr" style="position:absolute;inset:0;background:#07080c;overflow:hidden">
 <div id="stage" style="position:absolute;left:0;top:0;width:480px;height:270px;overflow:hidden;transform:scale(4);transform-origin:0 0">
  <!-- 20 dust divs generated in JS (position:absolute;border-radius:50%;background:#fff) -->
  <div class="slot" data-i="0" style="position:absolute;inset:0">
    <svg viewBox="-240 -135 480 270" style="position:absolute;inset:0;width:100%;height:100%"> <!-- circles per slot, ids c0a, c1a..c, --></svg>
    <div class="wordbox" style="position:absolute;left:50%;top:50%;font:800 56px/1 -apple-system,'Helvetica Neue',sans-serif">
      <div class="outline" style="color:transparent;-webkit-text-stroke:1px #6a7186">Faster</div>
      <div class="fill" style="position:absolute;inset:0;color:#fff">Faster</div>
      <!-- slot 3 only: .white and .sheen overlays instead of .fill -->
    </div></div>
  <!-- slots 1 and 2 likewise -->
 </div></div>
```
`render(f)`: `t=f/179`; for each slot compute `tin,tout,fillp|sh,sweep,white,grow,trim` with the formulas above, then set `style.opacity`, `style.transform` (`translate(-50%,-52%) scale(...)`), `style.clipPath`, `strokeDashoffset`, `backgroundPosition` etc. Drive with `tl.fromTo(proxy,{f:0},{f:179,duration:179/30,ease:'none',onUpdate:()=>render(proxy.f)},S)`.

**Inputs.** Three words (same grammatical form, <= 8 letters), optional palette override (#07080c bg, #565e78 geometry, #6a7186 outline); no images. Final word is the "conclusion" (gets the sheen).

---

## 3. steep-tilt-glide  (camera/steep-tilt-glide.md; demo `demos/camera/steep-tilt-glide/SteepTiltGlide.tsx`, v7)

**Visual / meaning.** Fixed camera; an upright wide page stands as a slanted wall at 60 deg rotateY (right edge near, left edge vanishing) and **the page itself slides along its own horizontal axis** past the lens like train carriages, with speed ghosting, text components that "drop" from floating height onto the page, revealed from dark to bright. Use for showy tours of long/multi-section UI, dark neon tone; complement of graze-face-tour (there the camera moves).

**Parameters (30 fps, 120f = 4.0 s single shot).**
- Camera constants (never change in the shot): `perspective:1100px` on the wrapper, `perspective-origin:30% 58%`. Anchor div `position:absolute; left:40%; top:15%; transform: rotateY(-60deg) rotateZ(-2deg); transform-origin: left top`. Inside: `transform: scale(0.62) translateX(lx px)`, origin left top (so `lx` is in panel px, rendered x0.62). Angle history: -45 rejected, -53 "a bit more", **-60 chosen**; keep within 55-65.
- Panel: 6200x2400, bg #f4f4f6, radius 64, glow `0 0 220px rgba(220,210,255,.35)`. Page bg #060409.
- Glide: `lx = 60 + (-4100-60)*glide(f/120)`, `glide = bezier(0.3,0.12,0.72,0.9)` (end slope not zero -> never "settles dead"). Average speed 34.7 px/f.
- Shade (black overlay #050409 on panel): keyframes f[0,18,44] -> [0.7,0.4,0] linear, clamp right (0 -> 0.6 s -> 1.47 s). Extra left-edge shadow: `linear-gradient(90deg, rgba(5,4,9,.9), rgba(5,4,9,0) 42%)` opacity `min(1, shade*1.6)`.
- Ghosts (drawn first, behind): `speed = |lx(f-1) - lx(f+1)|/2`; `g1 = min(0.42, speed*0.03)` at `lx(f-2.5)`, `g2 = min(0.22, speed*0.016)` at `lx(f-5)`; each rendered only if > 0.02. (Opacity proportional to speed; with 34.7 px/f average the caps bind most of the shot; constant ghosting reads as a glitch, so keep speed-proportional.) Each ghost is a whole copy of the panel layer with its own perspective wrapper.
- Float-drop: `t = interpolate(f,[4,100],[0,1])` (0.133-3.333 s); `lift(t,land,H=230) = (1 - easeFall(clamp((t-(land-0.32))/0.32))) * H`, `easeFall = bezier(0.5,0.05,0.6,1)`. FloatWrap(h): shadow copy `translate(h*.24, h*.46) scale(1+h*.0009)`, `filter: blur(5+h*.075 px) brightness(.35) saturate(.4)`, opacity `min(.38, .15+h*.0016)`; main `translate(-h*.34, -h*.8)`. Land times: tab title 0.30 (H230), "ClickUp 3.0" 0.42 (280), logo row 0.54 (250), Dropbox tile 0.62 (260), Home pill 0.68 (260), Inbox 0.80 (240), Docs 0.86 / Dashboards 0.92 (230).
- Purple halo: `radial-gradient(ellipse 40% 50% at 20% 66%, rgba(118,58,190,.30), transparent 70%)`, opacity `interpolate(f,[14,70],[.15,1])`. Vignette: `radial-gradient(ellipse 105% 95% at 55% 42%, transparent 60%, rgba(3,2,8,.25) 85%, rgba(2,1,6,.5) 100%)`.
- Panel contents (demo): left ~3500 px = top tab bar (230 tall) + sidebar items; right ~2640 px = "Product Management" list page (starts x=3560). Fonts 58-165 px at panel scale.

**Pitfalls (translated).**
- Tuned on placeholder; verify with real assets.
- **Crux: object moves, camera does not** - perspective, origin and rotY are constants for the whole shot; the only animated variable is the page's local translateX. A moving camera was explicitly rejected ("the camera is fixed; the page itself moves along the horizontal plane of its own 3D space"). Do not animate rotate/perspective.
- Angle is the identity of the card; practical range 55-65 deg, outside = a different technique. Beyond ~-70 content unreadable.
- Glide curve: stopping mid-shot was caught in review (v4); full-linear lacks the start breath.
- Ghost opacity must scale with speed.
- Page must be >= 3 screens wide (too narrow = 2-second slide).
- Differentiation: graze-face-tour = camera moves, page static (choose one per section); runway-ground-skim = top-down lying plane, orthogonal axis.
- Hand-building a 6200 px page is costly: use a real long screenshot instead (slide logic identical).

**GSAP port (Pattern P).**
```html
<div id="stg" style="position:absolute;inset:0;background:#060409;overflow:hidden">
  <div class="halo" style="position:absolute;inset:0"></div>
  <div class="layer ghost2" style="position:absolute;inset:0;perspective:1100px;perspective-origin:30% 58%"><div class="anchor"><div class="slide"><div class="panel">…</div></div></div></div>
  <div class="layer ghost1" …same…>
  <div class="layer main" …same…>
  <div class="vignette" style="position:absolute;inset:0;pointer-events:none"></div>
</div>
```
CSS: `.anchor{position:absolute;left:40%;top:15%;transform:rotateY(-60deg) rotateZ(-2deg);transform-origin:left top}`, `.slide{transform-origin:left top}`, `.panel{width:6200px;height:2400px}`. Replace the hand-built panel with `<img src="long-screenshot.png" style="width:6200px;height:2400px">` (keep aspect 6200:2400, or change `lx` end to `-(imgW - ~2100)`), plus a shade `div` and left-edge gradient `div`.
```js
const glide = bz(.3,.12,.72,.9);
const lxAt = f => lerp(glide(clamp01(f/120)), 60, -4100);
function render(f){
  const lx = lxAt(f), shade = itpN(Math.min(f,44),[0,18,44],[.7,.4,0]);
  const sp = Math.abs(lxAt(f-1)-lxAt(f+1))/2, g1=Math.min(.42,sp*.03), g2=Math.min(.22,sp*.016);
  setLayer(ghost2, lxAt(f-5), g2>.02?g2:0, shade); setLayer(ghost1, lxAt(f-2.5), g1>.02?g1:0, shade); setLayer(main, lx, 1, shade);
  // setLayer: slide.style.transform=`scale(.62) translateX(${lx}px)`; layer.style.opacity=op; shade overlay opacity=shade; edge overlay opacity=Math.min(1,shade*1.6)
  const drop = itp(f,4,100,0,1); floats.forEach(fl => setFloat(fl, lift(drop, fl.land, fl.H)));
  halo.style.opacity = itp(f,14,70,.15,1);
}
tl.fromTo(proxy,{f:0},{f:120,duration:4,ease:'none',onUpdate:()=>render(proxy.f)},S);
```
Float elements are only meaningful if the page is built from DOM text components (title, logo, tiles, etc.); with a flat screenshot omit the float-drop (keep slide, ghosts, shade).

**Inputs.** A very wide page image (>= 3 screens, e.g. 6200x2400) or a DOM-built page; for the demo look, dark bg with purple halo (#060409). Optionally separate foreground component crops for float-drop.

---

## 4. transition-travel  (transition/transition-travel.md; demos `demos/transition/transition-travel/SharedElementMorph.tsx`, `LetterformZoom.tsx`)

**Meaning.** "Fly-through" transitions (vs hand-off transitions in shot-transitions): the next scene already exists inside the previous frame as a real element (grid slot / glyph hole) and one continuous spatial move enters it - no hand-off instant. Choose per seam: next scene can be "pre-present" in the first -> fly-through; merely sequential -> hand-off. One seam, one technique; never add white flash/shake on top (reads as a mistake). Technique card, no energy slot; frames come from adjacent shots' budgets.

### 4A. shared-element-morph (detail -> overview, "put this card back")
**Visual.** A full-screen close-up of a card shrinks, translates and grows rounded corners, landing exactly in its slot in a dashboard grid with 3% overshoot.
**Parameters (30 fps, 130f = 4.333 s).**
| Segment | Frames | Seconds |
|---|---|---|
| close-up hold | 0-35 | 0-1.167 |
| morph (bezier(0.4,0,0.2,1), 0 -> **1.03**) | 35-60 | 1.167-2.0 (25f = 0.833 s) |
| settle (outCubic 1.03 -> 1) | 60-70 | 2.0-2.333 (10f = 0.333 s) |
| still | 70-130 | 2.333-4.333 (2 s) |
- One progress `p` drives left/top/width/height/radius: FULL `{0,0,1920,1080,r0}` -> SLOT `{x808,y590,w524,h454,r14}`; `lerp(p,...)`, so at p=1.03 it overshoots the slot by 3% of the travel.
- Slot math: sidebar 220 + grid padding 36 -> col width (1920-220-72-56)/3 = 524; header 72 + padding 36, row height (1008-72-28)/2 = 454; middle column x = 220+36+524+28 = 808; row 2 y = 72+36+454+28 = 590.
- Content is the same card rendered at slot size (524x454, seed 5) with `transform: scale(w/524)` origin top-left (3.664 -> 1; container clips overflow because aspect differs: 524x454 vs 16:9). Card's own radius `r / contentScale`, card shadow off.
- Container shadow: `0 ${lerp(ps,36,2)}px ${lerp(ps,110,8)}px rgba(0,0,0,${lerp(ps,.32,.06)})`, `ps=clamp(p,0,1)`; bg `#ffffff` (G.card), `overflow:hidden`.
- Background dashboard opacity 0.9 -> 1 over f58-63 (1.933-2.1 s) `Easing.out(quad)` (= "power1.out") - the "home arrival" beat.
**Pitfalls (translated).** Position, size and radius must share one progress curve (separate curves read as "morph" not "same object"); overshoot >5% looks like jelly. Content must be the slot-size render scaled uniformly (re-flowing content = a different card, breaks the fly-through); shadow must converge or the card never "lands". Slot coordinates must be pixel-exact (even a few px of post-landing correction reads as "flew near then snapped"). Background must idle at 0.9 and brighten at landing; full brightness all along removes the arrival beat. Pairs with F-style window-through (that goes in, this goes back).
**GSAP.**
```js
const m = { p: 0 };
const upd = () => { const p=m.p, ps=clamp01(p), cs=lerp(p,1920,524)/524;
  Object.assign(hero.style,{left:lerp(p,0,808)+'px',top:lerp(p,0,590)+'px',width:lerp(p,1920,524)+'px',height:lerp(p,1080,454)+'px',borderRadius:lerp(p,0,14)+'px',
    boxShadow:`0 ${lerp(ps,36,2)}px ${lerp(ps,110,8)}px rgba(0,0,0,${lerp(ps,.32,.06)})`});
  inner.style.transform=`scale(${cs})`; innerCard.style.borderRadius=lerp(p,0,14)/cs+'px'; };
tl.to(m,{p:1.03,duration:F(25),ease:bz(.4,0,.2,1),onUpdate:upd},S+F(35))
  .to(m,{p:1,duration:F(10),ease:'power2.out',onUpdate:upd},S+F(60))
  .fromTo('#dashA',{opacity:.9},{opacity:1,duration:F(5),ease:'power1.out'},S+F(58));
```
DOM: `#dashA` full-screen overview screenshot; `#hero` (absolute, overflow hidden, bg #fff) > `#inner` (524x454, origin top left) containing the detail card at slot size.

### 4C. letterform-zoom (chapter title card -> body, "title is the door")
**Visual.** A beige plate with a giant word "DASH" punched out as a mask hole, showing the next page through the glyphs; an exponential push-in through the triangular counter of "A"; when the hole fills the frame the new page takes over and leftover strokes fly off.
**Parameters (30 fps, 140f = 4.667 s).**
| Segment | Frames | Seconds |
|---|---|---|
| establish hold | 0-25 | 0-0.833 |
| push | 25-85 | 0.833-2.833 (60f = 2.0 s) |
| B dolly recovery | 85-110 | 2.833-3.667 (outCubic, 1.1 -> 1) |
| still | 110-140 | 3.667-4.667 |
- `t = interpolate(f,[25,85],[0,1], bezier(0.6,0,0.85,0.5))` (slow start, steep end); `scale = 28^t` (`ZOOM_MAX = 28`, exponential = constant perceived speed). Origin = counter centre `(773, 508)` px for BOTH plate and B layer (font-metric estimate for Helvetica Neue 900, 560px: "DASH" width ~2.833 em, centred start x~167, "A" spans 571-975, baseline y=741, centre ~0.42 em above baseline).
- Plate: SVG 1920x1080; `<mask>` = white rect + black `<text x=960 y=741 text-anchor=middle font-size=560 font-weight=900 font-family="Helvetica Neue,Helvetica,Arial,sans-serif">DASH</text>`; `<rect fill=#ececea mask=url(#cut)>`; extra stroked text (stroke #2f2f2f 3px, opacity .3, fill none) for hole edge legibility; subtitle bars at top 812: 240x16 #c2c2c0 and 130x16 #dcdcda radius 8, gap 16, centred; plate scales as one group.
- Plate opacity `interpolate(scale,[15,24],[1,0])` (linear in scale) -> with this curve scale 15 is reached at **f82** and 24 at **f85**: the plate vanishes in ~3 frames at the very end (0.1 s); unmount (display:none) when 0.
- Blur: desired visible blur `interpolate(t,[0,.45,1],[0,1.5,16])` px; CSS blur written as `visBlur / scale` (else the transform magnifies it into a smear wall); apply when > 0.02 px.
- B layer (next page, full screen, origin (773,508)): scale `lerp(t,1,1.1)` during push; after f85 `1.1 -> 1` over 25f outCubic.
**Pitfalls (translated).** Centre coordinates are a font-metric estimate; changed font/word/renderer kerning will drift - after rendering, check the first push frames and nudge origin (do not trust computed numbers). ZOOM_MAX scales with hole size (smaller counter => bigger factor); slow start gives viewers time to see "something is in the hole". `blur` must be divided by scale. B must dolly with the push, else the hole shows a dead still ("flying into a living page" perception breaks). Not stacked with white flash / shake. Do not use alongside text-as-mask in the same film.
**GSAP.**
```js
const m = { t: 0 }, push = bz(.6,0,.85,.5);
tl.to(m,{t:1,duration:2,ease:push,onUpdate(){ const s=Math.pow(28,m.t);
  const vb=itpN(m.t,[0,.45,1],[0,1.5,16]);
  Object.assign(plate.style,{transform:`scale(${s})`,transformOrigin:'773px 508px',opacity:1-clamp01((s-15)/9),display:s>=24?'none':'block',filter:vb/s>.02?`blur(${vb/s}px)`:'none'});
  B.style.transform=`scale(${lerp(m.t,1,1.1)})`; }},S+F(25));
tl.fromTo(B,{scale:1.1,transformOrigin:'773px 508px'},{scale:1,duration:F(25),ease:'power2.out'},S+F(85));
```
(Opacity = `interpolate(scale,[15,24],[1,0])` = `1 - clamp01((s-15)/9)`.) Keep `transformOrigin` set once at build, not in the tween. Keep B's own origin also at 773px 508px.

**Inputs.** A: an overview screenshot (with slot at exact px) + a hi-res detail of that card. C: plate colour/title word, next-page screenshot (1920x1080); font stack Helvetica Neue 900 (re-check origin if swapped).

---

## 5. timeline-travel  (data/timeline-travel.md; demo `demos/data/timeline-travel/TimelineTravel.tsx`)

**Visual / meaning.** Horizontal time-axis trip: camera starts slow, sprints, brakes at "Today"; as the camera passes each version tick (v1.0, v2.0, v3.0, Today) a card springs up from the tick (overshoot), no stop; final tick gets a 1.28x push-in. Speed says "we ship fast", the stop says "now is what matters". Use for changelog/milestones/history. Horizontal counterpart of scroll-brake-moves (vertical list brake).

**Parameters (30 fps, 160f = 5.333 s).**
- Rest f0-12 (0.4 s); travel f12-104 (92f = **3.067 s**, "estop" frame 104 = 3.467 s); zoom f104-114 (10f = 0.333 s) `1 -> 1.28`, `Easing.out(cubic)`, transform-origin `50% 62%`; still to f160 (card asks >= 30 f; demo ends at 160).
- World: `W=1920`, axis y=700, TICK_GAP 1400, ticks at world x = 960, 2360, 3760, 5160; `WORLD_W = 960+4200+960 = 6120`; world layer moves by `translateX(-camX)`, camX total = 4200 px. 22 minor dots at `x = 960 + i*280`, 4x24 px #c2c2c0 (y = 688); axis line left 200, width WORLD_W-400, 6 px #c2c2c0; tick: 6x56 #2f2f2f centred on axis, label 40px/800 #2f2f2f below (top +44, width 160).
- Camera curve: `t = (f-12)/92` clamped; `eased = interpolate(t, [0,.15,.88,1], [0,.055,.9,1], {easing: Easing.inOut(Easing.quad)})` - **easing is per segment** (so velocity touches zero at t=0.15 and 0.88, and the last 12% moves 0.9 -> 1). `camX = eased * 4200`. Replicate exactly (pop frames derive from it).
- Card pop frames (computed by inverting camX; demo code: first frame where camX >= tick.x-960, minus 6): v1.0 **f6**, v2.0 **f48**, v3.0 **f63**, Today **f98** (0.2 s, 1.6 s, 2.1 s, 3.267 s). Card 360x240, `top = 700-36-240`, `transform-origin 50% 100%`, `transform: scaleY(s) scaleX(0.6+0.4*s)`, opacity `min(1, 2s)`, mounted from pop frame; `s = spring({damping:11, stiffness:160, mass:0.9, durationInFrames:26})`: zeta = 0.458, w0 = 13.3 rad/s, ~20% overshoot, peak ~0.265 s natural (~f8); Remotion's `durationInFrames:26` compresses time slightly (estimate x1.3 -> peak ~f6 so the card peaks as camera passes).
- Title "TIMELINE TRAVEL" at top 90, 64 px (placeholder).

**Pitfalls (translated).** Placeholder-tuned. Mid-sprint too slow = no "journey" feel; constant speed = cheap PPT. Pop 6 f before the camera reaches the tick (later = viewers already missed it; much earlier = reads as a preview). Minor ticks are the speed references; delete them and the speed vanishes. Without push-in the stop is only "stopped", push-in makes "arrived". If sprint blurs the cards, wrap only the fast section in camera motion blur. Reserve >= 30 f of stillness after the stop first, then schedule the travel backwards (demo v1 had 25 f only). Each pop card is an information slot - use real version highlights; make sure at least the last two are legible at passing speed. Sound: a light tick per pop, an impact on the stop.

**GSAP port (Pattern P).**
```html
<div id="tt" style="position:absolute;inset:0;background:#ececea;overflow:hidden">
  <div id="zoomL" style="position:absolute;inset:0;transform-origin:50% 62%">
    <div id="world" style="position:absolute;left:0;top:0;width:6120px;height:1080px"> axis, 22 dots, 4 ticks(+label), 4 .pop cards (transform-origin:50% 100%) </div>
  </div></div>
```
```js
const camX = f => itpN(clamp01((f-12)/92),[0,.15,.88,1],[0,.055,.9,1],E.inOutQuad)*4200;
const POP = [6,48,63,98];                     // or compute by scanning camX like the demo
const STRETCH = 1.3;                          // estimate of Remotion durationInFrames:26 time compression
function render(f){
  world.style.transform=`translateX(${-camX(f)}px)`;
  zoomL.style.transform=`scale(${itp(f,104,114,1,1.28,E.outCubic)})`;
  cards.forEach((c,i)=>{ const k=f-POP[i]; if(k<0){c.style.display='none';return;}
    const s = k>=26?1:spring(k/30*STRETCH,11,160,.9);  // snap to 1 at the 26f horizon
    Object.assign(c.style,{display:'block',transform:`scaleY(${s}) scaleX(${.6+.4*s})`,opacity:Math.min(1,s*2)}); });
}
tl.fromTo(proxy,{f:0},{f:160,duration:160/30,ease:'none',onUpdate:()=>render(proxy.f)},S);
```
Note the card's spring can go slightly >1 (overshoot) and `scaleY` > 1 is intended. Verify the 26-frame cut: with STRETCH 1.3 the spring at k=26 is ~0.2 s x... compare to 1; adjust STRETCH until residual < 0.5%.

**Inputs.** 4 milestone labels (v1.0/v2.0/v3.0/Today) and 4 card images or DOM cards (real version highlights, 360x240 or rescale); title text.

---

## 6. beat-step-list-theme-cycle  (rhythm/beat-step-list-theme-cycle.md; demo `demos/rhythm/beat-step-list-theme-cycle/BeatStepListThemeCycle.tsx`)

**Visual / meaning.** "Metronome": dark field with a vertical adjective list; a fixed pill at the viewport centre "catches" the next word on each beat while its colour and the whole background colour change in the same frame - three channels (row, colour, field) locked to one beat. Use for "same product, many moods/themes" sections (modern / playful / expressive...), the densest rhythm beat of a film, music-synced.

**Parameters (30 fps, 110f = 3.667 s).**
- Pre-roll f0-30 (1.0 s) static. `BEAT_LEN = 18f (0.6 s ~ 100 BPM)`, `FIRST_BEAT = 30`, `N_BEATS = 3` -> beats at f30/48/66 = **1.0 s / 1.6 s / 2.2 s**; snap windows 6f (0.2 s) at the head of each beat; remaining 12f (0.4 s) fully still; last beat holds 72-110 (1.267 s).
- `beat = clamp(floor((f-30)/18)+1, 0, 3)`; `beatStart = 30 + (beat-1)*18`; `tInBeat = beat==0 ? 1 : snap((f-beatStart)/6)`, `snap(x)=1-(1-clamp(x))^3.2`; `step = beat==0 ? 0 : (beat-1) + tInBeat` -> list `translateY(-step*150px)` (ROW_H 150).
- Words (need >= beats+2): `['modern','playful','expressive','seamless','intuitive']`, 92 px / 800 / letter-spacing -1.5, selected index = `beat` (flips on the beat's first frame, integer), colour: selected `#fff` (beat 0: `#2a2018`), others `rgba(255,255,255,.34)`.
- Themes (pill / bg): [0] `#d8d8d4` / `#241a12`; [1] `#4fae62` / `#1e2416`; [2] `#8e6fd8` / `#221a33`; [3] `#d64d55` / `#141c2e`. Colours: per-channel RGB linear mix between `THEMES[beat-1]` and `THEMES[beat]` at `tInBeat` (the eased value).
- Pill: fixed, 900x130, `left:50%`, `top: 540 - ROW_H/2 + 10 = 475`, height `ROW_H-20 = 130`, radius 999, shadow `0 14px 40px rgba(0,0,0,.35)`, `scale(pop)`, `pop = beat==0 ? 1 : interpolate(tInBeat,[0,.6,1],[1.12,.97,1])` (keyed on the **eased** value, so squash is also a 6-frame move). List container `top: 540 - 75 = 465`. Feather gradients 300 px top and bottom from `bgColor` (live, not hard-coded), z-index above text.

**Pitfalls (translated).**
- Placeholder-tuned. Three channels must share one beat clock (one `tInBeat` drives list, colours and squash; a lagging channel turns "in-step" into three animations).
- Snap window 6f (not >10f) with steep ease-out (exponent 3.2); otherwise "jump" turns into "slide" and the metronome becomes a scrolling list. Beat length <12f is unreadable, >26f scatters; 3-4 beats (5+ glazes, 1-2 doesn't establish the metronome).
- Without squash the pill looks like a recoloured texture; >1.2 steals attention.
- Adjacent theme backgrounds must have equal lightness and different hue (dark -> light reads as a flash).
- Pre-roll 30f essential (else the first beat reads as a bug); hold >= 30f after the last beat.
- Keep the selection flip on the integer beat, colour on the fractional value (both fractional = half-white mid-state words).
- Strongly sound-dependent: align BEAT_LEN to the music BPM; silent version reads as UI glitching. Do not run next to cel-flash-stomp (same 0.6 s cadence - beat fatigue). Differs from theme-switch-moves (single ceremonial swap vs repeated swap as a beat).
- Feather colour must track bgColor.

**GSAP port (Pattern P).**
```html
<div id="bs" style="position:absolute;inset:0"><div id="pill" style="position:absolute;left:50%;top:475px;width:900px;height:130px;margin-left:-450px;border-radius:999px;box-shadow:0 14px 40px rgba(0,0,0,.35)"></div>
 <div id="list" style="position:absolute;left:0;right:0;top:465px"> <!-- .row{height:150px;display:flex;align-items:center;justify-content:center} span{font:800 92px Helvetica;letter-spacing:-1.5px;position:relative;z-index:2} --></div>
 <div id="fadeT" style="position:absolute;left:0;right:0;top:0;height:300px;z-index:3"></div><div id="fadeB" style="position:absolute;left:0;right:0;bottom:0;height:300px;z-index:3"></div></div>
```
```js
const snap = x => 1-Math.pow(1-clamp01(x),3.2);
const mix = (a,b,t) => { const p=h=>[1,3,5].map(i=>parseInt(h.slice(i,i+2),16)); const A=p(a),B=p(b); return `rgb(${A.map((v,i)=>Math.round(v+(B[i]-v)*t)).join(',')})`; };
function render(f){ const beat=Math.min(3,Math.max(0,Math.floor((f-30)/18)+1)), start=30+(beat-1)*18;
  const tb = beat===0?1:snap((f-start)/6), step = beat===0?0:(beat-1)+tb;
  list.style.transform=`translateY(${-step*150}px)`;
  const prev=THEMES[Math.max(0,beat-1)], now=THEMES[beat];
  const pillC=mix(prev.pill,now.pill,tb), bgC=mix(prev.bg,now.bg,tb);
  pill.style.background=pillC; pill.style.transform=`scale(${beat===0?1:itpN(tb,[0,.6,1],[1.12,.97,1])})`; bs.style.background=bgC;
  fadeT.style.background=`linear-gradient(${bgC},transparent)`; fadeB.style.background=`linear-gradient(transparent,${bgC})`;
  spans.forEach((s,i)=> s.style.color = i===beat ? (beat===0?'#2a2018':'#fff') : 'rgba(255,255,255,.34)'); }
tl.fromTo(proxy,{f:0},{f:110,duration:110/30,ease:'none',onUpdate:()=>render(proxy.f)},S);
```
Native alternative: per beat at `S+1.0/1.6/2.2`, `tl.to(listState,{step:+1,duration:.2,ease:t=>1-Math.pow(1-t,3.2)})` etc. Pattern P preferred (same clock for all channels).

**Inputs.** Word list (>= beats+2 words, same part of speech), theme table (pill colour + same-lightness dark bg per beat), tempo/BPM of the music (set BEAT_LEN = 1800/BPM frames... BEAT_LEN_s = 60/BPM).

---

## 7. wall-reveal-moves . bento-light-up  (ui-entrance/wall-reveal-moves.md; demo `demos/ui-entrance/wall-reveal-moves/BentoLightUp.tsx`)

**Visual / meaning.** Dark 3x2 bento wall dimmed to 18%; an amber stroke races around each cell's border, then the cell's content brightens and rises into place with a small back-out overshoot; six cells in even sequence, then a slow 4% push settles. Elements show "in place" (no travel in), layout valid from frame 1. Use for solemn/dark brand sections and calm feature overviews. Ask first: should this wall "pour in" (deck-deal-flyin) or "light up" (this card)? Sibling styles (not in scope): grid-wave-flip, wireframe-draw-on.

**Parameters (30 fps, 150f = 5.0 s).**
- bg `#2a2a28`, `AMBER #e8b45e`. Cells 480x330, gutter 44, grid left = (1920-(3*480+2*44))/2 = **196**, top = (1080-(2*330+44))/2 + 30 = **218**; cell i: col=i%3, row=floor(i/3), x = 196 + col*524, y = 218 + row*374, radius 14.
- Cell i start `s_i = 20 + 12*i` -> f20, 32, 44, 56, 68, 80 (0.667 s, +0.4 s steps; last cell fully lit ~f94-96 = 3.2 s). Even spacing = the solemnity; do not accelerate.
  - stroke `draw = interpolate(f,[s,s+8],[0,1], outCubic)`: SVG `<rect x=2 y=2 w=cell-4 h=cell-4 rx=14 fill=none stroke=#e8b45e stroke-width=4 pathLength=100 stroke-dasharray=100 stroke-dashoffset=100*(1-draw)>` with `filter: drop-shadow(0 0 (6+jitter*4)px #e8b45e)`; opacity `strokeFade = interpolate(f,[s+12,s+26],[1,0.4], outQuad)`; svg translateY follows `ty` (same as card).
  - content `lit = interpolate(f,[s+6,s+14],[0,1], outCubic)` (relay: starts 6f after the stroke begins, i.e. after >half the stroke = 0.2 s); `rise = same window, bezier(0.3,1.4,0.5,1)` (back-out overshoot); `opacity = 0.18 + 0.82*lit`; `ty = 20*(1-rise)`; glow `= lit*(1-lit)*4*(14 + jitter*6)` px, box-shadow `0 0 glow rgba(232,180,94, 0.35*lit*(1-lit)*4)` applied only when `lit > 0.5` (demo behaviour; the parabola peaks at lit=.5).
  - `jitter_i = |frac(sin(i*127.3)*43758.5453)|` = 0, 0.718, 0.774, 0.516, 0.606, 0.93 for i=0..5 (sine hash, no random).
- Push: f96-121 (3.2-4.033 s, 25f = 0.833 s) `scale 1 -> 1.04`, bezier(0.33,0,0.2,1), origin 960px 540px, whole wall; then still f121-150 (0.967 s).
- Title "Features": 64 px dark bold inverted to white, at left 196, top 218-110 = 108, opacity `interpolate(f,[20,40],[.25,.75], outQuad)`.

**Pitfalls (translated).**
- Placeholder-tuned. 12f cascade is the balance between "each cell readable" and "wall drags"; 8-10f ok for more cells but keep spacing uniform.
- Stroke and content pop must **relay, not sync** (same-frame = whole cell flashes). Glow pulse peak magnitude varies per cell by seed (sine hash, never real random).
- Wall-lighting is a "single high-quality light effect": at most once per film (A + wireframe-draw-on in one film counts as two - pick one).
- Dim state 0.18 only works on a dark base (#2a2a28); on a light base it reads as fading/glitch.
- Pure "reveal in place"; no mixed translate-in (that is deck-deal-flyin).
- Static >= 15f at the end, all glow/shadow residue locked.

**GSAP port (Pattern P).**
```html
<div id="bl" style="position:absolute;inset:0;background:#2a2a28;overflow:hidden"><div id="wall" style="position:absolute;inset:0;transform-origin:960px 540px">
  <div id="title" style="position:absolute;left:196px;top:108px;font:800 64px Helvetica;color:#fff">Features</div>
  <!-- x6 -->
  <div class="cell" style="position:absolute;left:..;top:..;width:480px;height:330px">
    <div class="card" style="border-radius:14px">…real feature card HTML/screenshot 480x330…</div>
    <svg width="480" height="330" viewBox="0 0 480 330" style="position:absolute;left:0;top:0;overflow:visible"><rect x="2" y="2" width="476" height="326" rx="14" fill="none" stroke="#e8b45e" stroke-width="4" pathLength="100" stroke-dasharray="100"/></svg>
  </div></div></div>
```
```js
const bk = bz(.3,1.4,.5,1), push = bz(.33,0,.2,1), JIT=[0,.718,.774,.516,.606,.93];
function render(f){ cells.forEach((c,i)=>{ const s=20+12*i, j=JIT[i];
  const draw=itp(f,s,s+8,0,1,E.outCubic), fade=itp(f,s+12,s+26,1,.4,E.outQuad), lit=itp(f,s+6,s+14,0,1,E.outCubic), rise=itp(f,s+6,s+14,0,1,bk);
  const ty=20*(1-rise), g=lit*(1-lit)*4*(14+j*6);
  c.card.style.opacity=.18+.82*lit; c.card.style.transform=`translateY(${ty}px)`;
  c.card.style.boxShadow = lit>.5?`0 0 ${g}px rgba(232,180,94,${.35*lit*(1-lit)*4})`:'none';
  c.rect.style.strokeDashoffset=100*(1-draw); c.rect.style.opacity=fade; c.rect.style.filter=`drop-shadow(0 0 ${6+j*4}px #e8b45e)`;
  c.svg.style.display = draw>0?'block':'none'; c.svg.style.top=ty+'px'; });
  wall.style.transform=`scale(${itp(f,96,121,1,1.04,push)})`; title.style.opacity=itp(f,20,40,.25,.75,E.outQuad); }
tl.fromTo(proxy,{f:0},{f:150,duration:5,ease:'none',onUpdate:()=>render(proxy.f)},S);
```
Native alternative per cell (start `S+(20+12i)/30`): `rect strokeDashoffset 100->0, .267s power2.out`; at +0.2 s card `opacity .18->1 .267s power2.out` and `y 20->0 .267s ease:bz(.3,1.4,.5,1)`; stroke opacity `1->.4` from +0.4 s for 0.467 s `power1.out`.

**Inputs.** 6 cell contents (feature cards ~480x330, real UI/hi-res), a heading, dark bg #2a2a28 (must be dark), accent colour (amber default #e8b45e).

---

## 8. theme-switch-moves . theme-sweep-toggle  (interaction/theme-switch-moves.md; demo `demos/interaction/theme-switch-moves/ThemeSweepToggle.tsx`)

**Visual / meaning.** The same dashboard in light and dark stacked; the dark version is revealed by a 15-degree slanted edge sweeping left-top to right-bottom with a 4 px white glowing edge line; where the edge passes light turns to dark in place, both themes coexisting for a moment ("same UI re-skins", not a scene change). Use for dark-mode/theming feature narration. Sibling style (not in scope): palette-theme-ripple (cmd-K collapses to a dot, circular ripple re-skins). Max one theme switch per film (it's feature narrative, not a transition).

**Parameters (30 fps; timeline ends settle at f64; source comment says static from f70; total length not stated in source - card says 3-4 s, ~120f is a safe frame budget).**
| Segment | Frames | Seconds |
|---|---|---|
| initial still (light) | 0-14 | 0-0.467 |
| sweep | 14-52 | 0.467-1.733 (38f = 1.267 s) |
| settle (dark scale) | 52-64 | 1.733-2.133 |
| static | 64+ | 2.133+ |
- Edge top x: `p = interpolate(f,[14,52],[-20, 1920+SLANT+40], Easing.out(Easing.poly(3)))` = `power2.out` (fast then slow); `SLANT = 1080*tan(15 deg) = 289.4 px`. Over-sweep (+40 px and +SLANT) so no light triangle remains bottom-right (p max = 2249.4).
- Dark layer: `clip-path: polygon(0 0, p px 0, (p-SLANT) px 1080px, 0 1080px)` (top edge right, bottom edge left -> "/" boundary), on top of the light layer.
- Edge line: 4 px x 1240 px white, `box-shadow: 0 0 18px 4px rgba(255,255,255,.75)`, `left: p - SLANT/2 - 2`, `top: 540-620 = -80`, `transform: rotate(15deg)` origin 50% 50%; opacity `interpolate(f,[14,18,48,54],[0,1,1,0])` linear; mounted only for 14 <= f < 54.
- Settle: dark layer `scale` keyframes f[52,53,64] -> [1, 0.995, 1] with `outCubic` per segment, origin 50% 50% (very subtle; card suggests 0.985 for real work).
- Palettes (hand-mapped, **no filters**): LIGHT bg #ececea, panel #f7f7f6, line #dcdcda, bar #c2c2c0, mid #8f8f8d, card #ffffff, border #d8d8d6, side #3a3a3a, sideBar #5a5a58. DARK bg #1c1c1b, panel #242423, line #3a3a38, bar #6e6e6c, mid #8f8f8d, card #2c2c2b, border #454543, side #0f0f0e, sideBar #6a6a68.
- Layout (identical in both): sidebar 220; header 72 (#panel, 2px bottom line); grid padding 36, gap 28, 3 cols x 2 rows, cards radius 14 with 2 px border.

**Pitfalls (translated).** Placeholder-tuned. Dark palette = per-key manual mapping (bg/card/border each set), filter-inverted dark is wrong (images/avatars invert). Both layouts must be pixel-identical or it reads as "switched to another page". Unmount light/edge layers after the sweep for true stillness. Real pages: take two real screenshots (light, dark) instead of a fake dark. One switch per film. Sound: one long whoosh over the sweep.

**GSAP port.**
```html
<div id="ts" style="position:absolute;inset:0;overflow:hidden;background:#ececea">
  <img id="light" src="ui-light.png" style="position:absolute;inset:0;width:1920px;height:1080px">
  <div id="darkWrap" style="position:absolute;inset:0;transform-origin:50% 50%;clip-path:polygon(0 0,-20px 0,-309px 1080px,0 1080px)"><img src="ui-dark.png" style="width:1920px;height:1080px"></div>
  <div id="edge" style="position:absolute;top:-80px;width:4px;height:1240px;background:#fff;box-shadow:0 0 18px 4px rgba(255,255,255,.75);transform:rotate(15deg);opacity:0"></div>
</div>
```
```js
const SLANT = 1080*Math.tan(15*Math.PI/180), P0=-20, P1=1920+SLANT+40, m={p:P0};
const draw = () => { const p=m.p; darkWrap.style.clipPath=`polygon(0 0,${p}px 0,${p-SLANT}px 1080px,0 1080px)`; edge.style.left=(p-SLANT/2-2)+'px'; };
draw();
tl.to(m,{p:P1,duration:F(38),ease:'power2.out',onUpdate:draw},S+F(14));
tl.fromTo(edge,{opacity:0},{opacity:1,duration:F(4),ease:'none'},S+F(14))
  .to(edge,{opacity:0,duration:F(6),ease:'none'},S+F(48));            // hold 1 from f18 to f48 -> keyframes [14,18,48,54]
tl.to(darkWrap,{scale:.995,duration:F(1),ease:'power2.out'},S+F(52))
  .to(darkWrap,{scale:1,duration:F(11),ease:'power2.out'},S+F(53));
```
Optionally apply `scale:.985` for visibility. If light/dark are DOM-built, share one DOM and swap CSS variables per layer (two copies, same structure).

**Inputs.** Two pixel-aligned 1920x1080 screenshots/DOMs of the same UI: light and dark (real, not filtered); optional accent for the edge line (default white).
