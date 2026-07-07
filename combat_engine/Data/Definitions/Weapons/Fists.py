from combat_engine.Data.Registries.WeaponRegistry import WeaponRegistry

from combat_engine.Domain.Stats import Stats
from combat_engine.Domain.Weapon import Weapon


class Fists(Weapon):
    aliases = ["fists", "unarmed", "punch"]

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

WeaponRegistry.register(Fists)
