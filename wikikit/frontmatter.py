"""Minimal frontmatter handling: a flat YAML subset, line based and EOL safe.

Supported values: scalars, inline lists `[a, b]`, and block lists (`- item`). Anything more exotic
is ignored rather than guessed. Editing (`set_key`) works on the list of lines, never with a
multiline regex over the text: in a CRLF file `$` sits between the CR and the LF and splits the pair.
"""
import re

_FM = re.compile(r"^---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|$)", re.S)


def split(text):
    """(frontmatter_text, body). frontmatter_text is '' when the note has none."""
    text = text.lstrip("﻿")
    m = _FM.match(text)
    return (m.group(1), text[m.end():]) if m else ("", text)


def parse(text):
    """(dict, body)."""
    fm_text, body = split(text)
    fm, key = {}, None
    for line in fm_text.splitlines():
        km = re.match(r"^([A-Za-z0-9_][\w-]*):\s*(.*)$", line)
        if km:
            key, val = km.group(1), km.group(2).strip()
            if val.startswith("[") and val.endswith("]"):
                fm[key] = [x.strip().strip('"').strip("'") for x in val[1:-1].split(",") if x.strip()]
            elif val == "":
                fm[key] = []  # may be filled by a following block list
            else:
                fm[key] = val.strip('"').strip("'")
            continue
        bm = re.match(r"^\s+-\s+(.*)$", line)
        if bm and key is not None and isinstance(fm.get(key), list):
            fm[key].append(bm.group(1).strip().strip('"').strip("'"))
    return fm, body


def as_list(value):
    if isinstance(value, list):
        return [v for v in value if v]
    return [value] if value else []


def get_raw(text, key):
    """Raw (unquoted-stripped) value of `key` as written, or None. Handles CRLF."""
    fm_text, _ = split(text)
    m = re.search(r"^[ \t]*%s[ \t]*:[ \t]*(.*?)[ \t]*$" % re.escape(key), fm_text, re.M)
    return m.group(1).rstrip("\r") if m else None


def set_key(text, key, value):
    """Set `key: value` in the frontmatter (replace the first match, or add before the closing ---).

    `text` keeps its EOL. Raises ValueError if the note has no closed frontmatter.
    """
    eol = "\r\n" if "\r\n" in text else "\n"
    lines = text.split(eol)
    if not lines or lines[0].strip() != "---":
        raise ValueError("no frontmatter")
    close = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if close is None:
        raise ValueError("frontmatter is not closed")
    new = "%s: %s" % (key, value)
    for i in range(1, close):
        if re.match(r"^%s[ \t]*:" % re.escape(key), lines[i]):
            lines[i] = new
            break
    else:
        lines.insert(close, new)
    return eol.join(lines)
