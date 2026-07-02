from app.Data.Definitions.Loadouts import LoadoutRegistry
from app.Domain.Loadout import Loadout
from app.Domain.Stats import Stats


def build_player_from_loadout(loadout_name: str, gear_input, player_levels: dict | None) -> "Player":
    if loadout_name.strip().lower() == "custom":
        if gear_input is None:
            raise ValueError("Gear input is required for the Custom loadout.")
        levels = Stats(player_levels) if player_levels else None
        return Loadout(gear_names=gear_input.pieces, player_levels=levels).build()

    player = LoadoutRegistry.get(loadout_name)
    if player is None:
        raise ValueError(f"Unknown loadout: {loadout_name}")
    return player
