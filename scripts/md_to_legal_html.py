#!/usr/bin/env python3
"""Convert Artio legal markdown to HTML for GitHub Pages."""

import re
import sys
from pathlib import Path

LINK_MAP = {
    "artio-privacy-policy.md": "/privacy",
    "artio-terms-of-service.md": "/terms",
}


def english_only(md: str) -> str:
    """Keep content before the Spanish section and drop bilingual boilerplate."""
    parts = re.split(r"^## Español\s*$", md, maxsplit=1, flags=re.MULTILINE)
    text = parts[0].rstrip()
    text = re.sub(
        r"^This document contains the .+ in English and Spanish\.\s*\n",
        "",
        text,
        flags=re.MULTILINE,
    )
    return text


def inline(text: str) -> str:
    text = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda m: f'<a href="{LINK_MAP.get(m.group(2), m.group(2))}">{m.group(1)}</a>',
        text,
    )
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return text


def slug_heading(text: str) -> str:
    s = text.lower().strip()
    s = s.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("ñ", "n")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "section"


def convert(md: str, *, strip_spanish: bool = True) -> str:
    if strip_spanish:
        md = english_only(md)
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    in_ul = False
    lang_prefix = ""
    skip_english_heading = strip_spanish

    def close_ul():
        nonlocal in_ul
        if in_ul:
            out.append("</ul>")
            in_ul = False

    def heading_id(text: str) -> str:
        base = slug_heading(text)
        return f"{lang_prefix}{base}" if lang_prefix else base

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped == "---":
            close_ul()
            out.append("<hr>")
            i += 1
            continue

        if stripped.startswith("#### "):
            close_ul()
            text = stripped[5:]
            out.append(f'<h4 id="{heading_id(text)}">{inline(text)}</h4>')
            i += 1
            continue

        if stripped.startswith("### "):
            close_ul()
            text = stripped[4:]
            out.append(f'<h3 id="{heading_id(text)}">{inline(text)}</h3>')
            i += 1
            continue

        if stripped.startswith("## "):
            close_ul()
            text = stripped[3:]
            if text == "English" and skip_english_heading:
                i += 1
                continue
            if text == "Español":
                break
            sid = slug_heading(text)
            out.append(f'<h2 id="{sid}" class="legal-lang-heading">{inline(text)}</h2>')
            i += 1
            continue

        if stripped.startswith("# "):
            close_ul()
            text = stripped[2:]
            out.append(f"<h1>{inline(text)}</h1>")
            i += 1
            continue

        if stripped.startswith("- "):
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{inline(stripped[2:])}</li>")
            i += 1
            continue

        if stripped == "":
            close_ul()
            i += 1
            continue

        close_ul()
        out.append(f"<p>{inline(stripped)}</p>")
        i += 1

    close_ul()
    return "\n      ".join(out)


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: md_to_legal_html.py input.md output.fragment.html", file=sys.stderr)
        sys.exit(1)

    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    html = convert(src.read_text(encoding="utf-8"))
    dst.write_text(html + "\n", encoding="utf-8")
    print(f"Wrote {dst}")


if __name__ == "__main__":
    main()
