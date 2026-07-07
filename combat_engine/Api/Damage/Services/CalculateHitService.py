from combat_engine.Api.Damage.Models.calculate_hit import CalculateHitInput
from combat_engine.Factories.PlayerFactory import build_player_from_loadout
from combat_engine.Data.Registries.MonsterRegistry import MonsterRegistry
from combat_engine.Data.Registries.WeaponRegistry import WeaponRegistry


def calculate_hit_damage(payload: CalculateHitInput) -> tuple[int, int]:
    monster = MonsterRegistry.get(payload.monster.name, scale=payload.scale)
    if monster is None:
        raise ValueError(f"Unknown monster: {payload.monster.name}")

    if payload.monster.reduce_defense:
        monster.stats.def_level = int(payload.monster.defense)

    weapon = WeaponRegistry.get(payload.weapon)
    if weapon is None:
        raise ValueError(f"Unknown weapon: {payload.weapon}")

    player = build_player_from_loadout(payload.loadout, payload.gear_input, payload.player_levels)
    player.equip_weapon(weapon)
    damage = player.do_attack(monster, always_hit=payload.always_hit)

    return damage, monster.stats.def_level
