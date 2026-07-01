"""Unit tests for Gear (abstract) and Loadout (abstract) base classes."""

import unittest
from app.GearItem import Gear
from app.Loadout import Loadout
from app.Player import Player
from app.Enums.gear_slot import GearSlot


class TestGearAbstract(unittest.TestCase):
    def test_subclass_must_implement_build(self):
        with self.assertRaises(TypeError):
            Gear()

    def test_concrete_subclass_works(self):
        class FireCape(Gear):
            name = "Fire Cape"
            slot = GearSlot.CAPE
            aliases = ["fc", "fire cape"]
            player_kwargs = {}

            def build(self) -> dict:
                return {"stab_def": 11, "strength_bonus": 4}

        fc = FireCape()
        self.assertEqual(fc.name, "Fire Cape")
        self.assertEqual(fc.slot, GearSlot.CAPE)
        self.assertIn("fc", fc.aliases)
        result = fc.build()
        self.assertEqual(result["stab_def"], 11)

    def test_player_kwargs_defaults_to_empty(self):
        class BareGear(Gear):
            name = "Bare"
            slot = GearSlot.RING
            def build(self) -> dict:
                return {}
        g = BareGear()
        self.assertEqual(g.player_kwargs, {})


class TestLoadoutAbstract(unittest.TestCase):
    def test_subclass_must_implement_build(self):
        with self.assertRaises(TypeError):
            Loadout()

    def test_concrete_subclass_returns_player(self):
        class MyLoadout(Loadout):
            name = "My Loadout"
            aliases = ["ml"]
            def build(self) -> Player:
                return Player(stats={"hp_level": 99, "attack_level": 70})

        lo = MyLoadout()
        self.assertEqual(lo.name, "My Loadout")
        self.assertIn("ml", lo.aliases)
        p = lo.build()
        self.assertIsInstance(p, Player)
        self.assertEqual(p.stats.hp_level, 99)


class TestGearDefaults(unittest.TestCase):
    def test_aliases_default_to_empty_list(self):
        class DefaultGear(Gear):
            name = "Default"
            slot = GearSlot.HEAD
            def build(self) -> dict:
                return {}
        g = DefaultGear()
        self.assertEqual(g.aliases, [])

    def test_loadout_aliases_default_to_empty_list(self):
        class DefaultLd(Loadout):
            name = "DefaultLd"
            def build(self) -> Player:
                return Player(stats={"hp_level": 1})
        lo = DefaultLd()
        self.assertEqual(lo.aliases, [])


if __name__ == "__main__":
    unittest.main()
