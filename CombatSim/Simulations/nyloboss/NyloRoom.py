"""NyloRoom — a NyloBoss-specific Room subclass."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from CombatSim.CombatEngine.Domain.Monster import Monster
from CombatSim.CombatEngine.Domain.Player import Player
from CombatSim.Simulations.shared.Room import Room, SpawnEntry
from CombatSim.Simulations.nyloboss.phases import NyloBossPhase, next_nylo_phase


@dataclass
class NyloRoom(Room):
    """Room subclass that adds NyloBoss phase-tracking fields."""

    phase: NyloBossPhase = NyloBossPhase.MELEE
    first_melee: bool = True
    first_ranged: bool = True
    prev_phase: Optional[NyloBossPhase] = None
    boss_defense: int = 0
    phase_duration: int = 10
    next_phase_tick: int = 10

    players: Dict[str, Player] = field(default_factory=dict)
    enemies: Dict[str, Monster] = field(default_factory=dict)
    dead_enemies: List[Monster] = field(default_factory=list)
    tick: int = 0
    spawn_table: Dict[str, SpawnEntry] = field(default_factory=dict)
    instance_timer_cycle_length: int = 4
    instance_timer: int = 0
    actions_blocked_this_tick: bool = field(default=False, init=False, repr=False)

    # ── Phase rotation ─────────────────────────────────────────────────

    def on_tick_start(self) -> None:
        if self.tick >= self.next_phase_tick:
            self.advance_phase()

    def advance_phase(self) -> None:
        old_phase = self.phase
        self.prev_phase = old_phase
        self.phase = next_nylo_phase(old_phase)
        if old_phase == NyloBossPhase.MELEE:
            self.first_melee = False
        if old_phase == NyloBossPhase.RANGED:
            self.first_ranged = False
        self.next_phase_tick += self.phase_duration
        self.actions_blocked_this_tick = True

    # ── Combat ─────────────────────────────────────────────────────────

    def player_attack(self, attack, player_key: str, enemy_key: str) -> int:
        if enemy_key not in self.enemies:
            return 0
        damage = super().player_attack(attack, player_key, enemy_key)
        if enemy_key in self.enemies:
            self.boss_defense = self.enemies[enemy_key].stats.def_level
        return damage
