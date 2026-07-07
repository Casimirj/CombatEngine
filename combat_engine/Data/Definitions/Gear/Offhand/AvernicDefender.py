from combat_engine.Domain.GearItem import Gear
from combat_engine.Domain.Enums.GearSlot import GearSlot
from combat_engine.Data.Registries.GearRegistry import GearRegistry


class AvernicDefender(Gear):
    name = "Avernic defender"
    slot = GearSlot.OFFHAND
    aliases = ["avernic defender", "avernic", "avernic def"]

    def build(self) -> dict:
        return {
            "stab_attack_bonus":  30,
            "slash_attack_bonus":  29,
            "crush_attack_bonus":  28,
            "magic_attack_bonus": -5,
            "ranged_attack_bonus": -4,
            "melee_strength_bonus":  8,
            "ranged_strength_bonus":  0,
            "magic_strength_bonus":  0,
            "stab_def":  30,
            "slash_def":  29,
            "crush_def":  28,
            "magic_def": -5,
            "ranged_def_light": -4,
            "ranged_def_med": -4,
            "ranged_def_heavy": -4
        }


GearRegistry.register(AvernicDefender())
