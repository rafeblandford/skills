# Tells: constructions often read as AI

The perception lens: editorial heuristics, not measurements of readers. Each entry gives a tell, how to spot it, how strong it is, and what the evidence is. It draws on community editorial lists — `humanizer` 3.1.0 (built on Wikipedia's "Signs of AI writing"), `stop-slop`, the Vale rule packs `jdkato/voices`, `tbhb/vale-ai-tells` and `JMill/deslop`, `petergyang/no-ai-slop`, Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) page as revised to 3 October 2026 (paraphrased and credited; Wikipedia text is licensed CC BY-SA 4.0) — and on a small controlled test. The first two lists are pinned in `upstream/` for licence and comparison; they are not read in a review.

Provenance, whether a claim is the author's at all, is not here: it is the first check in `SKILL.md`, and the most important. **What this author does is in their pack, not here**: their rates and which of their habits are long-standing in `craft.md`, their edits in `edits.md`. Where a tell appears in the author's own words, `SKILL.md` §3 decides how to raise it.

## How to read an entry

- **Strength 1**: one sighting is worth a proposed edit in drafted text. **2**: an edit only when two or more tells share a passage. In the author's own words no strength earns an edit; a known tell there can earn one *their call* note (`SKILL.md` §3). **A**: an absence; the proposal is to restore something from the source or to ask, never to invent.
- **Weigh by rarity.** A tell counts in proportion to how rarely a careful writer would make the choice on purpose (`humanizer`).
- **Every sentence should add something** the reader didn't already have, and no proposed edit may add or drop a fact, name, number, date, quotation or claim (`humanizer`).

**The evidence is thin, and says so.** The controlled test is one brief given to four Claude models (claude-fable-5-1, -opus-5-5, -sonnet-5-5, haiku-4-5), two essays and two short posts each, 4 October 2026: enough to see that a pattern recurs, not how common it is or whether it generalises. An independent review the same day corrected several earlier claims; what remains is labelled. "Exploratory" means counted by a simple candidate-finder whose matches haven't all been read; treat the rate as a pointer. Pair evidence comes from one author's edits of model drafts.

---

## 1. Seen in all four models in the test

**Choppy sentences.** Mean sentence length well below the author's register (the pack's `craft.md`), with a third or more of sentences at eight words or fewer.
- Strength 1, judged over the whole piece, never passage by passage: it is not a second tell that lets a lone strength-2 tell in a passage earn an edit. The repair is usually joining clauses.
- Essays averaged 11.4 (Haiku), 12.8 (Opus), 13.5 (Sonnet) and 14.5 (Fable) words a sentence, and stayed short with headings and list markers removed; older Opus 4.6 drafts and AI-authored site posts were similar. Fewer commas per sentence too (0.4–0.8; compare with the author's own prose in the pack; exploratory). Drafting from dictation rather than a brief produced longer sentences in one Fable chain, so source material may matter as well as model. A dependency parse (5 October) shows what the shortness is: about half of the model drafts' sentences were a single clause, where careful human prose in the same registers runs nearer a third, so reasoning that belongs inside one sentence gets split across several. With a voice guide and a pack loaded, essays reached the author's clause depth and short posts only part of the way: check short posts hardest.

**Restating closing lines.** A paragraph or section that ends on a short sentence restating what it just showed ("Snags are the user research."), including the paired form: two blunt sentences after a long one.
- Strength 1 when it restates; 2 when it adds a fact. Shortness alone isn't the tell; judge what the line does. Exploratory count; `humanizer` §2; repeatedly cut in one author's review.

**Split contrast: "X is not A. It is B."** Also "The question is not whether… It is whether…" and "not because X, but because Y".
- Strength 2. Listed as an AI construction by several editorial guides (`humanizer` §1, `stop-slop`, Wikipedia), and also used by human writers; in the test Haiku 4.5 produced far more candidates than the other models. In text that isn't the author's, propose a plain statement **of the same claim**: if the claim is itself a negation ("the hard part was never the method"), it stays a negation said plainly ("the method was never the hard part"), never swapped for a positive claim ("the hard part was trust") unless they say that is what they mean; in theirs, it is *their call* with a perception note. Exploratory count. The clipped ", not Y" ("more important, not less") is a weaker case: question only whether the author said something softer.

**Few asides.** Model essays carried few parentheses (0.4–1.6 per 1,000 words, counting every bracket). Strength A: restore an aside the source contains; never write one.

**At one remove.** The draft reports what happened rather than what the author thought: less first-person singular than the author's own prose in every model's essays. Strength A, and only as a question: the fix is their view, asked for.

## 1b. Seen in a second test, with a voice guide loaded

A second small test: the same brief and the same four models, re-run on 5 October 2026 with `voice` and an author pack loaded (two essays and two short posts each, sixteen drafts), and measured against the author's own registers with committed code. The guide closed some gaps and left others; these are the ones it left, or opened. The method and the literature behind each measure (Hyland's metadiscourse, Lu's clause counts, Biber's registers) are explained in the essay that accompanies the release, <https://rafeblandford.com/writing-with-ai-in-my-own-voice/>.

**Qualification stripped out.** Fewer contrastive and trade-off markers ("but", "however", "although", "in practice", "for now") than the author's own prose, with or without a voice guide: claims arrive without the scope the author would give them. Strength A: restore a qualification the source contains, or ask whether the claim needs one; never write one. Contrast as such is not a tell; the split-contrast entry in §1 is one construction, not contrast in general.

**Under-commitment.** Hedges without boosters: the drafts softened claims but almost never committed to one, and in short posts carried no boosters at all. Strength A, and only as a question: ask whether the author holds the view firmly; never add certainty to a claim.

**Unsourced evidence phrases.** "Research shows", "studies suggest", "the evidence is clear", "data tells us". A provenance flag, strength 1 in drafted text: name the source from the material, or ask for it; if there isn't one, the claim is the author's to make or drop. Related to false agency (§2). *Evidence: borrowed from the community lists, not observed in the tests.* Unnamed evidence was all but absent in both same-brief runs, with or without a voice guide; what rose with the guide was **named** attribution ("X argues", "Y found"), which is good practice, not a tell. An earlier version of this entry misread that rise.

**Reader address and instructions in essays.** "You", "your" and imperative openings at two to three times the author's essay rate without a guide, and still well above it with one. **Essays only**: reader address is normal in email and short posts, and the author's own rates there are high. Strength 2. In the author's own words it is *their call*.

Not tells, though the test measured them: sentence-length variation (the drafts varied *more* than the author), one-sentence paragraphs (the drafts had fewer), and first person (low by design: a voice guide that won't invent leaves those places as questions).

## 2. From single-piece review

Seen in one author's tier-3 reviews of a Fable 5.1 draft, and on the community lists; not tested across models.

- **Drafter's framing and forward references.** "This post is about…", "and I'll come back to that", a tidy line restating the test just applied. Strength 1; `humanizer` §25.
- **Mannered phrasing.** A figure of speech where a literal phrase was available: "earns its keep", "dressed as". Strength 1, unless it's the author's own image. Anthropic's guidance, quoted in `residue.md`.
- **Repetition from assembly.** The same uncommon word in neighbouring sentences, a lesson restated twenty lines apart, a cluster of honesty markers. Strength 2: one flag each.
- **False agency.** Inanimate things doing what people did: "the data tells us". Name the actor. Strength 2; `stop-slop`.

## 3. Seen in some models in the test

Use these to decide what to look for first when the drafting model is known; never to decide whether a claim is supported.

| Tell | Seen in | Not seen in | Evidence | Strength |
|---|---|---|---|---|
| **Em dashes**, especially two or more in one paragraph | Haiku 4.5 (all four drafts); older Opus 4.6 and 4.8; Codex | Fable 5.1, Opus 5.5, Sonnet 5.5 (none in twelve drafts) | Measured in the test. Vendor data puts GPT-4.1 high and Gemini 2.5 Pro low (vendor claim). A corpus-level signal, not a per-document one (Czuma 2026) | 1 for a cluster in one paragraph of drafted text; otherwise judge against the author's register in the pack, as context, not a quota |
| **Questions the text answers itself** | Fable 5.1, Haiku 4.5, Sonnet 5.5 (once, as bold headings) | Opus 5.5 rarely | Exploratory, checked by reading; `humanizer` §5 | 2 |
| **Bold in prose or as labels** | Sonnet 5.5 (both essays), Opus 5.5 (one) | Fable 5.1, Haiku 4.5; no posts | Measured; `humanizer` §19 | 1 for decorative bold in prose |
| **Negative listing** ("Not a X. Not a Y. A Z.") | Haiku 4.5 | The other three | Measured; `stop-slop` | 1 |
| **"No + noun" lists** ("no ceremony, no handover, no owner") | Haiku 4.5, Fable 5.1 | Sonnet 5.5 | Exploratory: a "no + word" candidate count, not negation in general; `tbhb/vale-ai-tells` | 2 |
| **American spelling** where the pack sets British (*organizational*, *gotten*) | Haiku 4.5 (verified examples) | Not confirmed elsewhere | Wikipedia: models default to American English. Some -ize forms are acceptable British spelling | 1 |
| **Explicit "not X but Y" / "not just X"** | Older Opus 4.8 drafts (from one author's revision pairs) | Low in all four current models | Pairs only | 2 |

## 4. Rare in the test, but readers know them

Rare or absent in the sixteen drafts. Readers still notice them, so check cheaply. The Claude models in that small test rarely produced them; other models, and later versions, may.

- Most of the vocabulary list (`humanizer` §12: *delve, tapestry, testament, pivotal, crucial, robust, showcase…*). "Leverage" appeared often, but because the brief cited a source that uses it: a word the source material uses isn't a tell.
- Inflated significance (§13), shallow -ing riders (§15), "serves as / stands as" (§18), sayings that sound deep (§3), staged openers such as "Here's the thing" (§4), chatbot residue (§22).
- From the newer lists: "that X is the point" verdicts, staged questions ("The result?"), "what nobody talks about" setups, counting before a list ("Three things changed."), announced precision ("I want to be precise"), narrow mannered verbs ("sits at the intersection of").

The population studies behind the vocabulary list (Kobak et al., *Science Advances* 2025) are sound, but corpus-level and about 2023–24 models.

## 5. Published tells not used as counted rules

Each has real evidence behind it. None fires on a count here, for the reason given; several are still worth a reader's eye when a passage already reads as drafted.

| Tell | Source | Why not a counted rule |
|---|---|---|
| Present participial clauses at 2–5× the human rate; nominalisations at 1.5–2× | Reinhart et al., *PNAS* 2025 | Plausible, and the study is careful. Not tested reliably here: a regex is a crude proxy for a grammatical feature, and the authors warn that it transfers poorly across registers |
| Lexical diversity shifting after AI editing | Shan, Lee & Hao, EMNLP 2026 | No movement in a crude local proxy; not a per-draft signal |
| One opener above 30%; sentence or paragraph variance below a fixed CV | `tbhb/vale-ai-tells` | Thresholds calibrated on technical documentation; silent on the choppiest drafts here |
| No em dashes, ever | `humanizer` §8, `stop-slop` | Wrong for most human writers; use the cluster signal (§3), with the author's register as context |
| Forced triads | `humanizer` §6 | A real tell when the three items aren't distinct: check that, don't count |
| "X rather than Y" | `humanizer` §1, `tbhb/vale-ai-tells` | A plain construction; flag only where it stages a contrast nobody holds |
| Borrowed-rigour vocabulary (*load-bearing, forcing function, first-order*) | `JMill/deslop`, `petergyang/no-ai-slop` | Not tested reliably; common in professional prose. A cluster may still read as AI |
| Colon reveals (a clause, a colon, then the point) | `humanizer` (staging) | They also occur in human prose, and the candidate counter can't tell a reveal from an ordinary colon; not a reliable discriminator. Several in a short passage may still read as staged |
| Long sentences chained with "and" | The Economist, July 2026 | Current Claude models wrote short sentences in the test |
| Hedge bans, "in order to", synonym cycling, single formal transitions, passive-voice density | Various | Hedges are a sign of human writing (Wikipedia agrees); the rest are historical or fire on careful prose |

## 6. Borrowed, not yet measured

Kept for breadth at tier 3, credible on their source's word.

- **Writing for the wrong reader** (`humanizer` §26): a reply that re-explains what the reader knows and puts the decision last. Most useful in correspondence.
- **Stacked qualifiers** (§9), as distinct from one hedge that scopes a claim.
- **Vague association** (§14): "linked to" where the source says how. **Borrowed authority** (§17): "experts argue".
- **Grading tails** (`JMill/deslop`): a clause tacked on to grade what was just said, such as "…, a distinction the old model never made".
- **The 2026 disclaimer form** (Wikipedia): "should be treated as X rather than Y".
- **Hyphenated pairs after the noun** (§10), **repeated sentence openings** (§7), **knowledge-limit disclaimers** (§23), **a heading repeated in the first sentence** (§24).

---

Review by **2027-01-04**, or when the drafting model changes. A tell that stops appearing moves to §4; one that appears in a new model goes in §3 with the model named. How to re-run the test is in the repository's developer notes, not here.
