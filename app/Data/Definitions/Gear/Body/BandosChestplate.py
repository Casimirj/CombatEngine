from app.Domain.GearItem import Gear
from app.Domain.Enums.GearSlot import GearSlot
from app.Data.Registries.GearRegistry import GearRegistry


class BandosChestplate(Gear):
    name = "Bandos chestplate"
    slot = GearSlot.BODY
    aliases = ["bandos chestplate", "bandos body", "bcp", "bandos chest", "bandos platebody"]

    def build(self) -> dict:
        return {
            "stab_attack_bonus":  0,
            "slash_attack_bonus":  0,
            "crush_attack_bonus":  0,
            "magic_attack_bonus": -15,
            "ranged_attack_bonus": -10,
            "melee_strength_bonus":  4,
            "ranged_strength_bonus":  0,
            "magic_strength_bonus":  0,
            "stab_def":  98,
            "slash_def":  93,
            "crush_def":  105,
            "magic_def": -6,
            "ranged_def_light":  133,
            "ranged_def_med":  133,
            "ranged_def_heavy":  133
        }


GearRegistry.register(BandosChestplate())
