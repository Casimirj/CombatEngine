from app.GearItem import Gear
from app.Enums.gear_slot import GearSlot
from app.Registries.GearRegistry import GearRegistry


class AmuletOfStrength(Gear):
    name = "Amulet of strength"
    slot = GearSlot.NECK
    aliases = ["strength amulet", "amulet of strength", "str amulet", "strength ammy"]

    def build(self) -> dict:
        return {
            "stab_attack_bonus":  0,
            "slash_attack_bonus":  0,
            "crush_attack_bonus":  0,
            "magic_attack_bonus":  0,
            "ranged_attack_bonus":  0,
            "melee_strength_bonus":  10,
            "ranged_strength_bonus":  0,
            "magic_strength_bonus":  0,
            "stab_def":  0,
            "slash_def":  0,
            "crush_def":  0,
            "magic_def":  0,
            "ranged_def_light":  0,
            "ranged_def_med":  0,
            "ranged_def_heavy":  0
        }


GearRegistry.register(AmuletOfStrength())
