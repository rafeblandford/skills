# Brief and conversation contract

The skill must work both when the user supplies a complete brief and when the idea has emerged through a longer conversation.

## Adaptive intake

Optimise for useful momentum, not exhaustive intake.

**Fast path:** reconstruct the idea from the request and relevant conversation, infer low-risk detail, state any material assumptions and proceed when the idea, audience, learning question, format and context are explicit or safely inferable.

**Guided path:** recommend a direction and ask one concise question when one unresolved choice would materially change the proposition, agency model, product context, learning goal or artefact. Do not ask for confirmation of choices the user has already made. Ask more than one pre-generation question only when separate missing answers are essential to creating a meaningful artefact.

**Cold start:** if there is no usable idea, briefly explain that the user can describe a rough thought, paste an existing brief or share a reference. Offer to help shape incomplete material; do not present the common brief as a form they must complete.

## Input mode A: explicit brief

Use the supplied wording and constraints. Infer only low-risk visual detail. Do not turn a short prompt into an invented requirements document.

## Input mode B: conversational context

Reconstruct the brief from the current request and relevant preceding turns:

- prefer the user's most recent formulation when language has evolved;
- preserve decisions the user accepted or explicitly preferred;
- treat discarded directions as historical context, not current requirements;
- do not ask the user to repeat material already available;
- call out an inference when it changes the proposition or behaviour, and carry it onto the artefact as **Proposed** when it is a material mechanism or the decisive interaction.

If the conversation contains several ideas, identify the one in active scope. Ask only when selecting the wrong idea would materially waste work.

## Minimum viable brief

Work can begin when these four things are reasonably clear:

1. the idea or `What if…?` proposition;
2. the audience or user;
3. the decisive interaction and changed outcome;
4. the important uncertainty or discussion question.

If one element is absent but safely inferable, infer it and label it. If its answer would alter the concept materially, ask one concise question.

## Common brief

Use this shape internally and save it as `brief.yaml` for a reusable pack:

```yaml
idea_name:
idea_scale: product | service | feature
idea:
audience:
decision_to_support:
current_situation:
current_friction:
what_if:
value_promised:
decisive_interaction:
system_response:
changed_outcome:
important_uncertainty:
question_to_provoke:

truth:
  known: []
  proposed: []
  assumed: []
  to_learn: []

brand_or_context:
must_show: []
must_avoid: []
evidence_or_sources: []

prototype_profile:
  focus: role | structure | product-experience | behaviour | implementation
  scope: slice | flow | system
  audience_for_artefact:
  deliberately_omits: []

references:
  host: []
  precedent: []
  treatment: []
  borrow: []
  avoid: []

format: auto
format_basis: unresolved
house_style: editorial-instrument@2
presentation_mode: editorial
brand_profile:
  id: "none"
  apply_to: []
evidence_record: none
output: single

delivery:
  core: true
  output_profiles: []
  powerpoint_mode: placed-vector
  design_target: figma
```

Do not require the user to fill every field. The structure is a memory and hand-off format, not a form barrier.

## Reference intake

References are optional. Request one only when its absence would force a consequential invention, especially when the idea must fit an existing product, brand, device or familiar interaction pattern. A screenshot is often high-value for a feature inside a known host product; it may be actively unhelpful during open proposition exploration.

Classify each supplied reference by the job it does:

- **Host:** the existing product screen, brand system or device context the idea must fit.
- **Precedent:** a comparable interaction, service or information pattern worth learning from.
- **Treatment:** a layout, visual language or atmosphere to borrow.

Record what to borrow and what to avoid copying. Do not reproduce a reference pixel for pixel, infer facts from appearance alone or allow a visual reference to replace the learning question.

## Direction checkpoint

Before substantial generation, state concisely:

- selected format and its basis: explicit format, explicit deliverable, prior decision, delegated choice or human confirmation;
- presentation mode and its basis when it is not the editorial default;
- exact proposition;
- decisive interaction;
- prototype focus, scope and what is deliberately omitted;
- the three editorial beats;
- the interaction model and principal states, when creating a prototype;
- question to provoke;
- the role of any consequential reference;
- any capability the selected format requires that is not present, and the options the user can choose between;
- whether a supporting evidence record is needed;
- material assumptions introduced.

The format does not need reconfirmation when the user named it, requested a deliverable that unmistakably entails it, accepted it earlier or explicitly delegated the choice. Otherwise recommend a format, distinguish the most relevant alternative in one sentence and ask the human to choose before generation. Do not use the product idea's mere presence of interaction or multiple states as sufficient evidence for HTML.

If the format is resolved and the interpretation is low risk, present the checkpoint as a progress update and continue. It is not a second approval gate.

## Iteration record

When revising, track:

```yaml
revision:
  request:
  preserve: []
  change: []
  accepted_decisions: []
```

Use the record to avoid reintroducing rejected treatments or disturbing accepted copy. A revision may change the common brief; when it does, update the brief before advancing to another format.

## Advancement

Moving to a higher-fidelity format should preserve:

- proposition and audience;
- accepted interaction names;
- question and uncertainty;
- truth labels;
- house-style version;
- prototype focus, scope and deliberate omissions;
- reference roles and any explicit borrow or avoid decisions;
- any explicit `must_show` and `must_avoid` constraints.

Add only the detail needed by the next learning question.

Do not treat advancement as automatic. A static artefact may be the finished outcome. When an interactive prototype is proposed, name the behavioural question that cannot be answered adequately by the current sketch, board or storyboard.

Changing format is a translation, not a revision. Preserve the current revision target unless the human asks to translate or accepts that recommendation.
