from CombatSim.CombatEngine.Data.Registries.MonsterRegistry import MonsterRegistry
from CombatSim.CombatEngine.Domain.Monster import Monster


class Maiden(Monster):
    aliases = ["maiden", "maiden of sugadinti"]

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
            'attack_level': 350,
            'strength_level': 350,
            'def_level': 200,
            'magic_level': 350,
            'ranged_level': 350,
            # 'prayer_level': 20,

            'attack_bonus': 0,
            'magic_attack_bonus': 300,
            'ranged_attack_bonus': 0,

            'strength_bonus': 0,
            'magic_strength_bonus': 0,
            'ranged_strength_bonus': 0,


            'stab_def': 0,
            'slash_def': 0,
            'crush_def': 0,
            'magic_def': 0,
            "ranged_def_light": 0,
            "ranged_def_med": 0,
            "ranged_def_heavy": 0
        }

        # stats = Stats(input_stats)
        super().__init__(input_stats, weak_to_salve=False)

MonsterRegistry.register(Maiden)
