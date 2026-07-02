from app.Domain.GearItem import Gear
from app.Domain.Enums.GearSlot import GearSlot
from app.Data.Registries.GearRegistry import GearRegistry


class DragonBoots(Gear):
    name = "Dragon boots"
    slot = GearSlot.BOOTS
    aliases = ["dragon boots", "d boots", "dboots"]

    def build(self) -> dict:
        return {
            "stab_attack_bonus":  0,
            "slash_attack_bonus":  0,
            "crush_attack_bonus":  0,
            "magic_attack_bonus": -3,
            "ranged_attack_bonus": -1,
            "melee_strength_bonus":  4,
            "ranged_strength_bonus":  0,
            "magic_strength_bonus":  0,
            "stab_def":  16,
            "slash_def":  17,
            "crush_def":  18,
            "magic_def":  0,
            "ranged_def_light":  0,
            "ranged_def_med":  0,
            "ranged_def_heavy":  0
        }


GearRegistry.register(DragonBoots())
