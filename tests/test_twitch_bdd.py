"""BDD tests for Twitch mobile web application."""

import pytest
from pytest_bdd import scenarios

# Import step definitions
from tests.features.steps.twitch_steps import *

# Load scenarios from feature files
scenarios('features/twitch.feature')


class TestTwitchBDD:
    """Test class for Twitch BDD tests."""
    # The actual test logic is in the feature file and step definitions
    # This class serves as an entry point for pytest to discover and run the BDD tests
    
    # You can add custom setup/teardown here if needed
    def setup_method(self):
        """Setup method that runs before each test."""
        pass
        
    def teardown_method(self):
        """Teardown method that runs after each test."""
        pass 