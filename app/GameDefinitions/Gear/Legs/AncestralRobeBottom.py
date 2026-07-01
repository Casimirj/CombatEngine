from app.GearItem import Gear
from app.Enums.gear_slot import GearSlot
from app.Registries.GearRegistry import GearRegistry


class AncestralRobeBottom(Gear):
    name = "Ancestral robe bottom"
    slot = GearSlot.LEGS
    aliases = ["ancestral bottom", "ancestral legs", "ances bottom", "ances legs", "ancestral robe bottom"]

    def build(self) -> dict:
        return {
            "stab_attack_bonus":  0,
            "slash_attack_bonus":  0,
            "crush_attack_bonus":  0,
            "magic_attack_bonus":  26,
            "ranged_attack_bonus": -7,
            "melee_strength_bonus":  0,
            "ranged_strength_bonus":  0,
            "magic_strength_bonus":  3,
            "stab_def":  27,
            "slash_def":  24,
            "crush_def":  30,
            "magic_def":  20,
            "ranged_def_light":  0,
            "ranged_def_med":  0,
            "ranged_def_heavy":  0
        }


GearRegistry.register(AncestralRobeBottom())
