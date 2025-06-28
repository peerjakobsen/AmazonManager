"""
Pytest configuration and fixtures for the Amazon Manager project.
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import os


def pytest_addoption(parser):
    """Add command line options for pytest."""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests on: chrome, firefox, headless-chrome"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode"
    )


@pytest.fixture(scope="session")
def browser_name(request):
    """Get browser name from command line."""
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def headless_mode(request):
    """Get headless mode setting from command line."""
    return request.config.getoption("--headless")


@pytest.fixture(scope="function")
def driver(browser_name, headless_mode):
    """
    Create a WebDriver instance based on browser selection.
    Uses function scope to ensure each test gets a fresh browser instance.
    """
    driver_instance = None
    
    try:
        if browser_name.lower() == "chrome" or browser_name.lower() == "headless-chrome":
            options = ChromeOptions()
            
            # Configure Chrome options
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            
            if headless_mode or browser_name.lower() == "headless-chrome":
                options.add_argument("--headless=new")
            
            driver_instance = webdriver.Chrome(options=options)
            
        elif browser_name.lower() == "firefox":
            options = FirefoxOptions()
            
            if headless_mode:
                options.add_argument("--headless")
                
            driver_instance = webdriver.Firefox(options=options)
            
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")
            
        # Configure implicit wait
        driver_instance.implicitly_wait(10)
        
        # Maximize window for consistent behavior
        driver_instance.maximize_window()
        
        yield driver_instance
        
    finally:
        if driver_instance:
            driver_instance.quit()


@pytest.fixture(scope="function")
def wait(driver):
    """Create WebDriverWait instance for explicit waits."""
    return WebDriverWait(driver, 20)


# We'll use pytest-django's built-in live_server fixture instead of defining our own


@pytest.fixture(scope="function")
def page_elements():
    """Common page element selectors."""
    return {
        'homepage': {
            'title': '[data-testid="page-title"]',
            'welcome_message': '[data-testid="welcome-message"]',
            'alpine_button': '[data-testid="alpine-button"]',
            'alpine_message': '[data-testid="alpine-message"]',
            'htmx_button': '[data-testid="htmx-button"]',
            'htmx_result': '[data-testid="htmx-result"]',
        }
    }


@pytest.fixture(scope="function")
def test_user():
    """Create a test user for authentication tests."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpassword123'
    )
    
    yield user
    
    # Cleanup
    user.delete()


class BaseSeleniumTest:
    """
    Base class for Selenium tests with common utilities.
    """
    
    def wait_for_element(self, driver, locator, timeout=20):
        """Wait for element to be present and visible."""
        wait = WebDriverWait(driver, timeout)
        return wait.until(
            EC.presence_of_element_located(locator)
        )
    
    def wait_for_element_clickable(self, driver, locator, timeout=20):
        """Wait for element to be clickable."""
        wait = WebDriverWait(driver, timeout)
        return wait.until(
            EC.element_to_be_clickable(locator)
        )
    
    def wait_for_text_in_element(self, driver, locator, text, timeout=20):
        """Wait for specific text to appear in element."""
        wait = WebDriverWait(driver, timeout)
        return wait.until(
            EC.text_to_be_present_in_element(locator, text)
        )
    
    def take_screenshot(self, driver, name="screenshot"):
        """Take a screenshot for debugging."""
        import datetime
        screenshots_dir = "test_screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)
        
        # Add timestamp to screenshot name for uniqueness
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{screenshots_dir}/{name}_{timestamp}.png"
        
        # Take full page screenshot if possible
        try:
            driver.save_screenshot(filename)
            print(f"Screenshot saved: {filename}")
        except Exception as e:
            print(f"Failed to take screenshot: {e}")
            
        return filename
    
    def take_element_screenshot(self, driver, element, name="element_screenshot"):
        """Take a screenshot of a specific element."""
        import datetime
        screenshots_dir = "test_screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{screenshots_dir}/{name}_{timestamp}.png"
        
        try:
            element.screenshot(filename)
            print(f"Element screenshot saved: {filename}")
        except Exception as e:
            print(f"Failed to take element screenshot: {e}")
            
        return filename
    
    def scroll_to_element(self, driver, element):
        """Scroll element into view."""
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
    
    def wait_for_page_load(self, driver, timeout=30):
        """Wait for page to finish loading."""
        wait = WebDriverWait(driver, timeout)
        wait.until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture screenshot on test failure."""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        # Get the driver from the test if available
        if hasattr(item, 'funcargs') and 'driver' in item.funcargs:
            driver = item.funcargs['driver']
            
            # Create screenshots directory
            screenshots_dir = "test_screenshots"
            os.makedirs(screenshots_dir, exist_ok=True)
            
            # Generate screenshot filename
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = item.nodeid.replace("::", "_").replace("/", "_")
            filename = f"{screenshots_dir}/FAILED_{test_name}_{timestamp}.png"
            
            try:
                driver.save_screenshot(filename)
                print(f"\n📸 Failure screenshot saved: {filename}")
                
                # Also capture page source for debugging
                source_filename = f"{screenshots_dir}/FAILED_{test_name}_{timestamp}_source.html"
                with open(source_filename, 'w', encoding='utf-8') as f:
                    f.write(driver.page_source)
                print(f"📄 Page source saved: {source_filename}")
                
            except Exception as e:
                print(f"Failed to capture failure screenshot: {e}")


@pytest.fixture(scope="function", autouse=True)
def auto_screenshot_on_steps(request):
    """Automatically take screenshots at key test steps."""
    # Check if this test uses the driver fixture
    if 'driver' not in request.fixturenames:
        yield
        return
        
    driver = request.getfixturevalue('driver')
    
    # Take screenshot at test start
    test_name = request.node.name
    base_test = BaseSeleniumTest()
    base_test.take_screenshot(driver, f"START_{test_name}")
    
    yield
    
    # Take screenshot at test end (success)
    base_test.take_screenshot(driver, f"END_{test_name}")