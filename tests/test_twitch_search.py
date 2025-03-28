import pytest
from pages.twitch_page import TwitchPage
from utils.gif_generator import GifGenerator
import logging
import time
import os

# Test data for parametrization
DEVICES = ["pixel_2", "iphone_12", "samsung_s20"]
BROWSERS = ["chrome", "firefox"]
SEARCH_QUERIES = ["StarCraft II", "League of Legends", "Dota 2"]

@pytest.mark.mobile
@pytest.mark.ui
@pytest.mark.search
@pytest.mark.parametrize("device", DEVICES)
@pytest.mark.parametrize("browser", BROWSERS)
@pytest.mark.parametrize("query", SEARCH_QUERIES)
class TestTwitchSearch:
    def test_search_and_select_streamer(self, driver, device, browser, query):
        """
        Test case to verify Twitch mobile search functionality:
        1. Navigate to Twitch
        2. Click search icon
        3. Search for query
        4. Scroll down twice
        5. Select a streamer
        6. Handle mature content popup if present
        7. Take screenshot of streamer page
        
        Args:
            driver: WebDriver instance
            device: Mobile device being emulated
            browser: Browser being used
            query: Search query to use
        """
        logger = logging.getLogger(__name__)
        logger.info(f'Starting Twitch search test on {device} device using {browser} browser')
        
        # Create screenshots directory for this test run
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        screenshots_dir = f'./screenshots/test_run_{device}_{browser}_{timestamp}'
        os.makedirs(screenshots_dir, exist_ok=True)
        
        try:
            # Initialize page and perform search flow
            twitch_page = TwitchPage(driver)
            twitch_page.navigate()
            driver.save_screenshot(f'{screenshots_dir}/01_home_page.png')
            
            # Search for content
            twitch_page.click_search()
            driver.save_screenshot(f'{screenshots_dir}/02_search_clicked.png')
            
            twitch_page.search_for(query)
            driver.save_screenshot(f'{screenshots_dir}/03_search_input.png')
            
            # Scroll down to see more results
            twitch_page.scroll_page(2, delay=1.5)
            driver.save_screenshot(f'{screenshots_dir}/04_scrolled_results.png')
            
            # Select a streamer and handle mature content
            twitch_page.select_streamer()
            driver.save_screenshot(f'{screenshots_dir}/05_streamer_selected.png')
            
            twitch_page.handle_mature_content()
            driver.save_screenshot(f'{screenshots_dir}/06_after_mature_content.png')
            
            # Take a screenshot of the result
            twitch_page.take_screenshot(f'streamer_page_{device}_{browser}_{query.replace(" ", "_")}')
            
            # Verify we're on a streamer's page (URL contains '/videos' or '/channel')
            assert any(x in driver.current_url for x in ['/videos', '/channel']), 'Not on streamer page'
            
            # Generate GIF from screenshots
            gif_generator = GifGenerator()
            gif_path = gif_generator.create_gif_from_screenshots(
                screenshots_dir,
                f'twitch_search_{device}_{browser}_{query.replace(" ", "_")}',
                duration=1000  # 1 second per frame
            )
            
            logger.info(f'Test completed successfully on {device} device using {browser} browser')
            logger.info(f'GIF created at: {gif_path}')
            
        except Exception as e:
            logger.error(f'Test failed on {device} device using {browser} browser: {str(e)}')
            # Take a screenshot on failure
            if driver:
                driver.save_screenshot(f'{screenshots_dir}/failure.png')
            raise