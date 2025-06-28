"""
Comprehensive Selenium test with extensive screenshot capture.
"""
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.conftest import BaseSeleniumTest


@pytest.mark.selenium
class TestFullDemoWithScreenshots(BaseSeleniumTest):
    """Comprehensive test with screenshot documentation."""
    
    def test_complete_homepage_workflow_with_screenshots(self, driver, live_server):
        """Test the complete homepage workflow with detailed screenshots."""
        
        # Step 1: Navigate to homepage
        print("🔍 Step 1: Navigating to homepage...")
        driver.get(f"{live_server.url}")
        self.wait_for_page_load(driver)
        self.take_screenshot(driver, "01_homepage_loaded")
        
        # Step 2: Verify page structure
        print("🔍 Step 2: Verifying page structure...")
        title_element = self.wait_for_element(
            driver, 
            (By.CSS_SELECTOR, '[data-testid="page-title"]')
        )
        assert "Amazon Manager" in title_element.text
        self.take_screenshot(driver, "02_page_structure_verified")
        
        # Step 3: Capture Alpine.js demo section
        print("🔍 Step 3: Testing Alpine.js functionality...")
        alpine_button = self.wait_for_element_clickable(
            driver,
            (By.CSS_SELECTOR, '[data-testid="alpine-button"]')
        )
        alpine_message = driver.find_element(
            By.CSS_SELECTOR, '[data-testid="alpine-message"]'
        )
        
        # Take screenshot of Alpine section
        self.take_element_screenshot(driver, alpine_button, "03_alpine_button_before_click")
        
        # Check initial Alpine.js state
        initial_message = alpine_message.text
        assert "Hello World from Alpine.js!" in initial_message
        self.take_screenshot(driver, "04_alpine_initial_state")
        
        # Click Alpine.js button
        print("🔍 Step 4: Clicking Alpine.js button...")
        alpine_button.click()
        
        # Wait for Alpine.js to update
        WebDriverWait(driver, 10).until(
            lambda d: "Alpine.js is working!" in alpine_message.text
        )
        
        # Capture Alpine.js updated state
        self.take_screenshot(driver, "05_alpine_after_click")
        self.take_element_screenshot(driver, alpine_message, "06_alpine_message_updated")
        
        # Step 5: Test HTMX functionality
        print("🔍 Step 5: Testing HTMX functionality...")
        htmx_button = driver.find_element(
            By.CSS_SELECTOR, '[data-testid="htmx-button"]'
        )
        htmx_result = driver.find_element(
            By.CSS_SELECTOR, '[data-testid="htmx-result"]'
        )
        
        # Take screenshot before HTMX interaction
        self.take_element_screenshot(driver, htmx_button, "07_htmx_button_before_click")
        
        # Verify HTMX result is initially empty
        assert htmx_result.text.strip() == ""
        self.take_screenshot(driver, "08_htmx_initial_state")
        
        # Click HTMX button
        print("🔍 Step 6: Clicking HTMX button...")
        htmx_button.click()
        
        # Wait for HTMX to load content
        self.wait_for_text_in_element(
            driver,
            (By.CSS_SELECTOR, '[data-testid="htmx-result"]'),
            "HTMX is working!",
            timeout=10
        )
        
        # Capture HTMX updated state
        self.take_screenshot(driver, "09_htmx_after_click")
        self.take_element_screenshot(driver, htmx_result, "10_htmx_result_loaded")
        
        # Step 7: Test multiple interactions
        print("🔍 Step 7: Testing multiple interactions...")
        
        # Click Alpine.js button again
        alpine_button.click()
        time.sleep(0.5)
        self.take_screenshot(driver, "11_alpine_second_click")
        
        # Click HTMX button again
        htmx_button.click()
        time.sleep(1)
        self.take_screenshot(driver, "12_htmx_second_click")
        
        # Step 8: Test responsive behavior
        print("🔍 Step 8: Testing responsive design...")
        
        # Test mobile view
        driver.set_window_size(375, 667)  # iPhone size
        time.sleep(0.5)
        self.take_screenshot(driver, "13_mobile_view")
        
        # Test tablet view
        driver.set_window_size(768, 1024)  # iPad size
        time.sleep(0.5)
        self.take_screenshot(driver, "14_tablet_view")
        
        # Return to desktop view
        driver.maximize_window()
        time.sleep(0.5)
        self.take_screenshot(driver, "15_desktop_view_restored")
        
        # Step 9: Scroll behavior test
        print("🔍 Step 9: Testing scroll behavior...")
        
        # Scroll to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
        self.take_screenshot(driver, "16_scrolled_to_bottom")
        
        # Scroll to top
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.5)
        self.take_screenshot(driver, "17_scrolled_to_top")
        
        # Step 10: Final verification
        print("🔍 Step 10: Final verification...")
        
        # Verify all elements are still functional
        assert "Alpine.js is working!" in alpine_message.text
        assert "HTMX is working!" in htmx_result.text
        
        # Take final screenshot
        self.take_screenshot(driver, "18_final_verification_complete")
        
        print("✅ Complete workflow test with screenshots finished successfully!")
        
    def test_error_scenarios_with_screenshots(self, driver, live_server):
        """Test error scenarios and capture screenshots."""
        
        print("🔍 Testing error scenarios...")
        
        # Navigate to homepage
        driver.get(f"{live_server.url}")
        self.wait_for_page_load(driver)
        self.take_screenshot(driver, "error_test_01_homepage")
        
        # Test JavaScript console errors
        logs = driver.get_log('browser')
        console_errors = [log for log in logs if log['level'] == 'SEVERE']
        
        self.take_screenshot(driver, "error_test_02_console_check")
        
        # Navigate to non-existent page
        driver.get(f"{live_server.url}/non-existent-page/")
        self.take_screenshot(driver, "error_test_03_404_page")
        
        # Go back to homepage
        driver.get(f"{live_server.url}")
        self.wait_for_page_load(driver)
        self.take_screenshot(driver, "error_test_04_back_to_homepage")
        
        print("✅ Error scenarios test completed!")
        
    def test_performance_with_screenshots(self, driver, live_server):
        """Test performance metrics and capture screenshots."""
        
        print("🔍 Testing performance...")
        
        # Navigate and measure load time
        start_time = time.time()
        driver.get(f"{live_server.url}")
        self.wait_for_page_load(driver)
        load_time = time.time() - start_time
        
        self.take_screenshot(driver, f"perf_01_loaded_in_{load_time:.2f}s")
        
        # Check if libraries are loaded
        htmx_loaded = driver.execute_script("return typeof htmx !== 'undefined'")
        alpine_loaded = driver.execute_script("return typeof Alpine !== 'undefined'")
        
        # Take screenshot showing performance metrics in console
        driver.execute_script("""
            console.log('HTMX Loaded:', typeof htmx !== 'undefined');
            console.log('Alpine Loaded:', typeof Alpine !== 'undefined');
            console.log('Load Time:', arguments[0] + 's');
        """, f"{load_time:.2f}")
        
        self.take_screenshot(driver, "perf_02_libraries_loaded")
        
        assert htmx_loaded, "HTMX should be loaded"
        assert alpine_loaded, "Alpine.js should be loaded"
        assert load_time < 10, f"Page should load within 10 seconds, took {load_time:.2f}s"
        
        print(f"✅ Performance test completed! Load time: {load_time:.2f}s")