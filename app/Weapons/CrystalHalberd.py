import math
import random

from beartype import beartype

from Weapons.Weapon import Weapon
from Monsters.NPC import NPC
from Stats import Stats

from Weapon import Weapon
from Stats import Stats


class CrystalHalberd(Weapon):

    def __init__(self):
        stats = Stats({
            "slash_attack_bonus": 110,
            "stab_attack_bonus": 85,
            "melee_strength_bonus": 118
        })   
        super().__init__(
            name="Crystal Halberd",
            stats=stats,
            combat_style="Melee",
            attack_type="Slash",
            attack_style="Aggressive",
            attack_speed=7,
            attack_range=1,
            has_special_attack=True,
            special_attack_style="Slash",
            special_attack_cost=50
        )
    
    @beartype
    def do_special_attack(self, max_hit:int, player_attack_roll:int, npc_def_roll:int, monster:NPC) -> int:
        hit_def_roll = random.randint(1, npc_def_roll)

        splat_1_hit = random.randint(1, player_attack_roll) >= hit_def_roll
        splat_2_hit = random.randint(1, player_attack_roll) >= hit_def_roll
        
        damage_total = 0

        if splat_1_hit:
            damage_total += random.randint(1, max_hit*1.05)
        if splat_2_hit:
            damage_total += random.randint(1, max_hit*1.05)
        
        return damage_total
            
        
