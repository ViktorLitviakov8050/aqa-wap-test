"""Utilities package for the Twitch test automation framework"""

import os

# Define project directories
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOTS_DIR = os.path.join(PROJECT_ROOT, "reports", "screenshots")
LOGS_DIR = os.path.join(PROJECT_ROOT, "reports", "logs")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
CONFIG_DIR = os.path.join(PROJECT_ROOT, "config")

# Create directories if they don't exist
for directory in [SCREENSHOTS_DIR, LOGS_DIR, DATA_DIR, CONFIG_DIR]:
    os.makedirs(directory, exist_ok=True) 