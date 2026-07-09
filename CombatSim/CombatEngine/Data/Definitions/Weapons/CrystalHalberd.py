from CombatSim.CombatEngine.Data.Registries.WeaponRegistry import WeaponRegistry
from CombatSim.CombatEngine.Domain.Rng import Rng


from CombatSim.CombatEngine.Domain.Monster import Monster
from CombatSim.CombatEngine.Domain.Stats import Stats
from CombatSim.CombatEngine.Domain.Weapon import Weapon


class CrystalHalberd(Weapon):
    aliases = ["chally", "halberd"]

    def __init__(self):
        stats = Stats({
            "slash_attack_bonus": 110,
            "stab_attack_bonus": 85,
            "melee_strength_bonus": 118
        })   
        super().__init__(
            name="Crystal Halberd",
            stats=stats,
            combat_style="Melee",
            attack_type="Slash",
            attack_style="Aggressive",
            attack_speed=7,
            attack_range=2,
            has_special_attack=True,
            special_attack_style="Slash",
            special_attack_cost=30
        )
    
    def do_special_attack(self, max_hit:int, player_attack_roll:int, npc_def_roll:int, monster:Monster, always_hit: bool = False) -> int:
        if always_hit:
            return Rng.randint(1, int(max_hit * 1.1)) + Rng.randint(1, int(max_hit * 1.1))

        hit_def_roll = Rng.randint(1, npc_def_roll)

        splat_1_hit = Rng.randint(1, player_attack_roll) >= hit_def_roll
        splat_2_hit = Rng.randint(1, int(player_attack_roll*.75)) >= hit_def_roll
        
        damage_total = 0

        if splat_1_hit:
            damage_total += Rng.randint(1, int(max_hit*1.1))
        if splat_2_hit:
            damage_total += Rng.randint(1, int(max_hit*1.1))
        
        return damage_total
            
        

WeaponRegistry.register(CrystalHalberd)
