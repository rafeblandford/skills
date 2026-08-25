# Rafe Blandford — Agent Skills

Skills I've built and found useful, published so other people's agents can use
them too. Each one is a folder with a `SKILL.md` — the [Agent Skills][spec]
format, which Claude Code, Codex, Gemini CLI, Cursor and others read.

They're written for agents, but they're plain Markdown: reading one tells you
what it does as clearly as running it.

## Skills

### Working with rafeblandford.com

**[`using-rafeblandford-com`](skills/using-rafeblandford-com/)** — how to find
out what I've done, written, or can evidence, without scraping the site.

My site publishes three interfaces for machines: an MCP endpoint for reasoning
about my career, a public Content API for bulk retrieval, and `llms.txt` plus
Markdown for crawling. This skill says which to reach for and — more
importantly — how to read what comes back without misrepresenting someone's
career. It carries two constraints that matter: the corpus is a *selection*, so
"not found" is a fact about the site and not about me; and case-study
`outcomes` are self-attested where `summary` is published.

*More to come.*

## Installing

| | |
|---|---|
| **Any agent** | `npx skills add rafeblandford/skills` |
| **Claude Code** | `/plugin marketplace add rafeblandford/skills` then `/plugin install using-rafeblandford-com@rafeblandford` |
| **Codex** | Copy the skill folder into `$HOME/.agents/skills/` |
| **Gemini CLI** | `gemini skills install https://github.com/rafeblandford/skills.git` |

## About these skills

**Provenance.** Each skill says in its own frontmatter how it was made —
`written-with-ai` means I wrote it working with an AI assistant, which is how
most of these come about. My site uses the same labelling for everything it
publishes: [rafeblandford.com/ai-provenance](https://rafeblandford.com/ai-provenance/).

**Licence.** Apache 2.0. Use them, change them, ship them.

**This repo is generated.** The sources live elsewhere and this is published
from them, so pull requests aren't accepted — but issues are very welcome, and
that's the right place to tell me something is wrong.

[spec]: https://agentskills.io/specification
