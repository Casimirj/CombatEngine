from CombatSim.CombatEngine.Data.Registries.WeaponRegistry import WeaponRegistry
from CombatSim.CombatEngine.Domain.Rng import Rng

from CombatSim.CombatEngine.Domain.Monster import Monster
from CombatSim.CombatEngine.Domain.Stats import Stats
from CombatSim.CombatEngine.Domain.Weapon import Weapon


class EyeOfAyak(Weapon):
    aliases = ["ayak", "eye of ayak"]

    def __init__(self):
        stats = Stats({
            "magic_attack_bonus": 30,
            "magic_strength_bonus": 0
        })

        super().__init__(
            name="Eye of ayak",
            stats=stats,
            combat_style="Mage",
            attack_type="Magic",
            attack_style="Autocast",
            attack_speed=3,
            attack_range=6,
            has_special_attack=True,
            special_attack_style="Magic",
            special_attack_cost=50
        )

    def do_attack(self, max_hit, player_attack_roll, npc_def_roll, monster: Monster = None, always_hit: bool = False):
        if always_hit:
            return Rng.randint(1, max_hit)

        if player_attack_roll > npc_def_roll:
            hit_chance = 1 - (npc_def_roll + 2) / (2 * (player_attack_roll + 1))
        else:
            hit_chance = player_attack_roll / (2 * (npc_def_roll + 1))

        if Rng.random() < hit_chance:
            return Rng.randint(1, max_hit)
        return 0

    def do_special_attack(self, max_hit: int, player_attack_roll: int, npc_def_roll: int, monster: Monster = None, always_hit: bool = False) -> int:
        if always_hit:
            damage = Rng.randint(1, int(max_hit * 1.3))
            if monster is not None and damage > 0:
                monster.stats.magic_def = max(0, monster.stats.magic_def - damage)
            return damage

        adjusted_attack_roll = player_attack_roll * 2
        adjusted_max_hit = int(max_hit * 1.3)

        if adjusted_attack_roll > npc_def_roll:
            hit_chance = 1 - (npc_def_roll + 2) / (2 * (adjusted_attack_roll + 1))
        else:
            hit_chance = adjusted_attack_roll / (2 * (npc_def_roll + 1))

        damage = 0
        if Rng.random() < hit_chance:
            damage = Rng.randint(1, adjusted_max_hit)
            if monster is not None and damage > 0:
                monster.stats.magic_def = max(0, monster.stats.magic_def - damage)

        return damage

WeaponRegistry.register(EyeOfAyak)
