"""Player factory — build Players from loadouts or setup dicts."""

from __future__ import annotations

from typing import TYPE_CHECKING, overload

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

    # ── overloads for build_player_from_loadout ────────────────────────

    @overload
    @staticmethod
    def build_player_from_loadout(*, name: str) -> Player: ...

    @overload
    @staticmethod
    def build_player_from_loadout(*, pieces: list[str], player_levels: dict | None = None, prayer: str | None = None, boosts: list[str] | None = None) -> Player: ...

    @staticmethod
    def build_player_from_loadout(*, name: str | None = None, pieces: list[str] | None = None, player_levels: dict | None = None, prayer: str | None = None, boosts: list[str] | None = None) -> Player:
        """Build a Player from a named loadout **or** custom gear pieces.

        **Named loadout**::

            PlayerFactory.build_player_from_loadout(name="OathTorvaSalve")

        **Custom gear**::

            PlayerFactory.build_player_from_loadout(
                pieces=["Salve (e)"],
                player_levels={"attack_level": 80},
                prayer="piety",
                boosts=["super combat"],
            )
        """
        if name is not None:
            loadout = LoadoutRegistry.get(name)
            if loadout is None:
                raise ValueError(f"Unknown loadout: {name}")
            return loadout.build()

        if pieces is None or not pieces:
            raise ValueError("Either name or pieces must be provided.")
        levels = Stats(player_levels) if player_levels else None
        player = Loadout(gear_names=pieces, player_levels=levels).build()
        if prayer is not None:
            player.prayer = PrayerRegistry.get(prayer)
        if boosts is not None:
            player.boosts = [PotionRegistry.get(b) for b in boosts]
        return player

    # ── build_player_from_setup ────────────────────────────────────────

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
