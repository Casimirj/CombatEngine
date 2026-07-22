"""NyloBoss TTK Analytics — batch simulation with stats & graphs."""

from __future__ import annotations

import math
import time
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing as _mp
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import matplotlib
matplotlib.use("Agg")  # non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

from CombatSim.Simulations.nyloboss.simulation import (
    DEFAULT_BOSS_SCALE,
    PlayerConfig,
    run_batch_with_data,
)
from CombatSim.Simulations.nyloboss.configs import DEFAULT_PLAYER_CONFIGS


# ── Stats container ─────────────────────────────────────────────────────────

@dataclass
class TTKStats:
    iterations: int
    kills: int
    kill_pct: float
    ticks: List[int]  # only successful kills
    min_ttk: int
    max_ttk: int
    median_ttk: float
    mean_ttk: float
    std_ttk: float
    percentiles: Dict[str, float]  # p25, p50, p75, p90, p95, p99
    elapsed_s: float


def compute_stats(ticks_raw: List[int], elapsed_s: float) -> TTKStats:
    """Compute descriptive statistics from raw tick list (inf = survived)."""
    kills = sum(1 for t in ticks_raw if t != float("inf"))
    iterations = len(ticks_raw)
    ticks = sorted([t for t in ticks_raw if t != float("inf")])
    arr = np.array(ticks, dtype=np.float64)

    return TTKStats(
        iterations=iterations,
        kills=kills,
        kill_pct=kills / iterations * 100 if iterations else 0.0,
        ticks=ticks,
        min_ttk=int(arr.min()) if len(arr) else 0,
        max_ttk=int(arr.max()) if len(arr) else 0,
        median_ttk=float(np.median(arr)) if len(arr) else 0.0,
        mean_ttk=float(arr.mean()) if len(arr) else 0.0,
        std_ttk=float(arr.std()) if len(arr) else 0.0,
        percentiles={
            "p25": float(np.percentile(arr, 25)) if len(arr) else 0.0,
            "p50": float(np.percentile(arr, 50)) if len(arr) else 0.0,
            "p75": float(np.percentile(arr, 75)) if len(arr) else 0.0,
            "p90": float(np.percentile(arr, 90)) if len(arr) else 0.0,
            "p95": float(np.percentile(arr, 95)) if len(arr) else 0.0,
            "p99": float(np.percentile(arr, 99)) if len(arr) else 0.0,
        },
        elapsed_s=elapsed_s,
    )


# ── Reporting ───────────────────────────────────────────────────────────────

def print_stats(stats: TTKStats) -> None:
    """Pretty-print TTK statistics."""
    def _t(t: float) -> str:
        return f"{t} ticks ({t * 0.6:.1f}s)"

    print()
    print("=" * 60)
    print(f"  NyloBoss TTK Analytics")
    print("=" * 60)
    print(f"  Iterations:   {stats.iterations:,}")
    print(f"  Kills:        {stats.kills:,} / {stats.iterations:,}  "
          f"({stats.kill_pct:.3f}%)")
    print(f"  Min TTK:      {_t(stats.min_ttk)}")
    print(f"  Max TTK:      {_t(stats.max_ttk)}")
    print(f"  Median TTK:   {_t(stats.median_ttk)}")
    print(f"  Mean TTK:     {_t(stats.mean_ttk)}")
    print(f"  Std Dev:      {stats.std_ttk:.1f} ticks ({stats.std_ttk * 0.6:.1f}s)")
    print(f"  ── Percentiles ──")
    for label, key in [("25th", "p25"), ("50th", "p50"), ("75th", "p75"),
                       ("90th", "p90"), ("95th", "p95"), ("99th", "p99")]:
        print(f"  {label:>5}:     {_t(stats.percentiles[key])}")
    print(f"  Elapsed:      {stats.elapsed_s:.2f}s")
    print("=" * 60)


# ── Plotting ────────────────────────────────────────────────────────────────

def plot_histogram(
    stats: TTKStats,
    out_path: str = "nyloboss_ttk_histogram.png",
    bins: int = 40,
) -> None:
    """Save a histogram of TTK distributions."""
    arr = np.array(stats.ticks, dtype=np.float64)
    if len(arr) == 0:
        print("No kills to plot.")
        return

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.hist(arr * 0.6, bins=bins, color="#4C72B0", edgecolor="white", alpha=0.85)

    # Vertical lines
    for label, val, color, style in [
        ("Median", stats.median_ttk * 0.6, "#DD8452", "--"),
        ("Mean", stats.mean_ttk * 0.6, "#55A868", "-"),
    ]:
        ax.axvline(val, color=color, linestyle=style, linewidth=2,
                   label=f"{label}: {val:.1f}s")

    ax.set_xlabel("Time to Kill (seconds)")
    ax.set_ylabel("Frequency")
    ax.set_title(
        f"NyloBoss TTK Distribution\n"
        f"{stats.kills:,} kills / {stats.iterations:,} iterations "
        f"({stats.kill_pct:.2f}%)"
    )
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"\n  Histogram saved → {out_path}")


def plot_boxplot(
    stats: TTKStats,
    out_path: str = "nyloboss_ttk_boxplot.png",
    num_players: int = 3,
    boss_scale: int = DEFAULT_BOSS_SCALE,
) -> None:
    """Save a horizontal box plot of TTK."""
    arr = np.array(stats.ticks, dtype=np.float64) * 0.6
    if len(arr) == 0:
        print("No kills to plot.")
        return

    fig, ax = plt.subplots(figsize=(10, 3))

    bp = ax.boxplot(
        arr,  orientation="horizontal", patch_artist=True, widths=0.5,
        flierprops={"marker": "o", "markersize": 3, "alpha": 0.4,
                    "markerfacecolor": "#4C72B0"},
        medianprops={"color": "#DD8452", "linewidth": 2},
        boxprops={"facecolor": "#4C72B0", "alpha": 0.5},
    )

    # Overlay scatter (if not too many points)
    if len(arr) <= 5000:
        jitter = np.random.default_rng(42).uniform(-0.12, 0.12, size=len(arr))
        ax.scatter(arr, np.ones_like(arr) + jitter, alpha=0.15, s=8,
                   color="#4C72B0", edgecolors="none")

    ax.set_yticks([1])
    ax.set_yticklabels([f"{num_players}p vs {boss_scale}-scale NyloBoss"])
    ax.set_xlabel("Time to Kill (seconds)")
    ax.set_title(
        f"NyloBoss TTK: min={stats.min_ttk * 0.6:.1f}s  "
        f"median={stats.median_ttk * 0.6:.1f}s  "
        f"max={stats.max_ttk * 0.6:.1f}s  "
        f"({stats.kills:,} kills)"
    )
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"  Box plot saved → {out_path}")


# ── Runner ──────────────────────────────────────────────────────────────────

def run_analytics(
    iterations: int = 10000,
    num_threads: int = 8,
    boss_scale: int = DEFAULT_BOSS_SCALE,
    player_configs: List[PlayerConfig] | None = None,
    output_dir: str = ".",
    bins: int = 40,
) -> TTKStats:
    """Run a batch simulation and produce stats + plots.

    Args:
        iterations: total number of runs.
        num_threads: number of parallel worker processes.
        boss_scale: NyloBoss scale (default 3).
        player_configs: per-player configs.
        output_dir: directory for PNG outputs.
        bins: histogram resolution.

    Returns:
        TTKStats with all computed metrics.
    """
    if player_configs is None:
        player_configs = DEFAULT_PLAYER_CONFIGS

    # Distribute work across threads
    base, rem = divmod(iterations, num_threads)
    batch_sizes = [base + 1] * rem + [base] * (num_threads - rem)
    batch_sizes = [b for b in batch_sizes if b > 0]

    all_ticks: List[int] = []
    total_kills = 0

    t0 = time.time()

    with ProcessPoolExecutor(max_workers=num_threads, mp_context=_mp.get_context("spawn")) as executor:
        futures = [
            executor.submit(run_batch_with_data, n, boss_scale, player_configs)
            for n in batch_sizes
        ]
        for i, future in enumerate(as_completed(futures), 1):
            ticks, kills = future.result()
            all_ticks.extend(ticks)
            total_kills += kills
            if i % max(1, len(batch_sizes) // 10) == 0:
                print(f"  [{i:>3}/{len(batch_sizes)}] batches complete  "
                      f"({total_kills:,} kills so far)")

    elapsed = time.time() - t0

    stats = compute_stats(all_ticks, elapsed)
    print_stats(stats)

    # Plots
    import os
    os.makedirs(output_dir, exist_ok=True)
    plot_histogram(stats, os.path.join(output_dir, "nyloboss_ttk_histogram.png"), bins=bins)
    plot_boxplot(stats, os.path.join(output_dir, "nyloboss_ttk_boxplot.png"),
                 num_players=len(player_configs), boss_scale=boss_scale)

    return stats


# ── Quick CLI ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="NyloBoss TTK Analytics")
    parser.add_argument("-n", "--iterations", type=int, default=1000,
                        help="Number of simulation iterations (default: 1000)")
    parser.add_argument("-t", "--threads", type=int, default=8,
                        help="Number of parallel workers (default: 8)")
    parser.add_argument("-s", "--scale", type=int, default=DEFAULT_BOSS_SCALE,
                        help=f"Boss scale (default: {DEFAULT_BOSS_SCALE})")
    parser.add_argument("-o", "--output", type=str, default=".",
                        help="Output directory for plots (default: .)")
    parser.add_argument("-b", "--bins", type=int, default=40,
                        help="Histogram bins (default: 40)")
    args = parser.parse_args()

    run_analytics(
        iterations=args.iterations,
        num_threads=args.threads,
        boss_scale=args.scale,
        output_dir=args.output,
        bins=args.bins,
    )
