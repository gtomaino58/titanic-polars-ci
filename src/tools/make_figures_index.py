from __future__ import annotations

import glob
import html
import os
from pathlib import Path


def main() -> int:
    figures_dir = Path(os.environ.get("FIGURES_DIR", "site/figures"))
    out_path = Path(os.environ.get("OUT_PATH", str(figures_dir / "index.html")))

    figures_dir.mkdir(parents=True, exist_ok=True)
    files = sorted(glob.glob(str(figures_dir / "*.png")))

    items = "\n".join(
        f'<li><a href="./{html.escape(Path(p).name)}">{html.escape(Path(p).name)}</a></li>'
        for p in files
    )

    page = f"""<!doctype html><html lang="es"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Figuras</title>
<style>
body{{font-family:system-ui,Segoe UI,Arial,sans-serif;max-width:980px;margin:40px auto;padding:0 16px}}
li{{margin:6px 0}}
a{{color:#0969da;text-decoration:none}} a:hover{{text-decoration:underline}}
</style></head>
<body>
<h1>Figuras (PNG)</h1>
<p><a href="../index.html">← Volver</a></p>
<ul>
{items}
</ul>
</body></html>
"""
    out_path.write_text(page, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
