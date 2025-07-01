import interaction
import player
import NPC


players = 2

scale_health = {
    5: 2000,
    4: 1750,
    3: 1500,
    2: 1500,
    1: 1500
}
npc_health = scale_health[players]


player_eff_attack_lvl = player.calc_eff_attack_level()
player_eff_str_lvl = player.calc_eff_strength_level()
player_max_hit = player.calc_max_hit(player_eff_str_lvl)

player_attack_roll = player.calc_att_roll(player_eff_attack_lvl)
npc_defence_roll = NPC.calc_def_roll()

import time
while(True):
    current_npc_health = npc_health
    i = 0
    while current_npc_health > 0:
        for a in range(0, players):
            current_npc_health = interaction.do_hit(current_npc_health, player_attack_roll, npc_defence_roll, player_max_hit)
            if current_npc_health == 0:
                break
        i+=1
        
    print(f"Bloat died in {i} hits!")
    time.sleep(1)
