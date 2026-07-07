"""Monster registry — the central lookup for monsters."""

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from .BaseRegistry import BaseRegistry, normalize_key

if TYPE_CHECKING:
    from combat_engine.Domain.Monster import Monster


class MonsterRegistry(BaseRegistry):
    """Central registry for monsters.

    Monster modules register themselves at import time via ``register()``.
    Callers look up a new ``Monster`` instance by name or alias via ``get()``.
    Registration derives the registered name from the class name.
    """

    _aliases: dict[str, str] = {}
    _items: dict[str, type] = {}

    @classmethod
    def register(cls, monster_class: type):
        instance = monster_class()
        key = normalize_key(monster_class.__name__)
        cls._items[key] = monster_class
        for alias in instance.aliases:
            cls._add_alias(alias, key)

    @classmethod
    def get(cls, name: str, scale: int = 1) -> Optional["Monster"]:
        """Return a new Monster instance for *name* (registered name or alias), or None."""
        key = cls._resolve_key(name)
        monster_class = cls._items.get(key)
        if monster_class is None:
            return None
        return monster_class(scale=scale)

    @classmethod
    def list_all(cls) -> list[str]:
        """Return registered names as originally spelled."""
        return [cls.__name__ for cls in cls._items.values()]


import combat_engine.Data.Definitions.Monsters  # noqa: F401, E402
