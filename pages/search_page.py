from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logging_utils import get_logger


class SearchPage(BasePage):
    """Page object for Twitch search results page"""
    
    # Locators
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[data-a-target='tw-input']")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[data-a-target='search-submit-button']")
    SEARCH_RESULTS = (By.CSS_SELECTOR, "div[data-a-target='search-result-card']")
    STREAMER_CARD = (By.CSS_SELECTOR, "a[data-a-target='search-result-card-link']")
    NO_RESULTS_MESSAGE = (By.CSS_SELECTOR, ".tw-align-items-center.tw-flex.tw-flex-col")
    CATEGORY_TAB = (By.CSS_SELECTOR, "button[data-a-target='search-tab-CATEGORY']")
    CHANNEL_TAB = (By.CSS_SELECTOR, "button[data-a-target='search-tab-CHANNEL']")
    
    def __init__(self, driver):
        """Initialize search page with WebDriver"""
        super().__init__(driver)
        self.logger = get_logger()
    
    def search_for(self, query):
        """
        Enter search query and submit
        
        Args:
            query: Search term to enter
            
        Returns:
            SearchPage: Self reference for method chaining
        """
        self.logger.info(f"Searching for: {query}")
        self.input_text(self.SEARCH_INPUT, query)
        self.click(self.SEARCH_BUTTON)
        return self
    
    def get_search_results(self):
        """
        Get all search result elements
        
        Returns:
            list: WebElements representing search results
        """
        self.logger.info("Getting search results")
        return self.find_elements(self.SEARCH_RESULTS)
    
    def has_results(self):
        """
        Check if search returned any results
        
        Returns:
            bool: True if results exist, False otherwise
        """
        results = self.get_search_results()
        has_results = len(results) > 0
        self.logger.info(f"Search has results: {has_results}")
        return has_results
    
    def has_no_results(self):
        """
        Check if search returned no results message
        
        Returns:
            bool: True if no results message exists
        """
        try:
            no_results = self.find_element(self.NO_RESULTS_MESSAGE, timeout=3)
            self.logger.info("No search results found message displayed")
            return True
        except:
            return False
    
    def click_streamer(self, index=0):
        """
        Click on a streamer from search results
        
        Args:
            index: Index of the streamer to click (default: 0 - first)
            
        Returns:
            StreamerPage: The streamer page object
        """
        streamers = self.find_elements(self.STREAMER_CARD)
        
        if not streamers:
            self.logger.error("No streamers found in search results")
            raise ValueError("No streamers found in search results")
        
        if index >= len(streamers):
            self.logger.warning(f"Index {index} out of range, clicking first streamer instead")
            index = 0
        
        self.logger.info(f"Clicking on streamer at index: {index}")
        self.scroll_to_element(streamers[index])
        self.click_element(streamers[index])
        
        # Import here to avoid circular import
        from pages.streamer_page import StreamerPage
        return StreamerPage(self.driver)
    
    def switch_to_channels_tab(self):
        """
        Switch to channels tab
        
        Returns:
            SearchPage: Self reference for method chaining
        """
        self.logger.info("Switching to Channels tab")
        self.click(self.CHANNEL_TAB)
        return self
    
    def switch_to_categories_tab(self):
        """
        Switch to categories tab
        
        Returns:
            SearchPage: Self reference for method chaining
        """
        self.logger.info("Switching to Categories tab")
        self.click(self.CATEGORY_TAB)
        return self 