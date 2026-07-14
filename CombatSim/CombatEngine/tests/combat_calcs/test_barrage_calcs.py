"""Magic damage and accuracy tests for Ice Barrage with Nightmare staff.

Add new setups by appending a dict to SETUPS with:
    name                  — snake_case identifier for generated names
    gear_names            — list of gear registry keys
    weapon                — weapon registry key
    attack_style_override — (optional) override weapon attack style
    prayer                — (optional) Prayer enum; default NONE
    boosts                — (optional) list of Potion enums
    spell                 — (optional) Spell enum for autocast weapons
    expected_accuracy_roll — expected player.attack_roll
    expected_max_hit       — expected player.max_hit
"""

import unittest
from CombatSim.CombatEngine.Factories.PlayerFactory import PlayerFactory

SETUPS = [
    # ── Naked (no prayers, no boosts) ────────────────────────────
    {
        "name": "naked_no_prayer_no_boosts",
        "gear_names": [],
        "weapon": "nightmare",
        "spell": "ice barrage",
        "prayer": "none",
        "expected_accuracy_roll": 8640,
        "expected_max_hit": 34,
    },
    # ── Naked + Augury + Saturated Heart ─────────────────────────
    {
        "name": "naked_barrage",
        "gear_names": [],
        "weapon": "nightmare",
        "spell": "ice barrage",
        "prayer": "augury",
        "boosts": ["saturated heart"],
        "expected_accuracy_roll": 11920,
        "expected_max_hit": 35,
    },
    # ── Max Mage (ancestral + occult + magus + imbued cape + treads) ───
    {
        "name": "max_mage_barrage",
        "gear_names": [
            "ancestral hat",
            "ancestral robe top",
            "ancestral robe bottom",
            "occult necklace",
            "magus ring",
            "imbued saradomin cape",
            "avernic treads",
            "confliction gauntlets",
            "fortified ward",
        ],
        "weapon": "nightmare",
        "spell": "ice barrage",
        "prayer": "augury",
        "boosts": ["saturated heart"],
        "expected_accuracy_roll": 36803,
        "expected_max_hit": 45,
    },
]

def _make_test_classes():
    """Create one TestCase subclass per setup."""

    for setup in SETUPS:
        setup_name = setup["name"]
        class_name = f"{setup_name}"

        def build_accuracy_test(setup=setup):
            def test(self):
                player = PlayerFactory.build_player_from_setup(setup)
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
                player = PlayerFactory.build_player_from_setup(setup)
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

_make_test_classes()

if __name__ == "__main__":
    unittest.main()
