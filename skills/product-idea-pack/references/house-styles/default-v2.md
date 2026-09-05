# House style: Editorial Instrument

**Identifier:** `editorial-instrument@2`  
**Status:** default

Make several ideas feel edited by the same product team without turning them into the same beige card template. Consistency comes from page anatomy, type, spacing and explanatory rhythm. The concept supplies the composition and any product-specific visual language.

## Shared frame

Every principal board or prototype opening state includes:

1. a compact identity block naming the concept, format, draft and discussion status;
2. one clear proposition title;
3. three concise beats describing mechanism and changed outcome;
4. one explicit question to provoke;
5. a subordinate truth, assumption or caveat note.

Let the format name communicate the stage of development. Do not repeat a generic `EARLY PRODUCT IDEA` or `PRODUCT CONCEPT` kicker on every artefact. Prefer a proposition people can debate over a large product-name heading.

The five elements are the pack signature, not a requirement to repeat the same composition. A sketch, mechanism board, storyboard and prototype should remain visibly different formats.

## Identity block

Every principal artefact must carry the same stable working name, format, draft number and discussion status. Prefer a compact two-line block above the proposition:

```text
CONCEPT NAME
FORMAT · DRAFT N · FOR DISCUSSION
```

For example:

```text
REPAIR RELAY
MECHANISM BOARD · DRAFT 1 · FOR DISCUSSION
```

A single line is acceptable when it fits comfortably, but do not allow automatic wrapping to create an accidental hierarchy. Place the identity block above the proposition in a static editorial rail and in the compact editorial header of an HTML overview. Keep it subordinate: the working name identifies the pack while the proposition remains the headline. If no name was supplied, choose a neutral working name, mark it as proposed in the decision record and reuse it across the pack.

Do not insert editorial metadata inside a product-only native capture. Identify that image through its filename and the labelled contact sheet or overview instead.

## Canvas and layout

- Default static canvas: 16:9, either 1672 × 941 or 1920 × 1080.
- Use outer margins of approximately 3–4% of canvas width.
- Static boards normally reserve 22–27% for an editorial rail and 65–72% for the visual proposition.
- Separate the neutral outer page from the working visual field. For sketches, use a white or near-white inset field; do not wash the entire page and every internal surface with the same cream tint.
- One visual idea must dominate. Supporting labels should frame it from clear lanes above, below or beside it rather than float arbitrarily over it.
- Vary the internal geometry to suit the idea. Do not default to three equal rounded cards merely because there are three editorial beats.
- Interactive prototypes are not constrained to 16:9. Keep the editorial opening compact and let the product surface dominate. Capture the product independently when a deck overview would distort its geometry.

For default static work, use `assets/templates/editorial-board.svg` as a token and grid reference. Proposition sketches have their own stronger scaffold at `assets/templates/proposition-sketch-page.svg`. Adapt the working field; do not turn either template into compulsory product geometry.

## Default palette and material

Use these tokens, or perceptually close equivalents, when no brand or host surface supplies a palette:

| Role | Default |
| --- | --- |
| Outer paper | neutral off-white `#F7F6F1` |
| Working field | white / warm white `#FFFEFA` |
| Primary ink | charcoal `#222321` |
| Muted copy | neutral grey `#6D6B65` |
| Rules | soft grey `#D8D6CF` |
| Editorial marker | pale yellow `#F2DC72` |

Yellow is the default editorial highlighter: small beat labels, numbered markers or a single decisive annotation. It is not a large panel colour.

A second product accent is optional. Derive it from a supplied host or use it for one semantic role such as **live**, **changed**, **uncertain** or **selected**. Muted coral may still express a live or uncertain state, but it is not the house colour. Never spread it across generic numerals, bullets, card borders, progress bars and callouts at the same time.

Keep colour sparse enough that the pack works in greyscale. Avoid gradients, glows and decorative tinted panels in the editorial frame. Use a shadow only to explain real elevation, such as a paper sheet or device—not to make every card feel polished.

## Editorial rail

Use this reading order:

1. concept name;
2. `FORMAT · DRAFT N · FOR DISCUSSION`;
3. proposition title;
4. three parallel mechanism → value beats;
5. dotted or hairline divider;
6. `QUESTION TO PROVOKE`;
7. `IMPORTANT ASSUMPTION`, `PRODUCT TRUTH` or `NOTES` at the bottom.

Keep each beat heading to one line and its explanation to one or two short lines. The rail must read cleanly without the central visual. Spatial labels around the hero may restate the sequence in shorter, situational language; do not duplicate paragraphs.

## Typography

- Use a neutral grotesk such as Arial, Inter, Aptos or Helvetica Neue.
- Identity block: concept name at 11–14 pt semibold or bold; metadata at 10–12 pt muted, both with restrained uppercase tracking.
- Static-board title: 32–42 pt; two to four deliberate lines.
- Section labels: 11–14 pt uppercase with restrained tracking.
- Explanatory copy: 15–19 pt.
- Use two weights where possible: regular and semibold or bold.
- Important copy stays typed and editable. Do not imitate handwriting with a display font.
- Avoid oversized titles that push the working surface below the fold or reduce the idea to a poster slogan.

## Connectors and annotations

- Give each important connector a dedicated lane and stop arrows before labels, hands, faces, devices and other focal objects.
- Prefer one continuous reading direction. Use bends only to reveal branching or hand-off.
- Use solid lines for proposed causal or navigational paths and dotted lines for unresolved, optional or source relationships.
- Keep callout boxes exceptional. Prefer a short label aligned to the visual architecture over a floating rounded card with a long leader line.
- A weak link may use a dashed boundary or product accent, but must also be labelled in words.

## Product truth

Distinguish:

- **Known:** supplied facts, constraints or evidence;
- **Proposed:** the interaction or behaviour being explored;
- **Assumed:** invented detail required to make the idea tangible;
- **To learn:** the uncertainty the artefact is designed to expose.

Never use polished presentation to conceal a weak inference. Show uncertainty where it occurs. When a material product mechanism or the decisive interaction was inferred rather than supplied by the user, identify it unobtrusively as **Proposed** on the artefact itself—a short label in the truth note or beside the element—not only in the conversation. Do not label trivial layout or interface detail this way.

## Pack consistency

Keep the status, proposition, three-beat rhythm, question and truth ordering stable. Also keep accepted interaction names and the semantic meaning of any product accent. Let each format express those decisions through its own geometry; cross-format consistency is not visual cloning.

## Reject or revise when

- the proposition cannot be stated after 15 seconds;
- the page is recognisable mainly as cream background plus coral cards rather than by the idea it contains;
- a sketch, board and storyboard could be mistaken for the same template with different copy;
- three equal panels appear without a comparison or sequence that requires them;
- the wrapper is louder or larger than a native product surface;
- annotations overlap connectors or focal imagery;
- the question is generic, assumptions are hidden or the board reads as finished design.

## Versioning

Version 2 deliberately replaces the broad warm-off-white and optional-coral guidance in version 1 with a neutral paper/white-field hierarchy, yellow-first editorial markers and an explicit accent budget. Keep `editorial-instrument@1` for historical packs; do not relabel them as version 2.
