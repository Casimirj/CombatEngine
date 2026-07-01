from app.GearItem import Gear
from app.Enums.gear_slot import GearSlot
from app.Registries.GearRegistry import GearRegistry


class ZaryteVambraces(Gear):
    name = "Zaryte vambraces"
    slot = GearSlot.HANDS
    aliases = ["zaryte vambs", "zaryte vambraces", "zaryte gloves", "zvambs"]

    def build(self) -> dict:
        return {
            "stab_attack_bonus": -8,
            "slash_attack_bonus": -8,
            "crush_attack_bonus": -8,
            "magic_attack_bonus":  0,
            "ranged_attack_bonus":  18,
            "melee_strength_bonus":  0,
            "ranged_strength_bonus":  2,
            "magic_strength_bonus":  0,
            "stab_def":  8,
            "slash_def":  8,
            "crush_def":  8,
            "magic_def":  5,
            "ranged_def_light":  8,
            "ranged_def_med":  8,
            "ranged_def_heavy":  8
        }


GearRegistry.register(ZaryteVambraces())
