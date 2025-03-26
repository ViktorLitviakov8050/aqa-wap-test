from selenium.webdriver.common.by import By
from .base_page import BasePage
from typing import Any

class TwitchPage(BasePage):
    # Locators
    SEARCH_ICON = (By.CSS_SELECTOR, '[data-a-target="search-button"]')
    SEARCH_INPUT = (By.CSS_SELECTOR, '[data-a-target="search-input"]')
    STREAMER_LINKS = (By.CSS_SELECTOR, '[data-a-target="preview-card-title-link"]')
    MODAL_CLOSE = (By.CSS_SELECTOR, '[data-a-target="modal-close-button"]')
    
    def __init__(self, driver: Any) -> None:
        super().__init__(driver)
        self.driver.get(self.config['base_url'])
    
    def click_search(self) -> None:
        self.click(*self.SEARCH_ICON)
    
    def search_for(self, query: str) -> None:
        self.input_text(*self.SEARCH_INPUT, query)
    
    def select_streamer(self, index: int = 0) -> None:
        streamers = self.driver.find_elements(*self.STREAMER_LINKS)
        if len(streamers) > index:
            streamers[index].click()
    
    def handle_modal(self) -> None:
        try:
            self.click(*self.MODAL_CLOSE)
        except:
            pass  # Modal might not appear