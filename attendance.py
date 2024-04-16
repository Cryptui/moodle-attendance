from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from datetime import datetime
# from selenium.webdriver.common.keys import Keys  # Not needed with the revised approach

# Configure options for headless browser
options = Options()
options.headless = True

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
    login_time_ranges = [("09:01", "09:02"), ("13:31", "13:32")]
    if (current_day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"] and
            not is_holiday(now) and
            any(start <= current_time <= end for start, end in login_time_ranges)):
        return True
    return False

def check_attendance(username, password):
    if is_attendance_time():
        with webdriver.Firefox(options=options) as driver:
            driver.get("https://moodle.becode.org/login/index.php")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys(password)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "loginbtn"))).click()
            driver.get("https://moodle.becode.org/mod/attendance/view.php?id=90")
            
            # Attempt to find the "Check in" button using the class and text
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
            # Ensure the browser session is ended
            # driver.quit()


# Retrieve username 
moodle_username = 'MOODLE_USERNAME'
moodle_password = 'MOODLE_PASSWORD'
check_attendance(moodle_username, moodle_password)