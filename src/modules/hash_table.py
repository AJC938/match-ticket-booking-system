"""Custom hash table with separate chaining and dynamic resizing.

Average complexity: O(1) insert/search/delete; O(n) worst case.
"""

from typing import Any, Iterator, List, Optional, Tuple


class HashTable:
    _INITIAL_CAPACITY = 16
    _LOAD_FACTOR_THRESHOLD = 0.75

    def __init__(self) -> None:
        self._capacity = self._INITIAL_CAPACITY
        self._size = 0
        self._buckets: List[List[Tuple[str, Any]]] = [[] for _ in range(self._capacity)]

    def _hash(self, key: str) -> int:
        h = 0
        for ch in key:
            h = (h * 31 + ord(ch)) & 0xFFFFFFFF
        return h % self._capacity

    def _resize(self) -> None:
        old_buckets = self._buckets
        self._capacity *= 2
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0
        for bucket in old_buckets:
            for key, value in bucket:
                self.insert(key, value)

    def insert(self, key: str, value: Any) -> None:
        bucket = self._buckets[self._hash(key)]
        for i, (stored_key, _) in enumerate(bucket):
            if stored_key == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self._size += 1
        if self._size / self._capacity > self._LOAD_FACTOR_THRESHOLD:
            self._resize()

    def search(self, key: str) -> Optional[Any]:
        for stored_key, value in self._buckets[self._hash(key)]:
            if stored_key == key:
                return value
        return None

    def delete(self, key: str) -> bool:
        bucket = self._buckets[self._hash(key)]
        for i, (stored_key, _) in enumerate(bucket):
            if stored_key == key:
                bucket.pop(i)
                self._size -= 1
                return True
        return False

    def __contains__(self, key: str) -> bool:
        return self.search(key) is not None

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[Any]:
        for bucket in self._buckets:
            for _, value in bucket:
                yield value

    def load_factor(self) -> float:
        return self._size / self._capacity

    def collision_count(self) -> int:
        return sum(max(0, len(bucket) - 1) for bucket in self._buckets)

    def stats(self) -> dict:
        return {
            "capacity": self._capacity,
            "size": self._size,
            "load_factor": round(self.load_factor(), 3),
            "collisions": self.collision_count(),
        }
