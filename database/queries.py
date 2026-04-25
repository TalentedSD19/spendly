from database.db import get_db
from datetime import datetime


def get_user_by_id(user_id: int) -> dict | None:
    raise NotImplementedError


def get_summary_stats(user_id: int) -> dict:
    raise NotImplementedError


def get_recent_transactions(user_id: int, limit: int = 10) -> list[dict]:
    raise NotImplementedError


def get_category_breakdown(user_id: int) -> list[dict]:
    raise NotImplementedError
