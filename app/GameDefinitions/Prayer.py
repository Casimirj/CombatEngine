"""Prayer dataclass — the core prayer definition used by the PrayerRegistry."""

from __future__ import annotations

from typing import Optional


class Prayer:
    """A prayer with effect multipliers for each combat style.

    Melee / Ranged multipliers apply to the effective level calculation
    (multiplied then floored).  Magic damage bonuses are additive (e.g. 0.04
    = +4% added to the PrimaryMagicDamage phase).

    Attributes
    ----------
    name : str
        Canonical registry name.
    label : str
        Display name.
    aliases : list[str]
        Alternate lookup keys.
    attack_multiplier : float
        Melee.  0.0 = no effect.
    strength_multiplier : float
        Melee.  0.0 = no effect.
    defence_multiplier : float
        Melee & Ranged & Magic.  0.0 = no effect.
    ranged_attack_multiplier : float
        0.0 = no effect.
    ranged_strength_multiplier : float
        0.0 = no effect.
    magic_attack_multiplier : float
        0.0 = no effect.
    magic_damage_bonus : float
        Additive bonus during PrimaryMagicDamage.  0.0 = no effect.
    """

    def __init__(
        self,
        name: str,
        label: str,
        attack_multiplier: float = 0.0,
        strength_multiplier: float = 0.0,
        defence_multiplier: float = 0.0,
        ranged_attack_multiplier: float = 0.0,
        ranged_strength_multiplier: float = 0.0,
        magic_attack_multiplier: float = 0.0,
        magic_damage_bonus: float = 0.0,
        aliases: Optional[list[str]] = None,
    ):
        self.name = name
        self.label = label
        self.aliases = aliases or []
        self.attack_multiplier = attack_multiplier
        self.strength_multiplier = strength_multiplier
        self.defence_multiplier = defence_multiplier
        self.ranged_attack_multiplier = ranged_attack_multiplier
        self.ranged_strength_multiplier = ranged_strength_multiplier
        self.magic_attack_multiplier = magic_attack_multiplier
        self.magic_damage_bonus = magic_damage_bonus

    # Backward-compatible shorthand aliases
    @property
    def atk_mult(self) -> float:
        return self.attack_multiplier

    @property
    def str_mult(self) -> float:
        return self.strength_multiplier

    @property
    def def_mult(self) -> float:
        return self.defence_multiplier
