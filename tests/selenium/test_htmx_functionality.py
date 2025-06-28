"""
Selenium tests for HTMX functionality.
"""
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from tests.conftest import BaseSeleniumTest


@pytest.mark.selenium
class TestHTMXFunctionality(BaseSeleniumTest):
    """Test cases for HTMX dynamic content loading."""
    
    def test_htmx_library_loaded(self, driver, live_server):
        """Test that HTMX library is properly loaded."""
        driver.get(f"{live_server.url}")
        self.wait_for_page_load(driver)
        
        # Check if HTMX is available in the global scope
        htmx_available = driver.execute_script("return typeof htmx !== 'undefined'")
        assert htmx_available, "HTMX library is not loaded"
        
        # Check HTMX version (if available)
        htmx_version = driver.execute_script("return htmx.version || 'unknown'")
        assert htmx_version != 'unknown', "HTMX version not available"
        
    def test_htmx_button_exists_and_clickable(self, driver, live_server):
        """Test that the HTMX demo button exists and is clickable."""
        driver.get(f"{live_server.url}")
        self.wait_for_page_load(driver)
        
        # Find the HTMX button
        htmx_button = self.wait_for_element_clickable(
            driver,
            (By.CSS_SELECTOR, '[data-testid="htmx-button"]')
        )
        
        assert htmx_button.is_displayed()
        assert htmx_button.is_enabled()
        assert "Load Content (HTMX)" in htmx_button.text
        
        # Check HTMX attributes
        hx_get = htmx_button.get_attribute("hx-get")
        hx_target = htmx_button.get_attribute("hx-target")
        hx_swap = htmx_button.get_attribute("hx-swap")
        
        assert hx_get is not None, "hx-get attribute not found"
        assert hx_target == "#htmx-result", "hx-target attribute incorrect"
        assert hx_swap == "innerHTML", "hx-swap attribute incorrect"
        
    def test_htmx_result_container_exists(self, driver, live_server):
        """Test that the HTMX result container exists."""
        driver.get(f"{live_server.url}")
        self.wait_for_page_load(driver)
        
        # Find the result container
        result_container = self.wait_for_element(
            driver,
            (By.CSS_SELECTOR, '[data-testid="htmx-result"]')
        )
        
        assert result_container.is_displayed()
        assert result_container.get_attribute("id") == "htmx-result"
        
        # Initially should be empty
        assert result_container.text.strip() == ""
        
    def test_htmx_content_loading(self, driver, live_server):
        """Test that HTMX loads content dynamically when button is clicked."""
        driver.get(f"{live_server.url}")
        self.wait_for_page_load(driver)
        
        # Find elements
        htmx_button = self.wait_for_element_clickable(
            driver,
            (By.CSS_SELECTOR, '[data-testid="htmx-button"]')
        )
        result_container = driver.find_element(
            By.CSS_SELECTOR, '[data-testid="htmx-result"]'
        )
        
        # Verify initial state
        assert result_container.text.strip() == ""
        
        # Click the button
        htmx_button.click()
        
        # Wait for content to load (HTMX should populate the result)
        try:
            self.wait_for_text_in_element(
                driver,
                (By.CSS_SELECTOR, '[data-testid="htmx-result"]'),
                "HTMX is working!",
                timeout=10
            )
            
            # Verify the content was loaded
            assert "HTMX is working!" in result_container.text
            
        except TimeoutException:
            # Take screenshot for debugging
            self.take_screenshot(driver, "htmx_load_failure")
            
            # Check if there was an error
            error_text = result_container.text
            assert False, f"HTMX content failed to load. Container text: '{error_text}'"
            
    def test_htmx_multiple_clicks(self, driver, live_server):
        """Test that HTMX works correctly with multiple button clicks."""
        driver.get(f"{live_server.url}")
        self.wait_for_page_load(driver)
        
        htmx_button = self.wait_for_element_clickable(
            driver,
            (By.CSS_SELECTOR, '[data-testid="htmx-button"]')
        )
        result_container = driver.find_element(
            By.CSS_SELECTOR, '[data-testid="htmx-result"]'
        )
        
        # Click multiple times to test consistency
        for i in range(3):
            htmx_button.click()
            
            # Wait for content to load
            self.wait_for_text_in_element(
                driver,
                (By.CSS_SELECTOR, '[data-testid="htmx-result"]'),
                "HTMX is working!",
                timeout=5
            )
            
            assert "HTMX is working!" in result_container.text
            
            # Small delay between clicks
            time.sleep(0.5)
            
    def test_htmx_request_attributes(self, driver, live_server):
        """Test HTMX request attributes and behavior."""
        driver.get(f"{live_server.url}")
        self.wait_for_page_load(driver)
        
        htmx_button = driver.find_element(
            By.CSS_SELECTOR, '[data-testid="htmx-button"]'
        )
        
        # Test that HTMX attributes are properly set
        attributes = {
            'hx-get': '/htmx-demo/',
            'hx-target': '#htmx-result',
            'hx-swap': 'innerHTML'
        }
        
        for attr, expected_value in attributes.items():
            actual_value = htmx_button.get_attribute(attr)
            assert actual_value == expected_value, f"{attr} mismatch: expected {expected_value}, got {actual_value}"
            
    def test_htmx_loading_states(self, driver, live_server):
        """Test HTMX loading states and indicators."""
        driver.get(f"{live_server.url}")
        self.wait_for_page_load(driver)
        
        htmx_button = self.wait_for_element_clickable(
            driver,
            (By.CSS_SELECTOR, '[data-testid="htmx-button"]')
        )
        
        # Monitor for HTMX loading class (if implemented)
        # HTMX typically adds 'htmx-request' class during requests
        original_classes = htmx_button.get_attribute("class")
        
        htmx_button.click()
        
        # Check if loading indicator appears (briefly)
        # Note: This might be too fast to catch reliably in all environments
        try:
            WebDriverWait(driver, 1).until(
                lambda d: "htmx-request" in htmx_button.get_attribute("class")
            )
        except TimeoutException:
            # Loading state might be too brief to catch, which is acceptable
            pass
            
        # Wait for request to complete
        self.wait_for_text_in_element(
            driver,
            (By.CSS_SELECTOR, '[data-testid="htmx-result"]'),
            "HTMX is working!",
            timeout=10
        )
        
        # Verify loading class is removed after completion
        final_classes = htmx_button.get_attribute("class")
        assert "htmx-request" not in final_classes
        
    def test_htmx_error_handling(self, driver, live_server):
        """Test HTMX error handling with invalid requests."""
        driver.get(f"{live_server.url}")
        self.wait_for_page_load(driver)
        
        # Inject a button with invalid HTMX URL for testing
        driver.execute_script("""
            var button = document.createElement('button');
            button.setAttribute('hx-get', '/invalid-url/');
            button.setAttribute('hx-target', '[data-testid="htmx-result"]');
            button.setAttribute('data-testid', 'htmx-error-button');
            button.textContent = 'Error Test Button';
            document.body.appendChild(button);
            htmx.process(button);
        """)
        
        error_button = driver.find_element(
            By.CSS_SELECTOR, '[data-testid="htmx-error-button"]'
        )
        result_container = driver.find_element(
            By.CSS_SELECTOR, '[data-testid="htmx-result"]'
        )
        
        # Click the error button
        error_button.click()
        
        # Wait a moment for the request to fail
        time.sleep(2)
        
        # HTMX should handle the error gracefully (content should remain unchanged)
        # The exact behavior depends on HTMX configuration and error handling
        # For now, we just verify the page doesn't crash
        assert driver.current_url == f"{live_server.url}/"