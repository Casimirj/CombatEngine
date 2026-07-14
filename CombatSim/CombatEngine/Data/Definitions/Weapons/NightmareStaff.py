from CombatSim.CombatEngine.Data.Registries.WeaponRegistry import WeaponRegistry
from CombatSim.CombatEngine.Domain.Rng import Rng

from CombatSim.CombatEngine.Domain.Monster import Monster
from CombatSim.CombatEngine.Domain.Stats import Stats
from CombatSim.CombatEngine.Domain.Weapon import Weapon


class NightmareStaff(Weapon):
    aliases = ["nightmare", "staff", "nm"]

    def __init__(self):
        stats = Stats({
            "magic_attack_bonus": 16,
            "magic_strength_bonus": 15
        })

        super().__init__(
            name="Nightmare staff",
            stats=stats,
            combat_style="Mage",
            attack_type="Magic",
            attack_style="Autocast",
            attack_speed=5,
            attack_range=7,
            has_special_attack=False
        )


    def do_attack(self, max_hit, player_attack_roll, npc_def_roll, monster: Monster = None, always_hit: bool = False):
        if always_hit:
            return Rng.randint(1, max_hit)

        if Rng.random() < self.calc_hit_chance(player_attack_roll, npc_def_roll):
            return Rng.randint(1, max_hit)
        return 0

WeaponRegistry.register(NightmareStaff)
