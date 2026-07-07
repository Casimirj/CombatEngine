from combat_engine.Domain.GearItem import Gear
from combat_engine.Domain.Enums.GearSlot import GearSlot
from combat_engine.Data.Registries.GearRegistry import GearRegistry


class FerociousGloves(Gear):
    name = "Ferocious gloves"
    slot = GearSlot.HANDS
    aliases = ["ferocious gloves", "fero gloves", "ferocious"]

    def build(self) -> dict:
        return {
            "stab_attack_bonus":  16,
            "slash_attack_bonus":  16,
            "crush_attack_bonus":  16,
            "magic_attack_bonus": -16,
            "ranged_attack_bonus": -16,
            "melee_strength_bonus":  14,
            "ranged_strength_bonus":  0,
            "magic_strength_bonus":  0,
            "stab_def":  0,
            "slash_def":  0,
            "crush_def":  0,
            "magic_def":  0,
            "ranged_def_light":  0,
            "ranged_def_med":  0,
            "ranged_def_heavy":  0
        }


GearRegistry.register(FerociousGloves())
