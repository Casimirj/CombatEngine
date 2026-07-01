"""Gear package."""

from app.GearItem import Gear                   # noqa: F401
from app.GearRegistry import GearRegistry  # noqa: F401

# Import gear modules so they self‑register
from . import Salve  # noqa: F401


__all__ = [
    "Gear",
    "GearRegistry",
    "Salve",
]
