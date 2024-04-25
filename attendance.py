import logging
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from datetime import datetime
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configure options for headless browser
options = Options()
options.headheadless = True

def is_holiday(date):
    holidays = [
        datetime(date.year, 5, 1),   # May 1
        datetime(date.year, 5, 9),   # May 9
        datetime(date.year, 5, 20),  # May 20
        *[datetime(date.year, 7, day) for day in range(8, 13)],  # July 8 till July 12
        datetime(date.year, 8, 15)   # August 15
    ]
    return date in holidays

def is_attendance_time():
    now = datetime.now()
    current_day = now.strftime("%A")
    current_time = now.strftime("%H:%M")
    login_time_ranges = [("09:00", "09:10"), ("13:30", "13:40")]
    if (current_day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"] and
            not is_holiday(now) and
            any(start <= current_time <= end for start, end in login_time_ranges)):
        return True
    return False

# Function to check attendance
def check_attendance(username, password):
    if is_attendance_time():
        try:
            driver = webdriver.Firefox(options=options)
            driver.get("https://moodle.becode.org/login/index.php")
            
            username_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "username")))
            username_field.send_keys(username)
            
            password_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "password")))
            password_field.send_keys(password)
            
            login_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "loginbtn")))
            login_button.click()
            
            # Navigate to attendance page
            driver.get("https://moodle.becode.org/mod/attendance/view.php?id=90")
            
            # Click the "Check in" button
            check_in_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@class='btn btn-primary' and contains(text(), 'Check in')]"))
            )
            check_in_button.click()

            # Select the location
            location_dropdown = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "id_location")))
            select = Select(location_dropdown)
            select.select_by_value("oncampus" if datetime.now().strftime("%A") in ["Monday", "Thursday"] else "athome")
            
            # Submit attendance
            save_changes_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "id_submitbutton")))
            save_changes_button.click()
            
            logging.info("Attendance checked successfully.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            # Save a screenshot for debugging
            driver.save_screenshot(f"debug_screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        finally:
            driver.quit()
    else:
        logging.info("It's not the time to check attendance.")

# Retrieve username and password from environment variables
moodle_username = os.getenv('MOODLE_USERNAME')
moodle_password = os.getenv('MOODLE_PASSWORD')
check_attendance(moodle_username, moodle_password)