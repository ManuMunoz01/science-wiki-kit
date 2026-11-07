"""Markdown section helpers (level-2 headings)."""
import re


def section_bounds(lines, name):
    """(start index of the heading, exclusive end index) of `## name` (exact heading), or None."""
    start = None
    for i, line in enumerate(lines):
        if re.match(r"^##\s+" + re.escape(name) + r"\s*$", line.rstrip("\r")):
            start = i
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if re.match(r"^##\s", lines[j].rstrip("\r")):
            end = j
            break
    return start, end


def get_section(text, heading):
    """Body of the first `## heading...` section (prefix match on a word boundary), without the heading."""
    out, inside = [], False
    for line in re.split(r"\r?\n", text):
        if re.match(r"^##\s+" + re.escape(heading) + r"\b", line):
            inside = True
            continue
        if inside and re.match(r"^##\s", line):
            break
        if inside:
            out.append(line)
    return "\n".join(out)


def remove_section(text, heading):
    """`text` without every `## heading...` section. Output is LF-joined."""
    out, inside = [], False
    for line in re.split(r"\r?\n", text):
        if re.match(r"^##\s+" + re.escape(heading) + r"\b", line):
            inside = True
            continue
        if inside and re.match(r"^##\s", line):
            inside = False
            out.append(line)
        elif not inside:
            out.append(line)
    return "\n".join(out)
