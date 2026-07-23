"""NyloBoss TTK Analytics — batch simulation with stats & graphs."""

from __future__ import annotations

import math
import os
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
from CombatSim.Simulations.nyloboss.NyloBossShadowAttackSchedule import NyloBossShadowAttackSchedule
from CombatSim.Simulations.nyloboss.NyloRole import NyloRole


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


@dataclass
class ComparisonResult:
    label_a: str
    stats_a: TTKStats
    label_b: str
    stats_b: TTKStats


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

def print_stats(stats: TTKStats, label: str = "NyloBoss TTK Analytics") -> None:
    """Pretty-print TTK statistics."""
    def _t(t: float) -> str:
        return f"{t} ticks ({t * 0.6:.1f}s)"

    print()
    print("=" * 60)
    print(f"  {label}")
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
    for lbl, key in [("25th", "p25"), ("50th", "p50"), ("75th", "p75"),
                     ("90th", "p90"), ("95th", "p95"), ("99th", "p99")]:
        print(f"  {lbl:>5}:     {_t(stats.percentiles[key])}")
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


def plot_comparison_boxplot(
    result: ComparisonResult,
    out_path: str = "nyloboss_ttk_comparison.png",
    num_players: int = 3,
    boss_scale: int = DEFAULT_BOSS_SCALE,
) -> None:
    """Save a side-by-side box plot comparing two TTK distributions."""
    arr_a = np.array(result.stats_a.ticks, dtype=np.float64) * 0.6
    arr_b = np.array(result.stats_b.ticks, dtype=np.float64) * 0.6

    if len(arr_a) == 0 and len(arr_b) == 0:
        print("No kills to plot.")
        return

    fig, ax = plt.subplots(figsize=(12, 5))

    data = []
    colors = ["#4C72B0", "#E24A33"]
    if len(arr_a) > 0:
        data.append(arr_a)
    if len(arr_b) > 0:
        data.append(arr_b)

    bp = ax.boxplot(
        data, vert=False, patch_artist=True, widths=0.6,
        flierprops={"marker": "o", "markersize": 3, "alpha": 0.35,
                    "markerfacecolor": "#555555"},
        medianprops={"color": "#333333", "linewidth": 2.5},
        boxprops={"linewidth": 1.5},
    )

    for patch, color in zip(bp["boxes"], colors[:len(data)]):
        patch.set_facecolor(color)
        patch.set_alpha(0.45)

    # Overlay swarm-like scatter
    rng = np.random.default_rng(42)
    for i, arr in enumerate(data):
        if len(arr) <= 5000:
            jitter = rng.uniform(-0.12, 0.12, size=len(arr))
            ax.scatter(arr, np.full_like(arr, i + 1) + jitter,
                       alpha=0.08, s=5, color=colors[i], edgecolors="none")

    ax.set_yticks([1, 2])
    ax.set_yticklabels(["Ayak schedule", "Shadow schedule"],
                        fontsize=12, fontweight="bold")
    ax.set_xlabel("Time to Kill (seconds)", fontsize=11)
    ax.set_title(
        f"NyloBoss TTK Comparison  —  {num_players}p vs {boss_scale}-scale  |  "
        f"{result.stats_a.iterations:,} iterations each",
        fontsize=12,
    )
    ax.set_ylim(0.3, 2.7)

    # Rotations summary as footer text
    ayak_label = f"Ayak:  {result.stats_a.median_ttk * 0.6:.1f}s median  |  3× Ayak → 3× BP → TBow after mage"
    shadow_label = f"Shadow:  {result.stats_b.median_ttk * 0.6:.1f}s median  |  2× Shadow → regular TBow after mage"
    ax.text(0.5, -0.18, f"{ayak_label}         {shadow_label}",
            transform=ax.transAxes, ha="center", fontsize=9,
            color="gray", style="italic")

    # Annotate medians
    for i, (arr, stats, color) in enumerate(zip(
        data,
        [result.stats_a, result.stats_b],
        colors[:len(data)],
    ), start=1):
        median_s = stats.median_ttk * 0.6
        mean_s = stats.mean_ttk * 0.6
        ax.annotate(
            f"median={median_s:.1f}s\nmean={mean_s:.1f}s",
            xy=(median_s, i + 0.30),
            fontsize=9, color=color, fontweight="bold",
            ha="center", va="bottom",
        )

    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"\n  Comparison box plot saved → {out_path}")



def plot_comparison_histogram(
    result: ComparisonResult,
    out_path: str = "nyloboss_ttk_histogram_comparison.png",
    num_players: int = 3,
    boss_scale: int = DEFAULT_BOSS_SCALE,
    bins: int = 50,
) -> None:
    """Save an overlaid histogram comparing two TTK distributions."""
    arr_a = np.array(result.stats_a.ticks, dtype=np.float64) * 0.6
    arr_b = np.array(result.stats_b.ticks, dtype=np.float64) * 0.6

    if len(arr_a) == 0 and len(arr_b) == 0:
        print("No kills to plot.")
        return

    fig, ax = plt.subplots(figsize=(12, 6))

    label_a_short = f"Schedule A — median={result.stats_a.median_ttk * 0.6:.1f}s"
    label_b_short = f"Schedule B — median={result.stats_b.median_ttk * 0.6:.1f}s"

    ax.hist(arr_a, bins=bins, color="#4C72B0", edgecolor="white",
            alpha=0.6, label=label_a_short)
    ax.hist(arr_b, bins=bins, color="#E24A33", edgecolor="white",
            alpha=0.6, label=label_b_short)

    # Median lines
    if len(arr_a) > 0:
        ax.axvline(result.stats_a.median_ttk * 0.6, color="#4C72B0",
                   linestyle="--", linewidth=2.5)
    if len(arr_b) > 0:
        ax.axvline(result.stats_b.median_ttk * 0.6, color="#E24A33",
                   linestyle="-", linewidth=2.5)

    ax.set_xlabel("Time to Kill (seconds)", fontsize=11)
    ax.set_ylabel("Frequency", fontsize=11)
    ax.set_title(
        f"NyloBoss TTK Distribution Comparison ({num_players}p vs {boss_scale}-scale)\n"
        f"{result.stats_a.kills:,} kills / {result.stats_b.kills:,} kills  |  "
        f"{result.stats_a.iterations:,} iterations each",
        fontsize=12,
    )
    ax.legend(fontsize=10)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"  Comparison histogram saved → {out_path}")




# ── Runners ─────────────────────────────────────────────────────────────────

def _batch_ticks(
    iterations: int,
    num_threads: int,
    boss_scale: int,
    player_configs: List[PlayerConfig],
    label: str,
) -> Tuple[List[int], float]:
    """Run a batch and return (ticks, elapsed_s)."""
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
                print(f"    [{label}] {i:>3}/{len(batch_sizes)} batches  "
                      f"({total_kills:,} kills so far)")

    return all_ticks, time.time() - t0


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

    all_ticks, elapsed = _batch_ticks(
        iterations, num_threads, boss_scale, player_configs, "Analytics",
    )

    stats = compute_stats(all_ticks, elapsed)
    print_stats(stats)

    # Plots
    os.makedirs(output_dir, exist_ok=True)
    plot_histogram(stats, os.path.join(output_dir, "nyloboss_ttk_histogram.png"), bins=bins)
    plot_boxplot(stats, os.path.join(output_dir, "nyloboss_ttk_boxplot.png"),
                 num_players=len(player_configs), boss_scale=boss_scale)

    return stats


# ── Comparison runner ───────────────────────────────────────────────────────

def _make_shadow_configs() -> List[PlayerConfig]:
    """Build default 3-player configs using the Shadow attack schedule."""
    return [
        PlayerConfig(name="P1", attack_schedule=NyloBossShadowAttackSchedule(role=NyloRole.BGS)),
        PlayerConfig(name="P2", attack_schedule=NyloBossShadowAttackSchedule(role=NyloRole.BACKUP_BGS)),
        PlayerConfig(name="P3", attack_schedule=NyloBossShadowAttackSchedule(role=NyloRole.CLAWS)),
    ]


def run_comparison(
    iterations: int = 10000,
    num_threads: int = 8,
    boss_scale: int = DEFAULT_BOSS_SCALE,
    player_configs_a: List[PlayerConfig] | None = None,
    player_configs_b: List[PlayerConfig] | None = None,
    output_dir: str = ".",
) -> ComparisonResult:
    """Run both attack schedules side-by-side and compare TTK distributions.

    Args:
        iterations: number of runs per schedule.
        num_threads: parallel workers.
        boss_scale: NyloBoss scale.
        player_configs_a: configs for schedule A (default: Ayak).
        player_configs_b: configs for schedule B (default: Shadow).
        output_dir: directory for comparison PNG.

    Returns:
        ComparisonResult with stats for both schedules.
    """
    if player_configs_a is None:
        player_configs_a = DEFAULT_PLAYER_CONFIGS
    if player_configs_b is None:
        player_configs_b = _make_shadow_configs()

    label_a = "Ayak (3× Ayak → 3× BP → TBow)"
    label_b = "Shadow (2× Shadow → TBow→TBow)"

    print()
    print("=" * 60)
    print("  NyloBoss TTK Comparison")
    print("=" * 60)
    print(f"  {iterations:,} iterations per schedule  |  {num_threads} threads")
    print()

    print(f"  ── Running: {label_a}")
    ticks_a, elapsed_a = _batch_ticks(
        iterations, num_threads, boss_scale, player_configs_a, "A",
    )
    stats_a = compute_stats(ticks_a, elapsed_a)
    print_stats(stats_a, label=f"Ayak Schedule")

    print(f"\n  ── Running: {label_b}")
    ticks_b, elapsed_b = _batch_ticks(
        iterations, num_threads, boss_scale, player_configs_b, "B",
    )
    stats_b = compute_stats(ticks_b, elapsed_b)
    print_stats(stats_b, label=f"Shadow Schedule")

    result = ComparisonResult(
        label_a=label_a,
        stats_a=stats_a,
        label_b=label_b,
        stats_b=stats_b,
    )

    # Side-by-side box plot and overlaid histogram
    os.makedirs(output_dir, exist_ok=True)
    plot_comparison_boxplot(
        result,
        os.path.join(output_dir, "nyloboss_ttk_comparison.png"),
        num_players=len(player_configs_a),
        boss_scale=boss_scale,
    )
    plot_comparison_histogram(
        result,
        os.path.join(output_dir, "nyloboss_ttk_histogram_comparison.png"),
        num_players=len(player_configs_a),
        boss_scale=boss_scale,
    )

    return result


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
    parser.add_argument("--compare", action="store_true",
                        help="Run both Ayak and Shadow schedules and produce a comparison box plot")
    args = parser.parse_args()

    if args.compare:
        run_comparison(
            iterations=args.iterations,
            num_threads=args.threads,
            boss_scale=args.scale,
            output_dir=args.output,
        )
    else:
        run_analytics(
            iterations=args.iterations,
            num_threads=args.threads,
            boss_scale=args.scale,
            output_dir=args.output,
            bins=args.bins,
        )
