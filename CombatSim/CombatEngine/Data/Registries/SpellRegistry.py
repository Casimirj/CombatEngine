"""Spell registry — the central lookup for spell definitions."""

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from .BaseRegistry import BaseRegistry, normalize_key

if TYPE_CHECKING:
    from CombatSim.CombatEngine.Domain.Spell import Spell


class SpellRegistry(BaseRegistry):
    """Central registry for spell definitions.

    Spell modules register themselves at import time via ``register()``.
    Callers look up a ``Spell`` instance by name or alias via ``get()``.
    """

    _aliases: dict[str, str] = {}
    _items: dict[str, "Spell"] = {}

    @classmethod
    def register(cls, spell: "Spell"):
        key = normalize_key(spell.name)
        cls._items[key] = spell
        for alias in spell.aliases:
            cls._add_alias(alias, key)

    @classmethod
    def get(cls, name: str) -> Optional["Spell"]:
        """Return the Spell for *name* (registered name or alias), or None."""
        key = cls._resolve_key(name)
        return cls._items.get(key)

    @classmethod
    def list_all(cls) -> list[str]:
        """Return registered names as originally spelled."""
        return [instance.name for instance in cls._items.values()]


import CombatSim.CombatEngine.Data.Definitions.Spells  # noqa: F401, E402
