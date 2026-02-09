from __future__ import annotations

import argparse
from pathlib import Path
from datetime import datetime

def ensure_dirs(base: Path) -> dict[str, Path]:
    outputs = base / "outputs"
    report = base / "report"
    figures = outputs / "figures"
    tables = outputs / "tables"
    for p in (outputs, report, figures, tables):
        p.mkdir(parents=True, exist_ok=True)
    return {"outputs": outputs, "report": report, "figures": figures, "tables": tables}

def write_stub_report(base: Path, dirs: dict[str, Path]) -> None:
    md_path = base / "INFORME_FINAL.md"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    md = f"""# Práctica Titanic (Polars) — Informe

Generado automáticamente: **{now}**

## Estructura de outputs
- Figuras: `{dirs["figures"].as_posix()}`
- Tablas: `{dirs["tables"].as_posix()}`

## Estado
Pipeline base creado. A continuación se implementarán Ejercicio 1 y Ejercicio 2.
"""
    md_path.write_text(md, encoding="utf-8")

def main() -> int:
    parser = argparse.ArgumentParser(description="Práctica Titanic sin pandas (Polars).")
    parser.add_argument("--data-dir", type=str, default="data", help="Carpeta donde están los CSV.")
    args = parser.parse_args()

    base = Path(__file__).resolve().parents[1]  # raíz del repo
    _ = Path(args.data_dir)  # reservado para pasos siguientes

    dirs = ensure_dirs(base)
    write_stub_report(base, dirs)

    print("OK: estructura creada y INFORME_FINAL.md generado.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
