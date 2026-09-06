# RafeOS People — edited working conversation

This is the substantive human–AI conversation that led to the public example.
It is lightly edited for readability: automatic environment text, hidden
instructions, tool calls, repetitive production updates and local paths are
omitted. Obvious speech-recognition errors are corrected. The product argument,
human choices, direction checkpoint and revision requests are retained.

The private Cockpit screenshot used as a host-product reference is not
reproduced. Its role is described where relevant.

## 1. Explore the idea before invoking the skill

**Rafe**

> I want to have a conversation about a product idea that I'm thinking about.
> I'm then going to use the Product Idea Pack to create some artefacts of that,
> but I don't want to use that skill until I say I'm ready to do so.

**Codex**

> Let’s talk it through. I’ll hold off on the Product Idea Pack skill until you
> explicitly say you’re ready. What’s the idea, and what prompted it?

Rafe then described a people module for RafeOS. Previous personal CRM products
had been too much work to maintain. His alternative was a concise, curated
people memory assembled from authorised email, messaging, meeting notes and
agent conversations. It would preserve contact routes, relationship context,
important interactions, provenance, confidence and access tiers while linking
back to the underlying evidence.

Most supported updates could happen automatically. New people, ambiguous
identity matches and consequential interpretations would come back to Rafe for
graduation or correction. The record would be readable Markdown, but its main
job would be to give authorised agents shared context.

**Codex**

> I’d frame this as **a shared people memory for RafeOS**: a maintained
> understanding of who someone is, your relationship with them, and where to
> find the relevant history. Every agent you use could start with that context.
>
> I can see four jobs within the idea:
>
> - **Recognise someone:** connect a name, email address and messaging
>   identities to the same person, while handling ambiguity.
> - **Remember the relationship:** retain useful background, significant
>   interactions and your own observations.
> - **Find the evidence:** give agents routes into the underlying emails, notes
>   and messages when a summary is insufficient.
> - **Help you act:** prepare for a conversation, draft something appropriately,
>   retrieve a commitment or surface a reason to reconnect.
>
> What would make this feel most valuable first: agents reliably knowing who
> you mean and remembering the context, or RafeOS actively helping you maintain
> relationships?

**Rafe**

> Both are important use cases, but they have different outcomes. Agents
> knowing who people are and remembering the context is going to be powerful
> day to day. As the database grows, I think it will also become much more
> active in helping maintain relationships: a reason to reconnect rather than
> just passive memory. Both sides are important, even if we have to represent
> them as two separate ideas.

**Codex**

> I’d keep them as **two explicit promises within one product**, sharing the
> same people memory:
>
> - **Context when you need it:** help me understand, remember and work with
>   this person.
> - **Attention when it matters:** notice when there’s a worthwhile reason for
>   me to act.
>
> The extra ingredient is **your intention for the relationship**. More history
> can help the system understand someone, but it does not establish whether you
> want to become closer, keep an occasional connection or simply retain useful
> context.

**Rafe**

> There are obvious things, like birthdays or when I promised an action and
> haven't followed up—for example agreeing to meet for dinner but not setting a
> date. It might notice that I haven't been in contact for a while and compare
> that with my intention for the relationship. You meet someone and realise
> you haven't seen them for six months or even a couple of years, then say,
> “Let's make sure we meet again sooner next time.” There is both a professional
> and a personal social side. I wonder whether they work together.

**Codex**

> They work together because the underlying need is the same: **help me give
> relationships the attention I intend to give them**. The meaning of that
> attention changes between people and situations.
>
> Three useful prompts emerge:
>
> - an occasion, such as a birthday;
> - an unfinished intention, such as the unarranged dinner;
> - a relationship drifting beyond your wishes, expressed as “the last contact
>   I have recorded”, because digital history will always be incomplete.
>
> The experience should feel warm and forgiving. Suggestions should remain
> suggestions rather than turning relationships into overdue tasks.

## 2. Place it in RafeOS

**Rafe**

> The natural places for nudges are a combination of the daily briefing in
> Cockpit and, when they need to be more prominent, a message from RafeOS on
> WhatsApp. It should also be possible to ask what I am due to catch up on in
> Codex or Claude Cowork. That could be a weekly or fortnightly habit covering
> nudges and curation, probably supported by a scheduled task.

Rafe supplied a private Cockpit screenshot so the later concept could borrow
the structure of the existing briefing without reproducing its personal data.

**Codex**

> I’d give the three surfaces distinct roles:
>
> - **Cockpit: everyday awareness.** A small number of relevant suggestions
>   woven into the wider briefing.
> - **WhatsApp: something worth bringing to you.** Timely prompts where waiting
>   would reduce their usefulness. Silence alone is not a reason to escalate.
> - **Codex or Claude Cowork: a conversational people review.** Ask what needs
>   attention and work through suggestions, commitments and curation.
>
> The review should put relationships first and housekeeping second. Its depth
> can follow the time you have available. The scheduled process prepares the
> review; human graduation and ambiguous judgements happen when you join in.
>
> One essential behaviour is shared memory of your response. If you say “We met
> last weekend”, Cockpit, WhatsApp and the next review should all reflect it.

**Rafe**

> The richer version is good because it can happen when I have time.

**Codex**

> Imagine a review exchange:
>
> **RafeOS:** You mentioned wanting to see Anna more often. Shall we pick up the
> dinner idea?
>
> **You:** We actually met on Saturday. She’s starting a new job next month.
>
> **RafeOS:** I’ll record the catch-up. Would you like a reminder to ask how the
> new job is going?
>
> One exchange updates the history, adds context and captures your intention.
> Missing a review should not stop supported updates or useful nudges.

## 3. Establish a neutral example and trust rules

**Codex**

> Let’s use **Anna Mercer, a fictional former colleague who has become a
> friend**. She lets us explore professional and personal context in one record.
>
> Her concise page can contain identity and contact routes, relationship,
> explicitly stated intention, current context, meaningful contact, linked
> commitments, useful history and restricted context. Each meaningful assertion
> retains its source and date; deeper history remains in its original systems.
>
> Three rules should be firm:
>
> - keep observation and interpretation distinct;
> - enforce access restrictions when information is retrieved;
> - keep relationship intention under human control.

**Rafe**

> This matches how I see it working and is a good neutral example—not based on
> anyone real.

**Codex**

> The concept is now defined enough for a first Product Idea Pack. We have two
> clear outcomes, the maintenance process, privacy principles and three places
> to interact with it.
>
> The strongest story is that **ordinary activity builds the memory,
> occasional conversation improves it, and that memory helps you give people
> the attention you intended**.

**Rafe**

> We can use the skill now.

## 4. Direction checkpoint and Draft 1

**Codex**

> I’ll make three formats: a proposition sketch, a mechanism board and a
> product storyboard. The storyboard will be the main feedback target, with
> separate views of everyday agent assistance and the richer people review.
>
> The proposition is **“Remember the context. Make time for people.”** The three
> beats are **Gather useful context → Curate a trusted memory → Help at the
> right moment**.
>
> The question across the pack is: **“When should RafeOS prompt you, and when
> should it wait?”** These are discussion drafts; connector availability and
> privacy enforcement remain implementation questions.

Codex produced four Draft 1 boards: a proposition sketch, mechanism board,
everyday-assistance storyboard and people-review storyboard. It performed
rendering and layout checks before delivery. The people review was identified
as the primary feedback target.

## 5. Human-directed revision

**Rafe**

> Draft 1 works well overall, but Anna would probably be one of multiple nudges
> in the wider RafeOS briefing. The everyday-assistance board should use a
> recognisable Codex or Claude Cowork-style surface to make the context real.
>
> The mechanism is largely correct. Align the source markers, and show that the
> scoped people API can support everyday agent context, relationship support
> and other use cases still to be determined.
>
> The proposition sketch currently has more sketch than information. The phone
> is the weakest part and its style does not fit. Improve the product concept
> without losing the human situation.

**Codex**

> I’ll make Draft 2 with Anna’s nudge inside a broader Cockpit briefing, a
> recognisable assistant setting, an API branch for future uses, and a clearer
> phone moment in the sketch. I’ll preserve Draft 1 and keep the agreed product
> model and fictional example fixed.

**Rafe**

> It might also be worth creating a separate board with things that feel like
> real mock-ups, sitting inside native product UX, to give the idea an “as if it
> had been created” artefact.

Codex added the native-product preview to Draft 2 and exposed its Cockpit,
Codex-style and WhatsApp surfaces separately. It checked the five revised boards
and preserved all Draft 1 artefacts.

## 6. Packaging and design hand-off

**Rafe**

> I’d also like a PDF pack and a Figma-ready design hand-off. Perhaps we could
> have a cover using the new product mock-ups in real devices with a London
> photo background.

**Codex**

> I’ll create a PDF pack and Figma-ready hand-off from Draft 2. The PDF will
> contain the cover followed by the five approved boards. The hand-off will
> include editable SVG boards and the three separate product mock-ups. I’ll
> also check them in Figma itself so import problems can be recorded.

The resulting PDF retained searchable text and vector diagrams. All six pages
and three independent product surfaces were imported into Figma. The destination
check found controlled font substitutions and a few missing decorative text
chevrons; these were recorded rather than described as pixel-identical fidelity.

## What the conversation changed

The first fifteen minutes did not merely add detail to a predetermined screen.
They separated two related outcomes, established the role of human intention,
defined three surfaces, identified the decisive correction and made trust
boundaries part of the proposition. The later human critique changed the visual
emphasis and product credibility without restarting the concept.
