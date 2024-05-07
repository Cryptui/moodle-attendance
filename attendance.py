from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from datetime import datetime
import logging
import os

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Browser options
opts = FirefoxOptions()
opts.add_argument("--headless")  # Add the headless argument explicitly

# Function to determine holidays
def is_holiday(date):
    holidays = [
        datetime(date.year, 1, 1).date(),  # New Year's Day
        datetime(date.year, 5, 1).date(),  # Labor Day
        datetime(date.year, 5, 9).date(),  # Holiday
        datetime(date.year, 12, 25).date(),  # Christmas
    ]
    return date.date() in holidays

# Function to check attendance
def check_attendance(username, password):
    today = datetime.now()
    if is_holiday(today):
        logging.info("Today is a holiday. No attendance check needed.")
        return

    with webdriver.Firefox(options=opts) as driver:
        driver.set_page_load_timeout(30)  # Ensure a numeric page load timeout
        try:
            driver.get("https://moodle.becode.org/login/index.php")
            
            username_field = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            username_field.send_keys(username)
            
            password_field = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "password"))
            )
            password_field.send_keys(password)
            
            login_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "loginbtn"))
            )
            login_button.click()
            
            driver.get("https://moodle.becode.org/mod/attendance/view.php?id=90")

            check_in_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@class='btn btn-primary' and contains(text(), 'Check in')]"))
            )
            check_in_button.click()

            location_dropdown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "id_location")))
            select = Select(location_dropdown)
            current_day = datetime.now().strftime("%A")
            if current_day in ["Monday", "Thursday"]:
                select.select_by_value("oncampus")
            else:
                select.select_by_value("athome")

            save_changes_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "id_submitbutton")))
            save_changes_button.click()
            
            logging.info("Attendance checked successfully.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            filename = f"debug_screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            driver.save_screenshot(filename)
            logging.info(f"Screenshot saved as {filename}")

# Retrieve username and password from environment variables
moodle_username = os.getenv('MOODLE_USERNAME', 'default_username')
moodle_password = os.getenv('MOODLE_PASSWORD', 'default_password')

check_attendance(moodle_username, moodle_password)
