#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging.config

logger = logging.getLogger(__name__)

# Set up ChromeDriver
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_service = ChromeService(ChromeDriverManager().install())

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

def get_product_info(url: str):
    """
    Get product info from a product page
    """
    try:
        driver.get(url)
        time.sleep(3)
        product_name = driver.find_element(By.CSS_SELECTOR, "[class*='title--wrap']").text
        product_price = driver.find_element(By.CSS_SELECTOR, "[class*='product-price-current'], [class*='price--current']").text
        return product_name, product_price

    except Exception as e:
        logger.error(f'Error getting product info: {e}')
        return None, None
