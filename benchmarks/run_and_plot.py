"""Run benchmarks multiple times and produce clearer runtime plots.

This script runs multiple repetitions per (distribution, size) to compute
mean runtime and standard deviation, then plots means with error bars. The
plot uses lines with markers which are often easier to interpret than bars
for time-vs-size comparisons.

Output:
    - `benchmarks/plots.png` (high-resolution PNG)
    - `benchmarks/bench_results.csv` (CSV with mean/std per configuration)
"""
import os
import sys
import time
import random
from statistics import mean, stdev
from typing import Dict


HERE = os.path.dirname(__file__)
SRC_DIR = os.path.abspath(os.path.join(HERE, "..", "src"))
sys.path.insert(0, SRC_DIR)

from heapsort import heapsort


def quicksort(arr):
    """Simple recursive quicksort used for benchmarking.

    Note: This is not an in-place, highly-optimized quicksort. It is
    intentionally simple to provide a baseline for comparison.
    """
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)


def mergesort(arr):
    """Classic merge sort implementation (returns new list)."""
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = mergesort(arr[:mid])
    right = mergesort(arr[mid:])
    i = j = 0
    merged = []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
    merged.extend(left[i:]); merged.extend(right[j:])
    return merged


def time_fn(fn, arr):
    """Time a function `fn` called with a copy of `arr` and return elapsed sec.

    `fn` is expected to accept a list and return a sorted list or mutate it.
    We pass a shallow copy to avoid side-effects across runs.
    """
    t0 = time.perf_counter()
    fn(list(arr))
    return time.perf_counter() - t0


def run_and_plot(out_path: str = None, repetitions: int = 5) -> None:
    """Run benchmarks and save plot and CSV results.

    Args:
        out_path: path for saved PNG plot. If None, uses `benchmarks/plots.png`.
        repetitions: number of repetitions per configuration to compute mean/std.
    """
    import csv
    import matplotlib.pyplot as plt

    sizes = [1000, 5000, 10000, 20000]
    distributions = ["random", "sorted", "reversed"]
    algs = ["heapsort", "quicksort", "mergesort", "timsort"]

    # store all runtimes per config
    results: Dict[str, Dict[int, Dict[str, list]]] = {d: {n: {a: [] for a in algs} for n in sizes} for d in distributions}

    for dist in distributions:
        for n in sizes:
            for _ in range(repetitions):
                if dist == "random":
                    a = [random.randint(0, n) for _ in range(n)]
                elif dist == "sorted":
                    a = list(range(n))
                else:
                    a = list(range(n, 0, -1))

                results[dist][n]["heapsort"].append(time_fn(heapsort, a))
                results[dist][n]["quicksort"].append(time_fn(quicksort, a))
                results[dist][n]["mergesort"].append(time_fn(mergesort, a))
                results[dist][n]["timsort"].append(time_fn(sorted, a))

    # compute mean and stddev
    stats = {d: {n: {a: (mean(results[d][n][a]), (stdev(results[d][n][a]) if len(results[d][n][a]) > 1 else 0.0)) for a in algs} for n in sizes} for d in distributions}

    # Save CSV for inspection
    csv_path = os.path.join(HERE, "bench_results.csv")
    with open(csv_path, "w", newline="") as cf:
        writer = csv.writer(cf)
        writer.writerow(["distribution", "n", "algorithm", "mean_s", "std_s"])
        for d in distributions:
            for n in sizes:
                for a in algs:
                    m, s = stats[d][n][a]
                    writer.writerow([d, n, a, f"{m:.6f}", f"{s:.6f}"])

    # Plotting: one subplot per distribution using line plots with error bars
    fig, axes = plt.subplots(1, len(distributions), figsize=(6 * len(distributions), 4))
    if len(distributions) == 1:
        axes = [axes]

    colors = {"heapsort": "C0", "quicksort": "C1", "mergesort": "C2", "timsort": "C3"}
    markers = {"heapsort": "o", "quicksort": "s", "mergesort": "^", "timsort": "D"}

    for ax, dist in zip(axes, distributions):
        x = list(sizes)
        for alg in algs:
            y = [stats[dist][n][alg][0] for n in x]
            yerr = [stats[dist][n][alg][1] for n in x]
            ax.errorbar(x, y, yerr=yerr, label=alg, marker=markers[alg], color=colors[alg], capsize=3)
        ax.set_title(f"Distribution: {dist}")
        ax.set_xlabel("n (array size)")
        ax.set_xticks(x)
        ax.set_ylabel("time (s)")
        ax.set_yscale("log")
        ax.grid(True, which="both", ls="--", lw=0.4)
        ax.legend()

    fig.tight_layout()
    if out_path is None:
        out_path = os.path.join(HERE, "plots.png")
    fig.savefig(out_path, dpi=200)
    print(f"Saved plot to: {out_path}")
    print(f"Saved CSV results to: {csv_path}")


if __name__ == "__main__":
    run_and_plot()
