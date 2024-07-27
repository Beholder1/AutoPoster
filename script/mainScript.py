import random
import time

import clipboard
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class MainScript:
    def __init__(self, db, hide, accounts, products, images, incognito):
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
                random.shuffle(products)

                # Logowanie
                driver.get("https://facebook.com")
                email = driver.find_element(By.ID, "email")
                email.send_keys(self.db.getA("email", account))
                password = driver.find_element(By.ID, "pass")
                password.send_keys(self.db.getA("password", account))
                password.send_keys(Keys.ENTER)
                time.sleep(4)
                counter = 0
                for product1 in products:
                    product = self.db.findProductByName(product1)
                    categories = db.findAllProductCategoriesByProductId(product[0])
                    categoriesIds = []
                    for i in categories:
                        categoriesIds.append(i[0])
                    category = categoriesIds[random.randint(0, len(categoriesIds) - 1)]

                    # Przejście do postowania ogłoszenia
                    driver.get("https://www.facebook.com/marketplace/create/item")
                    time.sleep(4)

                    # Zdjęcia
                    images1 = self.db.findAllImagesByProduct(product1)
                    images2 = []
                    for image in images[counter]:
                        images2.append(images1[int(image) - 1])
                    counter += 1
                    photos = WebDriverWait(driver, 10).until(
                        ec.presence_of_element_located((By.XPATH, "//input[@accept='image/*,image/heif,image/heic']")))
                    paths = ""
                    for image in images2:
                        paths = paths + image[0] + "\n"

                    paths = paths[:len(paths) - 1]
                    photos.send_keys(paths)

                    # Tytuł
                    title = driver.find_element(By.XPATH, "//label[@aria-label='Tytuł']")
                    clipboard.copy(product[2])
                    title.send_keys(Keys.CONTROL + "v")
                    # title.send_keys(product[2])

                    # Cena
                    price = driver.find_element(By.XPATH, "//label[@aria-label='Cena']")
                    price.send_keys(product[3])

                    # Kategoria
                    kategoria = driver.find_element(By.XPATH, "//label[@aria-label='Kategoria']")
                    kategoria.click()
                    time.sleep(1)
                    tools = driver.find_elements(By.XPATH, "//div[@role='button']")
                    tools[len(tools) - 1 - (26 - category)].click()

                    # Stan
                    time.sleep(5)
                    stan = driver.find_element(By.XPATH, "//label[@aria-label='Stan']")
                    stan.click()
                    time.sleep(5)
                    try:
                        test = WebDriverWait(driver, 5).until(
                            ec.presence_of_element_located((By.XPATH, "//span[normalize-space()='Nowy']")))
                    except selenium.common.exceptions.StaleElementReferenceException:
                        stan.click()
                        test = WebDriverWait(driver, 5).until(
                            ec.presence_of_element_located((By.XPATH, "//span[normalize-space()='Nowy']")))

                    test.click()

                    # Opis
                    desc = driver.find_element(By.XPATH, "//label[@aria-label='Opis']")
                    desc.send_keys(product[4])

                    # Dostępność
                    # accessibility = driver.find_element_by_xpath("//label[@aria-label='Dostępność']")
                    # accessibility.click()
                    # available = WebDriverWait(driver, 10).until(
                    #     EC.presence_of_element_located((By.XPATH, "//div[@aria-selected='false']")))
                    # available.click()

                    # Lokalizacja
                    location = driver.find_element(By.XPATH, "//label[@aria-label='Lokalizacja']")
                    locations = self.db.fetch("localizations", "localization")
                    counter1 = 0
                    for i in locations:
                        locations[counter1] = i[0]
                        counter1 += 1
                    time.sleep(5)
                    location.send_keys(Keys.BACKSPACE * 10 + locations[random.randint(0, len(locations) - 1)])
                    location.click()
                    time.sleep(5)
                    location.send_keys(Keys.ARROW_DOWN + Keys.ENTER)

                    # Ukryj przed znajomymi
                    if hide != 0:
                        hideBeforeFriends = driver.find_elements(By.XPATH, "(//div[@role='switch'])[2]")
                        hideBeforeFriends[len(hideBeforeFriends) - 1].click()

                    try:
                        # Dalej
                        next = driver.find_element(By.XPATH, "//div[@aria-label='Dalej']")
                        next.click()
                    except selenium.common.exceptions.NoSuchElementException:
                        pass

                    # Opublikuj
                    time.sleep(5)
                    post = driver.find_element(By.XPATH, "//div[@aria-label='Opublikuj']")
                    post.click()

                    time.sleep(3)
                driver.quit()
            except BaseException as e:
                driver.quit()
                accountsWithErrors.append(account)
                print(e)
        if len(accountsWithErrors) > 0:
            print("Błąd podczas wrzucania kont o nazwach: ", accountsWithErrors)
