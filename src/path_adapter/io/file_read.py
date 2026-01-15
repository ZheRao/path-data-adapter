from __future__ import annotations
from pathlib import Path
from typing import Optional
import pandas as pd
import datetime as dt
from importlib.resources import files
import json

from path_adapter.common.config import csvReadConfig

def read_configs(config_type:str, name:str) -> dict:
    """
    Reads and return configurations stored in json_configs/config_type/name, e.g., json_configs/io/path.win.json
    """
    p = files("path_adapter.json_configs").joinpath(f"{config_type}/{name}")
    return json.loads(p.read_text())

def _read_csv_from_path(csv_path: Path, 
                        cfg: csvReadConfig) -> pd.DataFrame:
    """
    Pure I/O boundary: reads CSV from a path and returns a DataFrame.
    No business logic, no column renames (keep it plain).
    """
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    df = pd.read_csv(
            csv_path,
            encoding=cfg.encoding,
            sep=cfg.delimiter,
            dtype=cfg.dtype,
            na_values=list(cfg.na_values),
            keep_default_na=cfg.keep_default_na,
            low_memory=False)

    return df

def _make_filename(prefix:str, d: dt.date) -> str:
    """ 
    compose the file name with dates
    """
    return f"{prefix}-{d.year}-{d.month}-{d.day}.csv"

def read_data(csv_dir: Path,
              cfg: csvReadConfig,
              prefix:str = "zheSO",
              today:dt = None) -> pd.DataFrame:
    """
    Implement one-day fallback of file reads (if today's file doesn't exist, it reads yesterday's file as failsafe)
    For now, it prints which route it took
    """
    if not today:
        today = dt.datetime.today()
    # safeguard accidental passing csv_dir as string
    if isinstance(csv_dir, str): csv_dir = Path(csv_dir)
    candidates = [csv_dir/_make_filename(prefix, today),
                  csv_dir/_make_filename(prefix, today - dt.timedelta(days=1))]
    for p in candidates:
        try:
            df = _read_csv_from_path(p, cfg)
            print(f"Reading PATH file: {p.name}")   # swap to logger later
            return df 
        except FileNotFoundError:
            continue 
    
    raise FileNotFoundError(
        f"No PATH CSV found for {prefix}. Tried: " + ", ".join(str(p) for p in candidates)
    )
        
