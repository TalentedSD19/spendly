import sqlite3
import pytest
from werkzeug.security import generate_password_hash

SEED_TOTAL        = 402.49
SEED_COUNT        = 8
SEED_TOP_CATEGORY = "Bills"
SEED_MEMBER_SINCE = "January 2026"
SEED_USER         = {"name": "Demo User", "email": "demo@spendly.com"}


def _make_db():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("""
        CREATE TABLE users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT NOT NULL,
            email         TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at    TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.execute("""
        CREATE TABLE expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id),
            amount      REAL NOT NULL,
            category    TEXT NOT NULL,
            date        TEXT NOT NULL,
            description TEXT,
            created_at  TEXT DEFAULT (datetime('now'))
        )
    """)
    cur = conn.execute(
        "INSERT INTO users (name, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
        ("Demo User", "demo@spendly.com", generate_password_hash("demo123"), "2026-01-15 09:00:00"),
    )
    uid = cur.lastrowid
    conn.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        [
            (uid, 45.50,  "Food",          "2026-04-01", "Grocery run"),
            (uid, 12.00,  "Transport",     "2026-04-03", "Bus pass top-up"),
            (uid, 120.00, "Bills",         "2026-04-05", "Electricity bill"),
            (uid, 35.00,  "Health",        "2026-04-08", "Pharmacy"),
            (uid, 25.00,  "Entertainment", "2026-04-10", "Movie tickets"),
            (uid, 89.99,  "Shopping",      "2026-04-13", "New shoes"),
            (uid, 15.00,  "Other",         "2026-04-16", "Miscellaneous"),
            (uid, 60.00,  "Food",          "2026-04-19", "Dinner out"),
        ],
    )
    conn.commit()
    return conn, uid


@pytest.fixture()
def seeded_db(monkeypatch):
    conn, uid = _make_db()
    import database.db as _db
    monkeypatch.setattr(_db, "get_db", lambda: conn)
    yield conn, uid
    conn.close()


@pytest.fixture()
def app(seeded_db):
    from app import app as flask_app
    flask_app.config.update({"TESTING": True, "SECRET_KEY": "test-secret"})
    yield flask_app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def auth_client(client, seeded_db):
    _, uid = seeded_db
    with client.session_transaction() as sess:
        sess["user_id"]   = uid
        sess["user_name"] = "Demo User"
    return client
