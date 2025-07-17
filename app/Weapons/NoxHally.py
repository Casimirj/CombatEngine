
import random
import math
from Weapon import Weapon
from Stats import Stats


class NoxHally(Weapon):

    def __init__(self):

        stats = Stats({
            "stab_attack_bonus": 80,
            "slash_attack_bonus": 132,
            "crush_attack_bonus": 0,
            "melee_strength_bonus": 142
        })

                
        super().__init__(
            name="Noxious Haleberd",
            stats=stats,
            combat_style="Melee",
            attack_type="Slash",
            attack_style="Aggressive",
            attack_speed=5,
            attack_range=2,
            has_special_attack=False
        )

