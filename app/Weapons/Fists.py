
import random
import math
from Weapon import Weapon
from Stats import Stats


class Fists(Weapon):

    def __init__(self):

        stats = Stats({})
                
        super().__init__(
            name="Fists",
            stats=stats,
            combat_style="Melee",
            attack_type="Crush",
            attack_style="Aggressive",
            attack_speed=4,
            attack_range=1,
            has_special_attack=False
        )

