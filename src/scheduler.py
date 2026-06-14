"""Simple scheduler simulation using `BinaryMaxHeap` priority queue.

This module provides a minimal simulation that enqueues tasks (possibly with
arrival times) and always schedules the highest-priority task next. It is
intended to demonstrate the `BinaryMaxHeap` usage in a scheduling context
and to collect simple statistics like average wait time.
"""
import random
from typing import List, Dict

from priority_queue import BinaryMaxHeap, Task


def simulate(tasks: List[Task], processing_time: float = 0.0) -> Dict[str, float]:
    """Simulate processing tasks by priority and collect statistics.

    The simulation proceeds in simulated time. Tasks that have `arrival_time`
    set will be enqueued when the clock reaches their arrival. When the
    priority queue is empty, the clock fast-forwards to the next arrival.

    Args:
        tasks: list of `Task` objects (each may have `arrival_time`)
        processing_time: simulated processing time per task (seconds)

    Returns:
        Dictionary with keys:
            - `num_tasks`: total tasks processed
            - `avg_wait`: average waiting time (clock - arrival_time)

    Complexity:
        The simulation runs in O(n log n) dominated by heap insert/extract
        operations for n tasks.
    """
    pq = BinaryMaxHeap()
    clock = 0.0
    completed = []

    # sort tasks by arrival_time for deterministic arrival handling
    tasks_sorted = sorted(tasks, key=lambda t: (t.arrival_time if t.arrival_time is not None else 0.0))
    i = 0
    n = len(tasks_sorted)

    while i < n or not pq.is_empty():
        # enqueue arrived tasks
        while i < n and (tasks_sorted[i].arrival_time is None or tasks_sorted[i].arrival_time <= clock):
            pq.insert(tasks_sorted[i])
            i += 1

        if pq.is_empty():
            # fast-forward to next arrival if any
            if i < n and tasks_sorted[i].arrival_time is not None:
                clock = tasks_sorted[i].arrival_time
            continue

        # get highest-priority task and record its waiting time
        task = pq.extract_max()
        wait_time = clock - (task.arrival_time if task.arrival_time is not None else 0.0)
        completed.append((task, wait_time))

        # advance simulated clock by processing time
        clock += processing_time

    avg_wait = sum(w for _, w in completed) / len(completed) if completed else 0.0
    return {"num_tasks": len(completed), "avg_wait": avg_wait}


def demo_random(n: int = 100, processing_time: float = 0.0) -> None:
    """Create `n` random tasks and run the simulation, printing stats.

    Each task receives a random priority in [0,1) and a random arrival time
    in the interval [0,10).
    """
    tasks = []
    for k in range(n):
        tasks.append(Task(task_id=f"task{k}", priority=random.random(), arrival_time=random.uniform(0, 10)))
    stats = simulate(tasks, processing_time=processing_time)
    print("demo stats:", stats)


if __name__ == "__main__":
    demo_random(20)