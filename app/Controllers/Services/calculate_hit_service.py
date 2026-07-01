from app.Controllers.Models.calculate_hit import CalculateHitInput
from app.GameDefinitions.Loadouts import LoadoutRegistry
from app.Loadout import Loadout
from app.Registries.MonsterRegistry import MonsterRegistry
from app.Registries.WeaponRegistry import WeaponRegistry
from app.Stats import Stats


def _resolve_player(loadout_name: str, gear_input, player_levels: dict | None) -> "Player":
    if loadout_name.strip().lower() == "custom":
        if gear_input is None:
            raise ValueError("Gear input is required for the Custom loadout.")
        levels = Stats(player_levels) if player_levels else None
        return Loadout(gear_names=gear_input.pieces, player_levels=levels).build()

    player = LoadoutRegistry.get(loadout_name)
    if player is None:
        raise ValueError(f"Unknown loadout: {loadout_name}")
    return player


def calculate_hit_damage(payload: CalculateHitInput) -> tuple[int, int]:
    monster = MonsterRegistry.get(payload.monster.name, scale=payload.scale)
    if monster is None:
        raise ValueError(f"Unknown monster: {payload.monster.name}")

    if payload.monster.reduce_defense:
        monster.stats.def_level = int(payload.monster.defense)

    weapon = WeaponRegistry.get(payload.weapon)
    if weapon is None:
        raise ValueError(f"Unknown weapon: {payload.weapon}")

    player = _resolve_player(payload.loadout, payload.gear_input, payload.player_levels)
    player.equip_weapon(weapon)
    damage = player.do_attack(monster)

    return damage, monster.stats.def_level
