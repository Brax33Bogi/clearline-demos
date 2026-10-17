"""What each trade's page says, and how to tell which trade a business is.

The old engine knew four trades and called everything else "Home Services".
It also trusted the Google category over the business's own name, which is
how A-1 Allstar Plumbing got a heating and air site. The name wins here,
with the category as the tie breaker when a name spans two trades.

Nothing in here states a fact about a specific business. Service lists,
hooks and promises are the ordinary offer of the trade; the facts (name,
phone, rating, address, photos) come from extract.py.
"""
from __future__ import annotations

import re

# ---------------------------------------------------------------------------
# Trades
# ---------------------------------------------------------------------------
TRADES: dict[str, dict] = {
    "hvac": {
        "label": "Heating and air",
        "verb": "heating and air",
        "hook": "Cool in summer, warm in winter, fixed the same day.",
        "sub": "Repair, replacement and tune-ups on every major brand. You get a straight price before anyone touches the unit.",
        "promise": "Same-day service on no-cool calls",
        "kind": "contractor",
        "look": "crisp",
        "services": [
            ("AC repair", "Diagnosed on the first visit and repaired the same day on most residential systems."),
            ("System replacement", "Right-sized equipment, installed clean, old unit hauled away."),
            ("Heating and furnace", "Ignition, blower and thermostat problems sorted before the cold hits."),
            ("Maintenance plans", "Seasonal tune-ups that keep the unit off the emergency list."),
            ("Ductwork", "Leaks sealed and airflow balanced so every room actually gets air."),
            ("Indoor air quality", "Filtration and ventilation upgrades for dust and allergy season."),
        ],
    },
    "refrigeration": {
        "label": "Heating, air and refrigeration",
        "verb": "heating, air and refrigeration",
        "hook": "Homes kept comfortable. Coolers and walk-ins kept cold.",
        "sub": "Residential comfort systems and commercial refrigeration from one crew. Straight pricing, parts on the truck.",
        "promise": "Same-day service on no-cool calls",
        "kind": "contractor",
        "look": "crisp",
        "services": [
            ("AC and heating repair", "Residential systems diagnosed and repaired on the first visit when the part is on hand."),
            ("Commercial refrigeration", "Walk-ins, reach-ins and display cases kept at temperature."),
            ("System replacement", "Right-sized equipment, installed clean, old unit hauled away."),
            ("Ice machines", "Cleaning, repair and replacement for restaurants and shops."),
            ("Maintenance plans", "Scheduled service that catches a failing compressor before it fails."),
            ("Ductwork", "Leaks sealed and airflow balanced so every room gets air."),
        ],
    },
    "ducts": {
        "label": "Air duct and dryer vent cleaning",
        "verb": "duct and dryer vent cleaning",
        "hook": "Cleaner air in every room, and a dryer vent that is not a fire risk.",
        "sub": "Whole-home duct cleaning and dryer vent clearing with before-and-after photos so you can see the difference.",
        "promise": "Most homes done in a single morning",
        "kind": "contractor",
        "look": "crisp",
        "services": [
            ("Air duct cleaning", "Supply and return ducts cleared of dust, dander and construction debris."),
            ("Dryer vent cleaning", "Lint cleared from the full run so the dryer works faster and safer."),
            ("Sanitizing", "Treatment for ducts after remodels, smoke or pests."),
            ("Vent and register cleaning", "Every grille pulled, washed and put back."),
            ("Inspections", "Camera look inside the system with photos you keep."),
            ("Filter upgrades", "Better filtration sized to the system you already have."),
        ],
    },
    "plumbing": {
        "label": "Plumbing",
        "verb": "plumbing",
        "hook": "Leaks stopped. Drains cleared. Done right the first time.",
        "sub": "Residential and light commercial plumbing. Upfront numbers, clean work, and someone who picks up the phone.",
        "promise": "Emergency calls answered 24 hours",
        "kind": "contractor",
        "look": "bold",
        "services": [
            ("Drain cleaning", "Kitchen, main line and sewer clogs cleared and camera checked."),
            ("Water heaters", "Tank and tankless repair, replacement and code-correct install."),
            ("Leak detection", "The source found without tearing out more wall than necessary."),
            ("Repipe", "Full and partial repipes for galvanized and failing copper."),
            ("Fixtures", "Faucets, toilets, disposals and shower valves swapped properly."),
            ("Emergency plumbing", "Burst lines and active leaks handled fast, any hour."),
        ],
    },
    "electrical": {
        "label": "Electrical",
        "verb": "electrical",
        "hook": "Power done right. Permitted, inspected, done once.",
        "sub": "Licensed electrical work for homes and small commercial. Panels, rewires, lighting and EV chargers.",
        "promise": "Licensed electrician on every job",
        "kind": "contractor",
        "look": "signal",
        "services": [
            ("Panel upgrades", "200A service upgrades and failing panel replacement."),
            ("Troubleshooting", "Dead circuits, breaker trips and flickering lights traced to the cause."),
            ("EV chargers", "Level 2 charger installs on a properly sized circuit."),
            ("Lighting", "Recessed, exterior and shop lighting installed and controlled."),
            ("Rewires", "Knob-and-tube and aluminum branch replacement."),
            ("Generators", "Interlocks and transfer switches for standby power."),
        ],
    },
    "motors": {
        "label": "Electric motor repair",
        "verb": "electric motor repair",
        "hook": "Motors rebuilt, rewound and back in service.",
        "sub": "Pumps, fans, compressors and ag motors repaired in the shop or replaced when that is the honest answer.",
        "promise": "Call for turnaround on your motor",
        "kind": "shop",
        "look": "signal",
        "services": [
            ("Motor rewinding", "Burnt windings replaced to original spec."),
            ("Bearing replacement", "Noisy or seized motors brought back smooth."),
            ("Pump repair", "Irrigation, well and booster pumps rebuilt."),
            ("New motors", "Replacement units sized and supplied when a rebuild does not pay."),
            ("Balancing and testing", "Every repair run and checked before it leaves."),
            ("Pickup and delivery", "Large motors collected and returned."),
        ],
    },
    "roofing": {
        "label": "Roofing",
        "verb": "roofing",
        "hook": "A roof that holds, and a straight answer about whether you need one.",
        "sub": "Repairs, replacements and honest inspections. We tell you when you do not need a new roof.",
        "promise": "Free roof inspection, no obligation",
        "kind": "contractor",
        "look": "heritage",
        "services": [
            ("Roof repair", "Targeted repair on leaks, flashing and storm damage."),
            ("Full replacement", "Tear-off and reroof with clean site protection and haul away."),
            ("Inspections", "A written condition report you can hand to an insurer or buyer."),
            ("Tile and shingle", "Composition, tile and flat systems all handled in house."),
            ("Gutters", "Replacement and repitching so water leaves the roof the right way."),
            ("Insurance claims", "Documentation and photos to support a legitimate claim."),
        ],
    },
    "construction": {
        "label": "General contracting",
        "verb": "construction",
        "hook": "Built right, from the first cut to the last coat.",
        "sub": "Additions, remodels and repairs with a written scope, a real schedule and a crew that cleans up.",
        "promise": "Written estimate after one walk-through",
        "kind": "contractor",
        "look": "workshop",
        "services": [
            ("Remodels", "Kitchens, baths and whole-home updates managed start to finish."),
            ("Additions", "Rooms, garages and ADUs from permit to final."),
            ("Roofing and exterior", "Roofs, siding and patio covers that stand up to valley heat."),
            ("Concrete and framing", "Foundations, slabs and structural framing done to code."),
            ("Repairs", "Dry rot, water damage and the jobs other contractors turned down."),
            ("Commercial work", "Tenant improvements and light commercial on a schedule."),
        ],
    },
    "handyman": {
        "label": "Handyman services",
        "verb": "handyman work",
        "hook": "The list of small jobs, done in one visit.",
        "sub": "Repairs, installs and the fixes that have been waiting. One person, one visit, one fair price.",
        "promise": "Most jobs scheduled within the week",
        "kind": "contractor",
        "look": "plain",
        "services": [
            ("Repairs", "Doors, drywall, trim, fences and the things that broke."),
            ("Installs", "Fans, fixtures, shelving, TV mounts and appliances."),
            ("Painting", "Rooms, trim and touch-ups done clean."),
            ("Plumbing fixes", "Faucets, toilets and disposals swapped properly."),
            ("Electrical fixes", "Outlets, switches and lighting replaced safely."),
            ("Punch lists", "The whole list knocked out in one trip."),
        ],
    },
    "concrete": {
        "label": "Concrete",
        "verb": "concrete",
        "hook": "Flatwork that stays flat.",
        "sub": "Driveways, patios, slabs and stamped finishes, formed right, poured right and finished by hand.",
        "promise": "Free on-site estimate, usually within 48 hours",
        "kind": "contractor",
        "look": "workshop",
        "services": [
            ("Driveways", "Removal and replacement, or new pours, with proper base and rebar."),
            ("Patios and walkways", "Broom, exposed aggregate and stamped finishes."),
            ("Slabs and foundations", "Shop, shed and addition slabs poured to spec."),
            ("Stamped and decorative", "Patterns and color that hold up to sun and sprinklers."),
            ("Retaining walls", "Block and poured walls that hold grade."),
            ("Demolition and haul off", "Old concrete out, site left clean."),
        ],
    },
    "fencing": {
        "label": "Fencing",
        "verb": "fencing",
        "hook": "Fences built straight, set to last.",
        "sub": "Wood, iron, chain link and vinyl fencing for homes, ranches and businesses. Posts set deep, lines kept true.",
        "promise": "Free on-site estimate, usually within 48 hours",
        "kind": "contractor",
        "look": "workshop",
        "services": [
            ("Wood fencing", "Redwood and cedar privacy fences with steel or treated posts."),
            ("Wrought iron", "Gates, railings and security fencing fabricated and installed."),
            ("Chain link", "Residential, commercial and ag runs of any length."),
            ("Vinyl", "Low-maintenance privacy and ranch rail."),
            ("Gates and openers", "Swing and slide gates, manual or automated."),
            ("Repairs", "Leaning posts, broken panels and storm damage fixed."),
        ],
    },
    "landscaping": {
        "label": "Landscaping",
        "verb": "landscaping",
        "hook": "Yards that look good all year, not just the week after.",
        "sub": "Design, install and maintenance for homes and commercial properties. Irrigation that works and plants that belong in this climate.",
        "promise": "Free on-site estimate, usually within 48 hours",
        "kind": "yard",
        "look": "field",
        "services": [
            ("Landscape design and install", "Plans built for valley heat and water rules, then built as drawn."),
            ("Lawn care and maintenance", "Weekly and biweekly service that keeps the property sharp."),
            ("Irrigation and sprinklers", "Repairs, drip conversions and smart controllers."),
            ("Planting and sod", "Trees, shrubs and turf that take hold."),
            ("Clean ups and hauling", "Overgrown yards brought back and the debris gone."),
            ("Hardscape", "Pavers, borders and gravel that cut the mowing."),
        ],
    },
    "tree": {
        "label": "Tree service",
        "verb": "tree work",
        "hook": "Trees trimmed, removed and cleaned up the same day.",
        "sub": "Trimming, removals and stump grinding by a crew with the right equipment, with the yard left clean.",
        "promise": "Free estimate, storm damage moved to the front of the line",
        "kind": "yard",
        "look": "field",
        "services": [
            ("Tree trimming", "Shaping, thinning and deadwood removal that keeps the tree healthy."),
            ("Tree removal", "Hazard and unwanted trees taken down safely, any size."),
            ("Stump grinding", "Stumps ground below grade so you can plant or pave."),
            ("Storm damage", "Fallen limbs and split trees cleared fast."),
            ("Palm trimming", "Dead fronds and seed pods cleared before they drop."),
            ("Hauling", "Everything chipped or hauled, nothing left on the lawn."),
        ],
    },
    "pool": {
        "label": "Pool service",
        "verb": "pool service",
        "hook": "Clear water every week, and repairs before small problems get big.",
        "sub": "Weekly cleaning, chemistry and equipment repair so the pool is ready whenever you are.",
        "promise": "Weekly service on a set day, same tech every time",
        "kind": "yard",
        "look": "field",
        "services": [
            ("Weekly cleaning", "Skim, brush, vacuum and chemistry on a fixed day."),
            ("Equipment repair", "Pumps, filters, heaters and automation fixed or replaced."),
            ("Green pool recovery", "Neglected water brought back clear."),
            ("Filter cleaning", "Cartridge and DE filters cleaned on schedule."),
            ("Leak detection", "Water loss found and fixed."),
            ("Openings and inspections", "Seasonal checks and pre-sale inspections."),
        ],
    },
    "nursery": {
        "label": "Nursery and garden center",
        "verb": "nursery",
        "hook": "Plants that grow here, from people who grow them here.",
        "sub": "Trees, shrubs, flowers and soil for the Central Valley climate, with advice from people who plant them every day.",
        "promise": "Open to the public, no appointment needed",
        "kind": "shop",
        "look": "field",
        "services": [
            ("Trees and shrubs", "Fruit, shade and ornamental trees suited to valley heat."),
            ("Flowers and color", "Seasonal annuals and perennials, ready to plant."),
            ("Vegetables and herbs", "Starts for every season in the valley."),
            ("Soil, mulch and amendments", "Bagged and bulk."),
            ("Pots and planters", "Sizes for patios, porches and entries."),
            ("Advice", "Bring a photo or a leaf and we will tell you what is going on."),
        ],
    },
    "autoglass": {
        "label": "Auto glass and window tint",
        "verb": "auto glass and tint",
        "hook": "Glass replaced and tint laid clean, usually the same day.",
        "sub": "Windshield replacement, chip repair and window tint done in the shop or at your driveway. Insurance handled for you.",
        "promise": "Most windshields replaced same day",
        "kind": "auto",
        "look": "shop",
        "services": [
            ("Windshield replacement", "OEM-quality glass, set with the right urethane and cure time."),
            ("Chip and crack repair", "Small damage fixed before it spreads across the glass."),
            ("Window tint", "Ceramic and carbon films cut to the vehicle, no bubbles, legal shades."),
            ("Side and rear glass", "Door, quarter and back glass replaced and cleaned out."),
            ("Mobile service", "We come to your home or work."),
            ("Insurance claims", "Direct billing with most carriers."),
        ],
    },
    "glass": {
        "label": "Glass, windows and doors",
        "verb": "glass work",
        "hook": "Glass, windows and doors, measured right and fitted clean.",
        "sub": "Replacement windows, shower enclosures, storefront glass and mirrors, measured by the people who install them.",
        "promise": "Free in-home measure and quote",
        "kind": "contractor",
        "look": "shop",
        "services": [
            ("Replacement windows", "Dual-pane units sized to the opening and sealed properly."),
            ("Shower enclosures", "Frameless and framed glass cut and hung plumb."),
            ("Mirrors and table tops", "Custom cut, polished edges."),
            ("Storefront glass", "Commercial doors and glazing, emergency board-up."),
            ("Doors", "Entry, patio and sliding doors installed and adjusted."),
            ("Screens and repairs", "Rescreens, broken glass and hardware fixed."),
        ],
    },
    "appliance": {
        "label": "Appliance repair",
        "verb": "appliance repair",
        "hook": "Appliances fixed in your home, usually in one visit.",
        "sub": "Washers, dryers, fridges, ovens and dishwashers repaired by a tech who carries the common parts on the truck.",
        "promise": "Same or next-day appointments",
        "kind": "shop",
        "look": "shop",
        "services": [
            ("Refrigerators and freezers", "Not cooling, leaking or noisy, diagnosed on the first visit."),
            ("Washers and dryers", "Spin, drain and heat problems on every major brand."),
            ("Ovens and ranges", "Gas and electric, ignition, element and control repairs."),
            ("Dishwashers", "Leaks, drain and wash problems fixed in place."),
            ("Commercial units", "Restaurant and laundromat equipment kept running."),
            ("Installs", "New units set, leveled and connected."),
        ],
    },
    "auto": {
        "label": "Auto repair",
        "verb": "auto repair",
        "hook": "Honest repairs, written estimate first.",
        "sub": "Diagnostics, maintenance and repair on cars and light trucks. You approve the price before any work starts.",
        "promise": "Call for same-day availability",
        "kind": "auto",
        "look": "shop",
        "services": [
            ("Diagnostics", "Check engine lights and drivability problems traced to the cause."),
            ("Brakes", "Pads, rotors and hydraulics done with quality parts."),
            ("Oil and maintenance", "Factory-schedule service that keeps the warranty intact."),
            ("Engine and transmission", "Repairs explained in plain words before you decide."),
            ("Electrical", "Starters, alternators, batteries and wiring faults."),
            ("Heating and AC", "Cold air back before summer hits."),
        ],
    },
    "autoelectric": {
        "label": "Auto electric",
        "verb": "auto electrical repair",
        "hook": "Starters, alternators and wiring faults, found and fixed.",
        "sub": "Automotive electrical specialists for cars, trucks and ag equipment. The fault traced, not guessed at.",
        "promise": "Call for same-day availability",
        "kind": "auto",
        "look": "shop",
        "services": [
            ("Starters and alternators", "Rebuilt or replaced, tested before they go back in."),
            ("Wiring and shorts", "Intermittent faults traced to the wire."),
            ("Batteries and charging", "Load tested, replaced and the charging system checked."),
            ("Lighting and accessories", "Headlights, trailer wiring and add-ons done right."),
            ("Ag and fleet", "Tractors, trucks and equipment electrical."),
            ("Diagnostics", "Check engine and sensor faults read and explained."),
        ],
    },
    "oilchange": {
        "label": "Oil change and quick service",
        "verb": "quick lube",
        "hook": "In and out, oil changed, no appointment.",
        "sub": "Drive-through oil changes and basic maintenance while you wait in the car.",
        "promise": "No appointment, most cars done in 15 minutes",
        "kind": "auto",
        "look": "shop",
        "services": [
            ("Oil changes", "Conventional, blend and full synthetic with a quality filter."),
            ("Fluids", "Transmission, coolant, brake and power steering topped or exchanged."),
            ("Filters", "Air and cabin filters checked and replaced."),
            ("Wipers and bulbs", "Swapped while you wait."),
            ("Tire pressure and inspection", "Every visit, no charge."),
            ("Fleet accounts", "Billing for work vehicles."),
        ],
    },
    "garagedoor": {
        "label": "Garage doors",
        "verb": "garage door service",
        "hook": "Garage doors fixed today, springs to openers.",
        "sub": "Repair and replacement for residential garage doors and openers, with the common parts on the truck.",
        "promise": "Same-day repairs on most calls",
        "kind": "contractor",
        "look": "shop",
        "services": [
            ("Spring replacement", "Torsion and extension springs replaced in pairs, safely."),
            ("Opener repair and install", "Belt and chain drives, smart openers, remotes and keypads."),
            ("New doors", "Steel, wood-look and insulated doors measured and installed."),
            ("Off-track and cable repair", "Doors back on the rails and balanced."),
            ("Panels and sections", "Dented or broken sections replaced."),
            ("Tune-ups", "Lubed, balanced and safety-tested."),
        ],
    },
    "cleaning": {
        "label": "Window and solar panel cleaning",
        "verb": "exterior cleaning",
        "hook": "Windows and solar panels, spotless.",
        "sub": "Residential and commercial window cleaning, solar panel washing and pressure washing on a schedule or one time.",
        "promise": "Free quote by phone or text",
        "kind": "yard",
        "look": "plain",
        "services": [
            ("Window cleaning", "Inside and out, tracks and screens included."),
            ("Solar panel cleaning", "Deionized water, no chemicals, more output."),
            ("Pressure washing", "Driveways, patios and siding brought back."),
            ("Gutter cleaning", "Cleared before the first rain."),
            ("Commercial", "Storefronts and offices on a route."),
            ("Recurring plans", "Monthly or quarterly so it never gets bad."),
        ],
    },
    "repairshop": {
        "label": "Phone and electronics repair",
        "verb": "electronics repair",
        "hook": "Phones, tablets and TVs fixed in days, not weeks.",
        "sub": "Screens, batteries, charge ports and more, repaired in the shop with a warranty on the work.",
        "promise": "Most phone repairs done while you wait",
        "kind": "shop",
        "look": "shop",
        "services": [
            ("Screen replacement", "Phones and tablets, every major brand."),
            ("Battery replacement", "Back to a full day on one charge."),
            ("Charge port repair", "Loose, dirty or dead ports fixed."),
            ("Water damage", "Cleaned and assessed before you buy a new one."),
            ("TV and audio", "Boards, backlights and power supplies repaired."),
            ("Game consoles and laptops", "Drives, fans, ports and screens."),
        ],
    },
    "hardware": {
        "label": "Hardware store",
        "verb": "hardware",
        "hook": "The part you need and someone who knows what it is.",
        "sub": "Plumbing, electrical, paint, tools and the odd fitting the big box does not stock, from people who can tell you how to use it.",
        "promise": "Open to the public, walk-ins welcome",
        "kind": "shop",
        "look": "plain",
        "services": [
            ("Plumbing parts", "Fittings, valves, water heater parts and repair kits."),
            ("Electrical", "Wire, breakers, boxes and fixtures."),
            ("Paint and supplies", "Mixed in store, with the brushes and tape to go with it."),
            ("Tools and fasteners", "Hand tools, power tools and bulk hardware."),
            ("Lawn and garden", "Irrigation, hoses and seasonal supplies."),
            ("Keys and repairs", "Keys cut, screens rescreened, glass cut."),
        ],
    },
    "general": {
        "label": "Home services",
        "verb": "work",
        "hook": "Work you can count on.",
        "sub": "Repairs, installs and maintenance for homeowners across the Central Valley. Straight pricing and clean work.",
        "promise": "Free estimate, no pressure",
        "kind": "contractor",
        "look": "plain",
        "services": [
            ("Repairs", "Fast diagnosis and repair on the problem you called about."),
            ("Installation", "New equipment sized and installed correctly the first time."),
            ("Maintenance", "Scheduled service that heads off emergency calls."),
            ("Inspections", "A written report on what is actually going on."),
            ("Emergency service", "Available when the problem cannot wait."),
            ("Free estimates", "A real number before any work begins."),
        ],
    },
}

# Name patterns in three tiers. Tier 1 is a niche trade and always wins over
# the Google category. Tier 2 is a core trade, where the category breaks a tie
# when a name spans two of them. Tier 3 is a vague word that only counts when
# nothing else matched and the category says nothing.
_NAME_RULES: list[tuple[int, str, str]] = [
    (1, r"auto\s*glass|window\s*tint|\btint\b|paint protection|wraps", "autoglass"),
    (1, r"auto\s*electric", "autoelectric"),
    (1, r"oil change", "oilchange"),
    (1, r"auto repair|automotive|\bauto\b", "auto"),
    (1, r"garage door", "garagedoor"),
    (1, r"appliance", "appliance"),
    (1, r"ifix|phone repair|television|\btv\b|audio repair|electronics", "repairshop"),
    (1, r"electric motor", "motors"),
    (1, r"duct|dryer vent", "ducts"),
    (1, r"refrigeration", "refrigeration"),
    (1, r"solar panel cleaning|window cleaning|pressure wash|washing", "cleaning"),
    (1, r"nursery", "nursery"),
    (1, r"hardware", "hardware"),
    (1, r"handyman", "handyman"),
    (1, r"concrete|bomanite|cement", "concrete"),
    (1, r"fenc", "fencing"),
    (1, r"\btree", "tree"),
    (1, r"\bpool", "pool"),
    (1, r"landscap|gardening|yard|lawn", "landscaping"),
    (1, r"\bglass\b|windows? (&|and) doors", "glass"),
    (2, r"roof", "roofing"),
    (2, r"plumb|sewer|drain|lateral", "plumbing"),
    (2, r"electric|energy|solar", "electrical"),
    (2, r"heat|\bair\b|hvac|cooling|a/?c\b|sheet metal|breez", "hvac"),
    (3, r"comfort", "hvac"),
    (3, r"construction|builders|contractor|home improvement|home services|general inc", "construction"),
]

_CATEGORY = {
    "Heating & Air": "hvac",
    "Plumbing": "plumbing",
    "Electrical": "electrical",
    "Roofing": "roofing",
}


def detect_trade(name: str, category: str) -> str:
    n = name.lower()
    hits: list[tuple[int, int, int, str]] = []  # (start, rule index, tier, key)
    for i, (tier, pat, key) in enumerate(_NAME_RULES):
        m = re.search(pat, n)
        if m:
            hits.append((m.start(), i, tier, key))
    hits.sort()
    cat = _CATEGORY.get(category)
    tier1 = [k for _, _, t, k in hits if t == 1]
    if tier1:
        return tier1[0]
    tier2 = [k for _, _, t, k in hits if t == 2]
    if tier2:
        return cat if cat in tier2 else tier2[0]
    if cat:
        return cat
    tier3 = [k for _, _, t, k in hits if t == 3]
    return tier3[0] if tier3 else "general"


# ---------------------------------------------------------------------------
# Service areas, by where the business actually sits
# ---------------------------------------------------------------------------
_REGIONS: dict[str, list[str]] = {
    "fresno": ["Fresno", "Clovis", "Sanger", "Selma", "Fowler", "Kingsburg", "Reedley", "Madera", "Kerman", "Parlier", "Dinuba"],
    "southvalley": ["Visalia", "Tulare", "Hanford", "Lemoore", "Exeter", "Farmersville", "Dinuba", "Lindsay", "Porterville", "Kingsburg", "Selma", "Corcoran"],
    "merced": ["Merced", "Atwater", "Los Banos", "Chowchilla", "Madera", "Livingston", "Turlock", "Dos Palos"],
    "stanislaus": ["Modesto", "Turlock", "Ceres", "Hilmar", "Patterson", "Oakdale", "Riverbank", "Manteca", "Tracy", "Merced"],
    "porterville": ["Porterville", "Delano", "Tulare", "Visalia", "Lindsay", "Exeter", "McFarland", "Wasco"],
}
_CITY_REGION = {
    **{c: "fresno" for c in ["Fresno", "Clovis", "Sanger", "Selma", "Fowler", "Kingsburg", "Reedley", "Madera", "Kerman", "Parlier", "Dinuba", "Cutler"]},
    **{c: "southvalley" for c in ["Visalia", "Tulare", "Hanford", "Lemoore", "Exeter", "Farmersville", "Lindsay", "Corcoran"]},
    **{c: "merced" for c in ["Merced", "Atwater", "Los Banos", "Chowchilla", "Livingston", "Dos Palos"]},
    **{c: "stanislaus" for c in ["Modesto", "Turlock", "Ceres", "Hilmar", "Patterson", "Oakdale", "Riverbank", "Manteca", "Tracy"]},
    **{c: "porterville" for c in ["Porterville", "Delano", "McFarland", "Wasco"]},
}


def service_areas(home_city: str, target_city: str, limit: int = 10) -> list[str]:
    """Towns around the business, the town it was found for first."""
    region = _CITY_REGION.get(home_city) or _CITY_REGION.get(target_city) or "fresno"
    towns = list(_REGIONS[region])
    if _CITY_REGION.get(target_city) == region:
        towns.insert(0, target_city)
    else:
        towns.append(target_city)
    out: list[str] = []
    for t in towns:
        if t != home_city and t not in out:
            out.append(t)
    return out[:limit]


# ---------------------------------------------------------------------------
# Trust and FAQ by kind of business
# ---------------------------------------------------------------------------
TRUST = {
    "contractor": [
        ("Licensed and insured", "Ask for the numbers before any work starts. Ask every contractor you talk to, not just us."),
        ("A written price first", "You see the number before anybody picks up a tool. No day-of surprises."),
        ("Workmanship guaranteed", "If something we did is not right, we come back and make it right."),
        ("Somebody answers", "A person picks up during hours. On a job, you get a call back the same day."),
    ],
    "yard": [
        ("Licensed and insured", "Ask for the numbers before any work starts. Ask every crew you talk to."),
        ("Free on-site estimate", "We look at the property and give you a real number, not a guess over the phone."),
        ("Clean up is part of the job", "Debris hauled, walkways blown, nothing left on the lawn."),
        ("Same crew, every time", "You know who is coming and they know your property."),
    ],
    "shop": [
        ("Locally owned and operated", "The owner is in the building. Ask for them."),
        ("Straight answers", "If it is not worth fixing, we say so before you pay for anything."),
        ("Price before work", "You approve the number first. No surprises at pickup."),
        ("Walk in or call ahead", "Call and we will have it ready, or come by during hours."),
    ],
    "auto": [
        ("Locally owned and operated", "The owner is in the shop. Ask for them."),
        ("Written estimate first", "You approve the price before any work starts."),
        ("Quality parts, work explained", "We show you the old part and tell you what it did."),
        ("Call for same-day", "Most days we can fit you in. Call before you drive over."),
    ],
}


def faqs(kind: str, city: str, phone: str, promise: str, label: str) -> list[tuple[str, str]]:
    area = f"Do you serve {city} and the surrounding area?"
    area_a = f"Yes. {city} is home base and we cover the surrounding towns. If you are not sure whether you are in range, call {phone} and ask. It takes ten seconds."
    if kind in ("contractor", "yard"):
        return [
            (area, area_a),
            ("How much does it cost?", "Every job is priced after we see it, because guessing over the phone is how people end up with a bill they did not expect. The estimate is free and there is no obligation."),
            ("How fast can you get out here?", f"{promise}. Urgent work moves to the front of the line."),
            ("Are you licensed and insured?", "Yes. We will hand you the numbers before any work starts, and you should ask every contractor for them."),
            ("What happens after I ask for a quote?", "Somebody calls you back, usually the same day. We set a time, look at the job, and you get a written price. No deposit to get a quote."),
            ("Do you offer a warranty?", "Yes. Workmanship is guaranteed and manufacturer warranties pass straight through to you."),
        ]
    if kind == "auto":
        return [
            (area, f"Yes. The shop is in {city} and people drive in from the surrounding towns. Call {phone} if you want to check hours before you come."),
            ("Do I need an appointment?", f"{promise}. A quick call gets you a slot and means the parts are here when you are."),
            ("How much will it cost?", "You get a written estimate after we look at it, and nothing happens until you approve it."),
            ("Do you use quality parts?", "Yes. We use parts we would put on our own vehicles, and we show you the old ones."),
            ("Is the work guaranteed?", "Yes. If something we did is not right, bring it back and we make it right."),
            ("How do I get a quote?", f"Call {phone} or send the form on this page. Tell us the year, make, model and what it is doing."),
        ]
    # shop
    return [
        (area, f"Yes. We are in {city} and people come in from the surrounding towns. Call {phone} to check hours or whether we have what you need."),
        ("Do I need an appointment?", f"{promise}. A quick call ahead never hurts."),
        ("How much will it cost?", "We tell you the price before any work or order. If it is not worth doing, we say so."),
        ("Is the work guaranteed?", "Yes. If something we did is not right, bring it back and we make it right."),
        ("What should I bring?", "The item, or a photo and a part number if you have one. If you are not sure, call and describe it."),
        ("How do I reach you?", f"Call {phone}, or send the form on this page and somebody gets back to you."),
    ]
