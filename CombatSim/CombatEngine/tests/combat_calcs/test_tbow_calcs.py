"""Ranged damage and accuracy tests for Twisted-bow-based setups.

The Twisted bow uses a special scaling mechanic: its accuracy roll and
max hit are multiplied by factors derived from the target's magic level
and magic attack bonus (capped at 250).
"""

import math
import unittest

from CombatSim.CombatEngine.Data.Registries.MonsterRegistry import MonsterRegistry
from CombatSim.CombatEngine.Factories.PlayerFactory import PlayerFactory

SETUPS = [
    # ── Naked + Twisted Bow + Dragon Arrows vs Maiden ───────────────────
    {
        "name": "maiden_only_dragon_noboosts",
        "gear_names": ["dragon arrows"],
        "weapon": "twisted bow",
        "monster": "maiden",
        "prayer": "none",
        "expected_accuracy_roll": 20216,
        "expected_max_hit": 51,
    },
    # ── Rigour + Ranging + Twisted Bow + Dragon Arrows vs Maiden ─────────
    {
        "name": "maiden_only_dragon",
        "gear_names": ["dragon arrows"],
        "weapon": "twisted bow",
        "monster": "maiden",
        "prayer": "rigour",
        "boosts": ["ranging"],
        "expected_accuracy_roll": 26829,
        "expected_max_hit": 70,
    },
    # ── Naked + Twisted Bow + Dragon Arrows vs Nylo Boss ─────────────────
    {
        "name": "nylo_only_dragon_noboosts",
        "gear_names": ["dragon arrows"],
        "weapon": "twisted bow",
        "monster": "nylo",
        "prayer": "none",
        "expected_accuracy_roll": 20216,
        "expected_max_hit": 51,
    },
    # ── Rigour + Ranging + Twisted Bow + Dragon Arrows vs Nylo Boss ──────
    {
        "name": "nylo_only_dragon",
        "gear_names": ["dragon arrows"],
        "weapon": "twisted bow",
        "monster": "nylo",
        "prayer": "rigour",
        "boosts": ["ranging"],
        "expected_accuracy_roll": 26829,
        "expected_max_hit": 70,
    },
        {
        "name": "maiden_only_Amethyst_noboosts",
        "gear_names": ["amethyst arrows"],
        "weapon": "twisted bow",
        "monster": "maiden",
        "prayer": "none",
        "expected_accuracy_roll": 20216,
        "expected_max_hit": 49,
    },
    # ── Rigour + Ranging + Twisted Bow + Amethyst Arrows vs Maiden ─────────
    {
        "name": "maiden_only_amethyst",
        "gear_names": ["amethyst arrows"],
        "weapon": "twisted bow",
        "monster": "maiden",
        "prayer": "rigour",
        "boosts": ["ranging"],
        "expected_accuracy_roll": 26829,
        "expected_max_hit": 66,
    },
    # ── Naked + Twisted Bow + Amethyst Arrows vs Nylo Boss ─────────────────
    {
        "name": "nylo_only_amethyst_noboosts",
        "gear_names": ["amethyst arrows"],
        "weapon": "twisted bow",
        "monster": "nylo",
        "prayer": "none",
        "expected_accuracy_roll": 20216,
        "expected_max_hit": 49,
    },
    # ── Rigour + Ranging + Twisted Bow + Amethyst Arrows vs Nylo Boss ──────
    {
        "name": "nylo_only_amethyst",
        "gear_names": ["amethyst arrows"],
        "weapon": "twisted bow",
        "monster": "nylo",
        "prayer": "rigour",
        "boosts": ["ranging"],
        "expected_accuracy_roll": 26829,
        "expected_max_hit": 66,
    },
]


def _build_monster_from_setup(setup):
    monster_name = setup["monster"]
    monster = MonsterRegistry.get(monster_name, scale=5)
    if monster is None:
        raise ValueError(f"Monster {monster_name!r} not found in registry")
    return monster


def _make_test_classes():
    """Create one TestCase subclass per setup."""

    for setup in SETUPS:
        setup_name = setup["name"]
        class_name = f"{setup_name}"

        def build_accuracy_test(setup=setup):
            def test(self):
                player = PlayerFactory.build_player_from_setup(setup)
                monster = _build_monster_from_setup(setup)
                player.calc_all_the_things(combat_style="Ranged", attack_type="Ranged")
                acc_mult, _ = player.weapon._calc_tbow_multipliers(monster)
                adjusted = math.floor(player.attack_roll * acc_mult)
                self.assertEqual(
                    adjusted, setup["expected_accuracy_roll"],
                    f"\n setup={setup['name']!r}"
                    f"\n gear={setup.get('gear_names', [])}"
                    f"\n expected_accuracy_roll={setup['expected_accuracy_roll']}"
                    f"\n actual_accuracy_roll={adjusted}"
                )
            return test

        def build_max_hit_test(setup=setup):
            def test(self):
                player = PlayerFactory.build_player_from_setup(setup)
                monster = _build_monster_from_setup(setup)
                player.calc_all_the_things(combat_style="Ranged", attack_type="Ranged")
                _, dmg_mult = player.weapon._calc_tbow_multipliers(monster)
                adjusted = math.floor(player.max_hit * dmg_mult)
                self.assertEqual(
                    adjusted, setup["expected_max_hit"],
                    f"\n setup={setup['name']!r}"
                    f"\n gear={setup.get('gear_names', [])}"
                    f"\n expected_max_hit={setup['expected_max_hit']}"
                    f"\n actual_max_hit={adjusted}"
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
