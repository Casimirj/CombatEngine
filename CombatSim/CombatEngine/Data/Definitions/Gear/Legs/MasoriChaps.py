from CombatSim.CombatEngine.Domain.GearItem import Gear
from CombatSim.CombatEngine.Domain.Enums.GearSlot import GearSlot
from CombatSim.CombatEngine.Data.Registries.GearRegistry import GearRegistry


class MasoriChaps(Gear):
    name = "Masori chaps"
    slot = GearSlot.LEGS
    aliases = ["masori legs", "masori bottom", "masori chaps"]

    def build(self) -> dict:
        return {
            "stab_attack_bonus":  0,
            "slash_attack_bonus":  0,
            "crush_attack_bonus":  0,
            "magic_attack_bonus": -2,
            "ranged_attack_bonus":  27,
            "melee_strength_bonus":  0,
            "ranged_strength_bonus":  2,
            "magic_strength_bonus":  0,
            "stab_def":  35,
            "slash_def":  30,
            "crush_def":  39,
            "magic_def":  46,
            "ranged_def_light":  37,
            "ranged_def_med":  37,
            "ranged_def_heavy":  37
        }


GearRegistry.register(MasoriChaps())
