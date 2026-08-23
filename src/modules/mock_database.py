"""Deterministic mock dataset of 100 fans for benchmarking."""

import random
from typing import List
from .models import User

_FIRST = ["Aisha", "Omar", "Yusuf", "Layla", "Nora", "Tariq", "Hadi", "Mariam", "Khalid", "Sara", "Fahd", "Rana", "Ahmad", "Reem", "Saud", "Lina", "Bandar", "Hala", "Faisal", "Dana", "Nasser", "Maya", "Salman", "Joud", "Diego", "Hannah", "Lucas", "Sofia", "Marco", "Anna", "Carlos", "Emma", "Hiroshi", "Yuki", "Andre", "Mei", "Rashid", "Nadia", "Talal", "Zaid", "Hazem", "Amal", "Rayan", "Lujain", "Mohannad", "Abeer", "Sami", "Ghada", "Waleed", "Rahaf", "Bader", "Noura", "Sultan", "Mona", "Abdulaziz", "Dina", "Turki", "Ruba", "Mishal", "Wafa", "Nawaf", "Hind", "Hamad", "Leen", "Mansour", "Asma", "Khaled", "Basma", "Ibrahim", "Arwa", "Yousef", "Rasha"]
_LAST = ["Al-Harbi", "Al-Otaibi", "Al-Qahtani", "Al-Saud", "Bin Talal", "Hassan", "Khan", "Mansour", "Zayd", "Pereira", "Becker", "Silva", "Nakamura", "Yamamoto", "Costa", "Ferrari", "Bin Salman", "Al-Ghamdi", "Al-Shehri", "Al-Dossari"]


def generate_mock_users(count: int = 100, seed: int = 42) -> List[User]:
    rng = random.Random(seed)
    n_vip = max(1, round(count * 0.35))
    n_high = max(1, round(count * 0.40))
    n_general = count - n_vip - n_high
    users: List[User] = []
    used_ids = set()

    def fresh_id(prefix: str) -> str:
        i = 1
        while True:
            uid = f"{prefix}{i:03d}"
            if uid not in used_ids:
                used_ids.add(uid)
                return uid
            i += 1

    def fresh_name() -> str:
        return f"{rng.choice(_FIRST)} {rng.choice(_LAST)}"

    for _ in range(n_vip):
        users.append(User(fresh_id("VIP"), fresh_name(), True, round(rng.uniform(85, 100), 1)))
    for _ in range(n_high):
        users.append(User(fresh_id("HA"), fresh_name(), False, round(rng.uniform(70, 95), 1)))
    for _ in range(n_general):
        users.append(User(fresh_id("GP"), fresh_name(), False, round(rng.uniform(0, 69), 1)))
    rng.shuffle(users)
    return users
