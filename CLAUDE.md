# AmazonManager - Claude Memory

## Project Overview
AmazonManager is a Django-based Amazon business management application designed to help users manage their Amazon business operations effectively.

## Technology Stack

### Backend Framework
- **Django**: Web framework for Python providing rapid development capabilities
- **Wagtail CMS**: Powerful, flexible content management system built on Django
  - Installation: `pip install wagtail`
  - Getting started: `wagtail start mysite`
  - Features: Page management, admin interface, rich content editing

### Frontend Technologies
- **HTMX**: High-power tools for HTML enabling modern web interactions without complex JavaScript
  - Installation via CDN: `<script src="https://unpkg.com/htmx.org@2.0.5/dist/htmx.min.js"></script>`
  - Key attributes: `hx-get`, `hx-post`, `hx-swap`, `hx-target`
  - Django integration: Works seamlessly with Django templates and views
  - Best practices: Use relative URLs, implement CSRF protection

- **Alpine.js**: Rugged, minimal framework for composing JavaScript behavior in markup
  - Installation via CDN: `<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>`
  - Installation via NPM: `npm install alpinejs`
  - Key directives: `x-data`, `x-text`, `x-show`, `x-on`, `x-model`, `x-init`
  - Perfect for reactive components and state management

### Architecture Pattern
This project follows a modern "hypermedia-driven" approach:
- **HTMX** handles server-side rendering and dynamic content updates
- **Alpine.js** provides client-side interactivity and component state
- **Wagtail** manages content and provides admin capabilities
- **Django** serves as the robust backend framework

### Key Integration Points
1. **Django + HTMX**: Server-side templates with dynamic partial updates
2. **HTMX + Alpine.js**: Server-driven content with client-side enhancements
3. **Wagtail + Django**: CMS functionality integrated with custom business logic

### Development Setup
1. Create virtual environment
2. Install Django and Wagtail: `pip install django wagtail`
3. Create project: `wagtail start amazonmanager`
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Create superuser: `python manage.py createsuperuser`
7. Start server: `python manage.py runserver`

### Frontend Asset Management
- Include HTMX and Alpine.js via CDN for rapid development
- Consider NPM installation for production builds
- HTMX should be loaded before Alpine.js
- Use `defer` attribute for script loading

### Testing Strategy
- **Django Unit Tests**: Built-in Django testing framework for models, views, and forms
- **Selenium Integration Tests**: Browser automation for end-to-end testing
- **pytest**: Modern testing framework with fixtures and plugins
- **Test Database**: Automatic test database creation and cleanup

## Testing Framework & Best Practices

### Selenium Testing Setup

#### Dependencies
```bash
pip install selenium pytest-django
```

#### Browser Support
- **Chrome/Chromium**: Primary browser for testing (with headless support)
- **Firefox**: Secondary browser support
- **Headless Mode**: For CI/CD environments and faster test execution

#### Test Structure
```
tests/
├── __init__.py
├── conftest.py              # pytest configuration and fixtures
├── selenium/
│   ├── __init__.py
│   ├── test_homepage.py     # Homepage functionality tests
│   ├── test_htmx_functionality.py    # HTMX dynamic content tests
│   └── test_alpine_functionality.py  # Alpine.js reactivity tests
└── unit/                    # Unit tests (if needed)
```

### Selenium Best Practices

#### 1. **Reliable Element Selection**
- Use `data-testid` attributes for test-specific element identification
- Avoid CSS selectors that depend on styling classes
- Prefer semantic selectors when possible

```html
<!-- Good -->
<button data-testid="alpine-button" @click="message = 'Alpine.js is working!'">
    Click me (Alpine.js)
</button>

<!-- Avoid -->
<button class="mt-2 px-4 py-2 bg-blue-500">Click me</button>
```

#### 2. **Explicit Waits Over Implicit Waits**
- Use `WebDriverWait` with expected conditions
- Set reasonable timeout values (typically 10-20 seconds)
- Avoid `time.sleep()` except for specific timing requirements

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Good
wait = WebDriverWait(driver, 20)
element = wait.until(EC.element_to_be_clickable((By.ID, "submit-button")))

# Avoid
driver.implicitly_wait(10)  # Less reliable
time.sleep(5)  # Inflexible
```

#### 3. **Page Object Model (POM)**
- Encapsulate page interactions in dedicated classes
- Separate test logic from page-specific code
- Improve maintainability and reusability

```python
class HomePage:
    def __init__(self, driver):
        self.driver = driver
        
    def click_alpine_button(self):
        button = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="alpine-button"]')
        button.click()
        
    def get_alpine_message(self):
        return self.driver.find_element(By.CSS_SELECTOR, '[data-testid="alpine-message"]').text
```

#### 4. **Test Data Management**
- Use fixtures for consistent test data setup
- Clean up test data after each test
- Use Django's test database features

```python
@pytest.fixture
def test_user():
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = User.objects.create_user(username='testuser', password='testpass')
    yield user
    user.delete()  # Cleanup
```

#### 5. **Error Handling and Debugging**
- Implement screenshot capture on test failures
- Use try-catch blocks for better error messages
- Log relevant information for debugging

```python
def test_alpine_reactivity(self, driver, live_server):
    try:
        # Test logic here
        pass
    except TimeoutException:
        self.take_screenshot(driver, "alpine_reactivity_failure")
        assert False, f"Alpine.js reactivity failed. Current message: '{current_message}'"
```

#### 6. **Cross-Browser Testing**
- Support multiple browsers through command-line options
- Use headless mode for CI/CD pipelines
- Configure browser-specific options

```bash
# Run tests with different browsers
pytest --browser=chrome tests/selenium/
pytest --browser=firefox tests/selenium/
pytest --browser=headless-chrome tests/selenium/
```

#### 7. **Performance Considerations**
- Use function-scoped fixtures for driver instances
- Implement parallel test execution when possible
- Monitor test execution time and optimize slow tests

#### 8. **CI/CD Integration**
- Use headless browsers in CI environments
- Configure proper timeouts for CI systems
- Generate test reports and artifacts

```yaml
# Example GitHub Actions configuration
- name: Run Selenium Tests
  run: |
    pytest tests/selenium/ --browser=headless-chrome --html=report.html
```

#### 9. **Test Organization**
- Group related tests in classes with descriptive names
- Use pytest markers for test categorization
- Implement proper test isolation

```python
@pytest.mark.selenium
@pytest.mark.slow
class TestHTMXFunctionality:
    """Test cases for HTMX dynamic content loading."""
```

#### 10. **Wagtail CMS Testing**
- Test content management workflows
- Verify page publishing and preview functionality
- Test admin interface interactions

### Running Tests

#### Basic Test Execution
```bash
# Run all tests
pytest

# Run only Selenium tests
pytest -m selenium

# Run with specific browser
pytest --browser=chrome tests/selenium/

# Run in headless mode
pytest --headless tests/selenium/

# Generate HTML report
pytest --html=report.html tests/selenium/
```

#### Test Configuration
The project uses `pytest.ini` for configuration:
- Django settings module configuration
- Test discovery patterns
- Custom markers for test categorization
- Output formatting options

### Testing HTMX Integration
- Verify HTMX library loading
- Test dynamic content updates
- Validate request/response cycles
- Check error handling

### Testing Alpine.js Integration
- Confirm Alpine.js initialization
- Test reactive data binding
- Validate component interactions
- Verify state management

## Repository Information
- **GitHub URL**: https://github.com/peerjakobsen/AmazonManager
- **Initial commit**: Comprehensive Django .gitignore file
- **Branch**: main