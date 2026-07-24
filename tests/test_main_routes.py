"""Tests for the main HTML routes."""


class TestIndexRoute:
    """Tests for the GET / route that renders the HTML page."""

    def test_index_returns_200(self, client):
        """GET / should return HTTP 200 OK."""
        response = client.get("/")
        assert response.status_code == 200

    def test_index_returns_html(self, client):
        """GET / should return an HTML content type."""
        response = client.get("/")
        assert "text/html" in response.content_type

    def test_index_contains_title(self, client):
        """GET / HTML should contain the app title 'Expense Tracker'."""
        response = client.get("/")
        assert b"Expense Tracker" in response.data
