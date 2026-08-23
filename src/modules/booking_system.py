"""Core booking engine composing the project's data structures.

Optimized mode uses a custom hash table and binary min-heap. Standard mode
uses linear lookup and a list-based priority scan as a baseline.
"""

from __future__ import annotations
import random
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from .hash_table import HashTable
from .match_catalogue import default_matches
from .mock_database import generate_mock_users
from .models import BookingRequest, Match, PriorityTier, User, Zone
from .priority_queue import PriorityQueue
from .searching import binary_search, hash_search, linear_search
from .seat_grid import SeatGrid
from .sorting import bubble_sort, merge_sort
from .user_store import load_registered_users, save_new_user

TIER_WINDOW_SECONDS = 120
MAX_TICKETS_PER_USER_PER_MATCH = 2


def default_zones() -> List[Zone]:
    return [
        Zone("VIP", "VIP Box", PriorityTier.VIP, "#e8b14a", 4, 12, 4.0),
        Zone("HIGH", "Premium Stand", PriorityTier.HIGH_ATTENDANCE, "#3aa6e0", 8, 18, 2.0),
        Zone("GEN", "General Admission", PriorityTier.GENERAL, "#8a8a8a", 10, 20, 1.0),
    ]


@dataclass
class KPIRegistry:
    bookings_processed: int = 0
    bookings_rejected: int = 0
    total_processing_ms: float = 0.0
    total_lookup_ms: float = 0.0
    lookup_count: int = 0
    total_wait_seconds: float = 0.0
    fans_who_waited: int = 0
    total_revenue: float = 0.0
    tier_counts: Dict[int, int] = field(default_factory=lambda: {1: 0, 2: 0, 3: 0})

    @property
    def avg_processing_ms(self) -> float:
        return self.total_processing_ms / self.bookings_processed if self.bookings_processed else 0.0

    @property
    def avg_lookup_ms(self) -> float:
        return self.total_lookup_ms / self.lookup_count if self.lookup_count else 0.0

    @property
    def throughput_per_sec(self) -> float:
        return self.bookings_processed / (self.total_processing_ms / 1000) if self.total_processing_ms else 0.0

    @property
    def avg_wait_seconds(self) -> float:
        return self.total_wait_seconds / self.fans_who_waited if self.fans_who_waited else 0.0


@dataclass
class MatchSimState:
    match_id: str
    is_running: bool = False
    current_tier: Optional[PriorityTier] = None
    queue: PriorityQueue = field(default_factory=PriorityQueue)
    queue_list: List[BookingRequest] = field(default_factory=list)
    arrival_times: Dict[str, float] = field(default_factory=dict)
    kpis: KPIRegistry = field(default_factory=KPIRegistry)


class BookingSystem:
    """Application service coordinating users, queues, seats and benchmarks."""

    def __init__(self) -> None:
        self.users = HashTable()
        for user in generate_mock_users(100):
            self.users.insert(user.user_id, user)
        for user in load_registered_users():
            if self.users.search(user.user_id) is None:
                self.users.insert(user.user_id, user)
        self.matches: List[Match] = default_matches()
        self.zones: List[Zone] = default_zones()
        self.seat_grids = {
            match.match_id: {zone.zone_id: SeatGrid(zone.zone_id, zone.rows, zone.cols) for zone in self.zones}
            for match in self.matches
        }
        self.match_states: Dict[str, MatchSimState] = {}
        self.mode = "optimized"

    def state(self, match_id: str) -> MatchSimState:
        if match_id not in self.match_states:
            self.match_states[match_id] = MatchSimState(match_id)
        return self.match_states[match_id]

    def get_match(self, match_id: str) -> Optional[Match]:
        return next((m for m in self.matches if m.match_id == match_id), None)

    def get_zone(self, zone_id: str) -> Optional[Zone]:
        return next((z for z in self.zones if z.zone_id == zone_id), None)

    def zone_for_tier(self, tier: PriorityTier) -> Zone:
        return next(z for z in self.zones if z.tier == tier)

    def grid(self, match_id: str, zone_id: str) -> SeatGrid:
        return self.seat_grids[match_id][zone_id]

    def login(self, fan_id: str) -> Tuple[User, bool, float]:
        fan_id = fan_id.strip().upper()
        start = time.perf_counter()
        user = linear_search(list(self.users), fan_id) if self.mode == "standard" else hash_search(self.users, fan_id)
        elapsed = (time.perf_counter() - start) * 1000
        if user is not None:
            return user, False, elapsed
        user = User(fan_id, f"Guest {fan_id}")
        self.users.insert(fan_id, user)
        save_new_user(user)
        return user, True, elapsed

    def start_session(self, match_id: str) -> None:
        state = self.state(match_id)
        state.is_running = True
        state.current_tier = PriorityTier.VIP

    def open_all_tiers(self, match_id: str) -> None:
        state = self.state(match_id)
        state.is_running = True
        state.current_tier = PriorityTier.GENERAL

    def tier_is_open(self, tier: PriorityTier, match_id: str) -> bool:
        state = self.state(match_id)
        return state.is_running and state.current_tier is not None and int(tier) <= int(state.current_tier)

    def submit_booking(self, user: User, match_id: str, seat_codes: List[str]) -> Tuple[bool, str]:
        state = self.state(match_id)
        if not state.is_running:
            state.kpis.bookings_rejected += 1
            return False, "Booking session is not running."
        if not 1 <= len(seat_codes) <= MAX_TICKETS_PER_USER_PER_MATCH:
            return False, f"Select 1–{MAX_TICKETS_PER_USER_PER_MATCH} seats."
        if len(self.user_seats_for_match(user.user_id, match_id)) + len(seat_codes) > MAX_TICKETS_PER_USER_PER_MATCH:
            state.kpis.bookings_rejected += 1
            return False, "Ticket limit exceeded."
        for code in seat_codes:
            zone_id, row, col = SeatGrid.parse_code(code)
            grid = self.seat_grids[match_id].get(zone_id)
            if grid is None or not grid.is_free(row, col):
                state.kpis.bookings_rejected += 1
                return False, f"Seat {code} is unavailable."
        request = BookingRequest(int(user.tier), time.time(), user.user_id, match_id, list(seat_codes))
        if self.mode == "standard":
            state.queue_list.append(request)
        else:
            state.queue.push(request)
        state.arrival_times[user.user_id] = request.timestamp
        return True, "Booking request queued."

    def process_next(self, match_id: str) -> Tuple[bool, str, List[str]]:
        state = self.state(match_id)
        if not state.is_running or state.current_tier is None:
            return False, "No booking window is open.", []
        start = time.perf_counter()
        if self.mode == "standard":
            candidates = [r for r in state.queue_list if r.tier <= int(state.current_tier)]
            if not candidates:
                return False, "No ready request.", []
            request = min(candidates, key=lambda r: (r.tier, r.timestamp))
            state.queue_list.remove(request)
            user = linear_search(list(self.users), request.user_id)
        else:
            head = state.queue.peek()
            if head is None or head.tier > int(state.current_tier):
                return False, "No ready request.", []
            request = state.queue.pop()
            user = self.users.search(request.user_id)
        if user is None or request is None:
            return False, "User not found.", []
        assigned: List[str] = []
        for code in request.seat_codes:
            zone_id, row, col = SeatGrid.parse_code(code)
            if self.seat_grids[match_id][zone_id].assign(row, col, user.user_id):
                assigned.append(code)
                user.tickets.append(code)
        elapsed = (time.perf_counter() - start) * 1000
        state.kpis.total_processing_ms += elapsed
        state.kpis.tier_counts[request.tier] += len(assigned)
        if assigned:
            state.kpis.bookings_processed += 1
            match = self.get_match(match_id)
            for code in assigned:
                zone_id, _, _ = SeatGrid.parse_code(code)
                zone = self.get_zone(zone_id)
                if match and zone:
                    state.kpis.total_revenue += match.base_price * zone.price_multiplier
        wait = max(0.0, time.time() - state.arrival_times.pop(user.user_id, request.timestamp))
        state.kpis.total_wait_seconds += wait
        state.kpis.fans_who_waited += 1
        return bool(assigned), "Booking processed." if assigned else "No seats assigned.", assigned

    def user_seats_for_match(self, user_id: str, match_id: str) -> List[str]:
        seats: List[str] = []
        for grid in self.seat_grids[match_id].values():
            seats.extend(grid.seats_for_user(user_id))
        return seats

    def benchmark_extended(self, search_n: int = 2000, sort_n: int = 200, runs: int = 10) -> dict:
        users = list(self.users)
        while len(users) < search_n:
            i = len(users)
            users.append(User(f"BENCH{i:05d}", f"Bench {i}", attendance=random.uniform(0, 100)))
        target = users[-1].user_id
        table = HashTable()
        for user in users:
            table.insert(user.user_id, user)
        sorted_users = sorted(users, key=lambda u: u.user_id)
        linear, binary, hashed, merge, bubble = [], [], [], [], []
        sort_users = users[:sort_n]
        for _ in range(runs):
            start = time.perf_counter(); linear_search(users, target); linear.append((time.perf_counter()-start)*1000)
            start = time.perf_counter(); binary_search(sorted_users, target); binary.append((time.perf_counter()-start)*1000)
            start = time.perf_counter(); hash_search(table, target); hashed.append((time.perf_counter()-start)*1000)
            start = time.perf_counter(); merge_sort(sort_users, key=lambda u: u.attendance); merge.append((time.perf_counter()-start)*1000)
            start = time.perf_counter(); bubble_sort(sort_users, key=lambda u: u.attendance); bubble.append((time.perf_counter()-start)*1000)
        avg = lambda values: sum(values) / len(values)
        return {
            "n_search": len(users), "n_sort": len(sort_users), "runs": runs,
            "linear_ms": avg(linear), "binary_ms": avg(binary), "hash_ms": avg(hashed),
            "merge_ms": avg(merge), "bubble_ms": avg(bubble),
            "binary_speedup": avg(linear) / avg(binary) if avg(binary) else 0,
            "search_speedup": avg(linear) / avg(hashed) if avg(hashed) else 0,
            "sort_speedup": avg(bubble) / avg(merge) if avg(merge) else 0,
        }
