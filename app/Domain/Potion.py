"""Potion dataclass — the core potion definition used by the PotionRegistry."""

from __future__ import annotations

import math
from typing import Optional


class Potion:
    """A potion (or other boost source) with its stat-boost formulas.

    Each boost is calculated as ``floor(level × percentage) + flat``.
    Negative percentages reduce the stat.

    Attributes
    ----------
    name : str
        Canonical registry name.
    label : str
        Display name.
    aliases : list[str]
        Alternate lookup keys.
    attack_percentage : float
        Percentage of base Attack level added as a boost.
    attack_flat : int
        Flat Attack boost added after the percentage.
    strength_percentage : float
        Percentage of base Strength level added as a boost.
    strength_flat : int
        Flat Strength boost added after the percentage.
    defence_percentage : float
        Percentage of base Defence level added as a boost.
    defence_flat : int
        Flat Defence boost added after the percentage.
    ranged_percentage : float
        Percentage of base Ranged level added as a boost.
    ranged_flat : int
        Flat Ranged boost added after the percentage.
    magic_percentage : float
        Percentage of base Magic level added as a boost.
    magic_flat : int
        Flat Magic boost added after the percentage.
    """

    def __init__(
        self,
        name: str,
        label: str,
        attack_percentage: float = 0.0,
        attack_flat: int = 0,
        strength_percentage: float = 0.0,
        strength_flat: int = 0,
        defence_percentage: float = 0.0,
        defence_flat: int = 0,
        ranged_percentage: float = 0.0,
        ranged_flat: int = 0,
        magic_percentage: float = 0.0,
        magic_flat: int = 0,
        aliases: Optional[list[str]] = None,
    ):
        self.name = name
        self.label = label
        self.aliases = aliases or []
        self.attack_percentage = attack_percentage
        self.attack_flat = attack_flat
        self.strength_percentage = strength_percentage
        self.strength_flat = strength_flat
        self.defence_percentage = defence_percentage
        self.defence_flat = defence_flat
        self.ranged_percentage = ranged_percentage
        self.ranged_flat = ranged_flat
        self.magic_percentage = magic_percentage
        self.magic_flat = magic_flat

    @staticmethod
    def compute_boost(level: int, percentage: float, flat: int) -> int:
        """Compute the boost value for a given level.

        ``floor(level × percentage) + flat`` for positive percentages;
        ``-(floor(level × |percentage|)) + flat`` for negative.
        """
        if percentage >= 0:
            return math.floor(level * percentage) + flat
        else:
            return -math.floor(level * abs(percentage)) + flat
