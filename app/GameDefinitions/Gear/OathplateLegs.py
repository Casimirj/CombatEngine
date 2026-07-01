from app.GearItem import Gear
from app.Enums.gear_slot import GearSlot
from app.Registries.GearRegistry import GearRegistry


class OathplateLegs(Gear):
    name = "Oathplate legs"
    slot = GearSlot.LEGS
    aliases = ["oathplate legs", "oath legs"]

    def build(self) -> dict:
        return {
            "stab_attack_bonus":  0,
            "slash_attack_bonus":  12,
            "crush_attack_bonus":  0,
            "magic_attack_bonus": -12,
            "ranged_attack_bonus": -14,
            "melee_strength_bonus":  2,
            "ranged_strength_bonus":  0,
            "magic_strength_bonus":  0,
            "stab_def":  75,
            "slash_def":  100,
            "crush_def":  73,
            "magic_def": -3,
            "ranged_def_light":  81,
            "ranged_def_med":  81,
            "ranged_def_heavy":  81
        }


GearRegistry.register(OathplateLegs())
