"""Hard-coded fixtures used by the booking system."""

from typing import List
from .models import Match


def default_matches() -> List[Match]:
    return [
        Match(
            match_id="UCL-FC-BAR-BAY",
            home="FC Barcelona",
            away="Bayern Munich",
            competition="UEFA Champions League - Quarter Final",
            date_str="May 15, 2026",
            kickoff="22:00 (Local)",
            venue="Spotify Camp Nou, Barcelona",
            base_price=350,
        ),
        Match(
            match_id="SPL-AHL-NSR",
            home="Al-Ahli FC",
            away="Al-Nassr FC",
            competition="Saudi Pro League - Matchday 30",
            date_str="May 17, 2026",
            kickoff="20:00 (Local)",
            venue="King Abdullah Sports City, Jeddah",
            base_price=150,
        ),
    ]
