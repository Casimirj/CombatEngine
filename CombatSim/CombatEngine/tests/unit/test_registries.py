"""Unit tests for MonsterRegistry, WeaponRegistry, GearRegistry, LoadoutRegistry."""

import unittest
from CombatSim.CombatEngine.Domain.Monster import Monster
from CombatSim.CombatEngine.Domain.Weapon import Weapon
from CombatSim.CombatEngine.Domain.Stats import Stats
from CombatSim.CombatEngine.Domain.GearItem import Gear
from CombatSim.CombatEngine.Domain.Loadout import Loadout
from CombatSim.CombatEngine.Domain.Enums.GearSlot import GearSlot
from CombatSim.CombatEngine.Data.Registries.MonsterRegistry import MonsterRegistry
from CombatSim.CombatEngine.Data.Registries.WeaponRegistry import WeaponRegistry
from CombatSim.CombatEngine.Data.Registries.GearRegistry import GearRegistry
from CombatSim.CombatEngine.Data.Registries.LoadoutRegistry import LoadoutRegistry


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _save_registry_state(registry_cls):
    return (dict(registry_cls._items), dict(registry_cls._aliases))

def _restore_registry_state(registry_cls, state):
    registry_cls._items, registry_cls._aliases = state


class TestGear(Gear):
    def __init__(self, name, slot: GearSlot, build_dict: dict = None, aliases=None):
        self.name = name
        self.slot = slot
        self.aliases = aliases or []
        self._build_dict = build_dict or {}

    def build(self) -> dict:
        return self._build_dict


# ---------------------------------------------------------------------------
# MonsterRegistry
# ---------------------------------------------------------------------------

class TestMonsterRegistry(unittest.TestCase):
    def setUp(self):
        self._saved = _save_registry_state(MonsterRegistry)
        MonsterRegistry._items = {}
        MonsterRegistry._aliases = {}

    def tearDown(self):
        _restore_registry_state(MonsterRegistry, self._saved)

    def test_register_and_get_by_name(self):
        class TestMonster(Monster):
            aliases = ["testy"]
            def __init__(self, scale=1):
                super().__init__({"hp_level": 100})
        MonsterRegistry.register(TestMonster)
        retrieved = MonsterRegistry.get("TestMonster")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.stats.hp_level, 100)

    def test_register_and_get_by_alias(self):
        class TestMonster(Monster):
            aliases = ["testy mctestface"]
            def __init__(self, scale=1):
                super().__init__({"hp_level": 200})
        MonsterRegistry.register(TestMonster)
        retrieved = MonsterRegistry.get("testy mctestface")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.stats.hp_level, 200)

    def test_missing_monster_returns_none(self):
        self.assertIsNone(MonsterRegistry.get("nonexistent"))


# ---------------------------------------------------------------------------
# WeaponRegistry
# ---------------------------------------------------------------------------

class TestWeaponRegistry(unittest.TestCase):
    def setUp(self):
        self._saved = _save_registry_state(WeaponRegistry)
        WeaponRegistry._items = {}
        WeaponRegistry._aliases = {}

    def tearDown(self):
        _restore_registry_state(WeaponRegistry, self._saved)

    def _make_weapon_class(self, name, aliases_param=None):
        p_aliases = aliases_param
        class TestWeapon(Weapon):
            aliases = p_aliases or []
            def __init__(self):
                super().__init__(
                    name=name,
                    stats=Stats({"stab_attack_bonus": 10}),
                    combat_style="Melee",
                    attack_type="Stab",
                    attack_style="Aggressive",
                    attack_speed=4,
                    attack_range=1,
                    has_special_attack=False,
                )
        return TestWeapon

    def test_register_and_get(self):
        cls = self._make_weapon_class("Test Blade")
        WeaponRegistry.register(cls)
        w = WeaponRegistry.get("Test Blade")
        self.assertIsNotNone(w)
        self.assertEqual(w.name, "Test blade")

    def test_register_with_aliases(self):
        cls = self._make_weapon_class("Super Sword", aliases_param=["ss", "super sword"])
        WeaponRegistry.register(cls)
        self.assertIsNotNone(WeaponRegistry.get("ss"))
        self.assertIsNotNone(WeaponRegistry.get("super sword"))

    def test_missing_weapon_returns_none(self):
        self.assertIsNone(WeaponRegistry.get("fantasy weapon"))


# ---------------------------------------------------------------------------
# GearRegistry
# ---------------------------------------------------------------------------

class TestGearRegistry(unittest.TestCase):
    def setUp(self):
        self._saved = _save_registry_state(GearRegistry)
        GearRegistry._items = {}
        GearRegistry._aliases = {}

    def tearDown(self):
        _restore_registry_state(GearRegistry, self._saved)

    def test_register_and_get(self):
        g = TestGear("Fire Cape", GearSlot.CAPE, {"stab_def": 11, "strength_bonus": 4})
        GearRegistry.register(g)
        retrieved = GearRegistry.get("Fire Cape")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.name, "Fire Cape")

    def test_register_with_alias(self):
        g = TestGear("Amulet of Fury", GearSlot.NECK, aliases=["fury"])
        GearRegistry.register(g)
        self.assertIsNotNone(GearRegistry.get("fury"))

    def test_missing_gear_returns_none(self):
        self.assertIsNone(GearRegistry.get("Mythical cape"))


# ---------------------------------------------------------------------------
# LoadoutRegistry
# ---------------------------------------------------------------------------

class TestLoadoutRegistry(unittest.TestCase):
    def setUp(self):
        self._saved = _save_registry_state(LoadoutRegistry)
        LoadoutRegistry._items = {}
        LoadoutRegistry._aliases = {}

    def tearDown(self):
        _restore_registry_state(LoadoutRegistry, self._saved)

    def test_register_and_get(self):
        class TestLoadout(Loadout):
            name = "Test Loadout"
            aliases = ["tl"]
            def build(self):
                from CombatSim.CombatEngine.Domain.Player import Player
                return Player(stats={"hp_level": 99, "attack_level": 80})

        LoadoutRegistry.register(TestLoadout())
        loadout = LoadoutRegistry.get("Test Loadout")
        self.assertIsNotNone(loadout)
        self.assertEqual(loadout.name, "Test Loadout")

    def test_loadout_registry_is_pure_lookup(self):
        """get() returns the registered Loadout (not a built Player)."""
        class PureLookupLoadout(Loadout):
            name = "PureLookup"
            aliases = []

        LoadoutRegistry.register(PureLookupLoadout())
        result = LoadoutRegistry.get("PureLookup")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, Loadout)

    def test_loadout_alias(self):
        class AliasedLoadout(Loadout):
            name = "Aliased"
            aliases = ["al"]

        LoadoutRegistry.register(AliasedLoadout())
        loadout = LoadoutRegistry.get("al")
        self.assertIsNotNone(loadout)
        self.assertEqual(loadout.name, "Aliased")


# ---------------------------------------------------------------------------
# Concrete weapon classes from GameDefinitions
# ---------------------------------------------------------------------------

class TestWeaponRegistryConcrete(unittest.TestCase):
    """Tests that registered weapons are retrievable."""

    @classmethod
    def setUpClass(cls):
        import CombatSim.CombatEngine.Data.Definitions.Weapons  # noqa: F811 — ensure registered

    def test_scythe_is_registered(self):
        w = WeaponRegistry.get("Scythe of Vitur")
        self.assertIsNotNone(w)
        self.assertEqual(w.name, "Scythe of vitur")

    def test_fists_is_registered(self):
        w = WeaponRegistry.get("Fists")
        self.assertIsNotNone(w)
        self.assertEqual(w.combat_style, "Melee")

    def test_twisted_bow_is_registered(self):
        w = WeaponRegistry.get("Twisted Bow")
        self.assertIsNotNone(w)
        self.assertEqual(w.combat_style, "Ranged")

    def test_tumekens_shadow_is_registered(self):
        w = WeaponRegistry.get("Tumeken's Shadow")
        self.assertIsNotNone(w)
        self.assertEqual(w.combat_style, "Mage")


class TestMonsterRegistryConcrete(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import CombatSim.CombatEngine.Data.Definitions.Monsters  # noqa: F811 — ensure registered

    def test_bloat_is_registered(self):
        m = MonsterRegistry.get("Bloat")
        self.assertIsNotNone(m)
        self.assertGreater(m.current_hp, 0)

    def test_maiden_is_registered(self):
        m = MonsterRegistry.get("Maiden")
        self.assertIsNotNone(m)

    def test_xarpus_is_registered(self):
        m = MonsterRegistry.get("Xarpus")
        self.assertIsNotNone(m)

    def test_p1_verzik_is_registered(self):
        m = MonsterRegistry.get("P1Verzik")
        self.assertIsNotNone(m)

    def test_sotetseg_is_registered(self):
        m = MonsterRegistry.get("Sotetseg")
        self.assertIsNotNone(m)


if __name__ == "__main__":
    unittest.main()
