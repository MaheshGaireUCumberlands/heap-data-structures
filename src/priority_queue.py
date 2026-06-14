"""A binary max-heap priority queue implementation.

This module implements a simple binary max-heap backed by a Python list
and a `position` dictionary that maps `task_id` to the task's index.
The `position` map enables O(1) lookup of where a task sits in the heap,
which allows `increase_key` and `decrease_key` operations to run in O(log n)
by bubbling or heapifying from that index.

Design notes:
- We use a max-heap (higher numeric priority => served first). This is a
  natural choice for many scheduling policies; to implement a min-heap,
  invert the sign of priority or adjust comparisons.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class Task:
    """Representation of a scheduled task.

    Attributes:
        task_id: Unique identifier (hashable) used in `position` mapping.
        priority: Numeric priority value; larger means higher priority.
        arrival_time: Optional numeric arrival time for simulations.
        deadline: Optional numeric deadline.
        payload: Arbitrary attached data.
    """
    task_id: Any
    priority: float
    arrival_time: Optional[float] = None
    deadline: Optional[float] = None
    payload: Any = None


class BinaryMaxHeap:
    """Binary max-heap priority queue with indexed positions.

    Public methods:
        - insert(task): insert Task into heap (O(log n)).
        - extract_max(): remove and return highest-priority Task (O(log n)).
        - increase_key(task_id, new_priority): raise priority and bubble up.
        - decrease_key(task_id, new_priority): lower priority and heapify down.
        - peek(): return top Task without removing.
        - is_empty(): return True if empty.
    """

    def __init__(self) -> None:
        self.heap: List[Task] = []
        # position maps task_id -> index in self.heap for O(1) lookup
        self.position: Dict[Any, int] = {}

    def _swap(self, i: int, j: int) -> None:
        """Swap two indices in the heap and update `position` map."""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.position[self.heap[i].task_id] = i
        self.position[self.heap[j].task_id] = j

    def _bubble_up(self, idx: int) -> None:
        """Move element at `idx` upwards while its priority is greater than parent.

        This preserves the heap property after an insertion or increase-key.
        """
        while idx > 0:
            parent = (idx - 1) // 2
            if self.heap[idx].priority <= self.heap[parent].priority:
                break
            self._swap(idx, parent)
            idx = parent

    def _heapify_down(self, idx: int) -> None:
        """Move element at `idx` downwards to restore heap property.

        Used after extracting root or decreasing a key.
        """
        n = len(self.heap)
        while True:
            left = 2 * idx + 1
            right = 2 * idx + 2
            largest = idx
            if left < n and self.heap[left].priority > self.heap[largest].priority:
                largest = left
            if right < n and self.heap[right].priority > self.heap[largest].priority:
                largest = right
            if largest == idx:
                break
            self._swap(idx, largest)
            idx = largest

    def insert(self, task: Task) -> None:
        """Insert a new `Task` into the heap.

        Raises `KeyError` if `task.task_id` already exists.

        Complexity: O(log n) (bubble-up)
        """
        if task.task_id in self.position:
            raise KeyError("Task with this ID already exists")
        idx = len(self.heap)
        self.heap.append(task)
        self.position[task.task_id] = idx
        self._bubble_up(idx)

    def extract_max(self) -> Task:
        """Remove and return the highest-priority `Task`.

        Raises `IndexError` if heap is empty.

        Complexity: O(log n) (heapify-down)
        """
        if not self.heap:
            raise IndexError("extract_max from empty heap")
        top = self.heap[0]
        last = self.heap.pop()
        del self.position[top.task_id]
        if self.heap:
            # Move last element to root and restore heap
            self.heap[0] = last
            self.position[last.task_id] = 0
            self._heapify_down(0)
        return top

    def peek(self) -> Optional[Task]:
        """Return the top `Task` without removing it, or `None` if empty."""
        return self.heap[0] if self.heap else None

    def increase_key(self, task_id: Any, new_priority: float) -> None:
        """Increase the priority of task `task_id` to `new_priority`.

        Raises KeyError if `task_id` not present and ValueError if the new
        priority is smaller than the current.

        Complexity: O(log n) due to bubbling up.
        """
        if task_id not in self.position:
            raise KeyError("task_id not found")
        idx = self.position[task_id]
        if new_priority < self.heap[idx].priority:
            raise ValueError("new priority is smaller than current; use decrease_key")
        self.heap[idx].priority = new_priority
        self._bubble_up(idx)

    def decrease_key(self, task_id: Any, new_priority: float) -> None:
        """Decrease the priority of task `task_id` to `new_priority`.

        Raises KeyError if `task_id` not present and ValueError if the new
        priority is larger than the current.

        Complexity: O(log n) due to heapify-down.
        """
        if task_id not in self.position:
            raise KeyError("task_id not found")
        idx = self.position[task_id]
        if new_priority > self.heap[idx].priority:
            raise ValueError("new priority is larger than current; use increase_key")
        self.heap[idx].priority = new_priority
        self._heapify_down(idx)

    def is_empty(self) -> bool:
        """Return True if heap contains no tasks."""
        return not self.heap

    def __len__(self) -> int:
        """Return number of tasks in the heap."""
        return len(self.heap)


if __name__ == "__main__":
    # Quick demonstration
    pq = BinaryMaxHeap()
    pq.insert(Task("t1", priority=5))
    pq.insert(Task("t2", priority=2))
    pq.insert(Task("t3", priority=8))
    print("peek:", pq.peek())
    print("extract:", pq.extract_max())
    pq.increase_key("t2", 10)
    print("after increase, extract:", pq.extract_max())