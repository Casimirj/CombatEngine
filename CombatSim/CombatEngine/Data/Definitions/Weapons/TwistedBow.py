from CombatSim.CombatEngine.Data.Registries.WeaponRegistry import WeaponRegistry
import math
from CombatSim.CombatEngine.Domain.Rng import Rng

from CombatSim.CombatEngine.Domain.Monster import Monster
from CombatSim.CombatEngine.Domain.Stats import Stats
from CombatSim.CombatEngine.Domain.Weapon import Weapon
from CombatSim.CombatEngine.Domain.Enums.AmmoType import AmmoType


class TwistedBow(Weapon):
    aliases = ["tbow", "twisted bow", "bow"]

    def __init__(self):
        stats = Stats({
            "ranged_attack_bonus": 70,
            "ranged_strength_bonus": 20
        })

        super().__init__(
            name="Twisted bow",
            stats=stats,
            combat_style="Ranged",
            attack_type="Ranged",
            attack_style="Rapid",
            attack_speed=6,
            attack_range=10,
            has_special_attack=False,
            ammo_type=AmmoType.ARROWS
        )

    def _calc_tbow_multipliers(self, monster: Monster = None):
        if monster is None:
            return 1.0, 1.0

        magic = max(monster.stats.magic_level, monster.stats.magic_attack_bonus)
        magic = min(magic, 250)

        m = magic
        # RuneScript-style integer division (truncation toward zero)
        acc_mod = 140 + (3 * m - 10) // 100 - (3 * m // 10 - 100) ** 2 // 100
        dmg_mod = 250 + (3 * m - 14) // 100 - (3 * m // 10 - 140) ** 2 // 100

        # Modifier IS the percentage multiplier (141% = 1.41x, 215% = 2.15x)
        acc_mult = acc_mod / 100.0
        dmg_mult = dmg_mod / 100.0
        return acc_mult, dmg_mult

    def do_attack(self, max_hit, player_attack_roll, npc_def_roll, monster: Monster = None, always_hit: bool = False):
        acc_mult, dmg_mult = self._calc_tbow_multipliers(monster)

        adjusted_max_hit = math.floor(max_hit * dmg_mult)

        if always_hit:
            return Rng.randint(1, adjusted_max_hit)

        adjusted_attack_roll = math.floor(player_attack_roll * acc_mult)

        if Rng.random() < self.calc_hit_chance(adjusted_attack_roll, npc_def_roll):
            return Rng.randint(1, adjusted_max_hit)
        else:
            return 0

WeaponRegistry.register(TwistedBow)
