import os
import logging.config
# import time
# import selenium.webdriver as webdriver
# from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By

load_dotenv()

AUTH = os.getenv('AUTH')
SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'

logger = logging.getLogger('scraper')

def scrape_website(website):
    logger.info("Launching Chrome Browser...")

    logger.debug(f"SBR_WEBDRIVER: {SBR_WEBDRIVER}")
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        logger.info('Connected! Navigating...')
        driver.get(website)
        # logger.info('Taking page screenshot to file page.png')
        # driver.get_screenshot_as_file('./page.png')
        # logger.info('Navigated! Scraping page content...')
        html = driver.page_source
        return html