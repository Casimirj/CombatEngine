from app.GearItem import Gear
from app.Enums.gear_slot import GearSlot
from app.Registries.GearRegistry import GearRegistry


class EliteVoidRobe(Gear):
    name = "Elite void robe"
    slot = GearSlot.LEGS
    aliases = ["elite void robe", "void robe", "elite void bottom", "elite void legs"]

    def build(self) -> dict:
        return {
            "stab_attack_bonus":  0,
            "slash_attack_bonus":  0,
            "crush_attack_bonus":  0,
            "magic_attack_bonus":  0,
            "ranged_attack_bonus":  0,
            "melee_strength_bonus":  0,
            "ranged_strength_bonus":  0,
            "magic_strength_bonus":  0,
            "stab_def":  30,
            "slash_def":  30,
            "crush_def":  30,
            "magic_def":  30,
            "ranged_def_light":  30,
            "ranged_def_med":  30,
            "ranged_def_heavy":  30
        }


GearRegistry.register(EliteVoidRobe())
