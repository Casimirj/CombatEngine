import math
import random

from app.Stats import Stats
from app.Weapon import Weapon
from app.Registries.WeaponRegistry import WeaponRegistry


class Scythe(Weapon):
    aliases = ["scythe"]

    def __init__(self):

        stats = Stats({
            "stab_attack_bonus": 0,
            "slash_attack_bonus": 125,
            "crush_attack_bonus": 30,
            "melee_strength_bonus": 75
        })

        super().__init__(
            name="Scythe of Vitur",
            stats = stats,
            combat_style="Melee",
            attack_type="Slash",
            attack_style="Aggressive",
            attack_speed=5,
            attack_range=1,
            has_special_attack=False
        )


    def do_attack(self, max_hit, player_attack_roll, npc_def_roll, monster=None):

        hit_def_roll = random.randint(1, npc_def_roll)

        splat_1_hit = random.randint(1, player_attack_roll) >= hit_def_roll
        splat_2_hit = random.randint(1, player_attack_roll) >= hit_def_roll
        splat_3_hit = random.randint(1, player_attack_roll) >= hit_def_roll

        damage_total = 0

        if splat_1_hit:
            damage_total += random.randint(1, max_hit)
        if splat_2_hit:
            damage_total += random.randint(1, math.floor(max_hit/2))
        if splat_3_hit:
            damage_total += random.randint(1, math.floor(max_hit/4))

        return damage_total


WeaponRegistry.register(Scythe)
