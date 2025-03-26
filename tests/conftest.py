import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import yaml
import logging
import os
from datetime import datetime

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

@pytest.fixture(scope='function')
def driver(config, request):
    """Set up WebDriver with mobile emulation"""
    options = webdriver.ChromeOptions()
    options.add_experimental_option('mobileEmulation', config['browser']['mobile_emulation'])
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.implicitly_wait(config['waits']['implicit'])
    
    # Create screenshots directory if it doesn't exist
    os.makedirs(config['screenshots']['path'], exist_ok=True)
    
    yield driver
    
    # Take screenshot on test failure
    if request.node.rep_call.failed:
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