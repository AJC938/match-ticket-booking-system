"""Manual Binary Min-Heap priority queue."""

from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


class PriorityQueue(Generic[T]):
    """Min-heap with O(log n) push/pop and O(1) peek."""

    def __init__(self) -> None:
        self._heap: List[Optional[T]] = [None]

    def _swap(self, i: int, j: int) -> None:
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    def _sift_up(self, i: int) -> None:
        while i > 1 and self._heap[i] < self._heap[i // 2]:
            self._swap(i, i // 2)
            i //= 2

    def _sift_down(self, i: int) -> None:
        n = len(self._heap) - 1
        while True:
            left, right = 2 * i, 2 * i + 1
            smallest = i
            if left <= n and self._heap[left] < self._heap[smallest]:
                smallest = left
            if right <= n and self._heap[right] < self._heap[smallest]:
                smallest = right
            if smallest == i:
                break
            self._swap(i, smallest)
            i = smallest

    def push(self, item: T) -> None:
        self._heap.append(item)
        self._sift_up(len(self._heap) - 1)

    def pop(self) -> Optional[T]:
        if len(self._heap) <= 1:
            return None
        top = self._heap[1]
        last = self._heap.pop()
        if len(self._heap) > 1:
            self._heap[1] = last
            self._sift_down(1)
        return top

    def peek(self) -> Optional[T]:
        return self._heap[1] if len(self._heap) > 1 else None

    def is_empty(self) -> bool:
        return len(self._heap) <= 1

    def __len__(self) -> int:
        return len(self._heap) - 1

    def snapshot(self) -> List[T]:
        return list(self._heap[1:])
