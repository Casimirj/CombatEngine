from CombatSim.CombatEngine.Factories.PlayerFactory import PlayerFactory


def resolve_player(loadout: str, gear_input, player_levels, prayer=None, boosts=None):
    """Resolve a Player from either a named loadout or custom gear."""
    if loadout.strip().lower() == "custom":
        pieces = gear_input.pieces if gear_input else []
        return PlayerFactory.build_player_from_loadout(
            pieces=pieces, player_levels=player_levels, prayer=prayer, boosts=boosts,
        )
    return PlayerFactory.build_player_from_loadout(name=loadout)
