"""Weapon registry — the central lookup for weapons."""

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from .BaseRegistry import BaseRegistry, normalize_key

if TYPE_CHECKING:
    from combat_engine.Domain.Weapon import Weapon


class WeaponRegistry(BaseRegistry):
    """Central registry for weapons.

    Weapon modules register themselves at import time via ``register()``.
    Callers look up a new ``Weapon`` instance by name or alias via ``get()``.
    """

    _aliases: dict[str, str] = {}
    _items: dict[str, type] = {}

    @classmethod
    def register(cls, weapon_class: type):
        instance = weapon_class()
        key = normalize_key(instance.name)
        cls._items[key] = weapon_class
        for alias in instance.aliases:
            cls._add_alias(alias, key)

    @classmethod
    def get(cls, name: str) -> Optional["Weapon"]:
        """Return a new Weapon instance for *name* (registered name or alias), or None."""
        key = cls._resolve_key(name)
        weapon_class = cls._items.get(key)
        if weapon_class is None:
            return None
        return weapon_class()

    @classmethod
    def list_all(cls) -> list[str]:
        """Return registered names as originally spelled."""
        result: list[str] = []
        for weapon_class in cls._items.values():
            instance = weapon_class()
            result.append(instance.name)
        return result


import combat_engine.Data.Definitions.Weapons  # noqa: F401, E402
