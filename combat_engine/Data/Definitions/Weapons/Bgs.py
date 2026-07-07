from combat_engine.Data.Registries.WeaponRegistry import WeaponRegistry
import math
import random

from combat_engine.Domain.Monster import Monster
from combat_engine.Domain.Stats import Stats
from combat_engine.Domain.Weapon import Weapon


class Bgs(Weapon):
    aliases = ["bgs", "bandos godsword", "godsword"]

    def __init__(self):
        stats = Stats({
            "slash_attack_bonus": 132,
            "crush_attack_bonus": 80,
            "melee_strength_bonus": 132
        })   
        super().__init__(
            name="Bandos Godsword",
            stats=stats,
            combat_style="Melee",
            attack_type="Slash",
            attack_style="Aggressive",
            attack_speed=6,
            attack_range=1,
            has_special_attack=True,
            special_attack_style="Slash",
            special_attack_cost=50
        )
        
    def do_special_attack(self, max_hit:int, player_attack_roll:int, npc_def_roll:int, monster:Monster, always_hit: bool = False) -> int:
        if always_hit:
            hit = random.randint(1, max_hit)
            adjusted_hit = math.floor(hit * 1.21)
            if adjusted_hit > 0:
                monster.reduce_defense_bgs(damage_amount=adjusted_hit)
            return adjusted_hit

        adjusted_attack_roll = player_attack_roll * 2
        hit = super().do_attack(max_hit, adjusted_attack_roll, npc_def_roll)
        adjusted_hit = math.floor(hit * 1.21)

        if adjusted_hit > 0:
            monster.reduce_defense_bgs(damage_amount=adjusted_hit)
        return adjusted_hit

WeaponRegistry.register(Bgs)
