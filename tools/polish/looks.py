"""Eight visual systems, so 158 pages do not look like one file.

None of them is Clearline's own brand. A demo site wears the prospect's trade,
not ours: the only Clearline pieces on the page are the preview strip and the
credit line from brand/demo-site-chrome.html. Ink and ultramarine, Space
Grotesk and Manrope stay off these pages on purpose.

Each look sets type, corner radius and which layout each section uses.
Each trade sets the palette inside that look.
"""

LOOKS = {
    # Clean, modern, rounded. Heating and air.
    "crisp": {
        "fonts": "Plus+Jakarta+Sans:wght@500;700;800",
        "display": "'Plus Jakarta Sans'", "body": "'Plus Jakarta Sans'",
        "dw": 800, "dls": "-0.03em", "dtt": "none", "dlh": 1.04,
        "rc": "10px", "rk": "18px",
        "hero": "split", "services": "cards", "gallery": "bento", "kicker": "upper",
    },
    # Heavy, square, high contrast. Plumbing.
    "bold": {
        "fonts": "Archivo:wght@500;700;900&family=Inter:wght@400;500;600",
        "display": "Archivo", "body": "Inter",
        "dw": 900, "dls": "-0.035em", "dtt": "none", "dlh": 1.0,
        "rc": "0px", "rk": "0px",
        "hero": "cover", "services": "tiles", "gallery": "strip", "kicker": "upper",
    },
    # Geometric, amber on charcoal. Electrical.
    "signal": {
        "fonts": "Sora:wght@500;700;800&family=Inter:wght@400;500;600",
        "display": "Sora", "body": "Inter",
        "dw": 800, "dls": "-0.03em", "dtt": "none", "dlh": 1.06,
        "rc": "6px", "rk": "12px",
        "hero": "split", "services": "rows", "gallery": "bento", "kicker": "upper",
    },
    # Serif, warm, editorial. Roofing.
    "heritage": {
        "fonts": "Fraunces:opsz,wght@9..144,500;9..144,700&family=Source+Sans+3:wght@400;600;700",
        "display": "Fraunces", "body": "'Source Sans 3'",
        "dw": 700, "dls": "-0.02em", "dtt": "none", "dlh": 1.04,
        "rc": "4px", "rk": "8px",
        "hero": "paper", "services": "rows", "gallery": "columns", "kicker": "small",
    },
    # Condensed, uppercase, industrial. Concrete, fencing, construction.
    "workshop": {
        "fonts": "Big+Shoulders+Display:wght@700;900&family=Public+Sans:wght@400;600;700",
        "display": "'Big Shoulders Display'", "body": "'Public Sans'",
        "dw": 900, "dls": "0.005em", "dtt": "uppercase", "dlh": 0.94,
        "rc": "0px", "rk": "4px",
        "hero": "cover", "services": "tiles", "gallery": "strip", "kicker": "upper",
    },
    # Soft serif, very rounded, cream. Landscaping, trees, pools, nursery.
    "field": {
        "fonts": "DM+Serif+Display&family=DM+Sans:wght@400;500;700",
        "display": "'DM Serif Display'", "body": "'DM Sans'",
        "dw": 400, "dls": "-0.015em", "dtt": "none", "dlh": 1.06,
        "rc": "999px", "rk": "22px",
        "hero": "paper", "services": "cards", "gallery": "bento", "kicker": "small",
    },
    # Graphite, friendly geometric. Glass, auto, appliances, repair shops.
    "shop": {
        "fonts": "Outfit:wght@500;700;800",
        "display": "Outfit", "body": "Outfit",
        "dw": 800, "dls": "-0.025em", "dtt": "none", "dlh": 1.04,
        "rc": "12px", "rk": "18px",
        "hero": "split", "services": "cards", "gallery": "strip", "kicker": "upper",
    },
    # Quiet, dependable. Handyman, hardware, cleaning, anything else.
    "plain": {
        "fonts": "Figtree:wght@500;700;800",
        "display": "Figtree", "body": "Figtree",
        "dw": 800, "dls": "-0.03em", "dtt": "none", "dlh": 1.06,
        "rc": "8px", "rk": "14px",
        "hero": "split", "services": "rows", "gallery": "bento", "kicker": "upper",
    },
}

# accent, deep accent (hover / dark band link), ink (dark bands), wash (light
# band), text colour on the accent, and whether headings on the accent field
# need ink instead of white.
PALETTES = {
    "hvac":          ("#0b63c7", "#084a95", "#0b1f33", "#eef4fb", "#ffffff"),
    "refrigeration": ("#0a7a8c", "#075f6d", "#092a30", "#ecf6f7", "#ffffff"),
    "ducts":         ("#1a8fa0", "#13707d", "#0b2a30", "#ecf6f7", "#ffffff"),
    "plumbing":      ("#0f6b8a", "#0b5068", "#082430", "#ecf5f8", "#ffffff"),
    "electrical":    ("#e39a12", "#b87a06", "#1c1a14", "#fbf6ea", "#1c1a14"),
    "motors":        ("#c97c0a", "#a06205", "#1c1a14", "#fbf5ea", "#1c1a14"),
    "roofing":       ("#b5542a", "#8f3f1c", "#2a1710", "#faf3ee", "#ffffff"),
    "construction":  ("#c2651b", "#9a4d10", "#1f1b17", "#f8f3ed", "#ffffff"),
    "handyman":      ("#2f6f4e", "#23543b", "#14221b", "#eef5f1", "#ffffff"),
    "concrete":      ("#e0702a", "#b9561a", "#1d2126", "#f2f3f5", "#ffffff"),
    "fencing":       ("#7a5230", "#5b3c22", "#241a12", "#f7f2ec", "#ffffff"),
    "landscaping":   ("#2e7d4f", "#215e3b", "#10281b", "#eef6ef", "#ffffff"),
    "tree":          ("#3b7a3a", "#2b5c2a", "#12240f", "#eff5ec", "#ffffff"),
    "pool":          ("#0e8ab3", "#0a6b8a", "#082a36", "#ebf6fa", "#ffffff"),
    "nursery":       ("#4e8a3c", "#3a692c", "#15261a", "#f1f6ec", "#ffffff"),
    "autoglass":     ("#1f6fd8", "#1654a8", "#0d1420", "#eef2f7", "#ffffff"),
    "glass":         ("#2a7ab8", "#1f5d8d", "#0f1a24", "#eef3f7", "#ffffff"),
    "appliance":     ("#c6462b", "#9c3520", "#1d1d1d", "#f8f1ee", "#ffffff"),
    "auto":          ("#c8311f", "#9b2415", "#161616", "#f6f3f1", "#ffffff"),
    "autoelectric":  ("#d6a211", "#ad820c", "#171410", "#fbf6e9", "#171410"),
    "oilchange":     ("#e3a71a", "#b8860f", "#17150f", "#fbf6ea", "#17150f"),
    "garagedoor":    ("#2b5ea8", "#204a85", "#0f1a2c", "#eef2f8", "#ffffff"),
    "cleaning":      ("#1b9bd1", "#157aa5", "#0b2230", "#ecf6fb", "#ffffff"),
    "repairshop":    ("#5a3fd6", "#4631a8", "#15122a", "#f1eefb", "#ffffff"),
    "hardware":      ("#b23a2e", "#8a2c23", "#1f1715", "#f8f0ee", "#ffffff"),
    "general":       ("#1d4e6b", "#163c52", "#0c1f2b", "#eef3f6", "#ffffff"),
}
