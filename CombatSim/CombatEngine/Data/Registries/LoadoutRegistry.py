"""Loadout registry — the central lookup for gear loadouts."""

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from .BaseRegistry import BaseRegistry, normalize_key

if TYPE_CHECKING:
    from CombatSim.CombatEngine.Domain.Loadout import Loadout


class LoadoutRegistry(BaseRegistry):
    """Central registry for gear loadouts.

    Loadout modules register themselves at import time via ``register()``.
    Callers look up a ``Loadout`` by name or alias via ``get()``.
    """

    _aliases: dict[str, str] = {}
    _items: dict[str, Loadout] = {}

    @classmethod
    def register(cls, loadout: Loadout):
        key = normalize_key(loadout.name)
        cls._items[key] = loadout
        for alias in loadout.aliases:
            cls._add_alias(alias, key)

    @classmethod
    def get(cls, name: str) -> Optional[Loadout]:
        """Return the Loadout for *name* (registered name or alias), or None."""
        key = cls._resolve_key(name)
        return cls._items.get(key)

    @classmethod
    def list_all(cls) -> list[str]:
        """Return registered names as originally spelled."""
        return [instance.name for instance in cls._items.values()]


import CombatSim.CombatEngine.Data.Definitions.Loadouts  # noqa: F401, E402
