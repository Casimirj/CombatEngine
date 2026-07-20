"""Unit tests for the NyloBoss phase system and simulation components."""

import unittest

from CombatSim.Simulations.nyloboss.phases import NyloBossPhase, next_nylo_phase
from CombatSim.Simulations.nyloboss.schedules import (
    NyloAttackSchedule,
    schedule_for_phase,
    schedule_for_phase_claws,
    FIRST_MELEE,
    FIRST_MELEE_CLAWS,
    FIRST_RANGED,
    MELEE,
    MELEE_CLAWS,
    RANGED,
    RANGED_AFTER_MAGE,
    MAGE,
    melee_setup,
    ranged_setup,
    ranged_after_mage_setup,
    mage_setup,
)
from CombatSim.Simulations.nyloboss.simulation import (
    _apply_setup,
    _fresh_player,
    simulate_kill,
    PlayerConfig,
    P1, P2, P3,
    DEFAULT_PLAYER_CONFIGS,
    _PlayerRuntime,
    _init_player_phase,
)
from CombatSim.CombatEngine.Data.Definitions.Weapons.Bgs import Bgs
from CombatSim.CombatEngine.Data.Definitions.Weapons.DragonClaws import DragonClaws
from CombatSim.CombatEngine.Data.Definitions.Weapons.Scythe import Scythe
from CombatSim.CombatEngine.Data.Definitions.Weapons.TwistedBow import TwistedBow
from CombatSim.CombatEngine.Data.Definitions.Weapons.ToxicBlowpipe import ToxicBlowpipe
from CombatSim.CombatEngine.Data.Definitions.Weapons.EyeOfAyak import EyeOfAyak
from CombatSim.CombatEngine.Data.Definitions.Weapons.ZaryteCrossbow import ZaryteCrossbow


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
        self.assertEqual(schedule, FIRST_RANGED)
        self.assertEqual(schedule[0][0], ZaryteCrossbow)
        self.assertTrue(schedule[0][1])
        self.assertEqual(schedule[1][0], TwistedBow)

    def test_ranged_after_mage_schedule(self):
        schedule = schedule_for_phase(
            NyloBossPhase.RANGED, first_melee=False,
            prev_phase=NyloBossPhase.MAGE, first_ranged=False,
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

    # ── Claws schedule tests ───────────────────────────────────────────────

    def test_first_melee_claws_has_claws_spec(self):
        schedule = schedule_for_phase_claws(NyloBossPhase.MELEE, first_melee=True)
        self.assertEqual(schedule, FIRST_MELEE_CLAWS)
        self.assertEqual(schedule[0][0], DragonClaws)
        self.assertTrue(schedule[0][1])
        self.assertEqual(schedule[1][0], Scythe)
        self.assertFalse(schedule[1][1])

    def test_regular_melee_claws_no_spec(self):
        schedule = schedule_for_phase_claws(NyloBossPhase.MELEE, first_melee=False)
        self.assertEqual(schedule, MELEE_CLAWS)
        self.assertNotIn(
            (DragonClaws, True), schedule.rotation,
            "Regular melee-claws schedule should not include claws spec"
        )

    def test_claws_ranged_mage_same_as_bgs(self):
        for phase, first in [
            (NyloBossPhase.RANGED, True),
            (NyloBossPhase.RANGED, False),
            (NyloBossPhase.MAGE, True),
            (NyloBossPhase.MAGE, False),
        ]:
            bgs_sched = schedule_for_phase(phase, first, first_ranged=False)
            claws_sched = schedule_for_phase_claws(phase, first, first_ranged=False)
            self.assertEqual(bgs_sched, claws_sched,
                             f"{phase} schedule should be identical for BGS and claws when first_ranged=False")

    # ── ZCB / first_ranged tests ────────────────────────────────────────────

    def test_first_ranged_zcb_spec(self):
        schedule = schedule_for_phase_claws(NyloBossPhase.RANGED, first_melee=True)
        self.assertEqual(schedule, FIRST_RANGED)
        self.assertEqual(schedule[0][0], ZaryteCrossbow)
        self.assertTrue(schedule[0][1])

    def test_ranged_after_first_no_zcb_spec(self):
        schedule = schedule_for_phase(NyloBossPhase.RANGED, first_melee=True, first_ranged=False)
        self.assertEqual(schedule, RANGED)
        self.assertEqual(schedule[0][0], TwistedBow)


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


class TestPlayerConfig(unittest.TestCase):
    def test_default_names(self):
        self.assertEqual(P1.name, "P1")
        self.assertEqual(P2.name, "P2")
        self.assertEqual(P3.name, "P3")

    def test_default_player_configs_length(self):
        self.assertEqual(len(DEFAULT_PLAYER_CONFIGS), 3)
        self.assertIs(DEFAULT_PLAYER_CONFIGS[0], P1)
        self.assertIs(DEFAULT_PLAYER_CONFIGS[1], P2)
        self.assertIs(DEFAULT_PLAYER_CONFIGS[2], P3)

    def test_p1_uses_bgs_defaults(self):
        self.assertIsNone(P1.setup_fn)
        self.assertIsNone(P1.schedule_fn)

    def test_p2_and_p3_use_claws_schedule(self):
        self.assertIs(P2.schedule_fn, schedule_for_phase_claws)
        self.assertIs(P3.schedule_fn, schedule_for_phase_claws)

    def test_p2_claws_schedule_on_first_melee(self):
        result = P2.schedule_fn(NyloBossPhase.MELEE, True, None, True)
        self.assertEqual(result, FIRST_MELEE_CLAWS)

    def test_p3_claws_schedule_on_melee(self):
        result = P3.schedule_fn(NyloBossPhase.MELEE, False, None, True)
        self.assertEqual(result, MELEE_CLAWS)


class TestPlayerRuntime(unittest.TestCase):
    def test_init_player_phase_defaults(self):
        player = _fresh_player()
        cfg = PlayerConfig(name="Test")
        rt = _PlayerRuntime(player, cfg)
        _init_player_phase(rt, NyloBossPhase.MELEE, first_melee=True, prev_phase=None)
        self.assertEqual(rt.schedule, FIRST_MELEE)
        self.assertEqual(rt.schedule_idx, 0)
        self.assertEqual(rt.weapon_on_cooldown, 0)

    def test_init_player_phase_claws_schedule(self):
        player = _fresh_player()
        cfg = PlayerConfig(name="Claws", schedule_fn=schedule_for_phase_claws)
        rt = _PlayerRuntime(player, cfg)
        _init_player_phase(rt, NyloBossPhase.MELEE, first_melee=True, prev_phase=None)
        self.assertEqual(rt.schedule, FIRST_MELEE_CLAWS)
        self.assertEqual(rt.schedule_idx, 0)

    def test_init_player_phase_custom_setup(self):
        calls = []

        def custom_setup(phase, prev_phase):
            calls.append((phase, prev_phase))
            return melee_setup

        player = _fresh_player()
        cfg = PlayerConfig(name="Custom", setup_fn=custom_setup)
        rt = _PlayerRuntime(player, cfg)
        _init_player_phase(rt, NyloBossPhase.RANGED, first_melee=False, prev_phase=NyloBossPhase.MAGE)
        self.assertEqual(calls, [(NyloBossPhase.RANGED, NyloBossPhase.MAGE)])

    def test_init_player_phase_custom_schedule(self):
        player = _fresh_player()
        cfg = PlayerConfig(name="Custom", schedule_fn=lambda p, fm, pp, fr: MELEE)
        rt = _PlayerRuntime(player, cfg)
        _init_player_phase(rt, NyloBossPhase.MAGE, first_melee=True, prev_phase=None)
        self.assertEqual(rt.schedule, MELEE)


class TestMultiPlayerSimulation(unittest.TestCase):
    def test_three_player_kill(self):
        killed, ticks = simulate_kill(
            boss_scale=3, player_configs=[P1, P2, P3], debug=False,
        )
        self.assertTrue(killed, "3 players should kill NyloBoss at scale 3")
        self.assertLess(ticks, 500, "Kill took unreasonably long")

    def test_default_player_configs_kill(self):
        killed, ticks = simulate_kill(boss_scale=3, debug=False)
        self.assertTrue(killed)
        self.assertLess(ticks, 500)

    def test_solo_player_scale_1(self):
        killed, ticks = simulate_kill(
            boss_scale=1, player_configs=[PlayerConfig(name="Solo")], debug=False,
        )
        self.assertTrue(killed, "Solo player should kill NyloBoss at scale 1")

    def test_two_player_scale_2(self):
        players = [PlayerConfig(name=f"Player{i+1}") for i in range(2)]
        killed, ticks = simulate_kill(
            boss_scale=2, player_configs=players, debug=False,
        )
        self.assertTrue(killed, "2 players should kill NyloBoss at scale 2")


if __name__ == "__main__":
    unittest.main()
