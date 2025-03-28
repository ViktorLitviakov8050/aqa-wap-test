# AQA WAP Test Framework 📱

Automated test suite for mobile web testing of Twitch.tv using Selenium WebDriver with Python.

## Project Structure 🏗️

```
aqa-wap-test/
├── config/                 # Configuration files
│   ├── config.yaml         # Environment settings
│   └── devices.json        # Mobile device definitions
├── pages/                  # Page Object Model implementation
│   ├── base_page.py        # Base page with common methods
│   ├── twitch_page.py      # Twitch specific base page
│   ├── home_page.py        # Twitch home page
│   ├── search_page.py      # Search results page
│   └── streamer_page.py    # Individual streamer page
├── tests/                  # Test cases
│   ├── conftest.py         # Pytest fixtures
│   ├── test_twitch_search.py    # Test cases
│   ├── test_twitch_bdd.py       # BDD test runner
│   └── features/           # BDD features
│       ├── twitch.feature  # Gherkin feature file
│       └── steps/          # Step definitions
│           └── twitch_steps.py
├── utils/                  # Utility modules
│   ├── driver_factory.py   # WebDriver setup/teardown
│   ├── logging_utils.py    # Custom logging
│   ├── waits.py            # Custom wait methods
│   └── bdd_helpers.py      # BDD utility functions
├── data/                   # Test data files
│   └── search_queries.json # Search query test data
├── reports/                # Test reports and artifacts
│   ├── screenshots/        # Test failure screenshots
│   └── logs/               # Test execution logs
├── requirements.txt        # Dependencies
└── README.md               # Project documentation
```

## Features ✨

- **Page Object Model** - Clean separation of test logic and page interactions
- **Fluent Interface** - Method chaining for better readability
- **Factory Pattern** - Flexible driver configuration for different devices
- **Custom Waits** - Robust element interaction strategies
- **Logging** - Detailed test execution logs
- **Screenshots** - Automatic capture on test failure
- **Mobile Emulation** - Chrome mobile device emulation
- **Data-Driven** - Parameterized tests with external data
- **BDD** - Behavior-Driven Development with Gherkin syntax

## Tech Stack 🛠️

- Python 3.9+
- Selenium WebDriver
- Pytest
- Pytest-BDD
- Chrome WebDriver
- PyYAML
- Python Logging

## Setup 🚀

### Prerequisites

- Python 3.9+
- Chrome browser
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/aqa-wap-test.git
   cd aqa-wap-test
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running Tests ▶️

### Basic Test Execution

```bash
pytest tests/
```

### Run BDD Tests Only

```bash
pytest tests/test_twitch_bdd.py
```

### Run with Specific Device

```bash
pytest tests/ --device=iphone_12
```

### Run with HTML Report

```bash
pytest tests/ --html=reports/report.html
```

### Run in Headless Mode

```bash
pytest tests/ --headless
```

## Mobile Emulation 📱

This framework uses Chrome's mobile emulation feature to test web applications in a mobile context. The implementation uses a factory pattern for creating WebDriver instances with specific mobile device configurations.

### Available Devices

The following devices are pre-configured in `config/devices.json`:

| Device | Description |
|--------|-------------|
| pixel_2 | Google Pixel 2 (default) |
| iphone_12 | Apple iPhone 12 |
| samsung_s20 | Samsung Galaxy S20 |

### Using Different Devices

You can specify which device to use during test execution with the `--device` flag:

```bash
# Run tests with iPhone 12 emulation
pytest tests/ --device=iphone_12

# Run tests with Samsung Galaxy S20 emulation
pytest tests/ --device=samsung_s20
```

### Browser Support

The framework supports the following browsers:

- Chrome (default) - Full mobile emulation support
- Firefox - Limited mobile emulation (user agent and dimensions only)

Specify the browser with the `--browser` flag:

```bash
# Run tests with Firefox
pytest tests/ --browser=firefox
```

### Headless Mode

Run tests in headless mode (without browser UI) using the `--headless` flag:

```bash
# Run tests in headless mode
pytest tests/ --headless
```

### How It Works

1. The `DriverFactory` class in `utils/driver_factory.py` handles WebDriver creation with device-specific configurations.
2. Device configurations are stored in `config/devices.json` and include dimensions, scale factor, and user agent.
3. The `conftest.py` file provides Pytest fixtures that use the factory to create WebDriver instances.
4. Command-line options allow selecting different devices, browsers, and running in headless mode.

### Adding a New Device

1. Add the device configuration to `config/devices.json`:
```json
"pixel_6": {
  "deviceName": "Pixel 6",
  "width": 412,
  "height": 915,
  "deviceScaleFactor": 2.6,
  "userAgent": "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.104 Mobile Safari/537.36"
}
```

2. Use the new device in your tests:
```bash
pytest tests/ --device=pixel_6
```

## Extending the Framework 🧩

### Adding a New Device

1. Add device configuration to `config/devices.json`:
   ```json
   "ipad_pro": {
     "deviceName": "iPad Pro",
     "width": 1024,
     "height": 1366,
     "deviceScaleFactor": 2,
     "userAgent": "Mozilla/5.0 (iPad; CPU OS 14_0...)"
   }
   ```

2. Run tests with new device:
   ```bash
   pytest tests/ --device=ipad_pro
   ```

### Adding a New Page Object

1. Create new page object in `pages/` directory
2. Extend BasePage or TwitchPage class
3. Implement page-specific methods and locators
4. Update `pages/__init__.py` to import the new page

### Adding New Tests

1. Create new test file in `tests/` directory
2. Use existing fixtures from `conftest.py`
3. Follow Page Object Model pattern for interactions

### Adding New BDD Scenarios

1. Add new scenarios to `tests/features/twitch.feature` using Gherkin syntax
2. Implement any new step definitions in `tests/features/steps/twitch_steps.py`
3. Run with `pytest tests/test_twitch_bdd.py`

## Test Execution Demo
Below is a GIF showing the test execution on a mobile device:

![Twitch Search Test Demo](reports/gifs/twitch_search_pixel_2_chrome_StarCraft_II.gif)

The GIF demonstrates:
1. Navigation to Twitch home page
2. Search functionality
3. Streamer selection
4. Mature content handling
5. Final streamer page verification 