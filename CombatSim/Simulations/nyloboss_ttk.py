#!/usr/bin/env python3
# Run from project root:  PYTHONPATH=. python CombatSim/Simulations/nyloboss_ttk.py

"""NyloBoss TTK — CLI entrypoint.

Usage:
  Debug mode:  PYTHONPATH=. python CombatSim/Simulations/nyloboss_ttk.py
  Batch mode:  PYTHONPATH=. python CombatSim/Simulations/nyloboss_ttk.py -n 5000 -t 8
  Analytics:   PYTHONPATH=. python CombatSim/Simulations/nyloboss_ttk.py -a -n 10000 -t 8 -o results/
  Compare:     PYTHONPATH=. python CombatSim/Simulations/nyloboss_ttk.py --compare -n 5000 -t 8 -o results/
"""

import argparse
import time
import multiprocessing as _mp
from concurrent.futures import ProcessPoolExecutor, as_completed

from CombatSim.Simulations.nyloboss.simulation import (
    simulate_kill,
    run_batch,
    DEFAULT_BOSS_SCALE,
)
from CombatSim.Simulations.nyloboss.configs import DEFAULT_PLAYER_CONFIGS
from CombatSim.Simulations.nyloboss.analytics import run_analytics, run_comparison


def main() -> None:
    parser = argparse.ArgumentParser(description="NyloBoss TTK Simulation")
    parser.add_argument("-n", "--iterations", type=int, default=1,
                        help="Number of iterations (default: 1 = single debug run)")
    parser.add_argument("-t", "--threads", type=int, default=1,
                        help="Parallel workers (default: 1)")
    parser.add_argument("-a", "--analytics", action="store_true",
                        help="Run in analytics mode (stats + graphs)")
    parser.add_argument("-c", "--compare", action="store_true",
                        help="Run both Ayak and Shadow schedules and produce a comparison box plot")
    parser.add_argument("-o", "--output", type=str, default=".",
                        help="Output directory for graphs (default: .)")
    parser.add_argument("-b", "--bins", type=int, default=40,
                        help="Histogram bins for analytics mode (default: 40)")
    parser.add_argument("--debug", action="store_true",
                        help="Show per-tick debug output (single-iteration mode)")
    args = parser.parse_args()

    # ── Comparison mode ──────────────────────────────────────────────
    if args.compare:
        run_comparison(
            iterations=args.iterations,
            num_threads=args.threads,
            output_dir=args.output,
        )
        return

    # ── Analytics mode ────────────────────────────────────────────────
    if args.analytics:
        run_analytics(
            iterations=args.iterations,
            num_threads=args.threads,
            output_dir=args.output,
            bins=args.bins,
        )
        return

    # ── Single debug run ──────────────────────────────────────────────
    if args.iterations == 1:
        killed, ticks = simulate_kill(
            boss_scale=DEFAULT_BOSS_SCALE,
            player_configs=DEFAULT_PLAYER_CONFIGS,
            debug=args.debug,
        )
        if killed:
            print(f"\nNyloBoss dead in {ticks} ticks ({ticks * 0.6:.1f}s)")
        else:
            print(f"\nNyloBoss survived {ticks} ticks")
        return

    # ── Batch mode (summary only, no graphs) ──────────────────────────
    base, rem = divmod(args.iterations, args.threads)
    batch_sizes = [base + 1] * rem + [base] * (args.threads - rem)

    t0 = time.time()
    kills = total_ticks = 0

    with ProcessPoolExecutor(max_workers=args.threads, mp_context=_mp.get_context("spawn")) as executor:
        futures = [
            executor.submit(run_batch, n, DEFAULT_BOSS_SCALE, DEFAULT_PLAYER_CONFIGS)
            for n in batch_sizes
        ]
        for i, future in enumerate(as_completed(futures), 1):
            k, t = future.result()
            kills += k
            total_ticks += t
            print(f"  [{i:>2}/{args.threads}] batch complete")

    elapsed = time.time() - t0
    pct = kills / args.iterations * 100
    avg_ttk = total_ticks / args.iterations
    avg_seconds = avg_ttk * 0.6

    print()
    print("=" * 60)
    print(f"  NyloBoss 3p  |  {args.iterations:,} iters  |  {args.threads} threads")
    print(f"  Kills:       {kills} / {args.iterations}  ({pct:.3f}%)")
    print(f"  Avg TTK:     {avg_ttk:.1f} ticks ({avg_seconds:.1f}s)")
    print(f"  Elapsed:     {elapsed:.2f}s")
    print("=" * 60)


if __name__ == "__main__":
    main()
