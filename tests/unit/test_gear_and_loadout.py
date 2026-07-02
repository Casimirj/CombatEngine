"""Unit tests for Gear (abstract), Loadout base classes, and Player gear system.

Organised into two sections:
  * Mechanics — gear-system behaviour (equip/unequip, slot conflicts,
    set detection, loadout orchestration, stat recomposition).
  * Contributions — exact stat values contributed by individual gear
    pieces and full sets.
"""

import unittest
from app.Domain.GearItem import Gear
from app.Domain.Loadout import Loadout
from app.Domain.Player import Player
from app.Domain.Stats import Stats
from app.Domain.Enums.GearSlot import GearSlot
from app.Data.Registries.GearRegistry import GearRegistry
from app.Domain.Exceptions.InvalidLoadoutException import InvalidLoadoutException


_DEFAULT_LEVELS = {
    "hp_level": 99,
    "attack_level": 99,
    "strength_level": 99,
    "def_level": 99,
    "magic_level": 99,
    "ranged_level": 99,
    "prayer_level": 99,
}


# ══════════════════════════════════════════════════════════════════════
#  Mechanics — gear-system behaviour
# ══════════════════════════════════════════════════════════════════════


class TestGearAbstract(unittest.TestCase):
    """Abstract Gear base class requirements."""

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


class TestLoadoutMechanics(unittest.TestCase):
    """Loadout construction and the default gear-composition builder."""

    def test_build_without_gear_names_raises(self):
        lo = Loadout()
        with self.assertRaises(NotImplementedError):
            lo.build()

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

    def test_aliases_default_to_empty_list(self):
        class DefaultLd(Loadout):
            name = "DefaultLd"
            def build(self) -> Player:
                return Player(stats={"hp_level": 1})
        lo = DefaultLd()
        self.assertEqual(lo.aliases, [])


class TestGearDefaults(unittest.TestCase):
    """Default values on the Gear protocol."""

    def test_aliases_default_to_empty_list(self):
        class DefaultGear(Gear):
            name = "Default"
            slot = GearSlot.HEAD
            def build(self) -> dict:
                return {}
        g = DefaultGear()
        self.assertEqual(g.aliases, [])


class TestPlayerEquipGear(unittest.TestCase):
    """Equip / unequip lifecycle and stat recomposition."""

    def setUp(self):
        self.player = Player(stats=_DEFAULT_LEVELS)

    def test_equip_gear_increases_stats(self):
        old_crush = self.player.stats.crush_attack_bonus
        gear = GearRegistry.get("Amulet of fury")
        self.player.equip_gear(gear)
        self.assertGreater(self.player.stats.crush_attack_bonus, old_crush)

    def test_equip_gear_stored_in_gear_dict(self):
        gear = GearRegistry.get("Amulet of fury")
        self.player.equip_gear(gear)
        self.assertIn(GearSlot.NECK, self.player.gear)
        self.assertIs(self.player.gear[GearSlot.NECK], gear)

    def test_unequip_gear_removes_from_dict(self):
        gear = GearRegistry.get("Amulet of fury")
        self.player.equip_gear(gear)
        self.player.unequip_gear(GearSlot.NECK)
        self.assertNotIn(GearSlot.NECK, self.player.gear)

    def test_unequip_gear_restores_stats(self):
        old_crush = self.player.stats.crush_attack_bonus
        gear = GearRegistry.get("Amulet of fury")
        self.player.equip_gear(gear)
        self.player.unequip_gear(GearSlot.NECK)
        self.assertEqual(self.player.stats.crush_attack_bonus, old_crush)

    def test_equip_unequip_roundtrip(self):
        """Equip, unequip, equip again — stats should be consistent."""
        gear = GearRegistry.get("Amulet of fury")
        old_crush = self.player.stats.crush_attack_bonus

        self.player.equip_gear(gear)
        mid = self.player.stats.crush_attack_bonus
        self.player.unequip_gear(GearSlot.NECK)
        self.assertEqual(self.player.stats.crush_attack_bonus, old_crush)

        self.player.equip_gear(gear)
        self.assertEqual(self.player.stats.crush_attack_bonus, mid)

    def test_equip_multiple_gear_pieces(self):
        ammy = GearRegistry.get("Amulet of fury")
        boots = GearRegistry.get("Primordial boots")

        self.player.equip_gear(ammy)
        self.player.equip_gear(boots)

        self.assertGreater(self.player.stats.crush_attack_bonus, 0)
        self.assertGreater(self.player.stats.melee_strength_bonus, 0)

    def test_base_stats_unchanged_by_equip(self):
        old_crush = self.player.stats.crush_attack_bonus
        gear = GearRegistry.get("Amulet of fury")
        self.player.equip_gear(gear)
        self.player.unequip_gear(GearSlot.NECK)
        self.assertEqual(self.player.stats.magic_level, 99)
        self.assertEqual(self.player.stats.crush_attack_bonus, old_crush)

    def test_compute_gear_stats_recomputes_correctly(self):
        gear = GearRegistry.get("Amulet of fury")
        self.player.equip_gear(gear)
        first_crush = self.player.stats.crush_attack_bonus
        self.player.unequip_gear(GearSlot.NECK)
        self.player.equip_gear(gear)
        self.assertEqual(self.player.stats.crush_attack_bonus, first_crush)


class TestPlayerVoidDetection(unittest.TestCase):
    """Void-knight four-piece set detection and style inference."""

    def setUp(self):
        self.player = Player(stats=_DEFAULT_LEVELS)

    def test_full_void_set_detected(self):
        for name in ["Void melee helm", "Elite void top",
                     "Elite void robe", "Void knight gloves"]:
            self.player.equip_gear(GearRegistry.get(name))
        self.assertTrue(self.player.wearing_void)
        self.assertEqual(self.player.void_style, "melee")

    def test_void_ranged_set_detected(self):
        for name in ["Void ranger helm", "Elite void top",
                     "Elite void robe", "Void knight gloves"]:
            self.player.equip_gear(GearRegistry.get(name))
        self.assertTrue(self.player.wearing_void)
        self.assertEqual(self.player.void_style, "ranged")

    def test_void_mage_set_detected(self):
        for name in ["Void mage helm", "Elite void top",
                     "Elite void robe", "Void knight gloves"]:
            self.player.equip_gear(GearRegistry.get(name))
        self.assertTrue(self.player.wearing_void)
        self.assertEqual(self.player.void_style, "mage")

    def test_incomplete_void_not_detected(self):
        self.player.equip_gear(GearRegistry.get("Void melee helm"))
        self.player.equip_gear(GearRegistry.get("Elite void top"))
        self.player.equip_gear(GearRegistry.get("Elite void robe"))
        self.assertFalse(self.player.wearing_void)

    def test_unequip_void_helm_disables_void(self):
        for name in ["Void melee helm", "Elite void top",
                     "Elite void robe", "Void knight gloves"]:
            self.player.equip_gear(GearRegistry.get(name))
        self.player.unequip_gear(GearSlot.HEAD)
        self.assertFalse(self.player.wearing_void)


class TestPlayerSalveInteraction(unittest.TestCase):
    """Salve-amulet flag toggles on equip / unequip."""

    def setUp(self):
        self.player = Player(stats=_DEFAULT_LEVELS)

    def test_equip_salve_sets_wearing_salve(self):
        salve = GearRegistry.get("Salve (e)")
        self.player.equip_gear(salve)
        self.assertTrue(self.player.wearing_salve)

    def test_unequip_salve_clears_wearing_salve(self):
        salve = GearRegistry.get("Salve (e)")
        self.player.equip_gear(salve)
        self.player.unequip_gear(GearSlot.NECK)
        self.assertFalse(self.player.wearing_salve)

    def test_salve_has_zero_attack_bonuses(self):
        salve = GearRegistry.get("Salve (e)")
        self.player.equip_gear(salve)
        self.assertEqual(self.player.stats.stab_attack_bonus, 0)
        self.assertTrue(self.player.wearing_salve)


class TestLoadoutBuildWithGear(unittest.TestCase):
    """Gear-name-driven loadout resolution."""

    def test_build_with_valid_gear_names(self):
        loadout = Loadout(gear_names=["Amulet of fury", "Primordial boots"])
        player = loadout.build()
        self.assertGreater(player.stats.crush_attack_bonus, 0)
        self.assertGreater(player.stats.melee_strength_bonus, 0)

    def test_build_with_single_gear(self):
        loadout = Loadout(gear_names=["Fire cape"])
        player = loadout.build()
        self.assertGreater(player.stats.stab_def, 0)

    def test_build_with_salve(self):
        loadout = Loadout(gear_names=["Salve (e)"])
        player = loadout.build()
        self.assertTrue(player.wearing_salve)

    def test_build_with_void_set(self):
        loadout = Loadout(gear_names=[
            "Void ranger helm", "Elite void top",
            "Elite void robe", "Void knight gloves",
        ])
        player = loadout.build()
        self.assertTrue(player.wearing_void)
        self.assertEqual(player.void_style, "ranged")

    def test_build_unknown_gear_raises(self):
        loadout = Loadout(gear_names=["Nonexistent gear item"])
        with self.assertRaises(KeyError):
            loadout.build()


class TestPlayerSlotConflict(unittest.TestCase):
    """Slot-exclusivity enforcement."""

    def setUp(self):
        self.player = Player(stats=_DEFAULT_LEVELS)

    def test_same_slot_different_gear_raises(self):
        ammy1 = GearRegistry.get("Amulet of fury")
        self.player.equip_gear(ammy1)
        ammy2 = GearRegistry.get("Salve (e)")
        with self.assertRaises(InvalidLoadoutException):
            self.player.equip_gear(ammy2)


class TestPlayerConstructorWithLoadout(unittest.TestCase):
    """Player instantiation with an attached Loadout."""

    def test_player_with_loadout_equips_gear(self):
        loadout = Loadout(gear_names=["Amulet of fury", "Primordial boots"])
        player = Player(stats=_DEFAULT_LEVELS, loadout=loadout)
        self.assertIn(GearSlot.NECK, player.gear)
        self.assertIn(GearSlot.BOOTS, player.gear)
        self.assertGreater(player.stats.crush_attack_bonus, 0)

    def test_player_with_loadout_detects_salve(self):
        loadout = Loadout(gear_names=["Salve (e)"])
        player = Player(stats=_DEFAULT_LEVELS, loadout=loadout)
        self.assertTrue(player.wearing_salve)

    def test_player_with_loadout_detects_void(self):
        loadout = Loadout(gear_names=[
            "Void ranger helm", "Elite void top",
            "Elite void robe", "Void knight gloves",
        ])
        player = Player(stats=_DEFAULT_LEVELS, loadout=loadout)
        self.assertTrue(player.wearing_void)
        self.assertEqual(player.void_style, "ranged")

    def test_player_no_loadout_has_empty_gear(self):
        player = Player(stats=_DEFAULT_LEVELS)
        self.assertEqual(player.gear, {})


class TestPlayerGearWeaponInterplay(unittest.TestCase):
    """Combined gear + weapon stat layering."""

    def setUp(self):
        self.player = Player(stats=_DEFAULT_LEVELS)

    def test_gear_and_weapon_stats_combined(self):
        gear = GearRegistry.get("Amulet of fury")
        self.player.equip_gear(gear)
        self.player.equip_weapon(_make_weapon())
        self.assertGreater(self.player.stats.crush_attack_bonus, 0)
        self.assertGreater(self.player.stats.stab_attack_bonus, 0)

    def test_weapon_then_gear_both_in_stats(self):
        self.player.equip_weapon(_make_weapon())
        gear = GearRegistry.get("Amulet of fury")
        self.player.equip_gear(gear)
        self.assertGreater(self.player.stats.crush_attack_bonus, 0)
        self.assertGreater(self.player.stats.stab_attack_bonus, 0)


class TestPlayerUnequipEmptySlot(unittest.TestCase):
    """Unequipping an empty slot is a no-op."""

    def setUp(self):
        self.player = Player(stats=_DEFAULT_LEVELS)

    def test_unequip_empty_slot_no_error(self):
        self.player.unequip_gear(GearSlot.NECK)
        self.assertNotIn(GearSlot.NECK, self.player.gear)


# ══════════════════════════════════════════════════════════════════════
#  Contributions — exact stat values from gear pieces and sets
# ══════════════════════════════════════════════════════════════════════


class TestContrib_AmuletOfRancour(unittest.TestCase):
    """Amulet of rancour: +25 stab attack, +12 melee strength."""

    def setUp(self):
        self.player = Player(stats=_DEFAULT_LEVELS)

    def test_rancour_grants_stab_and_strength(self):
        gear = GearRegistry.get("Amulet of rancour")
        self.player.equip_gear(gear)
        self.assertEqual(self.player.stats.stab_attack_bonus, 25)
        self.assertEqual(self.player.stats.melee_strength_bonus, 12)


class TestContrib_TorvaFullHelm(unittest.TestCase):
    """Torva full helm: +8 strength, 59+ stab defence."""

    def setUp(self):
        self.player = Player(stats=_DEFAULT_LEVELS)

    def test_torva_helm_strength_and_stab_def(self):
        helm = GearRegistry.get("Torva full helm")
        self.player.equip_gear(helm)
        self.assertEqual(self.player.stats.melee_strength_bonus, 8)
        self.assertGreaterEqual(self.player.stats.stab_def, 59)


class TestContrib_TorvaPlatebody(unittest.TestCase):
    """Torva platebody: +6 strength, 117 stab / crush defence."""

    def setUp(self):
        self.player = Player(stats=_DEFAULT_LEVELS)

    def test_torva_body_crush_def_and_strength(self):
        body = GearRegistry.get("Torva platebody")
        self.player.equip_gear(body)
        self.assertEqual(self.player.stats.melee_strength_bonus, 6)
        self.assertEqual(self.player.stats.crush_def, 117)


class TestContrib_TorvaPlatelegs(unittest.TestCase):
    """Torva platelegs: +4 strength, 79 crush defence."""

    def setUp(self):
        self.player = Player(stats=_DEFAULT_LEVELS)

    def test_torva_legs_strength_and_crush_def(self):
        legs = GearRegistry.get("Torva platelegs")
        self.player.equip_gear(legs)
        self.assertEqual(self.player.stats.melee_strength_bonus, 4)
        self.assertGreaterEqual(self.player.stats.crush_def, 79)


class TestContrib_BandosChestplate(unittest.TestCase):
    """Bandos chestplate: +4 strength, 105 crush defence."""

    def setUp(self):
        self.player = Player(stats=_DEFAULT_LEVELS)

    def test_bandos_chest_strength_and_crush_def(self):
        bcp = GearRegistry.get("Bandos chestplate")
        self.player.equip_gear(bcp)
        self.assertEqual(self.player.stats.melee_strength_bonus, 4)
        self.assertEqual(self.player.stats.crush_def, 105)


class TestContrib_BandosTassets(unittest.TestCase):
    """Bandos tassets: +2 strength, 63+ slash defence."""

    def setUp(self):
        self.player = Player(stats=_DEFAULT_LEVELS)

    def test_bandos_tassets_strength_and_slash_def(self):
        tassets = GearRegistry.get("Bandos tassets")
        self.player.equip_gear(tassets)
        self.assertEqual(self.player.stats.melee_strength_bonus, 2)
        self.assertGreaterEqual(self.player.stats.slash_def, 63)


class TestContrib_FerociousGloves(unittest.TestCase):
    """Ferocious gloves: +16 crush attack, +14 melee strength."""

    def setUp(self):
        self.player = Player(stats=_DEFAULT_LEVELS)

    def test_ferocious_gloves_crush_and_strength(self):
        gloves = GearRegistry.get("Ferocious gloves")
        self.player.equip_gear(gloves)
        self.assertEqual(self.player.stats.crush_attack_bonus, 16)
        self.assertEqual(self.player.stats.melee_strength_bonus, 14)


class TestContrib_UltorRing(unittest.TestCase):
    """Ultor ring: +12 strength, no attack bonuses."""

    def setUp(self):
        self.player = Player(stats=_DEFAULT_LEVELS)

    def test_ultor_ring_strength_only(self):
        ring = GearRegistry.get("Ultor ring")
        self.player.equip_gear(ring)
        self.assertEqual(self.player.stats.melee_strength_bonus, 12)
        self.assertEqual(self.player.stats.stab_attack_bonus, 0)


class TestContrib_BerserkerRingI(unittest.TestCase):
    """Berserker ring (i): +8 strength, +8 crush defence."""

    def setUp(self):
        self.player = Player(stats=_DEFAULT_LEVELS)

    def test_bring_strength_and_crush_def(self):
        ring = GearRegistry.get("Berserker ring (i)")
        self.player.equip_gear(ring)
        self.assertEqual(self.player.stats.melee_strength_bonus, 8)
        self.assertEqual(self.player.stats.crush_def, 8)


class TestContrib_AvernicDefender(unittest.TestCase):
    """Avernic defender: +30 stab attack, +8 melee strength."""

    def setUp(self):
        self.player = Player(stats=_DEFAULT_LEVELS)

    def test_avernic_stab_attack_and_strength(self):
        defender = GearRegistry.get("Avernic defender")
        self.player.equip_gear(defender)
        self.assertEqual(self.player.stats.stab_attack_bonus, 30)
        self.assertEqual(self.player.stats.melee_strength_bonus, 8)


class TestContrib_MagusRing(unittest.TestCase):
    """Magus ring: +15 magic attack, +2 magic damage."""

    def setUp(self):
        self.player = Player(stats=_DEFAULT_LEVELS)

    def test_magus_magic_attack_and_damage(self):
        ring = GearRegistry.get("Magus ring")
        self.player.equip_gear(ring)
        self.assertEqual(self.player.stats.magic_attack_bonus, 15)
        self.assertEqual(self.player.stats.magic_strength_bonus, 2)


class TestContrib_VenatorRing(unittest.TestCase):
    """Venator ring: +10 ranged attack, +2 ranged strength."""

    def setUp(self):
        self.player = Player(stats=_DEFAULT_LEVELS)

    def test_venator_ranged_attack_and_strength(self):
        ring = GearRegistry.get("Venator ring")
        self.player.equip_gear(ring)
        self.assertEqual(self.player.stats.ranged_attack_bonus, 10)
        self.assertEqual(self.player.stats.ranged_strength_bonus, 2)


class TestContrib_OccultNecklace(unittest.TestCase):
    """Occult necklace: +12 magic attack, +5 magic damage."""

    def setUp(self):
        self.player = Player(stats=_DEFAULT_LEVELS)

    def test_occult_magic_attack_and_strength(self):
        amulet = GearRegistry.get("Occult necklace")
        self.player.equip_gear(amulet)
        self.assertEqual(self.player.stats.magic_attack_bonus, 12)
        self.assertEqual(self.player.stats.magic_strength_bonus, 5)


class TestContrib_NecklaceOfAnguish(unittest.TestCase):
    """Necklace of anguish: +15 ranged attack, +5 ranged strength."""

    def setUp(self):
        self.player = Player(stats=_DEFAULT_LEVELS)

    def test_anguish_ranged_attack_and_strength(self):
        amulet = GearRegistry.get("Necklace of anguish")
        self.player.equip_gear(amulet)
        self.assertEqual(self.player.stats.ranged_attack_bonus, 15)
        self.assertEqual(self.player.stats.ranged_strength_bonus, 5)


class TestContrib_MasoriMask(unittest.TestCase):
    """Masori mask: +12 ranged attack, +2 ranged strength."""

    def setUp(self):
        self.player = Player(stats=_DEFAULT_LEVELS)

    def test_masori_mask_ranged_attack(self):
        mask = GearRegistry.get("Masori mask")
        self.player.equip_gear(mask)
        self.assertEqual(self.player.stats.ranged_attack_bonus, 12)
        self.assertEqual(self.player.stats.ranged_strength_bonus, 2)


class TestContrib_ZaryteVambraces(unittest.TestCase):
    """Zaryte vambraces: +18 ranged attack, +2 ranged strength."""

    def setUp(self):
        self.player = Player(stats=_DEFAULT_LEVELS)

    def test_zaryte_vambs_ranged_attack(self):
        vambs = GearRegistry.get("Zaryte vambraces")
        self.player.equip_gear(vambs)
        self.assertEqual(self.player.stats.ranged_attack_bonus, 18)
        self.assertEqual(self.player.stats.ranged_strength_bonus, 2)


class TestContrib_DizanasQuiver(unittest.TestCase):
    """Dizana's quiver: +18 ranged attack, +3 ranged strength."""

    def setUp(self):
        self.player = Player(stats=_DEFAULT_LEVELS)

    def test_quiver_ranged_attack(self):
        quiver = GearRegistry.get("Dizana's quiver")
        self.player.equip_gear(quiver)
        self.assertEqual(self.player.stats.ranged_attack_bonus, 18)
        self.assertEqual(self.player.stats.ranged_strength_bonus, 3)


class TestContrib_AncestralSet(unittest.TestCase):
    """Full ancestral (hat / top / bottom): +69 magic attack, +9 magic damage."""

    def setUp(self):
        self.player = Player(stats=_DEFAULT_LEVELS)

    def test_full_ancestral_magic_stats(self):
        for name in ["Ancestral hat", "Ancestral robe top", "Ancestral robe bottom"]:
            self.player.equip_gear(GearRegistry.get(name))
        self.assertEqual(self.player.stats.magic_attack_bonus, 69)
        self.assertEqual(self.player.stats.magic_strength_bonus, 9)


class TestContrib_MasoriSet(unittest.TestCase):
    """Full Masori (mask / body / chaps): +82 ranged attack, +8 ranged strength."""

    def setUp(self):
        self.player = Player(stats=_DEFAULT_LEVELS)

    def test_full_masori_ranged_stats(self):
        for name in ["Masori mask", "Masori body", "Masori chaps"]:
            self.player.equip_gear(GearRegistry.get(name))
        self.assertEqual(self.player.stats.ranged_attack_bonus, 82)
        self.assertEqual(self.player.stats.ranged_strength_bonus, 8)


class TestContrib_OathplateSet(unittest.TestCase):
    """Full Oathplate (helm / body / legs): +12 strength, 230+ stab def."""

    def setUp(self):
        self.player = Player(stats=_DEFAULT_LEVELS)

    def test_full_oathplate_set_bonuses(self):
        for name in ["Oathplate helm", "Oathplate body", "Oathplate legs"]:
            self.player.equip_gear(GearRegistry.get(name))
        self.assertEqual(self.player.stats.melee_strength_bonus, 12)
        self.assertGreaterEqual(self.player.stats.stab_def, 230)
        self.assertGreaterEqual(self.player.stats.crush_def, 218)


# ---------------------------------------------------------------------------
#  Helpers
# ---------------------------------------------------------------------------


def _make_weapon(name="Test Sword", combat_style="Melee", attack_type="Slash",
                 attack_style="Aggressive", attack_speed=4, has_special=False,
                 special_attack_style=None, special_attack_cost=0):
    from app.Domain.Weapon import Weapon
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


if __name__ == "__main__":
    unittest.main()
