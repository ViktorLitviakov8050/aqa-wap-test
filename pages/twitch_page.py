from selenium.webdriver.common.by import By
from .base_page import BasePage
from typing import Any
import random

class TwitchPage(BasePage):
    # Locators
    SEARCH_ICON = (By.CSS_SELECTOR, '[data-a-target="search-button"]')
    SEARCH_INPUT = (By.CSS_SELECTOR, '[data-a-target="search-input"]')
    STREAMER_LINK = (By.CSS_SELECTOR, '[data-a-target="preview-card-title-link"]')
    MATURE_CONTENT_ACCEPT = (By.CSS_SELECTOR, '[data-a-target="player-overlay-mature-accept"]')
    
    def __init__(self, driver: Any) -> None:
        super().__init__(driver)
        self.driver.get(self.config['base_url'])
    
    def navigate(self) -> 'TwitchPage':
        """Navigate to the base URL"""
        self.driver.get(self.config['base_url'])
        return self
    
    def click_search(self) -> None:
        """Click search icon in navigation panel"""
        self.click(self.SEARCH_ICON)
        self.logger.info('Clicked search icon in navigation')
    
    def search_for(self, query: str) -> None:
        """Input search query"""
        self.input_text(self.SEARCH_INPUT, query)
        self.logger.info(f'Searched for: {query}')
    
    def select_streamer(self, index: int = None) -> None:
        """
        Select streamer from search results
        
        Args:
            index: Optional index of streamer to select. If None, selects random streamer.
        """
        streamers = self.find_elements(self.STREAMER_LINK)
        if not streamers:
            raise Exception('No streamers found in search results')
        
        # If index is not provided, select random streamer
        if index is None:
            index = random.randint(0, len(streamers) - 1)
            self.logger.info(f'Selected random streamer at index {index} from {len(streamers)} available')
        elif index >= len(streamers):
            self.logger.warning(f'Index {index} out of range, selecting random streamer instead')
            index = random.randint(0, len(streamers) - 1)
        
        # Use ActionChains for more reliable clicking
        self.scroll_to_element(streamers[index])
        self.click_with_actions(streamers[index])
        self.logger.info(f'Selected streamer at index {index}')
    
    def handle_mature_content(self) -> None:
        """Handle mature content popup if present"""
        self.handle_popup(self.MATURE_CONTENT_ACCEPT)
    
    def perform_search_flow(self, query: str) -> None:
        """Perform complete search flow"""
        self.click_search()
        self.search_for(query)
        self.scroll_page(2)
        self.select_streamer()  # Now selects random streamer by default
        self.handle_mature_content()
        self.take_screenshot('streamer_page')