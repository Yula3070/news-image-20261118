#!/usr/bin/env python3
"""Draw the front page for make.fun news-image-20261118 (round 2).

A 1024x1024 newspaper front page summarising Wednesday 18 November 2026,
rendered with PIL from real headlines researched on the day. Round 2 expands
the grid from 15 to 24 stories (25 with the lead) to match the live board's
breadth, while keeping every headline and blurb short so the page stays
legible. The hero art is an original flat-vector illustration
(assets/hero-bridge.png) drawn for the lead story.
Run: python3 build_frontpage.py  ->  writes entry.png
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 28                      # side margin
CW = W - 2 * M              # content width = 968
PAPER = (248, 244, 236)
INK = (20, 20, 20)
NAVY = (27, 42, 74)
RED = (163, 22, 33)
GREY = (90, 86, 78)
RULE = (20, 20, 20)


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


def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ------------------------------------------------------
    d.line([(M, 12), (W - M, 12)], fill=RULE, width=3)
    title = "THE DAILY GLOBE"
    tf = SERIF_B(68)
    d.text(((W - d.textlength(title, font=tf)) / 2, 16), title, font=tf, fill=NAVY)
    d.line([(M, 92), (W - M, 92)], fill=RULE, width=2)
    dl = "WEDNESDAY, 18 NOVEMBER 2026"
    df = SANS_B(22)
    d.text((M, 98), dl, font=df, fill=INK)
    dr = "25 STORIES  \u2022  SIX CONTINENTS"
    drf = SANS_B(17)
    d.text((W - M - d.textlength(dr, font=drf), 101), dr, font=drf, fill=RED)
    d.line([(M, 126), (W - M, 126)], fill=RULE, width=3)

    # --- hero illustration ---------------------------------------------
    hero = Image.open("assets/hero-bridge.png").convert("RGB")
    hw, hh = hero.size
    # crop a band that keeps the bridge deck and the smoke column, then scale
    top = int(hh * 0.55)
    band = hero.crop((0, top, hw, int(hh * 0.88)))
    band = band.resize((CW, 120), Image.LANCZOS)
    img.paste(band, (M, 132))
    d.text((M, 256), "ILLUSTRATION \u2014 The Kerch Strait crossing, struck for a second straight day.",
           font=SERIF_I(13), fill=GREY)

    # --- lead story ------------------------------------------------------
    lead_h = "UKRAINE HITS CRIMEA BRIDGE AGAIN"
    lf = SERIF_B(38)
    d.text((M, 274), lead_h, font=lf, fill=INK)
    lead_s = ("Kyiv strikes the strategic crossing for a second consecutive day, "
              "as Russian missiles pound bridges around the capital.")
    sf = SANS(16)
    y = 322
    for line in wrap(d, lead_s, sf, CW):
        d.text((M, y), line, font=sf, fill=INK)
        y += 20
    d.line([(M, 370), (W - M, 370)], fill=RULE, width=2)

    # --- story grid: 3 columns x 8 rows = 24 stories --------------------
    # Every headline <= 2 lines at 17pt, every blurb exactly 1 line at 12pt
    # in a 312px column; the build fails loudly if any text overflows.
    stories = [
        ("ASIA", "Trump lands in Manila for Quad talks",
         "US president arrives ahead of a visit to China."),
        ("MIDDLE EAST", "Drones hit US radar site in Bahrain",
         "Gulf states report interceptions after the attack."),
        ("ASIA", "Modi offers free e-visas at ASEAN",
         "India's PM pitches a maritime pact in Manila."),
        ("AMERICAS", "Xi meets Carney as trade deals extend",
         "Canada, China deepen ties before the APEC summit."),
        ("EUROPE", "Britain sanctions settlement firms",
         "London acts to protect the two-state solution."),
        ("MIDDLE EAST", "Eisenkot to form Israel's government",
         "Herzog bypasses Netanyahu, picks the ex-army chief."),
        ("MIDDLE EAST", "Four nations demand Gaza aid access",
         "Australia, Canada, Italy, UK cite flooding in Gaza."),
        ("EUROPE", "EU to borrow \u20ac45bn to fund Ukraine",
         "Brussels plans bonds to cover Kyiv's \u20ac70bn gap."),
        ("TECH", "Nvidia revenue jumps 103%; Huang out",
         "Sales double; the board refuses to reinstate Huang."),
        ("BUSINESS", "Amazon's $7bn for India renewables",
         "Investment backs clean-energy projects in India."),
        ("TECH", "Baidu chief warns of an AI bubble",
         "China's search giant cautions on valuations."),
        ("ASIA", "Cyclone Akvan bears down on Bengal",
         "Storm to intensify; Chennai\u2013Yangon flights axed."),
        ("EUROPE", "Cyber-attack freezes store freezers",
         "Freezers fail in dozens of stores in seven nations."),
        ("SPORT", "Dhoni retires from IPL, becomes mentor",
         "The Chennai great ends his playing career to coach."),
        ("SPORT", "India lift 10th SAFF title over Pakistan",
         "India beat Pakistan 2\u20131 in the final in Dhaka."),
        ("AMERICAS", "Trump plotter jailed for 27\u00bd years",
         "Merchant gets 330 months for the Iran-backed plot."),
        ("MIDDLE EAST", "Tanker hit in Hormuz; 21 Indians saved",
         "LPG tanker attacked; 21 of 24 Indians evacuated."),
        ("EUROPE", "Latvia approves Kulbergs cabinet",
         "Latvia's parliament backs the new cabinet in a vote."),
        ("MIDDLE EAST", "WFP: Gaza gets one hot meal in two days",
         "Gaza camps face a cooking-gas shortage, WFP warns."),
        ("TECH", "India re-elected to UN telecom council",
         "New Delhi keeps its ITU Council seat for 2027\u20132030."),
        ("SPORT", "Jay Shah re-elected ICC chairman",
         "The cricket chief wins a second consecutive term."),
        ("ASIA", "ASEAN backs AI growth for small firms",
         "Leaders adopt a plan to bring AI to small business."),
        ("AMERICAS", "Judge delays Trump BBC deposition",
         "$10bn BBC defamation deposition moves to 22 January."),
        ("BUSINESS", "Deutsche Bank ignored risk warnings",
         "Leaked files show alerts over risky clients ignored."),
    ]
    assert len(stories) == 24, len(stories)
    col_w, gap, row_h = 312, 16, 72
    x0s = [M, M + col_w + gap, M + 2 * (col_w + gap)]
    kf, hf, bf = SANS_B(11), SERIF_B(17), SANS(12)
    for i, (kick, head, body) in enumerate(stories):
        r, c = divmod(i, 3)
        x, y = x0s[c], 378 + r * row_h
        d.text((x, y), kick, font=kf, fill=RED)
        hlines = wrap(d, head, hf, col_w)
        if len(hlines) > 2:
            raise SystemExit(f"OVERFLOW headline {i} ({kick}): {head!r} -> {hlines}")
        yy = y + 13
        for line in hlines:
            d.text((x, yy), line, font=hf, fill=INK)
            yy += 19
        blines = wrap(d, body, bf, col_w)
        if len(blines) > 1:
            raise SystemExit(f"OVERFLOW blurb {i} ({kick}): {body!r} -> {blines}")
        d.text((x, y + 53), blines[0], font=bf, fill=(50, 48, 44))
        if c < 2:  # vertical divider between columns
            d.line([(x + col_w + gap // 2, y + 2), (x + col_w + gap // 2, y + row_h - 8)],
                   fill=(200, 192, 178), width=1)

    # --- by the numbers ---------------------------------------------------
    y = 960
    d.line([(M, y), (W - M, y)], fill=RULE, width=2)
    nums = ("BY THE NUMBERS:  \u20ac45bn EU loan  \u2022  +103% Nvidia  "
            "\u2022  $7bn Amazon  \u2022  2,230 Sudan deaths  \u2022  "
            "372 Ukraine deaths (Oct)  \u2022  27\u00bd yrs Merchant")
    nf = SANS_B(14)
    nw = d.textlength(nums, font=nf)
    if nw > CW:
        raise SystemExit(f"OVERFLOW numbers strip: {nw:.0f}px > {CW}px")
    d.text((M, y + 6), nums, font=nf, fill=NAVY)

    # --- footer ------------------------------------------------------------
    d.line([(M, 986), (W - M, 986)], fill=RULE, width=1)
    foot = "Every story above was first reported on Wednesday, 18 November 2026  \u2022  The Daily Globe"
    ff = SERIF_I(12)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 992), foot, font=ff, fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    draw()
