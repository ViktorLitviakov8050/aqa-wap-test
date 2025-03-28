import json
import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


class DriverFactory:
    """Factory class to create WebDriver instances with mobile emulation"""
    
    @staticmethod
    def get_device_config(device_name="pixel_2"):
        """Load device configuration from devices.json file"""
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                 "config", "devices.json")
        
        with open(config_path, "r") as f:
            devices = json.load(f)
            
        if device_name not in devices:
            available_devices = ", ".join(devices.keys())
            logging.error(f"Device '{device_name}' not found. Available devices: {available_devices}")
            raise ValueError(f"Device '{device_name}' not found in configuration")
            
        logging.info(f"Using device configuration: {device_name}")
        return devices[device_name]
    
    @staticmethod
    def create_driver(device_name="pixel_2", browser_type="chrome", headless=False):
        """Create and configure a WebDriver instance based on device and browser type
        
        Args:
            device_name (str): Name of the device to emulate (must exist in devices.json)
            browser_type (str): Type of browser to use ('chrome' or 'firefox')
            headless (bool): Whether to run the browser in headless mode
            
        Returns:
            WebDriver: Configured WebDriver instance
        """
        browser_type = browser_type.lower()
        logging.info(f"Creating driver for {device_name} using {browser_type} browser (headless: {headless})")
        
        if browser_type == "chrome":
            return DriverFactory._create_chrome_driver(device_name, headless)
        elif browser_type == "firefox":
            return DriverFactory._create_firefox_driver(device_name, headless)
        else:
            logging.error(f"Browser type '{browser_type}' not supported")
            raise ValueError(f"Browser type '{browser_type}' not supported")
    
    @staticmethod
    def _create_chrome_driver(device_name, headless):
        """Create a Chrome WebDriver with mobile emulation settings"""
        device_config = DriverFactory.get_device_config(device_name)
        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("mobileEmulation", device_config)
        
        if headless:
            chrome_options.add_argument("--headless=new")
        
        # Additional options for better stability
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        
        try:
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Set window size slightly larger than the device dimensions to account for browser UI
            driver.set_window_size(
                device_config["width"] + 50, 
                device_config["height"] + 100
            )
            
            return driver
        except Exception as e:
            logging.error(f"Failed to create Chrome driver: {str(e)}")
            raise
    
    @staticmethod
    def _create_firefox_driver(device_name, headless):
        """Create a Firefox WebDriver with mobile emulation settings"""
        device_config = DriverFactory.get_device_config(device_name)
        
        firefox_options = webdriver.FirefoxOptions()
        
        # Set the user agent
        firefox_options.set_preference("general.useragent.override", device_config["userAgent"])
        
        if headless:
            firefox_options.add_argument("--headless")
        
        try:
            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=firefox_options)
            
            # Firefox doesn't support direct mobile emulation like Chrome,
            # so we set the window size to match the device dimensions
            driver.set_window_size(device_config["width"], device_config["height"])
            
            return driver
        except Exception as e:
            logging.error(f"Failed to create Firefox driver: {str(e)}")
            raise 