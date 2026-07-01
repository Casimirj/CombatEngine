"""Unit tests for app.Enums — Potion, Prayer, GearSlot."""

import unittest
import math
from app.Enums import Potion, Prayer, GearSlot


class TestPotionComputeBoost(unittest.TestCase):
    def test_positive_percentage(self):
        self.assertEqual(Potion.compute_boost(99, 0.15, 5),
                         math.floor(99 * 0.15) + 5)

    def test_zero_percentage(self):
        self.assertEqual(Potion.compute_boost(99, 0.0, 3), 3)

    def test_negative_percentage(self):
        self.assertEqual(Potion.compute_boost(99, -0.10, -2),
                         -math.floor(99 * 0.10) - 2)

    def test_floor_behaviour_positive(self):
        result = Potion.compute_boost(98, 0.15, 5)
        self.assertEqual(result, 19)  # floor(98*0.15)=14, +5 = 19

    def test_floor_behaviour_negative(self):
        result = Potion.compute_boost(98, -0.10, -2)
        self.assertEqual(result, -11)  # -floor(9.8)-2 = -9-2 = -11


class TestPotionLabels(unittest.TestCase):
    def test_super_combat_has_label(self):
        self.assertEqual(Potion.SUPER_COMBAT.label, "Super combat")

    def test_none_has_label(self):
        self.assertEqual(Potion.NONE.label, "None")

    def test_zamorak_brew_has_negative_defence(self):
        self.assertLess(Potion.ZAMORAK_BREW.defence_percentage, 0)


class TestPrayerProperties(unittest.TestCase):
    def test_piety_values(self):
        p = Prayer.PIETY
        self.assertEqual(p.attack_multiplier, 1.20)
        self.assertEqual(p.strength_multiplier, 1.23)
        self.assertEqual(p.defence_multiplier, 1.25)
        self.assertEqual(p.ranged_attack_multiplier, 0.0)

    def test_rigour_values(self):
        r = Prayer.RIGOUR
        self.assertAlmostEqual(r.ranged_attack_multiplier, 1.20)
        self.assertAlmostEqual(r.ranged_strength_multiplier, 1.23)
        self.assertEqual(r.attack_multiplier, 0.0)

    def test_augury_values(self):
        a = Prayer.AUGURY
        self.assertAlmostEqual(a.magic_attack_multiplier, 1.25)
        self.assertAlmostEqual(a.magic_damage_bonus, 0.04)

    def test_none_prayer(self):
        n = Prayer.NONE
        self.assertEqual(n.attack_multiplier, 0.0)
        self.assertEqual(n.strength_multiplier, 0.0)

    def test_backward_compat_aliases(self):
        p = Prayer.PIETY
        self.assertEqual(p.atk_mult, p.attack_multiplier)
        self.assertEqual(p.str_mult, p.strength_multiplier)
        self.assertEqual(p.def_mult, p.defence_multiplier)


class TestGearSlot(unittest.TestCase):
    def test_distinct_values(self):
        slots = list(GearSlot)
        self.assertEqual(len(slots), 11)
        values = {s.value for s in slots}
        self.assertEqual(len(values), 11)

    def test_expected_members(self):
        self.assertIn(GearSlot.HEAD, GearSlot)
        self.assertIn(GearSlot.WEAPON, GearSlot)
        self.assertIn(GearSlot.OFFHAND, GearSlot)
        self.assertIn(GearSlot.RING, GearSlot)


class TestPotionBoostIntegrity(unittest.TestCase):
    """Sanity-checks that potions have all required fields."""

    def test_every_potion_has_required_fields(self):
        required = [
            "label", "attack_percentage", "attack_flat",
            "strength_percentage", "strength_flat",
            "defence_percentage", "defence_flat",
            "ranged_percentage", "ranged_flat",
            "magic_percentage", "magic_flat",
        ]
        for potion in Potion:
            for field in required:
                with self.subTest(potion=potion, field=field):
                    self.assertTrue(hasattr(potion, field),
                                    f"{potion.name} missing {field}")

    def test_no_potion_crashes_compute_boost(self):
        level = 99
        for potion in Potion:
            with self.subTest(potion=potion):
                Potion.compute_boost(level, potion.attack_percentage, potion.attack_flat)
                Potion.compute_boost(level, potion.strength_percentage, potion.strength_flat)
                Potion.compute_boost(level, potion.defence_percentage, potion.defence_flat)


class TestPrayerIntegrity(unittest.TestCase):
    def test_every_prayer_has_required_fields(self):
        required = [
            "label", "attack_multiplier", "strength_multiplier",
            "defence_multiplier", "ranged_attack_multiplier",
            "ranged_strength_multiplier", "magic_attack_multiplier",
            "magic_damage_bonus",
        ]
        for prayer in Prayer:
            for field in required:
                with self.subTest(prayer=prayer, field=field):
                    self.assertTrue(hasattr(prayer, field),
                                    f"{prayer.name} missing {field}")


if __name__ == "__main__":
    unittest.main()
