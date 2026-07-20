from CombatSim.CombatEngine.Domain.GearItem import Gear
from CombatSim.CombatEngine.Domain.Enums.GearSlot import GearSlot
from CombatSim.CombatEngine.Data.Registries.GearRegistry import GearRegistry


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
            "stab_def":  8,
            "slash_def":  10,
            "crush_def":  12,
            "magic_def":  12,
            "ranged_def_light":  9,
            "ranged_def_med":  9,
            "ranged_def_heavy":  9
        }


GearRegistry.register(MasoriMask())
