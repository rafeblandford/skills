# deslop

Review a draft before it goes out under your own name. `deslop` never rewrites
unless you ask. It returns located flags, each with one proposed edit or a
question, and ends with a Decision column for you: accept, keep the original, or
revise differently. It reviews anything, from a two-line reply to an essay,
whether or not its partner skill [`voice`](../voice/) drafted it.

[Read the website guide](https://rafeblandford.com/voice-and-deslop/) ·
[Read the launch article](https://rafeblandford.com/writing-with-ai-in-my-own-voice/) ·
[See the examples](https://github.com/rafeblandford/skills/tree/main/examples/deslop) ·
[Install](https://github.com/rafeblandford/skills#installing)

## Before you start: build your own voice pack

Some of `deslop` works without a pack: the AI residue and the tells lists. To
review as you (what's yours, what's long-standing in your writing, what you've
changed before), it needs a **voice pack** built from your own writing. This
skill ships with a **fictional example pack** at `references/pack/` (a civil
engineer writing about infrastructure) to show the shape. It's nobody's voice:
`deslop` says so and reviews generically until you give it your own.

The guide to building your own is
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
reviews generically, without judging anything against your voice.

A pack can quote your correspondence and your unpublished work, so keep it
private.

## What it does

It asks two separate questions:

- **Is the argument yours?** Every claim traces to your material or your
  approval, or it becomes a question.
- **Might a reader take this as AI?** Constructions on the current editorial
  lists of AI tells, raised as candidates, never as verdicts.

It sets its depth by a **tier**: how much it matters that the piece sounds like
you.

| Tier | Typical pieces | `deslop` |
|---|---|---|
| 1 | Quick email, replies | AI residue only; no pack needed |
| 2 | Short public posts, internal documents | Adds the tells list and your pack |
| 3 | Essays, talks, anything read closely | Checks every claim against your source |

Say the tier, and what you wrote yourself, when you ask. Words you wrote or
approved are never cut or replaced: at most they get a *their call* note.

## The decision page

`scripts/decision_page.py` turns a review into a single page you open in a
browser. The draft sits on one side and its flags on the other. Each flag is
highlighted where it sits in the text: pick a flag and the draft scrolls to it,
click the text and its flag comes up. Accepting a proposed edit shows the new
wording in place.

When the page appears depends on the care tier. At tier 2 and 3 it is built
and shown with every review you're handed back, without asking (a review with
no flags has nothing to decide, so it gets none); at tier 1 it is offered in
one line. Asking for it ("show me the decision page") always builds it.

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

You don't edit on the page. Choose an answer for each flag (a note on a flag
you leave undecided counts as a revision), use **Copy as Markdown**, and paste
the result back to the assistant, which makes the changes.

**Copy text** and **Copy text as Markdown**, above the draft, copy it as it
stands with the edits you've accepted, to paste wherever it's going next.
Selecting the text by hand leaves out the paragraph numbers and flag tags too.

```sh
python3 scripts/decision_page.py render deslop-r1.md --draft draft-r1.md   # the page
python3 scripts/decision_page.py record pasted.md --review deslop-r1.md   # decisions-r1.md, with counts
```

Each page is one file that works offline. Worked example:
[a decision page](https://artefacts.rafeblandford.com/deslop-decision-page-example/).

## In this folder

| Path | What it is |
|---|---|
| `SKILL.md` | The instructions the agent follows |
| `references/residue.md`, `references/tells.md` | Common AI residue and lists of AI tells, the same for everyone |
| `references/comparative-read.md` | For passages the lists can't settle |
| `references/flags-block.md` | The format of the flags block a review ends with |
| `references/upstream/` | Pinned copies of the humanizer and stop-slop material, with their licences |
| `references/pack/` | The voice pack: the fictional example until you replace it |
| `scripts/decision_page.py` | Builds the decision page and records decisions (Python 3, no dependencies) |

## Limits

- **Early version.** The evidence behind the defaults comes largely from one
  writer's work, and the controlled tests are small. Treat the tells as
  editorial heuristics, not measurements of readers.
- **Not an AI detector.** It never asks whether text "reads human"; it asks
  whether the argument is yours and whether a construction is one readers
  notice.
- **Reviews vary run to run.** Every proposal lands in the Decision column, so
  nothing changes without you.

Apache-2.0. `deslop` draws on, and credits, humanizer and stop-slop (pinned
copies, MIT) and other community lists; see `references/tells.md` and the
[website guide](https://rafeblandford.com/voice-and-deslop/) for the full
credits.
