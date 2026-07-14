from CombatSim.CombatEngine.Domain.GearItem import Gear
from CombatSim.CombatEngine.Domain.Enums.GearSlot import GearSlot
from CombatSim.CombatEngine.Data.Registries.GearRegistry import GearRegistry


class WardOfElidinisF(Gear):
    name = "Ward of elidinis (f)"
    slot = GearSlot.OFFHAND
    aliases = ["ward of elidinis (f)", "elidinis ward (f)", "ward (f)", "fortified ward"]

    def build(self) -> dict:
        return {
            "stab_attack_bonus":    0,
            "slash_attack_bonus":   0,
            "crush_attack_bonus":   0,
            "magic_attack_bonus":   25,
            "ranged_attack_bonus":  0,
            "melee_strength_bonus":  0,
            "ranged_strength_bonus": 0,
            "magic_strength_bonus":  5,
            "stab_def":   53,
            "slash_def":  55,
            "crush_def":  73,
            "magic_def":  2,
            "ranged_def_light": 52,
            "ranged_def_med":   52,
            "ranged_def_heavy": 52,
        }


GearRegistry.register(WardOfElidinisF())
