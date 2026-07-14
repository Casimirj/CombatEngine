from CombatSim.CombatEngine.Data.Registries.MonsterRegistry import MonsterRegistry

from CombatSim.CombatEngine.Domain.Monster import Monster


class NyloBoss(Monster):
    """NyloBoss — a multi-phase boss that cycles through Melee, Ranged, and Mage phases.

    Stats are placeholder values; final numbers should come from the OSRS wiki.
    """

    aliases = ["nyloboss", "nylo boss", "nylo"]

    def __init__(self, scale=1):
        input_stats = {
            'hp_level': 2000,
            'attack_level': 300,
            'strength_level': 300,
            'def_level': 200,
            'magic_level': 250,
            'ranged_level': 200,

            'attack_bonus': 0,
            'magic_attack_bonus': 200,
            'ranged_attack_bonus': 0,

            'strength_bonus': 0,
            'magic_strength_bonus': 0,
            'ranged_strength_bonus': 0,

            'stab_def': 100,
            'slash_def': 100,
            'crush_def': 100,
            'magic_def': 200,
            "ranged_def_light": 200,
            "ranged_def_med": 200,
            "ranged_def_heavy": 200
        }

        super().__init__(input_stats, weak_to_salve=False)


MonsterRegistry.register(NyloBoss)
