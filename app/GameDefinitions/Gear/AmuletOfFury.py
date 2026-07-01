from app.GearItem import Gear
from app.Enums.gear_slot import GearSlot
from app.Registries.GearRegistry import GearRegistry


class AmuletOfFury(Gear):
    name = "Amulet of fury"
    slot = GearSlot.NECK
    aliases = ["fury", "fury amulet", "amulet of fury"]

    def build(self) -> dict:
        return {
            "stab_attack_bonus":  10,
            "slash_attack_bonus":  10,
            "crush_attack_bonus":  10,
            "magic_attack_bonus":  10,
            "ranged_attack_bonus":  10,
            "melee_strength_bonus":  8,
            "ranged_strength_bonus":  0,
            "magic_strength_bonus":  0,
            "stab_def":  15,
            "slash_def":  15,
            "crush_def":  15,
            "magic_def":  15,
            "ranged_def_light":  15,
            "ranged_def_med":  15,
            "ranged_def_heavy":  15
        }


GearRegistry.register(AmuletOfFury())
