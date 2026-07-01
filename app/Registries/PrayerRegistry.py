"""Prayer registry — the central lookup for prayers."""

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from .BaseRegistry import BaseRegistry, normalize_key

if TYPE_CHECKING:
    from app.GameDefinitions.Prayer import Prayer


class PrayerRegistry(BaseRegistry):
    """Central registry for prayer definitions.

    Prayer modules register themselves at import time via ``register()``.
    Callers look up a ``Prayer`` instance by name or alias via ``get()``.
    """

    _aliases: dict[str, str] = {}
    _items: dict[str, "Prayer"] = {}

    @classmethod
    def register(cls, prayer: "Prayer"):
        key = normalize_key(prayer.name)
        cls._items[key] = prayer
        for alias in prayer.aliases:
            cls._add_alias(alias, key)

    @classmethod
    def get(cls, name: str) -> Optional["Prayer"]:
        """Return the Prayer for *name* (registered name or alias), or None."""
        key = cls._resolve_key(name)
        return cls._items.get(key)

    @classmethod
    def list_all(cls) -> list[str]:
        """Return registered names as originally spelled."""
        return [instance.name for instance in cls._items.values()]
