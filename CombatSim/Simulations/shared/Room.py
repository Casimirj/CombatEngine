from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

from CombatSim.CombatEngine.Domain.Monster import Monster
from CombatSim.CombatEngine.Domain.Player import Player
from CombatSim.CombatEngine.Domain.Weapon import Weapon
from CombatSim.CombatEngine.Data.Registries.GearRegistry import GearRegistry
from CombatSim.CombatEngine.Data.Registries.PrayerRegistry import PrayerRegistry
from CombatSim.CombatEngine.Data.Registries.PotionRegistry import PotionRegistry


@dataclass
class SpawnEntry:
    key: str
    factory: Callable[[], Monster]
    trigger_tick: Optional[int] = None
    trigger_condition: Optional[Callable[["Room"], bool]] = None
    _consumed: bool = field(default=False, init=False, repr=False)

    def __post_init__(self):
        if not self.key:
            raise ValueError("SpawnEntry requires a non-empty key")
        if self.trigger_tick is None and self.trigger_condition is None:
            raise ValueError(
                "SpawnEntry requires at least one of trigger_tick or trigger_condition"
            )

    def should_spawn(self, room: "Room") -> bool:
        if self._consumed:
            return False
        if self.trigger_tick is not None and room.tick >= self.trigger_tick:
            return True
        if self.trigger_condition is not None and self.trigger_condition(room):
            return True
        return False

    def spawn(self) -> Monster:
        self._consumed = True
        return self.factory()


@dataclass
class Room:
    players: Dict[str, Player] = field(default_factory=dict)
    enemies: Dict[str, Monster] = field(default_factory=dict)
    dead_enemies: List[Monster] = field(default_factory=list)
    tick: int = 0
    spawn_table: Dict[str, SpawnEntry] = field(default_factory=dict)
    instance_timer_cycle_length: int = 4
    instance_timer: int = 0
    actions_blocked_this_tick: bool = field(default=False, init=False, repr=False)

    _weapon_cache: Dict[type, Weapon] = field(default_factory=dict, init=False, repr=False)

    # ── Lifecycle hooks ────────────────────────────────────────────────

    def step(self):
        self.on_tick_start()
        spawned = self.spawn_pending()
        self.move_dead_enemies()
        self.advance_tick()
        self.on_tick_end()
        return spawned

    def on_tick_start(self):
        pass

    def on_tick_end(self):
        pass

    # ── Tick ───────────────────────────────────────────────────────────

    def advance_tick(self) -> int:
        self.tick += 1
        self.instance_timer += 1
        if self.instance_timer >= self.instance_timer_cycle_length:
            self.instance_timer = 0
        self.actions_blocked_this_tick = False
        return self.tick

    # ── Combat ─────────────────────────────────────────────────────────

    def _equip_setup(self, player: Player, setup) -> None:
        """Clear current gear and equip a new phase setup."""
        player.clear_gear()
        gear_pieces = [GearRegistry.get(name) for name in setup.pieces]
        player.equip_gear(*gear_pieces)
        player.prayer = PrayerRegistry.get(setup.prayer)
        player.boosts = [PotionRegistry.get(b) for b in setup.boosts] if setup.boosts else []

    def player_attack(self, attack, player_key: str, enemy_key: str) -> int:
        """Apply the attack's setup (if any), equip its weapon, and
        resolve the hit against the enemy.

        Weapon instances are cached per class so the same object is
        reused across ticks.

        Returns the damage dealt (0 on miss).

        Override in subclasses for encounter-specific post-attack logic
        (defense sync, phase immunity, etc.).
        """
        player = self.players[player_key]
        enemy = self.enemies[enemy_key]

        if attack.setup is not None:
            self._equip_setup(player, attack.setup)

        weapon_cls = attack.weapon
        if weapon_cls not in self._weapon_cache:
            self._weapon_cache[weapon_cls] = weapon_cls()
        weapon = self._weapon_cache[weapon_cls]
        player.equip_weapon(weapon)

        damage = player.do_attack(
            enemy,
            special_attack=attack.use_special_attack,
        )
        enemy.reduce_hp(damage)
        return damage

    # ── Spawning ───────────────────────────────────────────────────────

    def spawn_pending(self):
        spawned: Dict[str, Monster] = {}
        for key, entry in list(self.spawn_table.items()):
            if key in self.enemies or entry._consumed:
                del self.spawn_table[key]
                continue
            if entry.should_spawn(self):
                monster = entry.spawn()
                self.enemies[key] = monster
                spawned[key] = monster
                del self.spawn_table[key]
        return spawned

    # ── Enemy lifecycle ────────────────────────────────────────────────

    def move_dead_enemies(self):
        moved = []
        for key, monster in list(self.enemies.items()):
            if monster.is_dead():
                self.dead_enemies.append(monster)
                del self.enemies[key]
                moved.append(monster)
        return moved

    # ── Queries ────────────────────────────────────────────────────────

    @property
    def alive_enemies(self):
        return {k: e for k, e in self.enemies.items() if e.is_alive()}

    @property
    def alive_players(self):
        return {k: p for k, p in self.players.items() if p.is_alive()}

    @property
    def is_encounter_over(self):
        return not self.alive_players or not self.alive_enemies
