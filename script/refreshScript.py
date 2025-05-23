import random
import time
from typing import List

from selenium import webdriver
from selenium.webdriver import ChromeOptions, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


class RefreshScript:
    LOGIN_URL = "https://facebook.com"
    MARKETPLACE_URL = "https://www.facebook.com/marketplace/selling/renew_listings"

    def __init__(self, db, accounts: List[str], incognito: bool, refresh: bool):
        self.db = db
        options = ChromeOptions()
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

        random.shuffle(accounts)

        def human_type(element, text):
            actions = ActionChains(driver)
            actions.move_to_element(element).click().perform()
            time.sleep(random.uniform(0.2, 0.5))
            for character in text:
                actions.send_keys(character).perform()
                time.sleep(random.uniform(0.1, 0.3))

        accountsWithErrors = []
        for account in accounts:
            driver = webdriver.Chrome(options=options)
            try:
                # Logowanie
                driver.get(self.LOGIN_URL)
                time.sleep(random.uniform(2, 5))
                cookies = driver.find_elements(By.XPATH, "//div[@role='button']")[-2]
                cookies.click()
                time.sleep(random.uniform(2, 5))
                email = driver.find_element(By.ID, "email")
                human_type(email, self.db.getA("email", account))
                time.sleep(random.uniform(2, 5))
                password = driver.find_element(By.ID, "pass")
                human_type(password, self.db.getA("password", account))
                time.sleep(random.uniform(2, 5))
                password.send_keys(Keys.ENTER)
                time.sleep(4)
                driver.get(self.MARKETPLACE_URL)
                while True:
                    refreshButtons = WebDriverWait(driver, 60).until(
                        ec.presence_of_all_elements_located((By.XPATH, "(//div[@aria-label='Odnów'])")))
                    if len(refreshButtons) == 0:
                        break
                    for refreshButton in refreshButtons:
                        refreshButton.click()
                    if not refresh:
                        break
                    driver.refresh()
                driver.quit()
            except BaseException as e:
                driver.quit()
                accountsWithErrors.append(account)
                print(e)
        if len(accountsWithErrors) > 0:
            print("Błąd podczas odświeżania ogłoszeń na kontach o nazwach: ", accountsWithErrors)
