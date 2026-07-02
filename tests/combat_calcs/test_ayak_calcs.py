"""Magic damage and accuracy tests for Eye-of-ayak-based setups.

Add new setups by appending a dict to SETUPS with:
    name                  — snake_case identifier for generated names
    gear_names            — list of gear registry keys
    weapon                — weapon registry key
    attack_style_override — (optional) override weapon attack style
    prayer                — (optional) Prayer enum; default NONE
    boosts                — (optional) list of Potion enums
    expected_accuracy_roll — expected player.attack_roll
    expected_max_hit       — expected player.max_hit
"""

import unittest

from app.Domain.Loadout import Loadout
from app.Data.Registries.WeaponRegistry import WeaponRegistry
from app.Domain.Enums import Prayer
from app.Domain.Enums import Potion

SETUPS = [
    # ── Naked + Ayak ─────────────────────────────────────────────
    {
        "name": "naked_ayak",
        "gear_names": [],
        "weapon": "ayak",
        "prayer": Prayer.NONE,
        "expected_accuracy_roll": 10152,
        "expected_max_hit": 37,
    },
    # ── Max Mage (ancestral + occult + magus + imbued cape + treads) ───
    {
        "name": "max_mage_ayak",
        "gear_names": [
            "ancestral hat",
            "ancestral robe top",
            "ancestral robe bottom",
            "occult necklace",
            "magus ring",
            "imbued saradomin cape",
            "avernic treads",
            "confliction gauntlets",
        ],
        "weapon": "ayak",
        "prayer": Prayer.AUGURY,
        "expected_accuracy_roll": 31152,
        "expected_max_hit": 59,
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
                player.calc_all_the_things(combat_style="Mage", attack_type="Magic")
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
                player.calc_all_the_things(combat_style="Mage", attack_type="Magic")
                self.assertEqual(
                    player.max_hit, setup["expected_max_hit"],
                    f"\n setup={setup['name']!r}"
                    f"\n gear={setup.get('gear_names', [])}"
                    f"\n expected_max_hit={setup['expected_max_hit']}"
                    f"\n actual_max_hit={player.max_hit}"
                )
            return test

        TestCls = type(class_name, (unittest.TestCase,), {
            "test_accuracy_roll": build_accuracy_test(setup),
            "test_max_hit":       build_max_hit_test(setup),
        })
        globals()[class_name] = TestCls


def _build_player_from_setup(setup):
    player = Loadout(gear_names=setup["gear_names"]).build()

    weapon = WeaponRegistry.get(setup["weapon"])
    player.equip_weapon(weapon)

    if "attack_style_override" in setup:
        player.weapon.attack_style = setup["attack_style_override"]

    if "prayer" in setup:
        player.prayer = setup["prayer"]

    if "boosts" in setup:
        player.boosts = setup["boosts"]

    return player


_make_test_classes()


if __name__ == "__main__":
    unittest.main()
