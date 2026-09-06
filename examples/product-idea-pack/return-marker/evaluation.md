# RETURN MARKER · PRODUCT STORYBOARD · DRAFT 1

## Run record

| Field | Value |
| --- | --- |
| Source revision | `d2046bc2852d` (`d2046bc`) |
| Harness | Codex desktop app · local workspace harness |
| Model | GPT-5 (Codex) |
| Human-feedback rounds | `0` |
| Run date | 2026-09-05 |
| Format | `product-storyboard` |
| Presentation mode | `native` |
| House style | `editorial-instrument@2` |
| Canvas | 1672 × 941 px |
| Concept input | Only the brief supplied for this run |

No earlier Return Marker output, brief, decision, evaluation, image or share archive was inspected or reused. No human feedback was supplied between the direction checkpoint and this Draft 1 evaluation.

## Direction assessed

The storyboard places a paragraph-level return marker inside a neutral desktop reading surface. A compact recap sits beside the prose, remains explicitly dismissible and leads to a small continuation state. The visual deliberately leaves the recap visible so the core uncertainty remains discussable: does it restore context, or become another interruption?

The board does not test meaningful-read detection, recap-generation accuracy, mobile behaviour, cross-device synchronisation or the feature’s measured effect on re-entry time.

## Product-storyboard rubric

| Criterion | Score | Evidence |
| --- | ---: | --- |
| Proposition | 2/2 | The rail states a specific changed experience: return to the last thought rather than hunt for it. |
| Visible value | 2/2 | The interruption, restored place and continued reading are connected in one situated sequence. |
| Decisive interaction | 2/2 | The hero state shows the paragraph marker, optional recap, close control and dismiss action. |
| Focus | 2/2 | The feature is the hero; the host is a deliberately neutral, partial reading surface. |
| Conceptual honesty | 2/2 | Illustrative content and simulated elapsed time, detection and recap copy are labelled. |
| Editability | 2/2 | Composition, interface, copy, connectors and truth labels remain editable SVG elements. |
| Discussion value | 2/2 | The board makes the recap’s potential helpfulness and interruptiveness visible at once. |
| **Total** | **14/14** | Target met; no zero in a critical criterion. |

## Static-layout QA

QA was applied after final copy reflow using the `static-layout-qa.md` version at source revision `d2046bc2852d`.

### Render and inspection

- Rendered the editable SVG to PNG at 1672 × 941 using the bundled `render_svg.cjs` helper with the workspace Node.js and Sharp runtime.
- Inspected the complete rendered board at presentation size for hierarchy, reading order, native-surface dominance and connector meaning.
- Inspected full-resolution crops of the editorial rail, re-entry marker and recap cluster, and the continuation/device-bottom region at 100–200% equivalent detail.
- Excluded temporary diagnostic crops from delivery.

### Corrections made from rendered pixels

1. The bold re-entry sentence extended into the recap zone. It was split across two lines and the following article copy was reflowed downward.
2. The browser footer statement extended behind the continuation inset. It was shortened to `THE ARTICLE REMAINS PRIMARY.`
3. The continuation caption and bottom-right host note competed visually. The caption was raised and the host/simulation disclosure was consolidated into one left-aligned truth line.

The affected regions were re-rendered and re-inspected after each correction group.

### Final result

| Pass | Result | Notes |
| --- | --- | --- |
| Boundary | Pass | All copy and strokes remain inside their intended zones; the exact identity is present and subordinate; the device outline is complete; screen content is clipped to the display. |
| Collision | Pass | Neither connector crosses readable copy; arrowheads stop clear of the return marker and continuation frame; the recap does not cover article prose. |
| Breathing room | Pass | The working-field perimeter remains quiet; native frames and labels retain visible clearance from field and canvas edges. |
| Two-scale inspection | Pass | Full-board hierarchy and magnified rail, feature cluster and bottom-edge regions were checked from the final PNG. |

## Material assumptions retained

- Paragraph-level “meaningfully read” progress can be inferred reliably.
- A desktop side placement is noticeable without pulling attention away from the prose.
- Eighteen minutes is illustrative interruption context only.
- The recap text is plausible illustrative copy, not evidence of summarisation quality.

## Recommended next learning step

Do not increase visual fidelity yet. Put this storyboard in front of readers and ask them to narrate the return moment. If they disagree about whether the recap should appear automatically, the sensible next format is a narrowly scoped interactive prototype comparing visible-by-default with collapsed-by-default recap states.
