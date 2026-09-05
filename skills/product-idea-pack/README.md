# Product Idea Pack

Product Idea Pack turns an early digital-product idea into a visual object that
people can discuss before anyone commits to polished interface design.

It can create a proposition sketch, mechanism board, product storyboard,
interactive HTML prototype, or a connected pack of several formats. The output
is deliberately a discussion artefact: clear enough to make the idea tangible,
open enough for somebody to disagree with it.

![Tide Window proposition sketch](https://raw.githubusercontent.com/rafeblandford/skills/main/examples/product-idea-pack/tide-window-astra-one-shot.png)

## What it is for

The skill helps you:

- make a product proposition visible quickly;
- expose a mechanism, hand-off or weak link before polishing the interface;
- compare different manifestations of one idea;
- capture a concept in editable and shareable forms;
- move from a loose thought to a prototype through short human critique rounds.

It is not a substitute for product judgement, research, design craft or testing
with the people affected. It accelerates ideation and concept capture. A human
still decides what matters, challenges the assumptions and chooses what to take
forward.

## Four formats

| Format | Use it to ask | Typical output |
| --- | --- | --- |
| **Proposition sketch** | Is this an interesting change for somebody? | A scanned-ink sketch page with a clear proposition, three beats, a question and notes |
| **Mechanism board** | How does it work, and where could it fail? | An editable line board of actors, relationships, hand-offs, assumptions and weak links |
| **Product storyboard** | Could this become a believable product experience? | A situated sequence of connected product moments |
| **Interactive prototype** | Does the behaviour make sense when operated? | A standalone HTML artefact with meaningful states and captures where available |

This is an increase in commitment, not a compulsory four-step process. Start at
the format that answers the question you have now. If the format is unclear, the
skill recommends one and briefly explains the closest alternative.

## Three ways to begin

### 1. Talk first, then invoke the skill

Use an ordinary conversation to work through the idea. When it is ready to make
visible, say:

> Use Product Idea Pack with the idea we have been discussing. Recommend the
> right format, carry forward the decisions already made, and ask only if a
> missing answer would materially change the result.

This is often the best route because the conversation already contains the
audience, tension, mechanism and open questions.

### 2. Give it a brief

If you know what you want, name the format and provide the important constraints:

> Use Product Idea Pack to create a proposition sketch for Tide Window. Weekend
> dinghy sailors struggle to decide whether today is worth the effort. The
> product proposes one two-hour window where tide, daylight and wind line up,
> explains why, and lets the sailor commit to it. The question is whether people
> will trust one recommendation over their own reading of the tables. Treat all
> values as illustrative and do not imply safety advice. Draft 1, default house
> style, no branding.

The format is already resolved, so the skill can move directly to its direction
checkpoint and creation.

### 3. Ask it to guide you

You can start with very little:

> Use Product Idea Pack to help me turn a rough product idea into something I can
> discuss. Ask me the one most useful question, recommend a format, and explain
> what you are inferring.

The skill is designed to keep this fast. It should not turn intake into a long
questionnaire.

## What determines the result

Short prompts are valid, but they give the agent more room to invent. The most
useful inputs are:

- **who it is for** and the situation they are in;
- **what changes** for them if the idea exists;
- the **distinctive mechanism or interaction**, if known;
- the **question the artefact should provoke**;
- the desired **format or use**, if already decided;
- facts, constraints and things the concept must not imply;
- a reference screenshot, parallel product or visual example when it would
  reduce invention;
- what you want to borrow from a reference, and what you want to avoid.

You do not need a final name, format or version. The skill can infer a working
name and starts at Draft 1. Material inferred mechanisms should be labelled
**Proposed** on the artefact rather than presented as settled product truth.

### A reusable brief template

```text
Idea:
Audience and situation:
What changes for them:
Important mechanism or interaction:
Question to provoke:
Known facts and constraints:
What must not be implied:
Preferred format or intended use (optional):
References and what to borrow or avoid (optional):
Output location or delivery needs (optional):
```

## References help when they have a job

A reference is useful when it reduces a specific uncertainty. It can be:

- a **host reference** showing the product or service the idea must fit into;
- a **functional precedent** showing a useful interaction or information pattern;
- a **treatment reference** showing the desired visual character.

Supply the image or file and say what matters about it. “Use the density and
phone proportions, but not the colour palette” is far more useful than “make it
like this”. If no reference is supplied, the default house style is restrained,
editorial and intentionally low-fidelity.

## Expect a conversation, not a one-shot design service

Draft 1 is a concrete object for critique. Useful feedback is specific:

- “The sketch explains the situation but not the product intervention.”
- “Keep Draft 1. In Draft 2, make the lender's risk the second beat.”
- “The phone is too dominant; preserve the copy and rebalance the composition.”
- “Translate this accepted mechanism board into an interactive prototype.”

The skill preserves earlier accepted drafts when the draft number changes and
records material human decisions. Translating an idea into another format is not
treated as a revision: each format answers a different question.

## Examples

The published examples deliberately cover different starting points and levels
of human intervention.

| Example | What it demonstrates |
| --- | --- |
| [Tide Window](https://github.com/rafeblandford/skills/tree/main/examples/product-idea-pack#tide-window) | A zero-feedback Astra proposition sketch, plus a later cross-format human revision |
| [Borrow Nearby](https://github.com/rafeblandford/skills/tree/main/examples/product-idea-pack#borrow-nearby) | One proposition expressed as both a human sketch and a rearrangeable mechanism board |
| [Return Marker](https://github.com/rafeblandford/skills/tree/main/examples/product-idea-pack#return-marker) | A specific feature shown inside a neutral host product rather than as a whole new service |
| [RafeOS Delta Brief](https://github.com/rafeblandford/skills/tree/main/examples/product-idea-pack#rafeos-delta-brief) | A thin brief where the skill selected an interactive prototype and the number of states |

“Zero human feedback rounds” means the agent received no critique between the
saved prompt and Draft 1. It does not mean the skill itself was made without
human involvement, nor that the agent skipped its own rendering and layout QA.

## Core and optional outputs

Static formats normally include an editable SVG and a presentation-ready PNG.
Interactive prototypes include standalone HTML and state captures where a browser
capture capability is available. Multi-format packs also keep a brief, decisions
and evaluation record.

After an artefact is accepted, the skill can optionally produce:

- a **presentation profile**: placed-vector PowerPoint plus matching PDF;
- a **design-handoff profile**: normalised SVGs, reference PNGs and import notes
  for tools such as Figma.

Branding is opt-in. A brand profile can add a logo, wordmark, colours and wrapper
rules without forcing the product surface itself to look branded.

## Installation

### Quickest cross-client route

If you use the community `skills` installer and have Node.js available:

```sh
npx skills add rafeblandford/skills
```

Choose `product-idea-pack` when prompted, then start a new agent session.

### Codex

The simplest route is to ask Codex:

> Install the `product-idea-pack` skill from
> `https://github.com/rafeblandford/skills/tree/main/skills/product-idea-pack`.

For a manual personal installation, copy the complete
`skills/product-idea-pack/` folder to `~/.codex/skills/product-idea-pack/` and
start a new task. For a project-local installation in a compatible client, place
it at `.agents/skills/product-idea-pack/` in that project.

Codex currently provides the strongest complete proposition-sketch route when
its image-generation capability is available.

### Claude Code

Add the public marketplace, then install the plugin:

```text
/plugin marketplace add rafeblandford/skills
/plugin install product-idea-pack@rafeblandford
```

Start a new session or run `/reload-plugins`. The explicit invocation is
`/product-idea-pack:product-idea-pack`, although Claude can also select the skill
from an ordinary matching request.

### Claude Cowork

Download `product-idea-pack.plugin` from the
[latest GitHub release](https://github.com/rafeblandford/skills/releases/latest),
open **Customize → Plugins**, and upload the file. Start a fresh Cowork session
after replacing an older version.

### Other Agent Skills clients

Install or copy the complete `skills/product-idea-pack/` directory using your
client's normal Agent Skills mechanism. Keep the folder intact: the skill routes
to its references, templates and helper scripts at run time.

## A quick installation test

Start a new session and try:

> Use Product Idea Pack. I have an idea for neighbours to borrow rarely used
> household tools. I want something I can show two friends, but I have not chosen
> a format. Recommend where to start and explain the closest alternative.

The skill should recommend one format and wait for your choice. If it immediately
builds an HTML prototype, the skill has not loaded correctly or another
instruction is overriding it.

## Capability differences

The underlying method is provider-neutral, but the tools are not identical.
Claude Code and Cowork did not expose native text-to-image generation in the
release tests. For a proposition sketch they therefore stop before composition
and offer three honest routes: generate the ink layer elsewhere, supply an
existing sketch, or accept a visibly incomplete ink field. Mechanism boards,
storyboards and HTML prototypes remain usable through the capabilities present.

Missing convenience exports are disclosed rather than faked. The editable source
remains the primary deliverable.

## Provenance

Product Idea Pack was created through human–AI collaboration. Rafe Blandford set
the product intent, format taxonomy, house style, quality bar and release
decisions through repeated critique. Codex and Claude agents helped research,
draft, generate, test and refine the skill and its example artefacts. Published
examples record their harness, model and number of human feedback rounds wherever
that information is available.

This is labelled `written-with-ai`, following
[Rafe's provenance vocabulary](https://rafeblandford.com/ai-provenance/).

## Licence and feedback

Product Idea Pack is available under the Apache License 2.0. You may use it,
modify it and distribute derivatives under the licence terms.

There is no requirement to tell Rafe that you used it, but he would genuinely
like to hear what you made or changed. Open an
[issue](https://github.com/rafeblandford/skills/issues) or get in touch through
[rafeblandford.com](https://rafeblandford.com/).
