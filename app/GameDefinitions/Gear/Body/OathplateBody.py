from app.GearItem import Gear
from app.Enums.gear_slot import GearSlot
from app.Registries.GearRegistry import GearRegistry


class OathplateBody(Gear):
    name = "Oathplate body"
    slot = GearSlot.BODY
    aliases = ["oathplate body", "oath body", "oath plate", "oath chest", "oathplate chest"]

    def build(self) -> dict:
        return {
            "stab_attack_bonus":  0,
            "slash_attack_bonus":  16,
            "crush_attack_bonus":  0,
            "magic_attack_bonus": -16,
            "ranged_attack_bonus": -18,
            "melee_strength_bonus":  4,
            "ranged_strength_bonus":  0,
            "magic_strength_bonus":  0,
            "stab_def":  105,
            "slash_def":  128,
            "crush_def":  100,
            "magic_def": -5,
            "ranged_def_light":  112,
            "ranged_def_med":  112,
            "ranged_def_heavy":  112
        }


GearRegistry.register(OathplateBody())
