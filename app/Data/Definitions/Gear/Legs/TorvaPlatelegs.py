from app.Domain.GearItem import Gear
from app.Domain.Enums.GearSlot import GearSlot
from app.Data.Registries.GearRegistry import GearRegistry


class TorvaPlatelegs(Gear):
    name = "Torva platelegs"
    slot = GearSlot.LEGS
    aliases = ["torva legs", "torva platelegs"]

    def build(self) -> dict:
        return {
            "stab_attack_bonus":  0,
            "slash_attack_bonus":  0,
            "crush_attack_bonus":  0,
            "magic_attack_bonus": -24,
            "ranged_attack_bonus": -11,
            "melee_strength_bonus":  4,
            "ranged_strength_bonus":  0,
            "magic_strength_bonus":  0,
            "stab_def":  87,
            "slash_def":  78,
            "crush_def":  79,
            "magic_def": -9,
            "ranged_def_light":  102,
            "ranged_def_med":  102,
            "ranged_def_heavy":  102
        }


GearRegistry.register(TorvaPlatelegs())
