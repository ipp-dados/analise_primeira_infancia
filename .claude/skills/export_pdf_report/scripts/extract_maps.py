"""Extract the MAPS array (5 pre-compressed base64 map images + captions)
that relatorio/*.html embeds inline, into a standalone JSON file, so
build_notebook_report.py doesn't need to re-encode/resize mapas/*.png itself
(the relatorio pages already ship them resized to ~130KB each as WebP).

Usage:
    python extract_maps.py <relatorio.html> <out.json>
"""
import json
import re
import sys

src_path = sys.argv[1]
out_path = sys.argv[2]

with open(src_path, "r", encoding="utf-8") as f:
    html = f.read()

m = re.search(r"const MAPS = (\[.*?\]);", html, re.S)
if not m:
    raise SystemExit(f"no 'const MAPS = [...]' found in {src_path}")

maps = json.loads(m.group(1))  # already valid JSON (Python-generated via json.dumps upstream)
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(maps, f)

print(f"extracted {len(maps)} maps -> {out_path}")
