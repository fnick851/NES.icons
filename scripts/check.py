#!/usr/bin/env python3
"""Repo invariant checks. Run: python3 scripts/check.py   (stdlib only)

Enforces what svg-to-path.py and consumers rely on:
  1. icons.json parses, and every icon it lists (including aliases) has an
     SVG file on disk.
  2. Every SVG on disk is listed in icons.json (the index stays complete).
  3. Every SVG is a 16x16 grid of 1x1 <rect> pixels — the exact format
     svg-to-path.py converts; anything else would convert silently wrong.
  4. svg-to-path.py produces a non-empty path for every icon.

Exit 0 = all good, 1 = violations.
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

spec = importlib.util.spec_from_file_location("svg_to_path", ROOT / "scripts" / "svg-to-path.py")
svg_to_path = importlib.util.module_from_spec(spec)
spec.loader.exec_module(svg_to_path)

fails = 0


def fail(msg):
    global fails
    print(f"FAIL: {msg}")
    fails += 1


meta = json.loads((ROOT / "icons.json").read_text())
alias_to_real = {a: real for real, aliases in meta.get("aliases", {}).items() for a in aliases}
listed = {n for icons in meta["iconsByCategory"].values() for n in icons}
on_disk = {p.stem for p in (ROOT / "icons").glob("*.svg")}

missing = {n for n in listed if n not in on_disk and alias_to_real.get(n) not in on_disk}
for n in sorted(missing):
    fail(f"icons.json lists '{n}' but icons/{n}.svg does not exist")

listed_real = {alias_to_real.get(n, n) for n in listed}
for n in sorted(on_disk - listed_real):
    fail(f"icons/{n}.svg is not listed in icons.json")

RECT = re.compile(r"<rect x=\"\d+\" y=\"\d+\" width=\"(\d+)\" height=\"(\d+)\"")
for p in sorted((ROOT / "icons").glob("*.svg")):
    s = p.read_text()
    if 'width="16" height="16"' not in s:
        fail(f"{p.name}: not declared 16x16")
    non_unit = [m for m in RECT.findall(s) if m != ("1", "1")]
    if non_unit:
        fail(f"{p.name}: contains non-1x1 rects (svg-to-path.py assumes unit pixels)")
    if re.search(r"<(path|polygon|circle|ellipse|line)\b", s):
        fail(f"{p.name}: contains non-rect shapes (svg-to-path.py only reads rects)")
    if not svg_to_path.to_path(p):
        fail(f"{p.name}: svg-to-path.py produced an empty path")

if fails:
    print(f"\n{fails} check(s) failed")
    sys.exit(1)
print(f"all checks passed ({len(on_disk)} icons, {len(listed)} index entries)")
