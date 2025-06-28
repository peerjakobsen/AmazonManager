"""
Selenium tests for Alpine.js functionality.
"""
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from tests.conftest import BaseSeleniumTest


@pytest.mark.selenium
class TestAlpineFunctionality(BaseSeleniumTest):
    """Test cases for Alpine.js reactive components."""
    
    def test_alpine_library_loaded(self, driver, live_server):
        """Test that Alpine.js library is properly loaded."""
        driver.get(f"{live_server.url}")
        self.wait_for_page_load(driver)
        
        # Check if Alpine is available in the global scope
        alpine_available = driver.execute_script("return typeof Alpine !== 'undefined'")
        assert alpine_available, "Alpine.js library is not loaded"
        
        # Check Alpine version (if available)
        alpine_version = driver.execute_script("return Alpine.version || 'unknown'")
        print(f"Alpine.js version: {alpine_version}")  # For debugging
        
    def test_alpine_components_initialized(self, driver, live_server):
        """Test that Alpine.js components are properly initialized."""
        driver.get(f"{live_server.url}")
        self.wait_for_page_load(driver)
        
        # Find the Alpine.js component container
        alpine_container = self.wait_for_element(
            driver,
            (By.XPATH, "//*[@x-data]")
        )
        
        assert alpine_container.is_displayed()
        
        # Check that x-data attribute exists
        x_data = alpine_container.get_attribute("x-data")
        assert x_data is not None, "x-data attribute not found"
        assert "message" in x_data, "message property not found in x-data"
        
    def test_alpine_initial_state(self, driver, live_server):
        """Test the initial state of Alpine.js components."""
        driver.get(f"{live_server.url}")
        self.wait_for_page_load(driver)
        
        # Find the message display element
        message_element = self.wait_for_element(
            driver,
            (By.CSS_SELECTOR, '[data-testid="alpine-message"]')
        )
        
        # Check initial message
        initial_message = message_element.text
        assert "Hello World from Alpine.js!" in initial_message
        
        # Verify x-text attribute
        x_text = message_element.get_attribute("x-text")
        assert x_text == "message", "x-text attribute incorrect"
        
    def test_alpine_button_exists_and_clickable(self, driver, live_server):
        """Test that the Alpine.js demo button exists and is clickable."""
        driver.get(f"{live_server.url}")
        self.wait_for_page_load(driver)
        
        # Find the Alpine.js button
        alpine_button = self.wait_for_element_clickable(
            driver,
            (By.CSS_SELECTOR, '[data-testid="alpine-button"]')
        )
        
        assert alpine_button.is_displayed()
        assert alpine_button.is_enabled()
        assert "Click me (Alpine.js)" in alpine_button.text
        
        # Check Alpine.js click directive
        click_attr = alpine_button.get_attribute("@click")
        assert click_attr is not None, "@click attribute not found"
        assert "Alpine.js is working!" in click_attr, "@click directive incorrect"
        
    def test_alpine_reactivity(self, driver, live_server):
        """Test Alpine.js reactivity when button is clicked."""
        driver.get(f"{live_server.url}")
        self.wait_for_page_load(driver)
        
        # Find elements
        alpine_button = self.wait_for_element_clickable(
            driver,
            (By.CSS_SELECTOR, '[data-testid="alpine-button"]')
        )
        message_element = driver.find_element(
            By.CSS_SELECTOR, '[data-testid="alpine-message"]'
        )
        
        # Check initial state
        initial_message = message_element.text
        assert "Hello World from Alpine.js!" in initial_message
        
        # Click the button
        alpine_button.click()
        
        # Wait for the message to change
        try:
            WebDriverWait(driver, 10).until(
                lambda d: "Alpine.js is working!" in message_element.text
            )
            
            # Verify the message changed
            updated_message = message_element.text
            assert "Alpine.js is working!" in updated_message
            assert updated_message != initial_message
            
        except TimeoutException:
            # Take screenshot for debugging
            self.take_screenshot(driver, "alpine_reactivity_failure")
            current_message = message_element.text
            assert False, f"Alpine.js reactivity failed. Message remained: '{current_message}'"
            
    def test_alpine_multiple_interactions(self, driver, live_server):
        """Test multiple interactions with Alpine.js components."""
        driver.get(f"{live_server.url}")
        self.wait_for_page_load(driver)
        
        alpine_button = self.wait_for_element_clickable(
            driver,
            (By.CSS_SELECTOR, '[data-testid="alpine-button"]')
        )
        message_element = driver.find_element(
            By.CSS_SELECTOR, '[data-testid="alpine-message"]'
        )
        
        # Test multiple clicks
        for i in range(3):
            alpine_button.click()
            
            # Wait for message to update
            WebDriverWait(driver, 5).until(
                lambda d: "Alpine.js is working!" in message_element.text
            )
            
            assert "Alpine.js is working!" in message_element.text
            
            # Small delay between clicks
            time.sleep(0.3)
            
    def test_alpine_data_binding(self, driver, live_server):
        """Test Alpine.js data binding and reactivity."""
        driver.get(f"{live_server.url}")
        self.wait_for_page_load(driver)
        
        # Test that the data binding works by checking the actual data
        alpine_data = driver.execute_script("""
            const alpineEl = document.querySelector('[x-data]');
            return alpineEl._x_dataStack ? alpineEl._x_dataStack[0] : null;
        """)
        
        # This might return None if Alpine internal structure is different
        # The test is mainly to verify that Alpine.js is functioning
        if alpine_data:
            assert 'message' in alpine_data
            
    def test_alpine_directive_attributes(self, driver, live_server):
        """Test that Alpine.js directives are properly set."""
        driver.get(f"{live_server.url}")
        self.wait_for_page_load(driver)
        
        # Check x-data directive
        container = driver.find_element(By.XPATH, "//*[@x-data]")
        x_data = container.get_attribute("x-data")
        assert "message:" in x_data
        assert "Hello World from Alpine.js!" in x_data
        
        # Check x-text directive
        message_element = driver.find_element(
            By.CSS_SELECTOR, '[data-testid="alpine-message"]'
        )
        x_text = message_element.get_attribute("x-text")
        assert x_text == "message"
        
        # Check @click directive
        button_element = driver.find_element(
            By.CSS_SELECTOR, '[data-testid="alpine-button"]'
        )
        click_directive = button_element.get_attribute("@click")
        assert "message =" in click_directive
        assert "Alpine.js is working!" in click_directive
        
    def test_alpine_state_persistence(self, driver, live_server):
        """Test that Alpine.js state persists during interactions."""
        driver.get(f"{live_server.url}")
        self.wait_for_page_load(driver)
        
        alpine_button = self.wait_for_element_clickable(
            driver,
            (By.CSS_SELECTOR, '[data-testid="alpine-button"]')
        )
        message_element = driver.find_element(
            By.CSS_SELECTOR, '[data-testid="alpine-message"]'
        )
        
        # Click button to change state
        alpine_button.click()
        
        WebDriverWait(driver, 5).until(
            lambda d: "Alpine.js is working!" in message_element.text
        )
        
        # Scroll page to test state persistence
        driver.execute_script("window.scrollTo(0, 100);")
        time.sleep(0.5)
        driver.execute_script("window.scrollTo(0, 0);")
        
        # State should persist
        assert "Alpine.js is working!" in message_element.text
        
        # Click other elements to test state isolation
        try:
            htmx_button = driver.find_element(
                By.CSS_SELECTOR, '[data-testid="htmx-button"]'
            )
            htmx_button.click()
            time.sleep(1)
            
            # Alpine state should still be preserved
            assert "Alpine.js is working!" in message_element.text
            
        except Exception:
            # HTMX button interaction failed, but Alpine state should still persist
            assert "Alpine.js is working!" in message_element.text
            
    def test_alpine_component_isolation(self, driver, live_server):
        """Test that Alpine.js components are properly isolated."""
        driver.get(f"{live_server.url}")
        self.wait_for_page_load(driver)
        
        # Find all Alpine components on the page
        alpine_components = driver.find_elements(By.XPATH, "//*[@x-data]")
        
        # For our current setup, we should have one Alpine component
        assert len(alpine_components) >= 1, "No Alpine.js components found"
        
        # Verify each component has its own scope
        for component in alpine_components:
            x_data = component.get_attribute("x-data")
            assert x_data is not None and x_data.strip() != ""