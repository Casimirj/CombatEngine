from CombatSim.CombatEngine.Domain.GearItem import Gear
from CombatSim.CombatEngine.Domain.Enums.GearSlot import GearSlot
from CombatSim.CombatEngine.Data.Registries.GearRegistry import GearRegistry


class MasoriBody(Gear):
    name = "Masori body"
    slot = GearSlot.BODY
    aliases = ["masori chest", "masori platebody", "masori top"]

    def build(self) -> dict:
        return {
            "stab_attack_bonus":  0,
            "slash_attack_bonus":  0,
            "crush_attack_bonus":  0,
            "magic_attack_bonus": -4,
            "ranged_attack_bonus":  43,
            "melee_strength_bonus":  0,
            "ranged_strength_bonus":  4,
            "magic_strength_bonus":  0,
            "stab_def":  59,
            "slash_def":  52,
            "crush_def":  64,
            "magic_def":  74,
            "ranged_def_light":  60,
            "ranged_def_med":  60,
            "ranged_def_heavy":  60
        }


GearRegistry.register(MasoriBody())
