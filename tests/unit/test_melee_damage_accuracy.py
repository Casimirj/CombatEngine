"""Melee damage and accuracy tests for Scythe-based setups.

Add new setups by appending a dict to SETUPS with:
    name                   — snake_case identifier for generated test names
    gear_names             — list of gear registry keys
    weapon                 — weapon registry key
    attack_style_override  — (optional) override weapon attack style
    prayer                 — (optional) Prayer enum; default PIETY
    boosts                 — (optional) list of Potion enums; default [SUPER_COMBAT]
    expected_accuracy_roll — expected player.attack_roll
    expected_max_hit       — expected player.max_hit (base, before Scythe splatting)

Scythe splats: max_hit + floor(max_hit/2) + floor(max_hit/4) = total.
"""

import unittest

from app.GameDefinitions.Loadouts.Custom import Custom
from app.Registries.WeaponRegistry import WeaponRegistry
from app.Enums.prayer import Prayer
from app.Enums.potion import Potion

SETUPS = [
    # ── Basic Setup ───────────────────────────────────────────────────
    {
        "name": "basic_setup",
        "gear_names": [
            "torva full helm",
            "oathplate body",
            "oathplate legs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 39783,
        "expected_max_hit": 50,  # scythe total: 50 + 25 + 12 = 87
    },
    # ── Basic + oathplate helm ────────────────────────────────────────
    {
        "name": "basic_oathplate_helm",
        "gear_names": [
            "oathplate helm",
            "oathplate body",
            "oathplate legs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 41273,
        "expected_max_hit": 49,  # scythe total: 49 + 24 + 12 = 85
    },
    # ── Basic + fire cape ─────────────────────────────────────────────
    {
        "name": "basic_fire_cape",
        "gear_names": [
            "torva full helm",
            "oathplate body",
            "oathplate legs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "fire cape",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 39336,
        "expected_max_hit": 49,  # scythe total: 49 + 24 + 12 = 85
    },
    # ── Basic + no piety ──────────────────────────────────────────────
    {
        "name": "basic_no_piety",
        "gear_names": [
            "torva full helm",
            "oathplate body",
            "oathplate legs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
        ],
        "weapon": "scythe",
        "prayer": Prayer.NONE,
        "expected_accuracy_roll": 33642,
        "expected_max_hit": 41,  # scythe total: 41 + 20 + 10 = 71
    },
    # ── Basic + accurate style ────────────────────────────────────────
    {
        "name": "basic_accurate_style",
        "gear_names": [
            "torva full helm",
            "oathplate body",
            "oathplate legs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
        ],
        "weapon": "scythe",
        "attack_style_override": "Accurate",
        "expected_accuracy_roll": 40584,
        "expected_max_hit": 49,  # scythe total: 49 + 24 + 12 = 85
    },
    # ── Basic + no supercombat ────────────────────────────────────────
    {
        "name": "basic_no_supercombat",
        "gear_names": [
            "torva full helm",
            "oathplate body",
            "oathplate legs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
        ],
        "weapon": "scythe",
        "boosts": [Potion.NONE],
        "expected_accuracy_roll": 33642,
        "expected_max_hit": 42,  # scythe total: 42 + 21 + 10 = 73
    },
    # ── Basic + no supercombat + no piety ─────────────────────────────
    {
        "name": "basic_no_scb_no_piety",
        "gear_names": [
            "torva full helm",
            "oathplate body",
            "oathplate legs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
        ],
        "weapon": "scythe",
        "prayer": Prayer.NONE,
        "boosts": [Potion.NONE],
        "expected_accuracy_roll": 28254,
        "expected_max_hit": 34,  # scythe total: 34 + 17 + 8 = 59
    },
    # ── Basic + torva body + torva legs ───────────────────────────────
    {
        "name": "basic_torva_body_legs",
        "gear_names": [
            "torva full helm",
            "torva platebody",
            "torva platelegs",
            "amulet of rancour",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 35611,
        "expected_max_hit": 51,  # scythe total: 51 + 25 + 12 = 88
    },
    # ── Basic + bandos + no necklace ──────────────────────────────────
    {
        "name": "basic_bandos_no_neck",
        "gear_names": [
            "torva full helm",
            "bandos chestplate",
            "bandos tassets",
            "ultor ring",
            "avernic treads",
            "ferocious gloves",
            "infernal cape",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 31886,
        "expected_max_hit": 47,  # scythe total: 47 + 23 + 11 = 81
    },
    # ── Basic + bandos + no necklace + no gloves ──────────────────────
    {
        "name": "basic_bandos_no_neck_no_gloves",
        "gear_names": [
            "torva full helm",
            "bandos chestplate",
            "bandos tassets",
            "ultor ring",
            "avernic treads",
            "infernal cape",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 29502,
        "expected_max_hit": 44,  # scythe total: 44 + 22 + 11 = 77
    },
    # ── Only Scythe ───────────────────────────────────────────────────
    {
        "name": "only_scythe",
        "gear_names": [],
        "weapon": "scythe",
        "expected_accuracy_roll": 28161,
        "expected_max_hit": 34,  # scythe total: 34 + 17 + 8 = 59
    },
    # ── Only Scythe + ultor ───────────────────────────────────────────
    {
        "name": "only_scythe_ultor",
        "gear_names": [
            "ultor ring",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 28161,
        "expected_max_hit": 37,  # scythe total: 37 + 18 + 9 = 64
    },
    # ── Only Scythe + avernic treads ──────────────────────────────────
    {
        "name": "only_scythe_avernic_treads",
        "gear_names": [
            "avernic treads",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 28906,
        "expected_max_hit": 35,  # scythe total: 35 + 17 + 8 = 60
    },
    # ── Only Scythe + ferocious gloves ────────────────────────────────
    {
        "name": "only_scythe_ferocious_gloves",
        "gear_names": [
            "ferocious gloves",
        ],
        "weapon": "scythe",
        "expected_accuracy_roll": 30545,
        "expected_max_hit": 37,  # scythe total: 37 + 18 + 9 = 64
    },
]


def _make_test_classes():
    """Create one TestCase subclass per setup so VS Code groups accuracy/max hit."""

    for setup in SETUPS:
        setup_name = setup["name"]
        class_name = f"Test_{setup_name}"

        def build_accuracy_test(setup=setup):
            def test(self):
                player = _build_player_from_setup(setup)
                player.calc_all_the_things(combat_style="Melee", attack_type="Slash")
                self.assertEqual(player.attack_roll, setup["expected_accuracy_roll"])
            return test

        def build_max_hit_test(setup=setup):
            def test(self):
                player = _build_player_from_setup(setup)
                player.calc_all_the_things(combat_style="Melee", attack_type="Slash")
                self.assertEqual(player.max_hit, setup["expected_max_hit"])
            return test

        TestCls = type(class_name, (unittest.TestCase,), {
            "test_accuracy_roll": build_accuracy_test(setup),
            "test_max_hit":      build_max_hit_test(setup),
        })
        globals()[class_name] = TestCls


def _build_player_from_setup(setup):
    player = Custom(gear_names=setup["gear_names"]).build()

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
