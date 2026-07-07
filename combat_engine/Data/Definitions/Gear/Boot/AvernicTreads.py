from combat_engine.Domain.GearItem import Gear
from combat_engine.Domain.Enums.GearSlot import GearSlot
from combat_engine.Data.Registries.GearRegistry import GearRegistry


class AvernicTreads(Gear):
    name = "Avernic treads"
    slot = GearSlot.BOOTS
    aliases = ["avernic treads", "avernic boots", "treads"]

    def build(self) -> dict:
        return {
            "stab_attack_bonus":  5,
            "slash_attack_bonus":  5,
            "crush_attack_bonus":  5,
            "magic_attack_bonus":  11,
            "ranged_attack_bonus":  15,
            "melee_strength_bonus":  6,
            "ranged_strength_bonus":  3,
            "magic_strength_bonus":  2,
            "stab_def":  21,
            "slash_def":  25,
            "crush_def":  25,
            "magic_def":  10,
            "ranged_def_light":  10,
            "ranged_def_med":  10,
            "ranged_def_heavy":  10
        }


GearRegistry.register(AvernicTreads())
