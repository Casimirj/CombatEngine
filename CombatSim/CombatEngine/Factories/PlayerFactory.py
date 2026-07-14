"""Player factory — build Players from loadouts or setup dicts."""

from __future__ import annotations

from typing import TYPE_CHECKING

from CombatSim.CombatEngine.Data.Definitions.Loadouts import LoadoutRegistry
from CombatSim.CombatEngine.Data.Registries.PotionRegistry import PotionRegistry
from CombatSim.CombatEngine.Data.Registries.PrayerRegistry import PrayerRegistry
from CombatSim.CombatEngine.Data.Registries.SpellRegistry import SpellRegistry
from CombatSim.CombatEngine.Data.Registries.WeaponRegistry import WeaponRegistry
from CombatSim.CombatEngine.Domain.Loadout import Loadout
from CombatSim.CombatEngine.Domain.Stats import Stats

if TYPE_CHECKING:
    from CombatSim.CombatEngine.Domain.Player import Player


class PlayerFactory:

    @staticmethod
    def build_player_from_simple_loadout(name: str) -> Player:
        """Build a Player from a named (registered) loadout."""
        loadout = LoadoutRegistry.get(name)
        if loadout is None:
            raise ValueError(f"Unknown loadout: {name}")
        return loadout.build()

    @staticmethod
    def build_player_from_custom_loadout(
        pieces: list[str],
        player_levels: dict | None = None,
    ) -> Player:
        """Build a Player from a custom list of gear pieces and optional levels."""
        if not pieces:
            raise ValueError("At least one gear piece is required for a custom loadout.")
        levels = Stats(player_levels) if player_levels else None
        return Loadout(gear_names=pieces, player_levels=levels).build()

    @staticmethod
    def build_player_from_setup(setup: dict) -> Player:
        """Build a Player from a setup dictionary.

        Expected keys (all optional except ``gear_names`` and ``weapon``):

        * ``gear_names`` — list of gear registry keys
        * ``weapon``     — weapon registry key
        * ``attack_style_override`` — override the weapon's attack style
        * ``prayer``     — prayer registry key (default: no prayer)
        * ``boosts``     — list of potion registry keys
        * ``spell``      — spell registry key
        """
        player = Loadout(gear_names=setup.get("gear_names", [])).build()

        weapon = WeaponRegistry.get(setup["weapon"])
        player.equip_weapon(weapon)

        if "attack_style_override" in setup:
            player.weapon.attack_style = setup["attack_style_override"]

        if "prayer" in setup:
            player.prayer = PrayerRegistry.get(setup["prayer"])

        if "boosts" in setup:
            player.boosts = [PotionRegistry.get(b) for b in setup["boosts"]]

        if "spell" in setup:
            player.spell = SpellRegistry.get(setup["spell"])

        return player
