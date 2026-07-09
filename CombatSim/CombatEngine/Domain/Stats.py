from __future__ import annotations

import json



class Stats:

    LEVEL_KEYS = {
        "hp_level", "attack_level", "strength_level", "def_level",
        "magic_level", "ranged_level", "prayer_level",
    }

    def get_stats(self):
        return vars(self)

    def print_stats(self):
        print(json.dumps(vars(self), sort_keys=True, indent=2))


    def set_default_stats(self):
        # Set all attributes to 0
        self.hp_level = 0
        self.attack_level = 0
        self.strength_level = 0
        self.def_level = 0
        self.magic_level = 0
        self.ranged_level = 0
        self.prayer_level = 0

        self.stab_attack_bonus = 0
        self.slash_attack_bonus = 0
        self.crush_attack_bonus = 0
        self.magic_attack_bonus = 0
        self.ranged_attack_bonus = 0

        self.melee_strength_bonus = 0
        self.ranged_strength_bonus = 0
        self.magic_strength_bonus = 0

        self.slash_def = 0
        self.stab_def = 0
        self.crush_def = 0
        self.magic_def = 0
        self.ranged_def_light = 0
        self.ranged_def_med = 0
        self.ranged_def_heavy = 0


    def copy(self):
        """Return a new Stats object with identical values."""
        new = Stats()
        new.hp_level = self.hp_level
        new.attack_level = self.attack_level
        new.strength_level = self.strength_level
        new.def_level = self.def_level
        new.magic_level = self.magic_level
        new.ranged_level = self.ranged_level
        new.prayer_level = self.prayer_level
        new.stab_attack_bonus = self.stab_attack_bonus
        new.slash_attack_bonus = self.slash_attack_bonus
        new.crush_attack_bonus = self.crush_attack_bonus
        new.magic_attack_bonus = self.magic_attack_bonus
        new.ranged_attack_bonus = self.ranged_attack_bonus
        new.melee_strength_bonus = self.melee_strength_bonus
        new.ranged_strength_bonus = self.ranged_strength_bonus
        new.magic_strength_bonus = self.magic_strength_bonus
        new.slash_def = self.slash_def
        new.stab_def = self.stab_def
        new.crush_def = self.crush_def
        new.magic_def = self.magic_def
        new.ranged_def_light = self.ranged_def_light
        new.ranged_def_med = self.ranged_def_med
        new.ranged_def_heavy = self.ranged_def_heavy
        return new

    def increase(self, extra_stats:Stats):
        """Increase this Stats object's properties by another Stats object's properties"""
        self.hp_level += extra_stats.hp_level
        self.attack_level += extra_stats.attack_level
        self.strength_level += extra_stats.strength_level
        self.def_level += extra_stats.def_level
        self.magic_level += extra_stats.magic_level
        self.ranged_level += extra_stats.ranged_level
        self.prayer_level += extra_stats.prayer_level

        self.stab_attack_bonus += extra_stats.stab_attack_bonus
        self.slash_attack_bonus += extra_stats.slash_attack_bonus
        self.crush_attack_bonus += extra_stats.crush_attack_bonus
        self.magic_attack_bonus += extra_stats.magic_attack_bonus
        self.ranged_attack_bonus += extra_stats.ranged_attack_bonus

        self.melee_strength_bonus += extra_stats.melee_strength_bonus
        self.ranged_strength_bonus += extra_stats.ranged_strength_bonus
        self.magic_strength_bonus += extra_stats.magic_strength_bonus

        self.slash_def += extra_stats.slash_def
        self.stab_def += extra_stats.stab_def
        self.crush_def += extra_stats.crush_def
        self.magic_def += extra_stats.magic_def
        self.ranged_def_light += extra_stats.ranged_def_light
        self.ranged_def_med += extra_stats.ranged_def_med
        self.ranged_def_heavy += extra_stats.ranged_def_heavy

    def decrease(self, extra_stats:Stats):
        """Decrease this Stats object's properties by another Stats object's properties"""
        self.hp_level -= extra_stats.hp_level
        self.attack_level -= extra_stats.attack_level
        self.strength_level -= extra_stats.strength_level
        self.def_level -= extra_stats.def_level
        self.magic_level -= extra_stats.magic_level
        self.ranged_level -= extra_stats.ranged_level
        self.prayer_level -= extra_stats.prayer_level

        self.stab_attack_bonus -= extra_stats.stab_attack_bonus
        self.slash_attack_bonus -= extra_stats.slash_attack_bonus
        self.crush_attack_bonus -= extra_stats.crush_attack_bonus
        self.magic_attack_bonus -= extra_stats.magic_attack_bonus
        self.ranged_attack_bonus -= extra_stats.ranged_attack_bonus

        self.melee_strength_bonus -= extra_stats.melee_strength_bonus
        self.ranged_strength_bonus -= extra_stats.ranged_strength_bonus
        self.magic_strength_bonus -= extra_stats.magic_strength_bonus

        self.slash_def -= extra_stats.slash_def
        self.stab_def -= extra_stats.stab_def
        self.crush_def -= extra_stats.crush_def
        self.magic_def -= extra_stats.magic_def
        self.ranged_def_light -= extra_stats.ranged_def_light
        self.ranged_def_med -= extra_stats.ranged_def_med
        self.ranged_def_heavy -= extra_stats.ranged_def_heavy


    def __init__(self, input_stats:dict=None):
        self.set_default_stats()
        if input_stats is not None:
            self.hp_level = input_stats.get("hp_level") if input_stats.get("hp_level") is not None else self.hp_level
            self.attack_level = input_stats.get("attack_level") if input_stats.get("attack_level") is not None else self.attack_level
            self.strength_level = input_stats.get("strength_level") if input_stats.get("strength_level") is not None else self.strength_level
            self.def_level = input_stats.get("def_level") if input_stats.get("def_level") is not None else self.def_level
            self.magic_level = input_stats.get("magic_level") if input_stats.get("magic_level") is not None else self.magic_level
            self.ranged_level = input_stats.get("ranged_level") if input_stats.get("ranged_level") is not None else self.ranged_level
            self.prayer_level = input_stats.get("prayer_level") if input_stats.get("prayer_level") is not None else self.prayer_level
            
            self.stab_attack_bonus = input_stats.get("stab_attack_bonus") if input_stats.get("stab_attack_bonus") is not None else self.stab_attack_bonus
            self.slash_attack_bonus = input_stats.get("slash_attack_bonus") if input_stats.get("slash_attack_bonus") is not None else self.slash_attack_bonus
            self.crush_attack_bonus = input_stats.get("crush_attack_bonus") if input_stats.get("crush_attack_bonus") is not None else self.crush_attack_bonus
            self.magic_attack_bonus = input_stats.get("magic_attack_bonus") if input_stats.get("magic_attack_bonus") is not None else self.magic_attack_bonus
            self.ranged_attack_bonus = input_stats.get("ranged_attack_bonus") if input_stats.get("ranged_attack_bonus") is not None else self.ranged_attack_bonus
            
            self.melee_strength_bonus = input_stats.get("melee_strength_bonus") if input_stats.get("melee_strength_bonus") is not None else self.melee_strength_bonus
            self.ranged_strength_bonus = input_stats.get("ranged_strength_bonus") if input_stats.get("ranged_strength_bonus") is not None else self.ranged_strength_bonus
            self.magic_strength_bonus = input_stats.get("magic_strength_bonus") if input_stats.get("magic_strength_bonus") is not None else self.magic_strength_bonus
            
            self.slash_def = input_stats.get("slash_def") if input_stats.get("slash_def") is not None else self.slash_def
            self.stab_def = input_stats.get("stab_def") if input_stats.get("stab_def") is not None else self.stab_def
            self.crush_def = input_stats.get("crush_def") if input_stats.get("crush_def") is not None else self.crush_def
            self.magic_def = input_stats.get("magic_def") if input_stats.get("magic_def") is not None else self.magic_def
            self.ranged_def_light = input_stats.get("ranged_def_light") if input_stats.get("ranged_def_light") is not None else self.ranged_def_light
            self.ranged_def_med = input_stats.get("ranged_def_med") if input_stats.get("ranged_def_med") is not None else self.ranged_def_med
            self.ranged_def_heavy = input_stats.get("ranged_def_heavy") if input_stats.get("ranged_def_heavy") is not None else self.ranged_def_heavy
