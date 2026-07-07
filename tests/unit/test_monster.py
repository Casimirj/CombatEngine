"""Unit tests for app.Monster."""

import unittest
from combat_engine.Domain.Monster import Monster
from combat_engine.Domain.Stats import Stats


class TestMonsterInit(unittest.TestCase):
    def test_init_sets_stats(self):
        m = Monster({"hp_level": 250, "strength_level": 200})
        self.assertEqual(m.stats.hp_level, 250)
        self.assertEqual(m.stats.strength_level, 200)

    def test_init_defaults(self):
        m = Monster({"hp_level": 100})
        self.assertEqual(m.current_hp, 100)
        self.assertEqual(m.minimum_def, 0)
        self.assertFalse(m.is_weak_to_salve)
        self.assertEqual(m.def_roll, 0)

    def test_init_weak_to_salve(self):
        m = Monster({"hp_level": 100}, weak_to_salve=True)
        self.assertTrue(m.is_weak_to_salve)

    def test_init_minimum_def(self):
        m = Monster({"hp_level": 100}, minimum_def=50)
        self.assertEqual(m.minimum_def, 50)

    def test_init_fails_without_stats(self):
        with self.assertRaises(ValueError):
            Monster(None)

    def test_init_fails_with_none(self):
        with self.assertRaises(ValueError):
            Monster()


class TestMonsterHP(unittest.TestCase):
    def setUp(self):
        self.m = Monster({"hp_level": 100})

    def test_reduce_hp(self):
        self.m.reduce_hp(30)
        self.assertEqual(self.m.current_hp, 70)

    def test_reduce_hp_not_below_zero(self):
        self.m.reduce_hp(150)
        self.assertEqual(self.m.current_hp, 0)

    def test_is_alive(self):
        self.assertTrue(self.m.is_alive())
        self.assertFalse(self.m.is_dead())

    def test_is_dead_after_lethal_damage(self):
        self.m.reduce_hp(100)
        self.assertTrue(self.m.is_dead())
        self.assertFalse(self.m.is_alive())


class TestMonsterDefRoll(unittest.TestCase):
    def test_no_combat_style_no_attack_type(self):
        m = Monster({"def_level": 80, "slash_def": 120})
        roll = m.calc_def_roll()
        # (level + 9) * (0 + 64) = 89 * 64
        self.assertEqual(roll, (80 + 9) * 64)

    def test_slash_def_uses_slash_bonus(self):
        m = Monster({"def_level": 80, "slash_def": 120})
        roll = m.calc_def_roll(attack_type="Slash")
        self.assertEqual(roll, (80 + 9) * (120 + 64))

    def test_crush_def_uses_crush_bonus(self):
        m = Monster({"def_level": 80, "crush_def": 200})
        roll = m.calc_def_roll(attack_type="Crush")
        self.assertEqual(roll, (80 + 9) * (200 + 64))

    def test_stab_def_uses_stab_bonus(self):
        m = Monster({"def_level": 80, "stab_def": 150})
        roll = m.calc_def_roll(attack_type="Stab")
        self.assertEqual(roll, (80 + 9) * (150 + 64))

    def test_ranged_uses_ranged_def_light(self):
        m = Monster({"def_level": 70, "ranged_def_light": 100})
        roll = m.calc_def_roll(combat_style="Ranged")
        self.assertEqual(roll, (70 + 9) * (100 + 64))

    def test_mage_uses_magic_def_and_magic_level(self):
        m = Monster({"def_level": 70, "magic_def": 80, "magic_level": 90})
        roll = m.calc_def_roll(combat_style="Mage")
        self.assertEqual(roll, (90 + 9) * (80 + 64))


class TestMonsterDefenseReduction(unittest.TestCase):
    def test_reduce_defense_basic(self):
        m = Monster({"hp_level": 100, "def_level": 80})
        m.reduce_defense(30)
        self.assertEqual(m.stats.def_level, 50)

    def test_reduce_defense_respects_minimum(self):
        m = Monster({"hp_level": 100, "def_level": 80}, minimum_def=60)
        m.reduce_defense(30)
        self.assertEqual(m.stats.def_level, 60)

    def test_reduce_defense_dwh_30_percent(self):
        m = Monster({"hp_level": 100, "def_level": 100})
        m.reduce_defense_dwh()
        self.assertEqual(m.stats.def_level, 70)

    def test_reduce_defense_maul_35_percent(self):
        m = Monster({"hp_level": 100, "def_level": 100})
        m.reduce_defense_maul()
        self.assertEqual(m.stats.def_level, 65)

    def test_reduce_defense_ralos(self):
        m = Monster({"hp_level": 100, "def_level": 100, "magic_level": 50})
        m.reduce_defense_ralos()
        self.assertEqual(m.stats.def_level, 95)  # 100 - (50/10) = 95


class TestMonsterBGSReduction(unittest.TestCase):
    def setUp(self):
        self.m = Monster({
            "hp_level": 200,
            "def_level": 100,
            "strength_level": 80,
            "prayer_level": 60,
            "attack_level": 90,
            "magic_level": 70,
            "ranged_level": 50,
        }, minimum_def=20)

    def test_bgs_reduces_def_first(self):
        self.m.reduce_defense_bgs(80)
        self.assertEqual(self.m.stats.def_level, 20)
        self.assertEqual(self.m.stats.strength_level, 80)

    def test_bgs_spills_to_strength(self):
        self.m.reduce_defense_bgs(100)
        self.assertEqual(self.m.stats.def_level, 20)
        self.assertEqual(self.m.stats.strength_level, 60)

    def test_bgs_spills_across_all_stats(self):
        self.m.reduce_defense_bgs(1000)
        self.assertEqual(self.m.stats.def_level, 20)
        self.assertEqual(self.m.stats.strength_level, 0)
        self.assertEqual(self.m.stats.prayer_level, 0)
        self.assertEqual(self.m.stats.attack_level, 0)
        self.assertEqual(self.m.stats.magic_level, 0)
        self.assertEqual(self.m.stats.ranged_level, 0)


class TestMonsterMagicReduction(unittest.TestCase):
    def test_reduce_magic_level_full_percentage(self):
        m = Monster({"hp_level": 100, "magic_level": 100})
        m.reduce_magic_level(0.30)
        self.assertEqual(m.stats.magic_level, 70)

    def test_reduce_magic_level_zero_percent(self):
        m = Monster({"hp_level": 100, "magic_level": 100})
        m.reduce_magic_level(0.0)
        self.assertEqual(m.stats.magic_level, 100)

    def test_reduce_magic_level_not_below_zero(self):
        m = Monster({"hp_level": 100, "magic_level": 10})
        m.reduce_magic_level(1.0)
        self.assertEqual(m.stats.magic_level, 0)


if __name__ == "__main__":
    unittest.main()
