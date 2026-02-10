from __future__ import annotations

import polars as pl
from pathlib import Path


# =========================================================
# Carga de datos
# =========================================================

def load_titanic(data_dir: Path) -> pl.DataFrame:
    return pl.read_csv(data_dir / "titanic.csv")


# =========================================================
# Análisis exploratorio básico
# =========================================================

def e1_head(df: pl.DataFrame, n: int = 5) -> pl.DataFrame:
    return df.head(n)


def e1_columns(df: pl.DataFrame) -> list[str]:
    return df.columns


def e1_info(df: pl.DataFrame) -> pl.DataFrame:
    schema = pl.DataFrame(
        {
            "column": df.columns,
            "dtype": [str(df.schema[c]) for c in df.columns],
        }
    )
    nulls = (
        df.null_count()
        .transpose(include_header=True, header_name="column", column_names=["nulls"])
    )
    return schema.join(nulls, on="column", how="left")


def e1_passengers_by_class(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df.group_by("Pclass")
        .agg(pl.len().alias("count"))
        .sort("Pclass")
    )


def e1_passengers_by_sex(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df.group_by("Sex")
        .agg(pl.len().alias("count"))
        .sort("Sex")
    )


def e1_sex_by_class(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df.group_by(["Pclass", "Sex"])
        .agg(pl.len().alias("count"))
        .sort(["Pclass", "Sex"])
    )


# =========================================================
# Punto 10 — SOLO supervivientes (pivot)
# =========================================================

def e1_survived_pivot_by_class_sex(df: pl.DataFrame) -> pl.DataFrame:
    """
    (10) Número de pasajeros que sobrevivieron en cada clase,
    agrupados por sexo, SOLO supervivientes.
    Incluye total por clase.
    """
    surv = df.filter(pl.col("Survived") == 1)

    pivot = (
        surv.group_by(["Pclass", "Sex"])
        .agg(pl.len().alias("count"))
        .pivot(
            index="Pclass",
            columns="Sex",
            values="count",
            aggregate_function="first",
        )
        .sort("Pclass")
    )

    # Asegurar columnas esperadas
    for col in ["female", "male"]:
        if col not in pivot.columns:
            pivot = pivot.with_columns(pl.lit(0).alias(col))

    pivot = pivot.with_columns(
        (pl.col("female").fill_null(0) + pl.col("male").fill_null(0))
        .alias("TotalSurvived")
    )

    return pivot.select(["Pclass", "female", "male", "TotalSurvived"])


# =========================================================
# Punto 12 — Total NO supervivientes
# =========================================================

def e1_total_not_survived(df: pl.DataFrame) -> pl.DataFrame:
    return df.filter(pl.col("Survived") == 0).select(
        pl.len().alias("not_survived_total")
    )


# =========================================================
# Punto 13 — NO supervivientes por clase y sexo
# =========================================================

def e1_not_survived_by_class_sex(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df.filter(pl.col("Survived") == 0)
        .group_by(["Pclass", "Sex"])
        .agg(pl.len().alias("count"))
        .sort(["Pclass", "Sex"])
    )


# =========================================================
# Punto 14 — Supervivieron y NO (pivot)
# =========================================================

def e1_survived_not_pivot_by_class_sex(df: pl.DataFrame) -> pl.DataFrame:
    """
    (14) Número de pasajeros que sobrevivieron y que no sobrevivieron,
    agrupados por clase y sexo (pivot).
    """
    base = (
        df.group_by(["Pclass", "Sex", "Survived"])
        .agg(pl.len().alias("count"))
        .sort(["Pclass", "Sex", "Survived"])
    )

    pivot = (
        base.pivot(
            index=["Pclass", "Sex"],
            columns="Survived",
            values="count",
            aggregate_function="first",
        )
        .sort(["Pclass", "Sex"])
    )

    # Normalizar columnas 0 y 1
    if 0 not in pivot.columns:
        pivot = pivot.with_columns(pl.lit(0).alias(0))
    if 1 not in pivot.columns:
        pivot = pivot.with_columns(pl.lit(0).alias(1))

    pivot = pivot.with_columns(
        (pl.col(0).fill_null(0) + pl.col(1).fill_null(0)).alias("Total")
    )

    return (
        pivot.rename({0: "NotSurvived_0", 1: "Survived_1"})
        .select(["Pclass", "Sex", "NotSurvived_0", "Survived_1", "Total"])
    )


# =========================================================
# Punto 15 — Eliminar edades nulas
# =========================================================

def e1_dropna_age(df: pl.DataFrame) -> pl.DataFrame:
    return df.filter(pl.col("Age").is_not_null())


# =========================================================
# Punto 18 — Menores de 16
# =========================================================

def e1_add_is_minor(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        pl.when(pl.col("Age").is_null())
        .then(None)
        .otherwise(pl.col("Age") < 16)
        .alias("IsMinor16")
    )
