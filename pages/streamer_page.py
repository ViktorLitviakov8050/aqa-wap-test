from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logging_utils import get_logger
import time
import os


class StreamerPage(BasePage):
    """Page object for Twitch streamer page"""
    
    # Locators
    VIDEO_PLAYER = (By.CSS_SELECTOR, ".video-player__container")
    STREAMER_NAME = (By.CSS_SELECTOR, "h1[data-a-target='stream-title']")
    FOLLOW_BUTTON = (By.CSS_SELECTOR, "button[data-a-target='follow-button']")
    SUBSCRIBE_BUTTON = (By.CSS_SELECTOR, "button[data-a-target='subscribe-button']")
    MATURE_CONTENT_ACCEPT = (By.CSS_SELECTOR, "button[data-a-target='player-overlay-mature-accept']")
    MODAL_CLOSE_BUTTON = (By.CSS_SELECTOR, "button[data-a-target='modal-close-button']")
    CHAT_INPUT = (By.CSS_SELECTOR, "textarea[data-a-target='chat-input']")
    CHAT_MESSAGES = (By.CSS_SELECTOR, ".chat-line__message")
    VIEWER_COUNT = (By.CSS_SELECTOR, "div[data-a-target='viewers-count']")
    
    def __init__(self, driver):
        """Initialize streamer page with WebDriver"""
        super().__init__(driver)
        self.logger = get_logger()
    
    def wait_for_video_player(self, timeout=10):
        """
        Wait for video player to be visible and loaded
        
        Args:
            timeout: Maximum time to wait in seconds
            
        Returns:
            StreamerPage: Self reference for method chaining
        """
        self.logger.info("Waiting for video player to load")
        self.wait_for_element_visible(self.VIDEO_PLAYER, timeout)
        # Additional wait to ensure player is loaded
        time.sleep(2)
        return self
    
    def handle_mature_content_warning(self):
        """
        Handle mature content warning if present
        
        Returns:
            StreamerPage: Self reference for method chaining
        """
        try:
            accept_button = self.find_element(self.MATURE_CONTENT_ACCEPT, timeout=3)
            if accept_button:
                self.logger.info("Handling mature content warning")
                self.click_element(accept_button)
        except:
            self.logger.info("No mature content warning detected")
        
        return self
    
    def handle_modal_popups(self):
        """
        Handle any modal popups by closing them
        
        Returns:
            StreamerPage: Self reference for method chaining
        """
        try:
            close_button = self.find_element(self.MODAL_CLOSE_BUTTON, timeout=3)
            if close_button:
                self.logger.info("Closing modal popup")
                self.click_element(close_button)
        except:
            self.logger.info("No modal popup detected")
        
        return self
    
    def get_streamer_name(self):
        """
        Get the streamer's name
        
        Returns:
            str: The streamer's name
        """
        element = self.find_element(self.STREAMER_NAME)
        name = element.text
        self.logger.info(f"Current streamer: {name}")
        return name
    
    def get_viewer_count(self):
        """
        Get current viewer count
        
        Returns:
            int: Number of viewers
        """
        element = self.find_element(self.VIEWER_COUNT)
        count_text = element.text.replace(",", "")
        try:
            count = int(count_text)
            self.logger.info(f"Current viewer count: {count}")
            return count
        except ValueError:
            self.logger.error(f"Could not parse viewer count: {count_text}")
            return 0
    
    def take_screenshot(self, filename=None):
        """
        Take a screenshot of the streamer page
        
        Args:
            filename: Name of the screenshot file (default: auto-generated)
            
        Returns:
            str: Path to the saved screenshot
        """
        if not filename:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            streamer_name = self.get_streamer_name().replace(" ", "_")[:20]
            filename = f"{streamer_name}_{timestamp}.png"
        
        screenshots_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                      "reports", "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)
        
        screenshot_path = os.path.join(screenshots_dir, filename)
        
        self.logger.info(f"Taking screenshot: {screenshot_path}")
        self.driver.save_screenshot(screenshot_path)
        return screenshot_path 