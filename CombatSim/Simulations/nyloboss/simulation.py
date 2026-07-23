"""NyloBoss Time-to-Kill Simulation."""

from dataclasses import dataclass
from typing import Callable, List, Tuple

from CombatSim.CombatEngine.Data.Definitions.Monsters.NyloBoss import NyloBoss
from CombatSim.CombatEngine.Domain.Player import Player
from CombatSim.CombatEngine.Domain.Stats import Stats

from CombatSim.Simulations.nyloboss.phases import NyloBossPhase
from CombatSim.Simulations.nyloboss.NyloBossAttackSchedule import NyloBossAttackSchedule
from CombatSim.Simulations.nyloboss.NyloRoom import NyloRoom

DEFAULT_BOSS_SCALE = 3

_PLAYER_LEVELS = {
    "hp_level": 99, "attack_level": 99, "strength_level": 99,
    "def_level": 99, "magic_level": 99, "ranged_level": 99, "prayer_level": 99,
}


def _fresh_player() -> Player:
    level_dict = {
        k: v for k, v in vars(Stats(_PLAYER_LEVELS)).items()
        if k in Stats.LEVEL_KEYS
    }
    player = Player(stats=level_dict)
    player.ignore_special_attack_cost = True
    player._validate_ammo = lambda: None
    return player


@dataclass
class PlayerConfig:
    name: str
    attack_schedule: NyloBossAttackSchedule
    setup_fn: Callable | None = None


class _PlayerRuntime:
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


def _init_player_phase(rt: _PlayerRuntime, room: NyloRoom) -> None:
    if rt.config.setup_fn is not None:
        setup = rt.config.setup_fn(room.phase, room.prev_phase)
        rt.attack_schedule._equip_setup(rt.player, setup)
    rt.attack_schedule.update_rotation(room)
    rt.schedule_idx = 0


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
    if player_configs is None:
        from CombatSim.Simulations.nyloboss.configs import DEFAULT_PLAYER_CONFIGS
        player_configs = DEFAULT_PLAYER_CONFIGS
    configs = player_configs
    monster = NyloBoss(boss_scale)

    runtimes: List[_PlayerRuntime] = []
    for cfg in configs:
        player = _fresh_player()
        rt = _PlayerRuntime(player, cfg)
        runtimes.append(rt)

    room = NyloRoom(
        enemies={"boss": monster},
        players={cfg.name: rt.player for cfg, rt in zip(configs, runtimes)},
        phase=NyloBossPhase.MELEE,
        first_melee=True,
        first_ranged=True,
        prev_phase=None,
        boss_defense=monster.stats.def_level,
        phase_duration=10,
        next_phase_tick=10,
    )

    for rt in runtimes:
        _init_player_phase(rt, room)

    MAX_TICKS = 10000
    while not monster.is_dead() and room.tick < MAX_TICKS:

        # ── Phase transition ──────────────────────────────────────────
        if room.tick >= room.next_phase_tick:
            room.advance_phase()
            if debug:
                _dbg_phase_change(
                    room.prev_phase, room.phase, room.tick,
                    monster.current_hp, room.boss_defense,
                )
            for rt in runtimes:
                _init_player_phase(rt, room)

        # ── Attacks ───────────────────────────────────────────────────
        hits: List[_HitRecord] = []

        for rt in runtimes:
            if rt.weapon_on_cooldown > 0:
                rt.weapon_on_cooldown -= 1
                continue

            if room.actions_blocked_this_tick and rt.schedule_idx == 0:
                continue

            if rt.schedule_idx >= len(rt.attack_schedule):
                continue

            attack = rt.attack_schedule.get_next_attack(rt.schedule_idx, room)
            rt.schedule_idx += 1

            dmg = room.player_attack(attack, rt.config.name, "boss")

            hits.append(_HitRecord(
                player_name=rt.config.name,
                weapon_name=rt.player.weapon.name,
                damage=dmg,
                is_spec=attack.use_special_attack,
            ))

            rt.weapon_on_cooldown = rt.player.weapon.attack_speed - 1
            rt.current_weapon_name = rt.player.weapon.name

            if monster.is_dead():
                break

        if debug:
            _dbg_tick_summary(room.tick, hits, monster.current_hp, room.boss_defense)

        if monster.is_dead():
            if debug:
                print(f"  >>> NYLOBOSS DEFEATED at tick {room.tick + 1}")
            room.step()
            return True, room.tick

        room.step()

    return monster.is_dead(), room.tick


# ── Debug ───────────────────────────────────────────────────────────────────

_PHASE_LABELS = {
    NyloBossPhase.MELEE: "MELEE",
    NyloBossPhase.RANGED: "RANGED",
    NyloBossPhase.MAGE: "MAGE",
}


def _dbg_tick_summary(tick, hits, boss_hp=0, boss_defense=0):
    def state():
        return f"  hp={boss_hp}  def={boss_defense}"
    if hits:
        parts = []
        for h in hits:
            spec_str = " [SPEC]" if h.is_spec else ""
            parts.append(f"[{h.player_name}] ({h.weapon_name}{spec_str}) dmg={h.damage}")
        joined = "  ".join(parts)
        print(f"  tick {tick:>4}  {joined}{state()}")
    else:
        print(f"  tick {tick:>4}{state()}")


def _dbg_phase_change(old, new, tick, boss_hp, boss_defense=0):
    print(f"  tick {tick:>4}  --- {_PHASE_LABELS[old]} -> {_PHASE_LABELS[new]}  |  boss_hp={boss_hp}  def={boss_defense} ---")


def run_batch(count, boss_scale=DEFAULT_BOSS_SCALE, player_configs=None):
    kills = total_ticks = 0
    for _ in range(count):
        killed, t = simulate_kill(boss_scale=boss_scale, player_configs=player_configs)
        total_ticks += t
        if killed:
            kills += 1
    return kills, total_ticks


def run_batch_with_data(count, boss_scale=DEFAULT_BOSS_SCALE, player_configs=None):
    ticks: List[int] = []
    kills = 0
    for _ in range(count):
        killed, t = simulate_kill(boss_scale=boss_scale, player_configs=player_configs, debug=False)
        ticks.append(t if killed else float('inf'))
        if killed:
            kills += 1
    return ticks, kills
