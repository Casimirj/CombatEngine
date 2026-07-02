from .AmmoType import AmmoType
from .GearSlot import GearSlot


# ---------------------------------------------------------------------------
# Potion — backward-compatible namespace proxying to PotionRegistry.
# ``Potion.SUPER_COMBAT`` returns a registered Potion instance, iteration
# yields all registered potions, and ``Potion.compute_boost`` is available.
# On first access the underlying ``app.Data.Definitions.Potions`` package is
# imported so the registry is populated.
# ---------------------------------------------------------------------------
import math
from typing import Iterator


_POTIONS_LOADED = False


def _ensure_potions_registered():
    global _POTIONS_LOADED
    if not _POTIONS_LOADED:
        import app.Data.Definitions.Potions  # noqa: F401
        _POTIONS_LOADED = True


class _PotionMeta(type):
    def __iter__(cls) -> Iterator:
        _ensure_potions_registered()
        from app.Data.Registries.PotionRegistry import PotionRegistry
        return iter(list(PotionRegistry._items.values()))

    def __getattr__(cls, name: str):
        _ensure_potions_registered()
        from app.Data.Registries.PotionRegistry import PotionRegistry
        p = PotionRegistry.get(name)
        if p is not None:
            return p
        raise AttributeError(name)


class Potion(metaclass=_PotionMeta):
    @staticmethod
    def compute_boost(level: int, percentage: float, flat: int) -> int:
        if percentage >= 0:
            return math.floor(level * percentage) + flat
        else:
            return -math.floor(level * abs(percentage)) + flat

    def __init_subclass__(cls, **kwargs):
        raise TypeError("Potion is a namespace; do not subclass it")

    def __init__(self):
        raise TypeError("Potion is a namespace; do not instantiate it")


# ---------------------------------------------------------------------------
# Prayer — backward-compatible namespace proxying to PrayerRegistry.
# ``Prayer.PIETY`` returns a registered Prayer instance and iteration
# yields all registered prayers.
# ---------------------------------------------------------------------------
_PRAYERS_LOADED = False


def _ensure_prayers_registered():
    global _PRAYERS_LOADED
    if not _PRAYERS_LOADED:
        import app.Data.Definitions.Prayers  # noqa: F401
        _PRAYERS_LOADED = True


class _PrayerMeta(type):
    def __iter__(cls) -> Iterator:
        _ensure_prayers_registered()
        from app.Data.Registries.PrayerRegistry import PrayerRegistry
        return iter(list(PrayerRegistry._items.values()))

    def __getattr__(cls, name: str):
        _ensure_prayers_registered()
        from app.Data.Registries.PrayerRegistry import PrayerRegistry
        p = PrayerRegistry.get(name)
        if p is not None:
            return p
        raise AttributeError(name)


class Prayer(metaclass=_PrayerMeta):
    def __init_subclass__(cls, **kwargs):
        raise TypeError("Prayer is a namespace; do not subclass it")

    def __init__(self):
        raise TypeError("Prayer is a namespace; do not instantiate it")
