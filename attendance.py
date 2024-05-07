import logging
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.remote.remote_connection import LOGGER as selenium_logger
from datetime import datetime, timezone
import os

# Configure logging
selenium_logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Browser options
options = Options()
options.headless = True  # Run in headless mode

def is_holiday(date):
    holidays = [
        datetime(date.year, 1, 1).date(),  # New Year's Day
        datetime(date.year, 5, 1).date(),  # Labor Day
        datetime(date.year, 5, 9).date(),  # Holiday
        datetime(date.year, 5, 10).date(),  # Bridge
        datetime(date.year, 12, 25).date(),  # Christmas
    ]
    return date.date() in holidays

def get_numeric_timeout(value, default=10):
    """Ensure a timeout value is numeric, returning a default if not."""
    try:
        return float(value)  # Convert to float (or int)
    except ValueError:
        return default

def check_attendance(username, password):
    today = datetime.now()
    if is_holiday(today):
        logging.info("Today is a holiday. No attendance check needed.")
        return

    # Define numeric timeouts explicitly
    page_load_timeout = get_numeric_timeout(30)
    webdriver_wait_timeout = get_numeric_timeout(20)
    click_timeout = get_numeric_timeout(10)

    with webdriver.Firefox(options=options) as driver:
        driver.set_page_load_timeout(page_load_timeout)  # Set page load timeout to a numeric value
        try:
            driver.get("https://moodle.becode.org/login/index.php")
            
            username_field = WebDriverWait(driver, webdriver_wait_timeout).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            username_field.send_keys(username)
            
            password_field = WebDriverWait(driver, webdriver_wait_timeout).until(
                EC.presence_of_element_located((By.ID, "password"))
            )
            password_field.send_keys(password)
            
            login_button = WebDriverWait(driver, webdriver_wait_timeout).until(
                EC.element_to_be_clickable((By.ID, "loginbtn"))
            )
            login_button.click()
            
            # Navigate to the attendance page
            driver.get("https://moodle.becode.org/mod/attendance/view.php?id=90")

            check_in_button = WebDriverWait(driver, click_timeout).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@class='btn btn-primary' and contains(text(), 'Check in')]"))
            )
            check_in_button.click()

            location_dropdown = WebDriverWait(driver, click_timeout).until(EC.presence_of_element_located((By.ID, "id_location")))
            select = Select(location_dropdown)
            current_day = datetime.now().strftime("%A")
            if current_day in ["Monday", "Thursday"]:
                select.select_by_value("oncampus")
            else:
                select.select_by_value("athome")

            save_changes_button = WebDriverWait(driver, click_timeout).until(EC.element_to_be_clickable((By.ID, "id_submitbutton")))
            save_changes_button.click()
            
            logging.info("Attendance checked successfully.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            filename = f"debug_screenshot_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.png"
            driver.save_screenshot(filename)
            logging.info(f"Screenshot saved as {filename}")

# Retrieve username and password from environment variables
moodle_username = os.getenv('MOODLE_USERNAME', 'default_username')
moodle_password = os.getenv('MOODLE_PASSWORD', 'default_password')

check_attendance(moodle_username, moodle_password)
