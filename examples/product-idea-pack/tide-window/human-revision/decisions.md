# Tide Window — Draft 2 decisions

## Pack intent

This is a cross-format translation test, not four independent concepts. Draft 1 is accepted. Draft 2 is a human-led, tightly scoped correction to the mechanism board and product storyboard only.

## Stable proposition

**Know where the water is now — and what it does next.**

The current prediction is placed on a compact curve, paired with direction and the next turning point, then carried into future days.

## Shared editorial frame

- Status: `EARLY PRODUCT IDEA — FOR DISCUSSION` for the sketch and board; `PRODUCT CONCEPT — FOR DISCUSSION` for the storyboard and prototype.
- Beat 1: `SEE NOW` — Predicted height and direction at a glance.
- Beat 2: `READ THE CURVE` — Place now between the last and next turn.
- Beat 3: `LOOK AHEAD` — Move day by day without adding unrelated conditions.
- Question: `Does the curve add confidence at glance size, or just density?`
- Caveat: `Illustrative tide prediction only — not weather, warnings or local hazard advice.`

## Interaction model

The HTML prototype uses one persistent, neutral 390 × 844 phone surface. Three semantic day buttons update the curve, height, direction and next turning point in place. The first rendered state is useful without interaction. Representative captures use the bounded product surface at 390 × 844; responsive checks use 736 px and 360 px page widths.

## Format translations

- Proposition sketch: situated sequence of packing, checking and reaching the beach. The phone remains subordinate to the human decision.
- Mechanism board: illustrative tide series becomes height, direction, a now marker and next turn; the curve is marked as the weak link under test.
- Product storyboard: the lock-screen widget is the hero; a future-day view and desktop translation are subordinate.
- Interactive prototype: the same information hierarchy is operated across Today, Tomorrow and Monday.

## Product and editorial colour

- House marker: pale yellow `#F2DC72`.
- Product state accent: muted tidal blue `#2E6973`, reserved for the curve, live/selected position and selected day.
- Primary ink: `#222321`; muted copy: `#6D6B65`; rules: `#D8D6CF`.

## Truth and scope

All names, dates, times and tide heights are illustrative. The concept does not report weather, warnings or local hazards and must never be treated as safety advice. No backend, live feed, affiliation or operational reliability is being tested.

## Draft status

Draft 2. Source revision `007ade1`. Harness: Codex desktop. Human-feedback rounds: `1`.

## Human-led revision record

```yaml
revision:
  request: Correct three local presentation and conceptual defects without redesigning accepted Draft 1.
  preserve:
    - Proposition
    - Composition
    - Copy
    - Hierarchy
    - Colours
    - Interaction
    - Entire scanned sketch
    - Standalone HTML prototype and its state captures
  change:
    - Clip all phone-screen contents to the existing rounded inner screen in the product storyboard.
    - Restore the right-hand boundary of the Local tide series box while retaining the connector gap.
    - Remove the future-day current height, direction and position marker from the storyboard's Tomorrow view.
    - Re-render only the mechanism-board PNG, storyboard PNG and contact sheet.
  accepted_decisions:
    - Draft 1 is accepted as the revision baseline.
    - Current height, rising or falling direction and a current-position marker belong to Today, not an unanchored future-day view.
    - The HTML prototype remains byte-identical in this scoped revision.
```
