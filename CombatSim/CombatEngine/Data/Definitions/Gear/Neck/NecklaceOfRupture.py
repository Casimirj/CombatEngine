from CombatSim.CombatEngine.Domain.GearItem import Gear
from CombatSim.CombatEngine.Domain.Enums.GearSlot import GearSlot
from CombatSim.CombatEngine.Data.Registries.GearRegistry import GearRegistry


class NecklaceOfRupture(Gear):
    name = "Necklace of rupture"
    slot = GearSlot.NECK
    aliases = ["rupture", "rupture necklace", "necklace of rupture"]

    def build(self) -> dict:
        return {
            "stab_attack_bonus":  0,
            "slash_attack_bonus":  0,
            "crush_attack_bonus":  0,
            "magic_attack_bonus":  0,
            "ranged_attack_bonus":  20,
            "melee_strength_bonus":  0,
            "ranged_strength_bonus":  8,
            "magic_strength_bonus":  0,
            "stab_def":  0,
            "slash_def":  0,
            "crush_def":  0,
            "magic_def":  0,
            "ranged_def_light":  0,
            "ranged_def_med":  0,
            "prayer_bonus": 3,
            "ranged_def_heavy":  0}


GearRegistry.register(NecklaceOfRupture())

