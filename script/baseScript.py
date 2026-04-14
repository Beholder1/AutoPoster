import random
import time

from selenium.webdriver import ChromeOptions, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


import os

class BaseScript:
    USER_DATA_DIR = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Google', 'Chrome', 'User Data')

    def __init__(self, db):
        self.db = db

    def get_options(self, profile: str = None):
        options = ChromeOptions()
        options.add_argument("--disable-infobars")
        options.add_argument("start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-search-engine-choice-screen")
        options.add_argument("--remote-debugging-port=0")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        if profile:
            options.add_argument(f"--user-data-dir={self.USER_DATA_DIR}")
            options.add_argument(f"--profile-directory={profile}")
        # Pass the argument 1 to allow and 2 to block
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2
        })
        print(options.arguments)
        return options

    def human_type(self, driver, element, text):
        actions = ActionChains(driver)
        actions.move_to_element(element).click().perform()
        time.sleep(random.uniform(0.2, 0.5))
        for character in text:
            actions.send_keys(character).perform()
            time.sleep(random.uniform(0.1, 0.3))

    def facebook_login(self, driver, account_name):
        driver.get("https://facebook.com")
        time.sleep(random.uniform(2, 5))
        
        # Akceptacja ciasteczek
        try:
            cookies = driver.find_elements(By.XPATH, "//div[@role='button']")[-2]
            cookies.click()
            time.sleep(random.uniform(2, 5))
        except (IndexError, Exception):
            pass

        try:
            email_elem = driver.find_element(By.XPATH, "//input[@type='text']")
            self.human_type(driver, email_elem, self.db.getA("email", account_name))
            time.sleep(random.uniform(2, 5))

            password_elem = driver.find_element(By.XPATH, "//input[@type='password']")
            self.human_type(driver, password_elem, self.db.getA("password", account_name))
            time.sleep(random.uniform(2, 5))
            
            password_elem.send_keys(Keys.ENTER)
            time.sleep(4)
        except Exception:
            pass
