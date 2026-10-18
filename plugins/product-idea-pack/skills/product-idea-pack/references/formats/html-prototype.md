# Format: Interactive prototype

## Use when

The remaining question concerns behaviour: sequence, navigation, state change, branching, user control or cause-and-effect. This is a step beyond a product storyboard, not a polished production implementation.

## Scope

- Choose the smallest interaction model that answers the behavioural question.
- Record the prototype's focus and scope, plus the qualities it deliberately does not test.
- Use one persistent surface for direct manipulation, a control changing data in place or a feature whose value appears without navigation.
- Use two states for a meaningful before/after or input/response transition.
- Use three or more only when sequence, branching, hand-off or a loop genuinely requires them.
- One decisive interaction should drive each state or meaningful change.
- Use local illustrative data. Do not imply a real backend, live model or autonomous action unless one exists.
- Preserve the proposition, truth labels and house-style version from the preceding brief or storyboard.

The house style's three editorial beats explain mechanism and value. They are not a required screen count, navigation model or progress indicator. Do not turn them into tabs merely because the shared frame contains three beats.

## Product shell

- Use one consistent application shell across states.
- Put app-wide navigation in the shell and local controls in the active screen.
- Make the first rendered state useful without interaction.
- Keep product surfaces opaque and the surrounding presentation surface restrained.
- Use realistic controls and visible labels; do not fake an interface with a screenshot.
- Name the intended product surface and canonical capture viewport in the decision record. If it is a phone, lock screen, widget or other familiar host, use recognisable proportions, safe areas, spacing and control conventions rather than a generic dashboard treatment.
- Do not squash or shorten a device frame to fit a presentation canvas. Let the editorial wrapper scroll or capture the product surface independently.

## Interaction

- Use semantic HTML controls and native keyboard order.
- Keep interactions local unless the user explicitly requests integration.
- Use `aria-live="polite"` for meaningful selected-state updates.
- Honour reduced-motion preferences.
- Do not add search, filters, dashboards or reset controls merely to make the prototype feel complete.

## Reusable state contract

When practical, expose:

- a root element with `data-prototype-root`;
- each control used for a representative export with sequential `data-stage-button` values beginning at `0`;
- matching stage regions when the prototype uses discrete screens;
- branch choices with `data-branch-choice` when the idea contains alternatives.

This allows the supplied exporter to capture discrete principal states without concept-specific automation. It is optional for continuous controls or a single persistent surface; use equivalent browser capture for the representative states instead of distorting the interaction to satisfy the helper.

## Responsive behaviour

- Design first at the viewport appropriate to the product surface, then verify the surrounding prototype at 736 px and 360 px. When no particular phone is specified, 390 × 844 is a useful mobile calibration rather than a mandatory device target.
- Reflow sequences vertically rather than shrinking text or creating horizontal scrolling.
- Keep important text at least 11 screen pixels.
- Avoid unnecessary internal scrolling. A full editorial prototype page may be taller than one viewport; do not compress the product merely to keep the whole explanatory wrapper above the fold.

## Standalone output

Create a self-contained HTML file with inline CSS, JavaScript and data and no build step. Avoid network dependencies. If a dependency is unavoidable, disclose it and ensure the core idea remains understandable when it fails.

The prototype is a thinking object. Do not add authentication, persistence, analytics or production architecture unless requested.

## Conversation and revision

Expect iteration after Draft 1. Preserve accepted shell, copy and state sequence while changing the smallest relevant behaviour. If feedback changes the proposition, update the common brief before editing the prototype.

## Output and QA

Produce:

- standalone HTML;
- one PNG for each principal or deliberately sampled state at the recorded product viewport or from the bounded product surface;
- an optional 16:9 overview capture when the artefact also needs to sit in a presentation deck;
- a zip containing the HTML and PNGs when sharing is likely.

Test:

- every control and state transition;
- the default state without interaction;
- light and dark appearance when theme-aware styling is used;
- desktop and narrow widths;
- credible geometry and interface conventions for any depicted host device;
- absence of console errors and horizontal overflow.

Use `scripts/export_html_states.cjs` from this skill's folder when the state contract is present and its runtime is already available; otherwise use an equivalent browser capture that is present, or deliver the HTML and flag the captures as outstanding. Run `scripts/check_pack.py` from this skill's folder for a reusable pack.
