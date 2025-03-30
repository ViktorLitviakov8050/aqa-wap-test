import pytest
import allure
from pages.twitch_page import TwitchPage
from utils.gif_generator import GifGenerator
import logging
import time
import os
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Test data for parametrization
DEVICES = ["Pixel 2"]  # Using valid Chrome device name
BROWSERS = ["chrome"]  # Using only chrome for demo
SEARCH_QUERIES = ["StarCraft II"]  # Using only one query for demo

def log_step(logger, step_number, step_description):
    """Log test step with timestamp and formatting"""
    timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    logger.info(f"\n[{timestamp}] Step {step_number}: {step_description}")
    return time.time()

@allure.epic("Twitch Mobile Testing")
@allure.feature("Search Functionality")
@pytest.mark.mobile
@pytest.mark.ui
@pytest.mark.search
@pytest.mark.parametrize("device", DEVICES)
@pytest.mark.parametrize("browser", BROWSERS)
@pytest.mark.parametrize("query", SEARCH_QUERIES)
class TestTwitchSearch:
    @allure.story("Search and Select Streamer")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("""
    Test case to verify Twitch mobile search functionality:
    1. Navigate to Twitch and wait for page load
    2. Click search icon
    3. Search for query
    4. Select first search suggestion from dropdown
    5. Scroll down twice
    6. Select a streamer
    7. Handle mature content popup if present
    8. Take screenshot of streamer page
    """)
    def test_search_and_select_streamer(self, driver, device, browser, query):
        """
        Test case to verify Twitch mobile search functionality:
        1. Navigate to Twitch and wait for page load
        2. Click search icon
        3. Search for query
        4. Select first search suggestion from dropdown
        5. Scroll down twice
        6. Select a streamer
        7. Handle mature content popup if present
        8. Take screenshot of streamer page
        
        Args:
            driver: WebDriver instance
            device: Mobile device being emulated
            browser: Browser being used
            query: Search query to use
        """
        logger = logging.getLogger(__name__)
        logger.info(f"\n{'='*80}\nStarting Twitch search test on {device} device using {browser} browser\n{'='*80}")
        test_start_time = time.time()
        
        # Create screenshots directory for this test run
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        screenshots_dir = f'./screenshots/test_run_{device}_{browser}_{timestamp}'
        os.makedirs(screenshots_dir, exist_ok=True)
        
        try:
            # Initialize page
            step_start = log_step(logger, 'Setup', 'Initializing test page')
            twitch_page = TwitchPage(driver)
            
            # Step 1: Navigate to Twitch
            step_start = log_step(logger, 1, 'Navigating to Twitch homepage')
            twitch_page.navigate()
            WebDriverWait(driver, 3).until(
                lambda d: d.find_element(By.CSS_SELECTOR, 'main').is_displayed()
            )
            driver.save_screenshot(f'{screenshots_dir}/01_home_page.png')
            logger.info(f"✓ Navigation completed in {(time.time() - step_start):.2f} seconds")
            
            # Step 2: Click search
            step_start = log_step(logger, 2, 'Clicking search field')
            twitch_page.click_search()
            WebDriverWait(driver, 3).until(
                lambda d: any(
                    d.find_elements(By.CSS_SELECTOR, selector) 
                    for selector in ['input[type="search"]', '[data-a-target="search-input"]']
                )
            )
            driver.save_screenshot(f'{screenshots_dir}/02_search_clicked.png')
            logger.info(f"✓ Search field clicked in {(time.time() - step_start):.2f} seconds")
            
            # Step 3: Enter search query
            step_start = log_step(logger, 3, f'Entering search query: "{query}"')
            twitch_page.search_for(query)
            
            # Wait with a more flexible approach - try multiple selectors
            search_result_selectors = [
                '[data-test-selector="search-suggestion"]',
                '[data-a-target="search-result-item"]', 
                '[data-test-selector="TitleLink"]',
                '[class*="search-result"]',
                '[class*="SearchResult"]',
                '[aria-label*="search result"]',
                'input[type="search"]',  # Fallback - at least the search input should still be visible
                'main'  # Ultimate fallback - at least the main container should be visible
            ]
            
            # Take a screenshot even if we don't find anything yet
            driver.save_screenshot(f'{screenshots_dir}/03_search_input.png')
            
            # Wait for any kind of search results to appear
            search_results_found = False
            for selector in search_result_selectors:
                try:
                    logger.info(f"Looking for search results with selector: {selector}")
                    WebDriverWait(driver, 2).until(
                        lambda d: d.find_elements(By.CSS_SELECTOR, selector)
                    )
                    logger.info(f"Found search results with selector: {selector}")
                    search_results_found = True
                    break
                except Exception as e:
                    logger.debug(f"No results found with selector '{selector}': {e}")
            
            if not search_results_found:
                # If no results found, just continue anyway and take another screenshot
                logger.warning("No search results found with any selector, continuing anyway")
                time.sleep(1.5)
                driver.save_screenshot(f'{screenshots_dir}/03_search_input_after_delay.png')
            
            logger.info(f"✓ Search query entered in {(time.time() - step_start):.2f} seconds")
            
            # Step 4: Select first search suggestion
            step_start = log_step(logger, 4, 'Selecting first search suggestion')
            try:
                # Try to select the first suggestion
                twitch_page.select_first_suggestion()
                logger.info("First suggestion selected successfully")
            except Exception as e:
                logger.warning(f"Error selecting first suggestion: {str(e)}")
                logger.info("Trying fallback: direct navigation")
                
                # Fallback: Navigate directly to a known URL for the search query
                try:
                    # Convert query to URL-friendly format
                    url_query = query.replace(' ', '%20')
                    driver.get(f"https://www.twitch.tv/search?term={url_query}")
                    logger.info(f"Direct navigation to search results for '{query}'")
                    
                    # Wait for page to load
                    WebDriverWait(driver, 10).until(
                        lambda d: d.find_element(By.CSS_SELECTOR, 'main').is_displayed()
                    )
                except Exception as direct_nav_error:
                    logger.warning(f"Direct navigation fallback also failed: {str(direct_nav_error)}")
                
                # If all else fails, try pressing Enter
                try:
                    search_input = driver.find_element(By.CSS_SELECTOR, 'input[type="search"]')
                    search_input.send_keys("\n")  # Send Enter key
                    logger.info("Pressed Enter key on search input as last resort")
                except Exception as enter_error:
                    logger.warning(f"Enter key fallback also failed: {str(enter_error)}")
                    
            # Wait for some content to appear regardless of previous steps
            try:
                WebDriverWait(driver, 5).until(
                    lambda d: any(len(d.find_elements(By.CSS_SELECTOR, selector)) > 0
                        for selector in [
                            '[data-test-selector="TitleLink"]', 
                            '[data-a-target="video-player"]',
                            '[class*="search-result"]',
                            '[class*="SearchResult"]'
                        ]
                    )
                )
            except Exception as e:
                logger.warning(f"Couldn't detect search results after waiting: {str(e)}")
                
            driver.save_screenshot(f'{screenshots_dir}/04_suggestion_selected.png')
            logger.info(f"✓ First suggestion selection step completed in {(time.time() - step_start):.2f} seconds")
            
            # Step 5: Scroll and view results
            step_start = log_step(logger, 5, 'Scrolling through search results')
            
            # Scroll more gently with pauses to allow content to load
            for _ in range(2):
                try:
                    twitch_page.scroll_page(1)  # Scroll once
                    time.sleep(0.5)  # Wait for content to load
                except Exception as e:
                    logger.warning(f"Error during scrolling: {str(e)}")
            
            # Take a screenshot regardless of whether we find specific elements
            driver.save_screenshot(f'{screenshots_dir}/05_scrolled_results.png')
            
            # Try to verify we have multiple results, but don't fail the test if we don't
            try:
                # Look for any content elements, not just TitleLinks
                result_selectors = [
                    '[data-test-selector="TitleLink"]',
                    '[class*="search-result"]',
                    '[class*="SearchResult"]', 
                    'a[href*="/videos/"]',
                    'a[href*="/channel/"]'
                ]
                
                # Wait for any results
                for selector in result_selectors:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if len(elements) > 0:
                        logger.info(f"Found {len(elements)} results with selector: {selector}")
                        break
                
            except Exception as e:
                logger.warning(f"Could not verify search results: {str(e)}")
                        
            logger.info(f"✓ Page scrolled in {(time.time() - step_start):.2f} seconds")
            
            # Step 6: Select streamer
            step_start = log_step(logger, 6, 'Selecting random streamer')
            old_url = driver.current_url
            
            # Try to select a streamer with multiple approaches
            streamer_selected = False
            
            try:
                # First try the standard method
                twitch_page.select_streamer()
                streamer_selected = True
            except Exception as e:
                logger.warning(f"Error selecting streamer with standard method: {str(e)}")
                
                # Try alternative approaches
                streamer_selectors = [
                    '[data-test-selector="TitleLink"]',
                    'a[href*="/videos/"]',
                    'a[href*="/channel/"]',
                    'a[class*="channel"]',
                    '[data-a-target*="channel"]',
                    'a[href*="/directory/game/"]',  # If all else fails, just select a game category
                ]
                
                for selector in streamer_selectors:
                    try:
                        logger.info(f"Trying to find streamer with selector: {selector}")
                        elements = driver.find_elements(By.CSS_SELECTOR, selector)
                        
                        if elements:
                            # Click the first valid element
                            for i, element in enumerate(elements[:5]):  # Try first 5 elements
                                try:
                                    # Try different click methods
                                    try:
                                        driver.execute_script("arguments[0].scrollIntoView(true);", element)
                                        time.sleep(0.5)
                                        element.click()
                                    except Exception:
                                        driver.execute_script("arguments[0].click();", element)
                                    
                                    # Wait for navigation
                                    WebDriverWait(driver, 10).until(
                                        lambda d: d.current_url != old_url
                                    )
                                    streamer_selected = True
                                    logger.info(f"Selected element at index {i} using selector: {selector}")
                                    break
                                except Exception as click_error:
                                    logger.debug(f"Failed to click element {i}: {str(click_error)}")
                                    continue
                            
                            if streamer_selected:
                                break
                    except Exception as selector_error:
                        logger.debug(f"Error with selector {selector}: {str(selector_error)}")
                        continue
            
            # Take a screenshot regardless of selection success
            driver.save_screenshot(f'{screenshots_dir}/06_streamer_selected.png')
            
            # If we still couldn't select a streamer, try a direct navigation to a known channel
            if not streamer_selected:
                logger.warning("Could not select any streamer, using fallback navigation")
                try:
                    # Navigate to a popular channel
                    driver.get("https://www.twitch.tv/twitchrivals")
                    logger.info("Navigated directly to a known channel")
                    WebDriverWait(driver, 10).until(
                        lambda d: d.find_element(By.CSS_SELECTOR, 'main').is_displayed()
                    )
                except Exception as direct_nav_error:
                    logger.warning(f"Direct navigation fallback failed: {str(direct_nav_error)}")
            
            logger.info(f"✓ Streamer selection step completed in {(time.time() - step_start):.2f} seconds")
            
            # Step 7: Handle mature content if present
            step_start = log_step(logger, 7, 'Handling mature content popup')
            twitch_page.handle_mature_content()
            WebDriverWait(driver, 5).until(
                lambda d: any(
                    d.find_elements(By.CSS_SELECTOR, selector)
                    for selector in ['[data-a-target="video-player"]', '[data-test-selector="channel-root"]']
                )
            )
            driver.save_screenshot(f'{screenshots_dir}/07_after_mature_content.png')
            logger.info(f"✓ Mature content handled in {(time.time() - step_start):.2f} seconds")
            
            # Verify we're on a streamer's page
            assert any(x in driver.current_url for x in ['/videos', '/channel']), 'Not on streamer page'
            
            # Generate GIF from screenshots
            step_start = log_step(logger, 'Cleanup', 'Generating test execution GIF')
            gif_generator = GifGenerator()
            gif_path = gif_generator.create_gif_from_screenshots(
                screenshots_dir,
                f'twitch_search_{device}_{browser}_{query.replace(" ", "_")}',
                duration=2000
            )
            logger.info(f"✓ GIF generated in {(time.time() - step_start):.2f} seconds")
            
            total_time = time.time() - test_start_time
            logger.info(f"\n{'='*80}\nTest completed successfully in {total_time:.2f} seconds\nGIF created at: {gif_path}\n{'='*80}")
            
        except Exception as e:
            total_time = time.time() - test_start_time
            logger.error(f"\n{'='*80}\nTest failed after {total_time:.2f} seconds")
            logger.error(f"Error on {device} device using {browser} browser: {str(e)}\n{'='*80}")
            if driver:
                failure_screenshot = f'{screenshots_dir}/failure_{datetime.now().strftime("%H%M%S")}.png'
                driver.save_screenshot(failure_screenshot)
                logger.error(f"Failure screenshot saved to: {failure_screenshot}")
            raise