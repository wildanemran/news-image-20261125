// news-image-20261125 — "The World in One Day".
// The entry is a front page (entry.png) summing up the world's news of
// Wednesday 25 November 2026: the Asian AI selloff (TAIEX -4.8%, KOSPI -6.2%,
// Nikkei -2.8%), Australia passing the Digital Duty of Care Bill, the
// Zaporizhzhia plant losing external power, four Houthi drones intercepted
// near Ras Tanura, Rutte meeting Trump in Florida, the CIA and ODNI breach,
// and the Iowa ammunition plant detonation plan.
// This program only puts that image where the grader reads it, as
// /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png when set).
// It copies bytes and nothing else, so two runs write identical output.

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outDir, { recursive: true });
const image = readFileSync(join(here, "entry.png"));
writeFileSync(join(outDir, "entry.png"), image);
