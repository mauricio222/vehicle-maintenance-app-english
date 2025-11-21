"""
Pytest configuration and fixtures for Playwright E2E tests.
"""
import pytest
from playwright.sync_api import Page, Browser, Playwright
import time
import os
from typing import Generator

# Base URL for the Flask application
BASE_URL = os.getenv("TEST_BASE_URL", "http://localhost:5000")

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context with additional settings."""
    return {
        **browser_context_args,
        "base_url": BASE_URL,
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
    }

@pytest.fixture(scope="function")
def authenticated_page(page: Page) -> Generator[Page, None, None]:
    """
    Fixture that provides a page with authenticated user session.
    Creates a test user and logs in before each test.
    """
    # Navigate to registration page
    page.goto("/register")

    # Generate unique test user credentials
    timestamp = str(int(time.time()))
    test_username = f"testuser_{timestamp}"
    test_password = "TestPass123!"

    # Fill registration form
    page.fill("input[name='username']", test_username)
    page.fill("input[name='password']", test_password)
    page.fill("input[name='confirm_password']", test_password)

    # Submit registration
    page.click("button[type='submit']")

    # Wait for redirect to login or dashboard
    page.wait_for_load_state("networkidle")

    # If redirected to login, perform login
    if "/login" in page.url:
        page.fill("input[name='username']", test_username)
        page.fill("input[name='password']", test_password)
        page.click("button[type='submit']")
        page.wait_for_load_state("networkidle")

    # Store credentials for potential use in tests
    page.context.test_username = test_username
    page.context.test_password = test_password

    yield page

    # Cleanup: Logout after test
    try:
        page.goto("/logout")
    except:
        pass  # Ignore errors during cleanup

@pytest.fixture(scope="function")
def test_vehicle_data():
    """Provides sample vehicle data for tests."""
    return {
        "marca": "Toyota",
        "modelo": "Corolla",
        "año": "2022",
        "kilometraje": "15000",
        "color": "Silver",
        "placa": f"TEST{int(time.time()) % 10000}",
    }

@pytest.fixture(scope="function")
def test_maintenance_data():
    """Provides sample maintenance data for tests."""
    return {
        "categoria": "Aceite",
        "tipo": "Cambio de Aceite",
        "kilometraje": "15500",
        "costo": "45.00",
        "mecanico": "Taller",
        "notas": "Test maintenance entry",
    }

@pytest.fixture(autouse=True)
def slow_down_tests():
    """
    Automatically slow down tests for better visibility during development.
    Remove or modify this fixture for CI/CD environments.
    """
    # Add a small delay between actions for visibility
    # You can set FAST_TESTS=1 environment variable to skip delays
    if not os.getenv("FAST_TESTS"):
        yield
        time.sleep(0.5)
    else:
        yield

def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "e2e: mark test as end-to-end test"
    )
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "auth: mark test as authentication test"
    )
    config.addinivalue_line(
        "markers", "maintenance: mark test as maintenance module test"
    )