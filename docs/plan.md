# AQA Home Test - Plan for WAP Testing (Twitch) ✅

## Repository 📁
`aqa-wap-test`

## Goal 📌
Automate a mobile web scenario on Twitch using Selenium in Python.

## Framework Architecture 🏗️

### Design Patterns
- **Page Object Model (POM)** - Encapsulate page elements and actions
- **Fluent Interface** - Chain methods for better readability (e.g., `home_page.search("StarCraft II").scroll_down().click_streamer()`)
- **Factory Pattern** - For driver initialization across different devices/browsers

### Project Structure
```
aqa-wap-test/
├── config/
│   ├── config.py           # Environment configuration
│   └── devices.json        # Mobile device definitions
├── pages/
│   ├── base_page.py        # Base page with common methods
│   ├── home_page.py
│   ├── search_page.py
│   └── streamer_page.py
├── tests/
│   ├── conftest.py         # Pytest fixtures
│   ├── test_twitch.py      # Test cases
│   └── features/           # BDD features (optional)
│       ├── twitch.feature
│       └── steps/
│           └── twitch_steps.py
├── utils/
│   ├── driver_factory.py   # WebDriver setup/teardown
│   ├── logging_utils.py    # Custom logging
│   └── waits.py            # Custom wait methods
├── data/                   # Test data files
│   └── search_queries.json
├── reports/
│   └── screenshots/        # Test execution artifacts
├── requirements.txt
└── README.md
```

## Steps to Implement ✅

### 1. Initialize the Project
- Create GitHub repo: `aqa-wap-test`
- Create virtual environment and install:
  - selenium
  - pytest
  - pytest-html (for reports)
  - python-dotenv (optional)
  - allure-pytest (for enhanced reporting)
  - webdriver-manager (for driver management)
  - pytest-bdd (optional, for BDD integration)
- Create folders: 
  - `pages/` 
  - `tests/` 
  - `reports/screenshots/` 
  - `config/`
  - `utils/`
  - `data/`

### 2. Configure Chrome Mobile Emulation
- Set up ChromeOptions in Selenium to emulate a mobile device (e.g. Pixel 2)
- Create device configurations in JSON for easy maintenance
- Implement driver factory pattern for scalability

### 3. Create Base Page Class
- Utilities for:
  - click (with multiple strategies: JS, Action chains)
  - find_element (with flexible wait strategies)
  - input_text
  - scroll_page (various scrolling methods)
  - handle_popup
  - take_screenshot
  - Custom explicit waits (element visible, clickable, etc.)
  - Logging of all page actions

### 4. Create Page Object(s)
- TwitchHomePage
- SearchResultsPage
- StreamerPage
- Implement fluent interface for method chaining

### 5. Write Test Case Using Pytest
Steps:
- Go to Twitch mobile site
- Click search
- Enter "StarCraft II"
- Scroll down twice
- Click any streamer
- Handle modal popup (if present)
- Wait for video to load
- Take a screenshot

### 6. Add Logging & Error Handling
- Configure Python's logging module
- Create custom exception handling for better debugging
- Log all test steps with appropriate detail level
- Implement retry mechanism for flaky elements

### 7. Create Test Execution Helpers
- Pytest fixtures for setup/teardown
- Parametrization for potential test variations
- Custom markers for test categorization
- Implement screenshot capture on test failure

### 8. Generate GIF of Test Execution
- Use LICEcap or ScreenToGif

### 9. Create README
- Short project intro
- Embedded GIF
- Tech stack + folder structure
- Setup instructions
- Test execution commands
- Design principles explanation
- Examples of extending the framework

### 10. Push to GitHub & Send Link

## Framework Extension Points 🔄

### 1. Device/Browser Management
**Description**: The framework supports configuring and running tests on different devices and browsers without code changes.

**Implementation**:
- Device configurations stored in `config/devices.json`:
  ```json
  {
    "pixel_2": {
      "deviceName": "Pixel 2",
      "width": 411, 
      "height": 731,
      "deviceScaleFactor": 2.6,
      "userAgent": "Mozilla/5.0 (Linux; Android 8.0; Pixel 2...)"
    },
    "iphone_12": {
      "deviceName": "iPhone 12",
      "width": 390,
      "height": 844,
      "deviceScaleFactor": 3,
      "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0...)"
    }
  }
  ```
- Driver factory dynamically creates appropriate WebDriver:
  ```python
  def get_driver(device_name="pixel_2", browser_type="chrome"):
      device_config = DeviceConfig.get_device(device_name)
      if browser_type == "chrome":
          options = webdriver.ChromeOptions()
          options.add_experimental_option("mobileEmulation", device_config)
          return webdriver.Chrome(options=options)
  ```
- Test configuration via pytest CLI:
  ```bash
  pytest tests/ --device=iphone_12 --browser=chrome
  ```

### 2. BDD Integration
**Description**: Enables writing tests in Gherkin syntax for better readability by non-technical stakeholders.

**Implementation**:
- Feature files in `tests/features/`:
  ```gherkin
  # twitch.feature
  Feature: Twitch Mobile Search
  
    Scenario: Find StarCraft II streams
      Given I open Twitch mobile site
      When I search for "StarCraft II" 
      And I scroll down 2 times
      And I select a streamer
      Then the video should play
  ```
- Step implementations in `tests/features/steps/`:
  ```python
  # twitch_steps.py
  from pytest_bdd import given, when, then, parsers
  
  @given("I open Twitch mobile site")
  def open_twitch(browser):
      return TwitchHomePage(browser).navigate()
      
  @when(parsers.parse('I search for "{query}"'))
  def search_for(browser, query):
      home_page = TwitchHomePage(browser)
      return home_page.click_search().search_for(query)
  ```

### 3. Data-Driven Testing
**Description**: Tests can be parameterized with external data for broader coverage without code duplication.

**Implementation**:
- Data files in `data/` directory:
  ```json
  # search_queries.json
  [
    {"query": "StarCraft II", "expected_results": true},
    {"query": "League of Legends", "expected_results": true},
    {"query": "RandomInvalidGameName12345", "expected_results": false}
  ]
  ```
- Data provider utilities:
  ```python
  # utils/data_provider.py
  def get_test_data(filename):
      with open(f"data/{filename}") as f:
          return json.load(f)
  ```
- Parameterized tests:
  ```python
  @pytest.mark.parametrize("test_data", get_test_data("search_queries.json"))
  def test_search_results(browser, test_data):
      results_page = (TwitchHomePage(browser)
                     .navigate()
                     .click_search()
                     .search_for(test_data["query"]))
      
      if test_data["expected_results"]:
          assert results_page.has_results()
      else:
          assert results_page.has_no_results()
  ```

### 4. Multi-Environment Support
**Description**: Framework supports running tests against different environments (dev/staging/prod) with environment-specific configurations.

**Implementation**:
- Environment configs in `config/environments.json`:
  ```json
  {
    "dev": {
      "base_url": "https://dev.twitch.tv",
      "timeout": 10
    },
    "staging": {
      "base_url": "https://stage.twitch.tv",
      "timeout": 15
    },
    "prod": {
      "base_url": "https://m.twitch.tv",
      "timeout": 20
    }
  }
  ```
- Environment manager:
  ```python
  # utils/env_manager.py
  class EnvironmentManager:
      @staticmethod
      def get_config(env_name="prod"):
          with open("config/environments.json") as f:
              envs = json.load(f)
          return envs.get(env_name, envs["prod"])
  ```
- Usage in test execution:
  ```bash
  pytest tests/ --env=staging
  ```

### 5. Visual Testing Integration
**Description**: Framework provides hooks for visual comparison of UI elements.

**Implementation**:
- Screenshot comparison utility:
  ```python
  # utils/visual_testing.py
  class VisualTesting:
      @staticmethod
      def compare_screenshots(actual_image, baseline_name, threshold=0.95):
          baseline_path = f"baseline/{baseline_name}.png"
          if not os.path.exists(baseline_path):
              # Save as new baseline
              shutil.copy(actual_image, baseline_path)
              return True
              
          # Compare with existing baseline
          return image_similarity(actual_image, baseline_path) >= threshold
  ```
- Usage in page objects:
  ```python
  def verify_search_results_ui(self):
      self.take_screenshot("search_results.png")
      assert VisualTesting.compare_screenshots(
          "search_results.png", 
          "search_results_baseline"
      )
  ```

### 6. API + UI Hybrid Testing
**Description**: Setup test state via API and verify via UI for faster test execution.

**Implementation**:
- API client:
  ```python
  # utils/api_client.py
  class TwitchAPI:
      def __init__(self, api_key):
          self.api_key = api_key
          self.base_url = "https://api.twitch.tv/helix"
          
      def get_top_games(self):
          response = requests.get(f"{self.base_url}/games/top", 
                                 headers={"Client-ID": self.api_key})
          return response.json()
  ```
- Hybrid test example:
  ```python
  def test_top_games(browser, api_client):
      # Get data via API
      top_games = api_client.get_top_games()
      first_game = top_games["data"][0]["name"]
      
      # Verify via UI
      home_page = TwitchHomePage(browser).navigate()
      assert home_page.get_top_game_name() == first_game
  ```

### 7. Self-Healing Elements
**Description**: Elements can be located using multiple strategies for increased test reliability.

**Implementation**:
- Multi-strategy element locator:
  ```python
  # utils/element_finder.py
  class ElementFinder:
      @staticmethod
      def find_with_retry(driver, locators_dict, timeout=10):
          for strategy, value in locators_dict.items():
              try:
                  if strategy == "id":
                      locator = (By.ID, value)
                  elif strategy == "css":
                      locator = (By.CSS_SELECTOR, value)
                  elif strategy == "xpath":
                      locator = (By.XPATH, value)
                      
                  return WebDriverWait(driver, timeout).until(
                      EC.presence_of_element_located(locator)
                  )
              except:
                  continue
                  
          raise ElementNotFound(f"Could not find element with any strategy: {locators_dict}")
  ```
- Usage in page objects:
  ```python
  def click_search_button(self):
      search_button = {
          "css": ".search-button",
          "xpath": "//button[@data-a-target='search-button']",
          "accessibility_id": "search_button"
      }
      ElementFinder.find_with_retry(self.driver, search_button).click()
      return SearchPage(self.driver)
  ```

### 8. Performance Metrics Tracking
**Description**: Collect performance metrics during functional testing for early detection of performance regressions.

**Implementation**:
- Performance metrics collector:
  ```python
  # utils/performance.py
  class PerformanceTracker:
      @staticmethod
      def get_page_load_time(driver):
          navigation_timing = driver.execute_script(
              "return window.performance.timing"
          )
          return navigation_timing["loadEventEnd"] - navigation_timing["navigationStart"]
          
      @staticmethod
      def log_metrics(page_name, metrics):
          with open("reports/performance.csv", "a") as f:
              f.write(f"{datetime.now()},{page_name},{metrics['load_time']}\n")
  ```
- Usage in tests:
  ```python
  def test_navigation_performance(browser):
      home_page = TwitchHomePage(browser).navigate()
      
      # Collect performance metrics
      load_time = PerformanceTracker.get_page_load_time(browser)
      PerformanceTracker.log_metrics("home_page", {"load_time": load_time})
      
      # Assert performance requirements
      assert load_time < 3000  # Load time under 3 seconds
  ```

## Additional Extension Points to Exceed Expectations 🚀

### 1. Data-Driven Framework
- External test data in CSV/JSON/YAML files
- Data providers for parameterized tests
- Example: Testing search with multiple queries

### 2. Visual Testing Integration
- Framework hooks for Applitools/Percy
- Visual comparison capabilities
- Pixel-perfect testing option

### 3. API + UI Hybrid Framework
- Ability to set up test state via API then verify via UI
- Combine Selenium with requests/httpx
- Faster test execution and more reliable test setup

### 4. Contract Testing Readiness
- Framework can be extended to verify API contracts
- Integration points for tools like Pact

### 5. Real Device Testing
- Appium integration for true mobile testing
- Same page objects can be reused with minimal adaptation

### 6. Multi-Environment Support
- Configuration for dev/staging/prod
- Environment-specific settings handling

### 7. Localization Testing Framework
- Support for testing in multiple languages
- Locale-specific test data

### 8. Test Impact Analysis
- Integration with tools to run only tests affected by code changes
- Metadata for mapping tests to features

### 9. Comprehensive Reporting
- Allure Reports with custom dashboards
- Historical test results
- Failure analysis tools

### 10. Self-Healing Elements
- AI-powered element location fallback strategies
- Multiple locator strategies per element

### 11. Configuration-as-Code
- YAML configuration for test prioritization, retry policies
- Environment-specific execution plans

### 12. Performance Metrics Collection
- Track page load times and other performance KPIs during functional tests
- Performance regression detection