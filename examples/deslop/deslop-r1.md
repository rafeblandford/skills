# Deslop r1: the Mill Lane footbridge post

**Verdict.** Accurate apart from one overstatement of the survey, and in register. The one argument (¶5) is the drafter's, so it needs your answer first. The dates assume posting today.

**Basis.** Tier 2. Pack: the example pack, treated as no pack. Ownership evidence: the notes and provenance block in `draft.md`. Drafter and reviewer are the same model, so weigh this more lightly than an independent pass.

## Flags, in priority order

**P1 · act on · ¶5 "Because a nine-week closure…"** The paragraph's reason is the drafter's. Is it yours?

**S1 · act on · ¶1 "this morning" / ¶4 "this month" / ¶6 "next month's"** Three time references fixed to the drafting date.

**S2 · act on · ¶3 "Coring each joist"** The notes say only the four flagged joists were cored.

**S3 · minor · ¶3 "simply solved"** "Simply" overstates how easy the repair was.

**S4 · minor · ¶3 "deck... and"** The drafter placed this ellipsis.

**S5 · minor · ¶5 "Why does six weeks matter?"** A question the text answers itself. No wording proposed.

**S6 · minor · ¶5 "the kind of thing that"** A staging phrase, inside P1's sentence. P1 may settle it.

**P2 · their call · ¶4** The thank-you is yours to give or not.

**A1 · minor · after ¶5** The post reports; it doesn't say what you think about closures. Add your view, if you have one.

## Keep

- **K1 · ¶2** The background paragraph is from your notes.

## Decision table

| Flag | Proposal | Decision |
|---|---|---|
| P1 | Is ¶5's reason yours? | |
| S1 | Make the time references match the posting date | |
| S2 | "each joist" → "the four flagged joists" | |
| S3 | "simply solved" → "solved" | |
| S4 | Place the ellipsis yourself | |
| S5 | No wording proposed | |
| S6 | No wording proposed; may be settled by P1 | |
| P2 | Keep as is, or tell me otherwise | |
| A1 | Your view, if you want one in the post | |

Choices: accept the proposal / keep the original / revise differently, with a word on why (meaning, voice, reads-as-AI).

## Flags block

```json
{
  "version": 1,
  "title": "Mill Lane footbridge post, r1",
  "source": {"path": "draft.md", "heading": "Post (r1)"},
  "length": {"unit": "characters", "min": 800, "max": 1300, "label": "register range"},
  "flags": [
    {"id": "P1", "severity": "act on", "where": "¶5", "origin": "drafter",
     "title": "Is this your reason the closure mattered?",
     "spans": [{"para": 5, "quote": "Because a nine-week closure on a school route is the kind of thing that turns a maintenance job into a council agenda item, and nobody’s deck is improved by that."}],
     "body": "This is the post's only argument, and the drafter wrote it. If it's yours, it stays.",
     "choices": {"accept": "Yes, that's my reason", "keep": "Leave it as written", "revise": "No, or only partly; here's my real reason"},
     "note": "Your reason in your own words. Rough is fine."},
    {"id": "S1", "severity": "act on", "where": "¶1 ¶4 ¶6", "origin": "drafter",
     "title": "Are you posting today?",
     "spans": [{"para": 1, "quote": "this morning"}, {"para": 4, "quote": "this month"}, {"para": 6, "quote": "next month’s"}],
     "body": "All three are written for posting today. If it goes out next week, **all three** go stale.",
     "choices": {"accept": "Yes, posting today", "keep": "Leave it as written", "revise": "No; posting later, so fix the dates"}},
    {"id": "S2", "severity": "act on", "where": "¶3", "origin": "drafter",
     "title": "“each joist” → “the four flagged joists”",
     "spans": [{"para": 3, "quote": "Coring each joist"}],
     "proposal": {"from": "Coring each joist", "to": "Coring the four flagged joists"},
     "body": "The notes say only the four flagged joists were cored. The claim stays; the scope becomes accurate."},
    {"id": "S3", "severity": "minor", "where": "¶3", "origin": "drafter",
     "title": "“simply solved” → “solved”",
     "spans": [{"para": 3, "quote": "simply solved"}],
     "proposal": {"from": "simply solved", "to": "solved"},
     "body": "“Simply” overstates how easy the repair was."},
    {"id": "S4", "severity": "minor", "where": "¶3", "origin": "drafter",
     "title": "The ellipsis after “deck”",
     "spans": [{"para": 3, "quote": "deck… and"}],
     "body": "The drafter placed this one. No wording proposed.",
     "choices": {"accept": "Fine where it is", "keep": "Leave it as written", "revise": "I'll place it myself"}},
    {"id": "S5", "severity": "minor", "where": "¶5", "origin": "drafter",
     "title": "Opening on a question the post answers itself",
     "spans": [{"para": 5, "quote": "Why does six weeks matter?"}],
     "body": "A recognised staging pattern. No wording proposed; P1 may replace the paragraph anyway.",
     "choices": {"accept": "Fine as is", "keep": "Leave it as written", "revise": "Revise differently"}},
    {"id": "S6", "severity": "minor", "where": "¶5", "origin": "drafter",
     "title": "“the kind of thing that”",
     "spans": [{"para": 5, "quote": "the kind of thing that"}],
     "body": "A staging phrase inside P1's sentence. Your answer on P1 may settle it.",
     "choices": {"accept": "Fine as is", "keep": "Leave it as written", "revise": "Revise differently"}},
    {"id": "P2", "severity": "their call", "where": "¶4", "origin": "author",
     "title": "The thank-you to the site team",
     "spans": [{"para": 4}],
     "body": "Your notes thank the team; whether to do it publicly is your call. Keep as is, or tell me otherwise.",
     "choices": {"accept": "Fine as is", "keep": "Keep as is", "revise": "Tell me otherwise"}},
    {"id": "A1", "severity": "minor", "where": "after ¶5", "origin": "unknown",
     "title": "Your view on closures, if you want one in the post",
     "spans": [{"after": 5}],
     "body": "The post reports what happened rather than what you think. I won't write a view for you.",
     "choices": {"accept": "Yes; here's my view", "keep": "No view needed", "revise": "Something else"},
     "note": "Your view, rough is fine."}
  ]
}
```
