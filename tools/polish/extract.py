"""Pull the real facts out of an existing demo page.

Everything the new page shows has to come from here. Nothing is invented:
name, phone, rating, review count, address, Google place id, photos and the
photo credit line are all already on the published page.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path


def _fix_mojibake(s: str) -> str:
    """Undo UTF-8 text that was decoded as Latin-1 once (Deeâ\x80\x99s -> Dee's)."""
    if "â" in s or "Ã" in s:
        try:
            s = s.encode("latin-1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass
    return s.replace("’", "'").replace("‘", "'")


def _text(s: str) -> str:
    return _fix_mojibake(html.unescape(s)).strip()


def _city_from_address(addr: str) -> str | None:
    # "..., Hanford, CA 93230, USA" -> Hanford. "City of Atwater" -> Atwater.
    m = re.search(r",\s*([^,]+?),\s*CA\b", addr)
    if not m:
        return None
    city = m.group(1).strip()
    city = re.sub(r"^City of\s+", "", city, flags=re.I)
    return city


def extract(site_dir: Path) -> dict:
    src = (site_dir / "index.html").read_text(encoding="utf-8")

    # A page this tool already rendered carries its facts as JSON, so the
    # facts survive a re-render and never have to be scraped twice.
    m = re.search(r'<script type="application/json" id="cl-facts">(.*?)</script>', src, re.S)
    if m:
        facts = json.loads(m.group(1))
        facts["slug"] = site_dir.name
        return facts

    title = _text(re.search(r"<title>([^<]*)", src).group(1))
    name, _, rest = title.rpartition(" | ")
    category = rest.split(" in ")[0].strip()
    short_name = name.split(" | ")[0].strip()
    target_city = _text(re.search(r"Serving ([A-Za-z .'-]+?) and the Central Valley", src).group(1))

    phone = _text(re.search(r"Call (\(\d{3}\) \d{3}-\d{4})", src).group(1))
    tel = re.sub(r"\D", "", phone)

    ld = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', src, re.S).group(1))
    agg = ld.get("aggregateRating") or {}
    rating = float(agg["ratingValue"]) if agg.get("ratingValue") else None
    reviews = int(agg["reviewCount"]) if agg.get("reviewCount") else 0

    address = _text(re.search(r'mt-6 text-sm text-white/55">([^<]*)', src).group(1))
    address = re.sub(r",\s*USA$", "", address)
    place_id = re.search(r"place_id:'([^']+)'", src).group(1)

    credits_m = re.search(r"Photos: ([^<]*?), via Google\.", src)
    credits = _text(credits_m.group(1)) if credits_m else ""

    photos = []
    for m in re.finditer(r'<img src="(photo-\d+\.jpg)"[^>]*?width="(\d+)" height="(\d+)"', src, re.S):
        f, w, h = m.group(1), int(m.group(2)), int(m.group(3))
        if (site_dir / f).exists() and f not in [p["file"] for p in photos]:
            photos.append({"file": f, "w": w, "h": h})
    # Any photo on disk the old page did not place still counts.
    for p in sorted(site_dir.glob("photo-*.jpg"), key=lambda p: int(re.search(r"\d+", p.name).group())):
        if p.name not in [x["file"] for x in photos]:
            photos.append({"file": p.name, "w": 1600, "h": 1200})

    home_city = _city_from_address(address) or target_city

    return {
        "slug": site_dir.name,
        "name": name,
        "short_name": short_name,
        "category": category,          # the label the old engine chose
        "target_city": target_city,    # the town the engine was hunting in
        "city": home_city,             # where the business actually sits
        "phone": phone,
        "tel": tel,
        "rating": rating,
        "reviews": reviews,
        "address": address,
        "place_id": place_id,
        "credits": credits,
        "photos": photos,
    }
