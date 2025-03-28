from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException


class WaitUtils:
    """Custom wait utilities for more robust element interaction"""
    
    @staticmethod
    def wait_for_element_visible(driver, locator, timeout=10):
        """Wait for an element to be visible"""
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))
    
    @staticmethod
    def wait_for_element_clickable(driver, locator, timeout=10):
        """Wait for an element to be clickable"""
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))
    
    @staticmethod
    def wait_for_element_present(driver, locator, timeout=10):
        """Wait for an element to be present in the DOM"""
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))
    
    @staticmethod
    def wait_for_text_present(driver, locator, text, timeout=10):
        """Wait for element to contain specific text"""
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.text_to_be_present_in_element(locator, text))
    
    @staticmethod
    def wait_for_invisibility(driver, locator, timeout=10):
        """Wait for an element to become invisible"""
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.invisibility_of_element_located(locator))
    
    @staticmethod
    def wait_for_url_contains(driver, url_part, timeout=10):
        """Wait for URL to contain specific text"""
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.url_contains(url_part))
    
    @staticmethod
    def wait_with_ignored_exceptions(driver, locator, condition_method, timeout=10):
        """Wait with custom ignored exceptions for flaky elements"""
        ignored_exceptions = (StaleElementReferenceException,)
        wait = WebDriverWait(driver, timeout, ignored_exceptions=ignored_exceptions)
        return wait.until(condition_method(locator)) 