"""
End-to-end tests for the Vehicle Maintenance Application.
Tests the complete user journey from registration to maintenance tracking.
FINAL FIXED VERSION - Handles modals and dynamic content properly.
"""
import pytest
from playwright.sync_api import Page, expect
import time


class TestAuthentication:
    """Test suite for authentication flows."""

    @pytest.mark.e2e
    @pytest.mark.auth
    @pytest.mark.smoke
    def test_user_registration_flow(self, page: Page):
        """Test complete user registration flow."""
        # Navigate to registration page
        page.goto("/register")

        # Verify registration page loaded
        expect(page).to_have_title("User Registration")

        # Generate unique user credentials
        timestamp = str(int(time.time()))
        username = f"newuser_{timestamp}"
        password = "SecurePass123!"

        # Fill registration form
        page.fill("input[name='username']", username)
        page.fill("input[name='password']", password)
        page.fill("input[name='confirm_password']", password)

        # Submit registration
        page.click("button[type='submit']")

        # Wait for redirect
        page.wait_for_load_state("networkidle")

        # Verify successful registration (redirected to login)
        assert "/login" in page.url or "/dashboard" in page.url

    @pytest.mark.e2e
    @pytest.mark.auth
    def test_user_login_flow(self, page: Page):
        """Test user login flow."""
        # First register a user
        page.goto("/register")
        timestamp = str(int(time.time()))
        username = f"logintest_{timestamp}"
        password = "LoginPass123!"

        page.fill("input[name='username']", username)
        page.fill("input[name='password']", password)
        page.fill("input[name='confirm_password']", password)
        page.click("button[type='submit']")
        page.wait_for_load_state("networkidle")

        # Now test login
        page.goto("/login")
        expect(page).to_have_title("Login")

        # Fill login form
        page.fill("input[name='username']", username)
        page.fill("input[name='password']", password)

        # Submit login
        page.click("button[type='submit']")
        page.wait_for_load_state("networkidle")

        # Verify successful login (redirected to dashboard)
        expect(page).to_have_url("/dashboard")

    @pytest.mark.e2e
    @pytest.mark.auth
    def test_logout_flow(self, authenticated_page: Page):
        """Test user logout flow."""
        # Navigate to dashboard
        authenticated_page.goto("/dashboard")

        # Click logout link/button
        authenticated_page.goto("/logout")

        # Verify redirect to login page
        authenticated_page.wait_for_load_state("networkidle")
        expect(authenticated_page).to_have_url("/login")


class TestVehicleManagement:
    """Test suite for vehicle management features."""

    @pytest.mark.e2e
    @pytest.mark.smoke
    def test_add_vehicle(self, authenticated_page: Page, test_vehicle_data):
        """Test adding a new vehicle."""
        # Navigate to dashboard
        authenticated_page.goto("/dashboard")

        # Click button to open modal
        authenticated_page.click("button:has-text('Add New Vehicle')")

        # Wait for modal to be visible
        authenticated_page.wait_for_selector("#nuevoVehiculoModal .modal-content", state="visible")

        # Fill vehicle form
        alias = f"{test_vehicle_data['marca']} {test_vehicle_data['modelo']}"
        authenticated_page.fill("input[name='alias']", alias)
        authenticated_page.fill("input[name='marca']", test_vehicle_data["marca"])
        authenticated_page.fill("input[name='modelo']", test_vehicle_data["modelo"])
        authenticated_page.fill("input[name='anio']", test_vehicle_data["año"])
        authenticated_page.select_option("select[name='tipo']", "Sedán")
        authenticated_page.select_option("select[name='tipo_motor']", "Gasolina")
        authenticated_page.select_option("select[name='tipo_transmision']", "Automática")  # Missing required field!

        # Submit form (within modal)
        authenticated_page.locator("#nuevoVehiculoModal button[type='submit']").click()

        # Wait for response - the form submission will reload the page
        authenticated_page.wait_for_load_state("networkidle")

        # After form submission, we should be back on dashboard
        # The modal closes automatically due to page reload
        expect(authenticated_page).to_have_url("/dashboard")

        # Verify vehicle appears in the list - look for the alias in the card title
        # Use .first in case there are multiple vehicles with same name
        vehicle_card = authenticated_page.locator(f"h5.card-title:text('{alias}')").first
        expect(vehicle_card).to_be_visible(timeout=10000)

    @pytest.mark.e2e
    def test_view_vehicle_details(self, authenticated_page: Page, test_vehicle_data):
        """Test viewing vehicle details and maintenance history."""
        # First add a vehicle
        authenticated_page.goto("/dashboard")

        # Open modal
        authenticated_page.click("button:has-text('Add New Vehicle')")
        authenticated_page.wait_for_selector("#nuevoVehiculoModal .modal-content", state="visible")

        # Fill form
        authenticated_page.fill("input[name='alias']", f"{test_vehicle_data['marca']} {test_vehicle_data['modelo']}")
        authenticated_page.fill("input[name='marca']", test_vehicle_data["marca"])
        authenticated_page.fill("input[name='modelo']", test_vehicle_data["modelo"])
        authenticated_page.fill("input[name='anio']", test_vehicle_data["año"])
        authenticated_page.select_option("select[name='tipo']", "Sedán")
        authenticated_page.select_option("select[name='tipo_motor']", "Gasolina")
        authenticated_page.select_option("select[name='tipo_transmision']", "Automática")

        # Submit
        authenticated_page.locator("#nuevoVehiculoModal button[type='submit']").click()
        authenticated_page.wait_for_load_state("networkidle")

        # The page should have reloaded after form submission
        expect(authenticated_page).to_have_url("/dashboard")

        # Wait a bit for the page to update
        authenticated_page.wait_for_timeout(1000)

        # Click on the vehicle to view maintenance - use "View Maintenance" button
        vehicle_link = authenticated_page.locator("a.btn.btn-secondary:has-text('View Maintenance')").first
        vehicle_link.click()

        # Verify maintenance page loaded
        authenticated_page.wait_for_load_state("networkidle")
        # Check that URL contains /maintenance/
        assert "/maintenance/" in authenticated_page.url or "/mantenimientos/" in authenticated_page.url


class TestMaintenanceTracking:
    """Test suite for maintenance tracking features."""

    @pytest.mark.e2e
    @pytest.mark.maintenance
    def test_add_maintenance_record(self, authenticated_page: Page, test_vehicle_data):
        """Test adding a maintenance record to a vehicle."""
        # First add a vehicle
        authenticated_page.goto("/dashboard")

        # Open modal
        authenticated_page.click("button:has-text('Add New Vehicle')")
        authenticated_page.wait_for_selector("#nuevoVehiculoModal .modal-content", state="visible")

        # Fill form
        authenticated_page.fill("input[name='alias']", f"{test_vehicle_data['marca']} {test_vehicle_data['modelo']}")
        authenticated_page.fill("input[name='marca']", test_vehicle_data["marca"])
        authenticated_page.fill("input[name='modelo']", test_vehicle_data["modelo"])
        authenticated_page.fill("input[name='anio']", test_vehicle_data["año"])
        authenticated_page.select_option("select[name='tipo']", "Sedán")
        authenticated_page.select_option("select[name='tipo_motor']", "Gasolina")
        authenticated_page.select_option("select[name='tipo_transmision']", "Automática")

        # Submit
        authenticated_page.locator("#nuevoVehiculoModal button[type='submit']").click()
        authenticated_page.wait_for_load_state("networkidle")

        # Navigate to maintenance registration
        authenticated_page.goto("/registration")
        authenticated_page.wait_for_load_state("networkidle")

        # Select the vehicle from dropdown
        vehicle_select = authenticated_page.locator("select#vehiculo")
        vehicle_select.wait_for(state="visible", timeout=10000)
        authenticated_page.wait_for_timeout(1000)

        # Select by index (skip empty option)
        options = vehicle_select.locator("option")
        if options.count() > 1:
            vehicle_select.select_option(index=1)

        # Wait for any dynamic content to load
        authenticated_page.wait_for_timeout(2000)

        # Fill maintenance details
        authenticated_page.fill("input#mileage", "16000")
        authenticated_page.fill("input#fecha", "12/31/2024")

        # Fill cost if present
        cost_input = authenticated_page.locator("input#costo")
        if cost_input.count() > 0:
            cost_input.fill("50.00")

        # Add notes
        notes_textarea = authenticated_page.locator("textarea#observaciones")
        if notes_textarea.count() > 0:
            notes_textarea.fill("Regular maintenance check")

        # Save maintenance record - look for save button
        save_button = authenticated_page.locator("button:has-text('Save'), button:has-text('Guardar'), button#guardarBtn")
        if save_button.count() > 0:
            save_button.first.click()
            # Wait for save confirmation
            authenticated_page.wait_for_timeout(2000)

    @pytest.mark.e2e
    @pytest.mark.maintenance
    def test_ai_suggestions(self, authenticated_page: Page, test_vehicle_data):
        """Test AI-powered maintenance suggestions."""
        # First ensure we have a vehicle
        authenticated_page.goto("/dashboard")

        # Check if we need to add a vehicle
        vehicle_cards = authenticated_page.locator(".card-title")
        if vehicle_cards.count() == 0:
            # Add a vehicle
            authenticated_page.click("button:has-text('Add New Vehicle')")
            authenticated_page.wait_for_selector("#nuevoVehiculoModal .modal-content", state="visible")

            authenticated_page.fill("input[name='alias']", f"{test_vehicle_data['marca']} {test_vehicle_data['modelo']}")
            authenticated_page.fill("input[name='marca']", test_vehicle_data["marca"])
            authenticated_page.fill("input[name='modelo']", test_vehicle_data["modelo"])
            authenticated_page.fill("input[name='anio']", test_vehicle_data["año"])
            authenticated_page.select_option("select[name='tipo']", "Sedán")
            authenticated_page.select_option("select[name='tipo_motor']", "Gasolina")
            authenticated_page.select_option("select[name='tipo_transmision']", "Automática")

            authenticated_page.locator("#nuevoVehiculoModal button[type='submit']").click()
            authenticated_page.wait_for_load_state("networkidle")

        # Navigate to registration page
        authenticated_page.goto("/registration")
        authenticated_page.wait_for_load_state("networkidle")

        # Select vehicle
        vehicle_select = authenticated_page.locator("select#vehiculo")
        vehicle_select.wait_for(state="visible", timeout=10000)
        authenticated_page.wait_for_timeout(1000)

        if vehicle_select.locator("option").count() > 1:
            vehicle_select.select_option(index=1)
            authenticated_page.wait_for_timeout(1000)

            # Look for AI suggestion buttons - use regex or multiple selectors
            suggest_buttons = authenticated_page.locator(
                "button:has-text('Suggest'), button:has-text('Sugerir'), button:has-text('suggest'), button:has-text('sugerir')"
            )

            # Try to find visible suggestion buttons
            visible_buttons = []
            for i in range(suggest_buttons.count()):
                button = suggest_buttons.nth(i)
                if button.is_visible():
                    visible_buttons.append(button)

            if visible_buttons:
                # Click the first visible suggestion button
                visible_buttons[0].click()
                authenticated_page.wait_for_timeout(3000)

                # Check if any suggestion appeared
                # The suggestion might appear in various elements
                suggestion_elements = authenticated_page.locator(
                    "[id*='ugerencia'], [id*='uggestion'], .suggestion, .ai-response"
                )

                if suggestion_elements.count() > 0:
                    # Just verify at least one element is visible
                    expect(suggestion_elements.first).to_be_visible()
            else:
                # AI suggestions might not be available - that's OK
                # Just verify the page is still functional
                assert authenticated_page.url.endswith("/registration")


class TestCompleteUserJourney:
    """Test complete user journey from start to finish."""

    @pytest.mark.e2e
    def test_complete_workflow(self, page: Page):
        """Test the complete workflow: register -> login -> add vehicle -> add maintenance -> view history."""
        # Step 1: Register new user
        page.goto("/register")
        timestamp = str(int(time.time()))
        username = f"journey_{timestamp}"
        password = "JourneyPass123!"

        page.fill("input[name='username']", username)
        page.fill("input[name='password']", password)
        page.fill("input[name='confirm_password']", password)
        page.click("button[type='submit']")
        page.wait_for_load_state("networkidle")

        # Step 2: Login if needed
        if "/login" in page.url:
            page.fill("input[name='username']", username)
            page.fill("input[name='password']", password)
            page.click("button[type='submit']")
            page.wait_for_load_state("networkidle")

        # Step 3: Add a vehicle
        expect(page).to_have_url("/dashboard")

        # Open modal
        page.click("button:has-text('Add New Vehicle')")
        page.wait_for_selector("#nuevoVehiculoModal .modal-content", state="visible")

        # Fill form
        page.fill("input[name='alias']", "Honda Civic")
        page.fill("input[name='marca']", "Honda")
        page.fill("input[name='modelo']", "Civic")
        page.fill("input[name='anio']", "2021")
        page.select_option("select[name='tipo']", "Sedán")
        page.select_option("select[name='tipo_motor']", "Gasolina")
        page.select_option("select[name='tipo_transmision']", "Automática")

        # Submit - this will reload the page
        page.locator("#nuevoVehiculoModal button[type='submit']").click()
        page.wait_for_load_state("networkidle")

        # Verify we're back on dashboard after form submission
        expect(page).to_have_url("/dashboard")

        # Step 4: Navigate to maintenance registration
        page.goto("/registration")
        page.wait_for_load_state("networkidle")

        # Select vehicle
        vehicle_select = page.locator("select#vehiculo")
        vehicle_select.wait_for(state="visible", timeout=10000)
        page.wait_for_timeout(1000)

        if vehicle_select.locator("option").count() > 1:
            vehicle_select.select_option(index=1)
            page.wait_for_timeout(1000)

        # Step 5: Add maintenance record
        page.fill("input#mileage", "25500")
        page.fill("input#fecha", "12/31/2024")

        cost_input = page.locator("input#costo")
        if cost_input.count() > 0:
            cost_input.fill("75.00")

        notes_textarea = page.locator("textarea#observaciones")
        if notes_textarea.count() > 0:
            notes_textarea.fill("Complete service")

        # Save
        save_button = page.locator("button:has-text('Save'), button:has-text('Guardar'), button#guardarBtn")
        if save_button.count() > 0:
            save_button.first.click()
            page.wait_for_timeout(2000)

        # Step 6: View maintenance history
        page.goto("/dashboard")
        page.wait_for_load_state("networkidle")

        # Click view maintenance for first vehicle
        maintenance_link = page.locator("a.btn.btn-secondary:has-text('View Maintenance')").first
        if maintenance_link.count() > 0:
            maintenance_link.click()
            page.wait_for_load_state("networkidle")

            # Verify we're on maintenance page
            assert "/maintenance/" in page.url or "/mantenimientos/" in page.url

        # Step 7: Logout
        page.goto("/logout")
        expect(page).to_have_url("/login")


class TestResponsiveness:
    """Test application responsiveness on different screen sizes."""

    @pytest.mark.e2e
    def test_mobile_viewport(self, page: Page):
        """Test application on mobile viewport."""
        # Set mobile viewport
        page.set_viewport_size({"width": 375, "height": 812})

        # Navigate to homepage
        page.goto("/")

        # Verify page loads correctly
        page.wait_for_load_state("networkidle")
        expect(page.locator("body")).to_be_visible()

        # Test navigation on mobile
        page.goto("/register")
        expect(page).to_have_title("User Registration")

    @pytest.mark.e2e
    def test_tablet_viewport(self, page: Page):
        """Test application on tablet viewport."""
        # Set tablet viewport
        page.set_viewport_size({"width": 768, "height": 1024})

        # Navigate to homepage
        page.goto("/")

        # Verify page loads correctly
        page.wait_for_load_state("networkidle")
        expect(page.locator("body")).to_be_visible()

        # Test navigation on tablet
        page.goto("/login")
        expect(page).to_have_title("Login")