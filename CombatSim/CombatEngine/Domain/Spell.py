"""Spell dataclass — the core spell definition used by the SpellRegistry."""

from __future__ import annotations

from typing import Optional


class Spell:
    """A combat spell with its base max hit and properties.

    Attributes
    ----------
    name : str
        Canonical registry name.
    label : str
        Display name.
    aliases : list[str]
        Alternate lookup keys.
    base_max : int
        The spell's base maximum damage (before gear/prayer multipliers).
    """

    def __init__(
        self,
        name: str,
        label: str,
        base_max: int,
        aliases: Optional[list[str]] = None,
    ):
        self.name = name
        self.label = label
        self.base_max = base_max
        self.aliases = aliases or []
