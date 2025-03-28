from selenium.webdriver.common.by import By
from pages.twitch_page import TwitchPage
from utils.logging_utils import get_logger


class HomePage(TwitchPage):
    """Page object for Twitch home page"""
    
    # Locators
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[data-a-target='header-search-button']")
    BROWSE_BUTTON = (By.CSS_SELECTOR, "a[data-a-target='browse-link']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[data-a-target='login-button']")
    COOKIE_CONSENT = (By.CSS_SELECTOR, "button[data-a-target='consent-banner-accept']")
    FEATURED_STREAMS = (By.CSS_SELECTOR, "div[data-test-selector='recommended-channel']")
    
    def __init__(self, driver):
        """Initialize home page with WebDriver"""
        super().__init__(driver)
        self.logger = get_logger()
    
    def navigate(self):
        """
        Navigate to Twitch home page
        
        Returns:
            HomePage: Self reference for method chaining
        """
        self.logger.info("Navigating to Twitch home page")
        super().navigate()
        self.handle_cookie_consent()
        return self
    
    def handle_cookie_consent(self):
        """
        Accept cookies if consent banner is present
        
        Returns:
            HomePage: Self reference for method chaining
        """
        try:
            consent_button = self.find_element(self.COOKIE_CONSENT, timeout=5)
            if consent_button:
                self.logger.info("Accepting cookies")
                self.click_element(consent_button)
        except:
            self.logger.info("No cookie consent banner detected")
        
        return self
    
    def click_search(self):
        """
        Click on search button to go to search page
        
        Returns:
            SearchPage: The search page object
        """
        self.logger.info("Clicking search button")
        self.click(self.SEARCH_BUTTON)
        
        from pages.search_page import SearchPage
        return SearchPage(self.driver)
    
    def click_browse(self):
        """
        Click on browse button
        
        Returns:
            HomePage: Self reference for method chaining
        """
        self.logger.info("Clicking browse button")
        self.click(self.BROWSE_BUTTON)
        return self
    
    def click_login(self):
        """
        Click on login button
        
        Returns:
            HomePage: Self reference for method chaining
        """
        self.logger.info("Clicking login button")
        self.click(self.LOGIN_BUTTON)
        return self
    
    def get_featured_streams(self):
        """
        Get all featured streams on home page
        
        Returns:
            list: WebElements representing featured streams
        """
        self.logger.info("Getting featured streams")
        return self.find_elements(self.FEATURED_STREAMS)
    
    def click_featured_stream(self, index=0):
        """
        Click on a featured stream
        
        Args:
            index: Index of the featured stream to click (default: 0 - first)
            
        Returns:
            StreamerPage: The streamer page object
        """
        streams = self.get_featured_streams()
        
        if not streams:
            self.logger.error("No featured streams found")
            raise ValueError("No featured streams found")
        
        if index >= len(streams):
            self.logger.warning(f"Index {index} out of range, clicking first stream instead")
            index = 0
        
        self.logger.info(f"Clicking on featured stream at index: {index}")
        self.scroll_to_element(streams[index])
        self.click_element(streams[index])
        
        from pages.streamer_page import StreamerPage
        return StreamerPage(self.driver) 