from __future__ import annotations

from pathlib import Path
import polars as pl


def save_table(df: pl.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.write_csv(path)


def save_text(lines: list[str], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
