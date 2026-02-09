from __future__ import annotations

import argparse
from pathlib import Path
from datetime import datetime

import polars as pl

from src.ejercicio1 import (
    load_titanic,
    e1_head,
    e1_columns,
    e1_info,
    e1_passengers_by_class,
    e1_passengers_by_sex,
    e1_sex_by_class,
    e1_survived_by_class_sex,
)
from src.io_utils import save_table, save_text


def ensure_dirs(base: Path) -> dict[str, Path]:
    outputs = base / "outputs"
    report = base / "report"
    figures = outputs / "figures"
    tables = outputs / "tables"
    for p in (outputs, report, figures, tables):
        p.mkdir(parents=True, exist_ok=True)
    return {"outputs": outputs, "report": report, "figures": figures, "tables": tables}


def write_report_stub(base: Path, dirs: dict[str, Path], sections: list[str]) -> None:
    md_path = base / "INFORME_FINAL.md"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    body = "\n".join(sections)
    md = f"""# Práctica Titanic (Polars) — Informe

Generado automáticamente: **{now}**

## Outputs
- Figuras: `{dirs["figures"].as_posix()}`
- Tablas: `{dirs["tables"].as_posix()}`

{body}
"""
    md_path.write_text(md, encoding="utf-8")


def run_ejercicio1(data_dir: Path, dirs: dict[str, Path]) -> list[str]:
    sections: list[str] = []
    df = load_titanic(data_dir)

    # 1) head
    save_table(e1_head(df), dirs["tables"] / "e1_head.csv")
    sections.append("## Ejercicio 1 — Titanic\n")
    sections.append("- (1) Primeras 5 filas: `outputs/tables/e1_head.csv`")

    # 2) columnas
    cols = e1_columns(df)
    save_text(cols, dirs["tables"] / "e1_columns.txt")
    sections.append("- (2) Columnas: `outputs/tables/e1_columns.txt`")

    # 3) info (schema + nulos)
    save_table(e1_info(df), dirs["tables"] / "e1_info.csv")
    sections.append("- (3) Info (dtype + nulos): `outputs/tables/e1_info.csv`")

    # 4) pasajeros por clase
    save_table(e1_passengers_by_class(df), dirs["tables"] / "e1_by_class.csv")
    sections.append("- (4) Nº pasajeros por clase: `outputs/tables/e1_by_class.csv`")

    # 6) por sexo
    save_table(e1_passengers_by_sex(df), dirs["tables"] / "e1_by_sex.csv")
    sections.append("- (6) Nº pasajeros por sexo: `outputs/tables/e1_by_sex.csv`")

    # 8) sexo por clase
    save_table(e1_sex_by_class(df), dirs["tables"] / "e1_sex_by_class.csv")
    sections.append("- (8) Nº hombres/mujeres por clase: `outputs/tables/e1_sex_by_class.csv`")

    # 10) sobrevivientes por clase/sexo (con Survived)
    save_table(e1_survived_by_class_sex(df), dirs["tables"] / "e1_surv_by_class_sex.csv")
    sections.append("- (10) Supervivencia por clase/sexo: `outputs/tables/e1_surv_by_class_sex.csv`")

    return sections


def main() -> int:
    parser = argparse.ArgumentParser(description="Práctica Titanic sin pandas (Polars).")
    parser.add_argument("--data-dir", type=str, default="data", help="Carpeta donde están los CSV.")
    args = parser.parse_args()

    base = Path(__file__).resolve().parents[1]
    data_dir = base / args.data_dir

    dirs = ensure_dirs(base)

    sections = []
    sections.extend(run_ejercicio1(data_dir, dirs))

    write_report_stub(base, dirs, sections)

    print("OK: Ejercicio 1 (tablas) generado en outputs/tables y actualizado INFORME_FINAL.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
