"""NyloBoss Time-to-Kill Simulation.

One player attacks a solo-scale NyloBoss that rotates through Melee,
Ranged, and Mage phases every 8 ticks. The player switches gear at each
phase boundary and follows per-phase attack schedules.
"""

from dataclasses import dataclass, field
from typing import List, Tuple

from CombatSim.CombatEngine.Data.Definitions.Monsters.NyloBoss import NyloBoss
from CombatSim.CombatEngine.Domain.Player import Player
from CombatSim.CombatEngine.Data.Registries.GearRegistry import GearRegistry
from CombatSim.CombatEngine.Data.Registries.PrayerRegistry import PrayerRegistry
from CombatSim.CombatEngine.Data.Registries.PotionRegistry import PotionRegistry
from CombatSim.CombatEngine.Domain.Stats import Stats

from CombatSim.Simulations.nyloboss.phases import NyloBossPhase, next_nylo_phase
from CombatSim.Simulations.nyloboss.schedules import (
    NyloAttackSchedule,
    schedule_for_phase,
)

PHASE_TICK_DURATION = 8
BOSS_SCALE = 1

_PLAYER_LEVELS = {
    "hp_level": 99, "attack_level": 99, "strength_level": 99,
    "def_level": 99, "magic_level": 99, "ranged_level": 99, "prayer_level": 99,
}


@dataclass
class Setup:
    """Bundles gear pieces, prayer, and boosts for a single phase."""
    pieces: List[str]
    prayer: str
    boosts: List[str] = field(default_factory=list)


# ── Phase Setups ────────────────────────────────────────────────────────────

MELEE_SETUP = Setup(
    pieces=[
        'Torva full helm',
        'Infernal cape',
        'Salve (e)',
        'Torva platebody',
        'Torva platelegs',
        'Ferocious gloves',
        'Primordial boots',
        'Berserker ring (i)',
        'Avernic defender',
    ],
    prayer="piety",
    boosts=["super_combat"],
)

RANGED_SETUP = Setup(
    pieces=[
        'Void ranger helm',
        "Dizana's quiver",
        'Necklace of anguish',
        'Elite void top',
        'Elite void robe',
        'Void knight gloves',
        'Amethyst arrows',
    ],
    prayer="rigour",
    boosts=["bastion"],
)

MAGE_SETUP = Setup(
    pieces=[
        'Void mage helm',
        'Imbued saradomin cape',
        'Occult necklace',
        'Elite void top',
        'Elite void robe',
        'Void knight gloves',
        'Ward of elidinis (f)',
        'Magus ring',
    ],
    prayer="augury",
    boosts=["imbued_heart"],
)


def _apply_setup(player: Player, setup: Setup):
    """Re-gear the player for a new phase setup."""
    player.clear_gear()
    gears = [GearRegistry.get(name) for name in setup.pieces]
    player.equip_gear(*gears)
    player.prayer = PrayerRegistry.get(setup.prayer)
    player.boosts = [PotionRegistry.get(b) for b in setup.boosts] if setup.boosts else []


def _fresh_player() -> Player:
    level_dict = {
        k: v for k, v in vars(Stats(_PLAYER_LEVELS)).items()
        if k in Stats.LEVEL_KEYS
    }
    player = Player(stats=level_dict)
    player.ignore_special_attack_cost = True
    return player


_SETUPS_BY_PHASE = {
    NyloBossPhase.MELEE: MELEE_SETUP,
    NyloBossPhase.RANGED: RANGED_SETUP,
    NyloBossPhase.MAGE: MAGE_SETUP,
}


# ── Simulation Core ─────────────────────────────────────────────────────────

def simulate_kill(debug: bool = False) -> Tuple[bool, int]:
    """One kill attempt. Returns (killed, total_ticks).

    When debug=True, prints every tick, phase change, and attack.
    """
    monster = NyloBoss(scale=BOSS_SCALE)
    player = _fresh_player()

    total_ticks = 0
    current_tick = 0
    first_melee = True

    phase = NyloBossPhase.MELEE
    _apply_setup(player, MELEE_SETUP)
    schedule: NyloAttackSchedule = schedule_for_phase(phase, first_melee)

    schedule_idx = 0
    next_phase_tick = PHASE_TICK_DURATION

    weapon_on_cooldown = 0
    current_weapon_name = ""

    while True:
        if monster.is_dead():
            if debug:
                print(f"  >>> NYLOBOSS DEFEATED at tick {total_ticks}")
            return True, total_ticks

        # Phase transition — gear swaps, but cooldown persists
        just_transitioned = False
        if current_tick >= next_phase_tick:
            old_phase = phase
            phase = next_nylo_phase(phase)

            if old_phase == NyloBossPhase.MELEE:
                first_melee = False

            _apply_setup(player, _SETUPS_BY_PHASE[phase])
            schedule = schedule_for_phase(phase, first_melee)
            schedule_idx = 0
            next_phase_tick += PHASE_TICK_DURATION

            just_transitioned = True
            if debug:
                _dbg_phase_change(old_phase, phase, current_tick, weapon_on_cooldown)

        # On cooldown — tick down (allowed during transition)
        if weapon_on_cooldown > 0:
            weapon_on_cooldown -= 1
            if debug and not just_transitioned:
                _dbg_cooldown_tick(current_tick, current_weapon_name)
            current_tick += 1
            total_ticks += 1
            continue

        # Transition tick with no cooldown — just skip this tick
        if just_transitioned:
            current_tick += 1
            total_ticks += 1
            continue

        # Ready to attack — dequeue next weapon
        if schedule_idx >= len(schedule):
            break

        weapon_cls, use_spec = schedule[schedule_idx]
        weapon = weapon_cls()
        player.equip_weapon(weapon)

        schedule_idx += 1

        dmg = player.do_attack(monster, special_attack=use_spec)
        monster.reduce_hp(dmg)

        if debug:
            _dbg_attack_hit(current_tick, weapon.name, dmg, monster.current_hp, use_spec)

        # Cooldown starts after the attack lands
        weapon_on_cooldown = weapon.attack_speed - 1
        current_weapon_name = weapon.name
        current_tick += 1
        total_ticks += 1

    return monster.is_dead(), total_ticks


# ── Debug Helpers ───────────────────────────────────────────────────────────

_PHASE_LABELS = {
    NyloBossPhase.MELEE: "MELEE",
    NyloBossPhase.RANGED: "RANGED",
    NyloBossPhase.MAGE: "MAGE",
}

def _dbg_phase_change(
    old: NyloBossPhase,
    new: NyloBossPhase,
    tick: int,
    cooldown: int = 0,
):
    cooldown_str = f" (on cooldown: {cooldown} remaining)" if cooldown > 0 else ""
    print(f"  tick {tick:>4}  --- {_PHASE_LABELS[old]} -> {_PHASE_LABELS[new]}{cooldown_str} ---")


def _dbg_attack_hit(
    tick: int,
    weapon_name: str,
    damage: int,
    boss_hp: int,
    is_spec: bool,
):
    spec_str = " [SPEC]" if is_spec else ""
    print(f"  tick {tick:>4}  ({weapon_name}{spec_str})  damage={damage:>3}  boss_hp={boss_hp}")


def _dbg_cooldown_tick(
    tick: int,
    weapon_name: str,
):
    print(f"  tick {tick:>4}")


def run_batch(count: int) -> Tuple[int, int]:
    """Simulate *count* kills. Returns (kills, total_ticks)."""
    kills = total_ticks = 0
    for _ in range(count):
        killed, t = simulate_kill()
        total_ticks += t
        if killed:
            kills += 1
    return kills, total_ticks
