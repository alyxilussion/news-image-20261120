// news-image-20261120 entry (Node 22, standard library only).
//
// The entry is the image in entry.png beside this file: a newspaper
// front page summing up Friday 20 November 2026, drawn in code by
// draw.py (PIL, run at build time -- the grader has no network and no
// third-party packages, so the program ships the finished PNG).
//
// This program copies entry.png to the output directory. It writes the
// same bytes on every run: the file is copied verbatim, nothing is
// generated or read from the network here.
//
// Local run:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, 'entry.png'), join(outDir, 'entry.png'));
