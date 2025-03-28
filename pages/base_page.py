from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
from typing import Any, List, Tuple, Union
from utils.exceptions import ElementNotFoundError, ElementNotClickableError
from utils.retry import retry_on_exception
import yaml
import logging
import time

class BasePage:
    def __init__(self, driver: Any) -> None:
        """Initialize base page with WebDriver instance"""
        self.driver = driver
        with open('config/config.yaml', 'r') as file:
            self.config = yaml.safe_load(file)
        self.wait = WebDriverWait(driver, self.config['waits']['explicit'])
        self.logger = logging.getLogger(__name__)
    
    @retry_on_exception()
    def find_element(self, locator: Union[Tuple, By, str], value: str = None, timeout: int = None) -> Any:
        """
        Find element with explicit wait and flexible locator format
        
        Args:
            locator: Locator in tuple format (By.ID, 'id_value') or By object
            value: Element identifier (used only if locator is a By object)
            timeout: Custom timeout in seconds, defaults to explicit wait config
            
        Returns:
            WebElement: Found element
            
        Raises:
            ElementNotFoundError: If element cannot be found
        """
        timeout = timeout or self.config['waits']['explicit']
        
        # Handle different locator formats
        if isinstance(locator, tuple) and len(locator) == 2:
            by, val = locator
        else:
            by, val = locator, value
            
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, val))
            )
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.error(f"Failed to find element {by}='{val}': {str(e)}")
            raise ElementNotFoundError(f"Element {by}='{val}' not found: {str(e)}")
    
    @retry_on_exception()
    def find_elements(self, locator: Union[Tuple, By, str], value: str = None, timeout: int = None) -> List:
        """
        Find all elements matching locator
        
        Args:
            locator: Locator in tuple format (By.ID, 'id_value') or By object
            value: Element identifier (used only if locator is a By object)
            timeout: Custom timeout in seconds, defaults to explicit wait config
            
        Returns:
            List[WebElement]: List of found elements
            
        Raises:
            ElementNotFoundError: If no elements are found
        """
        timeout = timeout or self.config['waits']['explicit']
        
        # Handle different locator formats
        if isinstance(locator, tuple) and len(locator) == 2:
            by, val = locator
        else:
            by, val = locator, value
            
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((by, val))
            )
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.error(f"Failed to find elements {by}='{val}': {str(e)}")
            raise ElementNotFoundError(f"Elements {by}='{val}' not found: {str(e)}")
    
    @retry_on_exception()
    def click_element(self, element: Any) -> None:
        """
        Click element with retry mechanism
        
        Args:
            element: WebElement to click
            
        Raises:
            ElementNotClickableError: If element cannot be clicked
        """
        try:
            element.click()
        except Exception as e:
            self.logger.error(f"Failed to click element: {str(e)}")
            raise ElementNotClickableError(f"Element not clickable: {str(e)}")
    
    def click(self, locator: Union[Tuple, By, str], value: str = None, timeout: int = None) -> None:
        """
        Click element with explicit wait
        
        Args:
            locator: Locator in tuple format (By.ID, 'id_value') or By object
            value: Element identifier (used only if locator is a By object)
            timeout: Custom timeout in seconds, defaults to explicit wait config
        """
        element = self.find_element(locator, value, timeout)
        try:
            element.click()
            self.logger.debug(f"Clicked element {locator}")
        except Exception as e:
            self.logger.warning(f"Standard click failed, trying alternative methods: {str(e)}")
            self.click_with_js(element)
    
    def click_with_js(self, element: Any = None, locator: Union[Tuple, By, str] = None, value: str = None) -> None:
        """
        Click element using JavaScript executor
        
        Args:
            element: WebElement to click (optional)
            locator: Locator in tuple format (By.ID, 'id_value') or By object (optional)
            value: Element identifier (used only if locator is a By object)
            
        Note: Either element OR locator must be provided
        """
        if element is None and locator is not None:
            element = self.find_element(locator, value)
            
        try:
            self.driver.execute_script("arguments[0].click();", element)
            self.logger.debug("Clicked element with JavaScript")
        except Exception as e:
            self.logger.error(f"JavaScript click failed: {str(e)}")
            raise
    
    def click_with_actions(self, element: Any = None, locator: Union[Tuple, By, str] = None, value: str = None) -> None:
        """
        Click element using ActionChains
        
        Args:
            element: WebElement to click (optional)
            locator: Locator in tuple format (By.ID, 'id_value') or By object (optional)
            value: Element identifier (used only if locator is a By object)
            
        Note: Either element OR locator must be provided
        """
        if element is None and locator is not None:
            element = self.find_element(locator, value)
            
        try:
            actions = ActionChains(self.driver)
            actions.move_to_element(element).click().perform()
            self.logger.debug("Clicked element with ActionChains")
        except Exception as e:
            self.logger.error(f"ActionChains click failed: {str(e)}")
            raise
    
    def input_text(self, locator: Union[Tuple, By, str], text: str, value: str = None, clear_first: bool = True) -> None:
        """
        Input text into element
        
        Args:
            locator: Locator in tuple format (By.ID, 'id_value') or By object
            text: Text to input
            value: Element identifier (used only if locator is a By object)
            clear_first: Whether to clear the field before typing
        """
        element = self.find_element(locator, value)
        try:
            if clear_first:
                element.clear()
            element.send_keys(text)
            self.logger.debug(f"Input text: '{text}'")
        except Exception as e:
            self.logger.error(f"Failed to input text: {str(e)}")
            raise
    
    def scroll_page(self, times: int = 1, delay: float = 1.0) -> None:
        """
        Scroll page to bottom specified number of times
        
        Args:
            times: Number of times to scroll
            delay: Delay between scrolls in seconds
        """
        for i in range(times):
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(delay)
            self.logger.info(f'Scrolled page {i + 1} time(s)')
    
    def scroll_to_element(self, element: Any = None, locator: Union[Tuple, By, str] = None, value: str = None) -> None:
        """
        Scroll to make element visible
        
        Args:
            element: WebElement to scroll to (optional)
            locator: Locator in tuple format (By.ID, 'id_value') or By object (optional)
            value: Element identifier (used only if locator is a By object)
            
        Note: Either element OR locator must be provided
        """
        if element is None and locator is not None:
            element = self.find_element(locator, value)
            
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            time.sleep(0.5)  # Small delay to let the scroll complete
            self.logger.debug("Scrolled to element")
        except Exception as e:
            self.logger.error(f"Failed to scroll to element: {str(e)}")
            raise
    
    def scroll_by(self, x_pixels: int = 0, y_pixels: int = 0) -> None:
        """
        Scroll by a specific amount of pixels
        
        Args:
            x_pixels: Horizontal scroll amount in pixels
            y_pixels: Vertical scroll amount in pixels
        """
        try:
            self.driver.execute_script(f"window.scrollBy({x_pixels}, {y_pixels});")
            self.logger.debug(f"Scrolled by x:{x_pixels}, y:{y_pixels} pixels")
        except Exception as e:
            self.logger.error(f"Failed to scroll: {str(e)}")
            raise
    
    def take_screenshot(self, name: str) -> str:
        """
        Take screenshot and save it to configured path
        
        Args:
            name: Name for the screenshot file (without extension)
            
        Returns:
            str: Path to the saved screenshot
        """
        path = f"{self.config['screenshots']['path']}/{name}.png"
        try:
            self.driver.save_screenshot(path)
            self.logger.info(f'Screenshot saved to {path}')
            return path
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {str(e)}")
            raise
    
    def handle_popup(self, locator: Union[Tuple, By, str], value: str = None, timeout: int = 5) -> bool:
        """
        Handle popup if present by clicking on it
        
        Args:
            locator: Locator in tuple format (By.ID, 'id_value') or By object
            value: Element identifier (used only if locator is a By object)
            timeout: Custom timeout for popup appearance in seconds
            
        Returns:
            bool: True if popup was handled, False if not found
        """
        # Standardize locator format
        if not isinstance(locator, tuple):
            locator = (locator, value)
            
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            element.click()
            self.logger.info('Popup handled successfully')
            return True
        except TimeoutException:
            self.logger.info('No popup found within timeout period')
            return False
        except Exception as e:
            self.logger.warning(f'Error handling popup: {str(e)}')
            return False
    
    def wait_for_element_visible(self, locator: Union[Tuple, By, str], value: str = None, timeout: int = None) -> Any:
        """
        Wait for element to be visible
        
        Args:
            locator: Locator in tuple format (By.ID, 'id_value') or By object
            value: Element identifier (used only if locator is a By object)
            timeout: Custom timeout in seconds, defaults to explicit wait config
            
        Returns:
            WebElement: The visible element
        """
        timeout = timeout or self.config['waits']['explicit']
        
        # Standardize locator format
        if not isinstance(locator, tuple):
            locator = (locator, value)
            
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException as e:
            self.logger.error(f"Element not visible within timeout: {str(e)}")
            raise
    
    def wait_for_url_contains(self, text: str, timeout: int = None) -> bool:
        """
        Wait for URL to contain specific text
        
        Args:
            text: Text that URL should contain
            timeout: Custom timeout in seconds, defaults to explicit wait config
            
        Returns:
            bool: True if condition was met within timeout
        """
        timeout = timeout or self.config['waits']['explicit']
        
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.url_contains(text)
            )
        except TimeoutException as e:
            self.logger.error(f"URL did not contain '{text}' within timeout: {str(e)}")
            raise
    
    def is_element_present(self, locator: Union[Tuple, By, str], value: str = None, timeout: int = 3) -> bool:
        """
        Check if element is present on the page
        
        Args:
            locator: Locator in tuple format (By.ID, 'id_value') or By object
            value: Element identifier (used only if locator is a By object)
            timeout: Custom timeout in seconds for quick check
            
        Returns:
            bool: True if element is present, False otherwise
        """
        # Standardize locator format
        if not isinstance(locator, tuple):
            locator = (locator, value)
            
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False