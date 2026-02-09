from __future__ import annotations

from pathlib import Path
import polars as pl


PORT_MAP = {
    "C": "Cherbourg",
    "Q": "Queenstown",
    "S": "Southampton",
}


def load_pasajeros(data_dir: Path) -> pl.DataFrame:
    return pl.read_csv(data_dir / "pasajeros.csv")


def load_supervivientes(data_dir: Path) -> pl.DataFrame:
    return pl.read_csv(data_dir / "supervivientes.csv")


def build_df(data_dir: Path) -> pl.DataFrame:
    # Enunciado: inner join por PassengerId
    df_p = load_pasajeros(data_dir)
    df_s = load_supervivientes(data_dir)

    # Normalizar tipo PassengerId por si acaso
    df_p = df_p.with_columns(pl.col("PassengerId").cast(pl.Int64))
    df_s = df_s.with_columns(pl.col("PassengerId").cast(pl.Int64))

    df = df_p.join(df_s, on="PassengerId", how="inner")
    return df


def add_puerto(df: pl.DataFrame) -> pl.DataFrame:
    # (1) nueva columna puerto con nombre
    return df.with_columns(
        pl.col("Embarked")
        .replace(PORT_MAP, default=None)
        .alias("puerto")
    )


def passengers_by_puerto(df: pl.DataFrame) -> pl.DataFrame:
    # (2) nº pasajeros por puerto
    return df.group_by("puerto").agg(pl.len().alias("count")).sort("puerto")


def passengers_by_sex(df: pl.DataFrame) -> pl.DataFrame:
    # (3) cuántos hombres y mujeres embarcaron
    return df.group_by("Sex").agg(pl.len().alias("count")).sort("Sex")


def mean_age_by_sex_survived(df: pl.DataFrame) -> pl.DataFrame:
    # (4) edad media H/M que sobrevivieron y murieron
    return (
        df.group_by(["Sex", "Survived"])
        .agg(pl.col("Age").mean().alias("mean_age"))
        .sort(["Sex", "Survived"])
    )


def add_age_range(df: pl.DataFrame) -> pl.DataFrame:
    # (5) rango edad: <18 joven, 18-65 adulto, >65 anciano
    return df.with_columns(
        pl.when(pl.col("Age").is_null())
        .then(None)
        .when(pl.col("Age") < 18)
        .then(pl.lit("joven"))
        .when(pl.col("Age") <= 65)
        .then(pl.lit("adulto"))
        .otherwise(pl.lit("anciano"))
        .alias("rango_edad")
    )


def deaths_by_age_range(df: pl.DataFrame) -> pl.DataFrame:
    # (5) muertos por rango edad
    dfr = add_age_range(df)
    return (
        dfr.filter(pl.col("Survived") == 0)
        .group_by("rango_edad")
        .agg(pl.len().alias("count"))
        .sort("rango_edad")
    )


def deaths_by_class_gender(df: pl.DataFrame) -> pl.DataFrame:
    # (6) muertos por clase y genero
    return (
        df.filter(pl.col("Survived") == 0)
        .group_by(["Pclass", "Sex"])
        .agg(pl.len().alias("count"))
        .sort(["Pclass", "Sex"])
    )


def survived_and_deaths_by_puerto(df: pl.DataFrame) -> pl.DataFrame:
    # (7) muertos y supervivientes por ciudad/puerto de origen
    # (lo interpretamos como puerto de embarque: 'puerto')
    return (
        df.group_by(["puerto", "Survived"])
        .agg(pl.len().alias("count"))
        .sort(["puerto", "Survived"])
    )


def join_quality(df_p: pl.DataFrame, df_s: pl.DataFrame, df_joined: pl.DataFrame) -> pl.DataFrame:
    # Tabla de diagnóstico: tamaños y PassengerId no emparejados
    p_ids = df_p.select("PassengerId").unique()
    s_ids = df_s.select("PassengerId").unique()
    j_ids = df_joined.select("PassengerId").unique()

    only_p = p_ids.join(s_ids, on="PassengerId", how="anti")
    only_s = s_ids.join(p_ids, on="PassengerId", how="anti")

    return pl.DataFrame(
        {
            "pasajeros_rows": [df_p.height],
            "supervivientes_rows": [df_s.height],
            "joined_rows": [df_joined.height],
            "pasajeros_only_ids": [only_p.height],
            "supervivientes_only_ids": [only_s.height],
        }
    )
