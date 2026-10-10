#!/usr/bin/env python3
"""Decision page for a deslop review: render it, check its anchors, record the decisions.

Standard library only. The review's flags block (a fenced ```json block at the end of
`deslop-r<n>.md`, specified in `references/flags-block.md`) supplies the flags; the draft
supplies the text.

  decision_page.py check  deslop-r1.md                  # locate every quote; report misses
  decision_page.py render deslop-r1.md [-o page.html]   # split-view page, works offline
  decision_page.py render deslop-r1.md --artifact       # also saves to a claude.ai artifact db
  decision_page.py record pasted.md --review deslop-r1.md [-o decisions-r1.md]
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import sys
from pathlib import Path

FENCE_RE = re.compile(r"^```json[ \t]*\n(.*?)^```[ \t]*$", re.M | re.S)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
INLINE_RE = re.compile(
    r"`([^`]+)`"                         # code
    r"|\*\*(.+?)\*\*|__(.+?)__"          # strong
    r"|(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])"  # em; leaves 2*3*4 alone
    r"|\[([^\]]+)\]\([^)]*\)"            # link: keep the text
)
LIST_RE = re.compile(r"^\s*([-*+]|\d+[.)])\s+")
SEVERITIES = ("act on", "minor", "their call")
CHOICES = ("accept", "keep", "revise")
SINGLE = {"\u2018": "'", "\u2019": "'", "\u201a": "'", "\u201b": "'", "\u2032": "'",
          "\u201c": '"', "\u201d": '"', "\u201e": '"', "\u2033": '"', "\u00a0": " "}


class ReviewError(Exception):
    pass


# ---------------------------------------------------------------- reading the review

def load_block(review_path: Path) -> dict:
    """The last fenced JSON block in the review that carries a `flags` list."""
    text = review_path.read_text(encoding="utf-8")
    for body in reversed(FENCE_RE.findall(text)):
        try:
            block = json.loads(body)
        except json.JSONDecodeError as exc:
            if '"flags"' in body:
                raise ReviewError(f"{review_path.name}: the flags block isn't valid JSON ({exc})")
            continue
        if isinstance(block, dict) and isinstance(block.get("flags"), list):
            if not block.get("title"):
                h1 = re.search(r"^#\s+(.+)$", text, re.M)
                block["title"] = h1.group(1).strip() if h1 else review_path.stem
            return block
    raise ReviewError(f"{review_path.name}: no ```json flags block found (see references/flags-block.md)")


def reviewed_text(draft: str, heading: str | None) -> str:
    """The part of the draft that was reviewed: the section under `heading`, else the body."""
    lines = draft.replace("\r\n", "\n").replace("\r", "\n").lstrip("\ufeff").splitlines()  # Windows endings, BOM
    if lines and lines[0].strip() == "---":  # YAML front matter
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                lines = lines[i + 1:]
                break
    if not heading:
        return "\n".join(lines)
    want = heading.strip().lstrip("#").strip()
    for i, line in enumerate(lines):
        m = HEADING_RE.match(line)
        if m and m.group(2).strip() == want:
            # A named section is the piece and nothing else: it ends at the next heading of any
            # level, so notes under sub-headings ("What changed", "Open before posting") stay out.
            out = []
            for nxt in lines[i + 1:]:
                if HEADING_RE.match(nxt) or nxt.strip() in ("---", "***", "___"):
                    break
                out.append(nxt)
            return "\n".join(out)
    raise ReviewError(f'heading "{want}" not found in the draft')


def md_inline(src: str) -> tuple[str, list[list]]:
    """Markdown inline -> (plain text, [[start, end, style]]). Styles: code, strong, em."""
    plain, styles, pos = [], [], 0
    length = 0
    for m in INLINE_RE.finditer(src):
        before = src[pos:m.start()]
        plain.append(before)
        length += len(before)
        for group, style in ((1, "code"), (2, "strong"), (3, "strong"), (4, "em"), (5, None)):
            inner = m.group(group)
            if inner is not None:
                if style != "code" and INLINE_RE.search(inner):
                    inner_plain, inner_styles = md_inline(inner)
                    styles.extend([s + length, e + length, st] for s, e, st in inner_styles)
                    inner = inner_plain
                if style:
                    styles.append([length, length + len(inner), style])
                plain.append(inner)
                length += len(inner)
                break
        pos = m.end()
    plain.append(src[pos:])
    return "".join(plain), styles


def paragraphs(text: str) -> list[dict]:
    """Blank-line-separated blocks. ¶n numbers body paragraphs only, as voice's records do:
    headings, tables, captions, images, diagram placeholders and question blocks are unnumbered."""
    blocks = [b for b in re.split(r"\n[ \t]*\n", text.strip("\n")) if b.strip()]
    out, n = [], 0
    for block in blocks:
        lines = [ln.rstrip() for ln in block.strip("\n").splitlines()]
        heading = HEADING_RE.match(lines[0]) if len(lines) == 1 else None
        first_list = next((k for k, ln in enumerate(lines) if LIST_RE.match(ln)), None)
        if len(lines) == 1 and re.fullmatch(r"\s*([-*_])(\s*\1){2,}\s*", lines[0]):
            continue  # a horizontal rule: not text, not a paragraph
        if heading:
            kind, raw = "h", heading.group(2)
        elif len(lines) >= 2 and all(ln.lstrip().startswith("|") for ln in lines) and re.match(r"^\|?\s*:?-{2,}", lines[1]):
            kind, raw = "table", "\n".join(" | ".join(c.strip() for c in ln.strip().strip("|").split("|")) for ln in [lines[0]] + lines[2:])
        elif len(lines) == 1 and re.match(r"^!\[[^\]]*\]\([^)]*\)$|^\[(DIAGRAM|FIGURE|IMAGE|CHART)\b", lines[0], re.I):
            kind, raw = "fig", lines[0]
        elif all(ln.lstrip().startswith(">") for ln in lines):
            kind, raw = "q", " ".join(ln.lstrip()[1:].strip() for ln in lines)
        elif first_list is not None and all(LIST_RE.match(ln) or ln.startswith((" ", "\t")) for ln in lines[first_list:]):
            lead = " ".join(ln.strip() for ln in lines[:first_list])
            kind, raw = "list", "\n".join(([lead] if lead else []) + [ln.strip() for ln in lines[first_list:]])
        else:
            kind, raw = "p", " ".join(ln.strip() for ln in lines)
            if re.fullmatch(r"\*(?!\*)[^*].*[^*]\*", raw):
                kind = "cap"
        plain, styles = md_inline(raw)
        label = ""
        if kind in ("p", "list"):
            n += 1
            label = f"¶{n}"
        out.append({"kind": kind, "text": plain, "styles": styles, "label": label})
    return out


def para_index(paras: list[dict], n) -> int | None:
    """The block that is ¶n, or None."""
    return next((i for i, p in enumerate(paras) if p["label"] == f"¶{n}"), None) if isinstance(n, int) else None


# ---------------------------------------------------------------- locating quotes

def normalise(s: str) -> tuple[str, list[int], list[int]]:
    """Fold typographic variants so a quote matches however it was typed.

    Returns the folded string and, per folded character, its start and end in `s`.
    """
    out, starts, ends = [], [], []
    prev_space = False
    for i, ch in enumerate(s):
        ch = SINGLE.get(ch, ch)
        if ch.isspace():
            if prev_space:
                ends[-1] = i + 1
                continue
            ch, prev_space = " ", True
        else:
            prev_space = False
        rep = "..." if ch == "\u2026" else ch
        for c in rep:
            out.append(c)
            starts.append(i)
            ends.append(i + 1)
    return "".join(out), starts, ends


def find_all(quote: str, text: str, fold_case: bool = False) -> list[tuple[int, int]]:
    q = normalise(md_inline(quote)[0].strip())[0]
    t, starts, ends = normalise(text)
    if fold_case:
        q, t = q.lower(), t.lower()
    if not q:
        return []
    hits, i = [], t.find(q)
    while i != -1:
        hits.append((starts[i], ends[i + len(q) - 1]))
        i = t.find(q, i + 1)
    return hits


def locate(quote: str, paras: list[dict], para: int | None, occurrence: int | None):
    """-> (para index, start, end, warning or None), or (None, None, None, warning)."""
    candidates = [quote]
    stripped = re.sub(r"(\u2026|\.\.\.)$", "", quote).strip()
    if stripped != quote:
        candidates.append(stripped)  # a truncated quote still anchors at its start
    order = list(range(len(paras)))
    if para is not None and 0 <= para < len(paras):
        order.remove(para)
        order.insert(0, para)
    for fold in (False, True):
        for cand in candidates:
            for p in order:
                hits = find_all(cand, paras[p]["text"], fold)
                if not hits:
                    continue
                notes = []
                if para is not None and p != para:
                    notes.append(f"found in {paras[p]['label'] or 'an unnumbered block'}, not {paras[para]['label']}")
                if fold:
                    notes.append("matched only ignoring case")
                if cand is not quote:
                    notes.append("matched without its trailing ellipsis")
                pick = 0
                if occurrence:
                    if occurrence <= len(hits):
                        pick = occurrence - 1
                    else:
                        notes.append(f"occurrence {occurrence} asked, {len(hits)} found; using the first")
                elif len(hits) > 1:
                    notes.append(f"appears {len(hits)} times in {paras[p]['label'] or 'that block'}; using the first (set occurrence)")
                if para is None and len(hits) == 1:
                    elsewhere = sum(len(find_all(cand, paras[o]["text"], fold)) for o in order if o != p)
                    if elsewhere:
                        notes.append(f"also appears in other paragraphs; set para")
                s, e = hits[pick]
                return p, s, e, "; ".join(notes) or None
    return None, None, None, "not found in the draft"


def resolve(block: dict, paras: list[dict]) -> dict:
    """Turn the flags block into the page's data: ranges, gutter marks, slots, proposals."""
    ranges, gutter, slots, proposals, warnings = [], [], [], {}, []
    seen = set()
    for flag in block["flags"]:
        fid = str(flag.get("id", "")).strip()
        if not fid:
            warnings.append("a flag has no id; skipped")
            continue
        if fid in seen:
            warnings.append(f"{fid}: id used twice")
        seen.add(fid)
        if flag.get("severity") not in SEVERITIES:
            warnings.append(f"{fid}: severity {flag.get('severity')!r} isn't one of {', '.join(SEVERITIES)}")
        mine = []
        for span in flag.get("spans") or []:
            para = span.get("para")
            pidx = para_index(paras, para)
            if para is not None and pidx is None:
                count = sum(1 for p in paras if p["label"])
                warnings.append(f"{fid}: ¶{para} doesn't exist (the text has {count})")
            if "after" in span:
                after = span["after"]
                at = -1 if after == 0 else para_index(paras, after)
                if at is not None:
                    slots.append({"after": at, "flag": fid})
                else:
                    warnings.append(f"{fid}: can't place an addition after ¶{after}")
                continue
            quote = span.get("quote")
            if not quote:
                if pidx is None:
                    warnings.append(f"{fid}: a span has neither a quote nor a valid para")
                else:
                    gutter.append({"p": pidx, "flag": fid})
                continue
            p, s, e, note = locate(quote, paras, pidx, span.get("occurrence"))
            if p is None:
                warnings.append(f'{fid}: "{quote}" {note}'
                                + (f"; marked on {paras[pidx]['label']} instead" if pidx is not None else ""))
                if pidx is not None:
                    gutter.append({"p": pidx, "flag": fid})
                continue
            if note:
                warnings.append(f'{fid}: "{quote}" {note}')
            ranges.append({"p": p, "s": s, "e": e, "flag": fid})
            mine.append((p, s, e))
        prop = flag.get("proposal")
        if isinstance(prop, dict) and prop.get("from") and prop.get("to") is not None:
            hit = None
            for p, s, e in mine:  # inside the flag's own span first
                inner = find_all(prop["from"], paras[p]["text"][s:e])
                if inner:
                    hit = (p, s + inner[0][0], s + inner[0][1])
                    break
            if hit is None:
                p, s, e, note = locate(prop["from"], paras, mine[0][0] if mine else None, None)
                if p is None:
                    warnings.append(f'{fid}: proposal "{prop["from"]}" not found; no live preview')
                else:
                    hit = (p, s, e)
            if hit:
                proposals[fid] = {"p": hit[0], "s": hit[1], "e": hit[2], "to": prop["to"]}
    # Two accepted proposals over the same words can't both preview.
    items = sorted(proposals.items(), key=lambda kv: (kv[1]["p"], kv[1]["s"]))
    for (a, x), (b, y) in zip(items, items[1:]):
        if x["p"] == y["p"] and y["s"] < x["e"]:
            warnings.append(f"{a} and {b}: proposals overlap; only the first accepted one previews")
    return {"ranges": ranges, "gutter": gutter, "slots": slots, "proposals": proposals,
            "warnings": warnings}


def build_data(review_path: Path, draft_override: str | None, heading_override: str | None) -> dict:
    block = load_block(review_path)
    source = block.get("source") or {}
    draft_name = draft_override or source.get("path")
    if not draft_name:
        raise ReviewError("no draft: set source.path in the flags block or pass --draft")
    draft_path = Path(draft_name).expanduser()
    if not draft_path.is_absolute() and not draft_override:
        draft_path = review_path.parent / draft_path
    if not draft_path.exists():
        raise ReviewError(f"draft not found: {draft_path}")
    heading = heading_override if heading_override is not None else source.get("heading")
    paras = paragraphs(reviewed_text(draft_path.read_text(encoding="utf-8"), heading))
    if not paras:
        raise ReviewError("the reviewed text is empty")
    data = resolve(block, paras)
    # Saved choices are keyed on this: the title, not the file name, as every first review is deslop-r1.
    slug = re.sub(r"[^a-z0-9]+", "-", (block.get("slug") or f"{block['title']} {review_path.stem}").lower()).strip("-")
    data.update({
        "title": block["title"],
        "slug": slug or "review",
        "review": review_path.name,
        "draft": draft_path.name,
        "length": block.get("length"),
        "paras": paras,
        "flags": [{k: f.get(k) for k in ("id", "severity", "where", "title", "body", "spans",
                                         "proposal", "choices", "note", "origin")}
                  for f in block["flags"] if f.get("id")],
    })
    return data


# ---------------------------------------------------------------- recording decisions

def split_row(line: str) -> list[str]:
    cells = re.split(r"(?<!\\)\|", line.strip().strip("|"))
    return [c.strip().replace("\\|", "|") for c in cells]


def parse_pasted(text: str) -> dict[str, dict]:
    """Rows from a pasted decision table, keyed by flag id. Reads the page's five-column
    table and the older four-column one ("why: a, b · note")."""
    rows, header = {}, None
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = split_row(line)
        if re.fullmatch(r":?-{2,}:?", cells[0] or "-"):
            continue
        if cells[0].lower() == "flag":
            header = [c.lower() for c in cells]
            continue
        if not re.fullmatch(r"[A-Z]+\d+", cells[0]):
            continue
        col = {name: (cells[i] if i < len(cells) else "") for i, name in enumerate(header or [])}
        decision_cell = col.get("decision", cells[2] if len(cells) > 2 else "")
        m = re.match(r"\s*(accept|keep|revise|undecided)\b\s*:?\s*(.*)", decision_cell, re.I)
        decision = m.group(1).lower() if m else ""
        label = m.group(2).strip() if m else decision_cell.strip()
        if decision == "undecided" or not decision:
            decision = "undecided" if (not decision_cell or decision == "undecided") else "unclear"
        why, note = col.get("why", ""), col.get("note", "")
        if "why / note" in col:
            combined = col["why / note"]
            parts = [p.strip() for p in combined.split("·")]
            if parts and parts[0].lower().startswith("why:"):
                why = parts.pop(0)[4:].strip()
            note = " · ".join(parts)
        rows[cells[0]] = {"decision": decision, "label": label,
                          "why": [w.strip() for w in why.split(",") if w.strip()], "note": note}
    return rows


def record(pasted: str, block: dict, review_name: str) -> str:
    rows = parse_pasted(pasted)
    flags = {f["id"]: f for f in block["flags"] if f.get("id")}
    unknown = [fid for fid in rows if fid not in flags]
    d = dt.date.today()
    today = f"{d.day} {d:%b %Y}"
    out = [f"# Decisions: {block.get('title') or review_name}", "",
           f"Recorded {today} from the decision page for `{review_name}`.", "",
           "| Flag | Severity | Question | Decision | Why | Note |", "|---|---|---|---|---|---|"]
    counts = {sev: dict.fromkeys(CHOICES + ("undecided",), 0) for sev in SEVERITIES}
    why_counts: dict[str, int] = {}
    own_words = {"proposals": 0, "kept": 0}
    for fid, flag in flags.items():
        row = rows.get(fid, {"decision": "undecided", "label": "", "why": [], "note": ""})
        sev = flag.get("severity") if flag.get("severity") in SEVERITIES else "minor"
        dec = row["decision"] if row["decision"] in CHOICES else "undecided"
        counts[sev][dec] += 1
        for w in row["why"]:
            why_counts[w] = why_counts.get(w, 0) + 1
        if flag.get("origin") == "author" and flag.get("proposal") and sev != "their call":
            own_words["proposals"] += 1
            own_words["kept"] += dec == "keep"
        shown = row["decision"] + (f": {row['label']}" if row["label"] else "")
        cells = [fid, sev, flag.get("title") or "", shown, ", ".join(row["why"]), row["note"]]
        out.append("| " + " | ".join(c.replace("|", "\\|").replace("\n", " ") for c in cells) + " |")
    out += ["", "## Counts", "", "| Severity | accept | keep | revise | undecided | total |",
            "|---|---|---|---|---|---|"]
    totals = dict.fromkeys(CHOICES + ("undecided",), 0)
    for sev in SEVERITIES:
        c = counts[sev]
        if sum(c.values()):
            out.append(f"| {sev} | " + " | ".join(str(c[k]) for k in totals) + f" | {sum(c.values())} |")
            for k in totals:
                totals[k] += c[k]
    out.append("| **all** | " + " | ".join(str(totals[k]) for k in totals) + f" | {sum(totals.values())} |")
    out.append("")
    if why_counts:
        out.append("Why: " + ", ".join(f"{k} {v}" for k, v in sorted(why_counts.items())) + ".")
    if own_words["proposals"]:
        out.append(f"Proposals on the author's own words (not *their call*): {own_words['proposals']}, "
                   f"of which kept as written: {own_words['kept']}.")
    out.append("A *their call* flag kept as written is a declined note, not a false alarm.")
    if unknown:
        out.append(f"Rows not in the flags block, ignored: {', '.join(unknown)}.")
    unclear = [fid for fid, r in rows.items() if r["decision"] == "unclear"]
    if unclear:
        out.append(f"Decisions not read as accept/keep/revise, counted as undecided: {', '.join(unclear)}.")
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- page

def render(data: dict, artifact: bool) -> str:
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    return (PAGE.replace("__TITLE__", html.escape(data["title"]))
                .replace("__ARTIFACT__", "true" if artifact else "false")
                .replace("__DATA__", payload))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("check", "render"):
        sp = sub.add_parser(name)
        sp.add_argument("review", type=Path, help="deslop-r<n>.md with a flags block")
        sp.add_argument("--draft", help="draft file, if not source.path in the block")
        sp.add_argument("--heading", help="section of the draft that was reviewed")
        if name == "render":
            sp.add_argument("-o", "--out", type=Path, help="default: decisions-r<n>.html beside the review")
            sp.add_argument("--artifact", action="store_true",
                            help="also save to a claude.ai artifact db (publish with capabilities {db:{}})")
            sp.add_argument("--strict", action="store_true", help="exit 1 if any anchor needs a look")
    rp = sub.add_parser("record")
    rp.add_argument("pasted", help="file holding the pasted decision table, or - for stdin")
    rp.add_argument("--review", type=Path, required=True, help="the deslop-r<n>.md it decides")
    rp.add_argument("-o", "--out", type=Path, help="default: decisions-r<n>.md beside the review")
    args = ap.parse_args(argv)

    try:
        if args.cmd == "record":
            block = load_block(args.review)
            pasted = sys.stdin.read() if args.pasted == "-" else Path(args.pasted).read_text(encoding="utf-8")
            out = args.out or args.review.with_name(re.sub(r"^deslop-", "decisions-", args.review.stem) + ".md")
            out.write_text(record(pasted, block, args.review.name), encoding="utf-8")
            print(out)
            return 0
        data = build_data(args.review, args.draft, args.heading)
    except (ReviewError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    for w in data["warnings"]:
        print(f"warning: {w}", file=sys.stderr)
    placed = len({r["flag"] for r in data["ranges"]} | {g["flag"] for g in data["gutter"]}
                 | {s["flag"] for s in data["slots"]})
    summary = (f"{len(data['flags'])} flags, {placed} placed in the text, {len(data['paras'])} paragraphs, "
               f"{len(data['warnings'])} warnings")
    if args.cmd == "check":
        print(summary)
        return 1 if data["warnings"] else 0
    out = args.out or args.review.with_name(re.sub(r"^deslop-", "decisions-", args.review.stem) + ".html")
    out.write_text(render(data, args.artifact), encoding="utf-8")
    print(f"{out} ({summary})")
    return 1 if args.strict and data["warnings"] else 0


PAGE = r"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
/* The draft sits in its own scrolling pane on the left; the flags scroll with the page on the right. One column below 900px. */
:root {
  --bg: #f5f6f8; --surface: #ffffff; --ink: #18202c; --muted: #5b6676; --line: #dde2ea;
  --accent: #1f4fbf; --accent-soft: #e6ecfa;
  --act: #b4361f; --act-soft: #fbe4de; --act-strong: #f4c3b6;
  --minor: #7d5f0c; --minor-soft: #fbf0cc; --minor-strong: #f2dc8e;
  --their: #4b5a70; --their-soft: #e8ecf2; --their-strong: #cdd6e3;
  --ok: #1d7a4c; --ok-soft: #e2f3ea;
  --font-read: Charter, "Iowan Old Style", "Palatino Linotype", Georgia, serif;
  --font-ui: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --font-mono: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #12161d; --surface: #1a2029; --ink: #e5e9f0; --muted: #98a3b3; --line: #2c3442;
    --accent: #8fb0ff; --accent-soft: #1f2b45;
    --act: #f08a74; --act-soft: #3a211c; --act-strong: #6a3427;
    --minor: #e0c26a; --minor-soft: #342c14; --minor-strong: #5e4c1c;
    --their: #a9b6c8; --their-soft: #252d39; --their-strong: #3b475a;
    --ok: #6fd3a0; --ok-soft: #173126; color-scheme: dark;
  }
}
:root[data-theme="dark"] {
  --bg: #12161d; --surface: #1a2029; --ink: #e5e9f0; --muted: #98a3b3; --line: #2c3442;
  --accent: #8fb0ff; --accent-soft: #1f2b45;
  --act: #f08a74; --act-soft: #3a211c; --act-strong: #6a3427;
  --minor: #e0c26a; --minor-soft: #342c14; --minor-strong: #5e4c1c;
  --their: #a9b6c8; --their-soft: #252d39; --their-strong: #3b475a;
  --ok: #6fd3a0; --ok-soft: #173126; color-scheme: dark;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--ink); font-family: var(--font-ui); font-size: 15px; line-height: 1.5; }
.wrap { max-width: 1280px; margin: 0 auto; padding: 24px 16px 64px; }
@media (min-width: 600px) { .wrap { padding-inline: 24px; } }
header.top { display: flex; flex-wrap: wrap; align-items: end; justify-content: space-between; gap: 12px 20px; margin-bottom: 20px; }
h1 { font-family: var(--font-read); font-weight: 500; font-size: 28px; line-height: 1.15; margin: 0 0 6px; text-wrap: balance; }
.sub { color: var(--muted); margin: 0; max-width: 64ch; }
.status { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }
.progress { font-variant-numeric: tabular-nums; font-weight: 600; }
.save { font-size: 13px; color: var(--muted); }
.save.err { color: var(--act); }
button { font: inherit; cursor: pointer; }
.btn { border: 1px solid var(--line); background: var(--surface); color: var(--ink); border-radius: 6px; padding: 7px 12px; font-size: 14px; }
.btn:hover { border-color: var(--accent); }
:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.warn { background: var(--minor-soft); border: 1px solid var(--line); border-radius: 8px; padding: 8px 12px; margin-bottom: 16px; font-size: 13.5px; }
.warn summary { cursor: pointer; font-weight: 600; }
.warn ul { margin: 6px 0 0; padding-left: 20px; }

.grid { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 24px; align-items: start; }
.pane { position: sticky; top: 12px; max-height: calc(100vh - 24px); overflow: auto; overscroll-behavior: contain;
  background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 18px 20px 18px 48px; min-width: 0; }
@media (max-width: 900px) {
  .grid { grid-template-columns: minmax(0, 1fr); }
  .pane { position: static; max-height: none; overflow: visible; }
}
.pane-head { display: flex; justify-content: space-between; gap: 8px 12px; flex-wrap: wrap; align-items: baseline; margin: 0 0 14px -28px; }
.label { font-size: 12px; letter-spacing: .06em; text-transform: uppercase; color: var(--muted); font-weight: 600; }
.count { font-size: 13px; color: var(--muted); font-variant-numeric: tabular-nums; }
.count.out { color: var(--act); }
.para { position: relative; font-family: var(--font-read); font-size: 18px; line-height: 1.6; margin: 0 0 14px; max-width: 65ch; }
.para.list { white-space: pre-line; }
.para.aside { font-family: var(--font-ui); font-size: 14.5px; color: var(--muted); }
h2.para { font-size: 21px; font-weight: 600; line-height: 1.3; }
.pn { position: absolute; left: -44px; top: 6px; width: 22px; text-align: right; font-family: var(--font-mono); font-size: 11px; line-height: 1; color: var(--muted); }
.para code { font-family: var(--font-mono); font-size: .82em; background: var(--accent-soft); padding: 1px 4px; border-radius: 3px; }

/* Inline flags: severity colours the highlight; the id is always shown as text, so colour is never the only signal. */
.hl { color: inherit; border-radius: 3px; padding: 0 1px; cursor: pointer; transition: background-color .15s, box-shadow .15s; }
.hl.sev-act { background: var(--act-soft); }
.hl.sev-minor { background: var(--minor-soft); }
.hl.sev-their { background: var(--their-soft); }
.hl.multi { box-shadow: inset 0 -2px 0 var(--muted); }          /* a span nested inside another flag's span */
.hl.done { background: transparent; text-decoration: underline 2px var(--ok); text-underline-offset: 4px; }
.hl.applied { background: var(--ok-soft); text-decoration: none; }
.hl.on.sev-act { background: var(--act-strong); }
.hl.on.sev-minor { background: var(--minor-strong); }
.hl.on.sev-their { background: var(--their-strong); }
.hl.on { box-shadow: 0 0 0 2px var(--accent); }
.tag { font-family: var(--font-mono); font-size: 10.5px; line-height: 1; vertical-align: super; color: var(--muted);
  background: none; border: 0; padding: 0 2px; margin-left: 1px; border-radius: 3px; }
.tag:hover, .tag.on { color: var(--surface); background: var(--accent); }
/* Paragraph-level flags: a bar in the gutter, labelled. */
.gut { position: absolute; left: -8px; top: 3px; bottom: 3px; display: flex; gap: 2px; transform: translateX(-100%); }
.gut button { width: 6px; padding: 0; border: 0; border-radius: 3px; position: relative; }
.gut button span { position: absolute; top: 16px; right: 9px; font-family: var(--font-mono); font-size: 10px; color: var(--muted); white-space: nowrap; }
.gut .sev-act { background: var(--act); } .gut .sev-minor { background: var(--minor); } .gut .sev-their { background: var(--their); }
.gut button.done { opacity: .35; }
.gut button.on { box-shadow: 0 0 0 2px var(--accent); }
.slot { display: block; width: 100%; max-width: 65ch; margin: -4px 0 14px; padding: 6px 10px; text-align: left; font-size: 13px; color: var(--muted);
  background: transparent; border: 1.5px dashed var(--line); border-radius: 6px; }
.slot.on { border-color: var(--accent); color: var(--accent); }
.slot.done { opacity: .5; }
.legend { display: flex; gap: 6px 14px; flex-wrap: wrap; font-size: 12px; color: var(--muted); margin-top: 16px; }
.legend i { display: inline-block; width: 10px; height: 10px; border-radius: 2px; margin-right: 5px; vertical-align: -1px; }

.flags { display: flex; flex-direction: column; gap: 14px; min-width: 0; }
.group-title { margin: 6px 0 -4px; }
.flag { background: var(--surface); border: 1px solid var(--line); border-left-width: 4px; border-radius: 10px; padding: 14px 16px; min-width: 0; scroll-margin-top: 16px; transition: box-shadow .2s, border-color .2s; }
.flag.sev-act { border-left-color: var(--act); } .flag.sev-minor { border-left-color: var(--minor); } .flag.sev-their { border-left-color: var(--their); }
.flag.on { box-shadow: 0 0 0 2px var(--accent-soft), 0 1px 6px rgb(0 0 0 / .06); }
.flag.pulse { box-shadow: 0 0 0 4px var(--accent); }
.flag-head { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; margin-bottom: 6px; }
.id { font-family: var(--font-mono); font-size: 13px; font-weight: 600; }
.chip { font-size: 11.5px; font-weight: 600; letter-spacing: .03em; padding: 2px 8px; border-radius: 20px; }
.chip.sev-act { background: var(--act-soft); color: var(--act); }
.chip.sev-minor { background: var(--minor-soft); color: var(--minor); }
.chip.sev-their { background: var(--their-soft); color: var(--their); }
.chip.where { background: var(--accent-soft); color: var(--accent); font-weight: 500; }
.chip.step { border: 1px solid transparent; cursor: pointer; }
.chip.step:hover { border-color: var(--accent); }
.chip.state { margin-left: auto; background: var(--ok-soft); color: var(--ok); }
.flag h3 { font-size: 16px; font-weight: 600; margin: 0 0 6px; text-wrap: balance; }
.quote { font-family: var(--font-read); font-size: 16px; border-left: 3px solid var(--line); padding-left: 10px; margin: 8px 0; }
.quote del { color: var(--muted); } .quote ins { text-decoration: none; background: var(--ok-soft); }
.flag p { margin: 6px 0; color: var(--muted); max-width: 65ch; }
.flag p strong { color: var(--ink); }
.choices { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }
.choice { border: 1px solid var(--line); background: var(--bg); color: var(--ink); border-radius: 6px; padding: 7px 12px; font-size: 14px; text-align: left; }
.choice[aria-pressed="true"] { background: var(--accent); border-color: var(--accent); color: var(--surface); }
.why { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; margin-top: 10px; font-size: 13px; color: var(--muted); }
.why button { border: 1px solid var(--line); background: transparent; color: var(--muted); border-radius: 20px; padding: 2px 10px; font-size: 12.5px; }
.why button[aria-pressed="true"] { border-color: var(--accent); color: var(--accent); background: var(--accent-soft); }
textarea { width: 100%; min-height: 60px; margin-top: 10px; font: inherit; font-size: 14px; color: var(--ink); background: var(--bg); border: 1px solid var(--line); border-radius: 6px; padding: 8px 10px; resize: vertical; }
textarea::placeholder { color: var(--muted); }

.summary { margin-top: 28px; background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 16px 18px; }
.summary-head { display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap; margin-bottom: 10px; }
.summary h2 { font-size: 17px; margin: 0; }
.table-wrap { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; font-size: 14px; }
th, td { text-align: left; padding: 7px 10px; border-bottom: 1px solid var(--line); vertical-align: top; }
th { font-size: 12px; text-transform: uppercase; letter-spacing: .05em; color: var(--muted); font-weight: 600; }
td.mono { font-family: var(--font-mono); font-size: 13px; }
td.pending { color: var(--muted); font-style: italic; }
#md { position: absolute; left: -9999px; white-space: pre; }
@media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
</style>
</head>
<body>
<div class="wrap">
  <header class="top">
    <div>
      <h1 id="title"></h1>
      <p class="sub" id="sub"></p>
    </div>
    <div class="status">
      <span class="progress" id="progress"></span>
      <span class="save" id="save"></span>
    </div>
  </header>
  <div id="warn"></div>
  <div class="grid">
    <article class="pane" id="pane" aria-label="The draft, with your accepted edits">
      <div class="pane-head"><span class="label">Draft · with accepted edits</span><span class="count" id="count"></span></div>
      <div id="text"></div>
      <div class="legend">
        <span><i style="background:var(--act-soft)"></i>act on</span>
        <span><i style="background:var(--minor-soft)"></i>minor</span>
        <span><i style="background:var(--their-soft)"></i>their call</span>
        <span><i style="background:var(--ok-soft)"></i>accepted edit</span>
        <span><i style="border-bottom:2px solid var(--ok);border-radius:0"></i>decided</span>
      </div>
    </article>
    <section class="flags" id="flags" aria-label="Flags"></section>
  </div>
  <section class="summary">
    <div class="summary-head">
      <h2>Decision table</h2>
      <button class="btn" id="copy" type="button">Copy as Markdown</button>
    </div>
    <div class="table-wrap"><table>
      <thead><tr><th>Flag</th><th>Question</th><th>Decision</th><th>Why</th><th>Note</th></tr></thead>
      <tbody id="table"></tbody>
    </table></div>
  </section>
  <pre id="md" aria-hidden="true"></pre>
</div>
<script>
const D = __DATA__;
const ARTIFACT = __ARTIFACT__;
const KEY = "deslop-decisions:" + D.slug;
const WHY = ["meaning", "voice", "reads as AI"];
const SEV = { "act on": "act", "minor": "minor", "their call": "their" };
const SEV_ORDER = ["act on", "minor", "their call"];
const DEFAULT_CHOICES = { accept: "Accept the proposal", keep: "Keep the original", revise: "Revise differently" };
const byId = Object.fromEntries(D.flags.map((f) => [f.id, f]));
const wide = matchMedia("(min-width: 901px)");
const calm = matchMedia("(prefers-reduced-motion: reduce)");

let state = { flags: {} };
let pinned = null, hover = null, hoverTimer = null;
const step = {};
let docRef = null, canSave = false, saveTimer = null;

const $ = (id) => document.getElementById(id);
const esc = (s) => String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
const rich = (s) => esc(s).replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>").replace(/`([^`]+)`/g, "<code>$1</code>");
const get = (id) => state.flags[id] || (state.flags[id] = { decision: null, why: [], note: "" });
const sev = (id) => SEV[(byId[id] || {}).severity] || "minor";
const choicesOf = (f) => Object.assign({}, DEFAULT_CHOICES, f.choices || {});
const accepted = (id) => get(id).decision === "accept";

// One paragraph: cut the text at every range, style and accepted-proposal boundary, then
// wrap each piece in a mark for the flags that cover it. The innermost flag is on top.
function paraHTML(i) {
  const P = D.paras[i], text = P.text;
  const rs = D.ranges.filter((r) => r.p === i);
  const props = [];
  for (const [id, x] of Object.entries(D.proposals)) {
    if (x.p === i && accepted(id) && !props.some((y) => x.s < y.e && y.s < x.e)) props.push({ id, ...x });
  }
  const cuts = new Set([0, text.length]);
  for (const r of rs) { cuts.add(r.s); cuts.add(r.e); }
  for (const [s, e] of P.styles) { cuts.add(s); cuts.add(e); }
  for (const x of props) { cuts.add(x.s); cuts.add(x.e); }
  const pts = [...cuts].sort((a, b) => a - b);
  const swallowed = (r) => props.some((x) => r.s >= x.s && r.e <= x.e && r.flag !== x.id);
  let html = "", plain = "";
  const mark = (inner, a, b, extra) => {
    const cover = rs.filter((r) => r.s <= a && r.e >= b && !swallowed(r));
    if (extra && !cover.some((r) => r.flag === extra)) cover.push({ flag: extra, s: a, e: b });
    if (!cover.length) return inner;
    cover.sort((x, y) => (x.e - x.s) - (y.e - y.s));
    const top = cover[0].flag, ids = [...new Set(cover.map((r) => r.flag))];
    const cls = ["hl", "sev-" + sev(top)];
    if (ids.length > 1) cls.push("multi");
    if (extra) cls.push("applied"); else if (get(top).decision) cls.push("done");
    return `<mark class="${cls.join(" ")}" data-flags="${ids.join(" ")}" data-top="${top}">${inner}</mark>`;
  };
  const tags = (pos) => rs.filter((r) => r.e === pos && !swallowed(r))
    .sort((x, y) => (x.e - x.s) - (y.e - y.s))
    .map((r) => `<button type="button" class="tag" data-flag="${r.flag}" aria-label="Go to ${r.flag}">${r.flag}</button>`).join("");
  for (let k = 0; k < pts.length - 1; k++) {
    const a = pts[k], b = pts[k + 1];
    const pr = props.find((x) => a >= x.s && b <= x.e);
    if (pr) {
      if (a === pr.s) { html += mark(esc(pr.to), pr.s, pr.e, pr.id); plain += pr.to; }
      if (b === pr.e) html += tags(b);
      continue;
    }
    let inner = esc(text.slice(a, b));
    for (const [s, e, st] of P.styles) if (s <= a && e >= b) inner = st === "code" ? `<code>${inner}</code>` : `<${st}>${inner}</${st}>`;
    plain += text.slice(a, b);
    html += mark(inner, a, b) + tags(b);
  }
  const gut = D.gutter.filter((g) => g.p === i);
  const gutIds = [...new Set(gut.map((g) => g.flag))];
  const bars = gutIds.length ? `<span class="gut">${gutIds.map((id) =>
    `<button type="button" class="sev-${sev(id)}${get(id).decision ? " done" : ""}" data-flag="${id}" aria-label="${id}: whole paragraph"><span>${id}</span></button>`).join("")}</span>` : "";
  const tag = P.kind === "h" ? "h2" : "div";
  const cls = "para" + (P.kind === "list" || P.kind === "table" ? " list" : "") + (P.kind === "q" || P.kind === "cap" || P.kind === "fig" ? " aside" : "");
  return { plain, html: `<${tag} class="${cls}" data-p="${i + 1}"${gutIds.length ? ` data-gutter="${gutIds.join(" ")}"` : ""}><span class="pn">${P.label}</span>${bars}${html}</${tag}>` };
}

function slotHTML(after) {
  return D.slots.filter((s) => s.after === after).map((s) =>
    `<button type="button" class="slot${get(s.flag).decision ? " done" : ""}" data-flag="${s.flag}">${s.flag} · an addition here: ${esc((byId[s.flag] || {}).title || "")}</button>`).join("");
}

function renderText() {
  const plains = [];
  let html = slotHTML(-1);
  D.paras.forEach((_, i) => { const r = paraHTML(i); plains.push(r.plain); html += r.html + slotHTML(i); });
  $("text").innerHTML = html;
  const all = plains.join("\n\n");
  const chars = all.length, words = (all.match(/\S+/g) || []).length;
  let msg = `${chars.toLocaleString("en-GB")} characters · ${words.toLocaleString("en-GB")} words`;
  const L = D.length, el = $("count");
  el.classList.remove("out");
  if (L && (L.min || L.max)) {
    const n = L.unit === "words" ? words : chars;
    msg += ` · ${esc(L.label || "range")} ${(L.min ?? 0).toLocaleString("en-GB")}–${(L.max ?? "").toLocaleString("en-GB")}`;
    if ((L.min && n < L.min) || (L.max && n > L.max)) el.classList.add("out");
  }
  el.textContent = msg;
}

function quoteHTML(f) {
  const p = f.proposal;
  if (p && p.from) return `<div class="quote"><del>${esc(p.from)}</del> → <ins>${esc(p.to ?? "")}</ins></div>`;
  const qs = (f.spans || []).filter((s) => s.quote).map((s) => "“" + esc(s.quote) + "”");
  return qs.length ? `<div class="quote">${qs.join(" · ")}</div>` : "";
}

function whereChip(f) {
  const places = new Set([...D.ranges, ...D.gutter].filter((r) => r.flag === f.id).map((r) => "p" + r.p)
    .concat(D.slots.filter((x) => x.flag === f.id).map((x) => "s" + x.after)));
  if (places.size < 2) return f.where ? `<span class="chip where">${esc(f.where)}</span>` : "";
  return `<button type="button" class="chip where step" data-step="${f.id}" title="Show the next place in the draft">${esc(f.where || places.size + " places")} ↓</button>`;
}

function renderFlags() {
  let html = "", last = null;
  for (const f of D.flags) {
    if (f.severity !== last) {
      html += `<div class="label group-title">${esc(f.severity || "")}</div>`;
      last = f.severity;
    }
    const s = get(f.id), ch = choicesOf(f);
    const choice = (k) => `<button type="button" class="choice" data-flag="${f.id}" data-choice="${k}" aria-pressed="${s.decision === k}">${esc(ch[k])}</button>`;
    const why = WHY.map((w) => `<button type="button" data-flag="${f.id}" data-why="${w}" aria-pressed="${s.why.includes(w)}">${w}</button>`).join("");
    html += `<article class="flag sev-${sev(f.id)}${f.id === pinned ? " on" : ""}" id="flag-${f.id}" data-flag="${f.id}" tabindex="-1">
      <div class="flag-head"><span class="id">${esc(f.id)}</span><span class="chip sev-${sev(f.id)}">${esc(f.severity || "")}</span>${whereChip(f)}${s.decision ? `<span class="chip state">Decided</span>` : ""}</div>
      <h3>${rich(f.title || "")}</h3>
      ${quoteHTML(f)}
      ${f.body ? `<p>${rich(f.body)}</p>` : ""}
      <div class="choices">${choice("accept")}${choice("keep")}${choice("revise")}</div>
      <div class="why"><span>Why:</span>${why}</div>
      <textarea data-flag="${f.id}" aria-label="Note on ${f.id}" placeholder="${esc(f.note || "A note, if you want one.")}">${esc(s.note)}</textarea>
    </article>`;
  }
  $("flags").innerHTML = html;
}

function renderSummary() {
  const done = D.flags.filter((f) => get(f.id).decision).length;
  $("progress").textContent = `${done} of ${D.flags.length} decided`;
  $("table").innerHTML = D.flags.map((f) => {
    const s = get(f.id);
    const d = s.decision ? `${s.decision}: ${esc(choicesOf(f)[s.decision])}` : "Not yet";
    return `<tr><td class="mono">${esc(f.id)}</td><td>${rich(f.title || "")}</td><td class="${s.decision ? "" : "pending"}">${d}</td><td>${esc(s.why.join(", "))}</td><td>${esc(s.note)}</td></tr>`;
  }).join("");
}

function toMarkdown() {
  const cell = (s) => String(s ?? "").replace(/\n+/g, " ").replace(/\|/g, "\\|");
  const rows = D.flags.map((f) => {
    const s = get(f.id);
    const d = s.decision ? `${s.decision}: ${choicesOf(f)[s.decision]}` : "undecided";
    return `| ${f.id} | ${cell(f.title)} | ${cell(d)} | ${cell(s.why.join(", "))} | ${cell(s.note)} |`;
  });
  return [`## Decisions: ${D.title}`, "", `Review: ${D.review}`, "", "| Flag | Question | Decision | Why | Note |", "|---|---|---|---|---|", ...rows].join("\n");
}

function renderAll() {
  const y = scrollY, py = $("pane").scrollTop;
  renderText(); renderFlags(); renderSummary(); paint();
  scrollTo(0, y); $("pane").scrollTop = py;
}

// Two-way linking. The active flag is the hovered card, else the last one chosen.
function paint() {
  const id = hover || pinned;
  document.querySelectorAll(".on").forEach((e) => e.classList.remove("on"));
  if (!id || !byId[id]) return;
  document.querySelectorAll(`[data-flags~="${id}"], .tag[data-flag="${id}"], .gut [data-flag="${id}"], .slot[data-flag="${id}"], #flag-${id}`)
    .forEach((e) => e.classList.add("on"));
}
// Each paragraph or slot a flag touches is one place; a flag in several places steps through them.
function placesOf(id) {
  const seen = new Set(), out = [];
  for (const el of $("pane").querySelectorAll(`mark[data-flags~="${id}"], .gut [data-flag="${id}"], .slot[data-flag="${id}"]`)) {
    const key = el.closest(".para, .slot");
    if (!seen.has(key)) { seen.add(key); out.push(el); }
  }
  return out;
}
function revealInText(id, n = 0, always = false) {
  const pane = $("pane"), t = placesOf(id)[n];
  if (!t) return;
  if (!wide.matches) {
    if (always) t.scrollIntoView({ behavior: calm.matches ? "auto" : "smooth", block: "center" });
    return;
  }
  // Aim for the part of the pane that is on screen: near the end of the page the sticky
  // pane is pushed partly off the top, and the bottom can sit below the fold.
  const pr = pane.getBoundingClientRect(), tr = t.getBoundingClientRect();
  const top = Math.max(pr.top, 0), bottom = Math.min(pr.bottom, innerHeight);
  if (bottom - top < 120) return;
  if (tr.top < top + 48 || tr.bottom > bottom - 48) {
    pane.scrollBy({ top: tr.top - top - (bottom - top) / 3, behavior: calm.matches ? "auto" : "smooth" });
  }
}
function pin(id, fromText) {
  step[id] = 0;
  pinned = id; hover = null; paint();
  if (fromText) {
    const card = $("flag-" + id);
    if (!card) return;
    card.scrollIntoView({ behavior: calm.matches ? "auto" : "smooth", block: "start" });
    card.classList.add("pulse");
    setTimeout(() => card.classList.remove("pulse"), 1100);
  } else {
    revealInText(id);
  }
}

$("flags").addEventListener("mouseover", (e) => {
  const card = e.target.closest(".flag");
  const id = card ? card.dataset.flag : null;
  if (id === hover) return;
  clearTimeout(hoverTimer);
  hover = id; paint();
  if (id) hoverTimer = setTimeout(() => revealInText(id), 160);
});
$("flags").addEventListener("mouseleave", () => { clearTimeout(hoverTimer); hover = null; paint(); });
$("flags").addEventListener("focusin", (e) => {
  const card = e.target.closest(".flag");
  if (card && card.dataset.flag !== pinned) pin(card.dataset.flag, false);
});

document.addEventListener("click", (e) => {
  const c = e.target.closest("[data-choice]");
  if (c) {
    const s = get(c.dataset.flag);
    s.decision = s.decision === c.dataset.choice ? null : c.dataset.choice;
    pinned = c.dataset.flag; renderAll(); persist();
    const again = document.querySelector(`[data-flag="${c.dataset.flag}"][data-choice="${c.dataset.choice}"]`);
    if (again) again.focus({ preventScroll: true });
    return;
  }
  const w = e.target.closest("[data-why]");
  if (w) {
    const s = get(w.dataset.flag), v = w.dataset.why;
    s.why = s.why.includes(v) ? s.why.filter((x) => x !== v) : [...s.why, v];
    w.setAttribute("aria-pressed", s.why.includes(v)); renderSummary(); persist(); return;
  }
  const st = e.target.closest("[data-step]");
  if (st) {
    const id = st.dataset.step, n = placesOf(id).length;
    step[id] = ((step[id] ?? 0) + 1) % n;
    pinned = id; hover = null; paint(); revealInText(id, step[id], true);
    return;
  }
  const t = e.target.closest("#text [data-flag]");
  if (t) { pin(t.dataset.flag, true); return; }
  const m = e.target.closest("#text .hl");
  if (m) { pin(m.dataset.top, true); return; }
  const card = e.target.closest(".flag");
  if (card && card.dataset.flag !== pinned) pin(card.dataset.flag, false);
});
document.addEventListener("input", (e) => {
  if (e.target.matches("textarea[data-flag]")) { get(e.target.dataset.flag).note = e.target.value; renderSummary(); persist(); }
});
$("copy").addEventListener("click", async () => {
  const md = toMarkdown(), btn = $("copy");
  try { await navigator.clipboard.writeText(md); btn.textContent = "Copied"; }
  catch (err) {
    const pre = $("md"); pre.textContent = md;
    const r = document.createRange(); r.selectNodeContents(pre);
    const sel = getSelection(); sel.removeAllRanges(); sel.addRange(r);
    btn.textContent = "Selected: press Copy";
  }
  setTimeout(() => { btn.textContent = "Copy as Markdown"; }, 2200);
});

function setSave(text, err) { const el = $("save"); el.textContent = text; el.classList.toggle("err", !!err); }
function persist() {
  try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {}
  if (!canSave) return;
  clearTimeout(saveTimer);
  setSave("Saving…");
  saveTimer = setTimeout(async () => {
    try { await docRef.set({ flags: state.flags, review: D.review, updatedAt: new Date().toISOString() }); setSave("Saved"); }
    catch (e) { setSave("Not saved. Use Copy as Markdown.", true); }
  }, 700);
}

$("title").textContent = D.title;
document.title = D.title;
$("sub").textContent = `${D.flags.length} flags on ${D.draft}, from ${D.review}. Pick an answer on each; click highlighted text to jump to its flag. `
  + (ARTIFACT ? "Choices save as you go." : "Choices stay in this browser: when you're done, use Copy as Markdown and paste it back.");
if (D.warnings.length) {
  $("warn").innerHTML = `<details class="warn"><summary>${D.warnings.length} anchor${D.warnings.length > 1 ? "s" : ""} to check</summary><ul>${D.warnings.map((w) => `<li>${esc(w)}</li>`).join("")}</ul></details>`;
}
try { const saved = JSON.parse(localStorage.getItem(KEY) || "null"); if (saved && saved.flags) state = saved; } catch (e) {}
renderAll();
setSave(ARTIFACT ? "Connecting…" : "");

// Optional: on claude.ai, publish with capabilities {db: {}} and the decisions save to the artifact's store.
if (ARTIFACT) (async () => {
  let db = null;
  try { db = window.claude && window.claude.use ? await window.claude.use("db") : null; } catch (e) { db = null; }
  if (!db) { setSave("Saving in this browser only. Use Copy as Markdown.", true); return; }
  docRef = db.doc("reviews/" + D.slug);
  try {
    const snap = await docRef.get();
    const d = snap.exists ? snap.data() : null;
    if (d && d.flags) { state = { flags: JSON.parse(JSON.stringify(d.flags)) }; renderAll(); }
    canSave = true;
    setSave(snap.exists ? "Saved" : "Ready: choices save as you go");
  } catch (e) { setSave("Can't reach the store. Use Copy as Markdown.", true); }
})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    sys.exit(main())
