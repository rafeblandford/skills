# Tide Window — Draft 2 evaluation

## Run provenance

| Field | Value |
| --- | --- |
| Product Idea Pack source revision | `007ade1` |
| Harness | Codex desktop |
| Run mode | Iterated |
| Human-feedback rounds | `1` |
| Draft | Draft 2 |
| House style | `editorial-instrument@2` |
| Primary format | None — deliberate cross-format comparison |
| Private test material | None |

Accepted `codex-007ade1-draft-1` was the sole revision baseline. The original brief remains in `input.md`; no other Tide Window runs or historical material were inspected. No web evidence was required because every tide value is explicitly illustrative.

## What the pack tests

The pack asks whether one proposition survives four different levels of commitment: a situated value sketch, an editable mechanism, a believable product experience and an operated state change. Across every format, the information grammar remains height → direction → curve position → next turn → future day.

The curve remains intentionally visible. Its value or excess density should be judged rather than hidden behind a disclosure.

## Accepted Draft 1 autonomous corrections

The accepted Draft 1 record contained these autonomous presentation corrections before human review:

- Reflowed the shared proposition title to four lines so it remained inside the editorial rail on all three static boards.
- Shortened one mechanism-board support line that exceeded its glance-cue boundary.
- Removed a storyboard transition annotation that collided with the future-day surface; the dedicated arrow lane remains.
- Moved the future-day direction into a compact pill and lowered the large curve so label and line no longer collided.
- Repositioned the desktop-translation label above its surface.
- Reordered the storyboard question copy to the top editable layer after the first export suppressed it visually.

## Draft 2 human-led corrections

One human-feedback round selected the mechanism board and product storyboard as the only revision targets. The proposition, composition, copy, hierarchy, colours and interaction remain accepted and unchanged.

- Product storyboard: clipped all screen contents to the existing rounded inner-phone boundary. This removes the square wallpaper overlap at the bottom edge without moving the phone or its contents.
- Mechanism board: restored the missing right-hand boundary of the `Local tide series` box at `x=720`; the derive connector still begins at `x=724`, preserving a 4 px clear lane.
- Product storyboard: removed the Tomorrow current-height value, rising/falling state and position marker. The selected future day retains its curve, two turning points, next turning point and scope caveat.
- The scanned sketch, standalone HTML prototype and all three prototype state captures were preserved byte-for-byte as explicitly requested.

## Static visual and export QA

- Parsed the two affected editable SVG sources successfully with `xmllint`.
- Re-exported only the mechanism board and product storyboard at `1672 × 941` (16:9), then re-rendered `contact-sheet.png`.
- Inspected both revised presentation PNGs at original size and together on the Draft 2 contact sheet.
- Proposition sketch: the generated ink layer is independent; all decision-bearing copy remains typed and editable; the phone is subordinate to a materially specific packing-to-beach situation; no title, logo, watermark or long pseudo-text is flattened into the ink.
- Mechanism board: the `Local tide series` boundary is complete; its outbound connector remains visually separate; the principal path still reads left to right.
- Product storyboard: every phone-screen element is contained by the rounded inner screen; the future Tomorrow view no longer implies a current level, direction or position; the host surface, curve and next-turn hierarchy remain unchanged.
- A directory comparison against accepted Draft 1 found differences only in the two revised SVG/PNG pairs, `brief.yaml`, `decisions.md`, `evaluation.md` and `contact-sheet.png`; the scanned sketch and HTML prototype directories are unchanged.
- `scripts/check_pack.py` passed with `0` warnings.

### Product storyboard score

| Criterion | Score (0–2) | Note |
| --- | ---: | --- |
| Proposition | 2 | Clear in the rail and product hierarchy. |
| Visible value | 2 | Now and next are legible in the hero surface. |
| Decisive interaction | 2 | The future-day transition preserves the curve and next-turn grammar without inventing a current state. |
| Focus | 2 | One phone widget is the hero; other moments are subordinate. |
| Conceptual honesty | 2 | Illustrative data and exclusions are visible in-product. |
| Editability | 2 | Interface, copy, curve and framing remain separate SVG elements. |
| Discussion value | 2 | The curve’s confidence-versus-density trade-off is explicit. |
| **Total** | **14/14** | No zero scores. |

## Preserved interaction QA

The standalone HTML was explicitly outside the Draft 2 edit scope. Byte comparison confirms that `prototype.html` and `screen-01.png` through `screen-03.png` are identical to accepted Draft 1. The following QA therefore remains the accepted Draft 1 interaction record rather than a new export pass:

- Exported all three principal states through the reusable `data-stage-button` contract.
- Verified the default Today state without interaction.
- Click-tested Today, Sunday 6 and Monday 7: height, direction, curve path, marker, previous turn, next turn and `aria-pressed` state update coherently.
- Verified sequential native keyboard order across all three day buttons.
- Verified an `aria-live="polite"` announcement for meaningful state changes.
- Verified reduced-motion handling.
- At a 736 px page viewport, the bounded product capture is exactly `390 × 844`.
- At both 736 px and 360 px page widths, there is no horizontal overflow; the phone reflows at 360 px and the smallest meaningful caveat remains 11 px.
- Browser QA completed with no page or console errors.

Preserved representative exports:

- `screen-01.png` — Today, `2.4 m`, rising, next high at `18:42`.
- `screen-02.png` — Sunday 6, `3.1 m`, falling, next low at `19:07`.
- `screen-03.png` — Monday 7, `1.7 m`, rising, next high at `19:36`.

The future-day semantics corrected in the Draft 2 storyboard are not retrofitted into these retained HTML states because the human instruction explicitly required the HTML prototype to remain unaltered.

## Export tooling

The two affected SVGs and the contact sheet were rendered with the supplied helper against the already bundled workspace dependency runtime (`26.904.11930`); nothing was installed. No HTML state export was run because the prototype was preserved.

## Remaining assumptions and limits

- A neutral phone lock screen is the sharpest test of glance density; the desktop widget is a subordinate translation rather than a second interactive prototype.
- Three days remain the accepted horizon from Draft 1.
- `St Ives` is only example location copy. Dates, times and heights are fictional and must not be read as a real prediction.
- The pack does not test prediction accuracy, coverage, technical feasibility, market demand, physical ergonomics, weather, warnings, hazards or safety outcomes.

## Evaluation outcome

Draft 2 passes the scoped visual and export gates. The two requested PNGs and contact sheet were re-rendered; accepted sketch and HTML artefacts were not altered. The proposition, composition, hierarchy and visual language remain recognisably Draft 1, while the boundary, phone clipping and future-day semantics are corrected locally.
