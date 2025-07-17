from NPC import NPC


class Sotetseg(NPC):

    def __init__(self, scale=1):
        scale_health = {
            5: 4000,
            4: 3500,
            3: 3000,
            2: 3000,
            1: 3000,
        }

        input_stats = {
            'hp_level': scale_health[scale],
            'attack_level': 250,
            'strength_level': 250,
            'def_level': 200,
            'magic_level': 250,
            'ranged_level': 250,
            # 'prayer_level': 20,

            'attack_bonus': 0,
            'magic_attack_bonus': 60,
            'ranged_attack_bonus': -10,

            'strength_bonus': 48,
            'magic_strength_bonus': 60,
            'ranged_strength_bonus': 60,


            'stab_def': 70,
            'slash_def': 70,
            'crush_def': 70,
            'magic_def': 30,
            "ranged_def_light": 150,
            "ranged_def_med": 150,
            "ranged_def_heavy": 150
        }

        # stats = Stats(input_stats)
        super().__init__(input_stats, minimum_def=100)

