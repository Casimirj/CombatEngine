#!/usr/bin/env python3
# Run from project root:  PYTHONPATH=. python CombatSim/Simulations/bloat_chance_to_kill.py

"""Bloat Chance-to-Kill Simulation.

Three OathTorvaRancour players with Scythe of Vitur attack a scale-3 Bloat.
Each player rotation: 10 scythe hits → 2 chally specs → 1 claw spec.
Outputs kill percentage after N iterations.
"""

import random
import time
from typing import Tuple

from CombatSim.CombatEngine.Data.Definitions.Monsters.Bloat import Bloat
from CombatSim.CombatEngine.Data.Definitions.Weapons.Scythe import Scythe
from CombatSim.CombatEngine.Data.Definitions.Weapons.CrystalHalberd import CrystalHalberd
from CombatSim.CombatEngine.Data.Definitions.Weapons.DragonClaws import DragonClaws
from CombatSim.CombatEngine.Data.Registries.LoadoutRegistry import LoadoutRegistry
from CombatSim.CombatEngine.Data.Registries.WeaponRegistry import WeaponRegistry
from CombatSim.CombatEngine.Domain.Player import Player

# ── config ──────────────────────────────────────────────────────────────────
NUM_ITERATIONS = 100_000
NUM_PLAYERS = 3
SCYTHE_HITS = 10
CHALLY_SPECS = 2
CLAW_SPECS = 1
LOADOUT_NAME = "OathTorvaRancour"


def _get_player() -> Player:
    """Return a fresh OathTorvaRancour player, ready for weapon equipping."""
    player = LoadoutRegistry.get(LOADOUT_NAME)
    if player is None:
        raise RuntimeError(f"Unknown loadout: {LOADOUT_NAME}")
    # Reset spec energy for a clean simulation start.
    player.current_special_attack = 110
    return player


def _run_one_iteration() -> Tuple[bool, int]:
    """Run one simulated kill attempt.

    Returns (killed: bool, total_damage: int).
    """
    monster = Bloat(scale=3)
    total_damage = 0

    for _ in range(NUM_PLAYERS):
        player = _get_player()

        # ── 10 scythe hits ──────────────────────────────────────────────
        scythe = Scythe()
        player.equip_weapon(scythe)
        for _ in range(SCYTHE_HITS):
            dmg = player.do_attack(monster, special_attack=False)
            monster.reduce_hp(dmg)
            total_damage += dmg
            if monster.is_dead():
                return True, total_damage

        # ── 2 chally specs ─────────────────────────────────────────────
        chally = CrystalHalberd()
        player.equip_weapon(chally)
        for _ in range(CHALLY_SPECS):
            dmg = player.do_attack(monster, special_attack=True)
            monster.reduce_hp(dmg)
            total_damage += dmg
            if monster.is_dead():
                return True, total_damage

        # ── 1 claw spec ────────────────────────────────────────────────
        claws = DragonClaws()
        player.equip_weapon(claws)
        for _ in range(CLAW_SPECS):
            dmg = player.do_attack(monster, special_attack=True)
            monster.reduce_hp(dmg)
            total_damage += dmg
            if monster.is_dead():
                return True, total_damage

    return monster.is_dead(), total_damage


def main() -> None:
    kills = 0
    total_damage = 0

    t0 = time.time()

    for i in range(NUM_ITERATIONS):
        killed, dmg = _run_one_iteration()
        total_damage += dmg
        if killed:
            kills += 1

        if (i + 1) % 1000 == 0:
            pct = kills / (i + 1) * 100
            avg_dmg = total_damage / (i + 1)
            print(f"  [{i + 1:>5}/{NUM_ITERATIONS}]  kills: {kills:>4}  "
                  f"rate: {pct:6.3f}%  avg_dmg: {avg_dmg:.1f}")

    pct = kills / NUM_ITERATIONS * 100
    avg_dmg = total_damage / NUM_ITERATIONS
    print()
    print("=" * 60)
    print(f"  Bloat scale-3  |  {NUM_PLAYERS} players  |  {NUM_ITERATIONS:,} iterations")
    print(f"  Kills: {kills} / {NUM_ITERATIONS}  ({pct:.3f}%)")
    print(f"  Avg total damage: {avg_dmg:.1f}")
    print(f"  Elapsed: {time.time() - t0:.2f}s")
    print("=" * 60)


if __name__ == "__main__":
    main()
