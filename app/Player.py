import json
import math
from beartype import beartype
from typing import Optional, Union

from NPC import NPC
from Stats import Stats
from Weapons.Fists import Fists
from Weapon import Weapon

class Player:

    def is_dead(self):
        return self.current_hp == 0
    def is_alive(self):
        return self.current_hp > 0
    
    @beartype
    def reduce_hp(self, amount:int):
        self.current_hp = self.current_hp - amount
        self.current_hp = self.current_hp if self.current_hp >= 0 else 0
        return self.current_hp
    
    @beartype
    def do_attack(self, monster:NPC, special_attack=False):
        if self.weapon is None:
            self.equip_weapon(Fists())
        if special_attack and self.current_special_attack < self.weapon.special_attack_cost:
            print("We tried to use a special attack but did not have enough energy, so we did a normal attack")
            print(f"{self.weapon.name} requires {self.weapon.special_attack_cost} but we only had {self.current_special_attack}")

        self.calc_all_the_things(self.weapon.attack_type, monster.is_weak_to_salve)
        monster.calc_def_roll(self.weapon.attack_type)

        if special_attack and self.current_special_attack >= self.weapon.special_attack_cost:
            self.current_special_attack -= self.weapon.special_attack_cost
            return self.weapon.do_special_attack(
                max_hit=self.max_hit, 
                player_attack_roll=self.attack_roll, 
                npc_def_roll=monster.def_roll,
                monster=monster
            )
        else:
            return self.weapon.do_attack(
                max_hit=self.max_hit, 
                player_attack_roll=self.attack_roll, 
                npc_def_roll=monster.def_roll
            )


    @beartype
    def equip_weapon(self, weapon:Weapon):
        if self.weapon is not None:
            self.unequip_weapon(self.weapon)
        self.weapon = weapon
        self.stats.increase(extra_stats=weapon.stats)

    @beartype
    def unequip_weapon(self, weapon:Weapon):
        self.stats.decrease(extra_stats=weapon.stats)
        self.weapon = Fists()




    #region Roll Calculation
    @beartype
    def calc_all_the_things(self, attack_style:str=None, monster_weak_to_salve:Optional[bool]=False):
        self.effective_att_level = self.calc_eff_attack_level()
        self.effective_str_level = self.calc_eff_strength_level()
        self.effective_def_level = self.calc_eff_defence_level()
        self.max_hit = self.calc_max_hit(monster_weak_to_salve)
        self.attack_roll = self.calc_att_roll(attack_style, monster_weak_to_salve)
        self.def_roll = self.calc_def_roll(attack_style)
    def calc_eff_attack_level(self):
        eff_att_level = self.stats.attack_level
        if(self.super_combat): eff_att_level += 19
        if(self.piety_active):
            eff_att_level *= 1.20
            eff_att_level = math.floor(eff_att_level)
            
        if(self.weapon.attack_style == "Accurate"): eff_att_level += 3
        if(self.weapon.attack_style == "Controlled"): eff_att_level += 1
        
        eff_att_level += 8
        return eff_att_level
    def calc_eff_strength_level(self):
        eff_str_level = self.stats.strength_level
        
        if(self.super_combat): eff_str_level += 19
        if(self.piety_active):
            eff_str_level *= 1.23
            eff_str_level = math.floor(eff_str_level)
            
        if(self.weapon.attack_style == "Aggressive"): eff_str_level += 3
        if(self.weapon.attack_style == "Controlled"): eff_str_level += 1
        
        eff_str_level += 8
        return eff_str_level
    def calc_eff_defence_level(self):
        eff_def_lvl = self.stats.def_level
        if(self.super_combat): eff_def_lvl += 19
        if(self.piety_active):
            eff_def_lvl *= 1.25
            eff_def_lvl = math.floor(eff_def_lvl)
        if(self.weapon.attack_style == "Defensive"): eff_def_lvl += 3
        if(self.weapon.attack_style == "Controlled"): eff_def_lvl += 1
        eff_def_lvl += 8
        return eff_def_lvl
    @beartype
    def calc_att_roll(self, attack_style:str=None, monster_weak_to_salve:bool=False):
        if attack_style is None:
            raise ValueError("Attack style must be set to calc attack roll")
        attack_bonus = 0
        if attack_style.capitalize() == "Slash": attack_bonus = self.stats.slash_attack_bonus
        if attack_style.capitalize() == "Crush": attack_bonus = self.stats.crush_attack_bonus
        if attack_style.capitalize() == "Stab": attack_bonus = self.stats.stab_attack_bonus
        attack_roll = self.effective_att_level * (attack_bonus + 64)
        if(self.wearing_salve and monster_weak_to_salve):
            attack_roll *= 1.20
        return math.floor(attack_roll)
    @beartype
    def calc_def_roll(self, attack_style:str=None):
        if attack_style is None:
            raise ValueError("Attack style must be set to calc attack roll")
        
        def_bonus = 0
        if attack_style.capitalize() == "Slash": def_bonus = self.stats.slash_def
        if attack_style.capitalize() == "Crush": def_bonus = self.stats.crush_def
        if attack_style.capitalize() == "Stab": def_bonus = self.stats.stab_def

        def_roll = self.effective_def_level * (def_bonus + 64)
        return def_roll
    @beartype
    def calc_max_hit(self, monster_weak_to_salve:bool=False):
        max_hit = self.effective_str_level * (self.stats.melee_strength_bonus + 64)
        max_hit += 320
        max_hit /= 640
        max_hit = math.floor(max_hit)
        if(self.wearing_salve and monster_weak_to_salve): 
            max_hit *= 1.2
        return math.floor(max_hit)
    
    #endregion



    @beartype
    def __init__(self, 
        stats:          dict    =None,
        weapon:         Weapon  =None,
        super_combat:   bool    =True,
        piety_active:   bool    =True,
        wearing_salve:  bool    =False
        ):
        
        if stats is None:
            raise ValueError("Stats cannot be null")
        self.stats = Stats(stats)

        self.current_hp = self.stats.hp_level
        self.current_prayer = self.stats.prayer_level
        self.current_special_attack = 100
        self.current_run = 100

        self.wearing_salve = wearing_salve
        self.super_combat = super_combat
        self.piety_active = piety_active
        self.weapon = weapon

        if self.weapon is None:
            self.equip_weapon(Fists())
        else:
            self.weapon=weapon



        # self.calc_all_the_things(self.weapon.attack_type)
