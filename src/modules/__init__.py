"""Python package for the Match Ticket Booking System."""

from .models import User, Match, Zone, BookingRequest, PriorityTier
from .hash_table import HashTable
from .priority_queue import PriorityQueue
from .seat_grid import SeatGrid
from .mock_database import generate_mock_users
from .match_catalogue import default_matches
from .booking_system import BookingSystem, KPIRegistry, MatchSimState, default_zones
from .sorting import merge_sort, bubble_sort, sort_users_by_attendance
from .searching import linear_search, hash_search, binary_search

__all__ = [
    "User", "Match", "Zone", "BookingRequest", "PriorityTier",
    "HashTable", "PriorityQueue", "SeatGrid", "generate_mock_users",
    "default_matches", "BookingSystem", "KPIRegistry", "MatchSimState",
    "default_zones", "merge_sort", "bubble_sort", "sort_users_by_attendance",
    "linear_search", "hash_search", "binary_search",
]
