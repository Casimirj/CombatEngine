"""Unit tests for app.Weapon."""

import unittest
from unittest.mock import patch, MagicMock
from app.Weapon import Weapon
from app.Stats import Stats


class TestWeaponInit(unittest.TestCase):
    def setUp(self):
        self.stats = Stats({"stab_attack_bonus": 80, "melee_strength_bonus": 70})

    def test_valid_melee_weapon(self):
        w = Weapon(
            name="abyssal whip",
            stats=self.stats,
            combat_style="Melee",
            attack_type="Slash",
            attack_style="Accurate",
            attack_speed=4,
            attack_range=1,
            has_special_attack=True,
            special_attack_style="Accurate",
            special_attack_cost=50,
        )
        self.assertEqual(w.name, "Abyssal whip")
        self.assertEqual(w.combat_style, "Melee")
        self.assertEqual(w.attack_speed, 4)

    def test_valid_ranged_weapon(self):
        w = Weapon(
            name="twisted bow",
            stats=self.stats,
            combat_style="Ranged",
            attack_type="Ranged",
            attack_style="Accurate",
            attack_speed=5,
            attack_range=10,
            has_special_attack=False,
        )
        self.assertEqual(w.name, "Twisted bow")

    def test_valid_magic_weapon(self):
        w = Weapon(
            name="tumeken's shadow",
            stats=self.stats,
            combat_style="Mage",
            attack_type="Magic",
            attack_style="Autocast",
            attack_speed=5,
            attack_range=8,
            has_special_attack=False,
        )
        self.assertEqual(w.combat_style, "Mage")

    def test_no_special_attack_without_style_raises(self):
        with self.assertRaises(ValueError):
            Weapon(
                name="broken",
                stats=self.stats,
                combat_style="Melee",
                attack_type="Slash",
                attack_style="Aggressive",
                attack_speed=4,
                attack_range=1,
                has_special_attack=True,
                special_attack_style=None,
            )

    def test_default_attack_range(self):
        w = Weapon(
            name="fists",
            stats=self.stats,
            combat_style="Melee",
            attack_type="Crush",
            attack_style="Aggressive",
            attack_speed=4,
            attack_range=None,
            has_special_attack=False,
        )
        self.assertEqual(w.attack_range, 1)

    def test_rapid_ranged_reduces_speed(self):
        w = Weapon(
            name="toxic blowpipe",
            stats=self.stats,
            combat_style="Ranged",
            attack_type="Ranged",
            attack_style="Rapid",
            attack_speed=3,
            attack_range=5,
            has_special_attack=False,
        )
        self.assertEqual(w.attack_speed, 2)

    def test_rapid_ranged_min_speed_one(self):
        w = Weapon(
            name="fast bow",
            stats=self.stats,
            combat_style="Ranged",
            attack_type="Ranged",
            attack_style="Rapid",
            attack_speed=1,
            attack_range=5,
            has_special_attack=False,
        )
        self.assertEqual(w.attack_speed, 1)

    def test_special_attack_cost_defaults_to_zero(self):
        w = Weapon(
            name="simple weapon",
            stats=self.stats,
            combat_style="Melee",
            attack_type="Slash",
            attack_style="Aggressive",
            attack_speed=4,
            attack_range=1,
            has_special_attack=False,
        )
        self.assertEqual(w.special_attack_cost, 0)


class TestWeaponAttack(unittest.TestCase):
    def setUp(self):
        self.stats = Stats({"stab_attack_bonus": 80})
        self.w = Weapon(
            name="test sword",
            stats=self.stats,
            combat_style="Melee",
            attack_type="Slash",
            attack_style="Aggressive",
            attack_speed=4,
            attack_range=1,
            has_special_attack=False,
        )

    def test_hit_when_attack_roll_exceeds_def_roll(self):
        with patch("random.random", return_value=0.1):
            damage = self.w.do_attack(max_hit=50, player_attack_roll=20000, npc_def_roll=10000)
            self.assertGreater(damage, 0)
            self.assertLessEqual(damage, 50)

    def test_miss_when_random_above_hit_chance(self):
        with patch("random.random", return_value=0.99):
            damage = self.w.do_attack(max_hit=50, player_attack_roll=10000, npc_def_roll=10000)
            self.assertEqual(damage, 0)

    def test_miss_when_attack_roll_below_def_roll(self):
        with patch("random.random", return_value=0.5):
            damage = self.w.do_attack(max_hit=50, player_attack_roll=5000, npc_def_roll=10000)
            self.assertEqual(damage, 0)


class TestWeaponSpecialAttack(unittest.TestCase):
    def setUp(self):
        self.stats = Stats({"stab_attack_bonus": 80})
        self.normal = Weapon(
            name="normal weapon",
            stats=self.stats,
            combat_style="Melee",
            attack_type="Slash",
            attack_style="Aggressive",
            attack_speed=4,
            attack_range=1,
            has_special_attack=False,
        )

    def test_no_special_falls_back_to_normal_attack(self):
        with patch("random.random", return_value=0.1):
            damage = self.normal.do_special_attack(max_hit=50, player_attack_roll=20000, npc_def_roll=10000)
            self.assertGreater(damage, 0)

    def test_unimplemented_special_raises_reference_error(self):
        w = Weapon(
            name="spec weapon",
            stats=self.stats,
            combat_style="Melee",
            attack_type="Slash",
            attack_style="Aggressive",
            attack_speed=4,
            attack_range=1,
            has_special_attack=True,
            special_attack_style="Aggressive",
            special_attack_cost=50,
        )
        with self.assertRaises(ReferenceError):
            w.do_special_attack(max_hit=50, player_attack_roll=20000, npc_def_roll=10000)


if __name__ == "__main__":
    unittest.main()
