import random
import time

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


class RefreshScript:
    def __init__(self, db, accounts, incognito, refresh):
        self.db = db
        options = ChromeOptions()
        options.add_argument("--disable-infobars")
        options.add_argument("start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-search-engine-choice-screen")
        if incognito != 0:
            options.add_argument("--incognito")
        # Pass the argument 1 to allow and 2 to block
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2
        })

        random.shuffle(accounts)

        accountsWithErrors = []
        for account in accounts:
            driver = webdriver.Chrome(options=options)
            try:
                # Logowanie
                driver.get("https://facebook.com")
                email = driver.find_element(By.ID, "email")
                time.sleep(random.uniform(2, 5))
                email.send_keys(self.db.getA("email", account))
                password = driver.find_element(By.ID, "pass")
                time.sleep(random.uniform(2, 5))
                password.send_keys(self.db.getA("password", account))
                time.sleep(random.uniform(2, 5))
                password.send_keys(Keys.ENTER)
                time.sleep(4)
                driver.get("https://www.facebook.com/marketplace/selling/renew_listings")
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
