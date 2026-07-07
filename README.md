# NES.icons (fnick851 fork)

Hand-drawn 16×16 pixel-art icon SVGs, forked from [nostalgic-css/NES.icons](https://github.com/nostalgic-css/NES.icons) (MIT). Upstream has been frozen at v3.0.0-beta.4 since 2020; this fork keeps the icon sources alive and drops the rest.

What upstream shipped was an icon *webfont* plus its build toolchain. Icon fonts are a legacy practice and that 2020 toolchain no longer runs, so this fork deleted it (recoverable from git history). What remains has **zero dependencies**:

- `icons/` — 53 icon SVGs, each a 16×16 grid of 1×1 `<rect>` pixels, plus `.aseprite` working files for some
- `icons.json` — category and alias index (kept in sync with the files)
- `scripts/svg-to-path.py` — converts an icon into one compact `<path>` d-string for inlining in HTML
- `scripts/check.py` — repo invariants: index ↔ files in sync, every SVG in the exact grid format the converter assumes

## Usage

```
$ python3 scripts/svg-to-path.py icons/trophy.svg
M2 0h11v1H2zM2 1h1v1H2z…
```

Wrap the output like:

```html
<svg viewBox="0 0 16 16" width="16" height="16" fill="currentColor" aria-hidden="true">
  <path d="…" />
</svg>
```

After changing anything, run `python3 scripts/check.py`.
