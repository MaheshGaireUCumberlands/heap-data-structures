"""Heapsort implementation (max-heap) and helpers.

This module provides a clear, well-documented, in-place Heapsort
implementation using a 0-based array representation for the heap.

Core API:
- `heapify(arr, n, i)`: ensure the subtree rooted at `i` satisfies the
  max-heap property for the first `n` elements of `arr`.
- `build_max_heap(arr)`: transform `arr` into a max-heap in-place.
- `heapsort_inplace(arr)`: sort `arr` in ascending order in-place.
- `heapsort(arr)`: non-destructive wrapper that returns a sorted copy.

Complexities:
- Time: O(n log n) overall (O(n) to build heap + n * O(log n) extracts).
- Space: O(1) extra (in-place). The implementation uses recursion only in
  `heapify` when necessary; recursion depth is O(log n).

Examples:
    >>> from heapsort import heapsort
    >>> heapsort([3,1,2])
    [1, 2, 3]

Notes:
- This implementation treats larger values as higher priority (max-heap),
  yielding ascending sorted output after repeated extract-max operations.
"""

from typing import List, Any


def heapify(arr: List[Any], n: int, i: int) -> None:
    """Ensure the subtree rooted at index `i` (0-based) is a max-heap.

    This function assumes that the binary trees rooted at the children of
    `i` are already max-heaps. If the element at `i` is smaller than one of
    its children, it is swapped with the largest child and the function
    continues recursively at the child's index.

    Args:
        arr: list containing heap elements (any comparable type)
        n: number of valid heap elements in `arr` (consider arr[0:n])
        i: root index to enforce heap property

    Returns:
        None (operates in-place)

    Complexity:
        Worst-case O(log n) time (height of heap) and O(1) extra space
        (excluding recursion stack).
    """
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    # Find largest among root and children
    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right

    # If root is not largest, swap and continue heapifying
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def build_max_heap(arr: List[Any]) -> None:
    """Transform `arr` into a max-heap in-place using bottom-up method.

    The bottom-up method starts at the last non-leaf node (index `n//2-1`) and
    calls `heapify` for each node moving backwards to index 0. This builds the
    heap in O(n) time (tight analysis uses summation of heights).

    Args:
        arr: list to transform (modified in-place)

    Returns:
        None
    """
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)


def heapsort_inplace(arr: List[Any]) -> None:
    """Sort `arr` in ascending order in-place using Heapsort.

    Steps:
    1. Build a max-heap from the array (largest element at index 0).
    2. Repeatedly swap the root (max) with the last element of the heap,
       reduce the considered heap size by one, and `heapify` at root.

    Args:
        arr: list to be sorted (modified in-place)

    Returns:
        None

    Complexity:
        Time: O(n log n) in best/average/worst cases.
        Space: O(1) extra.
    """
    n = len(arr)
    build_max_heap(arr)
    # Extract elements from heap and place at end of array
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)


def heapsort(arr: List[Any]) -> List[Any]:
    """Return a new ascending-sorted list from `arr` without mutating it.

    This is a convenience wrapper that makes a shallow copy and sorts it
    in-place using `heapsort_inplace` so callers receive a fresh sorted list.

    Args:
        arr: input iterable (list-like)

    Returns:
        A new list containing the sorted elements.
    """
    copy = list(arr)
    heapsort_inplace(copy)
    return copy


if __name__ == "__main__":
    # Simple self-check
    data = [3, 1, 4, 1, 5, 9, 2, 6]
    print("original:", data)
    print("heapsort:", heapsort(data))