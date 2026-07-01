from app.GearItem import Gear
from app.Enums.gear_slot import GearSlot
from app.Registries.GearRegistry import GearRegistry


class MasoriMask(Gear):
    name = "Masori mask"
    slot = GearSlot.HEAD
    aliases = ["masori helm", "masori helmet", "masori head"]

    def build(self) -> dict:
        return {
            "stab_attack_bonus":  0,
            "slash_attack_bonus":  0,
            "crush_attack_bonus":  0,
            "magic_attack_bonus": -1,
            "ranged_attack_bonus":  12,
            "melee_strength_bonus":  0,
            "ranged_strength_bonus":  2,
            "magic_strength_bonus":  0,
            "stab_def":  3,
            "slash_def":  4,
            "crush_def":  3,
            "magic_def":  6,
            "ranged_def_light":  4,
            "ranged_def_med":  4,
            "ranged_def_heavy":  4
        }


GearRegistry.register(MasoriMask())
