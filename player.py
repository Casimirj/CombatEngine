
import math
import random


class player:

    def __init__(self):
        #player properties
        self.player_att_level = 99
        self.player_str_level = 99
        self.player_def_level = 99
        self.super_combat = True
        self.piety_active = True
        self.attack_style = "aggressive"
        self.using_salve = True

        #gear properties
        self.str_bonus = 132
        self.slash_bonus = 147
        self.slash_def_bonus = 313

    def calc_eff_strength_level(self):
        eff_str_level = self.player_str_level
        
        if(self.super_combat): eff_str_level += 19
        if(self.piety_active):
            eff_str_level *= 1.23
            eff_str_level = math.floor(eff_str_level)
            
        if(self.attack_style.lower() == "aggressive"): eff_str_level += 3
        if(self.attack_style.lower() == "controlled"): eff_str_level += 1
        
        eff_str_level += 8
        return eff_str_level

    def calc_eff_attack_level(self):
        eff_att_level = self.player_att_level
        if(self.super_combat): eff_att_level += 19
        if(self.piety_active):
            eff_att_level *= 1.20
            eff_att_level = math.floor(eff_att_level)
            
        if(self.attack_style.lower() == "accurate"): eff_att_level += 3
        if(self.attack_style.lower() == "controlled"): eff_att_level += 1
        
        eff_att_level += 8
        return eff_att_level

    def calc_att_roll(self, eff_attack_lvl):
        attack_roll = eff_attack_lvl * (self.slash_bonus + 64)
        return math.floor(attack_roll)
        
    def calc_eff_defence_level(self):
        eff_def_lvl = self.player_def_level
        if(self.super_combat): eff_def_lvl += 19
        if(self.piety_active):
            eff_def_lvl *= 1.25
            eff_def_lvl = math.floor(eff_def_lvl)
        if(self.attack_style.lower() == "defensive"): eff_def_lvl += 3
        if(self.attack_style.lower() == "controlled"): eff_def_lvl += 1
        eff_def_lvl += 8
        return eff_def_lvl

    def calc_def_roll(self, eff_def_level):
        def_roll = eff_def_level * (self.slash_def_bonus + 64)
        return def_roll

    def calc_max_hit(self, eff_str_level):
        max_hit = eff_str_level * (self.str_bonus + 64)
        max_hit += 320
        max_hit /= 640
        max_hit = math.floor(max_hit)
        if(self.using_salve): 
            max_hit *= 1.2
        
        
        return math.floor(max_hit)


    def get_hit(self, max_hit):
        return random.randint(0, max_hit)





# eff_str_lvl = calc_eff_strength_level()
# eff_att_lvl = calc_eff_attack_level()
# eff_def_lvl = calc_eff_defence_level()
# att_roll = calc_att_roll(eff_att_lvl)
# def_roll = calc_def_roll(eff_def_lvl)
# max_hit = calc_max_hit(eff_str_lvl)
# print(f"eff strength lvl: {eff_str_lvl}")
# print(f"eff attack lvl: {eff_att_lvl}")
# print(f"attack roll: {att_roll}")
# print(f"defence roll: {def_roll}")
# print(f"max hit: {max_hit}")


# import time
# while(True):
#     print(f"player hit: {get_hit(max_hit)}")
#     time.sleep(1)
    