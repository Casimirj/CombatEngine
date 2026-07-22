"""Ranged damage and accuracy tests for Toxic-blowpipe-based setups."""

import unittest
from CombatSim.CombatEngine.Factories.PlayerFactory import PlayerFactory

SETUPS = [
    # ── Naked + Blowpipe + Dragon Darts ─────────────────────────────────
    {
        "name": "only_dragon_noboosts",
        "gear_names": [
            "dragon darts",
        ],
        "weapon": "blowpipe",
        "prayer": "none",
        "expected_accuracy_roll": 10058,
        "expected_max_hit": 20,
    },
    # ── Rigour + Ranging + Blowpipe + Dragon Darts ──────────────────────
    {
        "name": "only_dragon",
        "gear_names": [
            "dragon darts",
        ],
        "weapon": "blowpipe",
        "prayer": "rigour",
        "boosts": [
            "ranging",
        ],
        "expected_accuracy_roll": 13348,
        "expected_max_hit": 27,
    },
    # ── Rupture + Quiver + Blowpipe + Dragon Darts (no boosts) ──────────
    {
        "name": "rupture_quiver_noboosts",
        "gear_names": [
            "dragon darts",
            "necklace of rupture",
            "quiver",
        ],
        "weapon": "blowpipe",
        "prayer": "none",
        "expected_accuracy_roll": 14124,
        "expected_max_hit": 22,
    },
    # ── Rupture + Quiver + Rigour + Ranging + Blowpipe ──────────────────
    {
        "name": "rupture_quiver",
        "gear_names": [
            "dragon darts",
            "necklace of rupture",
            "quiver",
        ],
        "weapon": "blowpipe",
        "prayer": "rigour",
        "boosts": [
            "ranging",
        ],
        "expected_accuracy_roll": 18744,
        "expected_max_hit": 29,
    },
    # ── Full Masori + Anguish + Quiver + Blowpipe (no boosts) ───────────
    {
        "name": "full_masori_noboosts",
        "gear_names": [
            "dragon darts",
            "masori mask",
            "masori body",
            "masori chaps",
            "necklace of anguish",
            "quiver",
        ],
        "weapon": "blowpipe",
        "prayer": "none",
        "expected_accuracy_roll": 22363,
        "expected_max_hit": 23,
    },
    # ── Full Masori + Anguish + Quiver + Rigour + Ranging ───────────────
    {
        "name": "full_masori",
        "gear_names": [
            "dragon darts",
            "masori mask",
            "masori body",
            "masori chaps",
            "necklace of anguish",
            "quiver",
        ],
        "weapon": "blowpipe",
        "prayer": "rigour",
        "boosts": [
            "ranging",
        ],
        "expected_accuracy_roll": 29678,
        "expected_max_hit": 31,
    },
    # ── MaxVoid (Full Elite Void Ranged + Rupture + Treads + Quiver) ────────
    {
        "name": "maxvoid_dragon_noboosts",
        "gear_names": [
            "dragon darts",
            "elite void top",
            "elite void robe",
            "void ranger helm",
            "void knight gloves",
            "necklace of rupture",
            "avernic treads",
            "quiver",
        ],
        "weapon": "blowpipe",
        "prayer": "none",
        "expected_accuracy_roll": 18918,
        "expected_max_hit": 24,
    },
    {
        "name": "maxvoid_dragon",
        "gear_names": [
            "dragon darts",
            "elite void top",
            "elite void robe",
            "void ranger helm",
            "void knight gloves",
            "necklace of rupture",
            "avernic treads",
            "quiver",
        ],
        "weapon": "blowpipe",
        "prayer": "rigour",
        "boosts": [
            "ranging",
        ],
        "expected_accuracy_roll": 25225,
        "expected_max_hit": 33,
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
                player = PlayerFactory.build_player_from_setup(setup)
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

_make_test_classes()

if __name__ == "__main__":
    unittest.main()
