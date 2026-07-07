from combat_engine.Data.Registries.WeaponRegistry import WeaponRegistry
import math
import random

from combat_engine.Domain.Monster import Monster
from combat_engine.Domain.Stats import Stats
from combat_engine.Domain.Weapon import Weapon


class TumekensShadow(Weapon):
    aliases = ["shadow", "tumekens", "tumeken"]

    def __init__(self):

        stats = Stats({
            "magic_attack_bonus": 35,
            "magic_strength_bonus": 0
        })

        super().__init__(
            name="Tumeken's shadow",
            stats=stats,
            combat_style="Mage",
            attack_type="Magic",
            attack_style="Autocast",
            attack_speed=5,
            attack_range=8,
            has_special_attack=False
        )

    def do_attack(self, max_hit, player_attack_roll, npc_def_roll, monster: Monster = None, always_hit: bool = False):
        adjusted_max_hit = int(max_hit * 4) if (monster and monster.is_toa_monster) else int(max_hit * 3)

        if always_hit:
            return random.randint(1, adjusted_max_hit)

        adjusted_attack_roll = player_attack_roll * 4 if (monster and monster.is_toa_monster) else player_attack_roll * 3

        if adjusted_attack_roll > npc_def_roll:
            hit_chance = 1 - (npc_def_roll + 2) / (2 * (adjusted_attack_roll + 1))
        else:
            hit_chance = adjusted_attack_roll / (2 * (npc_def_roll + 1))

        if random.random() < hit_chance:
            return random.randint(1, adjusted_max_hit)
        else:
            return 0

WeaponRegistry.register(TumekensShadow)
