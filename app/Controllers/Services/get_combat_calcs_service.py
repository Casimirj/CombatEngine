from app.Controllers.Models.get_combat_calcs import GetCombatCalcsInput, GetCombatCalcsOutput
from app.Controllers.Models.get_combat_calcs.response import PlayerInfo, PlayerStats, PlayerGear, PlayerSetup
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


def _build_player_info(player) -> PlayerInfo:
    stats = player.stats
    return PlayerInfo(
        stats=PlayerStats(
            attack_level=stats.attack_level,
            strength_level=stats.strength_level,
            defence_level=stats.def_level,
            ranged_level=stats.ranged_level,
            magic_level=stats.magic_level,
            hitpoints_level=stats.hp_level,
            stab_attack_bonus=stats.stab_attack_bonus,
            slash_attack_bonus=stats.slash_attack_bonus,
            crush_attack_bonus=stats.crush_attack_bonus,
            magic_attack_bonus=stats.magic_attack_bonus,
            ranged_attack_bonus=stats.ranged_attack_bonus,
            melee_strength_bonus=stats.melee_strength_bonus,
            ranged_strength_bonus=stats.ranged_strength_bonus,
            magic_strength_bonus=stats.magic_strength_bonus,
            stab_defence_bonus=stats.stab_def,
            slash_defence_bonus=stats.slash_def,
            crush_defence_bonus=stats.crush_def,
            magic_defence_bonus=stats.magic_def,
        ),
        gear=PlayerGear(
            weapon_name=player.weapon.name,
            weapon_attack_style=player.weapon.attack_style,
            weapon_attack_type=player.weapon.attack_type,
        ),
        setup=PlayerSetup(
            prayer=player.prayer.label,
            boosts=[potion.label for potion in player.boosts],
            wearing_salve=player.wearing_salve,
        ),
    )


def get_combat_calcs(payload: GetCombatCalcsInput) -> GetCombatCalcsOutput:
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

    player.calc_all_the_things(player.weapon.combat_style, player.weapon.attack_type, monster.is_weak_to_salve)
    monster.calc_def_roll(player.weapon.attack_type)

    if player.attack_roll > monster.def_roll:
        hit_chance = 1 - (monster.def_roll + 2) / (2 * (player.attack_roll + 1))
    else:
        hit_chance = player.attack_roll / (2 * (monster.def_roll + 1))

    return GetCombatCalcsOutput(
        player=_build_player_info(player),
        effective_attack_level=getattr(player, "effective_att_level", 0),
        effective_strength_level=getattr(player, "effective_str_level", 0),
        effective_defence_level=getattr(player, "effective_def_level", 0),
        effective_ranged_attack_level=player.calc_eff_ranged_attack_level(),
        effective_ranged_strength_level=player.calc_eff_ranged_strength_level(),
        effective_magic_level=player.calc_eff_magic_level(),
        max_hit=player.max_hit,
        player_attack_roll=player.attack_roll,
        player_defence_roll=getattr(player, "def_roll", 0),
        npc_defence_roll=monster.def_roll,
        hit_chance=hit_chance,
    )
