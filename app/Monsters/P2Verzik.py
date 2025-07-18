from Monsters.NPC import NPC


class P2Verzik(NPC):

    def __init__(self, scale=1):
        scale_health = {
            5: 3500,
            4: 3000,
            3: 2500,
            2: 2500,
            1: 2500
        }
##need to double check hp still
      
        input_stats = {
            'hp_level': scale_health[scale],
            'attack_level': 400,
            'strength_level': 400,
            'def_level': 200,
            'magic_level': 400,
            'ranged_level': 400,
            # 'prayer_level': 20,

            'attack_bonus': 0,
            'magic_attack_bonus': 80,
            'ranged_attack_bonus': 80,

            'strength_bonus': 0,
            'magic_strength_bonus': 80,
            'ranged_strength_bonus': 80,


            'stab_def': 100,
            'slash_def': 60,
            'crush_def': 100,
            'magic_def': 70,
            "ranged_def_light": 250,
            "ranged_def_med": 250,
            "ranged_def_heavy": 250
        }

        # stats = Stats(input_stats)
        super().__init__(input_stats, weak_to_salve=False, minimum_def=200)

