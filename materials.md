# Materials

Every string, number and screen in the film points to a file here. Status per recon:
SEEN (user's own account) · DOCS (official Kissflow) · CLAIM (in-app marketing copy).
Full product truth: ../kissflow-placewell-promo/replica/recon.md

## Brand (from the v7 project, Kissflow guideline)
- `brand/kissflow-logo.svg` — official flat mark; upright, full opacity, own colours, never 3D/recoloured.
- `fonts/graphik-{regular,medium,semibold}.ttf` — Graphik, no italics. "Kissflow", capital K, never all-caps.
- Colours: petals #CF2C91 magenta · #1F80FF blue · #F58220 orange · #4AA147 green · #000000.
  AI Builder UI: white + pale-blue wash (#EEF3FC-ish), action blue #1F80FF, step chips green.

## Product captures (aibuilder.kissflow.com, user's account, 1920×1080, 2026-11-03)
| file | what | status |
|---|---|---|
| screens/c01-landing.png | public hero: "You write the spec. The agents build exactly that." agents→SPECIFICATION card→VERIFIED · ZERO DRIFT; "Runs on the Kissflow platform · Your data stays in your tenant" | SEEN (public) |
| screens/c02-pipeline-full.png | Pipeline page: "Seven agents. Seven gates. Nothing moves on a maybe."; 7 gates; "Built for the controls your auditors already ask about" | page SEEN, contents CLAIM (demo data) |
| screens/c03-memo-workspace.png, c04-versions.png | workspace with **Versions · Latest** dropdown | SEEN |
| screens/c05–c08-chat-*.png | build log: "Reading the BRD…", "Now running the verifier", "IR verifies clean", "Gate passes clean", fixes + re-verify | SEEN |
| screens/c09-bp-BRD-detailed.png, c10-bp-BRD.png | BRD: **Draft — awaiting sign-off · Version 1.0**, Brief / Detailed — for sign-off, ⤓HTML ⎙PDF, stat row 20·8·12·24·8·75·17 | SEEN |
| screens/c11–c18-bp-*.png | Data Model ER, Data & Fields, Business Logic (formulas + "Possibly missing expressions 9"), Workflows (steps + ONLY WHEN conditions), Roles & Permissions matrix, Pages & Nav, Automations (internal·built, rationale traced to BRD rules), Decisions (Your decisions 0 · Decision log 5) | SEEN |
| screens/10-about … 20-09 | earlier 1600×900 set | SEEN |

Privacy: the header shows "Abhiram" + avatar, and Prototype/Preview frames show the generated UI → crop/mask
the user name; Prototype/Preview frames stay out (v3 footage rule). Persona names inside the BRD
(Priya Nandakumar etc.) are fictional and fine.

## Recordings (v7 project, real takes)
- `rec/ai-builder-1.mp4` — home, prompt types, BRD attached, Start building, Express choice.
- `rec/ai-builder-4-blueprint.mp4` — "Your app is ready" → full Blueprint tour → cursor rests on Generate.
- `rec/aib-timelapse-chat.mp4` — time-lapse of the agents' chat build.
- `rec/ai-builder-veyl.mp4` — second app started (university ops).

## Cast / props (v7, used with permission in the earlier film)
- `cast/*.png` — halftone cut-out people: builder, approver, broker, finance (stock-derived, as in v7).
- `props/*.png` — plane, calendar, watch, tube, ring, arrow, icon-{audit,data,perm,proc}.

## Reference
- `ref/v7.mp4`, `ref/v7-sheet.jpg` — previous film: parchment ground, halftone cast, 3D robot, blue side bands.

## Process facts (for the script; user-visible behaviour)
Requirements → architecture → design by parallel specialists → adversarial verifier after every step →
whole-app coherence → decisions logged, plan frozen as v1 → review & sign-off (Blueprint + prototype) →
build only on Generate → Build it, into the Development sandbox, with the user's own permissions →
acceptance tests drive real records through every journey → every build saved as a version; never
auto-publishes to production (promotion is a human/admin step on Kissflow).
Sources: app-builder plugin commands/agents (behaviour only), chat logs above, kissflow.com/llm-info.

## Not available / not used
- Kissflow tenant Deploy wizard + deployment history: not captured (needs Kissflow sign-in; the film
  focuses on the build process, so the production half is told through the Blueprint + "never auto-publish").
- Dev → UAT → Prod: not shown (llm-info: dev + prod only).
- ElevenLabs fresh images: to generate once a direction is chosen.
