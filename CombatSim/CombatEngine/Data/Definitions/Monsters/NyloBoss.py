from CombatSim.CombatEngine.Data.Registries.MonsterRegistry import MonsterRegistry

from CombatSim.CombatEngine.Domain.Monster import Monster


class NyloBoss(Monster):
    """Nylocas Vasilias — Theatre of Blood boss.

    Stats sourced from OSRS Wiki. HP scales by team size:
      1-3 players: 1875 HP
      4 players:   2187 HP
      5 players:   2500 HP
    """

    aliases = ["nyloboss", "nylo boss", "nylo", "nylocas vasilias"]

    def __init__(self, scale=1):
        # Static HP by scale — no multipliers
        scale_hp = {
            1: 1875,
            2: 1875,
            3: 1875,
            4: 2187,
            5: 2500,
        }
        hp = scale_hp.get(scale, 1875)

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
