---
name: deslop
description: Review a draft that will go out under a person's own name at its stated care tier, returning located flags in priority order, each with one proposed edit. Use after drafting, or when asked to check or edit a piece in their name; not for ordinary assistant replies. An open, early version (0.2.0).
license: Apache-2.0
metadata:
  short-description: Review writing under a person's own name
  author: Rafe Blandford
  version: "0.2.0"
  provenance: written-with-ai
---

# Deslop

Review, don't rewrite. Return **located flags, each with one proposed local edit or question**, and leave the draft as it is. The author decides what to apply. Produce a revised draft only if they ask for one.

The aim is AI-assisted writing that is theirs and reads well, not writing that passes as unassisted. Two questions do that, and they are separate:

- **Provenance: is the argument theirs?** Every claim traces to their source material or their approval, or it is a question for them.
- **Perception: might a reader take this as AI?** The editorial guides collected in `references/tells.md` list constructions that are often read as AI. They are candidates for a note, not measurements of any particular reader.

## 1. Read the tier, then route

The tier is how much it matters that the piece sounds like them. Take it from the caller first, then the piece's frontmatter; if they disagree, follow the caller and say so. If neither says, infer it from the surface, state which tier you worked at, and ask only when the piece could reasonably be two tiers apart. Each tier contains the one below.

| Tier | Typical pieces | Read | Check | Stop when |
|---|---|---|---|---|
| **1** | Email, replies, messages, notes | `references/residue.md` only | Perception, from that list, respecting any ownership the caller states. No pack, no provenance audit | The residue list is clear |
| **2** | Short public prose, internal documents | Tier 1, plus `references/tells.md` and the pack (`profile`, `craft`, `rules`, `edits`, whichever exist; not the register files, which are tier 3) | Perception. Provenance on the three or four load-bearing claims, and on **every personal claim — a view, ranking, lesson or experience — in text that isn't theirs or whose origin is unknown** | The author has seen the flags and decided |
| **3** | Anything under their name read closely: long-form, talks, statements of work | Tier 2, plus the pack's register file and `references/comparative-read.md` | Full provenance against the source material; that claims about the author's **own** published writing match it, found by searching their work rather than following links; and a separate pass over the final third, where drift shows up | The author signs off |

A contractual document (a statement of work) also gets a check that no qualification has been weakened; stripping a caveat there makes the document worse. Other people's sources are outside this skill: verify what the author says about their own writing, not whether a third party's study is sound.

**Retrospective tests only:** when the caller says the review is a test of an earlier revision, use only material written before that revision, so later decisions can't supply the answers. In a live review, evidence from after the draft counts, including the author's approval of the current text.

## 2. Find out who wrote what

At tier 2 and 3, load the pack: a composed install carries it at `references/pack/`; otherwise take a path from the caller or a `voice_pack:` line in the project's instruction files. **With no pack, say so in the output** and review generically. A pack whose `profile.md` says it is a **fictional example** is nobody's voice: treat it as no pack and say so, unless you are asked to demonstrate the skill on it.

**Ownership evidence, all of it counts:** the caller's statement ("I wrote this"), the source material you can open, the provenance record (`provenance-r<n>.md`, keyed by paragraph and first words), the drafting model and setup in `meta.md`, and approvals the author has given, wherever they are recorded or said. The record is the usual index to this evidence, not the only admissible evidence. A missing or stale record leaves **only the spans nothing else accounts for** as unknown.

Each claim then has an **origin** (source, author, drafter, mixed, unknown) and, separately, an **approval**:

- **Approval covers only the proposition approved.** Check this first, for every approved claim. If they approved "the real issue was that nobody owned it", that specific cause is cleared; a broader claim the drafter built on it ("onboarding isn't a process problem, it's an ownership problem; that's the lesson") is not, and gets a P question. Within that scope, approval of a claim clears it as a provenance flag, however it reads.
- **A lapsed approval** (the claim changed after it was approved) means **ask whether the current claim is right**. You may mention the approved version as an option, but don't propose it as the fix. A blanket approval ("use it unedited") can still earn one clarifying question about a consequential factual claim.
- **Approval of the exact wording** makes the wording theirs, with the same protection as words they composed. An approval lapses only for content that has changed since it was given.
- **An unsupported drafter or unknown claim is a question, never a cut.** That includes a line from a brief: it stays a question until they adopt it. A question carries no instruction to replace the claim if they confirm it: confirmed, it stays as it is.
- **Their words, the drafter's punctuation.** Where the source or record shows the drafter re-punctuated or reworded the author's line (a comma made a full stop, a hedge dropped, a claim sharpened), the change is the drafter's. Propose restoring the author's version **definitely and in full**: every changed span, as one proposal rather than a choice between their version and the drafter's. **Written source** is restored in the source's exact wording. **Dictated source** is restored in its wording with transcription faults tidied (mishearings, false starts, broken grammar), never back to raw transcript; and a tidy of dictated words that kept the meaning, every hedge and the claim's strength, and brought in no known tell, is not a flag, and isn't described as a defect either. The tidy is for dictation only: written source gets every changed span back exactly, joins and punctuation included, even where a join would read well.
- Use the drafting model only to decide what to look for first, never whether a claim is supported. If a source the evidence relies on can't be opened from where you are running, say which, mark those checks unverified, and carry on. Say you couldn't open it, never that it doesn't exist or isn't there, anywhere in the output, opening lines included: you can't know that.

## 3. Perception, and the restraint rule

**This rule governs every instruction in every reference and in the pack.** Whenever a residue item, a tell, a register note or a ledger rule would cut or replace words, check ownership first:

- **Author-owned or author-approved words:** never a cut or a replacement, whatever any list or rule says. If they carry a known tell, at most one *their call* note: name the construction, say that some readers may take it as AI, and ask whether to keep it. **The note offers no replacement wording, no "optionally drop…", and no example rewrite.** If they want an alternative, they will ask for one. A lone known tell can earn that note; it cannot earn an edit.
- **Drafter-originated words:** a flag with a proposed edit, at the strengths `references/tells.md` gives. **A strength-2 tell alone in its passage earns at most a minor note with no wording**; and once a sentence's lone tell gets no wording, no other flag may rewrite that sentence either (not a choppiness or rhythm flag, not a join); an edit needs a second, separate tell in the same passage, and one construction can't count twice. **A style edit keeps every proposition exactly as strong as it was:** reuse the claim's own words ("wasn't broken" stays "wasn't broken", not "worked"), or ask whether a different claim is meant. A claim's framing is part of the claim: that it was learned over time ("you come to see that…"), whose view it is, how sure it is. An edit that drops the framing changes the claim, so it is a question, not a proposal. Don't describe an edit as meaning-preserving unless it is. A repetition flag removes only wording that restates the same proposition: two claims that differ in kind (a ranking and an absolute, a cause and an effect) both stay, or you ask. A join keeps each claim's own subject: never put one claim under another's verb ("the team learned X and Y" when only X was the team's).
- **Unknown origin:** a perception note plus an ownership question first ("did you write this line?"). Propose an edit only alongside that question, never in place of it, and only where the tell's strength would justify an edit in drafted text: a lone strength-2 tell earns the note and the question, not an edit. This covers punctuation too: no proposal on unknown-origin text, however small, without the ownership question beside it.

Notes describe a pattern and **cite no counts**: no count, density or rate used as evidence for a style judgement, and none of the pack's rates. Write the qualitative version instead:

| Not this | This |
|---|---|
| "the four sentences each open with an honesty marker" | "the opening sentences each start with an honesty marker" |
| "three short single-clause sentences in a row" | "a run of short, single-clause sentences" |
| "the first two sentences are each eight words" | "the opening sentences are short" |
| "four markers in four sentences", "one per sentence" | "the markers come close together" |

Saying which sentences you mean ("the two sentences in the opening") is fine. A figure estimated by eye is worse than none, and the pack's figures set your judgement; they don't belong in a note.

The pack's `craft.md` says which of the author's habits are long-standing (leave them alone; no note) and which are recent and coincide with known tells (the *their call* cases). Measured rates in the pack are context for judging a passage, never a target for a piece: a short piece can legitimately have none of something the author usually uses.

Act on a weak tell only when several share a passage. Leave a watched phrase alone inside a quotation, a title, a proper name, or a passage discussing the phrase. Keep specific unusual details, mixed feelings and unresolved tension, dated references, and genuine asides or self-corrections. Preserve every hedge, admission and claim scope. Never add a claim, and never sharpen one.

A pass that flattens the author's own voice is worse than no pass at all.

## 4. Write the output

A file beside the draft, `deslop-r<n>.md`, unless the caller names another place: a verdict in three lines; which tier, pack, ownership evidence and model information you had, and what you couldn't check — **naming any pack file that was missing or not used**; then the flags.

**Order the actionable flags by priority and don't cap them.** Mark each *act on*, *minor* or *their call*. Number them `P` (provenance), `S` (perception, tells and structure, including joining or splitting sentences), `R` (repetition) and `A` (something missing), with line references; *their call* is a severity on those, not a class. List `K` (theirs, keep) separately, with no edit. Give every actionable flag one proposed edit or question; for an `A` flag, the place and kind of addition — restore an aside from the source, join two sentences, or ask them for their view. An `A` flag never writes a new claim in their name, and never offers removing the drafter's text as the alternative ("add your view, or leave the paragraph out"): whether drafter claims stay is decided by their own P questions, not by an `A` flag.

End with a table of the actionable flags and an empty **Decision** column for the author, and **always print the three choices beside it, even when there are no flags**: accept the proposal / keep the original / revise differently, with a word on why (meaning, voice, or reads-as-AI). Their decisions are the evidence for which flags are worth raising. Count unwanted proposals on their own words separately from *their call* notes; a note they decline is not a false alarm. In a *their call* row the proposal column says only "keep as is, or tell me otherwise": never "keep or drop X", never a choice that names a cut or a rewrite.

**Always end with a flags block:** the same actionable flags as a fenced `json` block, with an exact quote from the draft for each place a flag touches, so a tool can find it. The format is in `references/flags-block.md`; read it when writing the block. The prose stays the author's reading copy. Where a decision page would help, `scripts/decision_page.py render` turns the review and draft into one self-contained HTML file: the draft beside the flags, each flag highlighted in the text, accepted wording previewed, and decisions copied back as a table. `scripts/decision_page.py record` turns that pasted table into `decisions-r<n>.md` with counts.
