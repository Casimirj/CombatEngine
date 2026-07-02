from app.Domain.GearItem import Gear
from app.Domain.Enums.GearSlot import GearSlot
from app.Data.Registries.GearRegistry import GearRegistry


class MagusRing(Gear):
    name = "Magus ring"
    slot = GearSlot.RING
    aliases = ["magus", "magus ring"]

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
            "stab_def":  0,
            "slash_def":  0,
            "crush_def":  0,
            "magic_def":  0,
            "ranged_def_light":  0,
            "ranged_def_med":  0,
            "ranged_def_heavy":  0
        }


GearRegistry.register(MagusRing())
