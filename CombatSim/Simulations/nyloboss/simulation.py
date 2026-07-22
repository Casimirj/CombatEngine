"""NyloBoss Time-to-Kill Simulation.

N players attack a NyloBoss (default: 3-scale / 5-man HP) that rotates
through Melee, Ranged, and Mage phases every 10 ticks. Each player is
independent — they switch gear at phase boundaries and follow their own
attack schedule with their own cooldown timer.

Per-player schedule differences are supported via ``PlayerConfig`` without
touching the simulation loop.  Module-level ``P1`` / ``P2`` / ``P3`` config
instances are wired to the same default schedules for now; swap their
``attack_schedule`` to give a player a custom rotation.
"""

from dataclasses import dataclass, field
from typing import Callable, List, Tuple

from CombatSim.CombatEngine.Data.Definitions.Monsters.NyloBoss import NyloBoss
from CombatSim.CombatEngine.Domain.Player import Player
from CombatSim.CombatEngine.Domain.Stats import Stats

from CombatSim.Simulations.nyloboss.phases import NyloBossPhase, next_nylo_phase
from CombatSim.Simulations.nyloboss.NyloBossAttackSchedule import NyloBossAttackSchedule, NyloRole
from CombatSim.Simulations.nyloboss.NyloRoomState import NyloRoomState

PHASE_TICK_DURATION = 10
DEFAULT_BOSS_SCALE = 3

_PLAYER_LEVELS = {
    "hp_level": 99, "attack_level": 99, "strength_level": 99,
    "def_level": 99, "magic_level": 99, "ranged_level": 99, "prayer_level": 99,
}

# ── Weapon Cache ────────────────────────────────────────────────────────────

_WEAPON_CACHE: dict = {}

def _cached_weapon(weapon_cls: type):
    if weapon_cls not in _WEAPON_CACHE:
        _WEAPON_CACHE[weapon_cls] = weapon_cls()
    return _WEAPON_CACHE[weapon_cls]


def _fresh_player() -> Player:
    level_dict = {
        k: v for k, v in vars(Stats(_PLAYER_LEVELS)).items()
        if k in Stats.LEVEL_KEYS
    }
    player = Player(stats=level_dict)
    player.ignore_special_attack_cost = True
    player._validate_ammo = lambda: None  # Skip ammo validation for phase-switching sims
    return player


# ── Player Configuration ───────────────────────────────────────────────────

@dataclass
class PlayerConfig:
    """Per-player schedule and setup configuration.

    When ``setup_fn`` is ``None`` the schedule's own gear logic is used.
    ``attack_schedule`` is a ``NyloBossAttackSchedule`` instance that
    drives per-player attack rotation and gear switching.
    """
    name: str = "Player"
    setup_fn: Callable | None = None
    attack_schedule: NyloBossAttackSchedule = field(
        default_factory=lambda: NyloBossAttackSchedule(role=NyloRole.BGS),
    )


# ── Default 3-player configs (BGS for P1; claws-first for P2 & P3) ─────────

P1 = PlayerConfig(
    name="P1",
    attack_schedule=NyloBossAttackSchedule(role=NyloRole.BGS),
)
P2 = PlayerConfig(
    name="P2",
    attack_schedule=NyloBossAttackSchedule(role=NyloRole.CLAWS),
)
P3 = PlayerConfig(
    name="P3",
    attack_schedule=NyloBossAttackSchedule(role=NyloRole.CLAWS),
)
DEFAULT_PLAYER_CONFIGS: List[PlayerConfig] = [P1, P2, P3]


class _PlayerRuntime:
    """Mutable per-player state during a single simulation run."""

    __slots__ = (
        "player", "config", "attack_schedule", "schedule_idx",
        "weapon_on_cooldown", "current_weapon_name",
    )

    def __init__(self, player: Player, config: PlayerConfig) -> None:
        self.player = player
        self.config = config
        self.attack_schedule: NyloBossAttackSchedule = config.attack_schedule
        self.schedule_idx: int = 0
        self.weapon_on_cooldown: int = 0
        self.current_weapon_name: str = ""


def _init_player_phase(rt: _PlayerRuntime, room_state: NyloRoomState) -> None:
    """(Re-)initialise a player's schedule for a new boss phase."""
    if rt.config.setup_fn is not None:
        setup = rt.config.setup_fn(room_state.phase, room_state.prev_phase)
        rt.attack_schedule._equip_setup(rt.player, setup)
    rt.attack_schedule.update_rotation(room_state)
    rt.schedule_idx = 0


# ── Data-carrying helper types ──────────────────────────────────────────────

@dataclass
class _HitRecord:
    player_name: str
    weapon_name: str
    damage: int
    is_spec: bool


def simulate_kill(
    boss_scale: int = DEFAULT_BOSS_SCALE,
    player_configs: List[PlayerConfig] | None = None,
    debug: bool = False,
) -> Tuple[bool, int]:
    """Run a single kill simulation. Returns (killed, total_ticks)."""
    configs = player_configs or DEFAULT_PLAYER_CONFIGS
    monster = NyloBoss(boss_scale)

    # Build runtimes
    runtimes: List[_PlayerRuntime] = []
    for cfg in configs:
        player = _fresh_player()
        rt = _PlayerRuntime(player, cfg)
        runtimes.append(rt)

    # Start in a random phase already in progress
    from random import choice as _choice
    phase = _choice(list(NyloBossPhase))
    room_state = NyloRoomState(
        phase=phase,
        first_melee=True,
        first_ranged=True,
        prev_phase=None,
        boss_defense=monster.stats.def_level,
    )
    next_phase_tick = PHASE_TICK_DURATION

    for rt in runtimes:
        _init_player_phase(rt, room_state)

    # ── Main tick loop ──────────────────────────────────────────────
    current_tick = 0
    total_ticks = 0

    while not monster.is_dead():
        just_transitioned = False
        if current_tick >= next_phase_tick:
            old_phase = room_state.phase
            room_state.prev_phase = old_phase
            room_state.phase = next_nylo_phase(old_phase)
            if old_phase == NyloBossPhase.MELEE:
                room_state.first_melee = False
            if old_phase == NyloBossPhase.RANGED:
                room_state.first_ranged = False

            for rt in runtimes:
                _init_player_phase(rt, room_state)

            next_phase_tick += PHASE_TICK_DURATION
            just_transitioned = True
            if debug:
                _dbg_phase_change(old_phase, room_state.phase, current_tick)

        # ── Collect all hits this tick ────────────────────────────────
        hits: List[_HitRecord] = []

        for rt in runtimes:
            # Cooldown ticking
            if rt.weapon_on_cooldown > 0:
                rt.weapon_on_cooldown -= 1
                continue

            # Skip first attack slot on the transition tick itself
            if just_transitioned and rt.schedule_idx == 0:
                continue

            # Schedule exhausted for this player
            if rt.schedule_idx >= len(rt.attack_schedule):
                continue

            # Attack
            attack = rt.attack_schedule[rt.schedule_idx]
            use_spec = attack.use_special_attack
            if attack.setup is not None:
                rt.attack_schedule._equip_setup(rt.player, attack.setup)
            weapon_cls = attack.weapon
            weapon = _cached_weapon(weapon_cls)
            rt.player.equip_weapon(weapon)
            rt.schedule_idx += 1

            dmg = rt.player.do_attack(monster, special_attack=use_spec)
            monster.reduce_hp(dmg)

            hits.append(_HitRecord(
                player_name=rt.config.name,
                weapon_name=weapon.name,
                damage=dmg,
                is_spec=use_spec,
            ))

            rt.weapon_on_cooldown = weapon.attack_speed - 1
            rt.current_weapon_name = weapon.name

            if monster.is_dead():
                break

        # ── Print debug line (always one line per tick) ───────────
        if debug:
            _dbg_tick_summary(current_tick, hits, monster.current_hp)

        if monster.is_dead():
            if debug:
                print(f"  >>> NYLOBOSS DEFEATED at tick {total_ticks + 1}")
            return True, total_ticks + 1

        # Advance the global clock by one tick
        current_tick += 1
        total_ticks += 1

    return monster.is_dead(), total_ticks


# ── Debug Helpers ───────────────────────────────────────────────────────────

_PHASE_LABELS = {
    NyloBossPhase.MELEE: "MELEE",
    NyloBossPhase.RANGED: "RANGED",
    NyloBossPhase.MAGE: "MAGE",
}


def _dbg_tick_summary(
    tick: int,
    hits: List[_HitRecord],
    boss_hp: int,
) -> None:
    """Print one line for a tick: all player hits, then boss HP after."""
    if hits:
        parts = []
        for h in hits:
            spec_str = " [SPEC]" if h.is_spec else ""
            parts.append(f"[{h.player_name}] ({h.weapon_name}{spec_str}) dmg={h.damage}")
        joined = "  ".join(parts)
        print(f"  tick {tick:>4}  {joined}  |  boss_hp={boss_hp}")
    else:
        print(f"  tick {tick:>4}  |  boss_hp={boss_hp}")


def _dbg_phase_change(
    old: NyloBossPhase, new: NyloBossPhase, tick: int,
) -> None:
    print(f"  tick {tick:>4}  --- {_PHASE_LABELS[old]} -> {_PHASE_LABELS[new]} ---")


def run_batch(
    count: int,
    boss_scale: int = DEFAULT_BOSS_SCALE,
    player_configs: List[PlayerConfig] | None = None,
) -> Tuple[int, int]:
    """Simulate *count* kills.  Returns (kills, total_ticks)."""
    kills = total_ticks = 0
    for _ in range(count):
        killed, t = simulate_kill(boss_scale=boss_scale, player_configs=player_configs)
        total_ticks += t
        if killed:
            kills += 1
    return kills, total_ticks

def run_batch_with_data(
    count: int,
    boss_scale: int = DEFAULT_BOSS_SCALE,
    player_configs: List[PlayerConfig] | None = None,
) -> Tuple[List[int], int]:
    """Simulate *count* kills, collecting per-kill tick counts.

    Returns:
        (tick_list, kills) — tick_list has one entry per iteration.
    """
    ticks: List[int] = []
    kills = 0
    for _ in range(count):
        killed, t = simulate_kill(boss_scale=boss_scale, player_configs=player_configs,
                                  debug=False)
        ticks.append(t if killed else float('inf'))
        if killed:
            kills += 1
    return ticks, kills
