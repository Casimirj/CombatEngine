from combat_engine.Domain.GearItem import Gear
from combat_engine.Domain.Enums.GearSlot import GearSlot
from combat_engine.Data.Registries.GearRegistry import GearRegistry


class OathplateHelm(Gear):
    name = "Oathplate helm"
    slot = GearSlot.HEAD
    aliases = ["oathplate helmet", "oath helm", "oath helmet"]

    def build(self) -> dict:
        return {
            "stab_attack_bonus":  0,
            "slash_attack_bonus":  10,
            "crush_attack_bonus":  0,
            "magic_attack_bonus": -2,
            "ranged_attack_bonus": -7,
            "melee_strength_bonus":  6,
            "ranged_strength_bonus":  0,
            "magic_strength_bonus":  0,
            "stab_def":  50,
            "slash_def":  72,
            "crush_def":  45,
            "magic_def":  0,
            "ranged_def_light":  50,
            "ranged_def_med":  50,
            "ranged_def_heavy":  50
        }


GearRegistry.register(OathplateHelm())
