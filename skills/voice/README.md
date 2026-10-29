# voice

Draft writing that goes out under your own name, in your voice and your
argument. `voice` drafts from your material (dictation, notes, a brief) and
keeps the argument yours: where a step in the reasoning is missing, it asks
rather than inventing one. Its partner skill, [`deslop`](../deslop/), reviews a
draft before it goes out.

[Read the website guide](https://rafeblandford.com/voice-and-deslop/) ·
[Read the launch article](https://rafeblandford.com/writing-with-ai-in-my-own-voice/) ·
[See the examples](https://github.com/rafeblandford/skills/tree/main/examples/voice) ·
[Install](https://github.com/rafeblandford/skills#installing)

## Before you start: build your own voice pack

The skill is a generic instrument. Everything about you lives in a separate
**voice pack**. This skill ships with a **fictional example pack** at
`references/pack/` (a civil engineer writing about infrastructure) to show the
shape. It's nobody's voice: `voice` says so and works generically until you
give it your own.

To have it write as you, build a pack from your own writing. The guide is
[`references/pack/README.md`](references/pack/README.md).

Then tell the skill where it is. It takes the pack from the first of these
that names one:

1. **What you say when you ask:** "use my voice pack in `~/writing/voice-pack/`".
2. **A `voice_pack:` line in your own instructions**, the file your tool loads
   into every conversation (`CLAUDE.md`, `AGENTS.md`, or the custom instructions
   in the Claude app):
   ```text
   voice_pack: ~/writing/voice-pack
   ```
   Put it in your global instructions to use the pack everywhere, or in one
   project's to use it there. This is the route that lasts: the pack lives
   outside the skill, so an update can't replace it. It works in every client,
   including the Claude app, where an installed skill's files can't easily be
   edited.
3. **The pack inside the skill**, at `references/pack/`. Replacing that folder
   in your copy works, but the next update puts the fictional pack back.

If it finds only the fictional pack, or nothing, the skill says so first and
works generically. It never presents a generic draft as your voice.

A pack can quote your correspondence and your unpublished work, so keep it
private.

## What it does

`voice` sets its depth by a **tier**: how much it matters that the piece sounds
like you.

| Tier | Typical pieces | `voice` |
|---|---|---|
| 1 | Quick email, replies | Drafts in your register |
| 2 | Short public posts, internal documents | Every claim traced to you |
| 3 | Essays, talks, anything read closely | Records where every line came from |

At tier 3 it writes a provenance record beside the draft
(`provenance-r<n>.md`): for each paragraph, whether it came from your source,
from you directly, or from the drafter, and whether you've approved it. Words
you wrote are carried over as they are; dictated words can be tidied but not
swapped for generic phrasing. Questions sit in the draft where the answers would
go, as `> **[Q1]** …`.

Say the register, the tier and what your source is when you ask; `voice` infers
them otherwise and says which it chose.

## The draft and revision page

`scripts/revision_page.py` turns a draft into a single page you open in a
browser. A first draft shows where each paragraph came from (when drafting at
tier 3), with its questions. After that, the page compares a draft with the one
before and numbers every change, so you can see quickly what changed rather than
hunting for it.

When the page appears depends on the care tier. At tier 2 and 3 it is built
and shown with every draft or revision you're handed back, without asking; at
tier 1 it is offered in one line. Asking for it ("show me what changed") always builds it.

To change that, add a line to your own instructions, beside any `voice_pack:`
line, or just say so in the conversation, which wins over the line:

| Line | What it does |
|---|---|
| `voice_pages: 2` | The default: built at tier 2 and 3, offered at tier 1 |
| `voice_pages: 1` | Built at every tier |
| `voice_pages: 3` | Built at tier 3, offered below it |
| `voice_pages: offer` | Offered at every tier, built if you say yes |
| `voice_pages: off` | Never offered; everything stays in the conversation |

The same line governs both `voice` and `deslop`.

You don't edit on the page. Talk or type the changes you want, and the numbers
mean you can say "on change 3…" and it knows which edit you mean; or jot notes
against changes, use **Copy notes as Markdown**, and paste them back.

**Copy text** and **Copy text as Markdown**, above the draft, copy the piece as
it stands, without its questions, to paste wherever it's going next. Selecting
the text by hand leaves out the paragraph and change numbers too.

```sh
python3 scripts/revision_page.py draft-r2.md          # compares with draft-r1.md beside it
python3 scripts/revision_page.py draft-r2.md --list   # the same numbered changes, as text
```

Each page is one file that works offline. Worked examples:
[a first draft](https://artefacts.rafeblandford.com/voice-first-draft-example/)
and [a revision page](https://artefacts.rafeblandford.com/voice-revision-page-example/).

## In this folder

| Path | What it is |
|---|---|
| `SKILL.md` | The instructions the agent follows |
| `references/pack/` | The voice pack: the fictional example until you replace it |
| `scripts/revision_page.py` | Builds the draft and revision page (Python 3, no dependencies) |

## Limits

- **Early version.** The evidence behind the defaults comes largely from one
  writer's work, and the controlled tests are small.
- **It can't judge what you say.** It keeps the argument yours; whether the
  argument is good is still your job.
- **Any Agent Skills client.** Plain folders in the open Agent Skills format.
  Tested in Claude Code, Codex and the Claude app.

Apache-2.0. See the [catalogue README](https://github.com/rafeblandford/skills)
for installing and provenance.
