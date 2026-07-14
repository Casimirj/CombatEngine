#!/usr/bin/env python3
# Run from project root:  PYTHONPATH=. python CombatSim/Simulations/bloat_chance_to_kill.py

"""Bloat Chance-to-Kill Simulation.

Three OathTorvaRancour players attack a scale-3 Bloat with interleaved
round-robin ticks: all players fire the same weapon before the next tick.
Iterations are parallelised across threads at the batch level.
"""

import copy
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import List, Tuple

from CombatSim.CombatEngine.Data.Definitions.Monsters.Bloat import Bloat
from CombatSim.CombatEngine.Data.Definitions.Weapons.Scythe import Scythe
from CombatSim.CombatEngine.Data.Definitions.Weapons.CrystalHalberd import CrystalHalberd
from CombatSim.CombatEngine.Data.Definitions.Weapons.DragonClaws import DragonClaws
from CombatSim.CombatEngine.Data.Registries.LoadoutRegistry import LoadoutRegistry
from CombatSim.CombatEngine.Domain.Player import Player

# ── Config ──────────────────────────────────────────────────────────────────
NUM_ITERATIONS = 100_000
NUM_THREADS    = 16
NUM_PLAYERS    = 3
LOADOUT_NAME   = "OathTorvaSalve"

# Round-robin attack order: each player fires the same (weapon, spec?) tick
# before everyone moves to the next tick.
TICK_ROTATION: List[Tuple[type, bool]] = [
    (CrystalHalberd, True),
    (Scythe,          False),
    (Scythe,          False),
    (Scythe,          False),
    (Scythe,          False),
    (CrystalHalberd, True),
    (DragonClaws,     True),
    (Scythe,          False),
    (Scythe,          False),
    (Scythe,          False),
    (Scythe,          False),
    (Scythe,          False),
]


def _fresh_player() -> Player:
    """Deep-copy the OathTorvaSalve loadout so threads run independently."""
    template = LoadoutRegistry.get(LOADOUT_NAME)
    if template is None:
        raise RuntimeError(f"Unknown loadout: {LOADOUT_NAME}")
    player = copy.deepcopy(template)
    player.current_special_attack = 9999  # ignore spec costs
    return player


def _simulate_kill() -> Tuple[bool, int]:
    """One kill attempt. Returns (killed, total_damage)."""
    monster = Bloat(scale=3)
    total_damage = 0
    players = [_fresh_player() for _ in range(NUM_PLAYERS)]

    for weapon_cls, use_spec in TICK_ROTATION:
        for player in players:
            weapon = weapon_cls()
            player.equip_weapon(weapon)
            dmg = player.do_attack(monster, special_attack=use_spec)
            monster.reduce_hp(dmg)
            total_damage += dmg
            if monster.is_dead():
                return True, total_damage

    return monster.is_dead(), total_damage


def _run_batch(count: int) -> Tuple[int, int]:
    """Simulate *count* kills. Returns (kills, total_damage)."""
    kills = total_damage = 0
    for _ in range(count):
        killed, dmg = _simulate_kill()
        total_damage += dmg
        if killed:
            kills += 1
    return kills, total_damage


def main() -> None:
    base, rem = divmod(NUM_ITERATIONS, NUM_THREADS)
    batch_sizes = [base + 1] * rem + [base] * (NUM_THREADS - rem)

    t0 = time.time()
    kills = total_damage = 0

    with ProcessPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = [executor.submit(_run_batch, n) for n in batch_sizes]
        for i, future in enumerate(as_completed(futures), 1):
            k, d = future.result()
            kills += k
            total_damage += d
            print(f"  [{i:>2}/{NUM_THREADS}] batch complete")

    elapsed = time.time() - t0
    pct = kills / NUM_ITERATIONS * 100
    avg_dmg = total_damage / NUM_ITERATIONS

    print()
    print("=" * 60)
    print(f"  Bloat scale-3  |  {NUM_PLAYERS} players  |  "
          f"{NUM_ITERATIONS:,} iters  |  {NUM_THREADS} threads")
    print(f"  Kills:    {kills} / {NUM_ITERATIONS}  ({pct:.3f}%)")
    print(f"  Avg dmg:  {avg_dmg:.1f}")
    print(f"  Elapsed:  {elapsed:.2f}s")
    print("=" * 60)


if __name__ == "__main__":
    main()
