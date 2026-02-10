# Práctica Titanic (Polars) — Informe automático

Generado automáticamente: **2026-02-10 18:33:08**

## Outputs
- Figuras: `/home/runner/work/titanic-polars-ci/titanic-polars-ci/outputs/figures`
- Tablas: `/home/runner/work/titanic-polars-ci/titanic-polars-ci/outputs/tables`

## Ejercicio 1 — Titanic

- (1) Primeras 5 filas: `outputs/tables/e1_01_head.csv`
- (2) Columnas: `outputs/tables/e1_02_columns.txt`
- (3) Info (dtype + nulos): `outputs/tables/e1_03_info.csv`
- (4) Nº pasajeros por clase: `outputs/tables/e1_04_by_class.csv`
- (5) Plot pasajeros por clase: `outputs/figures/e1_05_passengers_by_class.png`
- (6) Nº pasajeros por sexo: `outputs/tables/e1_06_by_sex.csv`
- (7) Plot pasajeros por sexo: `outputs/figures/e1_07_passengers_by_sex.png`
- (8) Nº hombres/mujeres por clase: `outputs/tables/e1_08_sex_by_class.csv`
- (9) Plot por sexo y clase: `outputs/figures/e1_09_sex_by_class.png`
- (10) Supervivientes por clase/sexo (pivot + total): `outputs/tables/e1_10_survived_by_class_sex_pivot.csv`
- (11) Plot supervivencia (Sí/No): `outputs/figures/e1_11_survived_vs_not.png`
- (12) Total no sobrevivieron: `outputs/tables/e1_12_total_not_survived.csv`
- (13) No sobrevivieron por clase/sexo: `outputs/tables/e1_13_not_surv_by_class_sex.csv`
- (14) Supervivieron y no por clase/sexo (pivot): `outputs/tables/e1_14_survived_not_by_class_sex_pivot.csv`
- (15) Eliminación Age nula (resumen): `outputs/tables/e1_15_dropna_age_summary.csv`
- (16) Distribución edad (hist + densidad): `outputs/figures/e1_16_age_hist_kde.png`
- (17) Histograma edad (alt): `outputs/figures/e1_17_age_hist_alt.png`
- (18) Menores de 16 (recuento): `outputs/tables/e1_18_minor16_counts.csv`

## Ejercicio 2 — Pasajeros + Supervivientes (inner join)

- Join quality: `outputs/tables/e2_00_join_quality.csv`
- (1) Columna puerto (sample): `outputs/tables/e2_01_puerto_sample.csv`
- (2) Nº pasajeros por puerto: `outputs/tables/e2_02_passengers_by_puerto.csv`
- (3) Nº hombres y mujeres: `outputs/tables/e2_03_passengers_by_sex.csv`
- (4) Edad media por sexo y supervivencia: `outputs/tables/e2_04_mean_age_by_sex_survived.csv`
- (5) Muertos por rango de edad: `outputs/tables/e2_05_deaths_by_age_range.csv`
- (6) Muertos por clase y género: `outputs/tables/e2_06_deaths_by_class_gender.csv`
- (7) Muertos y supervivientes por puerto: `outputs/tables/e2_07_survived_and_deaths_by_puerto.csv`
