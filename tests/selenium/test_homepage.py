"""
Selenium tests for the homepage functionality.
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.conftest import BaseSeleniumTest


@pytest.mark.selenium
class TestHomepage(BaseSeleniumTest):
    """Test cases for the homepage functionality."""
    
    def test_homepage_loads_successfully(self, driver, live_server):
        """Test that the homepage loads without errors."""
        # Navigate to homepage
        driver.get(f"{live_server.url}")
        
        # Wait for page to load completely
        self.wait_for_page_load(driver)
        
        # Verify page title is correct
        assert "Amazon Manager" in driver.title
        
        # Verify main heading is present
        title_element = self.wait_for_element(
            driver, 
            (By.CSS_SELECTOR, '[data-testid="page-title"]')
        )
        assert title_element.is_displayed()
        assert "Amazon Manager" in title_element.text
        
    def test_homepage_content_structure(self, driver, live_server):
        """Test that all main content sections are present."""
        driver.get(f"{live_server.url}")
        self.wait_for_page_load(driver)
        
        # Check for welcome message
        welcome_element = self.wait_for_element(
            driver,
            (By.CSS_SELECTOR, '[data-testid="welcome-message"]')
        )
        assert welcome_element.is_displayed()
        assert "Welcome to Amazon Manager" in welcome_element.text
        
        # Check for Alpine.js demo section
        alpine_button = self.wait_for_element(
            driver,
            (By.CSS_SELECTOR, '[data-testid="alpine-button"]')
        )
        assert alpine_button.is_displayed()
        
        # Check for HTMX demo section
        htmx_button = self.wait_for_element(
            driver,
            (By.CSS_SELECTOR, '[data-testid="htmx-button"]')
        )
        assert htmx_button.is_displayed()
        
    def test_page_responsive_design(self, driver, live_server):
        """Test that the page adapts to different screen sizes."""
        driver.get(f"{live_server.url}")
        self.wait_for_page_load(driver)
        
        # Test desktop size (default)
        title_element = driver.find_element(By.CSS_SELECTOR, '[data-testid="page-title"]')
        assert title_element.is_displayed()
        
        # Test mobile size
        driver.set_window_size(375, 667)  # iPhone size
        assert title_element.is_displayed()
        
        # Test tablet size
        driver.set_window_size(768, 1024)  # iPad size
        assert title_element.is_displayed()
        
        # Reset to desktop size
        driver.maximize_window()
        
    def test_tailwind_css_styling(self, driver, live_server):
        """Test that Tailwind CSS classes are applied correctly."""
        driver.get(f"{live_server.url}")
        self.wait_for_page_load(driver)
        
        # Check that Tailwind CSS is loaded by verifying computed styles
        title_element = driver.find_element(By.CSS_SELECTOR, '[data-testid="page-title"]')
        
        # Get computed styles
        font_size = driver.execute_script(
            "return window.getComputedStyle(arguments[0]).fontSize", 
            title_element
        )
        
        # Tailwind's text-4xl should result in a large font size
        assert font_size is not None
        # Convert to pixels and check it's reasonably large (expecting ~36px for text-4xl)
        font_size_px = float(font_size.replace('px', ''))
        assert font_size_px > 30, f"Font size too small: {font_size_px}px"
        
    def test_page_accessibility_features(self, driver, live_server):
        """Test basic accessibility features."""
        driver.get(f"{live_server.url}")
        self.wait_for_page_load(driver)
        
        # Check that main heading has proper structure
        title_element = driver.find_element(By.CSS_SELECTOR, '[data-testid="page-title"]')
        assert title_element.tag_name.lower() == "h1"
        
        # Check that buttons have proper attributes
        alpine_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="alpine-button"]')
        htmx_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="htmx-button"]')
        
        assert alpine_button.tag_name.lower() == "button"
        assert htmx_button.tag_name.lower() == "button"
        
        # Check that buttons have text content
        assert alpine_button.text.strip() != ""
        assert htmx_button.text.strip() != ""
        
    def test_page_performance_metrics(self, driver, live_server):
        """Test basic performance metrics."""
        driver.get(f"{live_server.url}")
        
        # Measure page load time using Navigation Timing API
        load_time = driver.execute_script("""
            var performance = window.performance;
            var timing = performance.timing;
            return timing.loadEventEnd - timing.navigationStart;
        """)
        
        # Page should load within reasonable time (5 seconds)
        assert load_time < 5000, f"Page load time too slow: {load_time}ms"
        
        # Check that external resources are loaded
        scripts = driver.find_elements(By.TAG_NAME, "script")
        assert len(scripts) > 0, "No scripts found on page"
        
        # Verify HTMX and Alpine.js are loaded
        htmx_loaded = driver.execute_script("return typeof htmx !== 'undefined'")
        alpine_loaded = driver.execute_script("return typeof Alpine !== 'undefined'")
        
        assert htmx_loaded, "HTMX library not loaded"
        assert alpine_loaded, "Alpine.js library not loaded"