import pytest
import yaml
import logging
import os
from datetime import datetime
from utils.driver_factory import DriverFactory

@pytest.fixture(scope='session', autouse=True)
def setup_logging():
    """Set up logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('test_execution.log'),
            logging.StreamHandler()
        ]
    )

@pytest.fixture(scope='session')
def config():
    """Load test configuration"""
    with open('config/config.yaml', 'r') as file:
        return yaml.safe_load(file)

@pytest.fixture
def device(request):
    """Get device name from command line or use default"""
    return request.config.getoption("--device")

@pytest.fixture
def browser(request):
    """Get browser type from command line or use default"""
    return request.config.getoption("--browser")

@pytest.fixture
def headless(request):
    """Get headless mode from command line or use default"""
    return request.config.getoption("--headless")

@pytest.fixture(scope='function')
def driver(config, device, browser, headless, request):
    """Set up WebDriver with mobile emulation using DriverFactory"""
    driver = DriverFactory.create_driver(
        device_name=device, 
        browser_type=browser,
        headless=headless
    )
    
    driver.implicitly_wait(config['waits']['implicit'])
    
    # Create screenshots directory if it doesn't exist
    os.makedirs(config['screenshots']['path'], exist_ok=True)
    
    yield driver
    
    # Take screenshot on test failure
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_path = f"{config['screenshots']['path']}/failure_{request.node.name}_{timestamp}.png"
        driver.save_screenshot(screenshot_path)
        logging.info(f'Failure screenshot saved to {screenshot_path}')
    
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to store test result for screenshot capture"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

def pytest_addoption(parser):
    """Add command line options for device, browser, and headless mode"""
    parser.addoption("--device", action="store", default="pixel_2", 
                     help="Mobile device to emulate: pixel_2, iphone_12, samsung_s20")
    parser.addoption("--browser", action="store", default="chrome", 
                     help="Browser to use for tests")
    parser.addoption("--headless", action="store_true", default=False, 
                     help="Run browser in headless mode")