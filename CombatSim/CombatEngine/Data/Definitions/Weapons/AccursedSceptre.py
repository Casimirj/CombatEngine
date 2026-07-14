from CombatSim.CombatEngine.Data.Registries.WeaponRegistry import WeaponRegistry
import math
from CombatSim.CombatEngine.Domain.Rng import Rng

from CombatSim.CombatEngine.Domain.Monster import Monster
from CombatSim.CombatEngine.Domain.Stats import Stats
from CombatSim.CombatEngine.Domain.Weapon import Weapon


class AccursedSceptre(Weapon):
    aliases = ["sceptre", "accursed"]

    def __init__(self):

        stats = Stats({
            "magic_attack_bonus": 22,
            "magic_strength_bonus": 0
        })

        super().__init__(
            name="Accursed sceptre",
            stats=stats,
            combat_style="Mage",
            attack_type="Magic",
            attack_style="Autocast",
            attack_speed=4,
            attack_range=7,
            has_special_attack=True,
            special_attack_style="Magic",
            special_attack_cost=50
        )

    def do_special_attack(self, max_hit: int, player_attack_roll: int, npc_def_roll: int, monster: Monster = None, always_hit: bool = False) -> int:
        if always_hit:
            damage = Rng.randint(1, int(max_hit * 1.5))
            if monster is not None:
                monster.reduce_defense(int(damage * 0.15))
                monster.reduce_magic_level(0.15)
            return damage

        adjusted_attack_roll = int(player_attack_roll * 1.5)
        adjusted_max_hit = int(max_hit * 1.5)

        damage = 0
        if Rng.random() < self._calc_hit_chance(adjusted_attack_roll, npc_def_roll):
            damage = Rng.randint(1, adjusted_max_hit)

        if damage > 0 and monster is not None:
            monster.reduce_defense(int(damage * 0.15))
            monster.reduce_magic_level(0.15)

        return damage

WeaponRegistry.register(AccursedSceptre)
