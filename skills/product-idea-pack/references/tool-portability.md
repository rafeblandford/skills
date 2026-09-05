# Tool portability

Choose tools by capability and verifiable result rather than by provider name.

## Check what is present

Before committing to a format's outputs, establish which of these is available: a native capability of the harness for the operation (image generation, browser control, rendering, presentation or design-tool access); the bundled helper's runtime and dependencies; an equivalent tool already present that preserves the output contract. Record the choice in the decision log. Do not treat a capability as present because it was present in an earlier session.

## Preferred order

1. Use an available native capability that can create the required editable source or verified export.
2. Use the bundled deterministic helper when its runtime and dependencies are already present.
3. Use an equivalent renderer, browser or presentation tool that is already present when it preserves the output contract.
4. Otherwise deliver the editable source, state plainly which export is missing and give the shortest reproducible next step.

Never install packages, enable connectors or broaden filesystem access automatically.

Distinguish two kinds of missing capability:

- A **defining capability** is one the selected format depends on to answer its learning question, such as image generation for a scanned proposition sketch. When it is absent, stop before composing the artefact: explain the limitation, offer the available routes (authorise or connect a capability, follow the external workflow below, supply existing material, or accept a disclosed gap) and wait for the user's choice. Do not compose first and ask afterwards.
- A **convenience export** is a rendering, capture or packaging step that does not change the artefact's meaning, such as state PNGs or a presentation profile. When it is unavailable, do not stop: ask once whether to authorise it if it is essential to what the user asked for, otherwise proceed with the fallback and disclose the missing export.

Whichever route is taken, preserve the agreed concept and the declared visual emphasis. State any compositional change before making it; a fallback must not quietly turn a multi-scene story into a different object study.

## Capability contracts

### SVG to PNG

Produce the requested dimensions, preserve type and line weight, and inspect the PNG at presentation size. `scripts/render_svg.cjs` in this skill's folder is an optional implementation and requires Node.js with Sharp already present.

### HTML state export

Open the standalone file in a modern browser, use the product viewport recorded in the decision log, activate each principal state and capture either the bounded product surface or the natural page. Do not impose 16:9 unless making a separate presentation overview. `scripts/export_html_states.cjs` in this skill's folder is an optional implementation and requires Node.js with Playwright and a compatible browser already present. If no browser capture capability is present, still open and exercise the prototype where the harness allows; then deliver the HTML, list the principal states and how to reach them, and state that the PNG captures are outstanding. Do not fake a capture or distort the prototype to suit a helper.

### Scanned image generation

Preserve editable decision-bearing copy outside the raster layer. Use whichever image-generation or image-editing capability is present, including an authorised connector, keeping the same prompt intent, reference images and visual verification.

Image generation is a defining capability for a scanned proposition sketch. If none is present, say so at the direction checkpoint, stop before composing the page, and offer these routes:

1. **External image workflow.** Write a self-contained `ink-layer-prompt.md` in the concept folder: the generation prompt, the drawing language, the declared emphasis that must be preserved, what the image must show and must not contain (no title, no long text, no logos, no pseudo-text) and the target size. Carry through the selected format's raster-text limit: for a proposition sketch, prefer no raster lettering and never request more than two short handwritten labels. Before delivering the prompt, count every requested literal label, including separate button or status labels, and reconcile the list with any stated maximum. Ask the user to generate or draw the image elsewhere and supply it; resume composition when it arrives.
2. **Supply an existing sketch** — a hand-drawn or photographed drawing to place in the ink field.
3. **Accept an intentionally incomplete ink field**, marked outstanding on the page, keeping the agreed composition and emphasis; any simplification of the field is stated before it is made.

Wait for the choice. Never substitute a programmatic drawing for the ink layer, and never present a vector object study as a scan.

### Presentation profile

Use an available presentation capability to place each approved SVG on a matching 16:9 slide, render every slide for comparison and export the same sequence to PDF. The observable contract is a faithful placed-vector deck and matching PDF, not a particular library. SVG remains the preferred placed source; use a PNG-only slide when SVG placement is unavailable and disclose it. Verify that any raster fallback stored beside the placed SVG is a genuine PNG of the approved artefact rather than SVG bytes under a `.png` name, and inspect the rendered slides through the presentation renderer that is present, because its text metrics can differ from the SVG renderer's.

### Design-handoff profile

Normalise the SVG for cross-tool import: self-contained assets, explicit paths for arrowheads, no patterns or external dependencies, useful group IDs and a matching reference PNG. When an authorised design-tool capability is available, import and inspect the result. Otherwise verify the normalised SVG by parsing and rendering it, and disclose that native-tool import was not exercised.

### Packaging and validation

Prefer the bundled Python standard-library helpers. Use explicit file lists for public archives and verify that no private or client material is included.
