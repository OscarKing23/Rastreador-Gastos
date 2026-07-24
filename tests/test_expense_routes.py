"""Tests for the JSON API expense endpoints."""
import json


def _create_expense(client, data=None):
    """Helper to POST a new expense and return the response."""
    if data is None:
        data = {
            "title": "Test Lunch",
            "amount": 12.50,
            "category": "Food",
            "date": "2025-07-20"
        }
    return client.post(
        "/expenses",
        data=json.dumps(data),
        content_type="application/json"
    )


class TestGetExpenses:
    """Tests for GET /expenses."""

    def test_get_expenses_empty(self, client):
        """GET /expenses on a clean database should return an empty list."""
        response = client.get("/expenses")
        data = response.get_json()
        assert response.status_code == 200
        assert data["status"] == "success"
        assert data["data"] == []


class TestCreateExpense:
    """Tests for POST /expenses."""

    def test_create_expense_success(self, client):
        """POST /expenses with valid data should return 201 and the expense."""
        response = _create_expense(client)
        data = response.get_json()
        assert response.status_code == 201
        assert data["status"] == "success"
        assert data["data"]["title"] == "Test Lunch"
        assert data["data"]["amount"] == 12.50

    def test_create_expense_missing_title(self, client):
        """POST /expenses with an empty title should return 400."""
        response = _create_expense(client, {
            "title": "",
            "amount": 10.00,
            "category": "Food",
            "date": "2025-07-20"
        })
        data = response.get_json()
        assert response.status_code == 400
        assert "Title must not be empty." in data["errors"]

    def test_create_expense_invalid_amount(self, client):
        """POST /expenses with a non-numeric amount should return 400."""
        response = _create_expense(client, {
            "title": "Bad Expense",
            "amount": "not-a-number",
            "category": "Misc",
            "date": "2025-07-20"
        })
        data = response.get_json()
        assert response.status_code == 400
        assert "Amount must be a valid number." in data["errors"]

    def test_create_expense_negative_amount(self, client):
        """POST /expenses with a negative amount should return 400."""
        response = _create_expense(client, {
            "title": "Negative",
            "amount": -5.00,
            "category": "Test",
            "date": "2025-07-20"
        })
        data = response.get_json()
        assert response.status_code == 400
        assert "Amount must be positive." in data["errors"]

    def test_create_expense_empty_body(self, client):
        """POST /expenses with an empty JSON body should return 400."""
        response = client.post(
            "/expenses",
            data=json.dumps({}),
            content_type="application/json"
        )
        assert response.status_code == 400


class TestGetExpensesAfterCreate:
    """Tests verifying expenses appear after creation."""

    def test_get_expenses_after_create(self, client):
        """After creating an expense, GET /expenses should include it."""
        _create_expense(client)
        response = client.get("/expenses")
        data = response.get_json()
        assert response.status_code == 200
        assert len(data["data"]) == 1
        assert data["data"][0]["title"] == "Test Lunch"


class TestDeleteExpense:
    """Tests for DELETE /expenses/<id>."""

    def test_delete_expense_success(self, client):
        """DELETE /expenses/<id> for an existing expense should return 200."""
        create_resp = _create_expense(client)
        expense_id = create_resp.get_json()["data"]["id"]
        response = client.delete(f"/expenses/{expense_id}")
        assert response.status_code == 200
        assert response.get_json()["status"] == "deleted"

    def test_delete_expense_not_found(self, client):
        """DELETE /expenses/<id> for a non-existent ID should return 404."""
        response = client.delete("/expenses/99999")
        assert response.status_code == 404
        assert response.get_json()["status"] == "error"

    def test_create_and_delete_flow(self, client):
        """Full flow: create an expense, verify it exists, delete it, verify it's gone."""
        # Create
        create_resp = _create_expense(client)
        expense_id = create_resp.get_json()["data"]["id"]

        # Verify it exists
        list_resp = client.get("/expenses")
        assert len(list_resp.get_json()["data"]) == 1

        # Delete
        del_resp = client.delete(f"/expenses/{expense_id}")
        assert del_resp.status_code == 200

        # Verify it's gone
        list_resp = client.get("/expenses")
        assert len(list_resp.get_json()["data"]) == 0
