from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from typing import Any
import yaml
import os

class BasePage:
    def __init__(self, driver: Any) -> None:
        self.driver = driver
        with open('config/config.yaml', 'r') as file:
            self.config = yaml.safe_load(file)
        self.wait = WebDriverWait(driver, self.config['waits']['explicit'])
    
    def find_element(self, by: By, value: str) -> Any:
        return self.wait.until(EC.presence_of_element_located((by, value)))
    
    def click(self, by: By, value: str) -> None:
        element = self.wait.until(EC.element_to_be_clickable((by, value)))
        ActionChains(self.driver).move_to_element(element).click().perform()
    
    def input_text(self, by: By, value: str, text: str) -> None:
        element = self.find_element(by, value)
        element.clear()
        element.send_keys(text)
    
    def scroll_page(self, times: int = 1) -> None:
        for _ in range(times):
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            self.driver.implicitly_wait(2)
    
    def take_screenshot(self, name: str) -> str:
        screenshot_dir = self.config['screenshots']['path']
        os.makedirs(screenshot_dir, exist_ok=True)
        file_path = os.path.join(screenshot_dir, f"{name}.png")
        self.driver.save_screenshot(file_path)
        return file_path