"""Ranged damage and accuracy tests for Toxic-blowpipe-based setups."""

import unittest

from app.Domain.Loadout import Loadout
from app.Data.Registries.WeaponRegistry import WeaponRegistry
from app.Data.Registries.PrayerRegistry import PrayerRegistry
from app.Data.Registries.PotionRegistry import PotionRegistry

SETUPS = [
    # ── Naked + Blowpipe + Dragon Darts ─────────────────────────────────
    {
        "name": "only_dragon_noboosts",
        "gear_names": ["dragon darts"],
        "weapon": "blowpipe",
        "prayer": "none",
        "expected_accuracy_roll": 10058,
        "expected_max_hit": 20,
    },
    # ── Rigour + Ranging + Blowpipe + Dragon Darts ──────────────────────
    {
        "name": "only_dragon",
        "gear_names": ["dragon darts"],
        "weapon": "blowpipe",
        "prayer": "rigour",
        "boosts": ["ranging"],
        "expected_accuracy_roll": 13348,
        "expected_max_hit": 27,
    },
]


def _make_test_classes():
    """Create one TestCase subclass per setup."""

    for setup in SETUPS:
        setup_name = setup["name"]
        class_name = f"{setup_name}"

        def build_accuracy_test(setup=setup):
            def test(self):
                player = _build_player_from_setup(setup)
                player.calc_all_the_things(combat_style="Ranged", attack_type="Ranged")
                self.assertEqual(
                    player.attack_roll, setup["expected_accuracy_roll"],
                    f"\n setup={setup['name']!r}"
                    f"\n gear={setup.get('gear_names', [])}"
                    f"\n expected_accuracy_roll={setup['expected_accuracy_roll']}"
                    f"\n actual_accuracy_roll={player.attack_roll}"
                )
            return test

        def build_max_hit_test(setup=setup):
            def test(self):
                player = _build_player_from_setup(setup)
                player.calc_all_the_things(combat_style="Ranged", attack_type="Ranged")
                self.assertEqual(
                    player.max_hit, setup["expected_max_hit"],
                    f"\n setup={setup['name']!r}"
                    f"\n gear={setup.get('gear_names', [])}"
                    f"\n expected_max_hit={setup['expected_max_hit']}"
                    f"\n actual_max_hit={player.max_hit}"
                )
            return test

        TestCls = type(class_name, (unittest.TestCase,), {
            "test_accuracy_roll":  build_accuracy_test(setup),
            "test_max_hit":        build_max_hit_test(setup),
        })
        globals()[class_name] = TestCls


def _build_player_from_setup(setup):
    player = Loadout(gear_names=setup["gear_names"]).build()

    weapon = WeaponRegistry.get(setup["weapon"])
    player.equip_weapon(weapon)

    if "attack_style_override" in setup:
        player.weapon.attack_style = setup["attack_style_override"]

    if "prayer" in setup:
        player.prayer = PrayerRegistry.get(setup["prayer"])

    if "boosts" in setup:
        player.boosts = [PotionRegistry.get(b) for b in setup["boosts"]]

    return player


_make_test_classes()


if __name__ == "__main__":
    unittest.main()
