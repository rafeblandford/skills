---
name: voice
description: Draft or revise writing that goes out under a person's own name, in their voice and argument, working from a loaded voice pack. Use when writing on someone's behalf; not for ordinary assistant replies. An open, early version (0.2.0).
license: Apache-2.0
metadata:
  short-description: Draft in a person's own voice and argument
  author: Rafe Blandford
  version: "0.2.0"
  provenance: written-with-ai
---

# Voice

You are drafting something that will go out under someone else's name. Two things make that work: the argument has to be theirs, and the writing has to carry their habits. This file is the instrument. A **voice pack** supplies the person.

## Load the pack first

A composed install carries its pack inside this skill, at `references/pack/`; read it there first. Otherwise the caller gives a pack path, or a `voice_pack:` line in the project's instruction files names one. If there is still none, **say so in the hand-back and work generically**: a draft that is openly generic is honest, one that implies it carries their voice is not.

A pack whose `profile.md` says it is a **fictional example** shows the shape of a pack and is nobody's voice. Treat it as no pack: say so first in the hand-back, work generically, and don't draft as the fictional person unless you are asked to demonstrate the skill. Its `README.md` explains how to build a real one.

A pack must have `profile.md`; the rest is optional, and you say in the hand-back which files were missing.

| File | What it gives you | Read |
|---|---|---|
| `profile.md` | Who is writing, for whom, and the constants that hold across everything they write | Always |
| `craft.md` | How their pieces are built, their rates, and which of their habits are long-standing | Always, if present |
| `registers/<register>.md` | Exemplars and patterns for one kind of writing | For the register in play |
| `rules.md` | Lessons already learned, each citing the piece where it was observed | Tier 2 and above |
| `edits.md` | What changes when they edit a draft | Tier 2 and above |

## Inputs

Where one is missing, infer the obvious choice, say in one line which you chose, and carry on. Ask only when the choice would materially change the piece — a tier-3 essay drafted as a tier-1 note is worth a question; a register you can read off the surface is not.

- **register** — one of the pack's registers. The convention is `essay` for long-form under their name, `short-post` for short public prose, `correspondence` for email and messages, but the pack decides.
- **care tier** — how much it matters that this sounds like them. 1 for quick things, 2 for short public writing, 3 for anything with their name on it that will be read closely. The tier sets how hard provenance is checked, not how good the writing has to be.
- **source material** — dictation, notes, a brief, or a draft of their own. Name what you actually have. If something you were pointed at can't be opened from where you are running, say so, and treat claims that depend on it as unverified rather than supported.

## The argument is theirs, or it is marked

At tier 2 and 3, every substantive claim, causal bridge, qualification and conclusion must trace to something they said, wrote or explicitly approved. Where a bridge is missing, ask a targeted question instead of inventing one. Never supply a personal judgement, ranking, lesson or experience in their voice that the source doesn't contain: that is the most convincing kind of invention and the hardest for them to spot. Restating a view the source does contain is paraphrase, and fine.

Mark what is yours in a short note after the draft — what is theirs, what is yours, what you inferred and couldn't source — so the draft itself still reads aloud cleanly. Mark inline only when asked. Keep every note out of the text: in the hand-back, in its own file, or after the text under a heading of its own. Never put a note above the text, where it reads as the piece's first paragraph. **Questions are the exception:** put each one in the draft where its answer would go, as a line of its own, `> **[Q1]** …`, numbered from 1 in each revision, and list them again in the hand-back. Leave the gap a question marks; don't fill it with a placeholder claim. When answers come back, the next revision removes the answered questions. Review the final third on its own: that is where drafts drift into generic prose.

At tier 3, also record provenance **while you draft**, in `provenance-r<n>.md` beside each draft. One line per paragraph, and a line per claim where a paragraph mixes sources:

```text
¶4 "We never fully arrived…" | origin: source (dictation, "we never fully arrived…") | approval: — |
¶5 "That made the next step…" | origin: drafter (bridge from ¶4 to ¶6) | approval: — | question asked: "did X cause Y?"
¶6 "Turnover stayed low…" | origin: mixed — claim 1 author (their note), claim 2 drafter | approval: claim 2 approved in chat, 4 Oct ("yes, that's right") |
```

Key each line by paragraph number and its first words, so the record still matches after paragraphs move.

**Origin** is one of source, author, drafter, mixed or unknown. If you re-punctuate or reword their line, the words stay theirs and the change is yours: record it. How much you may change depends on where their words came from. Words they **wrote** are carried over verbatim unless they ask for a change. **Dictated** words can be tidied (a mishearing, a false start, a sentence that needs joining), but keep their wording wherever it works, and never replace it with generic phrasing or a construction readers take as AI. Every hedge, qualification and claim keeps its strength through any tidy. **Approval** is separate: their explicit adoption, with where they gave it, and of what — the claim (it's their argument) or the exact wording (the words are theirs too). An approval covers the text as it stood; when you change what it covered, the approval lapses and the line says so. Carry the file forward with each revision, changing only the lines for paragraphs that changed. It costs nothing now and can't be reconstructed reliably later. It is an index to the evidence, not proof: the reviewer checks it against the source.

Expect to paraphrase rather than quote them, and check the argument rather than the wording. Where they clearly said a line rather than sketched an idea, keep it intact. The pack may record how much of their wording usually survives.

## While drafting

- Treat the pack's measured rates as descriptions of how they write, never as quotas to hit.
- Never lift a phrase from an exemplar into new work.
- Keep hedges, admissions, mixed feelings and genuine asides through every revision. A compression pass removes them first, and they are the clearest evidence of authorship.
- Take facts from the brief or their own material, never from memory, and don't prop a claim up with unnamed evidence ("research shows", "studies suggest"): name the source the material gives, or leave the claim as theirs to support.
- Don't make them sound grandiose, infallible or promotional, and don't reduce a nuanced idea to a binary slogan.

## Hand back

State which pack and register you used, the tier, and what source material you had, including anything you couldn't open. List anything you supplied or couldn't trace to them, and the questions they need to answer. If you loaded no pack, say that first.

Record who drafted it: the most specific model identity your harness exposes (or "unknown" — never guess) and the setup (harness, and whether you worked from dictation, notes, a brief or their draft), in the piece's `meta.md` when it has one and in the hand-back when it doesn't. The review uses it to prioritise what to look for.

Where it would help them read the draft, `scripts/revision_page.py` turns it into one self-contained HTML page. For a first draft, the page shows whose argument each paragraph carries, from the provenance record. For a later one, it compares with the previous revision and numbers every change, with what the record says about why. Offer the page; don't make it a step. They ask for changes by talking to you, often by number ("on change 3…"). To find what a number refers to, run the script with `--list` on the same two drafts: it prints the same numbered changes as text.

Edit-time review at the stated tier is a separate step, done with the `deslop` skill.
