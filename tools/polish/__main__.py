"""Re-render every demo page in this repo from its own recorded facts.

    python3 -m tools.polish            # all sites
    python3 -m tools.polish slug ...   # just those

Run from the repo root. Each site's index.html is rewritten in place; photos
are untouched. Safe to run twice.
"""
from __future__ import annotations

import sys
from pathlib import Path

from .extract import extract
from .render import render

ROOT = Path(__file__).resolve().parents[2]


def main(argv: list[str]) -> int:
    if argv:
        dirs = [ROOT / a for a in argv]
    else:
        dirs = sorted(p.parent for p in ROOT.glob("*/index.html") if not p.parent.name.startswith(("tools", ".")))
    n = 0
    for d in dirs:
        if not (d / "index.html").exists():
            print(f"skip {d.name}: no index.html", file=sys.stderr)
            continue
        data = extract(d)
        (d / "index.html").write_text(render(data), encoding="utf-8")
        n += 1
    print(f"rendered {n} site(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
