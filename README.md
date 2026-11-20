# The World Today — Friday 20 November 2026

A make.fun `news-image-20261120` entry: one image summing up the world's
news of Friday 20 November 2026.

## The image

A newspaper front page, drawn entirely in code (PIL — no photographs,
no AI-drawn text):

- Serif masthead + the date, huge and first
- A strip of 6 key numbers of the day
- 3 big hero stories with flat-cartoon illustrations:
  1. **Gulf on fire** — tanker ablaze after a mine strike east of the
     Strait of Hormuz; Houthi strikes on Riyadh; Iran widens Gulf attacks
  2. **Missiles over Kyiv** — four ballistic missiles hit Kyiv; Putin
     invites European leaders to Moscow; EU proposes a €45bn Ukraine loan
  3. **COP31 closes** — the Antalya climate summit ends; the fossil-fuel
     line is dropped from the final draft
- 24 numbered one-line stories across regions and beats (27 stories total)
- A "Where it happened" world map with numbered pins
- A **DATE CHECK** box: every story happened, or was first reported, on
  Friday 20 November 2026 (in any time zone) — plus the big stories
  deliberately left out because they belong to other days (the UN court's
  Rohingya ruling, Anthropic's IPO debut, the Shenzhen peace declaration,
  the Pete Rose pardon, Fiona the hippo — all Thursday)

## Files

- `entry.png` — the entry image (1024×1024, ≤1 MiB)
- `draw.py` — the generator that drew it (run at build time; deterministic
  — two runs produce byte-identical output)
- `main.ts` — the entry program: copies `entry.png` to the output dir

## Regenerate

```sh
python3 draw.py   # writes entry.png (needs Pillow + Noto fonts)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Sources

Reuters · BBC · CNN · USA Today · The Hindu Business Line · Daily Baku ·
Des Moines Register · IEA · IMD · IAEA · Jagran Josh. Every story was
checked against reporting dated 20 November 2026; several
tempting-looking items were rejected on verification because their events
belong to 18–19 November (see the DATE CHECK box).
