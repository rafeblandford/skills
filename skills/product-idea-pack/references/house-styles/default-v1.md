# House style: Editorial Instrument

**Identifier:** `editorial-instrument@1`  
**Status:** default

This house style makes multiple ideas look related without forcing them into the same composition. Consistency comes from the editorial frame, hierarchy and explanatory rhythm more than colour.

## Shared frame

Every principal board or prototype opening state includes:

1. a small status label;
2. one clear title;
3. three beats describing the idea or sequence;
4. one explicit question to provoke;
5. a bottom note distinguishing truth, assumption or the most important caveat.

Use `EARLY PRODUCT IDEA — FOR DISCUSSION` for proposition sketches and mechanism boards, and `PRODUCT CONCEPT — FOR DISCUSSION` for product storyboards and interactive prototypes.

## Canvas and layout

- Default static canvas: 16:9, either 1672 × 941 or 1920 × 1080.
- Use generous outer margins: approximately 3–4% of canvas width.
- Static boards reserve 22–27% for the editorial rail and 65–72% for the visual proposition.
- Interactive prototypes are not constrained to 16:9. Use a responsive editorial wrapper with a compact header, three-beat explanatory strip, product surface, question and truth note; allow that wrapper to scroll when necessary. Render the product surface at geometry appropriate to its actual context and capture it independently when a deck-shaped overview would compromise fidelity. The three beats belong to the editorial frame; they do not prescribe the prototype's screens, states or navigation.
- Leave meaningful whitespace between idea clusters. Density should be deliberate, not evenly distributed.
- One visual idea must dominate. Supporting fragments explain it; they do not compete with it.

## Editorial rail

Use this order:

1. status label;
2. title or `What if…?` proposition;
3. three short mechanism → value beats;
4. dotted or hairline divider;
5. `QUESTION TO PROVOKE`;
6. `IMPORTANT ASSUMPTION`, `PRODUCT TRUTH` or `NOTES` at the bottom.

Keep the three beats grammatically parallel. Each heading should fit on one line where possible; each explanation should fit in one or two short lines.

## Typography

- Use a neutral grotesk such as Arial, Inter, Aptos or Helvetica Neue.
- Static-board title: 32–42 pt; two to four short lines.
- Section labels: 11–14 pt uppercase with restrained tracking.
- Explanatory copy: 15–19 pt.
- Interface copy must remain readable when the complete board is shown in a presentation.
- Use two weights where possible: regular and semibold/bold.
- Avoid cursive, novelty type and generated pseudo-handwriting for important copy.

## Colour and material

- Default canvas: warm off-white; primary ink: charcoal or near-black.
- Use one restrained accent to indicate the decisive interaction, selected state or weak link.
- Pale yellow is suitable for editorial highlighting; muted coral is suitable for active or uncertain product states.
- Colour is supportive. The hierarchy and pack relationship must survive in greyscale.
- Scanned paper texture may add tooth, but it must not reduce contrast or become nostalgic decoration.

## Connectors

- Give each important connector a dedicated lane.
- Stop arrows before labels, cards and icons; never run a line through copy.
- Prefer one continuous reading direction. Use bends only to reveal branching or hand-off.
- Use solid lines for proposed causal or navigational paths and dotted lines for unresolved, optional or source relationships.
- A weak link may use the accent and a dashed boundary, but must also be labelled in words.

## Product truth

Distinguish:

- **Known:** supplied facts, constraints or evidence;
- **Proposed:** the interaction or behaviour being explored;
- **Assumed:** invented detail required to make the idea tangible;
- **To learn:** the uncertainty the artefact is designed to expose.

Never use polished presentation to conceal a weak inference. Show the uncertainty where it occurs.

## Pack consistency

- Keep status labels, title placement, three-beat rhythm, question placement and truth-note ordering stable.
- Keep the same concept name and proposition across formats unless a revision explicitly changes them.
- Carry the same accent meaning across the pack.
- Preserve accepted names for interactions and entities.
- Use format-specific composition inside the shared frame; do not force every idea into identical card geometry.

## Quality threshold

Reject or revise a board when:

- the proposition cannot be stated after 15 seconds;
- the three beats describe features instead of a mechanism and changed outcome;
- annotations overlap connectors;
- the question is generic rather than exposing a real choice;
- assumptions are hidden;
- the board reads as a finished design rather than a discussion object.

## Versioning

Do not edit an established house-style version when the change would materially alter existing pack appearance. Create `default-v2.md` or a named variant and update the identifier. Small corrections that do not change the visual contract may remain within the current version.
