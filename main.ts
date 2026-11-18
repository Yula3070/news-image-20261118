// The Daily Globe — make.fun news-image-20261118 entry (Node 22, stdlib only).
// The front page is drawn by build_frontpage.py into entry.png; this program
// copies that image to the grader's output directory, deterministically:
// the same bytes in, the same bytes out, on every run. No network, no
// randomness, no writes anywhere else.

import { copyFileSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
copyFileSync(new URL("./entry.png", import.meta.url), join(outDir, "entry.png"));
