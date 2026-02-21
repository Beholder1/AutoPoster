import random
import time
from selenium import webdriver
from selenium.webdriver import EdgeOptions, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class BaseScript:
    def __init__(self, db):
        self.db = db

    def get_options(self, incognito: bool):
        options = EdgeOptions()
        options.add_argument("--disable-infobars")
        options.add_argument("start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-search-engine-choice-screen")
        if incognito:
            options.add_argument("--incognito")
        # Pass the argument 1 to allow and 2 to block
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2
        })
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

        email_elem = driver.find_element(By.XPATH, "//input[@type='text']")
        self.human_type(driver, email_elem, self.db.getA("email", account_name))
        time.sleep(random.uniform(2, 5))

        password_elem = driver.find_element(By.XPATH, "//input[@type='password']")
        self.human_type(driver, password_elem, self.db.getA("password", account_name))
        time.sleep(random.uniform(2, 5))
        
        password_elem.send_keys(Keys.ENTER)
        time.sleep(4)
