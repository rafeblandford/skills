# The flags block

The last thing in `deslop-r<n>.md`: a fenced `json` block under a `## Flags block` heading, holding the same actionable flags as the prose, in the same order. The prose is for the author to read. The block lets a tool place each flag in the draft and build a decision page. The two must agree; where they differ, fix the block. **The block records what the prose decided and never decides anything itself:** write the prose first, under §3's restraint rule, then copy it into the block.

```json
{
  "version": 1,
  "title": "Short name for the piece, r1",
  "source": {"path": "draft.md", "heading": "Post (r1)"},
  "length": {"unit": "characters", "min": 1200, "max": 1800, "label": "register range"},
  "flags": [
    {"id": "S2", "severity": "act on", "where": "¶3", "origin": "drafter",
     "title": "“crawler” → “parser”",
     "spans": [{"para": 3, "quote": "the crawler has no such problem"}],
     "proposal": {"from": "crawler", "to": "parser"},
     "body": "One or two sentences: why, and any fact checked.",
     "choices": {"accept": "Accept the change", "keep": "Keep “crawler”", "revise": "Revise differently"},
     "note": "Placeholder for the author's note, if a prompt helps."}
  ]
}
```

## Fields

- **`source`**: the draft's path, relative to the review file, and the heading of the reviewed section if the draft holds more than the piece (notes, provenance). Leave `heading` out when the whole file is the piece.
- **`length`** (optional): the register's range from the pack, if it has one. A page shows the count against it.
- **`id`, `severity`, `where`, `title`, `body`**: as in the prose. `severity` is `act on`, `minor` or `their call`. `title` is the short question or change, as in the Decision table.
- **`origin`** (optional): whose words the flag is on: `author`, `drafter`, `mixed`, `source` or `unknown`, from the provenance record. It lets proposals on the author's own words be counted separately.
- **`spans`**: where the flag sits. There are three kinds, and a flag may have several spans:
  - `{"para": n, "quote": "…"}`: inline. `quote` is an **exact substring of paragraph n**: copy it, never paraphrase, describe or shorten it with `…`. Quote enough words to be unique in the paragraph, or add `"occurrence": 2`.
  - `{"para": n}`: the whole paragraph, for a flag about its structure or argument.
  - `{"after": n}`: a place for an addition after paragraph n (`0` is before the first). Use it for `A` flags.
  A flag that touches several places (three time references, say) has one span for each.
- **`proposal`** (optional): only when the prose flag already offers replacement wording. `from` is an exact substring of the draft, usually the span's quote or part of it, and `to` is the replacement. A note, a question or any flag whose prose gives no wording has no `proposal`. Having the field is never a reason to propose.
- **`choices`** (optional): labels for accept, keep and revise *on this flag*, so the author can answer at a glance. The values themselves stay accept / keep / revise, and each label must mean its value, because the decisions are counted by value: **accept** takes the proposal (for a question, "yes"); **keep** leaves the draft exactly as it is; **revise** is any change other than the proposal, including a partial one. For a question flag, for example: "Yes, that's my reason / Leave it as written / No, or only partly; here's my real reason". Never put "partly" or "I'll adjust it" under keep. A *their call* flag, or any flag on the author's own or approved words, offers no change of its own: its revise label is always "Tell me otherwise", never "I'll revise it", "Revise differently" or a cut, and accept and keep both leave the words as they are.
- **`note`** (optional): a placeholder for the author's note.

## Numbering

¶n counts the body paragraphs of the reviewed text from 1, as voice's provenance records do: each blank-line-separated block of prose, or a list, counts as one. The title, headings, tables, captions, images, diagram placeholders and question blocks (`> **[Q1]** …`) are not counted. Use the same numbers in the prose.

## Checking it

If you can run scripts, run `python3 <skill>/scripts/decision_page.py check deslop-r<n>.md`. It reports any quote it can't find or that matches more than once. Fix the quote, not the draft. If you can't run scripts, copy each quote straight from the draft.
