import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import random
import clipboard

from db import Database

db = Database("store.db")


class MainScript:
    def __init__(self, hide, email1, products, images):

        PATH = "driver/chromedriver.exe"
        option = Options()
        option.add_argument("--disable-infobars")
        option.add_argument("start-maximized")
        option.add_argument("--disable-extensions")
        # Pass the argument 1 to allow and 2 to block
        option.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2
        })
        driver = webdriver.Chrome(chrome_options=option, executable_path=PATH)

        # Logowanie
        driver.get("https://facebook.com")
        email = driver.find_element_by_id("email")
        email.send_keys(db.getA("email", email1))
        password = driver.find_element_by_id("pass")
        password.send_keys(db.getA("password", email1))
        password.send_keys(Keys.ENTER)
        time.sleep(4)
        counter = 0
        for product1 in products:

            # Przejście do postowania ogłoszenia
            driver.get("https://www.facebook.com/marketplace/create/item")
            time.sleep(4)

            # Zdjęcia
            images1 = db.fetchI(product1)
            images2 = []
            for image in images[counter]:
                images2.append(images1[int(image) - 1])
            counter += 1
            photos = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@accept='image/*,image/heif,image/heic']")))
            paths = ""
            for image in images2:
                paths = paths + image[0] + "\n"

            paths = paths[:len(paths) - 1]
            photos.send_keys(paths)

            # Tytuł
            title = driver.find_element_by_xpath("//label[@aria-label='Tytuł']")
            product = db.getP(product1)
            clipboard.copy(product[2])
            title.send_keys(Keys.CONTROL + "v")
            # title.send_keys(product[2])

            # Cena
            price = driver.find_element_by_xpath("//label[@aria-label='Cena']")
            price.send_keys(product[3])

            # Kategoria WIP
            kategoria = driver.find_element_by_xpath("//label[@aria-label='Kategoria']")
            kategoria.click()
            time.sleep(1)
            tools = driver.find_elements_by_xpath("//div[@role='button']")
            tools[len(tools) - 1 - (26 - product[5])].click()

            # Stan WIP
            time.sleep(5)
            stan = driver.find_element_by_xpath("//label[@aria-label='Stan']")
            stan.click()
            time.sleep(5)
            try:
                test = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@role='menuitemradio']")))
            except selenium.common.exceptions.StaleElementReferenceException:
                stan.click()
                test = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@role='menuitemradio']")))

            test.click()

            # Opis
            desc = driver.find_element_by_xpath("//label[@aria-label='Opis']")
            desc.send_keys(product[4])

            # Dostępność
            accessibility = driver.find_element_by_xpath("//label[@aria-label='Dostępność']")
            accessibility.click()
            avaible = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@aria-checked='false']")))
            avaible.click()

            # Lokalizacja
            location = driver.find_element_by_xpath("//label[@aria-label='Lokalizacja']")
            locations = db.fetch("localizations", "localization")
            counter1 = 0
            for i in locations:
                locations[counter1] = i[0]
                counter1 += 1
            location.send_keys(Keys.BACKSPACE * 10 + locations[random.randint(0, len(locations) - 1)])
            location.click()
            time.sleep(1)
            location.send_keys(Keys.ARROW_DOWN + Keys.ENTER)

            # Ukryj przed znajomymi
            if hide != 0:
                hideBeforeFriends = driver.find_elements_by_xpath("//input[@aria-label='Włączone']")
                hideBeforeFriends[len(hideBeforeFriends) - 1].click()

            # Dalej
            next = driver.find_element_by_xpath("//div[@aria-label='Dalej']")
            next.click()

            # Opublikuj
            time.sleep(5)
            post = driver.find_element_by_xpath("//div[@aria-label='Opublikuj']")
            post.click()

            time.sleep(3)
        driver.quit()
