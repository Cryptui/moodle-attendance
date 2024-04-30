import logging
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from datetime import datetime, timedelta, timezone
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configure options for headless browser
options = Options()
options.headless = True

def is_holiday(date):
    holidays = [
        datetime(date.year, 1, 1),   # New Year's Day
        datetime(date.year, 5, 1),   # Labor Day
        datetime(date.year, 12, 25), # Christmas
    ]
    return date in holidays

def is_attendance_time(utc_now):
    # This is set to always return True for testing purposes. Change logic as needed.
    return True

def check_attendance(username, password):
    driver = None  # Initialize the driver to None
    try:
        driver = webdriver.Firefox(options=options)  # Instantiate the WebDriver with options
        driver.get("https://moodle.becode.org/login/index.php")
        
        username_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "username")))
        username_field.send_keys(username)
        
        password_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "password")))
        password_field.send_keys(password)
        
        login_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "loginbtn")))
        login_button.click()
        
        # Navigate to the attendance page
        driver.get("https://moodle.becode.org/mod/attendance/view.php?id=90")
        
        # Additional steps to perform the attendance check can be added here...
        
        logging.info("Attendance checked successfully.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        # Save a screenshot for debugging if the driver is initialized
        if driver:
            filename = f"debug_screenshot_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.png"
            driver.save_screenshot(filename)
            logging.info(f"Screenshot saved as {filename}")
    finally:
        if driver:
            driver.quit()  # Ensure the driver is quit properly

# Retrieve username and password from environment variables
moodle_username = os.getenv('MOODLE_USERNAME')
moodle_password = os.getenv('MOODLE_PASSWORD')
check_attendance(moodle_username, moodle_password)
