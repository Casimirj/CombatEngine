"""Unit tests for app.Stats."""

import unittest
from CombatSim.CombatEngine.Domain.Stats import Stats


class TestStatsDefaults(unittest.TestCase):
    def setUp(self):
        self.s = Stats()

    def test_default_levels_are_zero(self):
        self.assertEqual(self.s.hp_level, 0)
        self.assertEqual(self.s.attack_level, 0)
        self.assertEqual(self.s.strength_level, 0)
        self.assertEqual(self.s.def_level, 0)
        self.assertEqual(self.s.magic_level, 0)
        self.assertEqual(self.s.ranged_level, 0)
        self.assertEqual(self.s.prayer_level, 0)

    def test_default_attack_bonuses_are_zero(self):
        self.assertEqual(self.s.stab_attack_bonus, 0)
        self.assertEqual(self.s.slash_attack_bonus, 0)
        self.assertEqual(self.s.crush_attack_bonus, 0)
        self.assertEqual(self.s.magic_attack_bonus, 0)
        self.assertEqual(self.s.ranged_attack_bonus, 0)

    def test_default_strength_bonuses_are_zero(self):
        self.assertEqual(self.s.melee_strength_bonus, 0)
        self.assertEqual(self.s.ranged_strength_bonus, 0)
        self.assertEqual(self.s.magic_strength_bonus, 0)

    def test_default_defence_bonuses_are_zero(self):
        self.assertEqual(self.s.stab_def, 0)
        self.assertEqual(self.s.slash_def, 0)
        self.assertEqual(self.s.crush_def, 0)
        self.assertEqual(self.s.magic_def, 0)
        self.assertEqual(self.s.ranged_def_light, 0)
        self.assertEqual(self.s.ranged_def_med, 0)
        self.assertEqual(self.s.ranged_def_heavy, 0)


class TestStatsInitWithDict(unittest.TestCase):
    def test_partial_dict_keeps_defaults(self):
        s = Stats({"hp_level": 99, "attack_level": 80})
        self.assertEqual(s.hp_level, 99)
        self.assertEqual(s.attack_level, 80)
        self.assertEqual(s.strength_level, 0)

    def test_dict_maps_attack_bonuses(self):
        s = Stats({"stab_attack_bonus": 50, "slash_attack_bonus": 60})
        self.assertEqual(s.stab_attack_bonus, 50)
        self.assertEqual(s.slash_attack_bonus, 60)

    def test_dict_maps_defence_bonuses(self):
        s = Stats({"stab_def": 100, "magic_def": 80})
        self.assertEqual(s.stab_def, 100)
        self.assertEqual(s.magic_def, 80)

    def test_dict_maps_strength_bonuses(self):
        s = Stats({"melee_strength_bonus": 75, "ranged_strength_bonus": 40})
        self.assertEqual(s.melee_strength_bonus, 75)
        self.assertEqual(s.ranged_strength_bonus, 40)

    def test_none_values_ignored(self):
        s = Stats({"hp_level": None, "attack_level": 70})
        self.assertEqual(s.hp_level, 0)
        self.assertEqual(s.attack_level, 70)


class TestStatsIncrease(unittest.TestCase):
    def setUp(self):
        self.a = Stats({"attack_level": 80, "strength_level": 70, "stab_attack_bonus": 50})
        self.b = Stats({"attack_level": 20, "strength_level": 15, "stab_attack_bonus": 25})

    def test_increase_adds_levels(self):
        self.a.increase(self.b)
        self.assertEqual(self.a.attack_level, 100)
        self.assertEqual(self.a.strength_level, 85)

    def test_increase_adds_bonuses(self):
        self.a.increase(self.b)
        self.assertEqual(self.a.stab_attack_bonus, 75)

    def test_increase_does_not_affect_unrelated_stats(self):
        old_hp = self.a.hp_level
        self.a.increase(self.b)
        self.assertEqual(self.a.hp_level, old_hp)


class TestStatsDecrease(unittest.TestCase):
    def setUp(self):
        self.a = Stats({"attack_level": 100, "strength_level": 85, "stab_attack_bonus": 50})
        self.b = Stats({"attack_level": 20, "strength_level": 15, "stab_attack_bonus": 25})

    def test_decrease_subtracts_levels(self):
        self.a.decrease(self.b)
        self.assertEqual(self.a.attack_level, 80)
        self.assertEqual(self.a.strength_level, 70)

    def test_decrease_subtracts_bonuses(self):
        self.a.decrease(self.b)
        self.assertEqual(self.a.stab_attack_bonus, 25)

    def test_decrease_can_go_negative(self):
        s = Stats({"attack_level": 5})
        s.decrease(Stats({"attack_level": 10}))
        self.assertEqual(s.attack_level, -5)


class TestStatsGetStats(unittest.TestCase):
    def test_get_stats_returns_dict_with_all_fields(self):
        s = Stats({"hp_level": 99})
        d = s.get_stats()
        self.assertIsInstance(d, dict)
        self.assertEqual(d["hp_level"], 99)
        self.assertEqual(d["strength_level"], 0)


if __name__ == "__main__":
    unittest.main()
