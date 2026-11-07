"""Locate and load wiki.config.json (the single configuration file of the kit)."""
import json
from pathlib import Path

DEFAULTS = {
    # layout. `vault_root` is relative to the folder holding wiki.config.json; `wiki_root` is
    # relative to the vault root. Either may be absolute.
    "vault_root": ".",
    "wiki_root": "wiki",
    "papers_folder": "papers",
    "books_folder": "books",
    "concepts_folder": "concepts",
    "methods_folder": "methods",
    "concept_folders": None,  # derived: [concepts_folder, methods_folder]
    "folders": None,  # derived: every wiki folder the lint scans
    "recursive_folders": ["fields"],
    "vault_ignore_dirs": [".obsidian", ".git", ".trash", "Assets", "templates", "Templates", "_archive", "_temp"],
    # language and policy
    "note_language": "en",
    "min_distinct_sources_for_final": 2,
    "pdf_library_dir": "",
    # vocabulary
    "vocabulary_file": "_VOCABULARY.md",
    "wiki_title": "Science Wiki",
    "field_titlecase_map": {},
    # synthesis layer
    "synthesis": {
        "min_sources": 3,
        "sr_levels": ["SR-MA", "SR"],
        # ISO date. A paper note dated BEFORE it, and not fulltext-sealed, is "pre-fulltext" (null = off).
        "prefulltext_cutoff": None,
        # Fields worked first by the worklist, in order (field slugs). Empty = no priority.
        "priority_fields": [],
    },
    # wiki-lint overrides, merged over wikikit/lint/defaults.json
    "lint": {},
}


def _merge(base, over):
    out = dict(base)
    for k, v in over.items():
        out[k] = _merge(base[k], v) if isinstance(v, dict) and isinstance(base.get(k), dict) else v
    return out


def _derive(cfg, user):
    """Fill the derived keys, honouring what the user wrote explicitly."""
    cf = user.get("concept_folders")
    if cf:  # older style: concept_folders = [concepts, methods]
        if "concepts_folder" not in user:
            cfg["concepts_folder"] = cf[0]
        if "methods_folder" not in user and len(cf) > 1:
            cfg["methods_folder"] = cf[1]
    cfg["concept_folders"] = [cfg["concepts_folder"], cfg["methods_folder"]]
    if not user.get("folders"):
        cfg["folders"] = [cfg["papers_folder"], cfg["concepts_folder"], cfg["methods_folder"],
                          cfg["books_folder"], "fields", "debates"]
    return cfg


def find_config_file(start="."):
    """Walk up from `start` to the first wiki.config.json. Returns a Path or None."""
    p = Path(start).resolve()
    for d in [p] + list(p.parents):
        cfg = d / "wiki.config.json"
        if cfg.is_file():
            return cfg
    return None


def load_config(start="."):
    """Return (config_dir, config). Without a config file: (start, DEFAULTS)."""
    f = find_config_file(start)
    if f is None:
        return Path(start).resolve(), _derive(_merge(DEFAULTS, {}), {})
    user = json.loads(f.read_bytes().decode("utf-8-sig"))
    return f.parent, _derive(_merge(DEFAULTS, user), user)


def vault_path(root, cfg):
    """Absolute path of the vault (every note, inside or outside the wiki, lives under it)."""
    return Path(root) / cfg["vault_root"]


def wiki_path(root, cfg):
    """Absolute path of the wiki folder."""
    return vault_path(root, cfg) / cfg["wiki_root"]
