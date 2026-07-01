"""Potion registry — the central lookup for potions / boost sources."""

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from .BaseRegistry import BaseRegistry, normalize_key

if TYPE_CHECKING:
    from app.GameDefinitions.Potion import Potion


class PotionRegistry(BaseRegistry):
    """Central registry for potion definitions.

    Potion modules register themselves at import time via ``register()``.
    Callers look up a ``Potion`` instance by name or alias via ``get()``.
    """

    _aliases: dict[str, str] = {}
    _items: dict[str, "Potion"] = {}

    @classmethod
    def register(cls, potion: "Potion"):
        key = normalize_key(potion.name)
        cls._items[key] = potion
        for alias in potion.aliases:
            cls._add_alias(alias, key)

    @classmethod
    def get(cls, name: str) -> Optional["Potion"]:
        """Return the Potion for *name* (registered name or alias), or None."""
        key = cls._resolve_key(name)
        return cls._items.get(key)

    @classmethod
    def list_all(cls) -> list[str]:
        """Return registered names as originally spelled."""
        return [instance.name for instance in cls._items.values()]
