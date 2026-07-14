from CombatSim.CombatEngine.Domain.GearItem import Gear
from CombatSim.CombatEngine.Domain.Enums.GearSlot import GearSlot
from CombatSim.CombatEngine.Data.Registries.GearRegistry import GearRegistry


class WardOfElidinis(Gear):
    name = "Ward of elidinis"
    slot = GearSlot.OFFHAND
    aliases = ["ward of elidinis", "elidinis ward", "ward"]

    def build(self) -> dict:
        return {
            "stab_attack_bonus":    0,
            "slash_attack_bonus":   0,
            "crush_attack_bonus":   0,
            "magic_attack_bonus":   5,
            "ranged_attack_bonus":  0,
            "melee_strength_bonus":  0,
            "ranged_strength_bonus": 0,
            "magic_strength_bonus":  3,
            "stab_def":   5,
            "slash_def":  3,
            "crush_def":  9,
            "magic_def":  0,
            "ranged_def_light": 6,
            "ranged_def_med":   6,
            "ranged_def_heavy": 6,
        }


GearRegistry.register(WardOfElidinis())
