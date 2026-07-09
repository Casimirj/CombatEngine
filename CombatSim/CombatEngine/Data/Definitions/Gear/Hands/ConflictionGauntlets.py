from CombatSim.CombatEngine.Domain.GearItem import Gear
from CombatSim.CombatEngine.Domain.Enums.GearSlot import GearSlot
from CombatSim.CombatEngine.Data.Registries.GearRegistry import GearRegistry


class ConflictionGauntlets(Gear):
    name = "Confliction gauntlets"
    slot = GearSlot.HANDS
    aliases = ["confliction gauntlets", "confliction", "cgauntlets"]

    def build(self) -> dict:
        return {
            "stab_attack_bonus":  0,
            "slash_attack_bonus":  0,
            "crush_attack_bonus":  0,
            "magic_attack_bonus":  20,
            "ranged_attack_bonus": -4,
            "melee_strength_bonus":  0,
            "ranged_strength_bonus":  0,
            "magic_strength_bonus":  7,
            "stab_def":  15,
            "slash_def":  18,
            "crush_def":  7,
            "magic_def":  5,
            "ranged_def_light":  5,
            "ranged_def_med":  5,
            "ranged_def_heavy":  5
        }


GearRegistry.register(ConflictionGauntlets())
