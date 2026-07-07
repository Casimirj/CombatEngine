from combat_engine.Domain.GearItem import Gear
from combat_engine.Domain.Enums.GearSlot import GearSlot
from combat_engine.Data.Registries.GearRegistry import GearRegistry


class TorvaFullHelm(Gear):
    name = "Torva full helm"
    slot = GearSlot.HEAD
    aliases = ["torva helm", "torva helmet", "torva full helm"]

    def build(self) -> dict:
        return {
            "stab_attack_bonus":  0,
            "slash_attack_bonus":  0,
            "crush_attack_bonus":  0,
            "magic_attack_bonus": -5,
            "ranged_attack_bonus": -5,
            "melee_strength_bonus":  8,
            "ranged_strength_bonus":  0,
            "magic_strength_bonus":  0,
            "stab_def":  59,
            "slash_def":  60,
            "crush_def":  62,
            "magic_def": -2,
            "ranged_def_light":  57,
            "ranged_def_med":  57,
            "ranged_def_heavy":  57
        }


GearRegistry.register(TorvaFullHelm())
