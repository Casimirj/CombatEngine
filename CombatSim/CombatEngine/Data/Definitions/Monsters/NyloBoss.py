from CombatSim.CombatEngine.Data.Registries.MonsterRegistry import MonsterRegistry

from CombatSim.CombatEngine.Domain.Monster import Monster


class NyloBoss(Monster):
    """Nylocas Vasilias — Theatre of Blood boss.

    Stats sourced from OSRS Wiki. HP scales by team size:
      1-3 players: 75%  (1875)
      4 players:   87.5% (2187)
      5 players:   100%  (2500)
    """

    aliases = ["nyloboss", "nylo boss", "nylo", "nylocas vasilias"]

    def __init__(self, scale=1):
        # Scale → team size: 1=solo (1-3), 2=4-man, 3=5-man
        scale_hp_mult = {
            1: 0.75,
            2: 0.875,
            3: 1.0,
        }
        base_hp = 2500
        hp = int(base_hp * scale_hp_mult.get(scale, 0.75))

        input_stats = {
            'hp_level': hp,
            'attack_level': 400,
            'strength_level': 350,
            'def_level': 50,
            'magic_level': 50,
            'ranged_level': 350,

            'attack_bonus': 0,
            'magic_attack_bonus': 600,
            'ranged_attack_bonus': 0,

            'strength_bonus': 60,
            'magic_strength_bonus': 600,
            'ranged_strength_bonus': 60,

            'stab_def': 0,
            'slash_def': 0,
            'crush_def': 0,
            'magic_def': 0,
            "ranged_def_light": 0,
            "ranged_def_med": 0,
            "ranged_def_heavy": 0,
        }

        super().__init__(input_stats, weak_to_salve=False)


MonsterRegistry.register(NyloBoss)
