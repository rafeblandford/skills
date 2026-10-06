# Tier 3: the comparative read

Read at tier 3 only, after the flags are written. It settles the passages the lists can't: ones that hold no tell but might not be the author's, and flags you would mark *their call*. Most passages never reach it.

## Never ask whether a passage reads human

That question points a model at its largest measured bias. Judges preferred the LLM-written version of a text over the human one 64–88% of the time, against 28–46% for human raters (Laurito et al., *PNAS* 2025), and a Claude model could not pick out its own prose above chance (arXiv:2312.17289). Ask a located, comparative question against the author's own writing instead.

## When to skip it

Skip it, and say so in the output, when either of these applies:

- **Fewer than two reference passages** of 100–250 words in the same register that the pack records as the author's own unassisted writing. Don't pad with AI-assisted passages or another register.
- **No independent second call.** The two orders must be judged separately, each in a fresh call that hasn't seen the other answer: a subagent or a new request. Re-reading in the same context isn't an independent judgement.

## The procedure

1. **References.** Take two or three passages from the pack's register file (or the author's own published work in the same register), each 100–250 words. Use only writing the pack records as their own unassisted work.
2. **The pair.** Put the passage under review beside one alternative: the previous revision of the same passage, or your proposed edit. One pair per question; never rank three or more options, since position bias grows with the number of candidates.
3. **The question.** "Which of A and B is closer to the reference passages in how the reasoning moves, where the hedges sit and how the sentences are built? Quote the evidence from each before answering. Answer A, B or undecided."
4. **Both orders, separately.** Ask again with A and B swapped, in a fresh call. The direction of position bias isn't stable from model to model, so it can't be corrected for, only averaged out.
5. **Read the two answers.**
   - Both pick the same text: report it as a finding, with the quoted evidence.
   - They disagree, or either says undecided: **escalate.** List it under *their call* with both texts side by side and no recommendation.

## Limits to state in the output

The combination has never been measured as a whole. Each step has a measured effect on its own: averaging over both orders, reference samples in the prompt, an undecided option, escalating the uncertain tail. Judges are least stable on emotionally textured prose, which voice-laden prose is. So treat a comparative finding as one more piece of evidence beside the provenance record, never as a verdict that overrides it. Where the author said the words, the restraint rule wins whatever the comparison says.
