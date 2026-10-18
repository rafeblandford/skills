# Pack output contract

Use this contract when creating two or more formats, a share pack, or a concept intended for later iteration. The folder structure and naming rules also apply to a single-format delivery: every generated file lives inside `concept-slug/`, never loose in the working directory.

## Folder structure

```text
concept-slug/
├── brief.yaml
├── decisions.md
├── evidence.md                 # optional portable supporting record
├── evidence.html               # optional browseable rendering; use only when useful
├── 01-proposition-sketch/
│   ├── page.png
│   ├── editable.svg
│   ├── ink-layer.png          # scanned treatment only
│   └── ink-layer-prompt.md    # only when the ink layer is made elsewhere
├── 02-mechanism-board/
│   ├── board.png
│   └── editable.svg
├── 03-product-storyboard/
│   ├── storyboard.png
│   └── editable.svg
├── 04-interactive-prototype/
│   ├── prototype.html
│   ├── screen-01.png
│   ├── screen-02.png          # one per principal or sampled state
│   └── overview.png           # optional 16:9 deck capture
├── presentation/              # optional output profile
│   ├── concept-pack.pptx
│   └── concept-pack.pdf
├── design-handoff/            # optional output profile
│   ├── 01-format-name.svg
│   ├── 01-format-name.png
│   ├── assets/
│   └── handoff.md
├── contact-sheet.png          # useful when two or more formats exist
└── share-pack.zip             # useful when several files will be sent
```

Include only formats actually requested or recommended. Do not create empty directories.

Likewise, create `presentation/` or `design-handoff/` only after the user requests or accepts that supplementary output profile. Adding an output profile packages the current artefact; it does not create another format or increment the draft.

The evidence record is supporting documentation, not a fifth visual output. Include it only when consequential claims, source roles or uncertainty need a durable record. Markdown is the portable default; HTML or a printable document may be primary when the intended use warrants it. Do not create both Markdown and HTML unless they can remain one coherent record.

Evidence records are not bound to 16:9. Let them extend vertically. If a presentation preview is useful, label it as an overview or extract and never crop rows while implying completeness.

## Naming

- Use lowercase ASCII kebab-case.
- Prefix ordered screens with two digits.
- Keep the concept slug stable through revisions.
- When the draft number increases, keep every accepted earlier draft's editable source and PNG under its own name (`editable.svg` and `page.png` stay Draft 1; Draft 2 is `editable-draft-2.svg` and `page-draft-2.png`). Update a draft in place only when its number does not change. Never overwrite Draft 1 and label the result Draft 2.
- Put the stable identity block—concept name plus `FORMAT · DRAFT N · FOR DISCUSSION`—on every principal static artefact and HTML overview. Keep product-only native captures free of editorial metadata and identify them on the contact sheet.

## Format deliverables

### Proposition sketch

- presentation PNG;
- editable SVG containing proposition and annotation overlays;
- independent ink layer;
- generation prompt when an image model was used, or `ink-layer-prompt.md` when the image is to be produced elsewhere.

### Mechanism board

- editable SVG;
- presentation PNG.

### Product storyboard

- editable SVG;
- presentation PNG;
- illustrative assets only when used.

### Interactive prototype

- standalone HTML with no build step;
- one PNG per principal or deliberately sampled state at the product's canonical viewport or from a bounded product surface;
- optional 16:9 overview PNG for presentation use;
- a zip containing the HTML and state PNGs when sharing is likely.

## Manifest

The saved `brief.yaml` is the pack manifest. In addition to the common brief, record:

```yaml
pack:
  status: draft
  house_style: editorial-instrument@2
  purpose: cross-format-translation | multi-deliverable
  primary_format: interactive-prototype
  formats: []
  current_revision: 1
  private_test_material_included: false

delivery:
  core: true
  output_profiles: []
  powerpoint_mode: placed-vector
  design_target: figma

brand_profile:
  id: "none"
  apply_to: []
```

The private-material flag must be `false` for anything described as shareable.

`primary_format` identifies the stable artefact on which feedback and revisions operate. If a deliberate cross-format comparison has no primary artefact, record `primary_format: none` and select a revision target with the human before changing any output. Moving the idea into another format is a translation and must not be numbered as the next revision of the original artefact.

## Maintained-example provenance

When an example is intended to demonstrate reproducible one-shot or iterated output, keep the original prompt in `input.md` and add:

```yaml
example_run:
  mode: one-shot | iterated
  source_prompt: input.md
  human_feedback_rounds: 0
  agent_qa: "Short factual record of autonomous checks or visible corrections."
```

`one-shot` means zero human feedback rounds after the saved prompt. It does not mean skipping visual, interaction or export QA. Record visible autonomous corrections in `evaluation.md`; if critique changes the proposition, mechanism or composition, change the mode to `iterated`.

## Shareability

- A standalone interactive prototype should work by opening the HTML file in a modern browser.
- Avoid network dependencies unless the interaction genuinely requires them. If used, state them plainly.
- Do not include current work, client material or private test fixtures in example packs.
- Use neutral placeholder evidence rather than fabricated personal or commercial data.

## Verification

Before delivery:

- render static editable sources and inspect their PNGs;
- apply the shared static-layout QA after final copy reflow, checking boundaries and connector-versus-copy collisions at presentation size and 100–200%;
- check static boards and optional overview captures at 16:9 presentation size;
- check prototype state captures at their recorded product viewport rather than expecting 16:9;
- test all prototype controls and state transitions;
- test the prototype at desktop and narrow widths;
- confirm that the share archive contains only intended files;
- for a presentation profile, confirm any raster fallback beside the placed SVG is a genuine PNG and inspect the rendered slides;
- run `scripts/check_pack.py` from this skill's folder for a reusable pack. It treats supporting assets (ink layers, `assets/`, `references/`, handoff assets) as free-ratio and checks only composition pages against 16:9.
