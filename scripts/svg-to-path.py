#!/usr/bin/env python3
"""Convert a NES.icons rect-grid SVG into one compact <path> d-string.

The icons in icons/ are 16x16 grids of 1x1 <rect> elements. For inlining an
icon into HTML (the way the portfolio consumes this repo), a single path with
horizontal run-length merging is ~5x smaller and one element instead of ~60.

Usage:  python3 scripts/svg-to-path.py icons/trophy.svg
Output: the d-string; wrap it like
  <svg class="title-icon" viewBox="0 0 16 16" width="16" height="16"
       fill="currentColor" aria-hidden="true"><path d="..."/></svg>
"""
import re
import sys


def to_path(svg_file):
    s = open(svg_file).read()
    px = sorted(set((int(m[0]), int(m[1])) for m in re.findall(r'<rect x="(\d+)" y="(\d+)"', s)))
    rows = {}
    for x, y in px:
        rows.setdefault(y, []).append(x)
    segs = []
    for y in sorted(rows):
        xs = sorted(rows[y])
        run_start, prev = xs[0], xs[0]
        for x in xs[1:] + [None]:
            if x != prev + 1:
                segs.append(f"M{run_start} {y}h{prev - run_start + 1}v1H{run_start}z")
                if x is not None:
                    run_start = x
            if x is not None:
                prev = x
    return "".join(segs)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    print(to_path(sys.argv[1]))
