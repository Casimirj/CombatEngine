"""Base registry with key normalization."""

from __future__ import annotations

import re
from typing import Optional


_NORMALIZE_RE = re.compile(r"[ _-]+")


def normalize_key(name: str) -> str:
    """Normalize a lookup key by stripping spaces, underscores, and hyphens."""
    return _NORMALIZE_RE.sub("", name).lower()


class BaseRegistry:
    """Base class for registries with alias resolution.

    Subclasses store items in ``_items`` keyed by normalized registered name,
    and aliases in ``_aliases`` mapping normalized alias → normalized name.
    """

    _aliases: dict[str, str] = {}
    _items: dict[str, object] = {}

    @classmethod
    def _add_alias(cls, alias: str, registered_key: str):
        cls._aliases[normalize_key(alias)] = registered_key

    @classmethod
    def _resolve_key(cls, name: str) -> str:
        key = normalize_key(name)
        return cls._aliases.get(key, key)

    @classmethod
    def get_by_key(cls, key: str) -> Optional[object]:
        return cls._items.get(key)
