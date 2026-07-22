"""Unit tests for the NyloBoss phase system and simulation components."""

import unittest

from CombatSim.Simulations.nyloboss.phases import NyloBossPhase, next_nylo_phase
from CombatSim.Simulations.nyloboss.NyloRoomState import NyloRoomState
from CombatSim.Simulations.nyloboss.NyloRole import NyloRole
from CombatSim.Simulations.nyloboss.NyloBossAttackSchedule import (
    NyloBossAttackSchedule,
    SETUPS,
)
from CombatSim.Simulations.shared.AttackSchedule import Attack, AttackSchedule
from CombatSim.Simulations.nyloboss.simulation import (
    _fresh_player,
    simulate_kill,
    PlayerConfig,
    _PlayerRuntime,
    _init_player_phase,
)
from CombatSim.Simulations.nyloboss.configs import P1, P2, P3
from CombatSim.CombatEngine.Data.Definitions.Weapons.Bgs import Bgs
from CombatSim.CombatEngine.Data.Definitions.Weapons.DragonClaws import DragonClaws
from CombatSim.CombatEngine.Data.Definitions.Weapons.Scythe import Scythe
from CombatSim.CombatEngine.Data.Definitions.Weapons.TwistedBow import TwistedBow
from CombatSim.CombatEngine.Data.Definitions.Weapons.ToxicBlowpipe import ToxicBlowpipe
from CombatSim.CombatEngine.Data.Definitions.Weapons.EyeOfAyak import EyeOfAyak
from CombatSim.CombatEngine.Data.Definitions.Weapons.ZaryteCrossbow import ZaryteCrossbow


def _room_state(phase, first_melee=True, first_ranged=True, prev_phase=None, boss_defense=0):
    return NyloRoomState(
        phase=phase,
        first_melee=first_melee,
        first_ranged=first_ranged,
        prev_phase=prev_phase,
        boss_defense=boss_defense,
    )


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


class TestAttackSchedule(unittest.TestCase):
    def test_requires_name(self):
        with self.assertRaises(ValueError):
            AttackSchedule("", [Attack(Bgs, use_special_attack=True)])

    def test_len_and_getitem(self):
        sched = AttackSchedule("Test", [
            Attack(Bgs, use_special_attack=True),
            Attack(Bgs),
        ])
        self.assertEqual(len(sched), 2)
        self.assertEqual(sched[0].weapon, Bgs)
        self.assertTrue(sched[0].use_special_attack)
        self.assertEqual(sched[1].weapon, Bgs)
        self.assertFalse(sched[1].use_special_attack)

    def test_equality(self):
        a = AttackSchedule("A", [Attack(Bgs, use_special_attack=True)])
        b = AttackSchedule("A", [Attack(Bgs, use_special_attack=True)])
        c = AttackSchedule("B", [Attack(Bgs, use_special_attack=True)])
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)

    def test_repr(self):
        sched = AttackSchedule("Foo", [Attack(Bgs, use_special_attack=True)])
        r = repr(sched)
        self.assertIn("Foo", r)


class TestAttackSetup(unittest.TestCase):
    def test_attack_defaults_no_setup(self):
        atk = Attack(Scythe)
        self.assertIsNone(atk.setup)
        self.assertFalse(atk.use_special_attack)
        self.assertFalse(atk.repeat)

    def test_attack_with_setup(self):
        atk = Attack(Scythe, setup=SETUPS["melee"], use_special_attack=True)
        self.assertEqual(atk.setup, SETUPS["melee"])
        self.assertTrue(atk.use_special_attack)

    def test_equip_setup_applies_gear_and_prayer_and_boosts(self):
        player = _fresh_player()
        schedule = AttackSchedule("Test", [Attack(Scythe)])
        schedule._equip_setup(player, SETUPS["melee"])
        self.assertTrue(player.ignore_special_attack_cost)


class TestNyloBossAttackSchedule(unittest.TestCase):
    # ── BGS role ───────────────────────────────────────────────────────────

    def test_first_melee_has_bgs_spec(self):
        schedule = NyloBossAttackSchedule(role=NyloRole.BGS)
        schedule.update_rotation(_room_state(NyloBossPhase.MELEE, first_melee=True))
        self.assertEqual(schedule[0].weapon, Bgs)
        self.assertTrue(schedule[0].use_special_attack)
        self.assertEqual(schedule[0].setup, SETUPS["melee"])

    def test_regular_melee_no_spec(self):
        schedule = NyloBossAttackSchedule(role=NyloRole.BGS)
        schedule.update_rotation(_room_state(NyloBossPhase.MELEE, first_melee=False))
        self.assertEqual(schedule[0].weapon, Scythe)
        self.assertEqual(schedule[0].setup, SETUPS["melee"])
        self.assertIsNone(schedule[1].setup)

    def test_ranged_schedule(self):
        schedule = NyloBossAttackSchedule(role=NyloRole.BGS)
        schedule.update_rotation(_room_state(NyloBossPhase.RANGED, first_ranged=True))
        self.assertEqual(schedule[0].weapon, ZaryteCrossbow)

    def test_mage_schedule(self):
        schedule = NyloBossAttackSchedule(role=NyloRole.BGS)
        schedule.update_rotation(_room_state(NyloBossPhase.MAGE))
        self.assertEqual(schedule[0].weapon, EyeOfAyak)
        self.assertEqual(schedule[0].setup, SETUPS["mage"])

    # ── Claws role ─────────────────────────────────────────────────────────

    def test_first_melee_claws_has_claws_spec(self):
        schedule = NyloBossAttackSchedule(role=NyloRole.CLAWS)
        schedule.update_rotation(_room_state(NyloBossPhase.MELEE, first_melee=True))
        self.assertEqual(schedule[0].weapon, DragonClaws)

    def test_ranged_mage_same_as_bgs(self):
        for phase in [NyloBossPhase.RANGED, NyloBossPhase.MAGE]:
            bgs = NyloBossAttackSchedule(role=NyloRole.BGS)
            bgs.update_rotation(_room_state(phase, first_ranged=False))
            claws = NyloBossAttackSchedule(role=NyloRole.CLAWS)
            claws.update_rotation(_room_state(phase, first_ranged=False))
            self.assertEqual(bgs.rotation, claws.rotation)

    def test_first_ranged_zcb_spec(self):
        schedule = NyloBossAttackSchedule(role=NyloRole.CLAWS)
        schedule.update_rotation(_room_state(NyloBossPhase.RANGED, first_ranged=True))
        self.assertEqual(schedule[0].weapon, ZaryteCrossbow)

    def test_ranged_after_first_no_zcb_spec(self):
        schedule = NyloBossAttackSchedule(role=NyloRole.CLAWS)
        schedule.update_rotation(_room_state(NyloBossPhase.RANGED, first_ranged=False))
        self.assertEqual(schedule[0].weapon, TwistedBow)

    # ── Backup BGS role ────────────────────────────────────────────────────

    def test_backup_first_melee_always_bgs(self):
        schedule = NyloBossAttackSchedule(role=NyloRole.BACKUP_BGS)
        room_state = _room_state(NyloBossPhase.MELEE, first_melee=True, boss_defense=50)
        schedule.update_rotation(room_state)
        self.assertEqual(schedule[0].weapon, Scythe)
        self.assertEqual(schedule[1].weapon, Bgs)
        self.assertTrue(schedule[1].use_special_attack)

    def test_backup_repeat_melee_bgs_when_def_high(self):
        schedule = NyloBossAttackSchedule(role=NyloRole.BACKUP_BGS)
        schedule.update_rotation(_room_state(NyloBossPhase.MELEE, first_melee=False, boss_defense=50))
        self.assertEqual(schedule[0].weapon, Scythe)
        self.assertEqual(schedule[1].weapon, Bgs)
        self.assertTrue(schedule[1].use_special_attack)

    def test_backup_repeat_melee_claws_when_def_low(self):
        schedule = NyloBossAttackSchedule(role=NyloRole.BACKUP_BGS)
        schedule.update_rotation(_room_state(NyloBossPhase.MELEE, first_melee=False, boss_defense=10))
        self.assertEqual(schedule[0].weapon, Scythe)
        self.assertEqual(schedule[1].weapon, DragonClaws)
        self.assertTrue(schedule[1].use_special_attack)

    def test_backup_repeat_melee_claws_at_threshold(self):
        schedule = NyloBossAttackSchedule(role=NyloRole.BACKUP_BGS)
        schedule.update_rotation(_room_state(NyloBossPhase.MELEE, first_melee=False, boss_defense=20))
        self.assertEqual(schedule[0].weapon, Scythe)
        self.assertEqual(schedule[1].weapon, DragonClaws)
        self.assertTrue(schedule[1].use_special_attack)

    def test_backup_repeat_melee_bgs_just_above_threshold(self):
        schedule = NyloBossAttackSchedule(role=NyloRole.BACKUP_BGS)
        schedule.update_rotation(_room_state(NyloBossPhase.MELEE, first_melee=False, boss_defense=21))
        self.assertEqual(schedule[0].weapon, Scythe)
        self.assertEqual(schedule[1].weapon, Bgs)
        self.assertTrue(schedule[1].use_special_attack)


class TestPlayerConfig(unittest.TestCase):
    def test_default_names(self):
        self.assertEqual(P1.name, "P1")
        self.assertEqual(P2.name, "P2")
        self.assertEqual(P3.name, "P3")

    def test_p1_uses_bgs_role(self):
        self.assertEqual(P1.attack_schedule.role, NyloRole.BGS)

    def test_p2_uses_backup_bgs_role(self):
        self.assertEqual(P2.attack_schedule.role, NyloRole.BACKUP_BGS)

    def test_p3_uses_claws_role(self):
        self.assertEqual(P3.attack_schedule.role, NyloRole.CLAWS)


class TestPlayerRuntime(unittest.TestCase):
    def test_init_player_phase_defaults(self):
        player = _fresh_player()
        cfg = PlayerConfig(name="Test", attack_schedule=NyloBossAttackSchedule(role=NyloRole.BGS))
        rt = _PlayerRuntime(player, cfg)
        _init_player_phase(rt, _room_state(NyloBossPhase.MELEE, first_melee=True))
        self.assertEqual(rt.attack_schedule[0].weapon, Bgs)
        self.assertTrue(rt.attack_schedule[0].use_special_attack)
        self.assertEqual(rt.schedule_idx, 0)
        self.assertEqual(rt.weapon_on_cooldown, 0)

    def test_init_player_phase_claws_schedule(self):
        player = _fresh_player()
        cfg = PlayerConfig(name="Claws", attack_schedule=NyloBossAttackSchedule(role=NyloRole.CLAWS))
        rt = _PlayerRuntime(player, cfg)
        _init_player_phase(rt, _room_state(NyloBossPhase.MELEE, first_melee=True))
        self.assertEqual(rt.attack_schedule[0].weapon, DragonClaws)
        self.assertTrue(rt.attack_schedule[0].use_special_attack)
        self.assertEqual(rt.schedule_idx, 0)

    def test_init_player_phase_custom_setup(self):
        calls = []

        def custom_setup(phase, prev_phase):
            calls.append((phase, prev_phase))
            return SETUPS["melee"]

        player = _fresh_player()
        cfg = PlayerConfig(name="Custom", setup_fn=custom_setup, attack_schedule=NyloBossAttackSchedule(role=NyloRole.BGS))
        rt = _PlayerRuntime(player, cfg)
        _init_player_phase(rt, _room_state(
            NyloBossPhase.RANGED, first_melee=False,
            prev_phase=NyloBossPhase.MAGE,
        ))
        self.assertEqual(calls, [(NyloBossPhase.RANGED, NyloBossPhase.MAGE)])


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
            boss_scale=1, player_configs=[PlayerConfig(name="Solo", attack_schedule=NyloBossAttackSchedule(role=NyloRole.BGS))], debug=False,
        )
        self.assertTrue(killed, "Solo player should kill NyloBoss at scale 1")

    def test_two_player_scale_2(self):
        players = [PlayerConfig(name=f"Player{i+1}", attack_schedule=NyloBossAttackSchedule(role=NyloRole.BGS)) for i in range(2)]
        killed, ticks = simulate_kill(
            boss_scale=2, player_configs=players, debug=False,
        )
        self.assertTrue(killed, "2 players should kill NyloBoss at scale 2")


if __name__ == "__main__":
    unittest.main()
