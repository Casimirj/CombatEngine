from CombatSim.CombatEngine.Data.Registries.WeaponRegistry import WeaponRegistry
from CombatSim.CombatEngine.Domain.Rng import Rng

from CombatSim.CombatEngine.Domain.Monster import Monster
from CombatSim.CombatEngine.Domain.Stats import Stats
from CombatSim.CombatEngine.Domain.Weapon import Weapon
from CombatSim.CombatEngine.Domain.Enums.AmmoType import AmmoType


class ToxicBlowpipe(Weapon):
    aliases = ["blowpipe", "bp", "pipe"]

    def __init__(self):
        stats = Stats({
            "ranged_attack_bonus": 30,
            "ranged_strength_bonus": 20
        })

        super().__init__(
            name="Toxic blowpipe",
            stats=stats,
            combat_style="Ranged",
            attack_type="Ranged",
            attack_style="Rapid",
            attack_speed=3,
            attack_range=5,
            has_special_attack=True,
            ammo_type=AmmoType.DARTS,
            special_attack_style="Ranged",
            special_attack_cost=50
        )

    def do_attack(self, max_hit, player_attack_roll, npc_def_roll, monster: Monster = None, always_hit: bool = False):
        if always_hit:
            damage = Rng.randint(1, max_hit)
            if Rng.random() < 0.25:
                damage += 6
            return damage

        if Rng.random() < self._calc_hit_chance(player_attack_roll, npc_def_roll):
            damage = Rng.randint(1, max_hit)
            if Rng.random() < 0.25:
                damage += 6
            return damage
        return 0

    def do_special_attack(self, max_hit: int, player_attack_roll: int, npc_def_roll: int, monster: Monster = None, always_hit: bool = False) -> int:
        if always_hit:
            return Rng.randint(1, int(max_hit * 1.5))

        adjusted_attack_roll = player_attack_roll * 2
        adjusted_max_hit = int(max_hit * 1.5)

        if Rng.random() < self._calc_hit_chance(adjusted_attack_roll, npc_def_roll):
            return Rng.randint(1, adjusted_max_hit)
        else:
            return 0

WeaponRegistry.register(ToxicBlowpipe)
