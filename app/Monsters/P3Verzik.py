from Monsters.NPC import NPC


class P3Verzik(NPC):

    def __init__(self, scale=1):
        scale_health = {
            5: 3500,
            4: 3063,
            3: 2625,
            2: 2625,
            1: 2625
        }

        input_stats = {
            'hp_level': scale_health[scale],
            'attack_level': 400,
            'strength_level': 400,
            'def_level': 150,
            'magic_level': 300,
            'ranged_level': 300,
            # 'prayer_level': 20,

            'attack_bonus': 150,
            'magic_attack_bonus': 80,
            'ranged_attack_bonus': 80,

            'strength_bonus': 82,
            'magic_strength_bonus': 5,
            'ranged_strength_bonus': 5,


            'stab_def': 70,
            'slash_def': 30,
            'crush_def': 70,
            'magic_def': 100,
            "ranged_def_light": 230,
            "ranged_def_med": 230,
            "ranged_def_heavy": 230
        }

        # stats = Stats(input_stats)
        super().__init__(input_stats, weak_to_salve=False)
