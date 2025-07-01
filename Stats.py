


class Stats:

    def __init__(self):

        # base stats
        self.hp_level = 0
        self.attack_level = 0
        self.strength_level = 0
        self.def_level = 0
        self.magic_level = 0
        self.ranged_level = 0

        # attack stats
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

    def __init__(self, stats=None):

        # Set all attributes to 0
        self.hp_level = 0
        self.attack_level = 0
        self.strength_level = 0
        self.def_level = 0
        self.magic_level = 0
        self.ranged_level = 0

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



        # Merge provided stats with defaults
        if stats is not None:
            self.update(stats)

    def get_stats(self):
        return self.stats.__dict__