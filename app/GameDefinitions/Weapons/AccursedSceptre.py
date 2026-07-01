from app.Registries.WeaponRegistry import WeaponRegistry
import math
import random

from app.Monster import Monster
from app.Stats import Stats
from app.Weapon import Weapon


class AccursedSceptre(Weapon):
    aliases = ["sceptre", "accursed"]

    def __init__(self):

        stats = Stats({
            "magic_attack_bonus": 22,
            "magic_strength_bonus": 0
        })

        super().__init__(
            name="Accursed sceptre",
            stats=stats,
            combat_style="Mage",
            attack_type="Magic",
            attack_style="Autocast",
            attack_speed=4,
            attack_range=7,
            has_special_attack=True,
            special_attack_style="Magic",
            special_attack_cost=50
        )

    def do_special_attack(self, max_hit: int, player_attack_roll: int, npc_def_roll: int, monster: Monster = None) -> int:
        adjusted_attack_roll = int(player_attack_roll * 1.5)
        adjusted_max_hit = int(max_hit * 1.5)

        if adjusted_attack_roll > npc_def_roll:
            hit_chance = 1 - (npc_def_roll + 2) / (2 * (adjusted_attack_roll + 1))
        else:
            hit_chance = adjusted_attack_roll / (2 * (npc_def_roll + 1))

        damage = 0
        if random.random() < hit_chance:
            damage = random.randint(1, adjusted_max_hit)

        if damage > 0 and monster is not None:
            monster.reduce_defense(int(damage * 0.15))
            monster.reduce_magic_level(0.15)

        return damage

WeaponRegistry.register(AccursedSceptre)
