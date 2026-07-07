from combat_engine.Data.Registries.WeaponRegistry import WeaponRegistry
import random

from combat_engine.Domain.Monster import Monster
from combat_engine.Domain.Stats import Stats
from combat_engine.Domain.Weapon import Weapon


class NightmareStaff(Weapon):
    aliases = ["nightmare", "staff", "nm"]

    def __init__(self):
        stats = Stats({
            "magic_attack_bonus": 16,
            "magic_strength_bonus": 15
        })

        super().__init__(
            name="Nightmare staff",
            stats=stats,
            combat_style="Mage",
            attack_type="Magic",
            attack_style="Autocast",
            attack_speed=5,
            attack_range=7,
            has_special_attack=False
        )

    def do_attack(self, max_hit, player_attack_roll, npc_def_roll, monster: Monster = None, always_hit: bool = False):
        if always_hit:
            return random.randint(1, max_hit)

        if player_attack_roll > npc_def_roll:
            hit_chance = 1 - (npc_def_roll + 2) / (2 * (player_attack_roll + 1))
        else:
            hit_chance = player_attack_roll / (2 * (npc_def_roll + 1))

        if random.random() < hit_chance:
            return random.randint(1, max_hit)
        return 0

WeaponRegistry.register(NightmareStaff)
