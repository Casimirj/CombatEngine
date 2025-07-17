from Player import Player


stats = {
    'hp_level': 99,
    'attack_level': 99,
    'strength_level': 99,
    'def_level': 99,
    'magic_level': 99,
    'ranged_level': 99,
    'prayer_level': 99,

    'slash_attack_bonus': 85,
    'stab_attack_bonus': 47,
    'crush_attack_bonus': 47,
    'magic_attack_bonus': 0,
    'ranged_attack_bonus': 0,

    'melee_strength_bonus': 63,
    'magic_strength_bonus': 0,
    'ranged_strength_bonus': 0,
}


player = Player(stats=stats)
