---
name: product-idea-pack
description: Explore and develop early digital-product ideas as proposition sketches, mechanism boards, product storyboards, interactive HTML prototypes, or coherent multi-format packs, with optional presentation and vector-design handoffs. Use for rapid product ideation, concept visuals, shareable prototypes, packaging accepted artefacts, or advancing an existing concept between formats; do not use for production UI implementation.
license: Apache-2.0
compatibility: Works in Agent Skills-compatible harnesses with file access. Complete scanned proposition sketches require image generation; other missing render or capture capabilities use an explicit hand-off or disclosed fallback.
metadata:
  short-description: Create consistent visual product-idea packs
  author: Rafe Blandford
  version: "0.1.0"
  provenance: written-with-ai
---

# Product Idea Pack

Turn an early proposition into a repeatable sequence of visual thinking artefacts. Preserve useful ambiguity at the sketch stage, expose structure before committing to product detail, and use an interactive prototype only when operating the behaviour will answer the remaining question.

## Model

There are four formats in a typical progression of increasing commitment and product specificity:

| Focus | Format | Question answered |
| --- | --- | --- |
| Role and value | Proposition sketch | Is this an interesting change for someone? |
| Structure | Mechanism board | How does it work, and where can it break? |
| Product experience | Product storyboard | Could this become a believable product experience? |
| Behaviour | Interactive prototype | Does it make sense when operated? |

This is a default route, not a compulsory ladder. Fidelity is multidimensional: an artefact may be specific about role, structure, look and feel or behaviour while deliberately omitting other qualities. Skip, repeat or return to a format when the learning question requires it. Do not use HTML to avoid resolving an unclear proposition or mechanism in a faster static format.

## Load references progressively

Always read:

- [brief-and-conversation.md](references/brief-and-conversation.md) to reconstruct or refine the brief;
- [default-v2.md](references/house-styles/default-v2.md) unless the user names another house style.

Then read an additional presentation-mode reference only when the brief calls for it:

- [Workshop Canvas](references/presentation-modes/workshop-canvas-v1.md) when the artefact is primarily a collaborative working board;
- [Native Surface](references/presentation-modes/native-surface-v1.md) when an intervention must be judged inside an existing product or device.

Then read only the selected format reference:

- [Proposition sketch](references/formats/scanned-sketch-page.md)
- [Mechanism board](references/formats/editable-line-board.md)
- [Product storyboard](references/formats/product-concept-scamp.md)
- [Interactive prototype](references/formats/html-prototype.md)

For a proposition sketch, mechanism board or product storyboard, also read and apply [static-layout-qa.md](references/static-layout-qa.md) after the copy and composition are settled.

Read [pack-output-contract.md](references/pack-output-contract.md) when creating two or more formats, a share pack, a reusable concept folder or a maintained public example.

Read [output-profiles.md](references/output-profiles.md) only when the user requests or accepts a presentation pack, a design handoff or both. These are supplementary delivery profiles, not concept formats.

Read [brand-profile.md](references/brand-profile.md) only when the user explicitly requests branding, supplies brand assets or selects a named profile. Branding is opt-in; do not present it as a routine intake choice.

When rendering or export requires a capability that may differ between environments, read [tool-portability.md](references/tool-portability.md). Use a bundled helper only when its runtime is already available; otherwise choose an equivalent available tool and verify the same observable result.

## Choose the format

Treat the format as resolved when any of these is true:

- the user explicitly names a format or asks for a full pack;
- the requested deliverable or use unmistakably entails one, such as an interactive prototype, editable workshop board, proposition sketch or product storyboard;
- the user accepted a format earlier in the conversation; or
- the user explicitly asks the skill to choose.

When the format is resolved by the requested use rather than a named label, state the interpretation and recommendation in the direction checkpoint, then proceed. When none of the conditions above applies, do not infer the format from the product idea alone: recommend one, briefly distinguish the most relevant alternative, and ask the human to choose before generation.

Use these learning-goal distinctions when making the recommendation:

- choose `proposition-sketch` for emotional clarity, provocation and alternative manifestations before structure is settled;
- choose `mechanism-board` for actors, relationships, dependencies, hand-offs, assumptions and weak links that people need to rearrange or challenge;
- choose `product-storyboard` for a credible stakeholder discussion about a situated product experience across connected moments;
- choose `interactive-prototype` when state, sequence, navigation or cause-and-effect must be experienced;
- choose `full-pack` only when the user asks for a pack or several stages.

An idea containing states or interaction does not itself entail HTML. The user must be asking to experience or test that behaviour, or must delegate the format choice. For a full pack, state whether it is testing cross-format translation or supplying several deliverables. Name one primary artefact for feedback, or explicitly record that no primary exists and ask the human to select a revision target before revising.

Apply a fidelity gate before recommending an interactive prototype:

- if the proposition is still being explored, start with a proposition sketch;
- if the mechanism, system or hand-offs are unresolved, use a mechanism board;
- if the key question is whether a feature or product moment feels credible in context, use a product storyboard;
- use HTML when an accepted or sufficiently concrete interaction must be operated to answer the remaining question, or when the user explicitly requests a prototype;
- an idea being interactive, having several possible states or mentioning AI is not by itself a reason to skip the static formats.

Recognise both proposition-scale ideas and feature-scale ideas. For a feature, show enough of the host product to make the intervention legible, but keep the feature—not an invented surrounding product—as the hero.

If the riskiest question is physical ergonomics, live service operations, market demand or technical feasibility, explain that this pack is insufficient on its own and recommend the relevant physical mock-up, service rehearsal, concierge test or technical spike.

## Intake and references

Use adaptive friction. Reconstruct the brief and infer low-risk detail before asking questions. If the current conversation resolves the idea, audience, learning question, format and context, state the material assumptions and proceed. Ask at most one pre-generation question unless separate missing answers are both essential to creating a meaningful artefact.

When there is no usable idea, offer a short guided start: the user may describe a rough thought, paste a brief or share a reference, and the skill will structure it. Do not present the common brief as a compulsory form.

Request a reference only when its absence would force a consequential invention, especially for a feature inside an existing product, brand or familiar platform pattern. Distinguish host-product references, functional precedents and visual-treatment references; record what to borrow and what to avoid copying. For open proposition exploration, do not request a reference merely to decorate the output.

## Conversation-aware workflow

1. Read the current request and relevant preceding conversation. Do not make the user repeat an idea already present.
2. Distil the concept and prototype profile using the common brief. Separate supplied facts from proposals, assumptions and questions.
3. If the direction is unresolved or the user asks for exploration, propose three structurally different manifestations and recommend one. Do not offer cosmetic variations.
4. Resolve the format using the user's wording, requested use and prior decisions. If it remains unresolved, recommend one and ask the human to choose before generating.
5. Before creating the artefact, present a concise direction checkpoint: format and selection basis, proposition, decisive interaction, composition or interaction model, exact annotation copy, assumptions, the question to provoke, and any capability the selected format needs that is not present together with the choice it implies. For a proposition sketch, name the intended context-led, balanced or product-led emphasis. State the three editorial beats and, separately, any prototype states; do not assume they map one-to-one. If the format was already resolved, this is a progress update rather than an approval gate—with one exception: when a capability the format depends on is not present, stop here, explain the limitation, offer the available routes and wait for the user's choice before composing anything. Optional convenience exports never trigger this stop; proceed and disclose them instead.
6. Ask one additional concise question only when the answer would materially change the proposition, agency model or primary interaction. Otherwise proceed once the format is resolved.
7. Create Draft 1 using the selected format reference and current house-style version. Include only the scope needed to expose the learning question, and say what the artefact deliberately does not test. After final copy reflow, visually verify it at its intended use size and run the relevant layout or interaction QA before delivery.
8. Treat critique as expected. Record what to change and what must remain fixed; revise the smallest relevant layer. Do not silently redesign accepted parts.
9. When the user advances the concept, carry the brief, accepted decisions, truth labels and house style into the next format. Do not restart from a generic prompt.

## Revision discipline

- Call the first artefact `Draft 1`, not final.
- For feedback, restate the requested change and preserved invariants briefly, then act.
- Change one visual variable at a time for image-generation edits: composition, looseness, accent, density or paper treatment.
- Keep decision-bearing copy editable. Correct copy in the editable layer rather than regenerating a raster image.
- Increase the draft number only while every accepted earlier draft keeps its own editable source and PNG under its own draft name. Never overwrite Draft 1 and call the result Draft 2.
- When a tool or fallback route changes, preserve the agreed concept and declared visual emphasis. State any compositional change before making it; a fallback must not quietly turn a multi-scene story into a different object study.
- Create or update `decisions.md` at the first human-directed revision, recording accepted decisions and what must stay fixed rather than a process log. After a substantial revision, update it so later formats inherit the decision.
- Keep revision and translation distinct: a revision changes an artefact within one format; recreating the idea in another format is a translation. Do not switch the revision target without asking.

## House style and presentation mode

The default house style is `editorial-instrument@2`. It controls the shared hierarchy and pack relationship, not the concept or product geometry. Keep it unless the user supplies another house style.

Choose one presentation mode independently:

- `editorial` is the default and needs no extra reference;
- `workshop` makes a static artefact visibly provisional, modular and easy to change;
- `native` lets host-product geometry and conventions dominate a storyboard or prototype.

Infer the mode when the intended use makes it clear. Do not show a routine mode chooser. Ask only when workshop editability and host-product credibility would lead to materially different artefacts.

An evidence record is optional supporting documentation, not a presentation mode or hero output. It is content-led and vertically extensible rather than constrained to a deck-shaped canvas. Read [evidence-record.md](references/evidence-record.md) only when consequential claims, sources or uncertainties need a durable record.

A fictional notification, receipt, letter, status screen or other in-world artefact is a composition pattern inside a proposition sketch or product storyboard. It is not a separate mode. Label speculative material clearly and distinguish fact, extrapolation and invention.

When a user wants a new house style, create a new versioned reference alongside the default. Do not silently overwrite the default or duplicate shared rules across every format reference.

## Output

The core output for one format is its editable or interactive source plus a presentation PNG. For an HTML prototype, also export each principal state. Write every output, including a single format, inside a concept folder named in lowercase ASCII kebab-case after the working name (for example `tide-window/`); do not leave files in the working directory. For multiple formats, follow the pack output contract and create a single share archive when useful.

Presentation and design-handoff profiles are optional packaging around the accepted core artefact. Do not create them by default and do not treat their later addition as a new concept revision. If the user has not already specified supplementary outputs, offer once after the first core delivery: “Would you also like a presentation pack (PowerPoint + PDF), a design handoff (Figma-safe SVG + assets), both, or just the core files?” Do not repeat the offer after routine revisions.

Report:

- the recommended use of each delivered file;
- the material assumptions still present;
- which format would be the sensible next step, if any.
