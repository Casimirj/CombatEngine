"""Ranged damage and accuracy tests for Twisted-bow-based setups.

The Twisted bow uses a special scaling mechanic: its accuracy roll and
max hit are multiplied by factors derived from the target's magic level
and magic attack bonus (capped at 250).

Add new setups by appending a dict to SETUPS with:
    name                          — snake_case identifier for generated names
    gear_names                    — list of gear registry keys
    weapon                        — weapon registry key
    ammo                          — ammo gear registry key
    monster                       — monster registry key (e.g. "maiden")
    attack_style_override         — (optional) override weapon attack style
    prayer                        — (optional) Prayer enum; default NONE
    boosts                        — (optional) list of Potion enums
    expected_base_accuracy_roll   — expected player.attack_roll (before tbow multiplier)
    expected_base_max_hit         — expected player.max_hit (before tbow multiplier)
    expected_tbow_accuracy_roll   — expected accuracy roll after tbow multiplier
    expected_tbow_max_hit         — expected max hit after tbow multiplier
"""

import math
import unittest

from app.Loadout import Loadout
from app.Registries.WeaponRegistry import WeaponRegistry
from app.Registries.GearRegistry import GearRegistry
from app.Registries.MonsterRegistry import MonsterRegistry
from app.Enums import Prayer
from app.Enums import Potion

SETUPS = [
    # ── Naked + Twisted Bow + Dragon Arrows vs Maiden ───────────────────
    {
        "name": "naked_tbow_dragon_arrows_vs_maiden",
        "gear_names": [],
        "weapon": "twisted bow",
        "ammo": "dragon arrows",
        "monster": "maiden",
        "prayer": Prayer.NONE,
        "expected_base_accuracy_roll": 14338,
        "expected_base_max_hit": 34,
        "expected_tbow_accuracy_roll": 34411,
        "expected_tbow_max_hit": 107,
    },
]


def _make_test_classes():
    """Create one TestCase subclass per setup."""

    for setup in SETUPS:
        setup_name = setup["name"]
        class_name = f"{setup_name}"

        def build_accuracy_test(setup=setup):
            def test(self):
                player, monster = _build_player_and_monster_from_setup(setup)
                player.calc_all_the_things(combat_style="Ranged", attack_type="Ranged")
                self.assertEqual(
                    player.attack_roll, setup["expected_base_accuracy_roll"],
                    f"\n setup={setup['name']!r}"
                    f"\n gear={setup.get('gear_names', [])}"
                    f"\n expected_base_accuracy_roll={setup['expected_base_accuracy_roll']}"
                    f"\n actual_base_accuracy_roll={player.attack_roll}"
                )
            return test

        def build_max_hit_test(setup=setup):
            def test(self):
                player, monster = _build_player_and_monster_from_setup(setup)
                player.calc_all_the_things(combat_style="Ranged", attack_type="Ranged")
                self.assertEqual(
                    player.max_hit, setup["expected_base_max_hit"],
                    f"\n setup={setup['name']!r}"
                    f"\n gear={setup.get('gear_names', [])}"
                    f"\n expected_base_max_hit={setup['expected_base_max_hit']}"
                    f"\n actual_base_max_hit={player.max_hit}"
                )
            return test

        def build_tbow_accuracy_test(setup=setup):
            def test(self):
                player, monster = _build_player_and_monster_from_setup(setup)
                player.calc_all_the_things(combat_style="Ranged", attack_type="Ranged")
                acc_mult, _ = player.weapon._calc_tbow_multipliers(monster)
                adjusted = math.floor(player.attack_roll * acc_mult)
                self.assertEqual(
                    adjusted, setup["expected_tbow_accuracy_roll"],
                    f"\n setup={setup['name']!r}"
                    f"\n gear={setup.get('gear_names', [])}"
                    f"\n expected_tbow_accuracy_roll={setup['expected_tbow_accuracy_roll']}"
                    f"\n actual_tbow_accuracy_roll={adjusted}"
                )
            return test

        def build_tbow_max_hit_test(setup=setup):
            def test(self):
                player, monster = _build_player_and_monster_from_setup(setup)
                player.calc_all_the_things(combat_style="Ranged", attack_type="Ranged")
                _, dmg_mult = player.weapon._calc_tbow_multipliers(monster)
                adjusted = math.floor(player.max_hit * dmg_mult)
                self.assertEqual(
                    adjusted, setup["expected_tbow_max_hit"],
                    f"\n setup={setup['name']!r}"
                    f"\n gear={setup.get('gear_names', [])}"
                    f"\n expected_tbow_max_hit={setup['expected_tbow_max_hit']}"
                    f"\n actual_tbow_max_hit={adjusted}"
                )
            return test

        TestCls = type(class_name, (unittest.TestCase,), {
            "test_base_accuracy_roll":  build_accuracy_test(setup),
            "test_base_max_hit":        build_max_hit_test(setup),
            "test_tbow_accuracy_roll":  build_tbow_accuracy_test(setup),
            "test_tbow_max_hit":        build_tbow_max_hit_test(setup),
        })
        globals()[class_name] = TestCls


def _build_player_and_monster_from_setup(setup):
    player = Loadout(gear_names=setup["gear_names"]).build()

    weapon = WeaponRegistry.get(setup["weapon"])
    player.equip_weapon(weapon)

    if "ammo" in setup:
        ammo_gear = GearRegistry.get(setup["ammo"])
        if ammo_gear is not None:
            from app.Enums.gear_slot import GearSlot
            player.gear[GearSlot.AMMO] = ammo_gear
            player.compute_gear_stats()

    if "attack_style_override" in setup:
        player.weapon.attack_style = setup["attack_style_override"]

    if "prayer" in setup:
        player.prayer = setup["prayer"]

    if "boosts" in setup:
        player.boosts = setup["boosts"]

    monster_name = setup["monster"]
    monster = MonsterRegistry.get(monster_name, scale=5)
    if monster is None:
        raise ValueError(f"Monster {monster_name!r} not found in registry")

    return player, monster


_make_test_classes()


if __name__ == "__main__":
    unittest.main()
