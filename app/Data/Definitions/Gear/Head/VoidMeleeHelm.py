from app.Domain.GearItem import Gear
from app.Domain.Enums.GearSlot import GearSlot
from app.Data.Registries.GearRegistry import GearRegistry


class VoidMeleeHelm(Gear):
    name = "Void melee helm"
    slot = GearSlot.HEAD
    aliases = ["void melee helm"]

    def build(self) -> dict:
        return {
            "stab_attack_bonus":  0,
            "slash_attack_bonus":  0,
            "crush_attack_bonus":  0,
            "magic_attack_bonus":  0,
            "ranged_attack_bonus":  0,
            "melee_strength_bonus":  0,
            "ranged_strength_bonus":  0,
            "magic_strength_bonus":  0,
            "stab_def":  6,
            "slash_def":  6,
            "crush_def":  6,
            "magic_def":  6,
            "ranged_def_light":  6,
            "ranged_def_med":  6,
            "ranged_def_heavy":  6
        }


GearRegistry.register(VoidMeleeHelm())
