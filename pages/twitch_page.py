from selenium.webdriver.common.by import By
from .base_page import BasePage
from typing import Any

class TwitchPage(BasePage):
    # Locators
    SEARCH_ICON = (By.CSS_SELECTOR, '[data-a-target="search-button"]')
    SEARCH_INPUT = (By.CSS_SELECTOR, '[data-a-target="search-input"]')
    STREAMER_LINK = (By.CSS_SELECTOR, '[data-a-target="preview-card-title-link"]')
    MATURE_CONTENT_ACCEPT = (By.CSS_SELECTOR, '[data-a-target="player-overlay-mature-accept"]')
    
    def __init__(self, driver: Any) -> None:
        super().__init__(driver)
        self.driver.get(self.config['base_url'])
    
    def click_search(self) -> None:
        """Click search icon"""
        self.click(*self.SEARCH_ICON)
        self.logger.info('Clicked search icon')
    
    def search_for(self, query: str) -> None:
        """Input search query"""
        self.input_text(*self.SEARCH_INPUT, query)
        self.logger.info(f'Searched for: {query}')
    
    def select_streamer(self, index: int = 0) -> None:
        """Select streamer from search results"""
        streamers = self.driver.find_elements(*self.STREAMER_LINK)
        if streamers:
            streamers[index].click()
            self.logger.info(f'Selected streamer at index {index}')
        else:
            raise Exception('No streamers found in search results')
    
    def handle_mature_content(self) -> None:
        """Handle mature content popup if present"""
        self.handle_popup(*self.MATURE_CONTENT_ACCEPT)
    
    def perform_search_flow(self, query: str) -> None:
        """Perform complete search flow"""
        self.click_search()
        self.search_for(query)
        self.scroll_page(2)
        self.select_streamer()
        self.handle_mature_content()
        self.take_screenshot('streamer_page')