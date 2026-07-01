from typing import Optional

from app.Player import Player
from app.Stats import Stats
from app.Exceptions.InvalidLoadoutException import InvalidLoadoutException
from app.Registries.GearRegistry import GearRegistry
from app.Loadout import Loadout


_DEFAULT_LEVELS = Stats({
    "hp_level": 99,
    "attack_level": 99,
    "strength_level": 99,
    "def_level": 99,
    "magic_level": 99,
    "ranged_level": 99,
    "prayer_level": 99,
})

_LEVEL_KEYS = {
    "hp_level", "attack_level", "strength_level", "def_level",
    "magic_level", "ranged_level", "prayer_level",
}

# Gear names that compose a complete void set
_VOID_BODY   = "Elite void top"
_VOID_LEGS   = "Elite void robe"
_VOID_GLOVES = "Void knight gloves"

# Void helms and their corresponding combat style
_VOID_HELMS = {
    "Void ranger helm": "ranged",
    "Void mage helm":   "mage",
    "Void melee helm":  "melee",
}


class Custom(Loadout):
    """Loadout built from named gear items.

    Construct with a list of gear names and optional player levels, then
    call ``build()``. If no levels are given, all combat stats default to 99::

        player = Custom(gear_names=["Salve (e)"]).build()
    """

    name = "Custom"
    aliases = ["custom loadout"]

    def __init__(self, gear_names: list[str], player_levels: Optional[Stats] = None):
        self.gear_names = gear_names
        self.player_levels = player_levels

    def build(self) -> Player:
        combined_stats: dict = {}
        combined_player_kwargs: dict = {}
        occupied_slots: dict = {}

        for gear_name in self.gear_names:
            gear = GearRegistry.get(gear_name)
            if gear is None:
                raise KeyError(f"Unknown gear: {gear_name}")

            if gear.slot in occupied_slots:
                raise InvalidLoadoutException(
                    f"Slot conflict: '{gear.name}' and '{occupied_slots[gear.slot]}' "
                    f"both occupy the {gear.slot.name.lower()} slot."
                )

            occupied_slots[gear.slot] = gear.name

            for key, value in gear.build().items():
                combined_stats[key] = combined_stats.get(key, 0) + value

            combined_player_kwargs.update(gear.player_kwargs)

        levels = self.player_levels if self.player_levels is not None else _DEFAULT_LEVELS
        level_dict = {k: v for k, v in vars(levels).items() if k in _LEVEL_KEYS}
        combined_stats.update(level_dict)

        # Detect complete void set
        void_style = self._detect_void_set(occupied_slots)
        if void_style:
            combined_player_kwargs["wearing_void"] = True
            combined_player_kwargs["void_style"] = void_style
        else:
            combined_player_kwargs["wearing_void"] = False
            combined_player_kwargs["void_style"] = None

        return Player(stats=combined_stats, **combined_player_kwargs)

    def _detect_void_set(self, occupied_slots: dict) -> Optional[str]:
        """Return the void combat style if a complete void set is equipped, else None.

        A complete elite void set requires all four pieces:
        - Body:  EliteVoidTop
        - Legs:  EliteVoidRobe
        - Hands: VoidKnightGloves
        - Head:  one of VoidRangerHelm / VoidMageHelm / VoidMeleeHelm
        """
        from app.Enums.gear_slot import GearSlot

        helm_name = occupied_slots.get(GearSlot.HEAD, "")
        if helm_name not in _VOID_HELMS:
            return None
        if occupied_slots.get(GearSlot.BODY) != _VOID_BODY:
            return None
        if occupied_slots.get(GearSlot.LEGS) != _VOID_LEGS:
            return None
        if occupied_slots.get(GearSlot.HANDS) != _VOID_GLOVES:
            return None

        return _VOID_HELMS[helm_name]
