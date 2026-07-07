"""Unit tests for BaseRegistry and key normalization."""

import unittest
from combat_engine.Data.Registries.BaseRegistry import BaseRegistry, normalize_key


class TestNormalizeKey(unittest.TestCase):
    def test_strips_spaces(self):
        self.assertEqual(normalize_key("super combat"), "supercombat")

    def test_strips_underscores(self):
        self.assertEqual(normalize_key("super_combat"), "supercombat")

    def test_strips_hyphens(self):
        self.assertEqual(normalize_key("super-combat"), "supercombat")

    def test_lowercases(self):
        self.assertEqual(normalize_key("Super Combat"), "supercombat")

    def test_mixed_delimiters(self):
        self.assertEqual(normalize_key("Super_ Combat-Potion"), "supercombatpotion")

    def test_no_delimiters(self):
        self.assertEqual(normalize_key("scythe"), "scythe")


class TestBaseRegistryAliasResolution(unittest.TestCase):
    def setUp(self):
        # Reinitialise class-level state between tests
        BaseRegistry._aliases = {}
        BaseRegistry._items = {}

    def test_add_and_resolve_alias(self):
        BaseRegistry._add_alias("scythe", "scytheofvitur")
        self.assertEqual(BaseRegistry._resolve_key("scythe"), "scytheofvitur")

    def test_alias_normalized_before_lookup(self):
        BaseRegistry._add_alias("T Bow", "twistedbow")
        self.assertEqual(BaseRegistry._resolve_key("t_bow"), "twistedbow")
        self.assertEqual(BaseRegistry._resolve_key("t bow"), "twistedbow")

    def test_unknown_key_returns_normalized_input(self):
        self.assertEqual(BaseRegistry._resolve_key("unknownthing"), "unknownthing")

    def test_get_by_key_finds_item(self):
        obj = object()
        BaseRegistry._items["testkey"] = obj
        self.assertIs(BaseRegistry.get_by_key("testkey"), obj)

    def test_get_by_key_missing_returns_none(self):
        self.assertIsNone(BaseRegistry.get_by_key("nope"))


if __name__ == "__main__":
    unittest.main()
