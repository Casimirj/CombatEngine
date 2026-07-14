#!/usr/bin/env python3
# Run from project root:  PYTHONPATH=. python CombatSim/Simulations/nyloboss_ttk.py

"""NyloBoss TTK — CLI entrypoint.

The simulation logic lives under CombatSim/Simulations/nyloboss/.
"""

import time
from concurrent.futures import ProcessPoolExecutor, as_completed

from CombatSim.Simulations.nyloboss.simulation import simulate_kill, run_batch

# ── Config ──────────────────────────────────────────────────────────────────
NUM_ITERATIONS = 1          # Single run for debugging
NUM_THREADS = 1
DEBUG = True


def main() -> None:
    if NUM_ITERATIONS == 1:
        killed, ticks = simulate_kill(debug=DEBUG)
        if killed:
            print(f"\nNyloBoss dead in {ticks} ticks ({ticks * 0.6:.1f}s)")
        else:
            print(f"\nNyloBoss survived {ticks} ticks")
        return

    # Parallel batch mode
    base, rem = divmod(NUM_ITERATIONS, NUM_THREADS)
    batch_sizes = [base + 1] * rem + [base] * (NUM_THREADS - rem)

    t0 = time.time()
    kills = total_ticks = 0

    with ProcessPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = [executor.submit(run_batch, n) for n in batch_sizes]
        for i, future in enumerate(as_completed(futures), 1):
            k, t = future.result()
            kills += k
            total_ticks += t
            print(f"  [{i:>2}/{NUM_THREADS}] batch complete")

    elapsed = time.time() - t0
    pct = kills / NUM_ITERATIONS * 100
    avg_ttk = total_ticks / NUM_ITERATIONS
    avg_seconds = avg_ttk * 0.6

    print()
    print("=" * 60)
    print(f"  NyloBoss solo  |  {NUM_ITERATIONS:,} iters  |  {NUM_THREADS} threads")
    print(f"  Kills:       {kills} / {NUM_ITERATIONS}  ({pct:.3f}%)")
    print(f"  Avg TTK:     {avg_ttk:.1f} ticks ({avg_seconds:.1f}s)")
    print(f"  Elapsed:     {elapsed:.2f}s")
    print("=" * 60)


if __name__ == "__main__":
    main()
