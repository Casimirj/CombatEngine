"""Unit tests for the NyloBoss phase system and simulation components."""

import unittest

from CombatSim.Simulations.nyloboss.phases import NyloBossPhase, next_nylo_phase
from CombatSim.Simulations.nyloboss.schedules import (
    NyloAttackSchedule,
    schedule_for_phase,
    FIRST_MELEE,
    MELEE,
    RANGED,
    RANGED_AFTER_MAGE,
    MAGE,
    melee_setup,
    ranged_setup,
    ranged_after_mage_setup,
    mage_setup,
)
from CombatSim.Simulations.nyloboss.simulation import _apply_setup, _fresh_player
from CombatSim.CombatEngine.Data.Definitions.Weapons.Bgs import Bgs
from CombatSim.CombatEngine.Data.Definitions.Weapons.TwistedBow import TwistedBow
from CombatSim.CombatEngine.Data.Definitions.Weapons.ToxicBlowpipe import ToxicBlowpipe
from CombatSim.CombatEngine.Data.Definitions.Weapons.EyeOfAyak import EyeOfAyak


class TestPhaseTransitions(unittest.TestCase):
    def test_next_phase_never_repeats(self):
        for _ in range(100):
            next_p = next_nylo_phase(NyloBossPhase.MELEE)
            self.assertNotEqual(next_p, NyloBossPhase.MELEE,
                                "Phase should not repeat MELEE")

            next2 = next_nylo_phase(NyloBossPhase.RANGED)
            self.assertNotEqual(next2, NyloBossPhase.RANGED,
                                "Phase should not repeat RANGED")

            next3 = next_nylo_phase(NyloBossPhase.MAGE)
            self.assertNotEqual(next3, NyloBossPhase.MAGE,
                                "Phase should not repeat MAGE")

    def test_next_phase_is_valid(self):
        valid = {NyloBossPhase.MELEE, NyloBossPhase.RANGED, NyloBossPhase.MAGE}
        for start in valid:
            for _ in range(20):
                self.assertIn(next_nylo_phase(start), valid)

    def test_randomness_covers_all(self):
        results = set()
        for _ in range(200):
            results.add(next_nylo_phase(NyloBossPhase.MELEE))
        self.assertGreater(len(results), 1,
                           "Should eventually return both possible phases")


class TestNyloAttackSchedule(unittest.TestCase):
    def test_requires_name_and_rotation(self):
        with self.assertRaises(ValueError):
            NyloAttackSchedule("", [(Bgs, True)])
        with self.assertRaises(ValueError):
            NyloAttackSchedule("Test", [])

    def test_len_and_getitem(self):
        sched = NyloAttackSchedule("Test", [(Bgs, True), (Bgs, False)])
        self.assertEqual(len(sched), 2)
        self.assertEqual(sched[0], (Bgs, True))
        self.assertEqual(sched[1], (Bgs, False))

    def test_equality(self):
        a = NyloAttackSchedule("A", [(Bgs, True)])
        b = NyloAttackSchedule("A", [(Bgs, True)])
        c = NyloAttackSchedule("B", [(Bgs, True)])
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)

    def test_repr(self):
        sched = NyloAttackSchedule("Foo", [(Bgs, True)])
        r = repr(sched)
        self.assertIn("Foo", r)


class TestAttackSchedules(unittest.TestCase):
    def test_first_melee_has_bgs_spec(self):
        schedule = schedule_for_phase(NyloBossPhase.MELEE, first_melee=True)
        self.assertEqual(schedule, FIRST_MELEE)
        self.assertEqual(schedule[0][0], Bgs)
        self.assertTrue(schedule[0][1])

    def test_regular_melee_no_bgs(self):
        schedule = schedule_for_phase(NyloBossPhase.MELEE, first_melee=False)
        self.assertEqual(schedule, MELEE)
        self.assertNotIn(
            (Bgs, True), schedule.rotation,
            "Regular melee schedule should not include BGS spec"
        )

    def test_ranged_schedule(self):
        schedule = schedule_for_phase(NyloBossPhase.RANGED, first_melee=True)
        self.assertEqual(schedule, RANGED)
        self.assertEqual(schedule[0][0], TwistedBow)

    def test_ranged_after_mage_schedule(self):
        schedule = schedule_for_phase(
            NyloBossPhase.RANGED, first_melee=False,
            prev_phase=NyloBossPhase.MAGE,
        )
        self.assertEqual(schedule, RANGED_AFTER_MAGE)
        self.assertEqual(schedule[0][0], ToxicBlowpipe)
        self.assertEqual(schedule[3][0], TwistedBow)
        self.assertEqual(len(schedule), 4)

    def test_mage_schedule(self):
        schedule = schedule_for_phase(NyloBossPhase.MAGE, first_melee=True)
        self.assertEqual(schedule, MAGE)
        self.assertEqual(schedule[0][0], EyeOfAyak)
        self.assertEqual(len(schedule), 3)


class TestSetupApply(unittest.TestCase):
    def test_melee_setup_applies(self):
        player = _fresh_player()
        _apply_setup(player, melee_setup)
        self.assertTrue(player.ignore_special_attack_cost)

    def test_ranged_setup_applies(self):
        player = _fresh_player()
        _apply_setup(player, ranged_setup)
        self.assertTrue(player.ignore_special_attack_cost)

    def test_ranged_after_mage_setup_applies(self):
        player = _fresh_player()
        _apply_setup(player, ranged_after_mage_setup)
        self.assertTrue(player.ignore_special_attack_cost)

    def test_mage_setup_applies(self):
        player = _fresh_player()
        _apply_setup(player, mage_setup)
        self.assertTrue(player.ignore_special_attack_cost)

    def test_setup_switching(self):
        player = _fresh_player()
        _apply_setup(player, melee_setup)
        _apply_setup(player, ranged_setup)
        _apply_setup(player, mage_setup)
        self.assertTrue(player.ignore_special_attack_cost)


if __name__ == "__main__":
    unittest.main()
