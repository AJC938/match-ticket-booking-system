"""Data models for users, matches, zones and booking requests."""

from dataclasses import dataclass, field
from enum import IntEnum
from typing import List


class PriorityTier(IntEnum):
    VIP = 1
    HIGH_ATTENDANCE = 2
    GENERAL = 3

    @property
    def label(self) -> str:
        return {1: "VIP Members", 2: "High Attendance (70%+)", 3: "General / Away Fans"}[self]

    @property
    def short_label(self) -> str:
        return {1: "VIP", 2: "HIGH", 3: "GEN"}[self]


@dataclass
class User:
    user_id: str
    name: str
    is_vip: bool = False
    attendance: float = 0.0
    tickets: List[str] = field(default_factory=list)

    @property
    def tier(self) -> PriorityTier:
        if self.is_vip:
            return PriorityTier.VIP
        if self.attendance >= 70:
            return PriorityTier.HIGH_ATTENDANCE
        return PriorityTier.GENERAL

    def can_book_more(self, max_tickets: int = 2) -> bool:
        return len(self.tickets) < max_tickets


@dataclass
class Match:
    match_id: str
    home: str
    away: str
    competition: str
    date_str: str
    kickoff: str
    venue: str
    base_price: int

    @property
    def title(self) -> str:
        return f"{self.home} vs {self.away}"


@dataclass
class Zone:
    zone_id: str
    name: str
    tier: PriorityTier
    color: str
    rows: int
    cols: int
    price_multiplier: float = 1.0

    def seat_count(self) -> int:
        return self.rows * self.cols


@dataclass(order=True)
class BookingRequest:
    sort_key: tuple = field(init=False, repr=False)
    tier: int
    timestamp: float
    user_id: str
    match_id: str
    seat_codes: List[str]

    def __post_init__(self) -> None:
        self.sort_key = (self.tier, self.timestamp)
