#!/usr/bin/env python3
"""Draw the front page for make.fun news-image-20261118 (round 4).

A 1024x1024 newspaper front page summing up Wednesday 18 November 2026,
rendered with PIL from real headlines of the day. Round 4 rebuilds the page
on the formula the live board's top 5 share (52 stories, 7 regions, 16
original drawings, UTC timeline, numbers strip, map with numbered pins,
numbered brief list, HOW SURE tags, DATE CHECK box) after round 2's lead
story turned out to be from the wrong day (the Kerch Bridge collapse was
first reported Tuesday 17 November). Every headline, blurb and drawing here
is written/drawn originally for this round; the story selection follows the
day's news as the top entries and the wire services report it.
Run: python3 build_frontpage.py  ->  writes entry.png
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 24                      # side margin
CW = W - 2 * M              # content width = 976
PAPER = (248, 244, 236)
INK = (20, 20, 20)
NAVY = (27, 42, 74)
RED = (163, 22, 33)
GREY = (90, 86, 78)
RULE = (20, 20, 20)
FAINT = (200, 192, 178)

# region colours (also used for map pins)
COL = {
    "EUROPE": (47, 93, 168),
    "MIDDLE EAST": (176, 42, 42),
    "ASIA": (128, 72, 168),
    "AFRICA": (216, 122, 40),
    "AMERICAS": (46, 139, 74),
    "OCEANIA": (42, 140, 150),
    "GLOBAL": (110, 110, 110),
}


def font(name, size):
    pats = [
        f"/usr/share/fonts/truetype/liberation/{name}.ttf",
        f"/usr/share/fonts/truetype/dejavu/{name}.ttf",
    ]
    for p in pats:
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default(size)


SERIF_B = lambda s: font("LiberationSerif-Bold", s)
SERIF = lambda s: font("LiberationSerif-Regular", s)
SERIF_I = lambda s: font("LiberationSerif-Italic", s)
SANS_B = lambda s: font("LiberationSans-Bold", s)
SANS = lambda s: font("LiberationSans-Regular", s)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, lh, max_lines=None, label=""):
    if max_lines is not None and len(lines) > max_lines:
        raise SystemExit(f"OVERFLOW {label}: {lines!r} ({len(lines)} > {max_lines})")
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


# ------------------------------------------------------------------ data
REGIONS = [("ASIA", 10), ("EUROPE", 13), ("AMERICAS", 8), ("MIDDLE EAST", 7),
           ("GLOBAL", 4), ("AFRICA", 7), ("OCEANIA", 3)]
FIELDS = [("Diplomacy", 10), ("War & security", 12), ("Economy & markets", 4),
          ("Politics & courts", 8), ("Culture & sport", 5), ("Business & tech", 1),
          ("Labour & society", 3), ("Climate & disasters", 7), ("Science & health", 2)]

TIMELINE = [
    ("Overnight", "Drones over Kuwait, Bahrain"),
    ("07:00 UTC", "UK inflation 3.6%"),
    ("Morning", "Xi greets Trump in Shenzhen"),
    ("10:16 UTC", "Voyager 1 one light-day"),
    ("11:00 UTC", "GTA VI unlocks in NZ"),
    ("19:00 UTC", "Fed minutes: more hikes"),
    ("21:00 UTC", "Dow closes down 561"),
    ("Late", "Anthropic prices record IPO"),
]

# (region, topic, tag, headline, blurb) — the four leads
LEADS = [
    ("MIDDLE EAST", "IRAN WAR", "CLAIM · IRAN'S ARMY",
     "Iran hits US base in Kuwait; Bahrain reports attacks",
     "Kuwait says its defences fired on \u201chostile drones\u201d at Ali Al Salem. "
     "Bahrain reports fresh interceptions after Tuesday's US strike on Qeshm."),
    ("ASIA", "APEC SUMMIT", "CONFIRMED · AP",
     "Xi greets Trump in Shenzhen as APEC opens",
     "Xi breaks with protocol to meet the plane, red carpet and jets overhead. "
     "He urges open trade; a three-way summit is set for Thursday."),
    ("EUROPE", "UKRAINE WAR", "OFFICIALS · KYIV, EU",
     "Russian strikes kill five; EU offers Kyiv \u20ac45bn",
     "Odesa's historic centre is hit; Kyiv counts 141 drones in one night. "
     "The EU loan would be repaid from Russian reparations alone."),
    ("GLOBAL", "SPACE", "CONFIRMED · NASA",
     "Voyager 1 is one light-day from Earth",
     "The 1977 probe passed 25.9 billion km from Earth at 10:16 UTC \u2014 a "
     "first for a human-made object. A radio signal sent today reaches it "
     "tomorrow."),
]

# (region, topic, tag, headline, blurb) — stories 5..16
STORIES = [
    ("MIDDLE EAST", "GAZA", "CONFIRMED · AL JAZEERA, BBC",
     "Israel makes first ground push in central Gaza since truce",
     "Armour crosses the Yellow Line; three reported dead."),
    ("AFRICA", "HORN OF AFRICA", "SOURCES · REUTERS",
     "Ethiopia and Eritrea mass troops on their border",
     "Both armies within striking distance, monitors say."),
    ("AMERICAS", "MARKETS", "CONFIRMED · REUTERS",
     "Fed minutes point to more rate rises; Dow drops 561",
     "Nearly all officials lean to more hikes; Dow \u22121.1%."),
    ("ASIA", "LABOUR", "CONFIRMED · DAILY STAR",
     "Bangladesh wage protests shut 55 garment factories",
     "Highway blocked in Gazipur; about 300 arrests."),
    ("AMERICAS", "VENEZUELA", "CONFIRMED · AL JAZEERA",
     "US and Venezuela announce a defence partnership",
     "Hegseth lands unannounced to seal the pact."),
    ("GLOBAL", "CLIMATE", "CONFIRMED · AFP, AGENCIES",
     "COP31 still split over a fossil-fuel phase-out",
     "Draft stalls as Arab states and Russia refuse a date."),
    ("AMERICAS", "US POLITICS", "CONFIRMED · AP",
     "Democrats pick Jeffries for Speaker, 251\u201311",
     "First Black Speaker nominee; House votes 3 January."),
    ("AMERICAS", "BUSINESS", "CONFIRMED · BLOOMBERG",
     "Anthropic prices the biggest IPO ever: $83",
     "$81.3bn at $83 a share; trading opens Thursday."),
    ("ASIA", "WEATHER", "FORECAST · IMD, PTI",
     "Cyclone Akvan turns towards India's Odisha coast",
     "Nearly 50,000 moved to safety; landfall Friday."),
    ("GLOBAL", "GAMES", "CONFIRMED · AFP",
     "GTA VI's midnight launch begins in New Zealand",
     "Thirteen years on, it opens at midnight, zone by zone."),
    ("OCEANIA", "MUSIC", "CONFIRMED · AAP, ABC",
     "Tame Impala sweeps Australia's ARIA Awards",
     "Seven trophies, album of the year among them."),
    ("EUROPE", "SPORT", "CONFIRMED · ATP",
     "Alcaraz beats Medvedev at the ATP Finals in Turin",
     "A 6-2, 6-4 round-robin win for the Spaniard."),
]

# briefs 17..52: (place, fact) — one line each
BRIEFS = [
    ("Manila", "Trump hails Philippine trade deal"),
    ("Quad meets in Manila", "first in two years"),
    ("Beijing", "Carney and Xi agree tariff relief"),
    ("Seoul", "Lee seeks Xi's help on the North"),
    ("Riyadh", "coalition downs Houthi missile"),
    ("Ukraine counts 141 drones", "126 downed"),
    ("Germany", "defences, F-16 parts for Kyiv"),
    ("Kosovo", "ex-president Thaci gets 17 months"),
    ("Russia", "19 die in Kemerovo crash"),
    ("London", "hands US Army spy suspect to US"),
    ("Australia", "sanctions settler leader Weiss"),
    ("Mozambique", "Mondlane on trial"),
    ("Conakry", "224 jailed over gold mining"),
    ("Port Louis", "UK given Chagos deadline"),
    ("Pretoria", "Nigeria's new envoy reprimanded"),
    ("Kinshasa", "WHO keeps Ebola emergency"),
    ("Caracas", "unions call 24-hour strike"),
    ("Bras\u00edlia", "Senate passes $10bn package"),
    ("Tumbes", "river passes red alert in Peru"),
    ("Paris", "Diallo to challenge Infantino"),
    ("London", "Lammy urges Burnham to back EU"),
    ("Berlin", "coalition agrees a power-tax cut"),
    ("Zaporizhzhia", "85 children ordered out"),
    ("Football", "Chelsea women beat PSG 1\u20130"),
    ("Beirut", "US adds sanctions on Hezbollah"),
    ("Baghdad", "six French jailed over ISIL"),
    ("Kuwait", "magnitude 4.1 quake"),
    ("Kashmir", "forces kill militant chief"),
    ("Bangladesh", "MP's clinic bombed"),
    ("Seoul", "Kospi jumps 2% as chip shares rally"),
    ("Dakar", "migrant boat capsizes, one dead"),
    ("Port-au-Prince", "gang chief's house razed"),
    ("Pew", "Islam set to be largest faith"),
    ("Hormuz", "Iran says it downed a US MQ-9"),
    ("The Hague", "ICJ sets Rohingya ruling"),
    ("Port Moresby", "magnitude 6.0 quake"),
]

NUMBERS = ("141 drones fired  \u2022  126 downed  \u2022  25.9bn km Voyager 1  "
           "\u2022  55 factories shut  \u2022  251\u201311 Jeffries vote  \u2022  "
           "$81.3bn Anthropic IPO  \u2022  2,230 Sudan civilians killed in 2026")

DATE_CHECK = ("Left out on purpose, because they were first reported before "
              "Wednesday: the Kerch Bridge span collapse \u00b7 Nvidia's $115.8bn "
              "quarter \u00b7 Peltola's Alaska win \u00b7 Mongolia's president resigning "
              "\u00b7 the Prague train crash \u00b7 the Knesset speaker vote \u00b7 the US "
              "strike on Qeshm \u00b7 COP31's first draft (Mon 16). Not yet: the "
              "Trump\u2013Xi\u2013Putin summit (Thu 19) \u00b7 Anthropic's first trade "
              "(Thu 19) \u00b7 GTA VI's US release (Thu 19) \u00b7 Akvan's landfall (Fri 20).")

SOURCES = ("Reuters \u00b7 AP \u00b7 AFP \u00b7 BBC \u00b7 Al Jazeera \u00b7 CNBC \u00b7 "
           "NASA \u00b7 ONS \u00b7 IMD \u00b7 ATP \u00b7 Bloomberg. Original drawings.")


# ------------------------------------------------------- illustrations
# Every illustration is drawn here from PIL primitives: flat-vector scenes,
# no photos, no copied artwork. Each takes the box (x, y, w, h).

def _sky(d, x, y, w, h, c):
    d.rectangle([x, y, x + w, y + h], fill=c)


def art_gulf(d, x, y, w, h):
    _sky(d, x, y, w, h, (174, 205, 226))
    d.polygon([(x + w * 0.55, y), (x + w, y), (x + w, y + h * 0.55),
               (x + w * 0.75, y + h * 0.45)], fill=(232, 214, 170))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(110, 160, 195))
    d.polygon([(x, y + h * 0.62), (x + w * 0.45, y + h * 0.62),
               (x + w * 0.38, y + h), (x, y + h)], fill=(210, 190, 150))
    # drone paths: dotted red arcs with small drone silhouettes
    for i in range(6):
        px = x + w * (0.15 + 0.13 * i)
        py = y + h * (0.28 + 0.06 * ((i * 7) % 3))
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(163, 22, 33))
    d.line([(x + w * 0.12, y + h * 0.30), (x + w * 0.85, y + h * 0.55)],
           fill=(163, 22, 33), width=2)
    d.polygon([(x + w * 0.30, y + h * 0.18), (x + w * 0.34, y + h * 0.24),
               (x + w * 0.30, y + h * 0.30), (x + w * 0.26, y + h * 0.24)],
              fill=(40, 40, 40))
    d.polygon([(x + w * 0.62, y + h * 0.42), (x + w * 0.66, y + h * 0.48),
               (x + w * 0.62, y + h * 0.54), (x + w * 0.58, y + h * 0.48)],
              fill=(40, 40, 40))
    # base marker
    bx, by = x + w * 0.72, y + h * 0.78
    d.polygon([(bx, by - 7), (bx + 2, by - 2), (bx + 7, by - 2), (bx + 3, by + 2),
               (bx + 5, by + 7), (bx, by + 4), (bx - 5, by + 7), (bx - 3, by + 2),
               (bx - 7, by - 2), (bx - 2, by - 2)], fill=(255, 255, 255))


def art_apec(d, x, y, w, h):
    _sky(d, x, y, w, h, (198, 220, 240))
    for i, bh in enumerate([0.42, 0.55, 0.35, 0.62, 0.48]):
        bx = x + w * (0.05 + i * 0.19)
        d.rectangle([bx, y + h * (0.85 - bh), bx + w * 0.15, y + h * 0.85],
                    fill=(120, 130, 145))
    d.polygon([(x, y + h), (x + w, y + h), (x + w * 0.72, y + h * 0.62),
               (x + w * 0.28, y + h * 0.62)], fill=(163, 22, 33))
    # plane: fuselage, windows, tail
    d.ellipse([x + w * 0.18, y + h * 0.30, x + w * 0.82, y + h * 0.52],
              fill=(245, 245, 245))
    d.polygon([(x + w * 0.74, y + h * 0.32), (x + w * 0.86, y + h * 0.16),
               (x + w * 0.86, y + h * 0.34)], fill=(200, 60, 60))
    for i in range(6):
        d.ellipse([x + w * (0.26 + i * 0.08), y + h * 0.38,
                   x + w * (0.29 + i * 0.08), y + h * 0.44], fill=(40, 80, 130))
    # flags on poles
    for fx, fc in [(0.10, (222, 40, 40)), (0.86, (60, 90, 170))]:
        d.line([(x + w * fx, y + h * 0.55), (x + w * fx, y + h * 0.85)],
               fill=(60, 60, 60), width=2)
        d.rectangle([x + w * fx, y + h * 0.55, x + w * (fx + 0.10), y + h * 0.66],
                    fill=fc)


def art_odesa(d, x, y, w, h):
    _sky(d, x, y, w, h, (18, 26, 46))
    for i in range(14):
        d.ellipse([x + w * ((i * 0.37) % 1.0), y + h * ((i * 0.53) % 0.35),
                   x + w * ((i * 0.37) % 1.0) + 2, y + h * ((i * 0.53) % 0.35) + 2],
                  fill=(255, 255, 255))
    for i, bh in enumerate([0.35, 0.5, 0.42, 0.58, 0.38]):
        bx = x + w * (0.03 + i * 0.19)
        d.rectangle([bx, y + h * (0.92 - bh), bx + w * 0.16, y + h * 0.92],
                    fill=(38, 44, 66))
        for wy in range(3):
            d.rectangle([bx + 4, y + h * (0.88 - bh) + wy * 10,
                         bx + 9, y + h * (0.88 - bh) + wy * 10 + 5],
                        fill=(250, 200, 90))
    # explosion bursts
    for ex, ey, r in [(0.30, 0.30, 14), (0.68, 0.22, 18)]:
        cx, cy = x + w * ex, y + h * ey
        for k in range(8):
            import math
            a = math.pi * k / 4
            d.line([(cx, cy), (cx + r * math.cos(a), cy + r * math.sin(a))],
                   fill=(250, 160, 40), width=3)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 220, 120))
    # EU panel
    d.rectangle([x + w * 0.62, y + h * 0.56, x + w * 0.97, y + h * 0.84],
                fill=(30, 60, 140))
    d.text((x + w * 0.66, y + h * 0.59), "\u20ac45bn", font=SANS_B(20),
           fill=(255, 255, 255))


def art_voyager(d, x, y, w, h):
    _sky(d, x, y, w, h, (8, 10, 20))
    for i in range(22):
        sx = x + w * ((i * 0.41 + 0.07) % 1.0)
        sy = y + h * ((i * 0.29 + 0.11) % 1.0)
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
    # Earth, bottom left
    d.ellipse([x + w * 0.04, y + h * 0.68, x + w * 0.24, y + h * 0.98],
              fill=(50, 110, 200))
    d.ellipse([x + w * 0.09, y + h * 0.74, x + w * 0.17, y + h * 0.84],
              fill=(70, 170, 90))
    # probe: gold body, dish, boom
    px, py = x + w * 0.62, y + h * 0.34
    d.rectangle([px, py, px + w * 0.16, py + h * 0.16], fill=(220, 180, 60))
    d.line([(px + w * 0.08, py), (px + w * 0.20, py - h * 0.18)],
           fill=(220, 220, 220), width=2)
    d.ellipse([px + w * 0.16, py - h * 0.22, px + w * 0.26, py - h * 0.10],
              outline=(220, 220, 220), width=2)
    d.line([(px + w * 0.16, py + h * 0.08), (px + w * 0.34, py + h * 0.14)],
           fill=(200, 200, 200), width=2)
    # dotted signal arc back to Earth
    for i in range(8):
        t = i / 7
        sx = x + w * (0.62 - 0.38 * t)
        sy = y + h * (0.34 + 0.42 * t * t)
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(250, 200, 90))


def art_gaza(d, x, y, w, h):
    _sky(d, x, y, w, h, (226, 208, 170))
    for i, bh in enumerate([0.30, 0.42, 0.34]):
        bx = x + w * (0.05 + i * 0.30)
        d.rectangle([bx, y + h * (0.72 - bh), bx + w * 0.24, y + h * 0.72],
                    fill=(150, 140, 125))
    d.line([(x, y + h * 0.72), (x + w, y + h * 0.72)], fill=(220, 180, 40), width=4)
    # tanks
    for tx in (0.12, 0.55):
        bx = x + w * tx
        d.rectangle([bx, y + h * 0.74, bx + w * 0.30, y + h * 0.88],
                    fill=(74, 92, 62))
        d.rectangle([bx + w * 0.08, y + h * 0.66, bx + w * 0.20, y + h * 0.75],
                    fill=(60, 78, 52))
        d.line([(bx + w * 0.20, y + h * 0.70), (bx + w * 0.33, y + h * 0.68)],
               fill=(60, 78, 52), width=3)


def art_horn(d, x, y, w, h):
    _sky(d, x, y, w, h, (238, 232, 210))
    d.polygon([(x + w * 0.62, y + h * 0.10), (x + w * 0.95, y + h * 0.30),
               (x + w * 0.88, y + h * 0.75), (x + w * 0.55, y + h * 0.90),
               (x + w * 0.45, y + h * 0.55), (x + w * 0.52, y + h * 0.22)],
              fill=(214, 186, 138))
    d.polygon([(x + w * 0.60, y + h * 0.55), (x + w * 0.98, y + h * 0.60),
               (x + w * 0.98, y + h), (x + w * 0.60, y + h)],
              fill=(120, 165, 195))
    d.line([(x + w * 0.15, y + h * 0.30), (x + w * 0.55, y + h * 0.42)],
           fill=(163, 22, 33), width=3)
    d.polygon([(x + w * 0.55, y + h * 0.42), (x + w * 0.47, y + h * 0.38),
               (x + w * 0.47, y + h * 0.47)], fill=(163, 22, 33))
    d.line([(x + w * 0.18, y + h * 0.68), (x + w * 0.55, y + h * 0.60)],
           fill=(163, 22, 33), width=3)
    d.polygon([(x + w * 0.55, y + h * 0.60), (x + w * 0.47, y + h * 0.56),
               (x + w * 0.47, y + h * 0.65)], fill=(163, 22, 33))
    for i in range(5):
        d.ellipse([x + w * (0.10 + i * 0.06), y + h * (0.22 + (i % 2) * 0.08),
                   x + w * (0.13 + i * 0.06), y + h * (0.25 + (i % 2) * 0.08)],
                  fill=(60, 60, 60))


def art_fed(d, x, y, w, h):
    _sky(d, x, y, w, h, (248, 244, 236))
    d.line([(x + w * 0.08, y + h * 0.12), (x + w * 0.08, y + h * 0.88)],
           fill=(120, 120, 120), width=2)
    d.line([(x + w * 0.08, y + h * 0.88), (x + w * 0.95, y + h * 0.88)],
           fill=(120, 120, 120), width=2)
    pts = [(0.12, 0.30), (0.28, 0.38), (0.44, 0.34), (0.60, 0.48),
           (0.76, 0.44), (0.92, 0.72)]
    for (a, b), (c, e) in zip(pts, pts[1:]):
        d.line([(x + w * a, y + h * b), (x + w * c, y + h * e)],
               fill=(163, 22, 33), width=3)
    for a, b in pts:
        d.ellipse([x + w * a - 3, y + h * b - 3, x + w * a + 3, y + h * b + 3],
                  fill=(163, 22, 33))
    d.polygon([(x + w * 0.92, y + h * 0.72), (x + w * 0.86, y + h * 0.66),
               (x + w * 0.86, y + h * 0.78)], fill=(163, 22, 33))
    d.text((x + w * 0.10, y + h * 0.06), "DOW \u2212561", font=SANS_B(15),
           fill=(163, 22, 33))


def art_dhaka(d, x, y, w, h):
    _sky(d, x, y, w, h, (205, 225, 235))
    d.rectangle([x + w * 0.05, y + h * 0.30, x + w * 0.60, y + h * 0.72],
                fill=(150, 150, 150))
    for i in range(3):
        d.polygon([(x + w * (0.08 + i * 0.18), y + h * 0.30),
                   (x + w * (0.17 + i * 0.18), y + h * 0.30),
                   (x + w * (0.13 + i * 0.18), y + h * 0.16)],
                  fill=(120, 120, 120))
    d.rectangle([x + w * 0.66, y + h * 0.22, x + w * 0.72, y + h * 0.72],
                fill=(130, 130, 130))
    d.rectangle([x, y + h * 0.72, x + w, y + h * 0.80], fill=(90, 85, 80))
    # crowd: heads and shoulders
    for i in range(9):
        cx = x + w * (0.06 + i * 0.10)
        d.ellipse([cx, y + h * 0.80, cx + w * 0.06, y + h * 0.88],
                  fill=(240, 200, 160))
        d.rectangle([cx - 2, y + h * 0.88, cx + w * 0.06 + 2, y + h * 0.98],
                    fill=[(200, 60, 60), (60, 90, 170), (220, 160, 40)][i % 3])
    d.rectangle([x + w * 0.78, y + h * 0.30, x + w * 0.95, y + h * 0.72],
                fill=(240, 240, 240))
    d.text((x + w * 0.80, y + h * 0.42), "55", font=SANS_B(20), fill=(163, 22, 33))


def art_caracas(d, x, y, w, h):
    _sky(d, x, y, w, h, (200, 222, 240))
    for i in range(4):
        bx = x + w * (0.05 + i * 0.24)
        d.rectangle([bx, y + h * (0.80 - 0.12 * (i % 3)), bx + w * 0.20, y + h * 0.80],
                    fill=(140, 145, 155))
    # two flags
    d.line([(x + w * 0.30, y + h * 0.12), (x + w * 0.30, y + h * 0.55)],
           fill=(60, 60, 60), width=2)
    for i in range(3):
        d.rectangle([x + w * 0.30, y + h * (0.12 + i * 0.07),
                     x + w * 0.48, y + h * (0.19 + i * 0.07)],
                    fill=[(176, 42, 42), (255, 255, 255), (47, 93, 168)][i])
    d.line([(x + w * 0.68, y + h * 0.12), (x + w * 0.68, y + h * 0.55)],
           fill=(60, 60, 60), width=2)
    for i, c in enumerate([(250, 200, 40), (40, 90, 180), (200, 40, 40)]):
        d.rectangle([x + w * 0.68, y + h * (0.12 + i * 0.07),
                     x + w * 0.86, y + h * (0.19 + i * 0.07)], fill=c)
    # green check shield
    d.polygon([(x + w * 0.44, y + h * 0.58), (x + w * 0.56, y + h * 0.58),
               (x + w * 0.56, y + h * 0.78), (x + w * 0.50, y + h * 0.88),
               (x + w * 0.44, y + h * 0.78)], fill=(46, 139, 74))
    d.line([(x + w * 0.46, y + h * 0.72), (x + w * 0.49, y + h * 0.76),
            (x + w * 0.55, y + h * 0.66)], fill=(255, 255, 255), width=3)


def art_cop31(d, x, y, w, h):
    _sky(d, x, y, w, h, (198, 222, 238))
    d.ellipse([x + w * 0.72, y + h * 0.06, x + w * 0.92, y + h * 0.26],
              fill=(250, 180, 60))
    # globe
    d.ellipse([x + w * 0.08, y + h * 0.18, x + w * 0.48, y + h * 0.82],
              fill=(70, 130, 200))
    d.ellipse([x + w * 0.14, y + h * 0.28, x + w * 0.28, y + h * 0.44],
              fill=(90, 170, 90))
    d.ellipse([x + w * 0.30, y + h * 0.52, x + w * 0.42, y + h * 0.70],
              fill=(90, 170, 90))
    # draft paper
    d.rectangle([x + w * 0.55, y + h * 0.42, x + w * 0.95, y + h * 0.92],
                fill=(255, 255, 255))
    for i in range(4):
        d.line([(x + w * 0.60, y + h * (0.52 + i * 0.10)),
                (x + w * 0.90, y + h * (0.52 + i * 0.10))],
               fill=(120, 120, 120), width=2)
    d.line([(x + w * 0.60, y + h * 0.52), (x + w * 0.90, y + h * 0.82)],
           fill=(163, 22, 33), width=3)


def art_jeffries(d, x, y, w, h):
    _sky(d, x, y, w, h, (240, 236, 226))
    # capitol dome
    d.rectangle([x + w * 0.10, y + h * 0.55, x + w * 0.90, y + h * 0.90],
                fill=(245, 245, 240))
    d.pieslice([x + w * 0.32, y + h * 0.18, x + w * 0.68, y + h * 0.58],
               180, 360, fill=(245, 245, 240))
    for i in range(5):
        d.line([(x + w * (0.18 + i * 0.16), y + h * 0.60),
                (x + w * (0.18 + i * 0.16), y + h * 0.88)],
               fill=(200, 200, 190), width=2)
    d.rectangle([x + w * 0.48, y + h * 0.08, x + w * 0.52, y + h * 0.20],
                fill=(200, 200, 190))
    # ballot box
    d.rectangle([x + w * 0.68, y + h * 0.56, x + w * 0.94, y + h * 0.84],
                fill=(27, 42, 74))
    d.text((x + w * 0.70, y + h * 0.60), "251\u201311", font=SANS_B(13),
           fill=(255, 255, 255))


def art_anthropic(d, x, y, w, h):
    _sky(d, x, y, w, h, (248, 244, 236))
    d.line([(x + w * 0.08, y + h * 0.12), (x + w * 0.08, y + h * 0.88)],
           fill=(120, 120, 120), width=2)
    d.line([(x + w * 0.08, y + h * 0.88), (x + w * 0.95, y + h * 0.88)],
           fill=(120, 120, 120), width=2)
    for i, bh in enumerate([0.22, 0.34, 0.30, 0.48, 0.66]):
        bx = x + w * (0.14 + i * 0.17)
        d.rectangle([bx, y + h * (0.88 - bh), bx + w * 0.12, y + h * 0.88],
                    fill=(220, 120, 40))
    d.text((x + w * 0.12, y + h * 0.06), "$83", font=SANS_B(18),
           fill=(163, 22, 33))


def art_akvan(d, x, y, w, h):
    _sky(d, x, y, w, h, (120, 165, 195))
    d.polygon([(x, y + h), (x + w * 0.45, y + h), (x + w * 0.35, y),
               (x, y + h * 0.30)], fill=(90, 150, 90))
    # cyclone spiral: concentric arcs
    cx, cy = x + w * 0.68, y + h * 0.45
    for r in (34, 26, 18, 10):
        d.arc([cx - r, cy - r * 0.8, cx + r, cy + r * 0.8], 20, 300,
              fill=(255, 255, 255), width=4)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 255, 255))
    # rain streaks
    for i in range(5):
        rx = x + w * (0.10 + i * 0.07)
        d.line([(rx, y + h * 0.12), (rx - 4, y + h * 0.26)], fill=(220, 235, 245),
               width=2)


def art_gta(d, x, y, w, h):
    _sky(d, x, y, w, h, (38, 28, 58))
    d.ellipse([x + w * 0.70, y + h * 0.08, x + w * 0.90, y + h * 0.32],
              fill=(240, 230, 200))
    d.ellipse([x + w * 0.74, y + h * 0.12, x + w * 0.80, y + h * 0.20],
              fill=(210, 200, 170))
    # controller
    d.rounded_rectangle([x + w * 0.10, y + h * 0.45, x + w * 0.90, y + h * 0.90],
                        radius=14, fill=(24, 18, 40))
    d.ellipse([x + w * 0.16, y + h * 0.58, x + w * 0.30, y + h * 0.76],
              fill=(60, 60, 80))
    d.ellipse([x + w * 0.70, y + h * 0.58, x + w * 0.84, y + h * 0.76],
              fill=(60, 60, 80))
    for i, c in enumerate([(220, 60, 60), (60, 180, 80), (60, 120, 220),
                           (230, 200, 60)]):
        bx = x + w * (0.40 + (i % 2) * 0.10)
        by = y + h * (0.55 + (i // 2) * 0.10)
        d.ellipse([bx, by, bx + 9, by + 9], fill=c)


def art_aria(d, x, y, w, h):
    _sky(d, x, y, w, h, (28, 18, 42))
    d.polygon([(x + w * 0.10, y), (x + w * 0.30, y), (x + w * 0.45, y + h * 0.55),
               (x + w * 0.05, y + h * 0.55)], fill=(90, 70, 140))
    d.polygon([(x + w * 0.70, y), (x + w * 0.90, y), (x + w * 0.95, y + h * 0.55),
               (x + w * 0.55, y + h * 0.55)], fill=(90, 70, 140))
    # trophy
    tx = x + w * 0.50
    d.polygon([(tx - w * 0.13, y + h * 0.28), (tx + w * 0.13, y + h * 0.28),
               (tx + w * 0.08, y + h * 0.52), (tx - w * 0.08, y + h * 0.52)],
              fill=(230, 180, 60))
    d.rectangle([tx - w * 0.05, y + h * 0.52, tx + w * 0.05, y + h * 0.66],
                fill=(200, 150, 40))
    d.rectangle([tx - w * 0.10, y + h * 0.66, tx + w * 0.10, y + h * 0.74],
                fill=(200, 150, 40))
    d.arc([tx - w * 0.20, y + h * 0.28, tx - w * 0.06, y + h * 0.44], 90, 270,
          fill=(230, 180, 60), width=4)
    d.arc([tx + w * 0.06, y + h * 0.28, tx + w * 0.20, y + h * 0.44], 270, 90,
          fill=(230, 180, 60), width=4)
    d.text((x + w * 0.78, y + h * 0.60), "7", font=SANS_B(26),
           fill=(230, 180, 60))


def art_tennis(d, x, y, w, h):
    _sky(d, x, y, w, h, (60, 140, 70))
    d.rectangle([x + w * 0.08, y + h * 0.14, x + w * 0.92, y + h * 0.86],
                fill=(50, 110, 200))
    d.rectangle([x + w * 0.08, y + h * 0.14, x + w * 0.92, y + h * 0.86],
                outline=(255, 255, 255), width=2)
    d.line([(x + w * 0.08, y + h * 0.50), (x + w * 0.92, y + h * 0.50)],
           fill=(255, 255, 255), width=3)
    d.line([(x + w * 0.50, y + h * 0.14), (x + w * 0.50, y + h * 0.86)],
           fill=(255, 255, 255), width=2)
    d.ellipse([x + w * 0.68, y + h * 0.20, x + w * 0.76, y + h * 0.32],
              fill=(220, 230, 60))


ARTS = [art_gulf, art_apec, art_odesa, art_voyager, art_gaza, art_horn,
        art_fed, art_dhaka, art_caracas, art_cop31, art_jeffries,
        art_anthropic, art_akvan, art_gta, art_aria, art_tennis]

# story number -> (lon, lat, region) for map pins
PINS = [
    (1, 48.5, 28.5, "MIDDLE EAST"), (2, 114.0, 22.5, "ASIA"),
    (3, 30.7, 46.5, "EUROPE"), (5, 34.5, 31.4, "MIDDLE EAST"),
    (6, 40.0, 12.0, "AFRICA"), (7, -74.0, 40.7, "AMERICAS"),
    (8, 90.4, 23.8, "ASIA"), (9, -66.9, 10.5, "AMERICAS"),
    (10, 30.7, 36.9, "EUROPE"), (11, -77.0, 38.9, "AMERICAS"),
    (12, -122.4, 37.8, "AMERICAS"), (13, 85.8, 20.2, "ASIA"),
    (14, 174.8, -41.3, "OCEANIA"), (15, 151.2, -33.9, "OCEANIA"),
    (16, 7.7, 45.1, "EUROPE"),
]

NA = [(-168, 66), (-150, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
      (-80, 62), (-75, 58), (-68, 58), (-60, 52), (-55, 47), (-60, 44),
      (-65, 42), (-70, 40), (-74, 35), (-76, 32), (-80, 26), (-84, 30),
      (-90, 21), (-94, 17), (-97, 16), (-102, 18), (-105, 21), (-110, 24),
      (-115, 29), (-120, 34), (-124, 42), (-124, 48), (-130, 55), (-140, 60),
      (-150, 61), (-158, 58), (-165, 60), (-168, 66)]
SA = [(-78, 8), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18),
      (-70, -23), (-70, -30), (-71, -35), (-73, -42), (-74, -50), (-70, -54),
      (-66, -55), (-68, -50), (-70, -45), (-72, -38), (-73, -30), (-70, -22),
      (-60, -25), (-50, -28), (-42, -23), (-38, -15), (-35, -8), (-38, -5),
      (-44, -3), (-50, 0), (-55, 4), (-60, 7), (-65, 10), (-70, 11), (-75, 10)]
EU = [(-10, 36), (-9, 43), (-2, 44), (-1, 46), (2, 48), (4, 52), (7, 54),
      (8, 57), (10, 59), (13, 58), (18, 56), (21, 55), (24, 58), (21, 60),
      (18, 62), (14, 64), (12, 66), (18, 69), (25, 71), (30, 70), (28, 66),
      (24, 62), (20, 60), (23, 58), (28, 56), (30, 54), (28, 50), (24, 48),
      (20, 46), (16, 44), (12, 44), (8, 44), (3, 42), (0, 40), (-2, 37),
      (-6, 36), (-9, 37)]
AF = [(-17, 15), (-16, 21), (-13, 27), (-10, 31), (-6, 33), (0, 36), (5, 37),
      (10, 37), (15, 32), (20, 32), (25, 32), (30, 31), (33, 28), (35, 23),
      (38, 18), (42, 12), (46, 11), (51, 12), (51, 10), (48, 5), (44, 0),
      (40, -5), (38, -12), (35, -18), (32, -25), (28, -32), (25, -34),
      (20, -35), (16, -33), (14, -28), (12, -18), (12, -10), (10, -2),
      (8, 4), (4, 6), (0, 5), (-4, 5), (-8, 4), (-13, 8), (-16, 11)]
AS = [(30, 70), (45, 70), (60, 72), (75, 73), (90, 75), (110, 76), (130, 74),
      (150, 72), (165, 70), (175, 67), (178, 65), (170, 62), (162, 60),
      (155, 58), (150, 52), (145, 48), (140, 42), (137, 38), (132, 35),
      (128, 32), (126, 28), (124, 22), (120, 18), (116, 14), (112, 10),
      (108, 8), (105, 5), (102, 8), (100, 12), (98, 16), (95, 18), (92, 21),
      (90, 22), (88, 20), (86, 18), (84, 14), (82, 10), (80, 7), (77, 8),
      (75, 12), (72, 20), (70, 24), (66, 25), (62, 25), (58, 26), (55, 27),
      (52, 28), (50, 30), (48, 32), (46, 35), (44, 38), (42, 40), (40, 42),
      (38, 44), (36, 42), (34, 40), (32, 38), (30, 36), (28, 38), (30, 42),
      (32, 46), (32, 52), (30, 58), (28, 64), (28, 70)]
AU = [(113, -22), (120, -15), (130, -12), (140, -15), (150, -20), (153, -28),
      (150, -37), (140, -38), (130, -32), (120, -35), (114, -30), (113, -22)]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(215, 228, 235))
    d.rectangle([x, y, x + w, y + h], outline=(150, 160, 170), width=1)

    def conv(lon, lat):
        return (x + (lon + 170) / 360 * w, y + (75 - lat) / 135 * h)

    for poly in (NA, SA, EU, AF, AS, AU):
        d.polygon([conv(lo, la) for lo, la in poly], fill=(172, 190, 158),
                  outline=(120, 140, 115))
    # deep-space inset for story 4 (Voyager 1)
    ix, iy, iw, ih = x + w - 34, y + 6, 28, 28
    d.rectangle([ix, iy, ix + iw, iy + ih], fill=(8, 10, 20))
    d.ellipse([ix + 9, iy + 9, ix + 19, iy + 19], fill=(220, 180, 60))
    d.text((ix + 10, iy + 20), "4", font=SANS_B(9), fill=(255, 255, 255))
    for num, lon, lat, region in PINS:
        px, py = conv(lon, lat)
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=COL[region],
                  outline=(255, 255, 255), width=1)
        tf = SANS_B(9)
        t = str(num)
        d.text((px - d.textlength(t, font=tf) / 2, py - 6), t, font=tf,
               fill=(255, 255, 255))


# ------------------------------------------------------------------ layout
def draw():
    assert len(LEADS) == 4 and len(STORIES) == 12 and len(BRIEFS) == 36
    assert sum(c for _, c in REGIONS) == 52, sum(c for _, c in REGIONS)
    assert sum(c for _, c in FIELDS) == 52, sum(c for _, c in FIELDS)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- kicker --------------------------------------------------------
    d.text((M, 8), "THE DAILY GLOBE", font=SERIF_B(14), fill=NAVY)
    kr = "52 STORIES  \u2022  7 REGIONS  \u2022  9 FIELDS  \u2022  16 DRAWN"
    d.text((W - M - d.textlength(kr, font=SANS_B(11)), 10), kr,
           font=SANS_B(11), fill=RED)
    d.line([(M, 26), (W - M, 26)], fill=RULE, width=2)

    # --- masthead: the date is the headline -----------------------------
    date = "Wednesday 18 November 2026"
    df = SERIF_B(52)
    d.text(((W - d.textlength(date, font=df)) / 2, 30), date, font=df, fill=INK)
    sub = "Everything on this page happened, or was first reported, on Wednesday 18 November 2026."
    sf = SERIF_I(13)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 92), sub, font=sf, fill=GREY)
    d.line([(M, 112), (W - M, 112)], fill=RULE, width=3)

    # --- region strip ----------------------------------------------------
    seg_w = CW / len(REGIONS)
    y = 116
    for i, (name, cnt) in enumerate(REGIONS):
        x0 = M + i * seg_w
        d.rectangle([x0, y, x0 + seg_w - 1, y + 19], fill=COL[name])
        t = f"{name} {cnt}"
        tf = SANS_B(11)
        d.text((x0 + (seg_w - d.textlength(t, font=tf)) / 2, y + 4), t,
               font=tf, fill=(255, 255, 255))

    # --- field strip -------------------------------------------------------
    y = 139
    fields = "BY FIELD \u2014 " + "  \u00b7  ".join(f"{n} {c}" for n, c in FIELDS)
    ff = SANS(10)
    d.text(((W - d.textlength(fields, font=ff)) / 2, y), fields, font=ff,
           fill=(50, 48, 44))

    # --- the day in UTC ----------------------------------------------------
    y = 157
    lab = "THE DAY IN UTC"
    lf = SANS_B(10)
    lw = d.textlength(lab, font=lf) + 12
    d.rectangle([M, y, M + lw, y + 27], fill=RED)
    d.text((M + 6, y + 8), lab, font=lf, fill=(255, 255, 255))
    tx = M + lw + 10
    for row, items in enumerate((TIMELINE[:4], TIMELINE[4:])):
        parts = []
        for t, s in items:
            parts.append((t, s))
        line = "   \u00b7   ".join(f"{t}: {s}" for t, s in parts)
        d.text((tx, y + 1 + row * 14), line, font=SANS(10), fill=INK)
    d.line([(M, 188), (W - M, 188)], fill=RULE, width=1)

    # --- four leads ---------------------------------------------------------
    lead_w, lead_gap, lead_ill = 235, 12, 100
    y0 = 194
    for i, (region, topic, tag, head, body) in enumerate(LEADS):
        x = M + i * (lead_w + lead_gap)
        ARTS[i](d, x, y0, lead_w, lead_ill)
        # proof tag as a strip at the foot of the illustration
        d.rectangle([x, y0 + lead_ill - 13, x + lead_w, y0 + lead_ill],
                    fill=NAVY)
        d.text((x + 4, y0 + lead_ill - 11), tag, font=SANS_B(8),
               fill=(255, 255, 255))
        yy = y0 + lead_ill + 5
        kick = f"{i + 1}  {region} \u00b7 {topic}"
        d.text((x, yy), kick, font=SANS_B(10), fill=COL[region])
        yy += 13
        hlines = wrap(d, head, SERIF_B(19), lead_w)
        yy = draw_lines(d, hlines, x, yy, SERIF_B(19), INK, 22,
                        max_lines=2, label=f"lead {i + 1} headline")
        yy += 2
        blines = wrap(d, body, SANS(10), lead_w)
        draw_lines(d, blines, x, yy, SANS(10), (50, 48, 44), 13,
                   max_lines=3, label=f"lead {i + 1} blurb")
        if i < 3:
            d.line([(x + lead_w + lead_gap // 2, y0),
                    (x + lead_w + lead_gap // 2, y0 + lead_ill + 108)],
                   fill=FAINT, width=1)
    d.line([(M, 410), (W - M, 410)], fill=RULE, width=2)

    # --- stories 5..16: two rows of six -------------------------------------
    st_w, st_gap, st_ill = 154, 10, 72
    for row in range(2):
        y0 = 418 + row * 164
        for c in range(6):
            i = row * 6 + c
            region, topic, tag, head, body = STORIES[i]
            x = M + c * (st_w + st_gap)
            ARTS[4 + i](d, x, y0, st_w, st_ill)
            d.rectangle([x, y0 + st_ill - 12, x + st_w, y0 + st_ill],
                        fill=NAVY)
            d.text((x + 3, y0 + st_ill - 10), tag, font=SANS_B(7),
                   fill=(255, 255, 255))
            yy = y0 + st_ill + 4
            kick = f"{5 + i}  {region} \u00b7 {topic}"
            d.text((x, yy), kick, font=SANS_B(9), fill=COL[region])
            yy += 12
            hlines = wrap(d, head, SERIF_B(13), st_w)
            yy = draw_lines(d, hlines, x, yy, SERIF_B(13), INK, 16,
                            max_lines=3, label=f"story {5 + i} headline")
            yy += 1
            blines = wrap(d, body, SANS(10), st_w)
            draw_lines(d, blines, x, yy, SANS(10), (50, 48, 44), 12,
                       max_lines=2, label=f"story {5 + i} blurb")
    d.line([(M, 744), (W - M, 744)], fill=RULE, width=2)

    # --- the day in numbers ---------------------------------------------------
    y = 750
    nums = "THE DAY IN NUMBERS:  " + NUMBERS
    nf = SANS_B(11)
    nw = d.textlength(nums, font=nf)
    if nw > CW:
        raise SystemExit(f"OVERFLOW numbers strip: {nw:.0f}px > {CW}px")
    d.text((M, y), nums, font=nf, fill=NAVY)

    # --- map + also on wednesday ----------------------------------------------
    y0 = 772
    d.text((M, y0), "WHERE IT HAPPENED", font=SANS_B(12), fill=INK)
    d.text((M + 316, y0), "ALSO ON WEDNESDAY 18 NOVEMBER", font=SANS_B(12),
           fill=INK)
    draw_map(d, M, y0 + 16, 300, 132)
    ly = y0 + 152
    d.text((M, ly), "Pins mark stories 1\u201316; the black square is 4, Voyager 1, in deep space.",
           font=SANS(9), fill=GREY)
    lx = M
    d.text((lx, ly + 12), "Pin colours:", font=SANS(9), fill=GREY)
    lx += d.textlength("Pin colours: ", font=SANS(9))
    for name in ("EUROPE", "MIDDLE EAST", "ASIA", "AFRICA"):
        d.ellipse([lx, ly + 14, lx + 7, ly + 21], fill=COL[name])
        lx += 10
        d.text((lx, ly + 12), name, font=SANS(9), fill=GREY)
        lx += d.textlength(name, font=SANS(9)) + 12
    lx = M
    for name in ("AMERICAS", "OCEANIA"):
        d.ellipse([lx, ly + 26, lx + 7, ly + 33], fill=COL[name])
        lx += 10
        d.text((lx, ly + 24), name, font=SANS(9), fill=GREY)
        lx += d.textlength(name, font=SANS(9)) + 12
    # briefs: 3 columns x 12 rows
    bw, bgap = 212, 12
    for col in range(3):
        bx = M + 316 + col * (bw + bgap)
        for r in range(12):
            i = col * 12 + r
            place, fact = BRIEFS[i]
            yy = y0 + 16 + r * 14
            d.text((bx, yy), f"{17 + i}", font=SANS_B(9), fill=RED)
            t = f"{place}: {fact}"
            tw = d.textlength(t, font=SANS(9))
            if tw > bw - 22:
                raise SystemExit(f"OVERFLOW brief {17 + i}: {t!r} ({tw:.0f}px)")
            d.text((bx + 22, yy), t, font=SANS(9), fill=INK)

    # --- how sure ------------------------------------------------------------
    y = 960
    hs = ("HOW SURE \u2014 CONFIRMED: on the record  \u00b7  CLAIM: one side's account  "
          "\u00b7  SOURCES: monitors or unnamed sources, via a news agency  \u00b7  "
          "FORECAST: an official prediction")
    d.text((M, y), hs, font=SANS(9), fill=GREY)

    # --- date check ------------------------------------------------------------
    y = 974
    d.rectangle([M, y, W - M, y + 30], outline=RED, width=2)
    dc = "DATE CHECK  \u2014  " + DATE_CHECK
    dlines = wrap(d, "DATE CHECK \u2014 " + DATE_CHECK, SANS(9), CW - 12)
    yy = y + 3
    for line in dlines[:2]:
        d.text((M + 6, yy), line, font=SANS(9), fill=INK)
        yy += 12
    if len(dlines) > 2:
        raise SystemExit(f"OVERFLOW date check: {len(dlines)} lines")

    # --- footer ------------------------------------------------------------------
    y = 1010
    foot = "Every story here happened, or was first reported, on Wednesday 18 November 2026.  Sources: " + SOURCES
    ff2 = SERIF_I(10)
    fw = d.textlength(foot, font=ff2)
    if fw > CW:
        raise SystemExit(f"OVERFLOW footer: {fw:.0f}px > {CW}px")
    d.text(((W - fw) / 2, y), foot, font=ff2, fill=GREY)
    if y + 12 > H:
        raise SystemExit("OVERFLOW page height")

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    draw()
