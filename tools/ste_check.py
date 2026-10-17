#!/usr/bin/env python3
"""Check the prose of the book pages against STYLE.md.

Usage:
    uv run python tools/ste_check.py                 # check the default paths
    uv run python tools/ste_check.py docs/topics/ch03-pressure-hydrostatic.md

The checker reads MyST Markdown. It skips the frontmatter, code cells, code blocks,
math, inline code, roles, URLs, comments and directive options. It checks the rest.

Each violation prints as `file:line: rule: text`. The exit code is 1 if there is a violation.

Rules:
    zh-sentence-length  A Chinese sentence has more than 40 counted characters.
    en-sentence-length  An English sentence has more than 25 words.
    paragraph-length    A paragraph has more than 6 sentences.
    passive-voice       Chinese 被 / 给出了 / 得到了, or English "be + past participle".
    parentheses         Parentheses in prose.
    interval-format     An interval that is not written as ［下限, 上限］.
    unit-space          A number without a space before its unit, or the symbol ℃.
    unit-symbol         The word 节 as the unit knot, for example "51 节". Write kt.
    rejected-term       A rejected synonym from glossary.md.

Suppress a check only when the text must show a wrong form, for example in an exercise:
    % ste-ignore                  skips the next paragraph
    % ste-ignore-start ... % ste-ignore-end
In files that GitHub renders (README.md), use <!-- ste-ignore --> and the same -start/-end forms.

Settings are in pyproject.toml under [tool.ste_check].
"""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DEFAULTS = {
    "paths": ["intro.md", "README.md", "docs"],
    "exclude": [],
    "glossary": "glossary.md",
    "zh_max_chars": 40,
    "en_max_words": 25,
    "max_sentences": 6,
    "number_list_min": 3,
    "allow": [],
}

# A placeholder for inline code, math, roles and URLs. It counts as nothing.
PH = ""

HAN = r"㐀-䶿一-鿿豈-﫿"
HAN_RE = re.compile(f"[{HAN}]")
LATIN_WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9_'’\-]*")
NUMBER_RE = re.compile(r"(?<![A-Za-z_])[-−+]?\d+(?:[.,]\d+)*")

# Directives whose body is not prose.
SKIP_DIRECTIVES = {
    "code-cell",
    "code",
    "code-block",
    "sourcecode",
    "literalinclude",
    "math",
    "mermaid",
    "raw",
    "include",
    "embed",
    "csv-table",
    "iframe",
    "image",
    "bibliography",
    "toc",
    "tableofcontents",
    "glue",
    "glue:figure",
    "glue:any",
    "eval",
    "any:bundle",
}

FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,}|:{3,})\s*(?:\{([^}]+)\})?(.*)$")
OPTION_RE = re.compile(r"^\s*:[A-Za-z][\w-]*:")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+")
LIST_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$")
TARGET_RE = re.compile(r"^\s*\([\w:.-]+\)=\s*$")

# Inline cleaning, applied in this order.
INLINE_SUBS = [
    (re.compile(r"<!--.*?-->"), ""),  # inline HTML comments
    (re.compile(r"(`+)(.+?)\1"), PH),  # inline code
    (re.compile(r"\{[\w:.-]+\}" + PH), PH),  # roles: {math}`x`
    (re.compile(r"\$\$.+?\$\$"), PH),  # one-line display math
    (re.compile(r"(?<![\\$])\$(?!\s)[^$\n]+?(?<![\s\\])\$(?!\d)"), PH),  # inline math
    (re.compile(r"!\[[^\]]*\]\([^)]*\)"), ""),  # images
    (re.compile(r"\[\]\([^)]*\)"), PH),  # empty-text cross references
    (re.compile(r"\[([^\]]+)\]\([^)]*\)"), r"\1"),  # links: keep the text
    (re.compile(r"\[\^[^\]]+\]"), ""),  # footnote references
    (re.compile(r"<https?://[^>]+>"), PH),  # autolinks
    (re.compile(r"https?://\S+"), PH),  # bare URLs
    (re.compile(r"</?[A-Za-z][^>]*>"), ""),  # HTML tags
    (re.compile(r"\{\{[^}]*\}\}"), PH),  # substitutions
]

ZH_END = "。！？"
EN_ABBREV = ("e.g.", "i.e.", "et al.", "etc.", "Fig.", "Eq.", "vs.", "cf.", "No.", "approx.")

ZH_PASSIVE_RE = re.compile(r"被(?!动)|给出了|得到了")
EN_PASSIVE_RE = re.compile(
    r"\b(?:is|are|was|were|be|been|being)\s+(?:\w+ly\s+)?"
    r"(\w+ed|known|given|shown|done|made|taken|seen|written|built|found|held|kept|meant|"
    r"put|read|run|sent|set|told|chosen|drawn|driven|grown|hidden|thrown|broken)\b",
    re.IGNORECASE,
)
EN_NOT_PASSIVE = {"saturated", "unsaturated", "mixed", "stratified", "interested", "need"}

NUM = r"[-−]?\d+(?:\.\d+)?"
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}(?:[T ]\d{2}(?::\d{2}){0,2})?|\d{1,2}:\d{2}")
RANGE_RE = re.compile(rf"(?<![\w.])({NUM})\s*(?:-|–|—|~|～|〜|至|到)\s*({NUM})(?![\w.])")
BAD_BRACKET_RE = re.compile(rf"[\[(（【]\s*{NUM}\s*[,，、]\s*{NUM}\s*[\])）】]")
FW_INTERVAL_RE = re.compile(r"［[^］]*］")
BOUND = rf"(?:{NUM}|{PH}|[-−]?∞)"
GOOD_INTERVAL_RE = re.compile(rf"^［({BOUND}), ({BOUND})］$")
UNITS = r"hPa|kPa|Pa|mb|dam|km|cm|mm|μm|nm|m|kg|g|K|°C|J|W|PVU|ppm|ppb|UTC|s|h|d"
UNIT_GLUE_RE = re.compile(rf"(?<![\w.^]){NUM}({UNITS})(?![A-Za-z0-9_])")
# 节 is a section of a document, for example "2.2 节" or "第 3 节". After an integer, or in
# "单位是节" and "以节为单位", it is the unit knot. The book writes that unit as kt.
KNOT_RE = re.compile(r"(?<![\d.])(?<!第)(?<!第 )\d+\s*节|单位是节|以节为单位")
PAREN_PAIR_RE = re.compile(r"[(（][^()（）]*[)）]")
PAREN_RE = re.compile(r"[()（）]")


@dataclass
class Violation:
    path: str
    line: int
    rule: str
    text: str

    def __str__(self) -> str:
        return f"{self.path}:{self.line}: {self.rule}: {self.text}"


@dataclass
class Unit:
    """A paragraph, a heading, a list item or a table cell, with its source lines."""

    pieces: list[tuple[int, str]] = field(default_factory=list)
    kind: str = "paragraph"


# --------------------------------------------------------------------------- glossary


@dataclass
class Glossary:
    pattern: re.Pattern | None
    approved: set[str]
    rejected: dict[str, list[str]]


def _norm(term: str) -> str:
    return re.sub(r"\s+", "", term)


def _term_regex(term: str) -> str:
    """Build a regex for a term. Spaces are optional between characters of the term."""
    chars = [c for c in term if not c.isspace()]
    body = r"\s*".join(re.escape(c) for c in chars)
    if chars and chars[0].isascii() and chars[0].isalnum():
        body = r"(?<![A-Za-z0-9_])" + body
    if chars and chars[-1].isascii() and chars[-1].isalnum():
        body = body + r"(?![A-Za-z0-9_])"
    return body


def load_glossary(path: Path, allow: list[str]) -> Glossary:
    approved: set[str] = set(allow)
    rejected: dict[str, list[str]] = {}
    if not path.exists():
        return Glossary(None, approved, rejected)
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or TABLE_SEP_RE.match(line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 6 or cells[0] in ("中文术语", ""):
            continue
        term = cells[0]
        approved.add(term)
        for word in re.split(r"[、，,]", cells[5]):
            word = word.strip()
            if word and word not in ("—", "-"):
                rejected.setdefault(word, []).append(term)
    terms = sorted(approved | set(rejected), key=lambda t: len(_norm(t)), reverse=True)
    pattern = re.compile("|".join(_term_regex(t) for t in terms)) if terms else None
    return Glossary(
        pattern, {_norm(t) for t in approved}, {_norm(k): v for k, v in rejected.items()}
    )


# --------------------------------------------------------------------------- parsing


def clean_inline(text: str) -> str:
    for regex, repl in INLINE_SUBS:
        text = regex.sub(repl, text)
    return text


def split_units(lines: list[str]) -> list[Unit]:
    """Split a MyST Markdown file into prose units. Skip everything that is not prose."""
    units: list[Unit] = []
    current: Unit | None = None
    fences: list[tuple[str, int, bool]] = []  # (char, length, is_prose)
    in_math = False
    in_comment = False
    ignore_next = 0  # 0: off, 1: waiting for the block, 2: inside the block
    ignoring_block = False
    directive_options = False

    def close() -> None:
        nonlocal current
        if current is not None and current.pieces:
            units.append(current)
        current = None

    i = 0
    if lines and lines[0].strip() == "---":
        for j in range(1, len(lines)):
            if lines[j].strip() in ("---", "..."):
                i = j + 1
                break

    while i < len(lines):
        raw = lines[i]
        lineno = i + 1
        i += 1
        stripped = raw.strip()

        # Ignore markers.
        marker = re.match(r"^(?:%|<!--)\s*ste-ignore(-start|-end)?\s*(?:-->)?\s*$", stripped)
        if marker:
            close()
            kind = marker.group(1)
            if kind == "-start":
                ignoring_block = True
            elif kind == "-end":
                ignoring_block = False
            else:
                ignore_next = 1
            continue
        if ignoring_block:
            continue
        if ignore_next:
            if stripped:
                ignore_next = 2
            elif ignore_next == 2:
                ignore_next = 0
            continue

        # HTML comments.
        if in_comment:
            if "-->" in raw:
                in_comment = False
            continue
        if stripped.startswith("<!--"):
            close()
            if "-->" not in stripped:
                in_comment = True
            continue

        # Fences.
        inside_code = bool(fences) and not fences[-1][2]
        m = FENCE_RE.match(raw)
        if m:
            char, length = m.group(2)[0], len(m.group(2))
            if (
                fences
                and fences[-1][0] == char
                and length >= fences[-1][1]
                and not m.group(3)
                and not m.group(4).strip()
            ):
                close()
                fences.pop()
                directive_options = False
                continue
            if not inside_code:
                close()
                name = (m.group(3) or "").strip()
                is_prose = bool(name) and name not in SKIP_DIRECTIVES
                fences.append((char, length, is_prose))
                directive_options = is_prose
                continue
        if bool(fences) and not fences[-1][2]:
            continue

        # Directive options directly after the opening line.
        if directive_options:
            if OPTION_RE.match(raw):
                continue
            directive_options = False

        # Display math.
        if in_math:
            if stripped.endswith("$$"):
                in_math = False
            continue
        if stripped.startswith("$$"):
            close()
            if not (len(stripped) > 2 and stripped.endswith("$$")):
                in_math = True
            continue

        if not stripped:
            close()
            continue
        if stripped.startswith("%") or stripped.startswith("+++") or TARGET_RE.match(raw):
            close()
            continue

        text = re.sub(r"^\s*(?:>\s?)+", "", raw)
        if TABLE_SEP_RE.match(text):
            continue
        if text.lstrip().startswith("|"):
            close()
            cleaned = clean_inline(text)
            for cell in cleaned.strip().strip("|").split("|"):
                if cell.strip():
                    units.append(Unit([(lineno, cell.strip())], kind="cell"))
            continue
        if HEADING_RE.match(text):
            close()
            units.append(Unit([(lineno, clean_inline(HEADING_RE.sub("", text)))], kind="heading"))
            continue
        if LIST_RE.match(text):
            close()
            current = Unit([(lineno, clean_inline(LIST_RE.sub("", text)))], kind="item")
            continue
        if current is None:
            current = Unit()
        current.pieces.append((lineno, clean_inline(text.strip())))
    close()
    return units


def join_unit(unit: Unit) -> tuple[str, list[int]]:
    """Join the lines of a unit. Return the text and the source line of each character."""
    text = ""
    where: list[int] = []
    for lineno, piece in unit.pieces:
        piece = piece.strip()
        if text and piece:
            ascii_join = text[-1].isascii() and piece[0].isascii()
            if ascii_join:
                text += " "
                where.append(lineno)
        text += piece
        where.extend([lineno] * len(piece))
    return text, where


def split_sentences(text: str) -> list[tuple[int, str]]:
    """Split text into sentences. Return (start offset, sentence)."""
    out: list[tuple[int, str]] = []
    start = 0
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        end = False
        if c in ZH_END or c in "!?":
            end = True
        elif c == ".":
            nxt = text[i + 1] if i + 1 < n else ""
            prev = text[i - 1] if i else ""
            word = text[max(0, text.rfind(" ", 0, i) + 1) : i + 1]
            if (nxt == "" or nxt.isspace()) and not prev.isdigit() and word not in EN_ABBREV:
                end = True
        if end:
            while i + 1 < n and text[i + 1] in "”’\"'）)":
                i += 1
            sentence = text[start : i + 1].strip()
            if sentence:
                out.append((start, sentence))
            start = i + 1
        i += 1
    tail = text[start:].strip()
    if tail:
        out.append((start, tail))
    return out


def zh_length(sentence: str, number_list_min: int) -> int:
    numbers = NUMBER_RE.findall(sentence)
    rest = NUMBER_RE.sub(" ", sentence)
    count = len(HAN_RE.findall(rest)) + len(LATIN_WORD_RE.findall(rest))
    if len(numbers) < number_list_min:
        count += len(numbers)
    return count


def _short(text: str, limit: int = 60) -> str:
    text = re.sub(r"\s+", " ", text.replace(PH, "…")).strip()
    return text if len(text) <= limit else text[: limit - 1] + "…"


# --------------------------------------------------------------------------- checks


def check_unit(unit: Unit, path: str, glossary: Glossary, cfg: dict) -> list[Violation]:
    text, where = join_unit(unit)
    if not text.strip():
        return []
    out: list[Violation] = []

    def at(offset: int) -> int:
        return where[min(offset, len(where) - 1)] if where else unit.pieces[0][0]

    # Dates and times are not intervals.
    masked = DATE_RE.sub(lambda m: "D" * len(m.group(0)), text)

    # Interval format.
    taken: list[tuple[int, int]] = []
    for m in RANGE_RE.finditer(masked):
        a, b = m.group(1), m.group(2)
        lo, hi = sorted((a, b), key=lambda x: float(x.replace("−", "-")))
        out.append(
            Violation(path, at(m.start()), "interval-format", f"{m.group(0)} → ［{lo}, {hi}］")
        )
        taken.append(m.span())
    for m in BAD_BRACKET_RE.finditer(masked):
        out.append(
            Violation(path, at(m.start()), "interval-format", f"{m.group(0)} → ［下限, 上限］")
        )
        taken.append(m.span())
    for m in FW_INTERVAL_RE.finditer(masked):
        good = GOOD_INTERVAL_RE.match(m.group(0))
        if not good:
            out.append(
                Violation(
                    path, at(m.start()), "interval-format", f"{_short(m.group(0))} → ［下限, 上限］"
                )
            )
            continue
        lo, hi = (g.replace("−", "-") for g in good.groups())
        try:
            if float(lo) >= float(hi):
                out.append(
                    Violation(
                        path, at(m.start()), "interval-format", f"{m.group(0)}: 下限必须小于上限"
                    )
                )
        except ValueError:
            pass

    # Parentheses outside the interval matches. Report a pair once.
    for m in PAREN_PAIR_RE.finditer(masked):
        if any(a <= m.start() < b for a, b in taken):
            continue
        out.append(Violation(path, at(m.start()), "parentheses", _short(text[m.start() : m.end()])))
        taken.append(m.span())
    for m in PAREN_RE.finditer(masked):
        if any(a <= m.start() < b for a, b in taken):
            continue
        out.append(
            Violation(
                path,
                at(m.start()),
                "parentheses",
                _short(text[max(0, m.start() - 15) : m.start() + 15]),
            )
        )

    # Units.
    for m in UNIT_GLUE_RE.finditer(masked):
        if m.group(1) == "s" and re.fullmatch(r"\d{4}s", m.group(0)):
            continue  # a decade such as 1990s
        out.append(
            Violation(path, at(m.start()), "unit-space", f"{m.group(0)} → 数字和单位之间加空格")
        )
    for m in re.finditer("℃", text):
        out.append(Violation(path, at(m.start()), "unit-space", "℃ → °C"))
    for m in KNOT_RE.finditer(masked):
        out.append(Violation(path, at(m.start()), "unit-symbol", f"{m.group(0)} → kt"))

    # Passive voice, Chinese.
    for m in ZH_PASSIVE_RE.finditer(text):
        out.append(
            Violation(
                path,
                at(m.start()),
                "passive-voice",
                _short(text[max(0, m.start() - 12) : m.start() + 12]),
            )
        )

    # Rejected terms.
    if glossary.pattern is not None:
        for m in glossary.pattern.finditer(text):
            key = _norm(m.group(0))
            if key in glossary.rejected and key not in glossary.approved:
                use = " / ".join(dict.fromkeys(glossary.rejected[key]))
                out.append(Violation(path, at(m.start()), "rejected-term", f"{m.group(0)} → {use}"))

    # Sentences.
    sentences = split_sentences(text)
    for offset, sentence in sentences:
        if HAN_RE.search(sentence):
            n = zh_length(sentence, cfg["number_list_min"])
            if n > cfg["zh_max_chars"]:
                out.append(
                    Violation(
                        path,
                        at(offset),
                        "zh-sentence-length",
                        f"{n} 字 > {cfg['zh_max_chars']}: {_short(sentence)}",
                    )
                )
        else:
            words = LATIN_WORD_RE.findall(sentence)
            if len(words) > cfg["en_max_words"]:
                out.append(
                    Violation(
                        path,
                        at(offset),
                        "en-sentence-length",
                        f"{len(words)} words > {cfg['en_max_words']}: {_short(sentence)}",
                    )
                )
            for m in EN_PASSIVE_RE.finditer(sentence):
                if m.group(1).lower() not in EN_NOT_PASSIVE:
                    out.append(Violation(path, at(offset), "passive-voice", m.group(0)))
    if unit.kind == "paragraph" and len(sentences) > cfg["max_sentences"]:
        out.append(
            Violation(
                path,
                at(0),
                "paragraph-length",
                f"{len(sentences)} 句 > {cfg['max_sentences']}: {_short(text, 30)}",
            )
        )
    return out


def check_text(
    text: str, path: str, glossary: Glossary, cfg: dict | None = None
) -> list[Violation]:
    cfg = {**DEFAULTS, **(cfg or {})}
    out: list[Violation] = []
    for unit in split_units(text.splitlines()):
        out.extend(check_unit(unit, path, glossary, cfg))
    out.sort(key=lambda v: (v.line, v.rule))
    return out


# --------------------------------------------------------------------------- CLI


def load_config(root: Path) -> dict:
    cfg = dict(DEFAULTS)
    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
        cfg.update(data.get("tool", {}).get("ste_check", {}))
    return cfg


def collect(paths: list[str], root: Path, exclude: list[str]) -> list[Path]:
    files: list[Path] = []
    for p in paths:
        path = (root / p) if not Path(p).is_absolute() else Path(p)
        if path.is_dir():
            files.extend(sorted(path.rglob("*.md")))
        elif path.suffix == ".md" and path.exists():
            files.append(path)
    skip = [(root / e).resolve() for e in exclude]
    out = []
    for f in files:
        r = f.resolve()
        if any(r == s or s in r.parents for s in skip):
            continue
        if any(part.startswith(".") or part == "_build" for part in f.parts):
            continue
        out.append(f)
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="*", help="files or directories; default from pyproject")
    args = parser.parse_args(argv)

    cfg = load_config(ROOT)
    glossary = load_glossary(ROOT / cfg["glossary"], list(cfg["allow"]))
    files = collect(args.paths or cfg["paths"], ROOT, cfg["exclude"])
    count = 0
    for f in files:
        try:
            shown = str(f.resolve().relative_to(ROOT))
        except ValueError:
            shown = str(f)
        for v in check_text(f.read_text(encoding="utf-8"), shown, glossary, cfg):
            print(v)
            count += 1
    if count:
        print(f"ste_check: {count} violation(s). See STYLE.md.", file=sys.stderr)
    return 1 if count else 0


if __name__ == "__main__":
    sys.exit(main())
