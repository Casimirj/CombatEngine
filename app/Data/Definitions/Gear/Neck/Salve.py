from app.Domain.GearItem import Gear
from app.Domain.Enums.GearSlot import GearSlot
from app.Data.Registries.GearRegistry import GearRegistry


class Salve(Gear):
    name = "Salve (e)"
    slot = GearSlot.NECK
    aliases = ["salve ie", "salve e", "salve amulet", "salve"]

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
            "stab_def":  3,
            "slash_def":  3,
            "crush_def":  3,
            "magic_def":  0,
            "ranged_def_light":  0,
            "ranged_def_med":  0,
            "ranged_def_heavy":  0,
        }


GearRegistry.register(Salve())
