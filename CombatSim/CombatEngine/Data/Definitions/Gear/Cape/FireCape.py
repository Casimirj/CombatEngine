from CombatSim.CombatEngine.Domain.GearItem import Gear
from CombatSim.CombatEngine.Domain.Enums.GearSlot import GearSlot
from CombatSim.CombatEngine.Data.Registries.GearRegistry import GearRegistry


class FireCape(Gear):
    name = "Fire cape"
    slot = GearSlot.CAPE
    aliases = ["fire cape", "fc"]

    def build(self) -> dict:
        return {
            "stab_attack_bonus":  1,
            "slash_attack_bonus":  1,
            "crush_attack_bonus":  1,
            "magic_attack_bonus":  1,
            "ranged_attack_bonus":  1,
            "melee_strength_bonus":  4,
            "ranged_strength_bonus":  0,
            "magic_strength_bonus":  0,
            "stab_def":  11,
            "slash_def":  11,
            "crush_def":  11,
            "magic_def":  11,
            "ranged_def_light":  11,
            "ranged_def_med":  11,
            "prayer_bonus": 2,
            "ranged_def_heavy":  11}


GearRegistry.register(FireCape())

