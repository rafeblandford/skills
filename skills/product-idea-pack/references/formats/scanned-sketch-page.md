# Format: Proposition sketch

## Use when

The question is whether the proposed change is interesting for someone. Focus on role, value and the human situation before product structure or interface detail. The output should feel like a strong product thinker captured an idea in motion, while the editorial frame keeps it legible and trustworthy.

Do not use it merely to make a finished interface look informal.

## Deliverable character

- one dominant black-fineline drawing on white or near-white paper;
- confident, slightly imperfect observational linework with selective material detail;
- a human situation or recognisable real-world context whenever it carries the proposition;
- pale yellow editorial markers, with an optional second accent reserved for one product state;
- generous negative space;
- important copy supplied as editable overlays, not generated handwriting.

A proposition sketch is not a mechanism board with rougher strokes. Do not satisfy this format with stick figures, an oversized phone outline, generic interface bars and floating callout cards. If the visual could be redrawn more honestly as boxes and arrows, it is probably the wrong sketch or the wrong format.

## Choose the emphasis

Name the intended emphasis before generating the ink layer:

- **Context-led:** use when role, emotion, social acceptability or the lived situation is the learning question. The product response must still be visible rather than implied by the caption.
- **Balanced:** the default. Give the human situation and the distinctive product moment comparable explanatory weight.
- **Product-led:** use when a control, visual mechanism, comparison or information treatment is what makes the proposition distinctive. Make that product fragment the hero and use human context as a smaller entry or outcome.

Do not equate “product-led” with polished UI. The sketch may remain loose while making the intervention specific. A reader should be able to point to what the product does from the sketch field itself, without relying on the editorial rail to invent the missing mechanism.

## Default page scaffold

With `editorial-instrument@2`, start from `../../assets/templates/proposition-sketch-page.svg` unless the brief or chosen composition needs another arrangement. Preserve its main architecture:

- an editorial rail that reads independently;
- a distinct white or near-white sketch field;
- short spatial beat markers above the field;
- a subordinate strip below the field for friction, product answer and changed outcome.

The rail and spatial markers may use different wording, but must describe the same logic without repeating full sentences. Remove a scaffold element when it does not help the chosen pattern; do not leave placeholder furniture.

## Composition patterns

Choose the pattern that best explains the idea:

- **Annotated key moment:** one large interface frame with two or three mechanism → value notes;
- **Three-vignette idea:** need → product response → changed outcome;
- **Before / possibility:** compressed present friction beside a larger proposed state;
- **Exploded interaction:** central user moment with three or four system-behaviour fragments;
- **Idea constellation:** three structurally different manifestations around one proposition.
- **In-world artefact:** a notification, receipt, letter, public notice or other ordinary object from the proposed future becomes the key visual.

Use a constellation only before a direction has been selected. Do not pretend three page layouts are three ideas.

Use an in-world artefact when consequences, norms or acceptability are more important than interface usability. Mark it clearly as speculative and keep fact, extrapolation and invention distinct.

Whichever pattern is used, make the current friction, proposed change and resulting tension legible. Show the product only where it clarifies the proposition; omit navigation, settings and other product furniture that imply decisions have already been made.

For a three-vignette or situated sequence, compose **human situation → decisive product moment → changed outcome**. Give each moment its own negative-space corridor and place arrows in those corridors. Do not run connectors across a face, hand, device or label. One scene or object may be much larger than the others when it is the actual decisive moment, but do not reduce the distinctive product intervention to an incidental prop.

## Layering

Use two independent layers:

1. **Ink layer:** frames, arrows, small interface fragments, recognisable people or objects and no more than two short handwritten labels.
2. **Editorial layer:** status, title, three beats, question, assumptions and decision-bearing labels.

Generate or draw the ink layer as a standalone raster with no title, long annotations, logos, watermarks or pseudo-text. When people, place, physical objects or atmosphere are important, use an available image-generation or genuine drawing capability for the ink layer; a programmatic SVG of stick figures is not an equivalent. If that capability is not present, stop at the direction checkpoint and offer the routes in `tool-portability.md`: the external image workflow via `ink-layer-prompt.md`, a supplied sketch, or an intentionally incomplete ink field. Wait for the choice before composing. If the user accepts the incomplete field, keep the agreed composition and declared emphasis; where the field must be simplified to an object-and-interaction study, say what will change and what it will no longer show before doing it, and disclose the limitation on the artefact and in the report. Compose the page before adding paper texture. The page must still work in monochrome.

## Drawing language

- Black or dark-charcoal fineliner.
- Firmer outer frames, lighter internal detail.
- Slightly uneven corners and occasional doubled construction line.
- Specific folds, hands, objects, surroundings or device details where they make the situation believable.
- Purposeful strokes rather than nervous scribble.
- No sepia nostalgia, notebook props, torn edges, coffee stains or childlike illustration.
- No polished UI rendered in black and white.
- No faux-hand-drawn vector shorthand made only from smooth thick strokes and generic figures.

## Copy

- Headline and three beat headings are typed and editable.
- Embedded ink labels contain one to four words in simple hand printing.
- The question must expose a real uncertainty, not ask whether the viewer likes the idea.
- Label assumptions plainly; sketchiness is not a substitute for conceptual honesty.

## Revision

For image-generation revisions, change one of composition, looseness, accent, density or paper treatment at a time and state what remains fixed. Correct editorial text without regenerating the ink layer.

## Output and QA

Produce:

- editable SVG page;
- presentation PNG;
- independent ink-layer PNG;
- the exact generation prompt when image generation was used, or `ink-layer-prompt.md` when the image is to be made elsewhere.

Reject the result if important copy is flattened into the scan, arrows collide with labels or focal objects, the page feels artificially messy, or the proposition cannot be understood in 15–20 seconds. Also reject it when the hero is merely a large device frame, the human context is generic shorthand, the drawing lacks material specificity, the distinctive product response cannot be identified from the sketch field, or the result could be mistaken for a mechanism board.
