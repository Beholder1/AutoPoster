import random
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from script.baseScript import BaseScript


class RefreshScript(BaseScript):
    LOGIN_URL = "https://facebook.com"
    MARKETPLACE_URL = "https://www.facebook.com/marketplace/selling/renew_listings/?is_routable_dialog=true"

    def __init__(self, db, accounts: List[str], refresh: bool):
        super().__init__(db)

        random.shuffle(accounts)

        accounts_with_errors = []
        for account in accounts:
            profile = self.db.getA("profile", account)
            driver = self.start_driver(profile)
            try:
                # Logowanie
                if not self.facebook_login(driver, account):
                    try:
                        driver.quit()
                    except Exception:
                        pass
                    continue

                driver.get(self.MARKETPLACE_URL)
                while True:
                    refresh_buttons = WebDriverWait(driver, 60).until(
                        ec.presence_of_all_elements_located((By.XPATH, "(//div[@aria-label='Odnów'])")))
                    if len(refresh_buttons) == 0:
                        break
                    for refresh_button in refresh_buttons:
                        refresh_button.click()
                    if not refresh:
                        break
                    driver.refresh()
                driver.quit()
            except BaseException as e:
                driver.quit()
                accounts_with_errors.append(account)
                print(e)
        if len(accounts_with_errors) > 0:
            print("Błąd podczas odświeżania ogłoszeń na kontach o nazwach: ", accounts_with_errors)
