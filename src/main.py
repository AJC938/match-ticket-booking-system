"""Command-line entry point for the Match Ticket Booking System."""

from modules import BookingSystem, PriorityTier


def main() -> None:
    system = BookingSystem()
    match = system.matches[0]
    user, _, lookup_ms = system.login("VIP001")

    system.start_session(match.match_id)
    vip_zone = system.zone_for_tier(PriorityTier.VIP)
    seat = system.grid(match.match_id, vip_zone.zone_id).seat_code(0, 0)
    queued, message = system.submit_booking(user, match.match_id, [seat])
    processed, result, seats = system.process_next(match.match_id)
    benchmark = system.benchmark_extended(runs=5)

    print("=" * 64)
    print("MATCH TICKET BOOKING SYSTEM")
    print("Data Structures & Algorithms Demonstration")
    print("=" * 64)
    print(f"Match:          {match.title}")
    print(f"Fan:            {user.user_id} ({user.tier.label})")
    print(f"Lookup:         {lookup_ms:.4f} ms")
    print(f"Queue:          {'accepted' if queued else 'rejected'} — {message}")
    print(f"Booking:        {'success' if processed else 'failed'} — {result}")
    print(f"Seats assigned: {', '.join(seats) if seats else 'none'}")
    print("-" * 64)
    print(f"Search speedup: {benchmark['search_speedup']:.2f}x (Linear vs Hash)")
    print(f"Binary speedup: {benchmark['binary_speedup']:.2f}x (Linear vs Binary)")
    print(f"Sort speedup:   {benchmark['sort_speedup']:.2f}x (Bubble vs Merge)")
    print("=" * 64)


if __name__ == "__main__":
    main()
