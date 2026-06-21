import random
import time
import traceback
from typing import List

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from script.baseScript import BaseScript


class ActivityScript(BaseScript):
    HOME_URL = "https://www.facebook.com/"

    # Reakcje pojawiające się w pasku po najechaniu na "Lubię to!" (polskie etykiety):
    # "Lubię to!" - kciuk w górę, "Super" - serduszko.
    REACTIONS = ["Lubię to!", "Super"]

    # Zabezpieczenie przed nieskończonym przewijaniem, gdy feed nie doładowuje nowych postów.
    MAX_EMPTY_SCROLLS = 10

    def __init__(self, db, accounts: List[str], number_of_posts: int):
        super().__init__(db)

        random.shuffle(accounts)

        accounts_with_errors = []
        for account in accounts:
            profile = self.db.get_or_create_profile(account, self.PROFILES_DIR)
            driver = self.start_driver(profile)
            try:
                # Logowanie
                if not self.facebook_login(driver, account):
                    try:
                        driver.quit()
                    except Exception:
                        pass
                    continue

                driver.get(self.HOME_URL)
                time.sleep(random.uniform(3, 6))

                reacted = 0
                processed = set()
                empty_scrolls = 0
                while reacted < number_of_posts and empty_scrolls < self.MAX_EMPTY_SCROLLS:
                    like_buttons = driver.find_elements(
                        By.XPATH, "//div[@aria-label='Lubię to!' and @role='button']")

                    progress = False
                    for like_button in like_buttons:
                        if reacted >= number_of_posts:
                            break
                        if like_button.id in processed:
                            continue
                        processed.add(like_button.id)
                        try:
                            driver.execute_script(
                                "arguments[0].scrollIntoView({block: 'center'});", like_button)
                            time.sleep(random.uniform(1, 2))

                            reaction = random.choice(self.REACTIONS)
                            if reaction == "Lubię to!":
                                like_button.click()
                            else:
                                # Najedź na "Lubię to!", aby rozwinąć pasek reakcji, a następnie kliknij serduszko.
                                ActionChains(driver).move_to_element(like_button).perform()
                                love = WebDriverWait(driver, 5).until(
                                    ec.element_to_be_clickable(
                                        (By.XPATH, "//div[@aria-label='Super' and @role='button']")))
                                love.click()

                            reacted += 1
                            progress = True
                            time.sleep(random.uniform(2, 4))
                        except Exception:
                            # Pojedynczy post może być nieklikany (reklama, znikający element) - pomiń go.
                            continue

                    if progress:
                        empty_scrolls = 0
                    else:
                        empty_scrolls += 1
                        # Brak nowych postów do reakcji - przewiń, aby doładować feed.
                        driver.execute_script("window.scrollBy(0, 1200);")
                        time.sleep(random.uniform(2, 4))

                driver.quit()
            except BaseException:
                driver.quit()
                accounts_with_errors.append(account)
                print(traceback.format_exc())
        if len(accounts_with_errors) > 0:
            print("Błąd podczas symulowania aktywności na kontach o nazwach: ", accounts_with_errors)
