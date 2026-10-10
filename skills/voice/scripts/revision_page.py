#!/usr/bin/env python3
"""Draft and revision page for voice: one draft with its provenance, or two drafts compared.

Standard library only. One self-contained HTML file out, no network calls.

  revision_page.py draft-r1.md                    # the draft, with whose argument each part carries
  revision_page.py draft-r2.md --compare draft-r1.md   # what changed from r1 to r2, and why
  options: -o page.html  --provenance provenance-r1.md [...]  --heading "Post (r2)"

Provenance records (`provenance-r<n>.md`, the format in voice's SKILL.md) are found beside
the draft unless given. Each record line is placed in the draft by the text it quotes; for
each paragraph the newest line that matches wins, so carried-forward records work.

The text helpers below (md_inline, normalise, find_all, reviewed_text) are kept in step with
deslop's scripts/decision_page.py; each skill ships on its own, so they are copied, not shared.
"""

from __future__ import annotations

import argparse
import difflib
import html
import json
import re
import sys
from pathlib import Path

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
INLINE_RE = re.compile(
    r"`([^`]+)`"
    r"|\*\*(.+?)\*\*|__(.+?)__"
    r"|(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])"
    r"|\[([^\]]+)\]\([^)]*\)"
)
LIST_RE = re.compile(r"^\s*([-*+]|\d+[.)])\s+")
SINGLE = {"\u2018": "'", "\u2019": "'", "\u201a": "'", "\u201b": "'", "\u2032": "'",
          "\u201c": '"', "\u201d": '"', "\u201e": '"', "\u2033": '"', "\u00a0": " "}
KIND_NAME = {"hr": "rule", "code": "code block", "h": "heading", "q": "question", "p": "paragraph", "list": "list", "table": "table",
             "img": "image", "fig": "diagram", "cap": "caption"}
ORIGINS = ("source", "author", "drafter", "mixed", "unknown")
ORIGIN_RE = re.compile(r"\b(source|author|drafter|mixed|unknown)\b", re.I)
QUOTE_RE = re.compile(r"[“\"]([^”\"]{3,}?)[”\"]")
TOKEN_RE = re.compile(r"\w+|[^\w\s]|\s+")


class PageError(Exception):
    pass


# ---------------------------------------------------------------- text (kept in step with deslop)

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
    raise PageError(f'heading "{want}" not found in the draft')


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


# ---------------------------------------------------------------- the draft

QUESTION_RE = re.compile(r"^\s*(\*\*)?\[?Q\d+\]?[:.]?(\*\*)?\s")
TABLE_SEP_RE = re.compile(r"^\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")
IMAGE_RE = re.compile(r'^!\[([^\]]*)\]\(\s*<?([^)\s>]+)>?(?:\s+"[^"]*")?\s*\)$')
FIGURE_RE = re.compile(r"^\[(DIAGRAM|FIGURE|IMAGE|CHART|TABLE)\b[:\s]*(.*?)\]$", re.I)


def split_blocks(text: str) -> list[str]:
    """Blank-line-separated blocks, keeping a fenced code block whole even if it holds blank lines."""
    out, cur, fence = [], [], None
    for line in text.strip("\n").splitlines():
        m = re.match(r"^\s*(`{3,}|~{3,})", line)
        if fence is None and m:
            if cur:
                out.append("\n".join(cur)); cur = []
            fence = m.group(1)[0] * len(m.group(1))
            cur.append(line)
            continue
        if fence is not None:
            cur.append(line)
            if line.strip().startswith(fence):
                out.append("\n".join(cur)); cur, fence = [], None
            continue
        if not line.strip():
            if cur:
                out.append("\n".join(cur)); cur = []
        else:
            cur.append(line)
    if cur:
        out.append("\n".join(cur))
    return out


def cells(row: str) -> list[str]:
    return [c.strip() for c in re.split(r"(?<!\\)\|", row.strip().strip("|"))]


def blocks(text: str) -> tuple[str | None, list[dict]]:
    """-> (title, blocks). Numbered as voice records number them: body paragraphs only.
    Headings, blockquotes (inline questions such as "> **[Q1]** …"), tables, images,
    diagram placeholders and captions are unnumbered."""
    title, out, n = None, [], 0
    for raw in split_blocks(text):
        lines = [ln.rstrip() for ln in raw.strip("\n").splitlines()]
        if re.match(r"^\s*(`{3,}|~{3,})", lines[0]):
            # Code: shown as written, unnumbered, never anchored or styled.
            body = "\n".join(lines[1:-1] if len(lines) > 1 and re.match(r"^\s*(`{3,}|~{3,})\s*$", lines[-1]) else lines[1:])
            out.append({"kind": "code", "text": body, "styles": [], "label": ""})
            continue
        if len(lines) == 1 and re.fullmatch(r"\s*([-*_])(\s*\1){2,}\s*", lines[0]):
            out.append({"kind": "hr", "text": "", "styles": [], "label": ""})  # a rule, not a paragraph
            continue
        heading = HEADING_RE.match(lines[0]) if len(lines) == 1 else None
        if heading and len(heading.group(1)) == 1 and title is None and not out:
            title = md_inline(heading.group(2))[0]
            continue
        extra = {}
        first_list = next((k for k, ln in enumerate(lines) if LIST_RE.match(ln)), None)
        if heading:
            kind, src = "h", heading.group(2)
        elif len(lines) >= 2 and all(ln.lstrip().startswith("|") for ln in lines) and TABLE_SEP_RE.match(lines[1]):
            # A table: diffed and anchored by its rows, one row per line of text.
            rows = [[md_inline(c)[0] for c in cells(ln)] for ln in [lines[0]] + lines[2:]]
            kind, extra = "table", {"rows": rows}
            out.append({"kind": kind, "text": "\n".join(" | ".join(r) for r in rows), "styles": [], "label": "", **extra})
            continue
        elif len(lines) == 1 and IMAGE_RE.match(lines[0]):
            m = IMAGE_RE.match(lines[0])
            out.append({"kind": "img", "text": f"![{m.group(1)}]({m.group(2)})", "styles": [], "label": "",
                        "alt": m.group(1), "src": m.group(2)})
            continue
        elif len(lines) == 1 and FIGURE_RE.match(lines[0]):
            out.append({"kind": "fig", "text": lines[0], "styles": [], "label": "",
                        "alt": FIGURE_RE.match(lines[0]).group(2) or FIGURE_RE.match(lines[0]).group(1)})
            continue
        elif all(ln.lstrip().startswith(">") for ln in lines):
            kind, src = "q", " ".join(ln.lstrip()[1:].strip() for ln in lines)
        elif QUESTION_RE.match(lines[0]):
            kind, src = "q", " ".join(ln.strip() for ln in lines)  # "[Q1] …" or "**Q1:** …" without the quote mark
        elif first_list is not None and all(LIST_RE.match(ln) or ln.startswith((" ", "\t")) for ln in lines[first_list:]):
            # A list, perhaps led in by a line of prose: keep the line breaks.
            lead = " ".join(ln.strip() for ln in lines[:first_list])
            kind, src = "list", "\n".join(([lead] if lead else []) + [ln.strip() for ln in lines[first_list:]])
        else:
            kind, src = "p", " ".join(ln.strip() for ln in lines)
            if re.fullmatch(r"\*(?!\*)[^*].*[^*]\*", src) or re.fullmatch(r"_[^_].*[^_]_", src):
                kind = "cap"  # an italic line on its own: a caption
        plain, styles = md_inline(src)
        label = ""
        if kind in ("p", "list"):
            n += 1
            label = f"¶{n}"
        out.append({"kind": kind, "text": plain, "styles": styles, "label": label})
    return title, out


def embed_images(bl: list[dict], base: Path) -> None:
    """Images beside the draft go into the page as data, so it still works on its own."""
    import base64, mimetypes
    for b in bl:
        if b["kind"] != "img" or re.match(r"^(https?:|data:)", b["src"]):
            continue
        f = (base / b["src"]).resolve()
        mime = mimetypes.guess_type(f.name)[0] or ""
        if f.is_file() and mime.startswith("image/") and f.stat().st_size <= 4_000_000:
            b["data"] = f"data:{mime};base64," + base64.b64encode(f.read_bytes()).decode()
        else:
            b["missing"] = True


def load_draft(path: Path, heading: str | None) -> tuple[str | None, list[dict]]:
    title, bl = blocks(reviewed_text(path.read_text(encoding="utf-8"), heading))
    embed_images(bl, path.parent)
    if not bl:
        raise PageError(f"{path.name}: no text found")
    return title, bl


def revision_of(path: Path) -> int | None:
    m = re.search(r"-r(\d+)\b", path.stem)
    return int(m.group(1)) if m else None


# ---------------------------------------------------------------- provenance records

def parse_record(path: Path) -> list[dict]:
    """Lenient: a line is a record entry if it quotes draft text. The key (before the first |)
    holds ¶n and the quote; the rest holds origin, approval and any question asked."""
    rev = revision_of(path)
    text = path.read_text(encoding="utf-8")
    body = text.split("\n---", 2)[-1] if text.startswith("---") else text
    entries = []
    for line in body.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.lower().startswith("key:"):
            continue
        bullet = bool(re.match(r"^[-*]\s+", line))
        if not (bullet or "|" in line or line.startswith("¶")):
            continue  # prose in the record's header or notes, not an entry
        line = re.sub(r"^[-*]\s+", "", line)
        key, _, rest = line.partition("|")
        quotes = QUOTE_RE.findall(key)
        if not quotes:
            continue
        para = re.search(r"¶\s*(\d+)", key)
        arrow = "→" in key or "->" in key
        anchor = quotes[-1] if arrow else quotes[0]
        segments = [s.strip() for s in rest.split("|") if s.strip()]
        origin = None
        for seg in segments or [key]:
            m = ORIGIN_RE.search(seg)
            if m and not seg.lower().startswith(("approval", "question")):
                origin = m.group(1).lower()
                break
        approval = next((s for s in segments if s.lower().startswith("approval")), "")
        approval = re.sub(r"^approval:\s*", "", approval, flags=re.I)
        if approval in ("—", "-", "–"):
            approval = ""
        question = next((s for s in segments if re.match(r"(question|flag)", s, re.I)), "")
        detail = " | ".join(s for s in segments if s not in (approval, question)
                            and not s.lower().startswith("approval"))
        entries.append({
            "rev": rev, "file": path.name, "para": int(para.group(1)) if para else None,
            # A line may also quote its source (a dictation, a chat message): every quote is a candidate.
            "quote": anchor, "candidates": [anchor] + ([] if arrow else [q for q in quotes[1:]]),
            "from": quotes[0] if arrow else None,
            "added": bool(re.search(r"\bNEW\b|¶\s*\d+\s*\+|^\+", key)),
            "removed": "REMOVED" in line, "origin": origin, "approval": approval,
            "question": question, "detail": detail or rest.strip(), "line": line,
        })
    return entries


def records_for(draft: Path, upto: int | None, given: list[Path] | None) -> list[Path]:
    if given:
        return given
    found = []
    for p in draft.parent.glob("provenance-r*.md"):
        r = revision_of(p)
        if r is not None and (upto is None or r <= upto):
            found.append(p)
    return sorted(found, key=revision_of)


def locate_in(quote: str, bl: list[dict], hint: int | None):
    """-> (block index, start, end) or None. Tries the trailing ellipsis off, and the hinted ¶ first."""
    cands = [quote]
    trimmed = re.sub(r"^\s*(…|\.\.\.|\+)\s*|\s*(…|\.\.\.)\s*$", "", quote).strip()
    if trimmed != quote and trimmed:
        cands.append(trimmed)
    head = re.split(r"…|\.\.\.", trimmed)[0].strip()
    if head != trimmed and len(head) >= 12:
        cands.append(head)  # "start… end" anchors on its start
    order = list(range(len(bl)))
    if hint is not None:
        hinted = [i for i, b in enumerate(bl) if b["label"] == f"¶{hint}"]
        order = hinted + [i for i in order if i not in hinted]
    for fold in (False, True):
        for cand in cands:
            for i in order:
                hits = find_all(cand, bl[i]["text"], fold)
                if hits:
                    return i, hits[0][0], hits[0][1]
    return None


# ---------------------------------------------------------------- comparing two drafts

def tokens(s: str) -> list[str]:
    return TOKEN_RE.findall(s)


def word_diff(old: str, new: str) -> list[list]:
    """-> [[kind, text, offset-in-new or None]], kind in eq / ins / del."""
    a, b = tokens(old), tokens(new)
    out, pos = [], 0
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal":
            t = "".join(b[j1:j2]); out.append(["eq", t, pos]); pos += len(t)
            continue
        if op in ("delete", "replace"):
            out.append(["del", "".join(a[i1:i2]), None])
        if op in ("insert", "replace"):
            t = "".join(b[j1:j2]); out.append(["ins", t, pos]); pos += len(t)
    # Whitespace-only changes read as noise: show them as unchanged.
    clean = []
    for k, t, off in out:
        if k != "eq" and not t.strip():
            if k == "del":
                continue
            k = "eq"
        if clean and clean[-1][0] == k and k != "del" and clean[-1][2] is not None:
            clean[-1][1] += t
        else:
            clean.append([k, t, off])
    # One edit per run of changes that only spaces separate: "each joist" -> "the four flagged
    # joists", not two fragments. Within a run, the old words come first, then the new.
    out, k = [], 0
    while k < len(clean):
        if clean[k][0] == "eq":
            out.append(clean[k]); k += 1
            continue
        run = [clean[k]]; k += 1
        while k < len(clean) and (clean[k][0] != "eq" or (not clean[k][1].strip() and k + 1 < len(clean) and clean[k + 1][0] != "eq")):
            if clean[k][0] == "eq":
                run += [["del", clean[k][1], None], ["ins", clean[k][1], clean[k][2]]]
            else:
                run.append(clean[k])
            k += 1
        dels = "".join(t for kk, t, _ in run if kk == "del")
        ins = [(t, off) for kk, t, off in run if kk == "ins"]
        if dels:
            out.append(["del", dels, None])
        if ins:
            out.append(["ins", "".join(t for t, _ in ins), ins[0][1]])
    return out


def family(b: dict) -> str:
    """Blocks that can be one another's earlier version: prose with prose, and each other kind with itself."""
    return "prose" if b["kind"] in ("p", "list") else b["kind"]


def align(old: list[dict], new: list[dict]):
    """Pair paragraphs of rM with rN. -> list of (old index or None, new index or None)."""
    key = lambda b: normalise(b["text"])[0]
    a, b = [key(x) for x in old], [key(x) for x in new]
    pairs = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal":
            pairs += [(i1 + k, j1 + k) for k in range(i2 - i1)]
            continue
        olds, news = list(range(i1, i2)), list(range(j1, j2))
        matched = {}
        for j in news:  # greedy, in order, so changed paragraphs pair with their earlier selves
            best, score = None, 0.45
            for i in olds:
                if i in matched.values() or (matched and i < max(matched.values())):
                    continue
                if family(old[i]) != family(new[j]):
                    continue  # a question never pairs with a paragraph, nor a table with a caption
                r = difflib.SequenceMatcher(None, a[i], b[j], autojunk=False).ratio()
                if r > score:
                    best, score = i, r
            if best is not None:
                matched[j] = best
        pending = list(olds)
        for j in news:
            if j in matched:
                i = matched[j]
                for x in [x for x in pending if x < i]:
                    pairs.append((x, None)); pending.remove(x)
                pairs.append((i, j)); pending.remove(i)
            else:
                pairs.append((None, j))
        pairs += [(x, None) for x in pending]
    return pairs


# ---------------------------------------------------------------- building the page data

def row_diff(old_rows: list[list[str]], new_rows: list[list[str]]) -> list[dict]:
    """A changed table, row by row: kept, added (ins) or cut (del). A changed row is a cut and an add."""
    key = lambda r: normalise(" | ".join(r))[0]
    out = []
    sm = difflib.SequenceMatcher(None, [key(r) for r in old_rows], [key(r) for r in new_rows], autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            out += [{"k": "eq", "cells": r} for r in new_rows[j1:j2]]
            continue
        out += [{"k": "del", "cells": r} for r in old_rows[i1:i2]]
        out += [{"k": "ins", "cells": r} for r in new_rows[j1:j2]]
    return out


def media(b: dict) -> dict:
    """What the page needs to draw a table, image or diagram placeholder."""
    keep = {k: b[k] for k in ("rows", "rowdiff", "alt", "src", "data", "missing") if k in b}
    if "was" in b:
        keep["was"] = {k: b["was"][k] for k in ("alt", "src", "data", "text") if k in b["was"]}
    return keep


def split_pieces(pieces: list[list], bounds: set[int]) -> list[list]:
    out = []
    for k, t, off in pieces:
        if off is None:
            out.append([k, t, None]); continue
        cuts = sorted(c for c in bounds if off < c < off + len(t))
        prev = off
        for c in cuts + [off + len(t)]:
            out.append([k, t[prev - off:c - off], prev]); prev = c
    return out


def decorate(block: dict, pieces: list[list], anchors: list[tuple[int, int, str]]) -> list[dict]:
    bounds = {s for s, _, _ in block["styles"]} | {e for _, e, _ in block["styles"]}
    bounds |= {s for s, _, _ in anchors} | {e for _, e, _ in anchors}
    out = []
    for k, t, off in split_pieces(pieces, bounds):
        if not t:
            continue
        st = [] if off is None else [s for a, b, s in block["styles"] if a <= off and off + len(t) <= b]
        an = [] if off is None else [c for a, b, c in anchors if a <= off and off + len(t) <= b]
        out.append({"k": k, "t": t, "st": st, "a": an})
    return out


def build(draft: Path, compare: Path | None, provenance: list[Path] | None, heading: str | None,
          compare_heading: str | None = None) -> dict:
    title, new = load_draft(draft, heading)
    rev_n = revision_of(draft)
    old, rev_m, old_title = None, None, None
    if compare:
        old_title, old = load_draft(compare, compare_heading if compare_heading is not None else heading)
        rev_m = revision_of(compare)
    warnings, cards, anchors = [], [], {i: [] for i in range(len(new))}
    para_cards = {i: [] for i in range(len(new))}
    origin_of = {}

    # Provenance: newest paragraph-level line per paragraph; every sentence-level line.
    recs = records_for(draft, rev_n, provenance)
    entries = [e for p in recs for e in parse_record(p)]
    placed_para, unplaced = {}, []
    for e in entries:
        hit = None
        for cand in e["candidates"]:
            hit = locate_in(cand, new, e["para"])
            if hit:
                e["quote"] = cand
                break
        if hit is None:
            if old is not None:
                for cand in e["candidates"]:
                    was = locate_in(cand, old, e["para"])
                    if was:
                        e["in_old"], e["old_block"] = True, was[0]
                        break
            unplaced.append(e)
            continue
        i, s, en = hit
        e["block"], e["span"] = i, (s, en)
        whole = s == 0 and (en >= len(new[i]["text"]) - 1 or e["quote"].rstrip().endswith(("…", "...")))
        e["level"] = "para" if (whole or (s == 0 and not e["added"] and not e["from"])) else "inline"
        if e["level"] == "para":
            prev = placed_para.get(i)
            if prev is None or (e["rev"] or 0) >= (prev["rev"] or 0):
                placed_para[i] = e
    show_from = rev_m if compare else None  # in compare mode, the lines that explain this change

    def card_for(e, cid):
        chips = []
        if e["origin"]:
            chips.append(["origin-" + e["origin"], e["origin"]])
        if e["approval"]:
            chips.append(["ok", "approved"])
        if e["question"]:
            chips.append(["ask", "question"])
        if e["rev"] is not None:
            chips.append(["rev", f"r{e['rev']}"])
        return {"id": cid, "kind": "record", "title": e["quote"], "chips": chips,
                "body": e["detail"], "approval": e["approval"], "question": e["question"],
                "level": e.get("level"), "file": e["file"]}

    n = 0
    for i, e in sorted(placed_para.items()):
        origin_of[i] = e["origin"]
        if compare and (e["rev"] or 0) <= (show_from or 0):
            continue
        n += 1
        cid = f"r{n}"
        cards.append(card_for(e, cid) | {"block": i})
        para_cards[i].append(cid)
    for e in entries:
        if e.get("level") != "inline":
            continue
        if compare and (e["rev"] or 0) <= (show_from or 0):
            continue
        n += 1
        cid = f"r{n}"
        cards.append(card_for(e, cid) | {"block": e["block"]})
        anchors[e["block"]].append((e["span"][0], e["span"][1], cid))

    # Questions written into the draft (blockquotes such as "> [Q1] …").
    for i, b in enumerate(new):
        if b["kind"] == "q":
            n += 1
            cid = f"q{n}"
            m = re.match(r"\s*\[?(Q\d+)\]?", b["text"])
            cards.append({"id": cid, "kind": "question", "title": m.group(1) if m else "Question in the draft",
                          "chips": [["ask", "question"]], "body": b["text"], "block": i})
            para_cards[i].append(cid)

    # Paragraphs and pieces, with the comparison if there is one.
    paras = []
    if old is None:
        for i, b in enumerate(new):
            pieces = decorate(b, [["eq", b["text"], 0]], anchors[i])
            paras.append({"i": i, "kind": b["kind"], "label": b["label"], "status": "same",
                          "origin": origin_of.get(i), "cards": para_cards[i], "pieces": pieces, **media(b)})
    else:
        pairs = align(old, new)
        # A removed paragraph that reappears unchanged elsewhere has moved.
        removed_text = {normalise(old[i]["text"])[0]: i for i, j in pairs if j is None}
        moved = {}
        for i, j in pairs:
            if i is None and normalise(new[j]["text"])[0] in removed_text:
                moved[j] = removed_text[normalise(new[j]["text"])[0]]
        moved_old = set(moved.values())
        changes = 0
        for i, j in pairs:
            if j is None:
                if i in moved_old:
                    continue
                b = old[i]
                changes += 1
                cid = f"c{changes}"
                cards.append({"id": cid, "kind": "change", "status": "removed", "title": f"Removed: {b['label'] or KIND_NAME[b['kind']]}",
                              "record": [e["detail"] or e["line"] for e in unplaced if e.get("old_block") == i
                                         and (e["rev"] or 0) > (rev_m or 0)],
                              "chips": [["del", "removed"]], "old": b["text"], "words": [len(b["text"].split()), 0]})
                paras.append({"i": None, "kind": b["kind"], "label": f"r{rev_m} {b['label']}".strip(), "status": "removed",
                              "origin": None, "cards": [cid], "pieces": [{"k": "del", "t": b["text"], "st": [], "a": []}], **media(b)})
                continue
            b = new[j]
            if i is None and j in moved:
                o = old[moved[j]]
                status, pieces = "moved", [["eq", b["text"], 0]]
            elif i is None:
                status, pieces = "new", [["ins", b["text"], 0]]
            elif b["kind"] in ("table", "img", "fig") or old[i]["kind"] in ("table", "img", "fig"):
                o = old[i]
                pieces = [["eq", b["text"], 0]]
                status = "same" if normalise(o["text"])[0] == normalise(b["text"])[0] else "changed"
                if status == "changed" and b["kind"] == "table" and o["kind"] == "table":
                    b = dict(b, rowdiff=row_diff(o["rows"], b["rows"]))
                elif status == "changed":
                    b = dict(b, was=o)
            else:
                o = old[i]
                pieces = word_diff(o["text"], b["text"])
                status = "same" if all(p[0] == "eq" for p in pieces) else "changed"
            cids = list(para_cards[j])
            if status != "same":
                changes += 1
                cid = f"c{changes}"
                ow = len((old[i] if i is not None else old[moved[j]] if j in moved else {"text": ""})["text"].split())
                nw = len(b["text"].split())
                label = {"changed": "Changed", "new": "New", "moved": "Moved"}[status]
                chip = {"changed": ["chg", "changed"], "new": ["ins", "new"], "moved": ["mov", "moved"]}[status]
                card = {"id": cid, "kind": "change", "status": status, "title": f"{label}: {b['label'] or b['kind']}",
                        "chips": [chip], "words": [ow, nw], "block": j, "preview": b["text"],
                        "from": (old[moved[j]]["label"] if j in moved else old[i]["label"] if i is not None else "")}
                card["why"] = [c["id"] for c in cards if c.get("block") == j and c["kind"] == "record"]
                cards.append(card)
                cids.insert(0, cid)
            paras.append({"i": j, "kind": b["kind"], "label": b["label"], "status": status,
                          "origin": origin_of.get(j), "cards": cids, "pieces": decorate(b, pieces, anchors[j]),
                          "from": (old[moved[j]]["label"] if j in moved else ""), **media(b)})
        number_changes(paras, cards)
        folded = {rid: c["id"] for c in cards if c["kind"] == "change" for rid in c.get("why", [])}
        for c in cards:
            if c["kind"] == "change" and c.get("why"):
                c["record"] = [next(x for x in cards if x["id"] == rid)["body"] or next(x for x in cards if x["id"] == rid)["title"]
                               for rid in c["why"]]
                c["why"] = []
        # Comparing is about what changed: a record line that explains no change has no card.
        cards[:] = [c for c in cards if c["id"] not in folded and c["kind"] != "record"]
        kept = {c["id"] for c in cards}
        for p in paras:
            for piece in p["pieces"]:
                piece["a"] = [cid for cid in piece["a"] if cid in kept or cid in folded]
        for p in paras:
            p["cards"] = list(dict.fromkeys(folded.get(cid, cid) for cid in p["cards"]))
            for piece in p["pieces"]:
                piece["a"] = list(dict.fromkeys(folded.get(cid, cid) for cid in piece["a"]))
        # Order cards as the text runs: each change, then the records that explain it.
        order = {cid: k for k, p in enumerate(paras) for cid in p["cards"]}
        for p_i, p in enumerate(paras):
            for piece in p["pieces"]:
                for cid in piece["a"]:
                    order.setdefault(cid, p_i)
        cards.sort(key=lambda c: (order.get(c["id"], 1e9), 0 if c["kind"] == "change" else 1))

    # Older lines quoting text since rewritten are history, not a fault: warn only about lines
    # from the records that describe this draft (its own, or every one since rM when comparing).
    latest = max((e["rev"] or 0 for e in entries), default=0)
    history = 0
    for e in unplaced:
        current = (e["rev"] or 0) > (show_from or 0) if compare else (e["rev"] or 0) == latest
        if not current:
            history += 1
        elif not e.get("in_old"):  # a line about text this revision removed is covered by the removal's card
            warnings.append(f'{e["file"]}: "{e["quote"][:70]}" not found in r{rev_n}')
    if old is None:
        cards.sort(key=lambda c: (c.get("block", 1e9), 0 if c.get("level") == "para" else 1))

    def words(bl):
        return sum(len(b["text"].split()) for b in bl if b["kind"] != "q")
    origins = {}
    for i, b in enumerate(new):
        if b["kind"] in ("p", "list"):
            key = origin_of.get(i) or "no record"
            origins[key] = origins.get(key, 0) + 1
    return {
        "title": title or draft.stem, "draft": draft.name, "rev": rev_n,
        "compare": compare.name if compare else None, "rev_old": rev_m,
        "records": [p.name for p in recs], "history": history, "paras": paras, "cards": cards, "warnings": warnings,
        "stats": {"words": words(new), "words_old": words(old) if old else None, "origins": origins,
                  "paragraphs": sum(1 for b in new if b["kind"] in ("p", "list"))},
        "slug": re.sub(r"[^a-z0-9]+", "-", f"{title or draft.stem} {draft.stem} {compare.stem if compare else ''}".lower()).strip("-"),
    }


def number_changes(paras: list[dict], cards: list[dict]) -> None:
    """Number every edit in reading order, so the author can say "change 3" to whoever revises it.
    A changed paragraph holds one number per run of edits; a new, moved or removed one holds one."""
    by_id = {c["id"]: c for c in cards}
    n = 0
    for p in paras:
        if p["status"] == "same":
            continue
        card = next((by_id[c] for c in p["cards"] if by_id.get(c, {}).get("kind") == "change"), None)
        nums, edits = [], []
        if p["status"] == "changed" and p.get("rowdiff"):
            prev = None
            for row in p["rowdiff"]:
                if row["k"] == "eq":
                    prev = None
                    continue
                if prev is None:
                    n += 1; nums.append(n); edits.append({"n": n, "del": "", "ins": "", "after": "", "table": True}); prev = n
                row["h"] = prev
                edits[-1][row["k"]] += ("; " if edits[-1][row["k"]] else "") + " | ".join(row["cells"])
        elif p["status"] == "changed" and p["kind"] in ("img", "fig"):
            n += 1; nums.append(n)
            edits.append({"n": n, "del": (p.get("was") or {}).get("text", ""), "ins": p["pieces"][0]["t"] if p["pieces"] else "", "after": ""})
        elif p["status"] == "changed":
            prev, before = None, ""
            for piece in p["pieces"]:
                if piece["k"] == "eq":
                    prev, before = None, (before + piece["t"])[-60:]
                    continue
                if piece["k"] == "ins":
                    before = (before + piece["t"])[-60:]  # context is the new text, edits included
                if prev is None:
                    # The few words before an edit say where it is, which a short edit can't.
                    after = " ".join((before[:-len(piece["t"])] if piece["k"] == "ins" else before).split()[-3:])
                    n += 1; nums.append(n); edits.append({"n": n, "del": "", "ins": "", "after": after}); prev = n
                piece["h"] = prev
                edits[-1][piece["k"]] += piece["t"]
        else:
            n += 1; nums.append(n)
            for piece in p["pieces"]:
                piece["h"] = n
        p["hunks"] = nums
        if card:
            name = p["label"] if "¶" in p["label"] else KIND_NAME.get(p["kind"], p["kind"])
            what = {"changed": f"{name} changed", "new": f"{name} new",
                    "moved": f"{name} moved from {p.get('from') or 'earlier'}", "removed": f"{p['label'] if '¶' in p['label'] else card['title'].split(': ', 1)[-1]} removed"}[p["status"]]
            nums_txt = f"Change {nums[0]}" if len(nums) == 1 else f"Changes {nums[0]}–{nums[-1]}"
            card.update({"hunks": nums, "edits": edits, "title": f"{nums_txt} · {what}"})


def change_list(data: dict) -> str:
    """The numbered changes as plain text, for an assistant resolving "change 3"."""
    clip = lambda t, k=90: (t[:k] + "…") if len(t) > k else t
    lines = [f"Changes from {data['compare']} to {data['draft']}:"]
    for c in data["cards"]:
        if c["kind"] != "change":
            continue
        if c.get("edits"):
            for e in c["edits"]:
                where = c["title"].split(" · ", 1)[1].replace(" changed", "")
                old, new = clip(e["del"].strip()), clip(e["ins"].strip())
                body = f'"{old}" → "{new}"' if old and new else f'added "{new}"' if new else f'cut "{old}"'
                if e.get("after") and len((old + " " + new).split()) <= 6:
                    body = f'after "{e["after"]}", {body}'
                lines.append(f"{e['n']:>3}  {where}: {body}")
        else:
            text = c.get("old") or next((p for p in [c.get("preview", "")]), "")
            lines.append(f"{c['hunks'][0]:>3}  {c['title'].split(' · ', 1)[1]}" + (f': "{clip(text)}"' if text else ""))
    return "\n".join(lines)


def render(data: dict) -> str:
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    return PAGE.replace("__TITLE__", html.escape(data["title"])).replace("__DATA__", payload)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("draft", type=Path, help="the draft to show (draft-r<n>.md)")
    ap.add_argument("--compare", type=Path, help="an earlier draft to compare against (default: draft-r<n-1>.md beside it, if there is one)")
    ap.add_argument("--alone", action="store_true", help="show the draft on its own, with its provenance, even if an earlier one exists")
    ap.add_argument("--list", action="store_true", help="print the numbered changes as text instead of writing a page")
    ap.add_argument("--provenance", type=Path, nargs="+", help="records to use (default: provenance-r*.md beside the draft, up to its revision)")
    ap.add_argument("--heading", help="section of the drafts to show, if they hold more than the piece")
    ap.add_argument("--compare-heading", help="the earlier draft's section, if it differs (two revisions in one file)")
    ap.add_argument("-o", "--out", type=Path, help="default: <draft>.html beside the draft")
    args = ap.parse_args(argv)
    rev = revision_of(args.draft)
    if not args.compare and not args.alone and rev and rev > 1:
        prev = args.draft.with_name(re.sub(rf"-r{rev}\b", f"-r{rev - 1}", args.draft.name))
        if prev.exists():
            args.compare = prev
    if args.list and not args.compare:
        print("error: --list needs an earlier draft to compare with", file=sys.stderr)
        return 2
    try:
        data = build(args.draft, args.compare, args.provenance, args.heading, args.compare_heading)
    except (PageError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.list:
        print(change_list(data))
        return 0
    for w in data["warnings"]:
        print(f"warning: {w}", file=sys.stderr)
    out = args.out or args.draft.with_name(args.draft.stem + (f"-vs-{args.compare.stem}" if args.compare else "") + ".html")
    out.write_text(render(data), encoding="utf-8")
    kinds = {}
    for c in data["cards"]:
        kinds[c.get("status") or c["kind"]] = kinds.get(c.get("status") or c["kind"], 0) + 1
    print(f"{out} ({', '.join(f'{v} {k}' for k, v in kinds.items()) or 'no cards'}; "
          f"{len(data['records'])} records, {len(data['warnings'])} unplaced lines)")
    return 0


PAGE = r"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
/* The draft sits in its own scrolling pane on the left; the cards scroll with the page on the right. One column below 900px. */
:root {
  --bg: #f5f6f8; --surface: #ffffff; --ink: #18202c; --muted: #5b6676; --line: #dde2ea;
  --accent: #1f4fbf; --accent-soft: #e6ecfa;
  --theirs: #1d7a4c; --theirs-soft: #e2f3ea;
  --drafter: #1f4fbf; --drafter-soft: #e6ecfa;
  --mixed: #8a6a12; --mixed-soft: #f8f0d9;
  --none: #98a3b3;
  --ins: #dcf2e4; --ins-ink: #14532d; --del: #fbe4de; --del-ink: #8a2a17;
  --ask: #b4361f; --ask-soft: #fbe4de;
  --font-read: Charter, "Iowan Old Style", "Palatino Linotype", Georgia, serif;
  --font-ui: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --font-mono: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #12161d; --surface: #1a2029; --ink: #e5e9f0; --muted: #98a3b3; --line: #2c3442;
    --accent: #8fb0ff; --accent-soft: #1f2b45;
    --theirs: #6fd3a0; --theirs-soft: #173126; --drafter: #8fb0ff; --drafter-soft: #1f2b45;
    --mixed: #e0c26a; --mixed-soft: #342c14; --none: #5b6676;
    --ins: #173a26; --ins-ink: #9be3b9; --del: #3a211c; --del-ink: #f4a593;
    --ask: #f08a74; --ask-soft: #3a211c; color-scheme: dark;
  }
}
:root[data-theme="dark"] {
  --bg: #12161d; --surface: #1a2029; --ink: #e5e9f0; --muted: #98a3b3; --line: #2c3442;
  --accent: #8fb0ff; --accent-soft: #1f2b45;
  --theirs: #6fd3a0; --theirs-soft: #173126; --drafter: #8fb0ff; --drafter-soft: #1f2b45;
  --mixed: #e0c26a; --mixed-soft: #342c14; --none: #5b6676;
  --ins: #173a26; --ins-ink: #9be3b9; --del: #3a211c; --del-ink: #f4a593;
  --ask: #f08a74; --ask-soft: #3a211c; color-scheme: dark;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--ink); font-family: var(--font-ui); font-size: 15px; line-height: 1.5; }
.wrap { max-width: 1280px; margin: 0 auto; padding: 24px 16px 64px; }
@media (min-width: 600px) { .wrap { padding-inline: 24px; } }
header.top { display: flex; flex-wrap: wrap; align-items: end; justify-content: space-between; gap: 12px 20px; margin-bottom: 16px; }
h1 { font-family: var(--font-read); font-weight: 500; font-size: 28px; line-height: 1.15; margin: 0 0 6px; text-wrap: balance; }
.sub { color: var(--muted); margin: 0; max-width: 70ch; }
.stats { display: flex; flex-wrap: wrap; gap: 6px 16px; font-size: 13px; color: var(--muted); font-variant-numeric: tabular-nums; margin: 0 0 14px; }
.stats b { color: var(--ink); font-weight: 600; }
button { font: inherit; cursor: pointer; }
.btn { border: 1px solid var(--line); background: var(--surface); color: var(--ink); border-radius: 6px; padding: 6px 11px; font-size: 14px; }
.btn:hover { border-color: var(--accent); }
.status { display: flex; gap: 8px; flex-wrap: wrap; justify-content: flex-end; }
.seg { display: inline-flex; border: 1px solid var(--line); border-radius: 7px; overflow: hidden; }
.seg button { border: 0; background: var(--surface); color: var(--ink); padding: 6px 11px; font-size: 13.5px; }
.seg button + button { border-left: 1px solid var(--line); }
.seg button[aria-pressed="true"] { background: var(--accent); color: var(--surface); }
:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.warn { background: var(--mixed-soft); border: 1px solid var(--line); border-radius: 8px; padding: 8px 12px; margin-bottom: 14px; font-size: 13.5px; }
.warn summary { cursor: pointer; font-weight: 600; }
.warn ul { margin: 6px 0 0; padding-left: 20px; }

.grid { display: grid; grid-template-columns: minmax(0, 1.1fr) minmax(0, 1fr); gap: 24px; align-items: start; }
.pane { position: sticky; top: 12px; max-height: calc(100vh - 24px); overflow: auto; overscroll-behavior: contain;
  background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 18px 20px 18px 52px; min-width: 0; }
@media (max-width: 900px) { .grid { grid-template-columns: minmax(0, 1fr); } .pane { position: static; max-height: none; overflow: visible; } }
.pane-head { display: flex; justify-content: space-between; gap: 8px 12px; flex-wrap: wrap; align-items: center; margin: 0 0 14px -32px; }
.label { font-size: 12px; letter-spacing: .06em; text-transform: uppercase; color: var(--muted); font-weight: 600; }
.blk { position: relative; font-family: var(--font-read); font-size: 18px; line-height: 1.6; margin: 0 0 14px; max-width: 66ch; border-radius: 4px; overflow-wrap: anywhere; }  /* long URLs and paths wrap rather than push the page wide */
.blk.list { white-space: pre-line; }
.blk hr { border: 0; border-top: 1px solid var(--line); margin: 6px 0; }
.blk.code { font-family: var(--font-mono); font-size: 13px; line-height: 1.5; white-space: pre-wrap; background: var(--bg); border: 1px solid var(--line); border-radius: 6px; padding: 8px 10px; overflow-wrap: anywhere; }
.blk.h { font-size: 21px; font-weight: 600; line-height: 1.3; margin-top: 22px; }
.blk.q { font-family: var(--font-ui); font-size: 15px; background: var(--ask-soft); border-left: 3px solid var(--ask); padding: 6px 10px; cursor: pointer; }
.blk code { font-family: var(--font-mono); font-size: .82em; background: var(--accent-soft); padding: 1px 4px; border-radius: 3px; }
.pn { position: absolute; left: -48px; top: 6px; width: 30px; text-align: right; font-family: var(--font-mono); font-size: 11px; line-height: 1.2; color: var(--muted); }
/* Origin: a bar in the margin, with its initial as text so colour is never the only signal. */
.og { position: absolute; left: -12px; top: 4px; bottom: 4px; width: 5px; border-radius: 3px; border: 0; padding: 0; background: var(--none); }
.og span { position: absolute; top: 18px; right: 9px; font-family: var(--font-mono); font-size: 10px; color: var(--muted); }
.og.o-author, .og.o-source { background: var(--theirs); }
.og.o-drafter { background: var(--drafter); }
.og.o-mixed { background: repeating-linear-gradient(180deg, var(--theirs) 0 6px, var(--drafter) 6px 12px); }
.blk.on { box-shadow: 0 0 0 2px var(--accent-soft); background: color-mix(in srgb, var(--accent-soft) 45%, transparent); }
.blk.on .og { box-shadow: 0 0 0 2px var(--accent); }
.blk.removed { opacity: .85; }
.blk .tagline { display: block; font-family: var(--font-ui); font-size: 12px; color: var(--muted); }
ins, del { text-decoration: none; border-radius: 3px; padding: 0 1px; }
ins { background: var(--ins); color: var(--ins-ink); }
del { background: var(--del); color: var(--del-ink); text-decoration: line-through; text-decoration-thickness: 1px; }
del + ins, ins + del { margin-left: 2px; }  /* keep a replaced word and its replacement apart */
.v-new del, .v-new .blk.removed { display: none; }
.v-new ins { background: none; color: inherit; }
.v-old ins, .v-old .blk.new { display: none; }
.v-old del { background: none; color: inherit; text-decoration: none; }
.v-old .blk.removed { opacity: 1; }
.an { border-bottom: 2px dotted var(--muted); cursor: pointer; }
.hk { font-family: var(--font-mono); font-size: 10.5px; font-weight: 600; line-height: 1; vertical-align: super; color: var(--surface);
  background: var(--accent); border: 0; border-radius: 8px; padding: 1px 5px; margin-left: 2px; }
.tagline .hk { vertical-align: 1px; margin: 0 4px 0 0; }
.v-new .hk, .v-old .hk { display: none; }
.card ol.edits { margin: 6px 0; padding-left: 26px; font-family: var(--font-read); font-size: 14.5px; }
.card ol.edits li { margin: 2px 0; }
.card ol.edits li::marker { font-family: var(--font-mono); font-size: 12px; color: var(--accent); font-weight: 600; }
.an.on { background: var(--accent-soft); border-bottom-color: var(--accent); }
.tw { overflow-x: auto; }
.blk.table { max-width: none; font-family: var(--font-ui); font-size: 14px; line-height: 1.4; }
.blk table { border-collapse: collapse; width: 100%; font-variant-numeric: tabular-nums; }
.blk th, .blk td { padding: 5px 8px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }
.blk th { font-size: 12px; color: var(--muted); font-weight: 600; }
.blk tr.ins td, .blk tr.ins th { background: var(--ins); color: var(--ins-ink); }
.blk tr.del td, .blk tr.del th { background: var(--del); color: var(--del-ink); text-decoration: line-through; text-decoration-thickness: 1px; }
.v-new tr.del, .v-old tr.ins { display: none; }
.v-new tr.ins td, .v-new tr.ins th, .v-old tr.del td, .v-old tr.del th { background: none; color: inherit; text-decoration: none; }
.blk figure { margin: 0; } .blk img { max-width: 100%; height: auto; border-radius: 6px; display: block; }
.blk figcaption, .blk.cap { font-family: var(--font-ui); font-size: 13.5px; font-style: italic; color: var(--muted); line-height: 1.45; }
.figph { font-family: var(--font-ui); font-size: 14px; color: var(--muted); border: 1.5px dashed var(--line); border-radius: 8px; padding: 18px 14px; text-align: center; }
.was { font-family: var(--font-ui); font-size: 13px; color: var(--muted); }
/* Read: the current revision at reading width, cards hidden, change numbers kept to jump between. */
body.read .grid { display: block; }
body.read .cards, body.read .summary, body.read .legend, body.read .og, body.read .stats { display: none; }
body.read .pane { position: static; max-height: none; overflow: visible; border: 0; background: transparent; max-width: 780px; margin: 0 auto; padding: 8px 16px 8px 56px; }
body.read .v-new .hk { display: inline-block; }
body.read .v-new ins { text-decoration: underline 2px var(--theirs); text-underline-offset: 4px; }
body.read .blk.new ins { text-decoration: none; }  /* a wholly new block: a bar beside it, not every line underlined */
body.read .blk.new { box-shadow: -10px 0 0 -7px var(--theirs); }
body.read .blk.new .tagline .tl { display: none; }  /* keep its number, so Prev/Next reaches it */
body.read .blk.on { background: transparent; box-shadow: none; }
#nav { position: fixed; right: 16px; bottom: 16px; display: none; align-items: center; gap: 4px; background: var(--surface); border: 1px solid var(--line);
  border-radius: 10px; padding: 4px; box-shadow: 0 2px 10px rgb(0 0 0 / .12); font-size: 13.5px; font-variant-numeric: tabular-nums; }
#nav button { border: 0; background: var(--bg); color: var(--ink); border-radius: 7px; padding: 6px 10px; }
#nav span { padding: 0 6px; color: var(--muted); }
body.read #nav.on { display: flex; }
.hk.pulse { box-shadow: 0 0 0 4px var(--accent-soft); }
.legend { display: flex; gap: 6px 14px; flex-wrap: wrap; font-size: 12px; color: var(--muted); margin-top: 16px; }
.legend i { display: inline-block; width: 10px; height: 10px; border-radius: 2px; margin-right: 5px; vertical-align: -1px; }

.cards { display: flex; flex-direction: column; gap: 12px; min-width: 0; }
.card { background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 13px 15px; min-width: 0; scroll-margin-top: 16px; transition: box-shadow .2s; }
.card.change { border-left: 4px solid var(--accent); }
.card.change.st-new { border-left-color: var(--theirs); } .card.change.st-removed { border-left-color: var(--ask); }
.card.record { margin-left: 18px; }
.card.on { box-shadow: 0 0 0 2px var(--accent-soft), 0 1px 6px rgb(0 0 0 / .06); }
.card.pulse { box-shadow: 0 0 0 4px var(--accent); }
.card-head { display: flex; gap: 6px; align-items: center; flex-wrap: wrap; margin-bottom: 4px; }
.chip { font-size: 11.5px; font-weight: 600; letter-spacing: .03em; padding: 2px 8px; border-radius: 20px; background: var(--bg); color: var(--muted); }
.chip.origin-author, .chip.origin-source { background: var(--theirs-soft); color: var(--theirs); }
.chip.origin-drafter { background: var(--drafter-soft); color: var(--drafter); }
.chip.origin-mixed { background: var(--mixed-soft); color: var(--mixed); }
.chip.ask { background: var(--ask-soft); color: var(--ask); }
.chip.ok { background: var(--theirs-soft); color: var(--theirs); }
.chip.ins { background: var(--ins); color: var(--ins-ink); } .chip.del { background: var(--del); color: var(--del-ink); }
.chip.chg, .chip.mov { background: var(--accent-soft); color: var(--accent); }
.chip.rev { font-family: var(--font-mono); font-weight: 500; }
.card h3 { font-size: 15.5px; font-weight: 600; margin: 2px 0 4px; }
.card .q { font-family: var(--font-read); font-size: 15.5px; color: var(--ink); }
.card p { margin: 4px 0; color: var(--muted); font-size: 14px; max-width: 70ch; overflow-wrap: anywhere; }
.card p strong { color: var(--ink); }
.card .old { font-family: var(--font-read); font-size: 15px; color: var(--del-ink); text-decoration: line-through; text-decoration-thickness: 1px; }
.card textarea { width: 100%; min-height: 42px; margin-top: 8px; font: inherit; font-size: 13.5px; color: var(--ink); background: var(--bg); border: 1px solid var(--line); border-radius: 6px; padding: 6px 9px; resize: vertical; }
.summary { margin-top: 24px; display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }
#md { position: absolute; left: -9999px; white-space: pre; }
@media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
</style>
</head>
<body>
<div class="wrap">
  <header class="top">
    <div><h1 id="title"></h1><p class="sub" id="sub"></p></div>
    <div class="status"><div id="views"></div><div class="seg" role="group" aria-label="Mode" id="modes"><button type="button" data-mode="review" aria-pressed="true">Review</button><button type="button" data-mode="read" aria-pressed="false">Read</button></div></div>
  </header>
  <div class="stats" id="stats"></div>
  <div id="warn"></div>
  <div class="grid">
    <article class="pane" id="pane" aria-label="The draft">
      <div class="pane-head"><span class="label" id="panelabel"></span></div>
      <div id="text"></div>
      <div class="legend" id="legend"></div>
    </article>
    <section class="cards" id="cards" aria-label="Changes and provenance"></section>
  </div>
  <div class="summary"><button class="btn" id="copy" type="button">Copy notes as Markdown</button><span class="sub" id="copyhint"></span></div>
  <pre id="md" aria-hidden="true"></pre>
</div>
<nav id="nav" aria-label="Changes"><button type="button" data-step="-1" aria-label="Previous change">‹ Prev</button><span id="navpos"></span><button type="button" data-step="1" aria-label="Next change">Next ›</button></nav>
<script>
const D = __DATA__;
const KEY = "voice-revision-notes:" + D.slug;
const wide = matchMedia("(min-width: 901px)");
const calm = matchMedia("(prefers-reduced-motion: reduce)");
const $ = (id) => document.getElementById(id);
const esc = (s) => String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
const byId = Object.fromEntries(D.cards.map((c) => [c.id, c]));
const ORIGIN_INITIAL = { author: "A", source: "S", drafter: "D", mixed: "M", unknown: "?" };
let notes = {};
try { notes = JSON.parse(localStorage.getItem(KEY) || "{}") || {}; } catch (e) {}
let view = "changes", pinned = null, hover = null, hoverTimer = null;

function piecesHTML(p, num) {
  return p.pieces.map((x, k) => {
    let h = esc(x.t);
    for (const st of x.st) h = st === "code" ? `<code>${h}</code>` : `<${st}>${h}</${st}>`;
    if (x.k === "ins") h = `<ins>${h}</ins>`;
    if (x.k === "del") h = `<del>${h}</del>`;
    if (x.a.length) h = `<span class="an" data-cards="${x.a.join(" ")}">${h}</span>`;
    const next = p.pieces[k + 1];
    if (num && x.h && (!next || next.h !== x.h)) h += num(x.h);  // the change's number after its last word
    return h;
  }).join("");
}

// Tables, images, diagram placeholders and captions, drawn as they read; prose as pieces.
function bodyHTML(p, num) {
  if (p.kind === "table") {
    const whole = p.status === "new" ? "ins" : p.status === "removed" ? "del" : "eq";
    const rows = p.rowdiff || (p.rows || []).map((cells) => ({ k: whole, cells }));
    const tr = rows.map((r, k) => {
      const tag = k === 0 ? "th" : "td";
      const last = num && r.h && (!rows[k + 1] || rows[k + 1].h !== r.h) ? num(r.h) : "";
      return `<tr class="${r.k}">${r.cells.map((c, ci) => `<${tag}>${esc(c)}${ci === r.cells.length - 1 ? last : ""}</${tag}>`).join("")}</tr>`;
    }).join("");
    return `<div class="tw"><table>${tr}</table></div>`;
  }
  if (p.kind === "img") {
    const was = p.was ? `<p class="was">Was: <del>${esc(p.was.alt || p.was.src || "")}</del>${num ? num(p.hunks[0]) : ""}</p>` : "";
    const img = p.missing ? `<div class="figph">Image not found beside the draft: ${esc(p.src)}</div>` : `<img src="${esc(p.data || p.src)}" alt="${esc(p.alt)}">`;
    return `<figure>${img}${p.alt ? `<figcaption>${esc(p.alt)}</figcaption>` : ""}${was}</figure>`;
  }
  if (p.kind === "hr") return "<hr>";
  if (p.kind === "fig") {
    const was = p.was ? ` <span class="was">(was: <del>${esc(p.was.text)}</del>)</span>${num ? num(p.hunks[0]) : ""}` : "";
    return `<div class="figph">Diagram: ${esc(p.alt)}${was}</div>`;
  }
  return piecesHTML(p, num);
}

function renderText() {
  $("text").innerHTML = D.paras.map((p) => {
    const origin = D.compare ? "" : p.origin || (p.kind === "p" || p.kind === "list" ? "none" : "");
    const bar = origin ? `<button type="button" class="og o-${origin}" aria-label="Origin: ${origin === "none" ? "no record" : origin}"${p.cards.length ? ` data-cards="${p.cards.join(" ")}"` : ""}><span>${ORIGIN_INITIAL[origin] || "–"}</span></button>` : "";
    const card = p.cards.find((id) => byId[id] && byId[id].kind === "change") || "";
    const num = (n) => `<button type="button" class="hk" data-cards="${card}" aria-label="Change ${n}">${n}</button>`;
    const whole = p.status === "moved" || p.status === "removed" || p.status === "new";
    const tag = p.status === "moved" ? `<span class="tagline">${num(p.hunks[0])} moved from ${esc(p.from)}</span>`
      : p.status === "removed" ? `<span class="tagline">${num(p.hunks[0])} removed</span>`
      : p.status === "new" ? `<span class="tagline">${num(p.hunks[0])} <span class="tl">new</span></span>` : "";
    const cls = `blk ${p.kind} ${p.status}`;
    return `<div class="${cls}" data-cards="${p.cards.join(" ")}"><span class="pn">${esc(p.label)}</span>${bar}${tag}${bodyHTML(p, whole ? null : num)}</div>`;
  }).join("");
  $("text").className = "v-" + view;
}

function cardHTML(c) {
  const chips = c.chips.map(([k, t]) => `<span class="chip ${k}">${esc(t)}</span>`).join("");
  let body = "";
  if (c.kind === "change") {
    const [ow, nw] = c.words || [0, 0];
    const delta = nw - ow;
    body += `<p>${c.from && c.status !== "new" ? `From ${esc(c.from)}. ` : ""}${ow} → ${nw} words${delta ? ` (${delta > 0 ? "+" : ""}${delta})` : ""}.</p>`;
    if (c.old) body += `<p class="old">${esc(c.old)}</p>`;
    if (c.edits && c.edits.length) body += `<ol class="edits">${c.edits.map((e) => `<li value="${e.n}">${e.del.trim() ? `<del>${esc(e.del.trim())}</del>` : ""}${e.del.trim() && e.ins.trim() ? " → " : ""}${e.ins.trim() ? `<ins>${esc(e.ins.trim())}</ins>` : ""}</li>`).join("")}</ol>`;
    if (c.why && c.why.length) body += `<p><strong>Record:</strong> ${c.why.map((id) => esc(byId[id].body || byId[id].title)).join(" · ")}</p>`;
    else if (c.record && c.record.length) body += `<p><strong>Record:</strong> ${c.record.map(esc).join(" · ")}</p>`;
  } else if (c.kind === "question") {
    body += `<p class="q">${esc(c.body)}</p>`;
  } else {
    body += `<p class="q">“${esc(c.title)}”</p>`;
    if (c.body) body += `<p>${esc(c.body)}</p>`;
    if (c.approval) body += `<p><strong>Approval:</strong> ${esc(c.approval)}</p>`;
    if (c.question) body += `<p><strong>Asked:</strong> ${esc(c.question)}</p>`;
  }
  const head = c.kind === "change" ? `<h3>${esc(c.title)}</h3>` : c.kind === "question" ? `<h3>${esc(c.title)}</h3>` : "";
  return `<article class="card ${c.kind}${c.status ? " st-" + c.status : ""}" id="card-${c.id}" data-card="${c.id}" tabindex="-1">
    <div class="card-head">${chips}</div>${head}${body}
    <textarea data-note="${c.id}" aria-label="Note" placeholder="A note for the next revision, if you want one.">${esc(notes[c.id] || "")}</textarea>
  </article>`;
}

function renderCards() {
  $("cards").innerHTML = D.cards.length ? D.cards.map(cardHTML).join("") : `<p class="sub">No changes, and no record lines to show.</p>`;
}

function renderHead() {
  $("title").textContent = D.title;
  document.title = D.title;
  const s = D.stats;
  if (D.compare) {
    $("sub").textContent = `What changed from ${D.compare} to ${D.draft}, numbered. To change something, say or type it to the assistant and name the change ("on change 3…"); jot notes on the cards as you go.`;
    const k = {};
    for (const c of D.cards) if (c.kind === "change") k[c.status] = (k[c.status] || 0) + 1;
    const delta = s.words - s.words_old;
    $("stats").innerHTML = `<span><b>${s.words_old.toLocaleString("en-GB")} → ${s.words.toLocaleString("en-GB")}</b> words (${delta >= 0 ? "+" : ""}${delta})</span>`
      + ["changed", "new", "moved", "removed"].filter((x) => k[x]).map((x) => `<span><b>${k[x]}</b> ${x}</span>`).join("");
    $("views").innerHTML = `<div class="seg" role="group" aria-label="View">${[["changes", "Changes"], ["new", "r" + D.rev + " only"], ["old", "r" + D.rev_old + " only"]]
      .map(([v, t]) => `<button type="button" data-view="${v}" aria-pressed="${view === v}">${esc(t)}</button>`).join("")}</div>`;
    $("panelabel").textContent = view === "old" ? `r${D.rev_old}` : view === "new" ? `r${D.rev}` : `r${D.rev_old} → r${D.rev}`;
  } else {
    $("sub").textContent = `${D.draft}, with whose argument each part carries, from ${D.records.length ? D.records.join(", ") : "no provenance record"}. Click the text or a card to link the two.`;
    $("stats").innerHTML = `<span><b>${s.words.toLocaleString("en-GB")}</b> words</span><span><b>${s.paragraphs}</b> paragraphs</span>`
      + Object.entries(s.origins).map(([o, n]) => `<span><b>${n}</b> ${esc(o)}</span>`).join("");
    $("panelabel").textContent = D.rev ? `Draft r${D.rev}` : "Draft";
  }
  $("legend").innerHTML = (D.compare
    ? `<span><i style="background:var(--ins)"></i>added</span><span><i style="background:var(--del)"></i>removed</span><span><i style="background:var(--accent);border-radius:8px"></i>change number</span>`
    : `<span><i style="background:var(--theirs)"></i>A author · S source</span><span><i style="background:var(--drafter)"></i>D drafter</span><span><i style="background:repeating-linear-gradient(180deg,var(--theirs) 0 4px,var(--drafter) 4px 8px)"></i>M mixed</span><span><i style="background:var(--none)"></i>– no record</span>`)
    + `<span><i style="border-bottom:2px dotted var(--muted);border-radius:0"></i>a sentence with its own record line</span>`;
  if (D.warnings.length) $("warn").innerHTML = `<details class="warn"><summary>${D.warnings.length} record line${D.warnings.length > 1 ? "s" : ""} not placed in the text</summary><ul>${D.warnings.map((w) => `<li>${esc(w)}</li>`).join("")}</ul></details>`;
}

// Two-way linking, as on the deslop decision page.
function paint() {
  const id = hover || pinned;
  document.querySelectorAll(".on").forEach((e) => e.classList.remove("on"));
  if (!id) return;
  document.querySelectorAll(`#text [data-cards~="${id}"], #card-${id}`).forEach((e) => e.classList.add("on"));
}
function reveal(id, always) {
  // Aim at the edit itself, not the top of a long paragraph.
  const blk = pane.querySelector(`.an[data-cards~="${id}"], .blk[data-cards~="${id}"]`);
  if (!blk) return;
  const t = (blk.classList.contains("changed") && blk.querySelector("ins, del")) || blk;
  if (!wide.matches) { if (always) t.scrollIntoView({ behavior: calm.matches ? "auto" : "smooth", block: "center" }); return; }
  const pr = pane.getBoundingClientRect(), tr = t.getBoundingClientRect();
  const top = Math.max(pr.top, 0), bottom = Math.min(pr.bottom, innerHeight);
  if (bottom - top < 120) return;
  const dy = tr.top - top - (bottom - top) / 3;
  if (tr.top < top + 48 || tr.bottom > bottom - 48) pane.scrollBy({ top: dy, behavior: calm.matches || Math.abs(dy) > 1200 ? "auto" : "smooth" });
}
function pin(id, fromText) {
  pinned = id; hover = null; paint();
  if (fromText) {
    const card = $("card-" + id);
    if (!card) return;
    card.scrollIntoView({ behavior: calm.matches ? "auto" : "smooth", block: "start" });
    card.classList.add("pulse"); setTimeout(() => card.classList.remove("pulse"), 1100);
  } else reveal(id);
}
$("cards").addEventListener("mouseover", (e) => {
  const c = e.target.closest(".card"), id = c ? c.dataset.card : null;
  if (id === hover) return;
  clearTimeout(hoverTimer); hover = id; paint();
  if (id) hoverTimer = setTimeout(() => reveal(id), 160);
});
$("cards").addEventListener("mouseleave", () => { clearTimeout(hoverTimer); hover = null; paint(); });
$("cards").addEventListener("focusin", (e) => { const c = e.target.closest(".card"); if (c && c.dataset.card !== pinned) pin(c.dataset.card, false); });
document.addEventListener("click", (e) => {
  const v = e.target.closest("[data-view]");
  if (v) { view = v.dataset.view; renderHead(); renderText(); paint(); return; }
  const m = e.target.closest("[data-mode]");
  if (m) { setMode(m.dataset.mode); return; }
  const st = e.target.closest("#nav [data-step]");
  if (st) { stepChange(+st.dataset.step); return; }
  const t = e.target.closest("#text [data-cards]");
  if (t && t.dataset.cards) {
    // The innermost link wins: a sentence's own record before its paragraph's.
    const ids = t.dataset.cards.split(" ").filter(Boolean);
    const cur = ids.indexOf(pinned);
    pin(ids[(cur + 1) % ids.length], true);  // a second click steps to the next card on the same text
    return;
  }
  const c = e.target.closest(".card");
  if (c && c.dataset.card !== pinned) pin(c.dataset.card, false);
});
document.addEventListener("input", (e) => {
  if (e.target.matches("[data-note]")) {
    notes[e.target.dataset.note] = e.target.value;
    try { localStorage.setItem(KEY, JSON.stringify(notes)); } catch (err) {}
  }
});
$("copy").addEventListener("click", async () => {
  const lines = [`## Notes on ${D.draft}${D.compare ? ` (compared with ${D.compare})` : ""}`, ""];
  for (const c of D.cards) {
    const n = (notes[c.id] || "").trim();
    if (!n) continue;
    const what = c.kind === "change" ? c.title : c.kind === "question" ? c.title : `“${c.title.slice(0, 60)}${c.title.length > 60 ? "…" : ""}”`;
    lines.push(`- **${what}:** ${n.replace(/\n+/g, " ")}`);
  }
  if (lines.length === 2) lines.push("(No notes.)");
  const md = lines.join("\n"), btn = $("copy");
  try { await navigator.clipboard.writeText(md); btn.textContent = "Copied"; }
  catch (err) {
    const pre = $("md"); pre.textContent = md;
    const r = document.createRange(); r.selectNodeContents(pre);
    const sel = getSelection(); sel.removeAllRanges(); sel.addRange(r);
    btn.textContent = "Selected: press Copy";
  }
  setTimeout(() => { btn.textContent = "Copy notes as Markdown"; }, 2200);
});
$("copyhint").textContent = "Notes stay in this browser; copy them and paste them back for the next revision.";
// Review is the split view; Read shows the current revision on its own, with the change numbers.
let mode = "review", reviewView = view, navAt = -1;
function setMode(next) {
  if (next === mode) return;
  if (next === "read") { reviewView = view; view = D.compare ? "new" : "changes"; } else { view = reviewView; }
  mode = next;
  document.body.classList.toggle("read", mode === "read");
  document.querySelectorAll("[data-mode]").forEach((b) => b.setAttribute("aria-pressed", b.dataset.mode === mode));
  $("views").style.display = mode === "read" ? "none" : "";
  renderHead(); renderText(); paint();
  $("nav").classList.toggle("on", !!D.compare && mode === "read");
  navAt = -1; updateNav();
}
function visibleChanges() { return [...document.querySelectorAll("#text .hk")].filter((b) => b.offsetParent); }
function updateNav() {
  const all = visibleChanges();
  $("navpos").textContent = all.length ? (navAt < 0 ? `${all.length} changes` : `Change ${all[navAt].textContent} · ${navAt + 1} of ${all.length}`) : "No changes";
}
function stepChange(d) {
  const all = visibleChanges();
  if (!all.length) return;
  navAt = navAt < 0 ? (d > 0 ? 0 : all.length - 1) : (navAt + d + all.length) % all.length;
  const b = all[navAt];
  b.scrollIntoView({ behavior: calm.matches ? "auto" : "smooth", block: "center" });
  b.classList.add("pulse"); setTimeout(() => b.classList.remove("pulse"), 1100);
  updateNav();
}
document.addEventListener("keydown", (e) => {
  if (mode !== "read" || e.target.closest("textarea, input")) return;
  if (e.key === "j" || e.key === "n") stepChange(1);
  if (e.key === "k" || e.key === "p") stepChange(-1);
});
renderHead(); renderText(); renderCards();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    sys.exit(main())
