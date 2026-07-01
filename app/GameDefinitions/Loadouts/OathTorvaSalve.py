from app.Player import Player
from app.Loadout import Loadout
from app.Registries.LoadoutRegistry import LoadoutRegistry


class OathTorvaSalve(Loadout):
    name = "OathTorvaSalve"
    aliases = ["torva salve", "oath salve"]

    def build(self) -> Player:
        stats = {
            'hp_level': 99,
            'attack_level': 99,
            'strength_level': 99,
            'def_level': 99,
            'magic_level': 99,
            'ranged_level': 99,
            'prayer_level': 99,

            'slash_attack_bonus': 50,
            'stab_attack_bonus': 22,
            'crush_attack_bonus': 22,
            'magic_attack_bonus': 0,
            'ranged_attack_bonus': 0,

            'melee_strength_bonus': 53,
            'magic_strength_bonus': 0,
            'ranged_strength_bonus': 0,
        }
        return Player(stats=stats, wearing_salve=True)


LoadoutRegistry.register(OathTorvaSalve())
player = LoadoutRegistry.get("OathTorvaSalve")
