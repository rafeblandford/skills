# Draft 1 evaluation

## Run record

| Field | Value |
| --- | --- |
| Skill source revision | `007ade1` |
| Verified repository revision | `007ade1` |
| Harness | Codex desktop |
| Model | GPT-5 |
| Date | 5 September 2026 |
| Example mode | One-shot |
| Human feedback rounds | **0** |
| House style | `editorial-instrument@2` |
| Selected format | Interactive prototype |
| Presentation mode | Editorial |

The supplied brief was the only concept input. No historical RafeOS Delta Brief output, brief, decision record, evaluation, image, prototype or archive was inspected or reused.

## Result

Draft 1 turns the brief into a three-state behaviour test:

1. a first briefing establishes the 07:30 baseline;
2. a later briefing leads with three material changes and a visible comparison point;
3. one action recovers the complete 17:30 briefing while preserving changed markers.

The primary learning question remains visible in the presentation frame: **Does leading with change reduce scanning without weakening trust in what was omitted?**

## Why this format and state count

The user delegated both decisions. An interactive prototype was selected because disclosure, recovery and reversibility need to be operated. A storyboard would show the moments but would not test whether “Show full briefing” feels immediate or whether returning to changes preserves orientation.

Three principal states are the smallest set that covers the edge condition and the core loop: no prior briefing, a later change-led briefing, and recovered full context. `Mark reviewed` is intentionally a reversible control inside the later state, not a fourth screen.

## Visual QA

Checked the rendered artefact at its intended 1440 × 1024 product viewport and as a 1672 × 941 presentation overview.

- The proposition, three editorial beats, question and truth note form a clear reading order.
- The feature remains the hero; the deliberately minimal RafeOS shell provides context without claiming native-product fidelity.
- Yellow is confined to editorial state selection and beat markers. Teal has one semantic role: changed or comparison-related content.
- Each surfaced change has a written `WHY THIS MATTERS` reason, so colour is not the only signal.
- The bounded product captures are 1376 × 736, 1376 × 736 and 1376 × 950 pixels; the full-context state grows naturally rather than being compressed.
- The final overview is exactly 1672 × 941 and includes the proposition, beats, change-led state, discussion question and truth note without clipping.

Autonomous corrections made during visual QA:

- Increased the smallest annotation and state-label text from 10 px to 11 px.
- Replaced an overview `zoom` treatment that overran the right edge with a bounded `transform: scale(.75)` composition. The corrected overview has zero horizontal overflow and keeps the product within the editorial frame.

These corrections did not change the proposition, mechanism, editorial beats or state model, so the run remains one-shot with zero human-feedback rounds.

## Interaction QA

Exercised every control in a browser, including the representative-state controls and the in-product path.

- `See the later briefing` moves state 0 → 1 and focuses the new heading.
- `Show full briefing` moves state 1 → 2; all nine items appear and all three changed markers remain.
- `Back to changes` returns state 2 → 1 and restores the change-led view.
- `Mark reviewed` toggles all three delta items, updates `3 unreviewed` → `3 reviewed`, changes its label to `Mark unreviewed`, and reverses cleanly.
- The polite live region announces state and reviewed-status changes.
- Keyboard order begins with `First briefing`, `Later · changes`, `Later · full context`, then the active state's primary path control.
- Controls use semantic `button` elements and visible focus treatment.
- Reduced-motion preferences are honoured.

## Responsive and runtime QA

| Width | Result |
| --- | --- |
| 1440 px | No horizontal overflow; three change items and all actions stay within the bounded product surface. |
| 736 px | No horizontal overflow; the comparison and change reasons reflow; minimum visible product text is 11 px. |
| 360 px | No horizontal overflow; global navigation is removed from the narrow layout, product controls remain at least 42 px high, and content becomes a single reading column. |

- Browser console errors and warnings: **0**.
- External network dependencies: **0**.
- Live backend, model or autonomous action implied: **none**; the interface says `Illustrative data` and `No live RafeOS data`.
- Theme QA: not applicable; Draft 1 intentionally declares a light-only colour scheme rather than offering theme-aware styling.

## Export and pack QA

- The supplied state exporter completed successfully for all three principal states at the recorded 1440 × 1024 viewport using bounded product capture.
- All four PNGs were opened and visually inspected after export.
- `check_pack.py` result: **passed with 0 warnings**.
- Placeholder and external-dependency scan found no unresolved placeholder copy, TODOs, FIXMEs or remote asset URLs.
- The share archive is built from an explicit public-safe file list and verified separately after creation.

## What Draft 1 does not establish

- Whether RafeOS can calculate materiality accurately.
- Whether the sample number of changes is representative over time.
- Whether a different comparison anchor—last read, last delivered or start of day—would be more trustworthy.
- How delta briefings should be notified, scheduled or persisted.
- Whether this visual shell matches the live RafeOS briefing.

## Recommended critique target

Use the change-led state (`screen-02.png` or `Later · changes` in the prototype) as the primary feedback target. Ask whether the comparison point, the three materiality reasons and the unchanged-context summary provide enough confidence to delay opening the full briefing.

The sensible next format is not another artefact yet. First run a short observed usability test with the prototype. If the disclosure model is accepted, the next step is a technical spike on comparison anchors and materiality rules rather than higher visual fidelity.
