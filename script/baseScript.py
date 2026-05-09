import os
import random
import sys
import time

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

if getattr(sys, 'frozen', False):
    PROJECT_ROOT: str = os.path.dirname(os.path.abspath(str(sys.executable)))
else:
    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class BaseScript:
    PROFILES_DIR = os.path.join(PROJECT_ROOT, 'profiles')

    def __init__(self, db):
        self.db = db
        os.makedirs(self.PROFILES_DIR, exist_ok=True)

    def start_driver(self, profile: str = None):
        options = self.get_options(profile)
        driver = webdriver.Chrome(options=options)
        real = None
        for handle in driver.window_handles:
            try:
                driver.switch_to.window(handle)
                driver.get_window_size()
                real = handle
                break
            except WebDriverException:
                continue
        if real is None:
            return driver
        driver.switch_to.window(real)
        return driver

    def get_options(self, profile: str = None):
        options = ChromeOptions()
        options.add_argument("--disable-infobars")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-search-engine-choice-screen")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-first-run")
        options.add_argument("--no-default-browser-check")
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
        )
        if profile:
            profile_path = os.path.join(self.PROFILES_DIR, profile)
            os.makedirs(profile_path, exist_ok=True)
            options.add_argument(f"--user-data-dir={profile_path}")
        # Pass the argument 1 to allow and 2 to block
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2
        })
        print(options.arguments)
        return options

    def facebook_login(self, driver, account_name):
        driver.get("https://facebook.com")
        time.sleep(random.uniform(2, 5))
        if not driver.find_elements(By.XPATH, "//input[@type='password']"):
            return True

        try:
            cookies = driver.find_elements(By.XPATH, "//div[@role='button']")[-2]
            cookies.click()
            time.sleep(random.uniform(2, 5))
        except Exception:
            pass

        try:
            email_elem = driver.find_element(By.XPATH, "//input[@type='text']")
            email_elem.send_keys(self.db.getA("email", account_name))

            password_elem = driver.find_element(By.XPATH, "//input[@type='password']")
            password_elem.send_keys(self.db.getA("password", account_name))

            password_elem.send_keys(Keys.ENTER)
            time.sleep(4)
        except Exception:
            pass

        print("Dokończ logowanie ręcznie (checkpoint/2FA) i zamknij przeglądarkę — "
              "sesja zapisze się w profilu i kolejne uruchomienia pójdą automatem.")
        while True:
            try:
                if not driver.window_handles:
                    break
            except WebDriverException:
                break
            time.sleep(1)
        return False
