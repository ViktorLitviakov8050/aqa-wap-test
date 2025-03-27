# AQA Home Test - Plan for WAP Testing (Twitch) ✅

## Repository 📁
`aqa-wap-test`

## Goal 📌
Automate a mobile web scenario on Twitch using Selenium in Python.

## Steps to Implement ✅

### 1. Initialize the Project
- Create GitHub repo: `aqa-wap-test`
- Create virtual environment and install:
  - selenium
  - pytest
  - python-dotenv (optional)
- Create folders: 
  - `pages/` 
  - `tests/` 
  - `screenshots/` 
  - `config/`

### 2. Configure Chrome Mobile Emulation
- Set up ChromeOptions in Selenium to emulate a mobile device (e.g. Pixel 2)

### 3. Create Base Page Class
- Utilities for:
  - click
  - find_element
  - input_text
  - scroll_page
  - handle_popup
  - take_screenshot

### 4. Create Page Object(s)
- TwitchHomePage
- SearchResultsPage
- StreamerPage

### 5. Write Test Case Using Pytest
Steps:
- Go to Twitch mobile site
- Click search
- Enter "StarCraft II"
- Scroll down twice
- Click any streamer
- Handle modal popup (if present)
- Wait for video to load
- Take a screenshot

### 6. Add Logging & Error Handling

### 7. Generate GIF of Test Execution
- Use LICEcap or ScreenToGif

### 8. Create README
- Short project intro
- Embedded GIF
- Tech stack + folder structure

### 9. Push to GitHub & Send Link