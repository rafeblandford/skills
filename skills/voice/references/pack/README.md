# This is a fictional example pack

The `voice` and `deslop` skills are a generic instrument. Everything about the writer lives in a separate **voice pack**. The pack in this folder belongs to an invented civil engineer, so you can see the shape a pack takes. It is nobody's voice, and both skills treat it as no pack unless you ask them to demonstrate on it.

To have the skills write and review as you, replace it with a pack built from your own writing.

## What a pack holds

```text
references/pack/
  profile.md              who is writing, and the constants, each with its edge
  craft.md                how their pieces are built, with measured rates and their sample
  registers/<name>.md     exemplars and notes for each kind of writing they do
  rules.md                lessons from past pieces, each citing where it was observed
  edits.md                what they change when they edit a draft
```

Only `profile.md` is required. The skills say which files they couldn't find.

## Building your own

1. **Collect writing that is unmistakably yours.** Published pieces you wrote without AI help, and your own sent email if you're comfortable with it staying private on your machine. Label each piece: date, where it appeared, and whether AI was involved. Only unassisted writing counts as evidence of your voice; assisted pieces are useful as contrast.
2. **Pick your registers.** Name them by form, not platform: `essay`, `short-post`, `correspondence` are the usual three. For each, choose two or three exemplars of 100–250 words and quote them exactly. The tier-3 comparative read in `deslop` needs at least two per register.
3. **Write the profile.** Who you are, who you write for, and a handful of constants: habits that hold across everything you write. Pair each with the failure that imitates it. That right-hand column is what makes the pack useful, because a drafter copying a habit usually produces the imitation.
4. **Measure, don't guess.** Rates in `craft.md` (sentence length, punctuation, how often you qualify or contrast) should come from counting your own writing, with the sample size beside each one. Read what a measure actually counts before you trust it. Rates describe you; they are never targets.
5. **Start the ledger from real edits.** Each time you change a draft, note what you cut or restored and why, citing the piece. One sighting is `weak`; a rule that holds more than once is `established`.
6. **If you can, compare drafts with what you published.** Pairs of draft and final text show what you reliably change. Hold a few pairs back to test whether your rules predict them.

## Keeping it private

A pack can quote your correspondence and your unpublished work, so keep it out of anything you publish.

## Where the skills find it

Each skill takes the pack from the first of these that names one:

1. **A path you give when you ask:** "use my voice pack in `~/writing/voice-pack/`".
2. **A `voice_pack:` line in your own instructions** (`CLAUDE.md`, `AGENTS.md`, or your app's custom instructions), global or per project: `voice_pack: ~/writing/voice-pack`. Keep the pack in one place and point at it this way: it lives outside the skills, so updating them can't replace it, and one pack serves both.
3. **This folder,** `references/pack/` inside each skill. Replacing it works, but an update puts this fictional pack back, and you have to replace it in both skills.

Finding only this fictional pack, the skills look for a path or a `voice_pack:` line before giving up, then say they have no pack and work generically.

## Fictional throughout

The engineer, their colleagues, the sites, the dates and every figure in these files are invented.
