from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from typing import Any
import yaml
import logging

class BasePage:
    def __init__(self, driver: Any) -> None:
        self.driver = driver
        with open('config/config.yaml', 'r') as file:
            self.config = yaml.safe_load(file)
        self.wait = WebDriverWait(driver, self.config['waits']['explicit'])
        self.logger = logging.getLogger(__name__)
    
    def find_element(self, by: By, value: str) -> Any:
        """Find element with explicit wait"""
        return self.wait.until(EC.presence_of_element_located((by, value)))
    
    def click(self, by: By, value: str) -> None:
        """Click element with explicit wait"""
        element = self.wait.until(EC.element_to_be_clickable((by, value)))
        element.click()
    
    def input_text(self, by: By, value: str, text: str) -> None:
        """Input text into element"""
        element = self.find_element(by, value)
        element.clear()
        element.send_keys(text)
    
    def scroll_page(self, times: int = 1) -> None:
        """Scroll page specified number of times"""
        for i in range(times):
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            self.driver.implicitly_wait(2)
            self.logger.info(f'Scrolled page {i + 1} time(s)')
    
    def take_screenshot(self, name: str) -> str:
        """Take screenshot and save it to configured path"""
        path = f"{self.config['screenshots']['path']}/{name}.png"
        self.driver.save_screenshot(path)
        self.logger.info(f'Screenshot saved to {path}')
        return path
    
    def handle_popup(self, by: By, value: str, timeout: int = 5) -> None:
        """Handle popup if present"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            element.click()
            self.logger.info('Popup handled successfully')
        except:
            self.logger.info('No popup found or popup handling timed out')