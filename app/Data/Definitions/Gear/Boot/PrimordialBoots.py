from app.Domain.GearItem import Gear
from app.Domain.Enums.GearSlot import GearSlot
from app.Data.Registries.GearRegistry import GearRegistry


class PrimordialBoots(Gear):
    name = "Primordial boots"
    slot = GearSlot.BOOTS
    aliases = ["primordial boots", "primordials", "prims", "prim boots"]

    def build(self) -> dict:
        return {
            "stab_attack_bonus":  2,
            "slash_attack_bonus":  2,
            "crush_attack_bonus":  2,
            "magic_attack_bonus": -4,
            "ranged_attack_bonus": -1,
            "melee_strength_bonus":  5,
            "ranged_strength_bonus":  0,
            "magic_strength_bonus":  0,
            "stab_def":  22,
            "slash_def":  22,
            "crush_def":  22,
            "magic_def":  0,
            "ranged_def_light":  0,
            "ranged_def_med":  0,
            "ranged_def_heavy":  0
        }


GearRegistry.register(PrimordialBoots())
