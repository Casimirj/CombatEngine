"""Gear registry — the central lookup for gear items."""

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from .BaseRegistry import BaseRegistry, normalize_key

if TYPE_CHECKING:
    from CombatSim.CombatEngine.Domain.GearItem import Gear


class GearRegistry(BaseRegistry):
    """Central registry for gear items.

    Gear modules register themselves at import time via ``register()``.
    Callers look up a ``Gear`` instance by name or alias via ``get()``.
    """

    _aliases: dict[str, str] = {}
    _items: dict[str, Gear] = {}

    @classmethod
    def register(cls, gear: Gear):
        key = normalize_key(gear.name)
        cls._items[key] = gear
        for alias in gear.aliases:
            cls._add_alias(alias, key)

    @classmethod
    def get(cls, name: str) -> Optional[Gear]:
        """Return the Gear for *name* (registered name or alias), or None."""
        key = cls._resolve_key(name)
        return cls._items.get(key)

    @classmethod
    def list_all(cls) -> list[str]:
        """Return registered names as originally spelled."""
        return [instance.name for instance in cls._items.values()]


import CombatSim.CombatEngine.Data.Definitions.Gear  # noqa: F401, E402
