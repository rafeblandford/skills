# Output profiles

Output profiles package an accepted concept artefact for a destination. They do not change its proposition, format, presentation mode, house style, brand profile or draft number. Branding remains an independent opt-in overlay.

## Core

Core is always produced:

- editable SVG or standalone HTML;
- presentation PNG;
- independent raster assets and generation prompt when used;
- brief and decision record for a reusable pack.

Do not make supplementary files merely because a capability is available.

## Presentation

Use when the artefact will be presented, circulated as slides or assembled with other concepts.

Produce:

- `presentation/concept-pack.pptx`;
- `presentation/concept-pack.pdf` rendered from the same slide sequence.

The default PowerPoint treatment is a **placed-vector deck**: place each final 16:9 SVG on a matching 16:9 slide without an additional decorative wrapper. This preserves the approved composition and remains sharp when scaled. Do not rebuild every element as native Office objects unless the user explicitly asks for a fully native-editable PowerPoint version.

For a single-format concept, one slide is sufficient; do not add a ceremonial cover. For a multi-format pack, use a compact overview only when it helps orientation, followed by one slide per principal artefact. Represent an interactive prototype with its overview and principal state captures rather than implying that the PowerPoint itself tests the interaction.

Verify the PPTX by rendering every slide through the presentation renderer that is present and comparing it with the approved PNG; its text metrics can differ from the SVG renderer's, so inspect the rendered slide, not only the source. Verify that any raster fallback stored beside the placed SVG is a genuine PNG of the approved artefact (some libraries write the SVG bytes under a `.png` name, which breaks viewers that use the fallback). Verify that the PDF has the same page count, order and visible content. If SVG placement is unsupported in the available environment, use the presentation PNG and disclose the loss of vector scaling.

## Design handoff

Use when someone will continue the work in Figma or another vector-design tool.

Produce one `design-handoff/` folder containing:

- a self-contained Figma-safe SVG for each principal static artefact;
- a reference PNG beside each SVG;
- original raster layers or illustrative assets in `design-handoff/assets/`;
- `design-handoff/handoff.md` recording fonts, colour tokens, canvas dimensions, embedded assets and any known import compromises.

Prepare the handoff SVG for transfer rather than merely renaming the core file:

- preserve useful, human-readable group IDs;
- keep decision-bearing copy as SVG text and use common or supplied fonts with explicit fallbacks;
- give text over raster artwork an explicit opaque fill, keep it outside inherited opacity, blend-mode and mask groups, and place it above the raster in document order;
- embed every visible raster dependency while also supplying its original file separately;
- replace SVG `marker` arrowheads and patterns with ordinary paths or shapes;
- use explicit fills and strokes and avoid unnecessary filters, external URLs or script dependencies;
- retain the exact canvas dimensions and `viewBox`;
- render the handoff SVG and compare it with the reference PNG after normalisation.

When the destination application is available, import the handoff SVG and inspect the actual imported result at normal size and 100–200%. Confirm text contrast and stacking, arrowheads, embedded raster layers, canvas geometry and grouping rather than relying only on a browser render. Text remaining editable but being split into separate line objects is an acceptable import compromise when appearance and reading order are preserved; record it in `handoff.md`. Missing, obscured or materially restyled text is a defect.

Do not create a proprietary `.fig` file unless an authorised Figma capability is available and the user specifically requests it. A portable SVG remains the source handoff.

## Both

Produce both folders and include them in the explicit allow-list for the share archive. Do not duplicate core files outside the destination folders unless the receiving tool requires it.

## Selection and manifest

If the destination already makes the choice clear, infer the profile and proceed. Otherwise create the core output first and offer the optional profiles once at delivery.

Record selected profiles in `brief.yaml`:

```yaml
delivery:
  core: true
  output_profiles:
    - presentation
    - design-handoff
  powerpoint_mode: placed-vector
  design_target: figma
```

An empty `output_profiles` list means the user kept the core files only.
