from __future__ import annotations

import glob
import html
import os
from pathlib import Path


def main() -> int:
    tables_dir = Path(os.environ.get("TABLES_DIR", "site/tables"))
    out_path = Path(os.environ.get("OUT_PATH", str(tables_dir / "index.html")))

    tables_dir.mkdir(parents=True, exist_ok=True)
    files = sorted(glob.glob(str(tables_dir / "*")))

    items: list[str] = []
    for p in files:
        bn = Path(p).name
        if bn == "index.html":
            continue
        if bn.endswith(".html"):
            # previews individuales no se listan
            continue
        if bn.endswith(".csv"):
            view = bn[:-4] + ".html"
            items.append(
                f'<li><a href="./{html.escape(view)}">{html.escape(bn)}</a> '
                f'<span style="color:#555;font-size:12px">(vista)</span></li>'
            )
        else:
            items.append(f'<li><a href="./{html.escape(bn)}">{html.escape(bn)}</a></li>')

    page = """<!doctype html><html lang="es"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tablas</title>
<style>
body{font-family:system-ui,Segoe UI,Arial,sans-serif;max-width:980px;margin:40px auto;padding:0 16px}
li{margin:6px 0}
a{color:#0969da;text-decoration:none} a:hover{text-decoration:underline}
.hint{color:#555;font-size:12px}
</style></head>
<body>
<h1>Tablas (CSV/TXT)</h1>
<p><a href="../index.html">← Volver</a></p>
<p class="hint">Los CSV se abren en vista previa HTML; puedes descargarlos desde cada página.</p>
<ul>
""" + "\n".join(items) + """
</ul>
</body></html>
"""
    out_path.write_text(page, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
