
import math
import Stats

class NPC:

    def __init__(self, stats=None):
        if stats == None:
            raise ValueError("Stats cannot be null")
        self.stats = Stats(stats)




    def calc_def_roll(self):
        def_roll = (self.def_level + 9) * (self.slash_def + 64)
        return def_roll
    

    def reduce_defense(self, amount):
        self.def_level = self.stats.def_level - amount
        return self.def_level

    def reduce_defense_dwh(self):
        current_def = self.stats.def_level
        reduce_amount = current_def * .30
        return self.reduce_defense(reduce_amount)

    def reduce_defense_maul(self):
        current_def = self.stats.def_level
        reduce_amount = current_def * .35
        return self.reduce_defense(reduce_amount)



    def reduce_defense_bgs(self, amount):
        return self.reduce_defense(amount)



# print(f"Monster Def Roll {calc_def_roll()}")



