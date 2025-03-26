import pytest
from pages.twitch_page import TwitchPage
import logging

@pytest.mark.mobile
class TestTwitchSearch:
    def test_search_and_select_streamer(self, driver):
        """
        Test case to verify Twitch mobile search functionality:
        1. Navigate to Twitch
        2. Click search icon
        3. Search for 'StarCraft II'
        4. Scroll down twice
        5. Select a streamer
        6. Handle mature content popup if present
        7. Take screenshot of streamer page
        """
        logger = logging.getLogger(__name__)
        logger.info('Starting Twitch search test')
        
        try:
            twitch_page = TwitchPage(driver)
            twitch_page.perform_search_flow('StarCraft II')
            
            # Verify we're on a streamer's page (URL contains '/videos')
            assert '/videos' in driver.current_url, 'Not on streamer page'
            logger.info('Test completed successfully')
            
        except Exception as e:
            logger.error(f'Test failed: {str(e)}')
            raise