from app.Registries.WeaponRegistry import WeaponRegistry
import random

from app.Monster import Monster
from app.Stats import Stats
from app.Weapon import Weapon


class ToxicBlowpipe(Weapon):
    aliases = ["blowpipe", "bp", "pipe"]

    def __init__(self):
        stats = Stats({
            "ranged_attack_bonus": 30,
            "ranged_strength_bonus": 55
        })

        super().__init__(
            name="Toxic blowpipe",
            stats=stats,
            combat_style="Ranged",
            attack_type="Ranged",
            attack_style="Rapid",
            attack_speed=3,
            attack_range=5,
            has_special_attack=True,
            special_attack_style="Ranged",
            special_attack_cost=50
        )

    def do_attack(self, max_hit, player_attack_roll, npc_def_roll, monster: Monster = None):
        if player_attack_roll > npc_def_roll:
            hit_chance = 1 - (npc_def_roll + 2) / (2 * (player_attack_roll + 1))
        else:
            hit_chance = player_attack_roll / (2 * (npc_def_roll + 1))

        if random.random() < hit_chance:
            damage = random.randint(1, max_hit)
            if random.random() < 0.25:
                damage += 6
            return damage
        return 0

    def do_special_attack(self, max_hit: int, player_attack_roll: int, npc_def_roll: int, monster: Monster = None) -> int:
        adjusted_attack_roll = player_attack_roll * 2
        adjusted_max_hit = int(max_hit * 1.5)

        if adjusted_attack_roll > npc_def_roll:
            hit_chance = 1 - (npc_def_roll + 2) / (2 * (adjusted_attack_roll + 1))
        else:
            hit_chance = adjusted_attack_roll / (2 * (npc_def_roll + 1))

        if random.random() < hit_chance:
            return random.randint(1, adjusted_max_hit)
        else:
            return 0

WeaponRegistry.register(ToxicBlowpipe)
