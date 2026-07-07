from combat_engine.Domain.GearItem import Gear
from combat_engine.Domain.Enums.GearSlot import GearSlot
from combat_engine.Data.Registries.GearRegistry import GearRegistry


class MasoriBody(Gear):
    name = "Masori body"
    slot = GearSlot.BODY
    aliases = ["masori chest", "masori platebody", "masori top"]

    def build(self) -> dict:
        return {
            "stab_attack_bonus":  0,
            "slash_attack_bonus":  0,
            "crush_attack_bonus":  0,
            "magic_attack_bonus": -4,
            "ranged_attack_bonus":  43,
            "melee_strength_bonus":  0,
            "ranged_strength_bonus":  4,
            "magic_strength_bonus":  0,
            "stab_def":  37,
            "slash_def":  35,
            "crush_def":  38,
            "magic_def":  25,
            "ranged_def_light":  33,
            "ranged_def_med":  33,
            "ranged_def_heavy":  33
        }


GearRegistry.register(MasoriBody())
