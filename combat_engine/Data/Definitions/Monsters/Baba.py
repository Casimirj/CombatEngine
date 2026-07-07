from combat_engine.Data.Registries.MonsterRegistry import MonsterRegistry
from combat_engine.Domain.Monster import Monster


class Baba(Monster):
    aliases = ["baba", "ba-ba"]

    def __init__(self, scale=1):
        scale_health = {
            5: 3800,
            4: 3300,
            3: 2800,
            2: 2800,
            1: 2800,
        }

        input_stats = {
            'hp_level': scale_health[scale],
            'attack_level': 150,
            'strength_level': 160,
            'def_level': 80,
            'magic_level': 100,
            'ranged_level': 0,

            'attack_bonus': 0,
            'strength_bonus': 26,
            'magic_attack_bonus': 0,
            'ranged_attack_bonus': 0,
            'magic_strength_bonus': 0,
            'ranged_strength_bonus': 0,

            'stab_def': 80,
            'slash_def': 160,
            'crush_def': 240,
            'magic_def': 280,
            "ranged_def_light": 200,
            "ranged_def_med": 200,
            "ranged_def_heavy": 120,
        }

        super().__init__(input_stats, minimum_def=0, is_toa_monster=True)


MonsterRegistry.register(Baba)
