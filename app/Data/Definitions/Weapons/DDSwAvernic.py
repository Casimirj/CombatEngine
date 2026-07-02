from app.Data.Registries.WeaponRegistry import WeaponRegistry
from app.Domain.Monster import Monster
from app.Domain.Stats import Stats
from app.Domain.Weapon import Weapon


class DDSwAvernic(Weapon):
    aliases = ["dds", "dragon dagger", "ddp++"]

    def __init__(self):
        stats = Stats({
            "stab_attack_bonus": 70,
            "slash_attack_bonus": 54,
            "melee_strength_bonus": 48
        })   
        super().__init__(
            name="Dragon Dagger",
            stats=stats,
            combat_style="Melee",
            attack_type="Stab",
            attack_style="Aggressive",
            attack_speed=4,
            attack_range=1,
            has_special_attack=True,
            special_attack_style="Stab",
            special_attack_cost=25
        )
        
    def do_special_attack(self, max_hit:int, player_attack_roll:int, npc_def_roll:int, monster:Monster, always_hit: bool = False) -> int:
        # Dragon Dagger special: Two hits with 15% accuracy and damage boost (1.15x multiplier)
        adjusted_attack_roll = int(player_attack_roll * 1.15)
        adjusted_max_hit = int(max_hit * 1.15)
        
        # First hit
        hit1 = super().do_attack(adjusted_max_hit, adjusted_attack_roll, npc_def_roll, always_hit=always_hit)
        
        # Second hit
        hit2 = super().do_attack(adjusted_max_hit, adjusted_attack_roll, npc_def_roll, always_hit=always_hit)
        
        total_hit = hit1 + hit2
        
        return total_hit

WeaponRegistry.register(DDSwAvernic)
