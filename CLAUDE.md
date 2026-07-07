# NES.icons fork (fnick851/NES.icons)

Personal fork of the dormant nostalgic-css/NES.icons (upstream frozen at v3.0.0-beta.4, last commit May 2020). Kept as **source custody for the pixel-art icon SVGs only** — the sibling of the NES.css fork at `~/workspace/others/NES.css`, consumed by the portfolio at `~/workspace/others/portfolio`.

## What this repo is (and isn't)

Upstream's deliverable was an icon webfont built by a 2020 toolchain (node-sass, `webfont`, semantic-release, CircleCI). That entire toolchain was **deliberately deleted** from this fork in July 2026 — icon fonts are a legacy practice, the build no longer ran, and the portfolio consumes raw SVGs instead. Do not reintroduce it; if it is ever genuinely needed, recover it from git history (or upstream) rather than rebuilding from memory.

What remains has zero dependencies: `icons/` (53 SVGs + `.aseprite` sources), `icons.json` (index), and two stdlib-Python scripts.

## How icons are consumed

The portfolio inlines icons directly in `index.html` as single-path SVGs with `fill="currentColor"`. To add one:

1. Pick an icon from `icons/` (`icons.json` lists them by category).
2. Run `python3 scripts/svg-to-path.py icons/<name>.svg` to get the compact d-string.
3. Inline it in the consumer:
   `<svg class="title-icon" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" aria-hidden="true"><path d="..."/></svg>`

Icons in use so far: `trophy` (EXPERIENCES title), `nes` (PROJECTS title). Per the portfolio's CLAUDE.md, icons must be semantic for their spot — purely decorative additions have been explicitly rejected.

## Invariants — run `python3 scripts/check.py` after any change

- Every icon listed in `icons.json` (including aliases) has an SVG file, and every SVG is listed — the index never drifts. (Upstream itself had drifted: a phantom `social` entry and an unindexed `star.svg`, fixed here in July 2026.)
- Every SVG is a 16×16 grid of 1×1 `<rect>` elements and nothing else. This is not just style: `svg-to-path.py` assumes unit rects, and any other shape would convert silently wrong. New icons must follow the same format.
