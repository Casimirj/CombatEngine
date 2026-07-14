from CombatSim.CombatEngine.Factories.PlayerFactory import PlayerFactory


def resolve_player(loadout: str, gear_input, player_levels):
    """Resolve a Player from either a named loadout or custom gear."""
    if loadout.strip().lower() == "custom":
        if gear_input is None:
            raise ValueError("Gear input is required for the Custom loadout.")
        return PlayerFactory.build_player_from_custom_loadout(gear_input.pieces, player_levels)
    return PlayerFactory.build_player_from_simple_loadout(loadout)
