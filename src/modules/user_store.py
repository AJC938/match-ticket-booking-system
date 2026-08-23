"""Persist manually registered users in a local JSON file."""

import json
import os
from typing import List
from .models import User

_HERE = os.path.dirname(os.path.abspath(__file__))
STORE_PATH = os.path.join(_HERE, "..", "registered_users.json")


def load_registered_users() -> List[User]:
    if not os.path.exists(STORE_PATH):
        return []
    try:
        with open(STORE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [User(entry["user_id"], entry["name"], entry.get("is_vip", False), entry.get("attendance", 0.0)) for entry in data]
    except (json.JSONDecodeError, KeyError, TypeError):
        return []


def save_new_user(user: User) -> None:
    existing = load_registered_users()
    if any(item.user_id == user.user_id for item in existing):
        return
    existing.append(user)
    with open(STORE_PATH, "w", encoding="utf-8") as f:
        json.dump([{"user_id": u.user_id, "name": u.name, "is_vip": u.is_vip, "attendance": u.attendance} for u in existing], f, indent=2)
