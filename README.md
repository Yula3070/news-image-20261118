# The Daily Globe — 18 November 2026

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/yula3070/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/yula3070/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

A one-image front page summing up Wednesday 18 November 2026's world news,
built for make.fun's `news-image-20261118` bounty ($250 USDC).

## The image

`entry.png` (1024×1024, PNG) is a newspaper front page — **The Daily Globe** —
with 25 stories from six continents, all first reported on 18 November 2026:

- **Lead:** Ukraine strikes the Crimea (Kerch) bridge for a second straight day
- **Asia:** Trump lands in Manila for Quad talks; Modi's e-visa offer at the
  ASEAN summit; Cyclone Akvan bears down on the Bay of Bengal; ASEAN backs
  AI growth for small firms
- **Middle East:** drones hit a US radar site in Bahrain; Eisenkot tapped to
  form Israel's government; four nations demand Gaza aid access; a tanker
  attacked in Hormuz with 21 Indians rescued; WFP: Gaza gets one hot meal
  in two days
- **Americas / Europe:** Xi meets Carney as Canada–China extend trade deals;
  Britain sanctions settlement firms; the EU's €45bn Ukraine loan; Latvia
  approves a new cabinet; a judge delays Trump's BBC deposition; the
  Trump-plotter jailed for 27½ years
- **Tech / Business:** Nvidia revenue +103% as Huang steps down; Amazon's $7bn
  for India's renewables; Baidu's chief warns of an AI bubble; India
  re-elected to the UN telecom council; Deutsche Bank ignored risk warnings
- **Sport:** Dhoni retires from the IPL; India lift a 10th SAFF title;
  Jay Shah re-elected ICC chairman

A "By the numbers" strip (now six figures, incl. 372 Ukraine civilian
deaths in October per the UN) and a dated footer close the page. The date
is named twice — in the masthead dateline and in the footer — so the day
it sums up is unmistakable.

## How it was made

- `build_frontpage.py` draws the page with PIL (Liberation Serif/Sans):
  masthead, dateline, lead story, a 3×8 story grid (24 stories), numbers
  strip, footer. It fails loudly if any headline needs more than 2 lines
  or any blurb more than 1 line, so no text is ever cut off or garbled.
- `assets/hero-bridge.png` is an original flat-vector illustration generated
  for the lead story (a strait bridge at dusk); it is captioned as an
  illustration in the image itself.
- `main.ts` (Node 22, standard library only) copies `entry.png` to the
  output directory. It runs offline and writes identical bytes every run.

## Files

- `entry.png` — the entry image (1024×1024, under 1 MiB)
- `main.ts` — entrypoint: copies `entry.png` to `$MAKEFUN_OUTPUT_DIR`
- `build_frontpage.py` — the program that draws the front page
- `assets/hero-bridge.png` — original hero illustration
- `LICENSE` — MIT

---

<sub>Entered on [make.fun](https://make.fun/?ref=tfznw81m&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
