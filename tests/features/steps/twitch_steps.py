import pytest
from pytest_bdd import given, when, then, parsers
import time
from pages.home_page import HomePage
from pages.search_page import SearchPage
from pages.streamer_page import StreamerPage
from utils.logging_utils import get_logger

# Initialize logger
logger = get_logger()

# Step Definitions
@given("I am on the Twitch mobile site")
def on_twitch_site(driver):
    """Navigate to Twitch mobile site."""
    logger.info("Navigating to Twitch mobile site")
    home_page = HomePage(driver)
    return home_page.navigate()

@when("I click on the search button")
def click_search(driver):
    """Click on the search button."""
    logger.info("Clicking on search button")
    home_page = HomePage(driver)
    return home_page.click_search()

@when(parsers.parse('I search for "{query}"'))
def search_for(driver, query):
    """Enter search query."""
    logger.info(f"Searching for: {query}")
    search_page = SearchPage(driver)
    return search_page.search_for(query)

@when(parsers.parse("I scroll down {count:d} times"))
def scroll_down(driver, count):
    """Scroll down a number of times."""
    logger.info(f"Scrolling down {count} times")
    search_page = SearchPage(driver)
    for _ in range(count):
        search_page.scroll_down()
        time.sleep(1)  # Small delay between scrolls
    return search_page

@then("I should see search results")
def should_see_results(driver):
    """Verify search results are displayed."""
    logger.info("Verifying search results")
    search_page = SearchPage(driver)
    assert search_page.has_results(), "Expected to see search results, but none found"
    return search_page

@then("I should see no results")
def should_see_no_results(driver):
    """Verify no search results are displayed."""
    logger.info("Verifying no search results")
    search_page = SearchPage(driver)
    assert search_page.has_no_results(), "Expected to see no results message, but results were found"
    return search_page

@then(parsers.parse("I should {result}"))
def should_have_expected_result(driver, result):
    """Handle different expected results based on the scenario outline."""
    logger.info(f"Checking for expected result: {result}")
    search_page = SearchPage(driver)
    
    if result == "see search results":
        assert search_page.has_results(), "Expected to see search results, but none found"
    elif result == "see no results":
        assert search_page.has_no_results(), "Expected to see no results message, but results were found"
    else:
        raise ValueError(f"Unknown result expectation: {result}")
    
    return search_page

@when("I click on a streamer")
def click_streamer(driver):
    """Click on the first streamer in search results."""
    logger.info("Clicking on streamer")
    search_page = SearchPage(driver)
    return search_page.click_streamer()

@then("I should handle mature content warning if present")
def handle_mature_content(driver):
    """Handle mature content warning if it appears."""
    logger.info("Handling any mature content warnings")
    streamer_page = StreamerPage(driver)
    return streamer_page.handle_mature_content_warning()

@then("the video should play")
def video_should_play(driver):
    """Verify video player is displayed and loaded."""
    logger.info("Verifying video is playing")
    streamer_page = StreamerPage(driver)
    streamer_page.wait_for_video_player()
    # Handle any modal popups that might appear
    streamer_page.handle_modal_popups()
    # Verify video player is visible
    assert streamer_page.is_element_visible(streamer_page.VIDEO_PLAYER), "Video player is not visible"
    return streamer_page

@then("I take a screenshot")
def take_screenshot(driver):
    """Take a screenshot of the current page."""
    logger.info("Taking screenshot")
    streamer_page = StreamerPage(driver)
    screenshot_path = streamer_page.take_screenshot()
    logger.info(f"Screenshot saved to: {screenshot_path}")
    return streamer_page 