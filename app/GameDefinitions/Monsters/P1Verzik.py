from app.Registries.MonsterRegistry import MonsterRegistry
from app.Monster import Monster


class P1Verzik(Monster):
    aliases = ["p1verzik", "verzik p1", "verzik 1"]

    def __init__(self, scale=1):
        scale_health = {
            5: 2000,
            4: 1500,
            3: 1000,
            2: 1000,
            1: 1000
        }
##need to double check hp still
      
        input_stats = {
            'hp_level': scale_health[scale],
            'attack_level': 400,
            'strength_level': 400,
            'def_level': 20,
            'magic_level': 400,
            'ranged_level': 400,
            # 'prayer_level': 20,

            'attack_bonus': 0,
            'magic_attack_bonus': 80,
            'ranged_attack_bonus': 80,

            'strength_bonus': 0,
            'magic_strength_bonus': 150,
            'ranged_strength_bonus': 80,


            'stab_def': 20,
            'slash_def': 20,
            'crush_def': 20,
            'magic_def': 20,
            "ranged_def_light": 20,
            "ranged_def_med": 20,
            "ranged_def_heavy": 20
        }

        # stats = Stats(input_stats)
        super().__init__(input_stats, weak_to_salve=False)

MonsterRegistry.register(P1Verzik)
