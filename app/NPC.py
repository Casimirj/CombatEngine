from typing import Optional, Union
from beartype import beartype

from Stats import Stats


class NPC:


    def reduce_hp(self, amount:int):
        self.current_hp = self.current_hp - amount
        self.current_hp = self.current_hp if self.current_hp >= 0 else 0
        return self.current_hp


    def is_dead(self):
        return self.current_hp == 0
    
    def is_alive(self):
        return self.current_hp > 0
    
    @beartype
    def calc_def_roll(self, attack_style:str=None):
        def_bonus = 0
        if attack_style is not None:
            if attack_style.capitalize() == "Slash": def_bonus = self.stats.slash_def
            if attack_style.capitalize() == "Crush": def_bonus = self.stats.crush_def
            if attack_style.capitalize() == "Stab": def_bonus = self.stats.stab_def

        self.def_roll = (self.stats.def_level + 9) * (def_bonus + 64)
        return self.def_roll

    def reduce_defense(self, damage_amount:int):
        new_def = max(self.stats.def_level - damage_amount, self.minimum_def)
        actual_reduction = self.stats.def_level - new_def
        self.stats.def_level = int(new_def)

    def reduce_defense_dwh(self):
        current_def = self.stats.def_level
        reduce_amount = int(current_def * .30)
        return self.reduce_defense(reduce_amount)

    def reduce_defense_maul(self):
        current_def = self.stats.def_level
        reduce_amount = int(current_def * .35)
        return self.reduce_defense(reduce_amount)
    
    def reduce_defense_ralos(self):
        reduction = self.stats.magic_level / 10
        self.stats.def_level = max(self.stats.def_level - reduction, 0)
    
    def reduce_defense_bgs(self, damage_amount:int):
        remaining_damage = damage_amount
        # Defense reduction
        if remaining_damage > 0 and self.stats.def_level > self.minimum_def:
            max_possible_reduction = self.stats.def_level - self.minimum_def
            reduction = min(remaining_damage, max_possible_reduction)
            self.stats.def_level -= reduction
            remaining_damage -= reduction
        # Strength reduction
        if remaining_damage > 0 and self.stats.strength_level > 0:
            reduction = min(remaining_damage, self.stats.strength_level)
            self.stats.strength_level -= reduction
            remaining_damage -= reduction
        # Prayer reduction
        if remaining_damage > 0 and self.stats.prayer_level > 0:
            reduction = min(remaining_damage, self.stats.prayer_level)
            self.stats.prayer_level -= reduction
            remaining_damage -= reduction
        # Attack reduction
        if remaining_damage > 0 and self.stats.attack_level > 0:
            reduction = min(remaining_damage, self.stats.attack_level)
            self.stats.attack_level -= reduction
            remaining_damage -= reduction
        # Magic reduction
        if remaining_damage > 0 and self.stats.magic_level > 0:
            reduction = min(remaining_damage, self.stats.magic_level)
            self.stats.magic_level -= reduction
            remaining_damage -= reduction
        # Ranged reduction
        if remaining_damage > 0 and self.stats.ranged_level > 0:
            reduction = min(remaining_damage, self.stats.ranged_level)
            self.stats.ranged_level -= reduction
            remaining_damage -= reduction




    def __init__(self, stats:dict=None, weak_to_salve:bool=False, minimum_def:int=0):
        if stats == None:
            raise ValueError("Stats cannot be null")
        self.stats = Stats(stats)

        self.minimum_def = minimum_def
        self.current_hp = self.stats.hp_level
        self.is_weak_to_salve = weak_to_salve
        
        self.def_roll = 0





