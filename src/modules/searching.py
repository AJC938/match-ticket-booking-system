"""Linear, binary and hash-based search implementations."""

from typing import List, Optional


def linear_search(users: List, user_id: str) -> Optional[object]:
    for user in users:
        if user.user_id == user_id:
            return user
    return None


def hash_search(table, user_id: str) -> Optional[object]:
    return table.search(user_id)


def binary_search(sorted_users: List, user_id: str) -> Optional[object]:
    lo, hi = 0, len(sorted_users) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if sorted_users[mid].user_id == user_id:
            return sorted_users[mid]
        if sorted_users[mid].user_id < user_id:
            lo = mid + 1
        else:
            hi = mid - 1
    return None
