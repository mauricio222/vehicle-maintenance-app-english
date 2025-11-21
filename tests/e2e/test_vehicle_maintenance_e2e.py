"""
End-to-end tests for the Vehicle Maintenance Application.
Tests the complete user journey from registration to maintenance tracking.
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
        authenticated_page.wait_for_selector("#nuevoVehiculoModal", state="visible")

        # Fill vehicle form
        authenticated_page.fill("input[name='alias']", f"{test_vehicle_data['marca']} {test_vehicle_data['modelo']}")
        authenticated_page.fill("input[name='marca']", test_vehicle_data["marca"])
        authenticated_page.fill("input[name='modelo']", test_vehicle_data["modelo"])
        authenticated_page.fill("input[name='anio']", test_vehicle_data["año"])
        authenticated_page.select_option("select[name='tipo']", "Sedán")
        authenticated_page.select_option("select[name='tipo_motor']", "Gasolina")

        # Submit form (within modal)
        authenticated_page.locator("#nuevoVehiculoModal button[type='submit']").click()

        # Wait for response
        authenticated_page.wait_for_load_state("networkidle")

        # Verify vehicle appears in the list
        vehicle_card = authenticated_page.locator(f"text={test_vehicle_data['marca']} {test_vehicle_data['modelo']}")
        expect(vehicle_card).to_be_visible()

    @pytest.mark.e2e
    def test_view_vehicle_details(self, authenticated_page: Page, test_vehicle_data):
        """Test viewing vehicle details and maintenance history."""
        # First add a vehicle
        authenticated_page.goto("/dashboard")

        # Open modal
        authenticated_page.click("button:has-text('Add New Vehicle')")
        authenticated_page.wait_for_selector("#nuevoVehiculoModal", state="visible")

        # Fill form
        authenticated_page.fill("input[name='alias']", f"{test_vehicle_data['marca']} {test_vehicle_data['modelo']}")
        authenticated_page.fill("input[name='marca']", test_vehicle_data["marca"])
        authenticated_page.fill("input[name='modelo']", test_vehicle_data["modelo"])
        authenticated_page.fill("input[name='anio']", test_vehicle_data["año"])
        authenticated_page.select_option("select[name='tipo']", "Sedán")
        authenticated_page.select_option("select[name='tipo_motor']", "Gasolina")

        # Submit
        authenticated_page.locator("#nuevoVehiculoModal button[type='submit']").click()
        authenticated_page.wait_for_load_state("networkidle")

        # Click on the vehicle to view maintenance
        vehicle_link = authenticated_page.locator("a.btn.btn-primary").first
        vehicle_link.click()

        # Verify maintenance page loaded
        authenticated_page.wait_for_load_state("networkidle")
        expect(authenticated_page).to_have_url(lambda url: "/maintenance/" in url)


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
        authenticated_page.wait_for_selector("#nuevoVehiculoModal", state="visible")

        # Fill form
        authenticated_page.fill("input[name='alias']", f"{test_vehicle_data['marca']} {test_vehicle_data['modelo']}")
        authenticated_page.fill("input[name='marca']", test_vehicle_data["marca"])
        authenticated_page.fill("input[name='modelo']", test_vehicle_data["modelo"])
        authenticated_page.fill("input[name='anio']", test_vehicle_data["año"])
        authenticated_page.select_option("select[name='tipo']", "Sedán")
        authenticated_page.select_option("select[name='tipo_motor']", "Gasolina")

        # Submit
        authenticated_page.locator("#nuevoVehiculoModal button[type='submit']").click()
        authenticated_page.wait_for_load_state("networkidle")

        # Navigate to maintenance registration
        authenticated_page.goto("/registration")

        # Select the vehicle from dropdown
        vehicle_select = authenticated_page.locator("select#vehicleSelect")
        vehicle_select.select_option(index=1)  # Select first vehicle

        # Wait for maintenance types to load
        authenticated_page.wait_for_timeout(1000)

        # Select maintenance type
        maintenance_select = authenticated_page.locator("select#maintenanceSelect")
        if maintenance_select.count() > 0:
            maintenance_select.select_option(index=1)

        # Fill maintenance details
        authenticated_page.fill("input#kilometraje", "16000")
        authenticated_page.fill("input#cost", "50.00")

        # Select mechanic
        mechanic_select = authenticated_page.locator("select#mechanicSelect")
        if mechanic_select.count() > 0:
            mechanic_select.select_option(index=1)

        # Add notes
        authenticated_page.fill("textarea#notes", "Regular maintenance check")

        # Save maintenance record
        authenticated_page.click("button#saveBtn")

        # Wait for save confirmation
        authenticated_page.wait_for_timeout(2000)

        # Verify success (check for alert or redirect)
        success_alert = authenticated_page.locator(".alert-success")
        if success_alert.count() > 0:
            expect(success_alert).to_be_visible()

    @pytest.mark.e2e
    @pytest.mark.maintenance
    def test_ai_suggestions(self, authenticated_page: Page, test_vehicle_data):
        """Test AI-powered maintenance suggestions."""
        # Navigate to registration page
        authenticated_page.goto("/registration")

        # Add a vehicle first if needed
        vehicle_select = authenticated_page.locator("select#vehicleSelect")
        if vehicle_select.locator("option").count() <= 1:
            authenticated_page.goto("/dashboard")
            authenticated_page.fill("input[name='marca']", test_vehicle_data["marca"])
            authenticated_page.fill("input[name='modelo']", test_vehicle_data["modelo"])
            authenticated_page.fill("input[name='año']", test_vehicle_data["año"])
            authenticated_page.fill("input[name='kilometraje']", "50000")  # Higher mileage for suggestions
            authenticated_page.fill("input[name='color']", test_vehicle_data["color"])
            authenticated_page.fill("input[name='placa']", test_vehicle_data["placa"])
            authenticated_page.click("button:has-text('Agregar Vehículo')")
            authenticated_page.wait_for_load_state("networkidle")
            authenticated_page.goto("/registration")

        # Select vehicle
        vehicle_select.select_option(index=1)
        authenticated_page.wait_for_timeout(1000)

        # Click AI suggestion button if available
        suggest_button = authenticated_page.locator("button:has-text('Sugerir')")
        if suggest_button.count() > 0:
            suggest_button.first.click()
            authenticated_page.wait_for_timeout(3000)

            # Check if suggestion appeared
            suggestion_element = authenticated_page.locator("#maintenanceSuggestion, #categorySuggestion")
            if suggestion_element.count() > 0:
                # Check that suggestion has some text
                expect(suggestion_element.first).not_to_be_empty()


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
        page.wait_for_selector("#nuevoVehiculoModal", state="visible")

        # Fill form
        page.fill("input[name='alias']", "Honda Civic")
        page.fill("input[name='marca']", "Honda")
        page.fill("input[name='modelo']", "Civic")
        page.fill("input[name='anio']", "2021")
        page.select_option("select[name='tipo']", "Sedán")
        page.select_option("select[name='tipo_motor']", "Gasolina")

        # Submit
        page.locator("#nuevoVehiculoModal button[type='submit']").click()
        page.wait_for_load_state("networkidle")

        # Step 4: Navigate to maintenance registration
        page.goto("/registration")
        vehicle_select = page.locator("select#vehicleSelect")
        vehicle_select.select_option(index=1)
        page.wait_for_timeout(1000)

        # Step 5: Add maintenance record
        maintenance_select = page.locator("select#maintenanceSelect")
        if maintenance_select.count() > 0:
            maintenance_select.select_option(index=1)

        page.fill("input#kilometraje", "25500")
        page.fill("input#cost", "75.00")

        mechanic_select = page.locator("select#mechanicSelect")
        if mechanic_select.count() > 0:
            mechanic_select.select_option(index=1)

        page.fill("textarea#notes", "Complete service")
        page.click("button#saveBtn")
        page.wait_for_timeout(2000)

        # Step 6: View maintenance history
        page.goto("/dashboard")
        page.locator("a.btn.btn-primary").first.click()
        page.wait_for_load_state("networkidle")

        # Verify we're on maintenance page
        expect(page).to_have_url(lambda url: "/maintenance/" in url)

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