from __future__ import annotations

import csv
import html
import os
from pathlib import Path


def csv_to_html(csv_path: Path, html_path: Path, max_rows: int = 200, max_cols: int = 50) -> None:
    with csv_path.open("r", encoding="utf-8", newline="") as fp:
        reader = csv.reader(fp)
        rows = list(reader)

    rows = rows[:max_rows]
    rows = [r[:max_cols] for r in rows]

    def td(cell: str, th: bool = False) -> str:
        tag = "th" if th else "td"
        return f"<{tag}>" + html.escape(cell) + f"</{tag}>"

    table = ["<table>"]
    for i, r in enumerate(rows):
        table.append("<tr>" + "".join(td(c, th=(i == 0)) for c in r) + "</tr>")
    table.append("</table>")
    table_html = "\n".join(table)

    title = csv_path.name

    page = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>{html.escape(title)}</title>
  <style>
    body{{font-family:system-ui,Segoe UI,Arial,sans-serif;max-width:1100px;margin:40px auto;padding:0 16px;line-height:1.5}}
    a{{color:#0969da;text-decoration:none}} a:hover{{text-decoration:underline}}
    table{{border-collapse:collapse;width:100%;font-size:14px}}
    th,td{{border:1px solid #e5e7eb;padding:6px 8px;vertical-align:top}}
    th{{background:#f6f8fa;position:sticky;top:0}}
    .topbar{{display:flex;gap:12px;align-items:center;margin-bottom:12px;flex-wrap:wrap}}
    .hint{{color:#555}}
  </style>
</head>
<body>
  <div class="topbar">
    <a href="./index.html">← Volver a Tablas</a>
    <a href="./{html.escape(title)}" download>Descargar CSV</a>
    <span class="hint">Vista previa (máx. {max_rows} filas)</span>
  </div>
  <h1>{html.escape(title)}</h1>
  {table_html}
</body>
</html>
"""
    html_path.write_text(page, encoding="utf-8")


def main() -> int:
    csv_path = Path(os.environ["CSV_PATH"])
    html_path = Path(os.environ["HTML_PATH"])
    max_rows = int(os.environ.get("MAX_ROWS", "200"))
    max_cols = int(os.environ.get("MAX_COLS", "50"))
    csv_to_html(csv_path, html_path, max_rows=max_rows, max_cols=max_cols)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
