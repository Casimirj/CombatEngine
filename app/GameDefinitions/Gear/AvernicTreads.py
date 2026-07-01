from app.GearItem import Gear
from app.Enums.gear_slot import GearSlot
from app.Registries.GearRegistry import GearRegistry


class AvernicTreads(Gear):
    name = "Avernic treads"
    slot = GearSlot.FEET
    aliases = ["avernic treads", "avernic boots", "treads"]

    def build(self) -> dict:
        return {
            "stab_attack_bonus":  5,
            "slash_attack_bonus":  5,
            "crush_attack_bonus":  5,
            "magic_attack_bonus":  11,
            "ranged_attack_bonus":  15,
            "melee_strength_bonus":  4,
            "ranged_strength_bonus":  2,
            "magic_strength_bonus":  1,
            "stab_def":  21,
            "slash_def":  25,
            "crush_def":  25,
            "magic_def":  10,
            "ranged_def_light":  10,
            "ranged_def_med":  10,
            "ranged_def_heavy":  10
        }


GearRegistry.register(AvernicTreads())
