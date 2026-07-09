from CombatSim.CombatEngine.Domain.GearItem import Gear
from CombatSim.CombatEngine.Domain.Enums.GearSlot import GearSlot
from CombatSim.CombatEngine.Data.Registries.GearRegistry import GearRegistry


class AncestralHat(Gear):
    name = "Ancestral hat"
    slot = GearSlot.HEAD
    aliases = ["ancestral helm", "ancestral helmet", "ances hat"]

    def build(self) -> dict:
        return {
            "stab_attack_bonus":  0,
            "slash_attack_bonus":  0,
            "crush_attack_bonus":  0,
            "magic_attack_bonus":  8,
            "ranged_attack_bonus": -2,
            "melee_strength_bonus":  0,
            "ranged_strength_bonus":  0,
            "magic_strength_bonus":  3,
            "stab_def":  12,
            "slash_def":  11,
            "crush_def":  13,
            "magic_def":  5,
            "ranged_def_light":  0,
            "ranged_def_med":  0,
            "ranged_def_heavy":  0
        }


GearRegistry.register(AncestralHat())
