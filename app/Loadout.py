from typing import Optional

from app.Player import Player
from app.Stats import Stats

_DEFAULT_LEVELS = Stats({
    "hp_level": 99,
    "attack_level": 99,
    "strength_level": 99,
    "def_level": 99,
    "magic_level": 99,
    "ranged_level": 99,
    "prayer_level": 99,
})

_UNSET = object()

class Loadout:
    """A gear loadout.

    Can be used directly by passing ``gear_names`` and optional
    ``player_levels``, or subclassed with a custom ``build()``.

    Direct usage (default gear-composition builder)::

        Loadout(gear_names=["Salve (e)"]).build()

    Subclass usage (hardcoded stats)::

        class MyLoadout(Loadout):
            name = "My Loadout"
            def build(self) -> Player:
                return Player(stats={"hp_level": 99, ...})
    """

    name: str = "Loadout"
    aliases: list[str] = []

    def __init__(
        self,
        gear_names: Optional[list[str]] = None,
        player_levels: Optional[Stats] = None,
        *,
        name: object = _UNSET,
        aliases: Optional[list[str]] = None,
    ):
        self.gear_names = gear_names
        self.player_levels = player_levels
        if name is not _UNSET:
            self.name = name
        if aliases is not None:
            self.aliases = aliases

    def build(self) -> Player:
        """Build a Player. Subclasses may override; the default composes gear."""
        if self.gear_names is None:
            raise NotImplementedError(
                "Subclass must override build() or provide gear_names"
            )

        levels = self.player_levels if self.player_levels is not None else _DEFAULT_LEVELS
        level_dict = {k: v for k, v in vars(levels).items() if k in Stats.LEVEL_KEYS}

        return Player(stats=level_dict, loadout=self)
