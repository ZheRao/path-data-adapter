from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict

@dataclass(frozen=True)
class csvReadConfig:
    encoding: str = "utf-8-sig"
    delimiter: str = ","
    dtype: Optional[Dict[str, str]] = None
    na_values: tuple[str, ...] = ("", "NA", "N/A", "null", "NULL")
    keep_default_na: bool = True
