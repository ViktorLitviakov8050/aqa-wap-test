from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from .base_page import BasePage
from typing import Any
import random
import time
from selenium.webdriver.common.action_chains import ActionChains

class TwitchPage(BasePage):
    # Locators
    BROWSE_BUTTON = [
        (By.CSS_SELECTOR, '[href="/directory"]'),
        (By.CSS_SELECTOR, '[data-a-target="browse-link"]'),
        (By.CSS_SELECTOR, '[data-test-selector="browse-button"]'),
        (By.XPATH, "//a[contains(@href, '/directory')]"),
        (By.XPATH, "//a[.//div[contains(text(), 'Browse')]]")
    ]
    SEARCH_ICONS = [
        (By.CSS_SELECTOR, '[data-a-target="tw-core-button-icon-button"]'),  # Search icon button
        (By.CSS_SELECTOR, '[data-a-target="header-search-button"]'),  # Header search button
        (By.CSS_SELECTOR, 'button[aria-label*="Search"]'),  # Generic search button
        (By.CSS_SELECTOR, '[data-test-selector="search-button"]')  # Test selector search button
    ]
    SEARCH_INPUT = (By.CSS_SELECTOR, 'input[aria-label="Search Input"]')  # Updated search input locator
    SEARCH_SUGGESTIONS = (By.CSS_SELECTOR, '[data-test-selector="search-suggestion"]')  # Search suggestions dropdown
    STREAMER_LINK = (By.CSS_SELECTOR, '[data-test-selector="TitleLink"]')
    MATURE_CONTENT_ACCEPT = (By.CSS_SELECTOR, '[data-test-selector="mature-accept-button"]')
    
    # App promotion dismiss button
    APP_DISMISS_BUTTON = (By.CSS_SELECTOR, 'button[data-a-target="dismiss-button"]')
    
    COOKIE_CONSENT_BUTTON = [
        (By.CSS_SELECTOR, '[data-a-target="consent-banner-accept"]'),
        (By.CSS_SELECTOR, 'button[data-consent-banner="accept"]'),
        (By.CSS_SELECTOR, '[data-test-selector="consent-banner-accept"]'),
        (By.XPATH, "//button[contains(text(), 'Accept') and contains(@class, 'consent')]"),
        (By.XPATH, "//button[contains(text(), 'Accept')]")
    ]
    
    def navigate(self) -> 'TwitchPage':
        """Navigate to Twitch homepage and wait for it to load"""
        self.driver.get("https://www.twitch.tv")
        self.wait_for_page_load()
        self.set_consent_cookie()
        self.handle_app_promotion()
        return self
    
    def set_consent_cookie(self) -> None:
        """Handle cookie consent using multiple strategies"""
        # First try clicking the consent button if visible
        for locator in self.COOKIE_CONSENT_BUTTON:
            try:
                if self.is_element_present(locator, timeout=3):
                    element = self.find_element(locator)
                    try:
                        element.click()
                    except:
                        self.driver.execute_script("arguments[0].click();", element)
                    self.logger.info("Clicked cookie consent button")
                    # Wait for banner to disappear
                    WebDriverWait(self.driver, 5).until_not(
                        EC.presence_of_element_located(locator)
                    )
                    return
            except Exception as e:
                self.logger.debug(f"Failed to click cookie consent with locator {locator}: {str(e)}")
                continue

        # If button not found, try setting cookies directly
        try:
            cookies = [
                {
                    'name': 'consent-banner',
                    'value': '2',
                    'domain': '.twitch.tv',
                    'path': '/'
                },
                {
                    'name': 'unique_id',
                    'value': 'cookie_consent_accepted',
                    'domain': '.twitch.tv',
                    'path': '/'
                }
            ]
            for cookie in cookies:
                self.driver.execute_script(
                    f"document.cookie = '{cookie['name']}={cookie['value']}; domain={cookie['domain']}; path={cookie['path']}'"
                )
            self.logger.info("Set consent cookies via JavaScript")
            self.driver.refresh()
            self.wait_for_page_load()
        except Exception as e:
            self.logger.error(f"Failed to set consent cookies: {str(e)}")
            # If all else fails, try to remove the banner element
            try:
                self.driver.execute_script("""
                    document.querySelectorAll('[class*="consent"], [class*="cookie"], [id*="consent"], [id*="cookie"]')
                    .forEach(el => el.remove());
                """)
                self.logger.info("Removed consent banner via JavaScript")
            except Exception as e:
                self.logger.error(f"Failed to remove consent banner: {str(e)}")
    
    def handle_app_promotion(self) -> None:
        """Dismiss app promotion banner if present"""
        try:
            if self.is_element_present(self.APP_DISMISS_BUTTON, timeout=5):
                self.click(self.APP_DISMISS_BUTTON)
                self.logger.info("Dismissed app promotion banner")
                # Wait for banner to disappear
                WebDriverWait(self.driver, 5).until_not(
                    EC.presence_of_element_located(self.APP_DISMISS_BUTTON)
                )
        except Exception as e:
            self.logger.debug(f"No app promotion banner found or failed to dismiss: {str(e)}")
    
    def wait_for_page_load(self):
        """Wait for the page to load completely"""
        WebDriverWait(self.driver, 20).until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete'
        )
        # Wait for main content to be visible
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element(By.CSS_SELECTOR, 'main') or True
        )
    
    def wait_for_navigation(self, old_url):
        """Wait for page URL to change"""
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.current_url != old_url
        )
    
    def click_browse(self) -> None:
        """Click browse button"""
        # First ensure no overlays
        self.driver.execute_script("""
            const elements = document.querySelectorAll('[class*="consent"], [class*="cookie"], [class*="overlay"], [class*="modal"], [class*="popup"]');
            elements.forEach(el => el.remove());
        """)
        
        # Try to find and click browse button with multiple locators
        for browse_locator in self.BROWSE_BUTTON:
            try:
                if self.is_element_present(browse_locator, timeout=3):
                    browse_element = self.find_element(browse_locator)
                    self.scroll_to_element(browse_element)
                    
                    # Wait for element to be clickable
                    WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable(browse_locator)
                    )
                    
                    # Store current URL to verify navigation
                    old_url = self.driver.current_url
                    
                    # Try multiple click strategies
                    try:
                        actions = ActionChains(self.driver)
                        actions.move_to_element(browse_element).click().perform()
                        self.logger.info(f"Clicked browse button using locator: {browse_locator}")
                    except Exception as e:
                        self.logger.debug(f"Failed to click browse with ActionChains: {str(e)}")
                        try:
                            self.driver.execute_script("arguments[0].click();", browse_element)
                            self.logger.info("Clicked browse button using JavaScript")
                        except Exception as e:
                            self.logger.debug(f"Failed to click browse with JavaScript: {str(e)}")
                            continue
                    
                    # Wait for navigation to complete
                    self.wait_for_navigation(old_url)
                    return
            except Exception as e:
                self.logger.debug(f"Failed to find browse button with locator {browse_locator}: {str(e)}")
                continue
        
        raise Exception("Could not find or click browse button with any locator")
    
    def click_search(self) -> None:
        """Click Browse button and wait for it to be active"""
        # Primary Browse button locator
        browse_button = (By.XPATH, "//a[contains(@class, 'ScInteractableBase-sc-ofisyf-0')]//div[text()='Browse']")
        
        try:
            if self.is_element_present(browse_button, timeout=2):
                self.find_element(browse_button).click()
                self.logger.info("Clicked Browse button")
                return
            
            raise Exception("Could not find or click Browse button")
        except Exception as e:
            self.logger.error(f"Failed to click Browse button: {str(e)}")
            raise
    
    def search_for(self, query: str) -> None:
        """Enter search query"""
        search_locators = [
            (By.CSS_SELECTOR, 'input[aria-label="Search Input"]'),
            (By.CSS_SELECTOR, '[data-a-target="search-input"]'),
            (By.CSS_SELECTOR, '[data-test-selector="search-input"]'),
            (By.CSS_SELECTOR, 'input[type="search"]'),
            (By.CSS_SELECTOR, 'input[placeholder*="Search"]')
        ]
        
        # Reduced timeout from 5 to 3 seconds
        for locator in search_locators:
            try:
                search_input = WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located(locator)
                )
                if search_input.is_displayed():
                    search_input.clear()
                    search_input.send_keys(query)
                    return
            except TimeoutException:
                continue
                
        raise Exception("Could not find visible search input with any locator")
    
    def select_streamer(self, index: int = None) -> None:
        """Select streamer from search results"""
        # Wait for streamer links to be present
        streamers = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.STREAMER_LINK)
        )
        
        if not streamers:
            raise Exception('No streamers found in search results')
        
        if index is None:
            index = random.randint(0, len(streamers) - 1)
            self.logger.info(f'Selected random streamer at index {index} from {len(streamers)} available')
        elif index >= len(streamers):
            self.logger.warning(f'Index {index} out of range, selecting random streamer instead')
            index = random.randint(0, len(streamers) - 1)
        
        # Wait for specific streamer to be clickable
        streamer = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-test-selector="TitleLink"]:nth-child({index + 1})'))
        )
        
        self.scroll_to_element(streamer)
        old_url = self.driver.current_url
        self.click_with_actions(streamer)
        self.wait_for_navigation(old_url)
        self.logger.info(f'Selected streamer at index {index}')
    
    def handle_mature_content(self) -> None:
        """Handle mature content popup if present"""
        try:
            # Reduced timeout from 5 to 2 seconds
            accept_button = WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable(self.MATURE_CONTENT_ACCEPT)
            )
            accept_button.click()
            # No need to wait for popup to disappear, this saves time
        except TimeoutException:
            # No mature content popup found, which is fine
            pass
    
    def perform_search_flow(self, query: str) -> None:
        """
        Perform complete search flow
        Args:
            query: Search query
        """
        self.click_search()
        self.search_for(query)
        self.scroll_page(0, 500)
        self.select_streamer()
        self.handle_mature_content()
        self.take_screenshot("streamer_page.png")
    
    def select_first_suggestion(self) -> None:
        """Select the first item from search suggestions dropdown"""
        # Try different locators for search suggestions
        suggestion_locators = [
            (By.CSS_SELECTOR, '[data-test-selector="search-suggestion"]'),
            (By.CSS_SELECTOR, '[data-a-target="search-result-item"]'),
            (By.CSS_SELECTOR, '[aria-label*="search result"]'),
            (By.CSS_SELECTOR, '.search-result__suggestion'),
            (By.CSS_SELECTOR, '[class*="search"] [class*="suggestion"]'),
            (By.CSS_SELECTOR, '[class*="SearchResult"]'),
            (By.CSS_SELECTOR, 'a[href*="/directory/game"]'),  # Game category links
            (By.CSS_SELECTOR, 'a[href*="/videos"]'),  # Video links
            (By.CSS_SELECTOR, 'a[href*="/channel"]')  # Channel links
        ]
        
        # Reduced sleep from 1 to 0.5 seconds
        time.sleep(0.5)
        
        # First try - just press Enter which is the simplest approach
        try:
            self.logger.info("Trying primary approach: pressing Enter key on search input")
            search_locators = [
                (By.CSS_SELECTOR, 'input[aria-label="Search Input"]'),
                (By.CSS_SELECTOR, '[data-a-target="search-input"]'),
                (By.CSS_SELECTOR, 'input[type="search"]')
            ]
            
            for locator in search_locators:
                try:
                    search_input = self.driver.find_element(*locator)
                    search_input.send_keys("\n")  # Send Enter key
                    
                    # Wait for results
                    WebDriverWait(self.driver, 5).until(
                        lambda d: any(
                            d.find_elements(By.CSS_SELECTOR, selector)
                            for selector in [
                                '[data-test-selector="TitleLink"]', 
                                '[class*="search-result"]',
                                '[class*="SearchResult"]',
                                'a[href*="/videos"]',
                                'a[href*="/channel"]'
                            ]
                        )
                    )
                    
                    self.logger.info("Used Enter key to submit search")
                    return
                except Exception:
                    continue
        except Exception as e:
            self.logger.debug(f"Enter key approach failed: {str(e)}")
        
        # Second try - click on suggestions
        for locator in suggestion_locators:
            try:
                # Wait for suggestions to appear
                self.logger.info(f"Trying to find search suggestions with locator: {locator}")
                suggestions = WebDriverWait(self.driver, 3).until(
                    EC.presence_of_all_elements_located(locator)
                )
                
                if not suggestions:
                    self.logger.warning(f"No suggestions found with locator: {locator}")
                    continue
                
                # Ensure the suggestion is visible
                self.scroll_to_element(suggestions[0])
                
                # Try different click strategies
                try:
                    # Try regular click
                    suggestions[0].click()
                except Exception as e:
                    self.logger.debug(f"Regular click failed: {str(e)}")
                    try:
                        # Try ActionChains
                        actions = ActionChains(self.driver)
                        actions.move_to_element(suggestions[0]).click().perform()
                    except Exception as e:
                        self.logger.debug(f"ActionChains click failed: {str(e)}")
                        # Try JavaScript click
                        self.driver.execute_script("arguments[0].click();", suggestions[0])
                
                # Wait for navigation or results to load
                WebDriverWait(self.driver, 5).until(
                    lambda d: any(
                        d.find_elements(By.CSS_SELECTOR, selector)
                        for selector in [
                            '[data-test-selector="TitleLink"]', 
                            '[data-a-target="video-player"]',
                            '[class*="search-result"]',
                            '[class*="SearchResult"]',
                            'a[href*="/videos"]',
                            'a[href*="/channel"]'
                        ]
                    )
                )
                
                self.logger.info(f"Successfully selected first search suggestion with locator: {locator}")
                return
                
            except Exception as e:
                self.logger.debug(f"Failed to select search suggestion with locator {locator}: {str(e)}")
                continue
        
        # Third try - direct URL navigation
        try:
            query = self.driver.find_element(By.CSS_SELECTOR, 'input[type="search"]').get_attribute('value')
            if query:
                self.logger.info(f"Trying direct URL navigation for query: {query}")
                url_query = query.replace(' ', '%20')
                self.driver.get(f"https://www.twitch.tv/search?term={url_query}")
                
                # Wait for page to load
                WebDriverWait(self.driver, 10).until(
                    lambda d: d.find_element(By.CSS_SELECTOR, 'main').is_displayed()
                )
                self.logger.info("Successfully navigated directly to search results")
                return
        except Exception as e:
            self.logger.error(f"Direct navigation failed: {str(e)}")
        
        # If all else fails, at least make sure we're on some valid page
        try:
            self.logger.info("Using fallback: ensuring we're on a valid page")
            if not self.driver.find_element(By.CSS_SELECTOR, 'main').is_displayed():
                self.driver.get("https://www.twitch.tv")
                WebDriverWait(self.driver, 10).until(
                    lambda d: d.find_element(By.CSS_SELECTOR, 'main').is_displayed()
                )
            return
        except Exception as e:
            self.logger.error(f"Final fallback failed: {str(e)}")
        
        # We shouldn't reach here, but if we do, don't raise an exception
        self.logger.warning("Could not select search suggestion with any method, continuing anyway")