from combat_engine.Domain.GearItem import Gear
from combat_engine.Domain.Enums.GearSlot import GearSlot
from combat_engine.Data.Registries.GearRegistry import GearRegistry


class ImbuedSaradominCape(Gear):
    name = "Imbued saradomin cape"
    slot = GearSlot.CAPE
    aliases = ["imbued sara cape", "sara god cape i", "saradomin god cape i", "imbued saradomin cape", "saradomin cape i"]

    def build(self) -> dict:
        return {
            "stab_attack_bonus":  0,
            "slash_attack_bonus":  0,
            "crush_attack_bonus":  0,
            "magic_attack_bonus":  15,
            "ranged_attack_bonus":  0,
            "melee_strength_bonus":  0,
            "ranged_strength_bonus":  0,
            "magic_strength_bonus":  2,
            "stab_def":  3,
            "slash_def":  3,
            "crush_def":  3,
            "magic_def":  15,
            "ranged_def_light":  0,
            "ranged_def_med":  0,
            "ranged_def_heavy":  0
        }


GearRegistry.register(ImbuedSaradominCape())
