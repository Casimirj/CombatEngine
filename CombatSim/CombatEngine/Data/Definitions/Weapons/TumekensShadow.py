from CombatSim.CombatEngine.Data.Registries.WeaponRegistry import WeaponRegistry
import math
from CombatSim.CombatEngine.Domain.Rng import Rng

from CombatSim.CombatEngine.Domain.Monster import Monster
from CombatSim.CombatEngine.Domain.Stats import Stats
from CombatSim.CombatEngine.Domain.Weapon import Weapon


class TumekensShadow(Weapon):
    aliases = ["shadow", "tumekens", "tumeken"]
    _HIT_DELAY_TABLE = {1: 2, 2: 3, 3: 3, 4: 3, 5: 4, 6: 4, 7: 4, 8: 5, 9: 5, 10: 5}

    def __init__(self):

        stats = Stats({
            "magic_attack_bonus": 35,
            "magic_strength_bonus": 0,
            "prayer_bonus": 1
        })

        super().__init__(
            name="Tumeken's shadow",
            stats=stats,
            combat_style="Mage",
            attack_type="Magic",
            attack_style="Autocast",
            attack_speed=5,
            attack_range=8,
            has_special_attack=False
        )

    def do_attack(self, max_hit, player_attack_roll, npc_def_roll, monster: Monster = None, always_hit: bool = False):
        adjusted_max_hit = int(max_hit * 4) if (monster and monster.is_toa_monster) else int(max_hit * 3)

        if always_hit:
            return Rng.randint(1, adjusted_max_hit)

        adjusted_attack_roll = player_attack_roll * 4 if (monster and monster.is_toa_monster) else player_attack_roll * 3

        if Rng.random() < self.calc_hit_chance(adjusted_attack_roll, npc_def_roll):
            return Rng.randint(1, adjusted_max_hit)
        else:
            return 0

WeaponRegistry.register(TumekensShadow)
