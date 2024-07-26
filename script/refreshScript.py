import random
import time

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class RefreshScript:
    def __init__(self, db, accounts, incognito):
        PATH = "driver/chromedriver.exe"
        self.db = db
        option = ChromeOptions()
        option.add_argument("--disable-infobars")
        option.add_argument("start-maximized")
        option.add_argument("--disable-extensions")
        if incognito != 0:
            option.add_argument("--incognito")
        # Pass the argument 1 to allow and 2 to block
        option.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2
        })

        random.shuffle(accounts)

        accountsWithErrors = []
        for account in accounts:
            driver = webdriver.Chrome(options=option)
            try:
                # Logowanie
                driver.get("https://facebook.com")
                email = driver.find_element(By.ID, "email")
                email.send_keys(self.db.getA("email", account))
                password = driver.find_element(By.ID, "pass")
                password.send_keys(self.db.getA("password", account))
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
                    driver.refresh()
                driver.quit()
            except BaseException as e:
                driver.quit()
                accountsWithErrors.append(account)
                print(e)
        if len(accountsWithErrors) > 0:
            print("Błąd podczas odświeżania ogłoszeń na kontach o nazwach: ", accountsWithErrors)
