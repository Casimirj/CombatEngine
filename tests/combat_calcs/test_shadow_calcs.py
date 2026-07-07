"""Magic damage and accuracy tests for Tumeken's-shadow-based setups.

The Tumeken's shadow triples both the accuracy roll and max hit.
These tests verify the base values (pre-multiplier) and the shadow-adjusted
values (3×) separately.

Add new setups by appending a dict to SETUPS with:
    name                        — snake_case identifier for generated names
    gear_names                  — list of gear registry keys
    weapon                      — weapon registry key
    attack_style_override       — (optional) override weapon attack style
    prayer                      — (optional) Prayer enum; default NONE
    boosts                      — (optional) list of Potion enums
    expected_base_accuracy_roll — expected player.attack_roll (before 3×)
    expected_base_max_hit       — expected player.max_hit (before 3×)
    expected_shadow_accuracy_roll — expected accuracy roll after 3×
    expected_shadow_max_hit       — expected max hit after 3×
"""

import unittest

from combat_engine.Domain.Loadout import Loadout
from combat_engine.Data.Registries.WeaponRegistry import WeaponRegistry
from combat_engine.Data.Registries.PrayerRegistry import PrayerRegistry
from combat_engine.Data.Registries.PotionRegistry import PotionRegistry

SETUPS = [
    # ── Naked + Shadow ─────────────────────────────────────────────
    {
        "name": "naked_shadow",
        "gear_names": [],
        "weapon": "tumeken",
        "prayer": "none",
        "expected_base_accuracy_roll": 10692,
        "expected_base_max_hit": 37,
        "expected_shadow_accuracy_roll": 32076,
        "expected_shadow_max_hit": 111,
    },
    # ── Max Mage (ancestral + occult + magus + imbued cape + treads) ───
    {
        "name": "max_mage_shadow",
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
        "weapon": "tumeken",
        "prayer": "augury",
        "expected_base_accuracy_roll": 31812,
        "expected_base_max_hit": 59,
        "expected_shadow_accuracy_roll": 95436,
        "expected_shadow_max_hit": 177,
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
                    player.attack_roll, setup["expected_base_accuracy_roll"],
                    f"\n setup={setup['name']!r}"
                    f"\n gear={setup.get('gear_names', [])}"
                    f"\n expected_base_accuracy_roll={setup['expected_base_accuracy_roll']}"
                    f"\n actual_base_accuracy_roll={player.attack_roll}"
                )
            return test

        def build_max_hit_test(setup=setup):
            def test(self):
                player = _build_player_from_setup(setup)
                player.calc_all_the_things(combat_style="Mage", attack_type="Magic")
                self.assertEqual(
                    player.max_hit, setup["expected_base_max_hit"],
                    f"\n setup={setup['name']!r}"
                    f"\n gear={setup.get('gear_names', [])}"
                    f"\n expected_base_max_hit={setup['expected_base_max_hit']}"
                    f"\n actual_base_max_hit={player.max_hit}"
                )
            return test

        def build_shadow_accuracy_test(setup=setup):
            def test(self):
                player = _build_player_from_setup(setup)
                player.calc_all_the_things(combat_style="Mage", attack_type="Magic")
                adjusted = player.attack_roll * 3
                self.assertEqual(
                    adjusted, setup["expected_shadow_accuracy_roll"],
                    f"\n setup={setup['name']!r}"
                    f"\n gear={setup.get('gear_names', [])}"
                    f"\n expected_shadow_accuracy_roll={setup['expected_shadow_accuracy_roll']}"
                    f"\n actual_shadow_accuracy_roll={adjusted}"
                )
            return test

        def build_shadow_max_hit_test(setup=setup):
            def test(self):
                player = _build_player_from_setup(setup)
                player.calc_all_the_things(combat_style="Mage", attack_type="Magic")
                adjusted = int(player.max_hit * 3)
                self.assertEqual(
                    adjusted, setup["expected_shadow_max_hit"],
                    f"\n setup={setup['name']!r}"
                    f"\n gear={setup.get('gear_names', [])}"
                    f"\n expected_shadow_max_hit={setup['expected_shadow_max_hit']}"
                    f"\n actual_shadow_max_hit={adjusted}"
                )
            return test

        TestCls = type(class_name, (unittest.TestCase,), {
            "test_base_accuracy_roll":   build_accuracy_test(setup),
            "test_base_max_hit":         build_max_hit_test(setup),
            "test_shadow_accuracy_roll": build_shadow_accuracy_test(setup),
            "test_shadow_max_hit":       build_shadow_max_hit_test(setup),
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
