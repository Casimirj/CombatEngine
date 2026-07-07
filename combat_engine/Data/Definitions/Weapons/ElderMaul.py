from combat_engine.Data.Registries.WeaponRegistry import WeaponRegistry

from combat_engine.Domain.Monster import Monster
from combat_engine.Domain.Stats import Stats
from combat_engine.Domain.Weapon import Weapon


class ElderMaul(Weapon):
    aliases = ["maul", "elder"]

    def __init__(self):

        stats = Stats({
            "crush_attack_bonus": 135,
            "melee_strength_bonus": 147
        })

                
        super().__init__(
            name="Elder Maul",
            stats=stats,
            combat_style="Melee",
            attack_type="Crush",
            attack_style="Accurate",
            attack_speed=6,
            attack_range=1,
            has_special_attack=True,
            special_attack_style="Crush",
            special_attack_cost=50
        )
        
    def do_special_attack(self, max_hit:int, player_attack_roll:int, npc_def_roll:int, monster:Monster, always_hit: bool = False) -> int:
        adjusted_attack_roll = int(player_attack_roll * 1.25)
        hit = super().do_attack(max_hit, adjusted_attack_roll, npc_def_roll, always_hit=always_hit)
        if hit > 0:
            monster.reduce_defense_maul()
        return hit

WeaponRegistry.register(ElderMaul)
