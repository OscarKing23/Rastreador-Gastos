"""
Phase 4: End-to-End tests using Selenium WebDriver.
These tests open a real Chrome browser and simulate user interactions.
"""
import os
import threading
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService

from app import create_app
from app.database import init_db

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

BASE_URL = "http://127.0.0.1:5555"


@pytest.fixture(scope="module")
def live_server():
    """Start the Flask app on a background thread for E2E testing."""
    app = create_app("testing")

    with app.app_context():
        init_db(app.config["DATABASE_PATH"])

    server_thread = threading.Thread(
        target=lambda: app.run(host="127.0.0.1", port=5555, use_reloader=False)
    )
    server_thread.daemon = True
    server_thread.start()

    # Wait for the server to be ready
    time.sleep(1.5)

    yield app

    # Cleanup is handled by daemon thread termination


@pytest.fixture(scope="module")
def browser(live_server):
    """Provide a Chrome browser instance. Uses headless mode in CI, visual mode locally."""
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-search-engine-choice-screen")

    # Detect CI environment and run headless
    if os.environ.get("CI"):
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
    else:
        options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)

    yield driver

    driver.quit()


def _clear_all_expenses(browser):
    """Helper: delete all expenses from the table via the UI."""
    browser.get(BASE_URL)
    time.sleep(0.5)
    while True:
        delete_buttons = browser.find_elements(By.CSS_SELECTOR, ".btn-danger")
        if not delete_buttons:
            break
        delete_buttons[0].click()
        time.sleep(0.5)


def _create_expense_via_form(browser, title, amount, category, date_str):
    """Helper: fill and submit the expense form."""
    browser.find_element(By.ID, "title").clear()
    browser.find_element(By.ID, "title").send_keys(title)

    browser.find_element(By.ID, "amount").clear()
    browser.find_element(By.ID, "amount").send_keys(str(amount))

    browser.find_element(By.ID, "category").clear()
    browser.find_element(By.ID, "category").send_keys(category)

    date_input = browser.find_element(By.ID, "date")
    date_input.clear()
    date_input.send_keys(date_str)

    browser.find_element(By.ID, "btn-add-expense").click()
    time.sleep(1)


# ---------------------------------------------------------------------------
# E2E Tests
# ---------------------------------------------------------------------------


class TestE2EPageLoad:
    """Test 1: Verify the page loads correctly with all 3 cards."""

    def test_page_loads_correctly(self, browser):
        """The main page should load with the header and 3 card sections."""
        _clear_all_expenses(browser)
        browser.get(BASE_URL)
        time.sleep(1)

        # Wait for the header to be visible
        header = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".logo h1"))
        )
        assert "Expense Tracker" in header.text

        # Wait for all 3 cards to be present
        WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".card"))
        )
        cards = browser.find_elements(By.CSS_SELECTOR, ".card")
        assert len(cards) == 3, f"Expected 3 cards, found {len(cards)}"

        # Verify each card is visible
        add_card = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.ID, "add-expense-card"))
        )
        assert add_card.is_displayed()

        filter_card = browser.find_element(By.ID, "filter-card")
        assert filter_card.is_displayed()

        expenses_card = browser.find_element(By.ID, "expenses-card")
        assert expenses_card.is_displayed()


class TestE2ECreateExpense:
    """Test 2: Create an expense through the form and verify it in the table."""

    def test_create_expense(self, browser):
        """Fill the form, submit, and verify the expense appears in the table."""
        _clear_all_expenses(browser)
        browser.get(BASE_URL)
        time.sleep(0.5)

        # Fill the form
        _create_expense_via_form(browser, "Selenium Lunch", "25.50", "Food", "07202025")

        # Wait for the toast notification
        WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".toast.success"))
        )

        # Verify the expense appears in the table
        table_body = browser.find_element(By.CSS_SELECTOR, "#expenses-table tbody")
        rows = table_body.find_elements(By.TAG_NAME, "tr")
        assert len(rows) >= 1

        # Verify the row content
        first_row_text = rows[0].text
        assert "Selenium Lunch" in first_row_text
        assert "25.50" in first_row_text


class TestE2EFilterExpenses:
    """Test 3: Create expenses and filter by category."""

    def test_filter_expenses(self, browser):
        """Create 2 expenses with different categories, filter, verify results."""
        _clear_all_expenses(browser)
        browser.get(BASE_URL)
        time.sleep(0.5)

        # Create expense 1: Food
        _create_expense_via_form(browser, "Pizza", "15.00", "Food", "07202025")

        # Create expense 2: Transport
        _create_expense_via_form(browser, "Taxi Ride", "8.50", "Transport", "07202025")

        # Verify both expenses are in the table
        rows = browser.find_elements(By.CSS_SELECTOR, "#expenses-table tbody tr")
        assert len(rows) == 2

        # Apply filter for "Food"
        filter_input = browser.find_element(By.ID, "filter-category")
        filter_input.clear()
        filter_input.send_keys("Food")
        browser.find_element(By.ID, "btn-apply-filter").click()
        time.sleep(1)

        # Verify only 1 expense is shown (Food)
        filtered_rows = browser.find_elements(By.CSS_SELECTOR, "#expenses-table tbody tr")
        assert len(filtered_rows) == 1
        assert "Pizza" in filtered_rows[0].text

        # Clear filter
        browser.find_element(By.ID, "btn-clear-filter").click()
        time.sleep(1)

        # Verify both are shown again
        all_rows = browser.find_elements(By.CSS_SELECTOR, "#expenses-table tbody tr")
        assert len(all_rows) == 2


class TestE2EDeleteExpense:
    """Test 4: Delete an expense and verify it's removed."""

    def test_delete_expense(self, browser):
        """Create an expense, delete it, and verify the table is empty."""
        _clear_all_expenses(browser)
        browser.get(BASE_URL)
        time.sleep(0.5)

        # Create an expense
        _create_expense_via_form(browser, "To Delete", "5.00", "Test", "07202025")

        # Verify it exists
        rows = browser.find_elements(By.CSS_SELECTOR, "#expenses-table tbody tr")
        assert len(rows) == 1

        # Click the delete button
        delete_btn = browser.find_element(By.CSS_SELECTOR, ".btn-danger")
        delete_btn.click()
        time.sleep(1)

        # Wait for toast
        WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".toast"))
        )

        # Verify the table is empty
        remaining_rows = browser.find_elements(By.CSS_SELECTOR, "#expenses-table tbody tr")
        assert len(remaining_rows) == 0
