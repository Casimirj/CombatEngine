from CombatSim.CombatEngine.Data.Registries.WeaponRegistry import WeaponRegistry
import math
from CombatSim.CombatEngine.Domain.Rng import Rng

from CombatSim.CombatEngine.Domain.Monster import Monster
from CombatSim.CombatEngine.Domain.Stats import Stats
from CombatSim.CombatEngine.Domain.Weapon import Weapon
from CombatSim.CombatEngine.Domain.Enums.AmmoType import AmmoType


class ZaryteCrossbow(Weapon):
    aliases = ["zcb", "zaryte crossbow", "zaryte cb", "zcb crossbow"]
    _HIT_DELAY_TABLE = {1: 1, 2: 1, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2, 8: 2, 9: 3, 10: 3}

    def __init__(self):
        stats = Stats({
            "ranged_attack_bonus": 110,
            "stab_def": 14,
            "slash_def": 14,
            "crush_def": 12,
            "magic_def": 15,
            "ranged_def_light": 16,
            "ranged_def_med": 16,
            "ranged_def_heavy": 16,
            "prayer_bonus": 1
        })

        super().__init__(
            name="Zaryte crossbow",
            stats=stats,
            combat_style="Ranged",
            attack_type="Ranged",
            attack_style="Rapid",
            attack_speed=6,
            attack_range=8,
            has_special_attack=True,
            ammo_type=AmmoType.BOLTS,
            special_attack_style="Ranged",
            special_attack_cost=75,
        )

    def _calc_ruby_bolt_proc(self, monster: Monster, always_proc: bool = False) -> int:
        """Ruby bolts (e): 11% chance on hit to deal 20% of target HP, capped at 110."""
        if monster is None or monster.current_hp <= 0:
            return 0

        if always_proc or Rng.random() < 0.11:
            bolt_damage = math.floor(monster.current_hp * 0.20)
            return min(bolt_damage, 110)
        return 0

    def do_attack(self, max_hit, player_attack_roll, npc_def_roll, monster: Monster = None, always_hit: bool = False):
        if always_hit:
            damage = Rng.randint(1, max_hit)
            if monster is not None:
                damage += self._calc_ruby_bolt_proc(monster)
            return damage

        if Rng.random() < self.calc_hit_chance(player_attack_roll, npc_def_roll):
            damage = Rng.randint(1, max_hit)
            if monster is not None:
                damage += self._calc_ruby_bolt_proc(monster)
            return damage
        return 0

    def do_special_attack(self, max_hit: int, player_attack_roll: int, npc_def_roll: int, monster: Monster = None, always_hit: bool = False) -> int:
        """Immolate: doubled accuracy, guaranteed ruby bolt (e) proc. Damage is the bolt proc only (110 cap)."""
        adjusted_attack_roll = player_attack_roll * 2

        if always_hit:
            return self._calc_ruby_bolt_proc(monster, always_proc=True) if monster is not None else 0

        if Rng.random() < self.calc_hit_chance(adjusted_attack_roll, npc_def_roll):
            return self._calc_ruby_bolt_proc(monster, always_proc=True) if monster is not None else 0
        return 0


WeaponRegistry.register(ZaryteCrossbow)
