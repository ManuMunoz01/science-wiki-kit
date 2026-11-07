"""Byte-safe text I/O. Never lets Python translate line endings behind your back."""
import time
from pathlib import Path


def read_text(path):
    """UTF-8 text with the file's own line endings untouched."""
    return Path(path).read_bytes().decode("utf-8")


def detect_eol(text):
    return "\r\n" if "\r\n" in text else "\n"


def to_lf(text):
    return text.replace("\r\n", "\n")


def with_eol(text, eol):
    """`text` may be LF or CRLF; return it with exactly `eol`."""
    lf = to_lf(text)
    return lf.replace("\n", "\r\n") if eol == "\r\n" else lf


def write_text(path, text, retries=8):
    """Write UTF-8 (no BOM), creating parent folders. Retries on transient OSError.

    On Windows a file that an editor (Obsidian) is reading can refuse a write with Errno 22;
    retrying avoids leaving a batch half written.
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    data = text.encode("utf-8")
    for k in range(retries):
        try:
            p.write_bytes(data)
            return
        except OSError:
            if k == retries - 1:
                raise
            time.sleep(0.5 * (k + 1))


def append_log(log_path, header, entry_lines):
    """Append an entry to a log file, creating it with `header` if absent."""
    p = Path(log_path)
    entry = "\n".join(entry_lines) + "\n"
    if p.exists():
        write_text(p, read_text(p).rstrip("\n") + "\n\n" + entry)
    else:
        write_text(p, header + "\n\n" + entry)
