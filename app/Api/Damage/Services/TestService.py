from app.Api.Damage.Models.test import TestInput, TestOutput
from app.Factories.PlayerFactory import build_player_from_loadout
from app.Data.Registries.MonsterRegistry import MonsterRegistry
from app.Data.Registries.WeaponRegistry import WeaponRegistry


def run_test(payload: TestInput) -> TestOutput:
    monster = MonsterRegistry.get(payload.monster.name, scale=payload.scale)
    if monster is None:
        raise ValueError(f"Unknown monster: {payload.monster.name}")

    weapon = WeaponRegistry.get(payload.weapon)
    if weapon is None:
        raise ValueError(f"Unknown weapon: {payload.weapon}")

    player = build_player_from_loadout(payload.loadout, payload.gear_input, payload.player_levels)
    player.equip_weapon(weapon)

    hits = 0
    while monster.is_alive():
        hits += 1
        for _ in range(payload.scale):
            damage = player.do_attack(monster)
            monster.reduce_hp(damage)
            if monster.is_dead():
                break

    message = f"Killed {payload.monster.name} in {hits} swings"
    return TestOutput(
        message=message,
        monster_alive=monster.is_alive(),
        hits_to_kill=hits,
        final_damage=monster.current_hp,
    )
