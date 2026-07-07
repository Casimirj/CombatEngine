from combat_engine.Domain.GearItem import Gear
from combat_engine.Domain.Enums.GearSlot import GearSlot
from combat_engine.Data.Registries.GearRegistry import GearRegistry


class BerserkerRingI(Gear):
    name = "Berserker ring (i)"
    slot = GearSlot.RING
    aliases = ["berserker ring (i)", "bring (i)", "bring(i)", "berserker ring i", "bring i"]

    def build(self) -> dict:
        return {
            "stab_attack_bonus":  0,
            "slash_attack_bonus":  0,
            "crush_attack_bonus":  0,
            "magic_attack_bonus":  0,
            "ranged_attack_bonus":  0,
            "melee_strength_bonus":  8,
            "ranged_strength_bonus":  0,
            "magic_strength_bonus":  0,
            "stab_def":  0,
            "slash_def":  0,
            "crush_def":  8,
            "magic_def":  0,
            "ranged_def_light":  0,
            "ranged_def_med":  0,
            "ranged_def_heavy":  0
        }


GearRegistry.register(BerserkerRingI())
