from __future__ import annotations

from pathlib import Path
import numpy as np
import polars as pl
import matplotlib.pyplot as plt


def _save(figpath: Path) -> None:
    figpath.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(figpath, dpi=160)
    plt.close()


def bar_counts(df_counts: pl.DataFrame, x_col: str, y_col: str, title: str, figpath: Path) -> None:
    x = df_counts[x_col].to_list()
    y = df_counts[y_col].to_list()

    plt.figure()
    plt.bar(x, y)
    plt.title(title)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    _save(figpath)


def bar_counts_hue(
    df_counts: pl.DataFrame,
    x_col: str,
    hue_col: str,
    y_col: str,
    title: str,
    figpath: Path,
) -> None:
    # barras agrupadas (x = clase, hue = sexo, etc.)
    xs = df_counts[x_col].unique().to_list()
    hues = df_counts[hue_col].unique().to_list()

    # ordenar para que quede bonito
    try:
        xs = sorted(xs)
    except Exception:
        xs = sorted(xs, key=str)
    hues = sorted(hues, key=str)

    # pivot a matriz (filas xs, columnas hues)
    pivot = (
        df_counts.pivot(index=x_col, columns=hue_col, values=y_col, aggregate_function="first")
        .sort(x_col)
    )
    x_vals = pivot[x_col].to_list()
    width = 0.8 / max(1, len(hues))
    base = np.arange(len(x_vals))

    plt.figure()
    for i, h in enumerate(hues):
        if h in pivot.columns:
            y = pivot[h].fill_null(0).to_numpy()
        else:
            y = np.zeros(len(x_vals))
        plt.bar(base + i * width, y, width=width, label=str(h))

    plt.xticks(base + width * (len(hues) - 1) / 2, [str(v) for v in x_vals])
    plt.title(title)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.legend(title=hue_col)
    _save(figpath)


def survived_vs_not(df: pl.DataFrame, figpath: Path) -> None:
    counts = df.group_by("Survived").agg(pl.len().alias("count")).sort("Survived")
    x = [("No" if v == 0 else "Sí") for v in counts["Survived"].to_list()]
    y = counts["count"].to_list()

    plt.figure()
    plt.bar(x, y)
    plt.title("Supervivieron vs No sobrevivieron")
    plt.xlabel("Survived")
    plt.ylabel("count")
    _save(figpath)


def age_hist_with_kde(df: pl.DataFrame, figpath: Path) -> None:
    # Q15 pide eliminar nulos en Age para distribuciones
    ages = df.select(pl.col("Age").drop_nulls()).to_series().to_numpy()
    ages = ages[~np.isnan(ages)]

    plt.figure()
    plt.hist(ages, bins=30, density=True)
    plt.title("Distribución de edad (histograma + densidad)")
    plt.xlabel("Age")
    plt.ylabel("density")

    # KDE simple con scipy si está
    try:
        from scipy.stats import gaussian_kde

        kde = gaussian_kde(ages)
        xs = np.linspace(ages.min(), ages.max(), 200)
        plt.plot(xs, kde(xs))
    except Exception:
        pass

    _save(figpath)


def age_hist_alt(df: pl.DataFrame, figpath: Path) -> None:
    ages = df.select(pl.col("Age").drop_nulls()).to_series().to_numpy()
    ages = ages[~np.isnan(ages)]

    plt.figure()
    plt.hist(ages, bins=20)
    plt.title("Histograma de edades (alternativo)")
    plt.xlabel("Age")
    plt.ylabel("count")
    _save(figpath)
