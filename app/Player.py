import math
from Stats import Stats
from Weapons.Fists import Fists

class Player:

    def is_dead(self):
        return self.current_hp == 0
    def is_alive(self):
        return self.current_hp > 0
    
    def reduce_hp(self, amount):
        self.current_hp = self.current_hp - amount
        self.current_hp = self.current_hp if self.current_hp >= 0 else 0
        return self.current_hp
    
    def do_attack(self, monster):
        if(self.weapon is None):
            self.equip_weapon(Fists())
        
        self.calc_all_the_things(monster_weak_to_salve=monster.is_weak_to_salve)

        return self.weapon.do_attack(
            max_hit=self.max_hit, 
            player_attack_roll=self.attack_roll, 
            npc_def_roll=monster.def_roll
        )

    def equip_weapon(self, weapon):
        if self.weapon is not None:
            self.unequip_weapon(self.weapon)
        self.weapon = weapon

        self.stats.increase(extra_stats=weapon.stats)
        self.calc_all_the_things()

    def unequip_weapon(self, weapon):
        self.stats.decrease(extra_stats=weapon.stats)
        self.weapon = Fists()
        self.calc_all_the_things()



    #region Roll Calculation
    def calc_all_the_things(self, monster_weak_to_salve=False):
        self.attack_style = self.weapon.attack_style
        self.effective_att_level = self.calc_eff_attack_level()
        self.effective_str_level = self.calc_eff_strength_level()
        self.effective_def_level = self.calc_eff_defence_level()
        self.max_hit = self.calc_max_hit(monster_weak_to_salve)
        self.attack_roll = self.calc_att_roll(monster_weak_to_salve)
        self.def_roll = self.calc_def_roll()

    def calc_eff_attack_level(self):
        eff_att_level = self.stats.attack_level
        if(self.super_combat): eff_att_level += 19
        if(self.piety_active):
            eff_att_level *= 1.20
            eff_att_level = math.floor(eff_att_level)
            
        if(self.attack_style == "Accurate"): eff_att_level += 3
        if(self.attack_style == "Controlled"): eff_att_level += 1
        
        eff_att_level += 8
        return eff_att_level
    def calc_eff_strength_level(self):
        eff_str_level = self.stats.strength_level
        
        if(self.super_combat): eff_str_level += 19
        if(self.piety_active):
            eff_str_level *= 1.23
            eff_str_level = math.floor(eff_str_level)
            
        if(self.attack_style == "Aggressive"): eff_str_level += 3
        if(self.attack_style == "Controlled"): eff_str_level += 1
        
        eff_str_level += 8
        return eff_str_level
    def calc_eff_defence_level(self):
        eff_def_lvl = self.stats.def_level
        if(self.super_combat): eff_def_lvl += 19
        if(self.piety_active):
            eff_def_lvl *= 1.25
            eff_def_lvl = math.floor(eff_def_lvl)
        if(self.attack_style == "Defensive"): eff_def_lvl += 3
        if(self.attack_style == "Controlled"): eff_def_lvl += 1
        eff_def_lvl += 8
        return eff_def_lvl
    def calc_att_roll(self, monster_weak_to_salve=False):
        attack_roll = self.effective_att_level * (self.stats.slash_attack_bonus + 64)
        if(self.wearing_salve and monster_weak_to_salve):
            attack_roll *= 1.20
        return math.floor(attack_roll)
    def calc_def_roll(self):
        def_roll = self.effective_def_level * (self.stats.slash_def + 64)
        return def_roll
    def calc_max_hit(self, monster_weak_to_salve=False):
        max_hit = self.effective_str_level * (self.stats.melee_strength_bonus + 64)
        max_hit += 320
        max_hit /= 640
        max_hit = math.floor(max_hit)
        if(self.wearing_salve and monster_weak_to_salve): 
            max_hit *= 1.2
        return math.floor(max_hit)
    #endregion


    def __init__(self, 
        stats=None,
        weapon=None,
        super_combat=True,
        piety_active=True,
        wearing_salve=False
        ):
        
        if stats is None:
            raise ValueError("Stats cannot be null")
        self.stats = Stats(stats)

        self.current_hp = self.stats.hp_level
        self.current_prayer = self.stats.prayer_level

        self.wearing_salve = wearing_salve
        self.super_combat = super_combat
        self.piety_active = piety_active
        self.weapon = weapon

        if self.weapon is None:
            self.equip_weapon(Fists())
        else:
            self.weapon=weapon



        self.calc_all_the_things()
