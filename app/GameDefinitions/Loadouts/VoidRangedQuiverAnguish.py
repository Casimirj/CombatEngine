from app.Player import Player
from app.Loadout import Loadout
from app.Registries.LoadoutRegistry import LoadoutRegistry


class VoidRangedQuiverAnguish(Loadout):
    name = "VoidRangedQuiverAnguish"
    aliases = ["void range", "void ranged", "void anguish"]

    def build(self) -> Player:
        # Raw equipment bonuses only.
        # Void set effects and other hidden passives are not represented in Stats.
        stats = {
            'hp_level': 99,
            'attack_level': 99,
            'strength_level': 99,
            'def_level': 99,
            'magic_level': 99,
            'ranged_level': 99,
            'prayer_level': 99,

            'slash_attack_bonus': 5,
            'stab_attack_bonus': 5,
            'crush_attack_bonus': 5,
            'magic_attack_bonus': 11,
            'ranged_attack_bonus': 48,

            'melee_strength_bonus': 6,
            'magic_strength_bonus': 2,
            'ranged_strength_bonus': 11,
        }
        return Player(stats=stats)


LoadoutRegistry.register(VoidRangedQuiverAnguish())
player = LoadoutRegistry.get("VoidRangedQuiverAnguish")
