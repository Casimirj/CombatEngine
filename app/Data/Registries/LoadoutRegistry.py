"""Loadout registry — the central lookup for gear loadouts."""

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from app.Domain.Player import Player

from .BaseRegistry import BaseRegistry, normalize_key

if TYPE_CHECKING:
    from app.Domain.Loadout import Loadout


class LoadoutRegistry(BaseRegistry):
    """Central registry for gear loadouts.

    Loadout modules register themselves at import time via ``register()``.
    Callers look up a ``Player`` by name or alias via ``get()``.
    """

    _built_players: dict[str, Player] = {}
    _aliases: dict[str, str] = {}
    _items: dict[str, Loadout] = {}

    @classmethod
    def register(cls, loadout: Loadout):
        key = normalize_key(loadout.name)
        cls._items[key] = loadout
        for alias in loadout.aliases:
            cls._add_alias(alias, key)

    @classmethod
    def get(cls, name: str) -> Optional[Player]:
        """Return a built Player for *name* (registered name or alias), or None."""
        key = cls._resolve_key(name)
        instance = cls._items.get(key)
        if instance is None:
            return None
        if key not in cls._built_players:
            cls._built_players[key] = instance.build()
        return cls._built_players[key]

    @classmethod
    def list_all(cls) -> list[str]:
        """Return registered names as originally spelled."""
        return [instance.name for instance in cls._items.values()]


import app.Data.Definitions.Loadouts  # noqa: F401, E402
