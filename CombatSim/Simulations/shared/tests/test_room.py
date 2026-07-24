"""Unit tests for Room and SpawnEntry."""

import unittest
from unittest.mock import MagicMock, patch

from CombatSim.Simulations.shared.Room import Room, SpawnEntry
from CombatSim.Simulations.shared.AttackSchedule import Attack, Setup


def _mock_monster(alive=True):
    m = MagicMock()
    m.is_alive.return_value = alive
    m.is_dead.return_value = not alive
    m.stats = MagicMock()
    m.snapshot.return_value = {}
    m.compute_drain.return_value = (0, {})
    m.restore_snapshot = MagicMock()
    return m


def _mock_player(alive=True):
    p = MagicMock()
    p.is_alive.return_value = alive
    p.is_dead.return_value = not alive
    p.weapon = MagicMock()
    return p


class _MockWeapon:
    attack_range = 1

    @staticmethod
    def get_hit_delay(distance):
        return 0


class TestSpawnEntry(unittest.TestCase):
    def test_requires_key(self):
        with self.assertRaises(ValueError):
            SpawnEntry(key="", factory=lambda: _mock_monster(), trigger_tick=5)

    def test_requires_at_least_one_trigger(self):
        with self.assertRaises(ValueError):
            SpawnEntry(key="add", factory=lambda: _mock_monster())

    def test_tick_based_spawn_not_ready_before_tick(self):
        entry = SpawnEntry(key="add", factory=lambda: _mock_monster(), trigger_tick=10)
        room = Room(tick=5)
        self.assertFalse(entry.should_spawn(room))

    def test_tick_based_spawn_ready_at_tick(self):
        entry = SpawnEntry(key="add", factory=lambda: _mock_monster(), trigger_tick=10)
        room = Room(tick=10)
        self.assertTrue(entry.should_spawn(room))

    def test_tick_based_spawn_ready_after_tick(self):
        entry = SpawnEntry(key="add", factory=lambda: _mock_monster(), trigger_tick=10)
        room = Room(tick=15)
        self.assertTrue(entry.should_spawn(room))

    def test_condition_based_spawn(self):
        entry = SpawnEntry(
            key="add", factory=lambda: _mock_monster(),
            trigger_condition=lambda r: len(r.enemies) == 0 and r.tick >= 3,
        )
        room = Room(tick=2)
        self.assertFalse(entry.should_spawn(room))
        room.tick = 3
        self.assertTrue(entry.should_spawn(room))

    def test_spawn_consumes_entry(self):
        monster = _mock_monster()
        entry = SpawnEntry(key="add", factory=lambda: monster, trigger_tick=0)
        result = entry.spawn()
        self.assertIs(result, monster)
        self.assertTrue(entry._consumed)

    def test_consumed_entry_never_should_spawn(self):
        entry = SpawnEntry(key="add", factory=lambda: _mock_monster(), trigger_tick=0)
        entry.spawn()
        room = Room(tick=100)
        self.assertFalse(entry.should_spawn(room))

    def test_condition_evaluated_before_tick(self):
        calls = 0

        def factory():
            nonlocal calls
            calls += 1
            return _mock_monster()

        entry = SpawnEntry(key="add", factory=factory, trigger_condition=lambda r: True)
        self.assertTrue(entry.should_spawn(Room()))
        entry.spawn()
        self.assertEqual(calls, 1)


class TestRoomBasics(unittest.TestCase):
    def test_default_initialization(self):
        room = Room()
        self.assertEqual(room.tick, 0)
        self.assertEqual(room.players, {})
        self.assertEqual(room.enemies, {})
        self.assertEqual(room.dead_enemies, [])
        self.assertEqual(room.spawn_table, {})
        self.assertEqual(room.instance_timer, 0)
        self.assertEqual(room.instance_timer_cycle_length, 4)
        self.assertFalse(room.actions_blocked_this_tick)

    def test_advance_tick(self):
        room = Room()
        self.assertEqual(room.advance_tick(), 1)
        self.assertEqual(room.tick, 1)

    def test_advance_tick_resets_blocked_flag(self):
        room = Room()
        room.actions_blocked_this_tick = True
        room.advance_tick()
        self.assertFalse(room.actions_blocked_this_tick)

    def test_instance_timer_cycles(self):
        room = Room(instance_timer_cycle_length=4)
        for i in range(1, 5):
            room.advance_tick()
        self.assertEqual(room.tick, 4)
        self.assertEqual(room.instance_timer, 0)

    def test_instance_timer_custom_cycle_length(self):
        room = Room(instance_timer_cycle_length=3)
        room.advance_tick()
        room.advance_tick()
        room.advance_tick()
        self.assertEqual(room.instance_timer, 0)

    def test_alive_enemies(self):
        alive = _mock_monster(alive=True)
        dead = _mock_monster(alive=False)
        room = Room(enemies={"a": alive, "d": dead})
        self.assertEqual(room.alive_enemies, {"a": alive})

    def test_alive_enemies_all_dead(self):
        room = Room(enemies={"d": _mock_monster(alive=False)})
        self.assertEqual(room.alive_enemies, {})

    def test_alive_players(self):
        alive = _mock_player(alive=True)
        dead = _mock_player(alive=False)
        room = Room(players={"p1": alive, "p2": dead})
        self.assertEqual(room.alive_players, {"p1": alive})

    def test_is_encounter_over_no_players(self):
        room = Room(players={}, enemies={"a": _mock_monster(alive=True)})
        self.assertTrue(room.is_encounter_over)

    def test_is_encounter_over_no_enemies(self):
        room = Room(players={"p1": _mock_player(alive=True)}, enemies={})
        self.assertTrue(room.is_encounter_over)

    def test_is_encounter_over_all_alive(self):
        room = Room(
            players={"p1": _mock_player(alive=True)},
            enemies={"boss": _mock_monster(alive=True)},
        )
        self.assertFalse(room.is_encounter_over)

    def test_is_encounter_over_players_dead(self):
        room = Room(
            players={"p1": _mock_player(alive=False)},
            enemies={"boss": _mock_monster(alive=True)},
        )
        self.assertTrue(room.is_encounter_over)

    def test_is_encounter_over_enemies_dead(self):
        room = Room(
            players={"p1": _mock_player(alive=True)},
            enemies={"boss": _mock_monster(alive=False)},
        )
        self.assertTrue(room.is_encounter_over)


class TestActionsBlocked(unittest.TestCase):
    def test_default_is_false(self):
        self.assertFalse(Room().actions_blocked_this_tick)

    def test_can_be_set_externally(self):
        room = Room()
        room.actions_blocked_this_tick = True
        self.assertTrue(room.actions_blocked_this_tick)

    def test_step_resets_via_advance_tick(self):
        room = Room()
        room.actions_blocked_this_tick = True
        room.step()
        self.assertFalse(room.actions_blocked_this_tick)


class TestMoveDeadEnemies(unittest.TestCase):
    def test_moves_dead_to_graveyard(self):
        dead = _mock_monster(alive=False)
        alive = _mock_monster(alive=True)
        room = Room(enemies={"boss": dead, "add": alive})
        moved = room.move_dead_enemies()
        self.assertEqual(moved, [dead])
        self.assertEqual(room.enemies, {"add": alive})
        self.assertEqual(room.dead_enemies, [dead])

    def test_leaves_alive_in_place(self):
        alive = _mock_monster(alive=True)
        room = Room(enemies={"boss": alive})
        self.assertEqual(room.move_dead_enemies(), [])

    def test_all_dead_clears_enemies(self):
        room = Room(enemies={"boss": _mock_monster(alive=False)})
        moved = room.move_dead_enemies()
        self.assertEqual(len(moved), 1)
        self.assertEqual(room.enemies, {})


class TestStep(unittest.TestCase):
    def test_step_advances_tick(self):
        room = Room()
        room.step()
        self.assertEqual(room.tick, 1)

    def test_step_calls_hooks(self):
        calls = []

        class HookRoom(Room):
            def on_tick_start(self):
                calls.append("start")
            def on_tick_end(self):
                calls.append("end")

        HookRoom().step()
        self.assertEqual(calls, ["start", "end"])

    def test_step_spawns_and_moves_dead(self):
        alive = _mock_monster(alive=True)
        dead = _mock_monster(alive=False)
        entry = SpawnEntry(key="wave", factory=lambda: alive, trigger_tick=0)
        room = Room(tick=0, enemies={"boss": dead}, spawn_table={"wave": entry})
        room.step()
        self.assertEqual(room.enemies, {"wave": alive})
        self.assertIn(dead, room.dead_enemies)


class TestRoomSpawning(unittest.TestCase):
    def test_spawn_pending_tick_based(self):
        entry = SpawnEntry(key="add", factory=lambda: _mock_monster(), trigger_tick=5)
        room = Room(tick=3, spawn_table={"add": entry})
        self.assertEqual(room.spawn_pending(), {})
        self.assertIn("add", room.spawn_table)

    def test_spawn_pending_fires_on_tick(self):
        monster = _mock_monster()
        entry = SpawnEntry(key="add", factory=lambda: monster, trigger_tick=5)
        room = Room(tick=5, spawn_table={"add": entry})
        self.assertEqual(room.spawn_pending(), {"add": monster})
        self.assertEqual(room.enemies, {"add": monster})
        self.assertEqual(room.spawn_table, {})

    def test_spawn_pending_skips_duplicate_key(self):
        room = Room(
            tick=5, enemies={"boss": _mock_monster()},
            spawn_table={"boss": SpawnEntry(key="boss", factory=lambda: _mock_monster(), trigger_tick=0)},
        )
        self.assertEqual(room.spawn_pending(), {})
        self.assertEqual(room.spawn_table, {})

    def test_spawn_pending_condition_based(self):
        monster = _mock_monster()

        def condition(r):
            return r.tick >= 3 and len(r.alive_enemies) <= 1

        room = Room(tick=2, spawn_table={
            "add": SpawnEntry(key="add", factory=lambda: monster, trigger_condition=condition),
        })
        self.assertEqual(room.spawn_pending(), {})
        room.tick = 5
        self.assertEqual(room.spawn_pending(), {"add": monster})

    def test_spawn_pending_multiple_entries(self):
        m1, m2 = _mock_monster(), _mock_monster()
        room = Room(tick=10, spawn_table={
            "wave1": SpawnEntry(key="wave1", factory=lambda: m1, trigger_tick=5),
            "wave2": SpawnEntry(key="wave2", factory=lambda: m2, trigger_tick=10),
        })
        self.assertEqual(room.spawn_pending(), {"wave1": m1, "wave2": m2})

    def test_spawn_pending_keeps_unconsumed(self):
        m1 = _mock_monster()
        room = Room(tick=5, spawn_table={
            "now": SpawnEntry(key="now", factory=lambda: m1, trigger_tick=5),
            "later": SpawnEntry(key="later", factory=lambda: _mock_monster(), trigger_tick=20),
        })
        spawned = room.spawn_pending()
        self.assertEqual(len(spawned), 1)
        self.assertEqual(spawned["now"], m1)
        self.assertEqual(len(room.spawn_table), 1)

    def test_spawn_pending_condition_already_met_at_start(self):
        monster = _mock_monster()
        room = Room(tick=0, spawn_table={
            "add": SpawnEntry(key="add", factory=lambda: monster, trigger_condition=lambda r: True),
        })
        self.assertEqual(room.spawn_pending(), {"add": monster})

    def test_dead_enemies_is_list(self):
        m1, m2 = _mock_monster(alive=False), _mock_monster(alive=False)
        room = Room(dead_enemies=[m1, m2])
        self.assertEqual(len(room.dead_enemies), 2)


class TestPlayerAttack(unittest.TestCase):
    def test_attack_resolves_damage(self):
        player = _mock_player(alive=True)
        monster = _mock_monster(alive=True)
        room = Room(players={"p1": player}, enemies={"boss": monster})
        attack = Attack(weapon=_MockWeapon)

        with patch.object(player, "do_attack", return_value=25):
            with patch.object(monster, "reduce_hp") as mock_reduce:
                dmg = room.player_attack(attack, "p1", "boss")
                mock_reduce.assert_called_once_with(25)
                self.assertEqual(dmg, 25)

    def test_attack_passes_special(self):
        player = _mock_player(alive=True)
        monster = _mock_monster(alive=True)
        room = Room(players={"p1": player}, enemies={"boss": monster})
        attack = Attack(weapon=_MockWeapon, use_special_attack=True)

        with patch.object(player, "do_attack", return_value=40) as mock_do:
            dmg = room.player_attack(attack, "p1", "boss")
            mock_do.assert_called_once_with(monster, special_attack=True)
            self.assertEqual(dmg, 40)

    def test_attack_applies_setup(self):
        player = _mock_player(alive=True)
        monster = _mock_monster(alive=True)
        room = Room(players={"p1": player}, enemies={"boss": monster})

        setup = Setup(pieces=[], prayer="piety")
        attack = Attack(weapon=_MockWeapon, setup=setup)

        with patch.object(player, "do_attack", return_value=10):
            with patch.object(room, "_equip_setup") as mock_equip:
                room.player_attack(attack, "p1", "boss")
                mock_equip.assert_called_once_with(player, setup)

    def test_weapon_cached(self):
        player = _mock_player(alive=True)
        monster = _mock_monster(alive=True)
        room = Room(players={"p1": player}, enemies={"boss": monster})

        cls = _MockWeapon
        attack = Attack(weapon=lambda: cls)

        with patch.object(player, "do_attack", return_value=10):
            room.player_attack(attack, "p1", "boss")
        # second call should use cached instance
        self.assertIn(attack.weapon, room._weapon_cache)

    def test_override_works(self):
        class CustomRoom(Room):
            def player_attack(self, attack, player_key, enemy_key):
                damage = super().player_attack(attack, player_key, enemy_key)
                return damage * 2

        player = _mock_player(alive=True)
        monster = _mock_monster(alive=True)
        room = CustomRoom(players={"p1": player}, enemies={"boss": monster})

        with patch.object(player, "do_attack", return_value=10):
            dmg = room.player_attack(Attack(weapon=_MockWeapon), "p1", "boss")
            self.assertEqual(dmg, 20)


class TestNyloRoomSubclass(unittest.TestCase):
    def test_nylo_room_inherits_room(self):
        from CombatSim.Simulations.nyloboss.NyloRoom import NyloRoom
        from CombatSim.Simulations.nyloboss.phases import NyloBossPhase

        nylo = NyloRoom(phase=NyloBossPhase.RANGED)
        self.assertEqual(nylo.phase, NyloBossPhase.RANGED)
        self.assertFalse(nylo.actions_blocked_this_tick)

    def test_advance_phase_sets_actions_blocked(self):
        from CombatSim.Simulations.nyloboss.NyloRoom import NyloRoom
        from CombatSim.Simulations.nyloboss.phases import NyloBossPhase

        nylo = NyloRoom(phase=NyloBossPhase.MELEE, next_phase_tick=10, tick=10)
        nylo.advance_phase()
        self.assertTrue(nylo.actions_blocked_this_tick)
        self.assertNotEqual(nylo.phase, NyloBossPhase.MELEE)
        self.assertFalse(nylo.first_melee)

    def test_player_attack_syncs_boss_defense(self):
        from CombatSim.Simulations.nyloboss.NyloRoom import NyloRoom

        player = _mock_player(alive=True)
        monster = _mock_monster(alive=True)
        monster.stats.def_level = 42
        nylo = NyloRoom(players={"p1": player}, enemies={"boss": monster}, boss_defense=50)

        with patch.object(player, "do_attack", return_value=10):
            nylo.player_attack(Attack(weapon=_MockWeapon), "p1", "boss")
            self.assertEqual(nylo.boss_defense, 42)


if __name__ == "__main__":
    unittest.main()
