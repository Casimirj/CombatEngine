from app.Registries.MonsterRegistry import MonsterRegistry
from app.Monster import Monster


class Xarpus(Monster):
    aliases = ["xarpus", "xarp"]

    def __init__(self, scale=1):
        scale_health = {
            5: 5000,
            4: 4000,
            3: 3000,
            2: 3000,
            1: 3000
        }
##need to double check hp
        
        input_stats = {
            'hp_level': scale_health[scale],
            'attack_level': 1,
            'strength_level': 1,
            'def_level': 250,
            'magic_level': 220,
            'ranged_level': 100,
            # 'prayer_level': 20,

            'attack_bonus': 0,
            'magic_attack_bonus': 0,
            'ranged_attack_bonus': 0,

            'strength_bonus': 0,
            'magic_strength_bonus': 0,
            'ranged_strength_bonus': 0,


            'stab_def': 0,
            'slash_def': 0,
            'crush_def': 0,
            'magic_def': 0,
            "ranged_def_light": 160,
            "ranged_def_med": 160,
            "ranged_def_heavy": 160
        }

        # stats = Stats(input_stats)
        super().__init__(input_stats, weak_to_salve=False)

MonsterRegistry.register(Xarpus)
