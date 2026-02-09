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
