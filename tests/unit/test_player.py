"""Unit tests for app.Player."""

import unittest
from unittest.mock import patch
from app.Player import Player
from app.Weapon import Weapon
from app.Stats import Stats
from app.Monster import Monster
from app.Enums import Potion, Prayer


_DEFAULT_STATS = {
    "hp_level": 99,
    "attack_level": 99,
    "strength_level": 99,
    "def_level": 99,
    "magic_level": 99,
    "ranged_level": 99,
    "prayer_level": 99,
}


def _make_weapon(name="Test Sword", combat_style="Melee", attack_type="Slash",
                 attack_style="Aggressive", attack_speed=4, has_special=False,
                 special_attack_style=None, special_attack_cost=0):
    return Weapon(
        name=name,
        stats=Stats({"stab_attack_bonus": 40, "melee_strength_bonus": 30}),
        combat_style=combat_style,
        attack_type=attack_type,
        attack_style=attack_style,
        attack_speed=attack_speed,
        attack_range=1,
        has_special_attack=has_special,
        special_attack_style=special_attack_style,
        special_attack_cost=special_attack_cost,
    )


class TestPlayerInit(unittest.TestCase):
    def test_player_initialises_with_stats(self):
        p = Player(stats=_DEFAULT_STATS)
        self.assertEqual(p.stats.hp_level, 99)
        self.assertEqual(p.current_hp, 99)
        self.assertEqual(p.current_special_attack, 100)
        self.assertEqual(p.current_run, 100)
        self.assertEqual(p.current_prayer, 99)

    def test_player_defaults_to_fists_when_no_weapon(self):
        p = Player(stats=_DEFAULT_STATS)
        self.assertIsNotNone(p.weapon)
        self.assertEqual(p.weapon.name, "Fists")

    def test_player_uses_given_weapon(self):
        w = _make_weapon()
        p = Player(stats=_DEFAULT_STATS, weapon=w)
        self.assertIs(p.weapon, w)

    def test_player_default_boosts_and_prayer(self):
        p = Player(stats=_DEFAULT_STATS)
        self.assertEqual(p.prayer, Prayer.NONE)
        self.assertEqual(p.boosts, [Potion.NONE])

    def test_player_wearing_salve(self):
        p = Player(stats=_DEFAULT_STATS, wearing_salve=True)
        self.assertTrue(p.wearing_salve)

    def test_player_stats_none_raises(self):
        with self.assertRaises(ValueError):
            Player()


class TestPlayerHP(unittest.TestCase):
    def setUp(self):
        self.p = Player(stats=_DEFAULT_STATS)

    def test_reduce_hp(self):
        self.p.reduce_hp(30)
        self.assertEqual(self.p.current_hp, 69)

    def test_reduce_hp_not_below_zero(self):
        self.p.reduce_hp(200)
        self.assertEqual(self.p.current_hp, 0)

    def test_is_alive_and_is_dead(self):
        self.assertTrue(self.p.is_alive())
        self.assertFalse(self.p.is_dead())
        self.p.reduce_hp(99)
        self.assertTrue(self.p.is_dead())
        self.assertFalse(self.p.is_alive())


class TestPlayerWeaponEquip(unittest.TestCase):
    def setUp(self):
        self.p = Player(stats=_DEFAULT_STATS)

    def test_equip_weapon_adds_stats(self):
        old_stab = self.p.stats.stab_attack_bonus
        w = _make_weapon()
        self.p.equip_weapon(w)
        self.assertGreater(self.p.stats.stab_attack_bonus, old_stab)

    def test_unequip_weapon_subtracts_stats(self):
        w = _make_weapon()
        self.p.equip_weapon(w)
        stabbed = self.p.stats.stab_attack_bonus
        self.p.unequip_weapon(w)
        self.assertLess(self.p.stats.stab_attack_bonus, stabbed)
        self.assertEqual(self.p.weapon.name, "Fists")


class TestPlayerMeleeCalcs(unittest.TestCase):
    def setUp(self):
        self.w = _make_weapon()
        self.p = Player(stats=_DEFAULT_STATS, weapon=self.w,
                        boosts=[Potion.SUPER_COMBAT], prayer=Prayer.PIETY)

    def test_calc_effective_attack_level(self):
        lvl = self.p.calc_eff_attack_level()
        self.assertGreater(lvl, 99)

    def test_calc_effective_strength_level(self):
        lvl = self.p.calc_eff_strength_level()
        self.assertGreater(lvl, 99)

    def test_calc_attack_roll(self):
        self.p.calc_all_the_things(combat_style="Melee", attack_type="Slash")
        self.assertGreater(self.p.attack_roll, 0)

    def test_calc_max_hit(self):
        self.p.calc_all_the_things(combat_style="Melee", attack_type="Slash")
        self.assertGreater(self.p.max_hit, 0)

    def test_calc_def_roll(self):
        self.p.calc_all_the_things(combat_style="Melee", attack_type="Slash")
        self.assertGreater(self.p.def_roll, 0)

    def test_salve_boosts_attack_roll(self):
        from app.Registries.GearRegistry import GearRegistry
        salve = GearRegistry.get("Salve (e)")
        p_salve = Player(stats=_DEFAULT_STATS, weapon=self.w,
                         boosts=[Potion.SUPER_COMBAT], prayer=Prayer.PIETY)
        p_salve.equip_gear(salve)
        self.p.calc_all_the_things(combat_style="Melee", attack_type="Slash",
                                   monster_weak_to_salve=False)
        p_salve.calc_all_the_things(combat_style="Melee", attack_type="Slash",
                                    monster_weak_to_salve=True)
        self.assertGreater(p_salve.attack_roll, self.p.attack_roll)

    def test_salve_boosts_max_hit(self):
        from app.Registries.GearRegistry import GearRegistry
        salve = GearRegistry.get("Salve (e)")
        p_salve = Player(stats=_DEFAULT_STATS, weapon=self.w,
                         boosts=[Potion.SUPER_COMBAT], prayer=Prayer.PIETY)
        p_salve.equip_gear(salve)
        self.p.calc_all_the_things(combat_style="Melee", attack_type="Slash",
                                   monster_weak_to_salve=False)
        p_salve.calc_all_the_things(combat_style="Melee", attack_type="Slash",
                                    monster_weak_to_salve=True)
        self.assertGreater(p_salve.max_hit, self.p.max_hit)


class TestPlayerRangedCalcs(unittest.TestCase):
    def setUp(self):
        self.w = Weapon(
            name="T Bow",
            stats=Stats({
                "ranged_attack_bonus": 100,
                "ranged_strength_bonus": 20,
            }),
            combat_style="Ranged",
            attack_type="Ranged",
            attack_style="Accurate",
            attack_speed=5,
            attack_range=10,
            has_special_attack=False,
        )
        self.p = Player(stats=_DEFAULT_STATS, weapon=self.w,
                        boosts=[Potion.RANGING], prayer=Prayer.RIGOUR)

    def test_calc_effective_ranged_attack(self):
        lvl = self.p.calc_eff_ranged_attack_level()
        self.assertGreater(lvl, 99)

    def test_calc_effective_ranged_strength(self):
        lvl = self.p.calc_eff_ranged_strength_level()
        self.assertGreater(lvl, 99)

    def test_calc_ranged_attack_roll(self):
        self.p.calc_all_the_things(combat_style="Ranged", attack_type="Ranged")
        self.assertGreater(self.p.attack_roll, 0)

    def test_calc_ranged_max_hit(self):
        self.p.calc_all_the_things(combat_style="Ranged", attack_type="Ranged")
        self.assertGreater(self.p.max_hit, 0)


class TestPlayerMagicCalcs(unittest.TestCase):
    def setUp(self):
        self.w = Weapon(
            name="Shadow",
            stats=Stats({
                "magic_attack_bonus": 80,
                "magic_strength_bonus": 12,
            }),
            combat_style="Mage",
            attack_type="Magic",
            attack_style="Autocast",
            attack_speed=5,
            attack_range=8,
            has_special_attack=False,
        )
        self.p = Player(stats=_DEFAULT_STATS, weapon=self.w,
                        boosts=[Potion.IMBUED_HEART], prayer=Prayer.AUGURY)

    def test_calc_effective_magic_level(self):
        lvl = self.p.calc_eff_magic_level()
        self.assertGreater(lvl, 99)

    def test_calc_magic_attack_roll(self):
        self.p.calc_all_the_things(combat_style="Mage", attack_type="Magic")
        self.assertGreater(self.p.attack_roll, 0)

    def test_calc_magic_max_hit(self):
        self.p.calc_all_the_things(combat_style="Mage", attack_type="Magic")
        self.assertGreater(self.p.max_hit, 0)


class TestPlayerDoAttack(unittest.TestCase):
    def setUp(self):
        self.w = _make_weapon()
        self.p = Player(stats=_DEFAULT_STATS, weapon=self.w,
                        boosts=[Potion.SUPER_COMBAT], prayer=Prayer.PIETY)
        self.m = Monster({"hp_level": 200, "def_level": 80, "slash_def": 100})

    def test_do_attack_returns_non_negative(self):
        damage = self.p.do_attack(self.m)
        self.assertGreaterEqual(damage, 0)

    def test_do_attack_on_dead_monster(self):
        self.m.reduce_hp(999)
        damage = self.p.do_attack(self.m)
        self.assertIsInstance(damage, int)

    def test_special_attack_with_insufficient_energy(self):
        # Falls through to normal attack when spec energy too low
        w = Weapon(
            name="Spec Weapon",
            stats=Stats({"stab_attack_bonus": 40}),
            combat_style="Melee",
            attack_type="Stab",
            attack_style="Aggressive",
            attack_speed=4,
            attack_range=1,
            has_special_attack=True,
            special_attack_style="Aggressive",
            special_attack_cost=100,
        )
        p = Player(stats=_DEFAULT_STATS, weapon=w,
                   boosts=[Potion.SUPER_COMBAT], prayer=Prayer.PIETY)
        p.current_special_attack = 0
        damage = p.do_attack(self.m, special_attack=True)
        # Falls through to normal attack — returns int damage, not ReferenceError
        self.assertIsInstance(damage, int)
        self.assertGreaterEqual(damage, 0)


class TestPlayerCalcAttRoll(unittest.TestCase):
    def setUp(self):
        self.p = Player(stats=_DEFAULT_STATS, weapon=_make_weapon(),
                        boosts=[Potion.NONE], prayer=Prayer.NONE)
        self.p.effective_att_level = 100
        # Set expected stat values directly for deterministic calc tests
        self.p.stats.stab_attack_bonus = 80
        self.p.stats.slash_attack_bonus = 80
        self.p.stats.crush_attack_bonus = 80

    def test_slash(self):
        roll = self.p.calc_att_roll(attack_style="Slash")
        self.assertEqual(roll, 100 * (80 + 64))

    def test_crush(self):
        roll = self.p.calc_att_roll(attack_style="Crush")
        self.assertEqual(roll, 100 * (80 + 64))

    def test_stab(self):
        roll = self.p.calc_att_roll(attack_style="Stab")
        self.assertEqual(roll, 100 * (80 + 64))

    def test_none_raises(self):
        with self.assertRaises(ValueError):
            self.p.calc_att_roll()


class TestPlayerCalcDefRoll(unittest.TestCase):
    def setUp(self):
        self.p = Player(stats=_DEFAULT_STATS, weapon=_make_weapon(),
                        boosts=[Potion.NONE], prayer=Prayer.NONE)
        self.p.effective_def_level = 100
        # Set expected stat values directly for deterministic calc tests
        self.p.stats.stab_def = 200
        self.p.stats.slash_def = 200
        self.p.stats.crush_def = 200

    def test_slash_def(self):
        roll = self.p.calc_def_roll(attack_style="Slash")
        self.assertEqual(roll, 100 * (200 + 64))

    def test_none_raises(self):
        with self.assertRaises(ValueError):
            self.p.calc_def_roll()


if __name__ == "__main__":
    unittest.main()
