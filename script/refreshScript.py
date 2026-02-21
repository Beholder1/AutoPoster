import random
from typing import List

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from script.baseScript import BaseScript


class RefreshScript(BaseScript):
    LOGIN_URL = "https://facebook.com"
    MARKETPLACE_URL = "https://www.facebook.com/marketplace/selling/renew_listings"

    def __init__(self, db, accounts: List[str], incognito: bool, refresh: bool):
        super().__init__(db)
        options = self.get_options(incognito)

        random.shuffle(accounts)

        accountsWithErrors = []
        for account in accounts:
            driver = webdriver.Chrome(options=options)
            try:
                # Logowanie
                self.facebook_login(driver, account)

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
