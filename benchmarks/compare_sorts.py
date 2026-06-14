"""Benchmark Heapsort vs Quicksort, Merge Sort, and Python's Timsort.

This script provides small, easy-to-understand implementations of three
sorting algorithms (quicksort, mergesort, and the provided heapsort) and
compares their wall-clock runtimes on a few input distributions.

Notes on usage and benchmarking hygiene:
- These Python implementations are intentionally simple and educational;
  they are not micro-optimized and therefore are meant for relative
  performance comparison and demonstration rather than absolute speed.
- Timings use `time.perf_counter()` which is suitable for short wall-clock
  measurements.
"""

import random
import time
from typing import List

import sys

# Ensure the local `src` directory is available for imports when running
# this script from the `benchmarks` directory.
sys.path.append("../src")

from heapsort import heapsort


def quicksort(arr: List[int]) -> List[int]:
    """A simple, functional-style quicksort.

    This implementation selects the middle element as pivot and builds
    three lists (`left`, `middle`, `right`) then recursively sorts `left`
    and `right`. It returns a new list and therefore uses O(n) additional
    space in the recursion. It is fine for small-to-medium benchmark runs
    and is easy to reason about for educational comparisons.

    Args:
        arr: list of integers to sort

    Returns:
        A new sorted list containing the elements of `arr`.
    """
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)


def mergesort(arr: List[int]) -> List[int]:
    """Classic merge sort that returns a new sorted list.

    The function recursively splits the array and merges the sorted halves.
    This implementation is stable and has guaranteed O(n log n) time but
    uses O(n) extra space for merging.

    Args:
        arr: list of integers to sort

    Returns:
        A new sorted list containing the elements of `arr`.
    """
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = mergesort(arr[:mid])
    right = mergesort(arr[mid:])
    i = j = 0
    merged = []
    # Merge two sorted lists
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    # Append remaining tail elements
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def time_fn(fn, arr: List[int]) -> float:
    """Measure the wall-clock time to run `fn` on a copy of `arr`.

    This helper makes a shallow copy of the input list so repeated timings
    do not interfere with each other via in-place mutations.

    Args:
        fn: callable that accepts a list (may return a list or mutate it)
        arr: input list to be copied and passed to `fn`

    Returns:
        Elapsed time in seconds as a float.
    """
    t0 = time.perf_counter()
    fn(list(arr))
    return time.perf_counter() - t0


def run_bench() -> None:
    """Run a small benchmark across multiple sizes and input distributions.

    The function prints timings to stdout. It is intentionally simple so
    that results are easy to reproduce and inspect.
    """
    sizes = [1000, 5000, 10000]
    distributions = ["random", "sorted", "reversed"]
    for dist in distributions:
        print(f"\nDistribution: {dist}")
        for n in sizes:
            # Prepare input array according to distribution
            if dist == "random":
                a = [random.randint(0, n) for _ in range(n)]
            elif dist == "sorted":
                a = list(range(n))
            else:
                a = list(range(n, 0, -1))

            # make copies for each algorithm to ensure fairness
            a1 = list(a)
            a2 = list(a)
            a3 = list(a)
            a4 = list(a)

            # Time each algorithm on its own copy
            t_heap = time_fn(heapsort, a1)
            t_quick = time_fn(quicksort, a2)
            t_merge = time_fn(mergesort, a3)
            t_timsort = time_fn(sorted, a4)

            print(
                f"n={n}: heapsort={t_heap:.4f}s quicksort={t_quick:.4f}s "
                f"merge={t_merge:.4f}s timsort={t_timsort:.4f}s"
            )


if __name__ == "__main__":
    run_bench()