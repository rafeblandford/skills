# Brand profiles

A brand profile is an optional overlay. The house style continues to control editorial hierarchy, spacing and explanatory rhythm; the brand profile supplies approved marks, typography, colour roles and attribution. It is neither a presentation mode nor an output profile.

Do not apply branding by default, infer a brand from the subject matter or routinely ask an unbranded user to choose one. Use a profile only when the user requests branding, supplies assets or selects an existing named profile.

## Intake

When branding is requested, use supplied assets and guidance. If no usable mark or brand reference is available and inventing one would affect credibility, ask one concise question for a logo, brand guide or representative screenshot. Do not redraw or approximate an established logo without explicit permission.

Record:

- profile identifier and version;
- supplied marks and their provenance;
- wordmark spelling and case;
- palette roles rather than a list of decorative colours;
- typefaces and safe fallbacks;
- minimum size, clear space and permitted backgrounds;
- where the brand should and should not appear.

## Application boundary

Brand the editorial wrapper, contact sheet and selected presentation or design-handoff packaging. Apply the brand inside a depicted product surface only when that product genuinely belongs to the brand. Do not stamp an editorial logo into a neutral host product, third-party interface or product-only native capture merely to make the pack look branded.

Keep the proposition, question and product mechanism more prominent than the logo. A brand accent may replace or complement a product accent, but it does not automatically replace the house-style yellow editorial marker. Preserve contrast and greyscale legibility.

## Assets and portability

Prefer original SVG or another supplied vector mark. Preserve a supplied raster mark without tracing it, record its pixel dimensions and avoid enlarging it beyond a credible display size. Do not package licensed fonts unless redistribution is permitted; record the required face and a safe fallback instead.

Keep public and client-specific profiles separate. Include a profile in a public release only when the marks and guidance are owned by the publisher or cleared for redistribution.

## Manifest

Record the choice in `brief.yaml`:

```yaml
brand_profile:
  id: "none"
  apply_to: []
```

For a selected profile:

```yaml
brand_profile:
  id: example-brand@1
  apply_to:
    - editorial-wrapper
    - presentation
    - design-handoff
```

Adding or removing a brand profile is a packaging and treatment change. It does not advance the concept format; increment the artefact draft only when the branded treatment itself is being reviewed as a revision.
