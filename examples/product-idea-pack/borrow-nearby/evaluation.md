# Draft 1 evaluation

## Run provenance

| Field | Recorded value |
| --- | --- |
| Harness | Codex desktop, local workspace |
| Model | GPT-6 Astra (`gpt-6-astra`) |
| Date | 5 September 2026 (`2026-09-05`), Europe/London |
| Requested source revision | `d2fab94` |
| Full source revision | `d2fab9408aeb51970a00abf774489bf6750604b9` |
| Skill used | Product Idea Pack at the verified source revision |
| Source verification | All 30 tracked Product Idea Pack package files compared byte-for-byte with that revision; zero mismatches |
| House style | `editorial-instrument@2` |
| Formats | Proposition sketch, editorial mode; mechanism board, workshop mode |
| Status | Draft 1 · For discussion |
| Run mode | One-shot; zero human feedback rounds; autonomous production QA correction recorded below |
| Primary feedback target | Mechanism board |
| Image generation | Built-in Image Generation tool; one generation, no input image, no image-edit call. Underlying image model identifier was not exposed. Exact prompt saved with the ink layer. |
| Rendering | Installed `scripts/render_svg.cjs`, using the available bundled Node.js and Sharp runtime |
| Commit | No generated files staged or committed |

The destination did not exist before this run. No prior Borrow Nearby output, brief, evaluation or rerun directory was inspected or reused. No visual reference, web research, functional precedent or existing concept example was used. Content was developed from the saved request and the installed skill's general references. Repository maintenance instructions and Image Generation/tool instructions were followed for execution only.

## Result against the request

| Requirement | Evidence in the delivered artefact | Result |
| --- | --- | --- |
| Human hand-off | One dominant, specific doorway scene showing two neighbours sharing the weight of a drill case | Present |
| Distinctive product intervention | Editable shared plan in the sketch field shows both-agreed collection and return, continuing visibility and owner-confirmed closure | Present |
| Complete borrowing loop | Board links need and time → voluntary offer → joint plan → collection → return → owner confirms safely back | Present |
| Weak links | Unmet request, changed return commitment and unresolved late/damaged/disputed return are separate editable clusters | Present |
| Workshop editability | Mechanism SVG contains 26 named groups, editable text and independent vector connector groups; zero raster elements | Present; native destination editor not exercised |
| Consistency without copying geometry | Same working name, proposition, three beats, question, truth note, typography and sparse yellow emphasis; observational sketch versus service hand-off map | Present |
| Trust question stays open | Exact central question on both artefacts; sketch asks about obligation, board invites comparison with a private reminder and spoken promise | Present; no behavioural conclusion claimed |
| Neutrality | No prices, marketplace inventory, booking flow, ratings, identity badge, payment, insurance or liability solution | Present |
| Core delivery only | Two sources and presentation PNGs, independent ink layer and prompt, contact sheet and run records | Present |

## Visual and layout QA

Both principal SVGs were rendered to **1920 × 1080** PNGs. The creating agent inspected the full renders and detailed regions at 200%. The contact sheet was also rendered and inspected at 1920 × 1080. Final checks covered identity hierarchy, the editorial divider, working-field perimeters, complete product-plan borders, label breathing room and connector endpoints.

**Visible autonomous correction:** the first sketch export placed the illustration too close to its scene note. The embedded ink layer was reduced from **847 × 565 at (542, 278)** to **810 × 540 at (552, 285)**. The final ink rectangle ends at y=825, leaving approximately **19 px** before the note's upper glyph edge. The illustration itself, proposition, copy and two-part composition were preserved. The page was rendered again and the affected strip re-inspected. This was a local spacing correction within Draft 1, not a human-directed concept iteration.

A fresh visual-review agent independently inspected only the two newly created PNGs and the general static-layout QA reference. It checked the full frames and dense details at 200%, confirmed the same initial scene-note defect, then rechecked the corrected final sketch. Its final assessment found **no visible overflow, clipping, connector/copy collision, ambiguous destination or inadequate perimeter clearance**. It confirmed the physical hand-off, visible return plan, voluntary owner agency, joint agreement and unresolved exceptions.

Supporting deterministic checks parsed both SVGs and measured text using the actual Arial and Arial Bold font files. They checked 61 sketch text lines and 75 mechanism-board text lines against the canvas safe area, rail divider and applicable frames, plus a 7 px halo between connector paths and text bounds. There were **zero reported problems**. All group IDs are unique. The sketch has **25 named groups and one embedded PNG**; the mechanism board has **26 named groups and zero images**. The sketch's image dependency is self-contained, and all decision-bearing copy in both sources remains SVG text.

These font-metric checks support the inspected pixels; they do not replace visual review or prove identical layout in every editor. Headless Chromium could not launch in the sandbox; the browser tool blocked direct file URLs, and a local preview server could not bind its port. No wider permissions were requested. Existing Sharp rendering, font-based bounds and the independent rendered-image review provided the observable static QA outcomes.

The installed pack checker passed with **zero errors and one warning**:

```text
WARNING: non-16:9 presentation PNG 01-proposition-sketch/ink-layer.png: 1536x1024
Pack check passed with 1 warning(s).
```

This warning concerns the independent 3:2 illustration asset, not a presentation page. Both requested presentation PNGs and the contact sheet are 16:9 at 1920 × 1080. Keeping the ink image at its original dimensions avoids altering its generated pixels.

Temporary bounds diagnostics, crops and construction helpers are outside the run folder. No diagnostic artefacts, optional presentation pack, archive or design handoff are included.

## Findings and limits

The pair of outputs gives a discussion a concrete target: the proposed shared plan records an expectation and keeps the loan open, but does not establish that the item will be returned or that trust improves. Owner-confirmed closure is a proposal with its own burden; forgetting to confirm could leave a safely returned item apparently outstanding.

The sketch's entire ink scene is a generated raster. Its copy, plan and page geometry are editable vectors, while changing the people or object requires editing or regenerating that ink layer. The mechanism board is fully vector-editable, with separate connectors that must be rerouted manually when clusters are moved. An SVG-capable destination editor was not opened, so destination-specific import and text layout remain unverified.

The most consequential assumptions are direct collection between neighbours, a plan visible only to the pair, explicit agreement to changed returns and an owner willing to confirm closure. Illustrative days, times and the drill are invented examples. No demand study, neighbour interviews, live loan, enforcement model or legal/financial solution was tested.

Recommended next learning step: use the editable board to rehearse a normal loan, a late return and a forgotten closure with prospective borrowers and owners. Compare the shared plan with a private reminder and a spoken promise. If the language and tone become the remaining question, translate the accepted mechanism into a situated product storyboard. Keep both current outputs at Draft 1 until human feedback chooses a revision.
