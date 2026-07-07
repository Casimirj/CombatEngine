from combat_engine.Data.Registries.WeaponRegistry import WeaponRegistry
import math
import random

from combat_engine.Domain.Monster import Monster
from combat_engine.Domain.Stats import Stats
from combat_engine.Domain.Weapon import Weapon
from combat_engine.Domain.Enums.AmmoType import AmmoType


class TwistedBow(Weapon):
    aliases = ["tbow", "twisted bow", "bow"]

    def __init__(self):
        stats = Stats({
            "ranged_attack_bonus": 70,
            "ranged_strength_bonus": 80
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
        acc_raw = 140.0 + (10.0 * 3.0 * m / 10.0 - 10.0) / 100.0 - ((3.0 * m / 10.0 - 100.0) ** 2) / 100.0
        dmg_raw = 250.0 + (10.0 * 3.0 * m / 10.0 - 14.0) / 100.0 - ((3.0 * m / 10.0 - 140.0) ** 2) / 100.0

        acc_modifier = max(0.0, min(140.0, acc_raw))
        dmg_modifier = max(0.0, min(250.0, dmg_raw))

        acc_mult = 1.0 + acc_modifier / 100.0
        dmg_mult = 1.0 + dmg_modifier / 100.0
        return acc_mult, dmg_mult

    def do_attack(self, max_hit, player_attack_roll, npc_def_roll, monster: Monster = None, always_hit: bool = False):
        acc_mult, dmg_mult = self._calc_tbow_multipliers(monster)

        adjusted_max_hit = math.floor(max_hit * dmg_mult)

        if always_hit:
            return random.randint(1, adjusted_max_hit)

        adjusted_attack_roll = math.floor(player_attack_roll * acc_mult)

        if adjusted_attack_roll > npc_def_roll:
            hit_chance = 1 - (npc_def_roll + 2) / (2 * (adjusted_attack_roll + 1))
        else:
            hit_chance = adjusted_attack_roll / (2 * (npc_def_roll + 1))

        if random.random() < hit_chance:
            return random.randint(1, adjusted_max_hit)
        else:
            return 0

WeaponRegistry.register(TwistedBow)
