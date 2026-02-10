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
    e1_total_not_survived,
    e1_not_survived_by_class_sex,
    e1_survived_and_not_by_class_sex,
    e1_add_is_minor,
    e1_dropna_age,   # <-- AÑADE ESTA LÍNEA
)


from src.ejercicio2 import (
    load_pasajeros,
    load_supervivientes,
    build_df,
    add_puerto,
    passengers_by_puerto,
    passengers_by_sex as e2_passengers_by_sex,
    mean_age_by_sex_survived,
    deaths_by_age_range,
    deaths_by_class_gender,
    survived_and_deaths_by_puerto,
    join_quality,
)

from src.io_utils import save_table, save_text

from src.plots import (
    bar_counts,
    bar_counts_hue,
    survived_vs_not,
    age_hist_with_kde,
    age_hist_alt,
)


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
    save_table(e1_head(df), dirs["tables"] / "e1_01_head.csv")
    sections.append("## Ejercicio 1 — Titanic\n")
    sections.append("- (1) Primeras 5 filas: `outputs/tables/e1_01_head.csv`")

    # 2) columnas
    cols = e1_columns(df)
    save_text(cols, dirs["tables"] / "e1_02_columns.txt")
    sections.append("- (2) Columnas: `outputs/tables/e1_columns.txt`")

    # 3) info (schema + nulos)
    save_table(e1_info(df), dirs["tables"] / "e1_03_info.csv")
    sections.append("- (3) Info (dtype + nulos): `outputs/tables/e1_03_info.csv`")

    # 4) pasajeros por clase
    save_table(e1_passengers_by_class(df), dirs["tables"] / "e1_04_by_class.csv")
    sections.append("- (4) Nº pasajeros por clase: `outputs/tables/e1_04_by_class.csv`")

     # 5) plot pasajeros por clase
    bar_counts(
        e1_passengers_by_class(df),
        x_col="Pclass",
        y_col="count",
        title="Recuento de pasajeros por clase",
        figpath=dirs["figures"] / "e1_05_passengers_by_class.png",
    )
    sections.append("- (5) Plot pasajeros por clase: `outputs/figures/e1_05_passengers_by_class.png`")

    # 6) por sexo
    save_table(e1_passengers_by_sex(df), dirs["tables"] / "e1_by_sex.csv")
    sections.append("- (6) Nº pasajeros por sexo: `outputs/tables/e1_06_by_sex.csv`")

    # 7) plot hombres vs mujeres
    bar_counts(
        e1_passengers_by_sex(df),
        x_col="Sex",
        y_col="count",
        title="Recuento de pasajeros por sexo",
        figpath=dirs["figures"] / "e1_07_passengers_by_sex.png",
    )
    sections.append("- (7) Plot pasajeros por sexo: `outputs/figures/e1_07_passengers_by_sex.png`")

    # 8) sexo por clase
    save_table(e1_sex_by_class(df), dirs["tables"] / "e1_08_sex_by_class.csv")
    sections.append("- (8) Nº hombres/mujeres por clase: `outputs/tables/e1_sex_by_class.csv`")

    # 9) plot sexo por clase (barras agrupadas)
    bar_counts_hue(
        e1_sex_by_class(df),
        x_col="Pclass",
        hue_col="Sex",
        y_col="count",
        title="Recuento por clase y sexo",
        figpath=dirs["figures"] / "e1_09_sex_by_class.png",
    )
    sections.append("- (9) Plot por sexo y clase: `outputs/figures/e1_09_sex_by_class.png`")

    # 10) sobrevivientes por clase/sexo (con Survived)
    save_table(e1_survived_by_class_sex(df), dirs["tables"] / "e1_10_surv_by_class_sex.csv")
    sections.append("- (10) Supervivencia por clase/sexo: `outputs/tables/e1_10_surv_by_class_sex.csv`")

     # 11) plot sobrevivieron vs no
    survived_vs_not(df, dirs["figures"] / "e1_11_survived_vs_not.png")
    sections.append("- (11) Plot supervivencia (Sí/No): `outputs/figures/e1_11_survived_vs_not.png`")

    # 12) total no sobrevivieron
    save_table(e1_total_not_survived(df), dirs["tables"] / "e1_12_total_not_survived.csv")
    sections.append("- (12) Total no sobrevivieron: `outputs/tables/e1_12_total_not_survived.csv`")

    # 13) no sobrevivieron por clase y sexo
    save_table(e1_not_survived_by_class_sex(df), dirs["tables"] / "e1_13_not_surv_by_class_sex.csv")
    sections.append("- (13) No sobrevivieron por clase/sexo: `outputs/tables/e1_13_not_surv_by_class_sex.csv`")

    # 14) sobrevivieron y no sobrevivieron por clase y sexo
    save_table(e1_survived_and_not_by_class_sex(df), dirs["tables"] / "e1_14_surv_and_not_by_class_sex.csv")
    sections.append("- (14) Sobrevivieron/No por clase/sexo: `outputs/tables/e1_14_surv_and_not_by_class_sex.csv`")

    # 15) eliminar registros con edad nula
    df_age_clean = e1_dropna_age(df)
    save_table(
        pl.DataFrame({
            "rows_before": [df.height],
            "rows_after": [df_age_clean.height],
        }),
        dirs["tables"] / "e1_15_dropna_age_summary.csv",
    )
    sections.append(
        "- (15) Eliminación de registros con Age nula — resumen: "
        "`outputs/tables/e1_15_dropna_age_summary.csv`"
    )
    
    # 16) distribución edad hist + densidad (tras eliminar nulos)
    age_hist_with_kde(df, dirs["figures"] / "e1_16_age_hist_kde.png")
    sections.append("- (16) Distribución edad (hist + densidad): `outputs/figures/e1_16_age_hist_kde.png`")

    # 17) hist alternativo
    age_hist_alt(df, dirs["figures"] / "e1_17_age_hist_alt.png")
    sections.append("- (17) Histograma edad (alt): `outputs/figures/e1_17_age_hist_alt.png`")

    # 18) columna IsMinor16 (muestra conteo final como verificación)
    df_minor = e1_add_is_minor(df)
    minor_counts = (
        df_minor.group_by("IsMinor16")
        .agg(pl.len().alias("count"))
        .sort("IsMinor16")
    )
    save_table(minor_counts, dirs["tables"] / "e1_18_minor16_counts.csv")
    sections.append("- (18) Menores de 16 (columna IsMinor16) — recuento: `outputs/tables/e1_18_minor16_counts.csv`")

    return sections

def run_ejercicio2(data_dir: Path, dirs: dict[str, Path]) -> list[str]:
    sections: list[str] = []
    sections.append("\n## Ejercicio 2 — Pasajeros + Supervivientes (inner join)\n")

    df_p = load_pasajeros(data_dir)
    df_s = load_supervivientes(data_dir)

    df_joined = build_df(data_dir)
    df = add_puerto(df_joined)

    # Diagnóstico join (muy importante porque tus tamaños no coinciden)
    save_table(join_quality(df_p, df_s, df_joined), dirs["tables"] / "e2_join_quality.csv")
    sections.append("- Join quality: `outputs/tables/e2_join_quality.csv`")

    # (1) puerto
    # (guardamos un ejemplo de columnas para ver que existe)
    save_table(df.select(["PassengerId", "Embarked", "puerto"]).head(20), dirs["tables"] / "e2_01_puerto_sample.csv")
    sections.append("- (1) Columna puerto (sample): `outputs/tables/e2_01_puerto_sample.csv`")

    # (2)
    save_table(passengers_by_puerto(df), dirs["tables"] / "e2_02_passengers_by_puerto.csv")
    sections.append("- (2) Nº pasajeros por puerto: `outputs/tables/e2_02_passengers_by_puerto.csv`")

    # (3)
    save_table(e2_passengers_by_sex(df), dirs["tables"] / "e2_03_passengers_by_sex.csv")
    sections.append("- (3) Nº hombres y mujeres: `outputs/tables/e2_03_passengers_by_sex.csv`")

    # (4)
    save_table(mean_age_by_sex_survived(df), dirs["tables"] / "e2_04_mean_age_by_sex_survived.csv")
    sections.append("- (4) Edad media por sexo y supervivencia: `outputs/tables/e2_04_mean_age_by_sex_survived.csv`")

    # (5)
    save_table(deaths_by_age_range(df), dirs["tables"] / "e2_05_deaths_by_age_range.csv")
    sections.append("- (5) Muertos por rango de edad: `outputs/tables/e2_05_deaths_by_age_range.csv`")

    # (6)
    save_table(deaths_by_class_gender(df), dirs["tables"] / "e2_06_deaths_by_class_gender.csv")
    sections.append("- (6) Muertos por clase y género: `outputs/tables/e2_06_deaths_by_class_gender.csv`")

    # (7)
    save_table(survived_and_deaths_by_puerto(df), dirs["tables"] / "e2_07_survived_and_deaths_by_puerto.csv")
    sections.append("- (7) Muertos y supervivientes por puerto: `outputs/tables/e2_07_survived_and_deaths_by_puerto.csv`")

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
    sections.extend(run_ejercicio2(data_dir, dirs))
    
    write_report_stub(base, dirs, sections)

    print("OK: Pipeline Completo (Ej1 + Ej2) ejecutado; outputs(tables + figures) e INFORME_FINAL.md generados.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#######################################################################################