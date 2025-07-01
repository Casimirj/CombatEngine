import random
import math

import player
import NPC





# player_eff_attack_lvl = player.calc_eff_attack_level()
# player_eff_str_lvl = player.calc_eff_strength_level()
# player_max_hit = player.calc_max_hit(player_eff_str_lvl)

# player_attack_roll = player.calc_att_roll(player_eff_attack_lvl)
# npc_defence_roll = npc.calc_def_roll()




def get_hit(player_att_roll, npc_def_roll, max_hit, weapon=None):
    hit = 0
    
    hit_att_roll = random.randint(1, player_att_roll)
    hit_def_roll = random.randint(1, npc_def_roll)
    
    if(hit_att_roll < hit_def_roll and weapon is not "scythe"):
        # print("The attack missed!")
        return hit
        
    
    if(weapon is None):
        hit = random.randint(1, max_hit)
        # hit = max_hit
        
    elif(weapon is "scythe"):
        first_max = get_hit(player_att_roll, npc_def_roll, max_hit)
        second_max = get_hit(player_att_roll, npc_def_roll, math.floor(max_hit/2))
        third_max = get_hit(player_att_roll, npc_def_roll, math.floor(max_hit/4))
                
        hit = first_max + second_max + third_max

    # print(f"The attack hit! {hit}")
    return hit


def do_hit(npc_health, player_att_roll, npc_def_roll, max_hit, weapon="scythe"):
    hit = get_hit(player_att_roll, npc_def_roll, max_hit, weapon="scythe")
    new_health = npc_health - hit
    if new_health < 0:
        return 0
    return new_health
    
    
    
    
# import time
# while(True):
#     hit = get_hit(player_attack_roll, npc_defence_roll, player_max_hit, scythe=True)
#     print(f"Hit {hit}")
#     time.sleep(0.5)
    
#     if(hit == 99):
#         print("We hit a true max hit!!")
#         break
