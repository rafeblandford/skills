---
name: verifying-ai-crawlers
description: Work out which AI crawler traffic in a log or analytics dataset is genuine, and report it honestly. Use when asked how much GPTBot/ClaudeBot/Perplexity traffic a site gets, whether a request claiming to be an AI crawler is real, or when analysing server logs, CDN analytics or bot reports for AI agent activity — and before quoting any figure for AI crawler volume.
license: Apache-2.0
metadata:
  provenance: written-with-ai
  version: "1.0"
---

# Verifying AI crawlers

**A user-agent is a text header. Anyone can send one.** `ClaudeBot/1.0` in a log
line is a claim by whoever sent the request, not evidence. Counting user-agent
strings produces a confident number that can be mostly fiction, and spoofing
only ever inflates it.

Spoofed AI-crawler user-agents are common because AI crawlers are widely
allowlisted. They frequently correlate with vulnerability scanning — the same
addresses probing for `/.env`, `/wp-admin` and similar. **A user-agent claiming
to be an AI crawler, from an IP doing that, is not an AI crawler.**

## What to do

1. **Group requests by claimed user-agent.** This is your *asserted* set. Never
   report it alone.
2. **For each operator, get its published IP ranges** (table below). Prefer the
   operator's own file over any aggregate.
3. **Check each source IP against the ranges.** Inside → *verified*. Outside →
   *asserted only*. No published ranges exist → *unverifiable*.
4. **If an operator signs its requests, check the signature instead** — it is
   stronger and needs no lists.
5. **Report the buckets separately.** Never blend them into one figure.
6. **Spot-check the failures.** If IPs claiming one operator are also hitting
   `/.env`, you have found a scanner, not a crawler.

⚠️ **Do all of this in the analysis, not at the edge.** Blocking on a failed
verification turns away real traffic silently and you find out late or never;
getting it wrong in the analysis means recomputing a number. Verification
belongs where being wrong is cheap.

## The three methods

| Method | How | When it works |
|---|---|---|
| **Signature** | Web Bot Auth / HTTP Message Signatures (RFC 9421). The operator publishes keys at `/.well-known/http-message-signatures-directory`; verify the signed request | Strongest and self-verifying. **Few operators do it yet** |
| **Published IP range** | Source IP inside the operator's published CIDRs | The working method today for most major operators |
| **Reverse DNS** | Resolve IP → hostname, confirm the operator's domain, resolve forward again | Google and Bing document it. ⚠️ **Fails for operators who publish IP lists instead — a failed rDNS check is not evidence of forgery** |

## Published ranges

| Operator | Source |
|---|---|
| OpenAI | `openai.com/gptbot.json`, `searchbot.json`, `chatgpt-user.json` |
| Anthropic | `claude.com/crawling/bots.json` — ClaudeBot, Claude-User, Claude-SearchBot |
| Google | `developers.google.com/static/search/apis/ipranges/` — `googlebot.json`, `special-crawlers.json`, `user-triggered-fetchers-google.json` |
| Bing | `bing.com/toolbox/bingbot.json` |
| Perplexity | `perplexity.com/perplexitybot.json`, `perplexity-user.json` |
| Apple | No file — documents `17.0.0.0/8` as its whole allocation |
| Others | [`ipverse/bot-ip-blocks`](https://github.com/ipverse/bot-ip-blocks) — aggregate feed, ~19 services, daily |

⚠️ **Use a first-party file where one exists.** If you publish the resulting
figure, *"the operator's own published range says so"* is auditable; *"a GitHub
repo said so"* is not. Where both exist, keep both and **record disagreement
rather than resolving it** — a prefix in one and not the other is a signal.

⚠️ **Never cite a feed URL you have not fetched.** Guessed filenames 404
silently, verify nothing, and look identical to "no traffic".

## Reporting: three buckets, never one

- **Verified** — source IP inside the published range, or signature checks out.
- **Asserted** — the user-agent says so and nothing corroborates it.
- **Unverifiable** — the operator publishes nothing to check against. **Not the
  same as failing.** Collapsing it into "asserted" penalises operators who are
  merely less organised.

Give verified and asserted side by side. A single blended number always
flatters.

⚠️ **"This operator publishes nothing" is a fact with a date on it, not a
property.** Operators add range files over time. Re-check before repeating an
absence you inherited from someone else's notes.

## Traps

**Sibling feeds that do not overlap.** Google publishes both
`user-triggered-fetchers.json` and `user-triggered-fetchers-google.json`, and
they contain different address space. Map a user-agent to the wrong one and
every fetch reports as spoofed — indistinguishable from genuine spoofing.
**If verification says an operator is 0% genuine, suspect your mapping first.**

**Crawler ranges are not an operator's other ranges.** The addresses a company
crawls from differ from those its API or tool traffic uses. Keep them separate.

**CDN and WAF bot flags are not verification.** A managed "verified bot" flag
reflects whatever that vendor checks — often reverse DNS — so it can read false
for a legitimate operator that verifies by published list. Treat it as one
signal, not the answer.

## What verification cannot tell you

It establishes **who**, not **why**. A verified request proves it came from that
operator's infrastructure. It says nothing about whether the fetch was for
training, search indexing, or a user asking a question in that moment — those
are separate user-agents by convention, and convention is not enforcement.

Never let a verified identity become a claim about purpose.
