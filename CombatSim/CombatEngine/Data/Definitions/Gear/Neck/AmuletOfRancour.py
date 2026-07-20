from CombatSim.CombatEngine.Domain.GearItem import Gear
from CombatSim.CombatEngine.Domain.Enums.GearSlot import GearSlot
from CombatSim.CombatEngine.Data.Registries.GearRegistry import GearRegistry


class AmuletOfRancour(Gear):
    name = "Amulet of rancour"
    slot = GearSlot.NECK
    aliases = ["rancour", "rancour amulet", "amulet of rancour", "necklace of rancour"]

    def build(self) -> dict:
        return {
            "stab_attack_bonus":  25,
            "slash_attack_bonus":  25,
            "crush_attack_bonus":  25,
            "magic_attack_bonus": -6,
            "ranged_attack_bonus": -8,
            "melee_strength_bonus":  12,
            "ranged_strength_bonus":  0,
            "magic_strength_bonus":  0,
            "stab_def":  0,
            "slash_def":  0,
            "crush_def":  0,
            "magic_def":  0,
            "ranged_def_light":  0,
            "ranged_def_med":  0,
            "prayer_bonus": 2,
            "ranged_def_heavy":  0}


GearRegistry.register(AmuletOfRancour())

