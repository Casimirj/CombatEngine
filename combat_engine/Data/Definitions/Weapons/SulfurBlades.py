from combat_engine.Data.Registries.WeaponRegistry import WeaponRegistry
import random

from combat_engine.Domain.Stats import Stats
from combat_engine.Domain.Weapon import Weapon


class SulfurBlades(Weapon):
    aliases = ["sulfur", "blades"]

    def __init__(self):

        stats = Stats({
            "stab_attack_bonus": 11,
            "slash_attack_bonus": 72,
            "crush_attack_bonus": 0,
            "melee_strength_bonus": 64
        })

      ##I need to doublecheck if we wanted this set to stab or slash
        super().__init__(
            name="Sulfur Blades",
            stats = stats,
            combat_style="Melee",
            attack_type="Slash",
            attack_style="Aggressive",
            attack_speed=4,
            attack_range=1,
            has_special_attack=False
        )


    def do_attack(self, max_hit, player_attack_roll, npc_def_roll, monster=None, always_hit: bool = False):

        if always_hit:
            return random.randint(1, max_hit) + random.randint(1, max_hit)

        hit_def_roll = random.randint(1, npc_def_roll)

        splat_1_hit = random.randint(1, player_attack_roll) >= hit_def_roll
        splat_2_hit = random.randint(1, player_attack_roll) >= hit_def_roll
        
        damage_total = 0

        if splat_1_hit:
            damage_total += random.randint(1, max_hit)
        if splat_2_hit:
            damage_total += random.randint(1, max_hit)
       
        return damage_total

WeaponRegistry.register(SulfurBlades)
