import math
import random

from beartype import beartype

from Weapons.Weapon import Weapon
from Monsters.NPC import NPC
from Stats import Stats


class DragonClaws(Weapon):

    def __init__(self):
        stats = Stats({
            "slash_attack_bonus": 57,
            "stab_attack_bonus": 41,
            "melee_strength_bonus": 56
        })   
        super().__init__(
            name="Dragon Claws",
            stats=stats,
            combat_style="Melee",
            attack_type="Slash",
            attack_style="Aggressive",
            attack_speed=4,
            attack_range=1,
            has_special_attack=True,
            special_attack_style="Slash",
            special_attack_cost=50
        )
    
    @beartype
    def do_special_attack(self, max_hit:int, player_attack_roll:int, npc_def_roll:int, monster:NPC) -> int:
        hit_def_roll = random.randint(1, npc_def_roll)

        splat_that_hit = 0
        for i in range(1, 4):
            if(random.randint(1, player_attack_roll) >= hit_def_roll):
                splat_that_hit = i
                break


        if splat_that_hit == 1: # all splats hit
            min_hit = math.floor(max_hit / 2)
            max_hit = max_hit - 1

            first_hit = random.randint(min_hit, max_hit)
            second_hit = math.floor(first_hit / 2)
            third_hit = math.floor(first_hit / 4)
            fourth_hit = third_hit + 1
            return first_hit + second_hit + third_hit + fourth_hit
        
        elif splat_that_hit == 2: # 2nd splat hit
            min_hit = math.floor(max_hit * (3/8))
            max_hit = math.floor(max_hit * (7/8))

            first_hit = random.randint(min_hit, max_hit)
            second_hit = math.floor(first_hit / 2)
            third_hit = second_hit + 1
            return first_hit + second_hit + third_hit
        
        elif splat_that_hit == 3: # 3rd splat hit
            min_hit = math.floor(max_hit * (1/4))
            max_hit = math.floor(max_hit * (3/4))

            first_hit = random.randint(min_hit, max_hit)
            second_hit = first_hit + 1
            return first_hit + second_hit
        
        elif splat_that_hit == 4: # 4th splat hit
            min_hit = math.floor(max_hit * (1/4))
            max_hit = math.floor(max_hit * (5/4))

            first_hit = random.randint(min_hit, max_hit)
            return first_hit
        
        else: # no splats hit
            chance = random.randint(1,3) 
            if chance > 1: return 2
            else: return 0 # 2/3rd chance of hitting 2, else 0

