from __future__ import annotations

from pathlib import Path
import polars as pl


def load_titanic(data_dir: Path) -> pl.DataFrame:
    return pl.read_csv(data_dir / "titanic.csv")


def e1_head(df: pl.DataFrame, n: int = 5) -> pl.DataFrame:
    return df.head(n)


def e1_columns(df: pl.DataFrame) -> list[str]:
    return df.columns


def e1_info(df: pl.DataFrame) -> pl.DataFrame:
    # En Polars, el "info" tipo pandas lo aproximamos con schema + nulos
    schema = pl.DataFrame(
        {"column": df.columns, "dtype": [str(df.schema[c]) for c in df.columns]}
    )
    nulls = df.null_count().transpose(include_header=True, header_name="column", column_names=["nulls"])
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


def e1_survived_by_class_sex(df: pl.DataFrame) -> pl.DataFrame:
    # sobrevivientes por clase y sexo + totales por clase/sexo incluidos como columnas
    grouped = (
        df.group_by(["Pclass", "Sex", "Survived"])
        .agg(pl.len().alias("count"))
        .sort(["Pclass", "Sex", "Survived"])
    )
    return grouped

def e1_counts_for_class_plot(df: pl.DataFrame) -> pl.DataFrame:
    # para plot #5
    return e1_passengers_by_class(df)

def e1_counts_for_sex_plot(df: pl.DataFrame) -> pl.DataFrame:
    # para plot #7
    return e1_passengers_by_sex(df)

def e1_counts_for_sex_class_plot(df: pl.DataFrame) -> pl.DataFrame:
    # para plot #9 (sexo + clase)
    return e1_sex_by_class(df)

import polars as pl


def e1_total_not_survived(df: pl.DataFrame) -> pl.DataFrame:
    # (12) número total de pasajeros que NO sobrevivieron
    return df.filter(pl.col("Survived") == 0).select(pl.len().alias("not_survived_total"))


def e1_not_survived_by_class_sex(df: pl.DataFrame) -> pl.DataFrame:
    # (13) no sobrevivieron por clase y sexo
    return (
        df.filter(pl.col("Survived") == 0)
        .group_by(["Pclass", "Sex"])
        .agg(pl.len().alias("count"))
        .sort(["Pclass", "Sex"])
    )


def e1_survived_and_not_by_class_sex(df: pl.DataFrame) -> pl.DataFrame:
    # (14) sobrevivieron y no sobrevivieron agrupados por clase y sexo
    # devuelve tabla con columnas: Pclass, Sex, Survived, count
    return (
        df.group_by(["Pclass", "Sex", "Survived"])
        .agg(pl.len().alias("count"))
        .sort(["Pclass", "Sex", "Survived"])
    )


def e1_add_is_minor(df: pl.DataFrame) -> pl.DataFrame:
    # (18) función menores de 16 -> creamos columna booleana
    # Nota: Age puede ser null
    return df.with_columns(
        pl.when(pl.col("Age").is_null())
        .then(None)
        .otherwise(pl.col("Age") < 16)
        .alias("IsMinor16")
    )

def e1_dropna_age(df: pl.DataFrame) -> pl.DataFrame:
    # (15) eliminar registros con edad nula
    return df.filter(pl.col("Age").is_not_null())
