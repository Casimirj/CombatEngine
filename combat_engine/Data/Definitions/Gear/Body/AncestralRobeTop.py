from combat_engine.Domain.GearItem import Gear
from combat_engine.Domain.Enums.GearSlot import GearSlot
from combat_engine.Data.Registries.GearRegistry import GearRegistry


class AncestralRobeTop(Gear):
    name = "Ancestral robe top"
    slot = GearSlot.BODY
    aliases = ["ancestral top", "ancestral body", "ances top", "ances body"]

    def build(self) -> dict:
        return {
            "stab_attack_bonus":  0,
            "slash_attack_bonus":  0,
            "crush_attack_bonus":  0,
            "magic_attack_bonus":  35,
            "ranged_attack_bonus": -8,
            "melee_strength_bonus":  0,
            "ranged_strength_bonus":  0,
            "magic_strength_bonus":  3,
            "stab_def":  42,
            "slash_def":  31,
            "crush_def":  51,
            "magic_def":  28,
            "ranged_def_light":  0,
            "ranged_def_med":  0,
            "ranged_def_heavy":  0
        }


GearRegistry.register(AncestralRobeTop())
