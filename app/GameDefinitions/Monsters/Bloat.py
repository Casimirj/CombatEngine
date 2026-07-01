from app.Registries.MonsterRegistry import MonsterRegistry
import math
import random

from app.Monster import Monster


class Bloat(Monster):
    aliases = ["bloat", "pestilent bloat"]

    def __init__(self, scale=1):
        scale_health = {
            5: 2000,
            4: 1750,
            3: 1500,
            2: 1500,
            1: 1500
        }

        input_stats = {
            'hp_level': scale_health[scale],
            'attack_level': 250,
            'strength_level': 340,
            'def_level': 50,
            'magic_level': 150,
            'ranged_level': 180,
            # 'prayer_level': 20,

            'attack_bonus': 150,
            'magic_attack_bonus': 0,
            'ranged_attack_bonus': 180,

            'strength_bonus': 82,
            'magic_strength_bonus': 0,
            'ranged_strength_bonus': 4,


            'stab_def': 30,
            'slash_def': 20,
            'crush_def': 40,
            'magic_def': 600,
            "ranged_def_light": 800,
            "ranged_def_med": 800,
            "ranged_def_heavy": 800
        }

        self.is_walking = False

        self.min_walk_duration = 32
        self.max_walk_durration = 47
        self.down_durration = 32


        # stats = Stats(input_stats)
        super().__init__(input_stats, weak_to_salve=True)


    def reduce_hp(self, amount:int):
        adjusted_amount = amount
        
        if self.is_walking:
            adjusted_amount = math.floor(amount / 2)
        
        super().reduce_hp(adjusted_amount)


    def get_walk_duration(self):
        return random.random(self.min_walk_duration, self.max_walk_durration)
            



MonsterRegistry.register(Bloat)
