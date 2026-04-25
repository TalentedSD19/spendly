def test_recent_transactions_returns_list(seeded_db):
    from database.queries import get_recent_transactions
    _, uid = seeded_db
    result = get_recent_transactions(uid)
    assert isinstance(result, list)
    assert len(result) == 8


def test_recent_transactions_shape(seeded_db):
    from database.queries import get_recent_transactions
    _, uid = seeded_db
    tx = get_recent_transactions(uid)[0]
    assert set(tx.keys()) == {"date", "description", "category", "amount"}


def test_recent_transactions_newest_first(seeded_db):
    from database.queries import get_recent_transactions
    _, uid = seeded_db
    result = get_recent_transactions(uid)
    dates = [r["date"] for r in result]
    assert dates == sorted(dates, reverse=True)


def test_recent_transactions_empty_user(seeded_db):
    from database.queries import get_recent_transactions
    result = get_recent_transactions(user_id=9999)
    assert result == []


def test_recent_transactions_limit(seeded_db):
    from database.queries import get_recent_transactions
    _, uid = seeded_db
    result = get_recent_transactions(uid, limit=3)
    assert len(result) == 3


def test_category_breakdown_order(seeded_db):
    from database.queries import get_category_breakdown
    _, uid = seeded_db
    result = get_category_breakdown(uid)
    amounts = [r["amount"] for r in result]
    assert amounts == sorted(amounts, reverse=True)


def test_category_breakdown_pct_sums_to_100(seeded_db):
    from database.queries import get_category_breakdown
    _, uid = seeded_db
    result = get_category_breakdown(uid)
    assert sum(r["pct"] for r in result) == 100


def test_category_breakdown_pct_are_integers(seeded_db):
    from database.queries import get_category_breakdown
    _, uid = seeded_db
    result = get_category_breakdown(uid)
    for r in result:
        assert isinstance(r["pct"], int)


def test_category_breakdown_shape(seeded_db):
    from database.queries import get_category_breakdown
    _, uid = seeded_db
    result = get_category_breakdown(uid)
    assert set(result[0].keys()) == {"name", "amount", "pct"}


def test_category_breakdown_seven_categories(seeded_db):
    from database.queries import get_category_breakdown
    _, uid = seeded_db
    result = get_category_breakdown(uid)
    assert len(result) == 7


def test_category_breakdown_empty_user(seeded_db):
    from database.queries import get_category_breakdown
    result = get_category_breakdown(user_id=9999)
    assert result == []


# --- get_summary_stats ---

def test_summary_stats_with_expenses(seeded_db):
    from database.queries import get_summary_stats
    _, uid = seeded_db
    result = get_summary_stats(uid)
    assert abs(result["total_spent"] - 402.49) < 0.01
    assert result["transaction_count"] == 8
    assert result["top_category"] == "Bills"


def test_summary_stats_no_expenses(seeded_db):
    from database.queries import get_summary_stats
    result = get_summary_stats(user_id=9999)
    assert result == {"total_spent": 0.0, "transaction_count": 0, "top_category": "—"}


def test_summary_stats_returns_dict(seeded_db):
    from database.queries import get_summary_stats
    _, uid = seeded_db
    result = get_summary_stats(uid)
    assert set(result.keys()) == {"total_spent", "transaction_count", "top_category"}


# --- get_user_by_id ---

def test_user_by_id_returns_correct_fields(seeded_db):
    from database.queries import get_user_by_id
    _, uid = seeded_db
    result = get_user_by_id(uid)
    assert result["name"] == "Demo User"
    assert result["email"] == "demo@spendly.com"
    assert result["member_since"] == "January 2026"


def test_user_by_id_nonexistent(seeded_db):
    from database.queries import get_user_by_id
    assert get_user_by_id(9999) is None


def test_user_by_id_no_password_hash(seeded_db):
    from database.queries import get_user_by_id
    _, uid = seeded_db
    result = get_user_by_id(uid)
    assert "password_hash" not in result


# --- GET /profile routes ---

def test_profile_unauthenticated_redirects(client):
    response = client.get("/profile")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_profile_authenticated_returns_200(auth_client):
    response = auth_client.get("/profile")
    assert response.status_code == 200


def test_profile_shows_seed_user_name(auth_client):
    response = auth_client.get("/profile")
    assert b"Demo User" in response.data


def test_profile_shows_seed_user_email(auth_client):
    response = auth_client.get("/profile")
    assert b"demo@spendly.com" in response.data


def test_profile_shows_rupee_symbol(auth_client):
    response = auth_client.get("/profile")
    assert "₹".encode() in response.data


def test_profile_total_spent(auth_client):
    response = auth_client.get("/profile")
    assert b"402.49" in response.data


def test_profile_transaction_count(auth_client):
    response = auth_client.get("/profile")
    assert b"8" in response.data


def test_profile_top_category(auth_client):
    response = auth_client.get("/profile")
    assert b"Bills" in response.data


def test_profile_member_since(auth_client):
    response = auth_client.get("/profile")
    assert b"January 2026" in response.data
