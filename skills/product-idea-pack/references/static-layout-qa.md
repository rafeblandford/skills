# Static layout QA

Apply this final pass to every proposition sketch, mechanism board and product storyboard. It catches production defects after the idea, copy and composition are already settled; it must not become a reason to redesign an accepted direction.

## Run it at the right time

1. Settle the final copy and line breaks.
2. Route connectors and apply clipping or masks.
3. Render the editable source with the same fonts and dimensions as the presentation PNG.
4. Inspect the export, correct local defects and render again.

Do not claim a static board passed because its source parses, its conceptual rubric scores well or an earlier export looked correct. The final rendered pixels are the test.

## Boundary pass

Check every text block, image and product surface against its intended zone:

- no glyph, stroke or fill crosses the canvas safe area, editorial-rail divider, working-field edge, card boundary or device bezel unless the composition deliberately shows an overflow;
- the identity block is present, uses the same working name across formats, includes format, draft and `FOR DISCUSSION`, and remains subordinate to the proposition;
- at 1672 × 941, leave approximately 16–24 px of visible clearance between a headline and the editorial-rail divider;
- when a headline is too wide, change line breaks first, tighten copy second and reduce type only within the house-style range;
- include the full last line, descenders and font fallback when judging fit;
- clip screen contents to the inner display shape and keep the complete device outline visible;
- treat an apparently missing border segment as a defect unless an open shape is intentional and visually unambiguous.

## Collision pass

Inspect connectors only after final text placement:

- no connector or arrowhead may cross readable copy, even when the text remains technically legible;
- preserve a small clear halo around labels—roughly half a line height is usually enough;
- stop leaders before the label or focal object they identify;
- keep arrowheads visually distinct from borders, rules, curves and text strokes;
- make the start, direction and destination of every important connection obvious at presentation size;
- if a collision appears, reroute or shorten the connector before moving accepted content.

Intentional underlines, brackets and graph axes are exceptions, but they must read as part of the labelled element rather than as an accidental crossing.

## Breathing-room pass

Passing a boundary check does not by itself make a composition comfortable. Inspect the complete artefact at normal presentation size and preserve a visibly quiet internal perimeter around the working field, especially beside outermost labels, arrowheads and device frames.

- Treat the safe area as a rejection boundary, not as extra layout space to consume.
- If the composition feels pinned to an edge, first reduce the hero slightly, shorten or reroute an annotation, or remove secondary detail.
- Do not solve a collision in one area by pushing several other elements against the field perimeter.
- A deliberately cropped or full-bleed image may reach an edge; explanatory text, connectors and complete product frames normally should not.

## Two-scale inspection

Inspect both:

- the complete board at normal presentation size, for hierarchy, reading order and connector meaning; and
- the rail, device edges, dense copy clusters and connector endpoints at 100–200%, for overflow, clipping and collisions.

When browser or vector tooling exposes element bounds, use it to check text against named layout zones and connector lanes. Automated bounds are supporting evidence, not a substitute for inspecting the rendered PNG.

## Renderer compatibility

Editable SVG must survive the renderers it will meet. Avoid the three-argument `rotate(angle cx cy)` transform, which some renderers silently drop; use `translate(cx cy) rotate(angle) translate(-cx -cy)` or position the group and rotate about its origin. Prefer plain paths, explicit fills and strokes, and common fonts with fallbacks. When a presentation profile is produced, inspect the artefact through the presentation renderer as well, since its text metrics can expose collisions the SVG renderer hides.

## Record and recheck

Record any visible corrections in the evaluation. After every correction, render and inspect the affected region again. Exclude temporary QA overlays or diagnostic crops from the share archive.

Give capture and render tools an absolute destination inside the concept folder when the tool supports it; some tools resolve a relative filename from the browser or session launch directory rather than the shell's current directory. Verify the actual output location after every capture. Keep rejected or intermediate renders in a task-specific temporary or `qa/` location rather than beside share files. Before delivery, scan the concept folder's parent for loose output-like files and remove or relocate only intermediates created by the current task.

Reject delivery while any headline enters another layout zone, product content overlaps its frame, border looks accidentally incomplete, or connector crosses copy.

## Independent review for consequential delivery

For a public example, release candidate, multi-format pack or destination handoff, use a fresh visual-review context when an independent reviewer capability is available. Give it the final rendered artefact, intended-use size and this acceptance checklist; ask for concrete production defects, not a new aesthetic direction. The creating agent remains responsible for checking and correcting the source.

Do not require an independent reviewer for an ordinary Draft 1, and do not block delivery merely because the current harness lacks one. Human review remains the strongest destination check when the artefact will be edited in a specific application.
