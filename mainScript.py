from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import random

from db import Database

db = Database("store.db")

class MainScript:
    def __init__(self, hide, email1, products):
        PATH = "C:\Program Files (x86)\chromedriver.exe"
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
        email.send_keys(email1)
        password = driver.find_element_by_id("pass")
        password.send_keys(db.getA(email1))
        password.send_keys(Keys.ENTER)
        time.sleep(6)
        for product1 in products:

            # Przejście do postowania ogłoszenia
            driver.get("https://www.facebook.com/marketplace/create/item")
            time.sleep(2)

            # Zdjęcia
            images = db.fetchI(product1)
            photos = driver.find_element_by_xpath("//input[@accept='image/*,image/heif,image/heic']")
            paths=""
            counter=0
            for image in images:
                paths = paths+image[0]+"\n"
                if counter==0:
                    counter=31
                elif counter<36:
                    counter+=5
                else:
                    counter+=2
            paths=paths[:len(paths)-1]
            photos.send_keys(paths)
            time.sleep(2)

            # Tytuł
            title = driver.find_element_by_xpath("//label[@aria-label='Tytuł']")
            title.send_keys(product1)
            product = db.getP(product1)

            # Cena
            price = driver.find_element_by_xpath("//label[@aria-label='Cena']")
            price.send_keys(product[3])

            # Kategoria WIP
            kategoria = driver.find_element_by_xpath("//label[@aria-label='Kategoria']")
            kategoria.click()
            time.sleep(2)
            tools = driver.find_elements_by_xpath("//div[@role='button']")
            print(product)
            tools[counter+int(product[5])-1].click()
            time.sleep(2)

            # Stan WIP
            stan = driver.find_element_by_xpath("//label[@aria-label='Stan']")
            stan.click()
            time.sleep(1)
            test = driver.find_element_by_xpath("//div[@role='menuitemradio']")
            test.click()

            # Opis
            desc = driver.find_element_by_xpath("//label[@aria-label='Opis']")
            desc.send_keys(product[4])

            # Dostępność
            accessibility = driver.find_element_by_xpath("//label[@aria-label='Dostępność']")
            accessibility.click()
            time.sleep(1)
            avaible = driver.find_element_by_xpath("//div[@aria-checked='false']")
            avaible.click()

            # Lokalizacja
            location = driver.find_element_by_xpath("//label[@aria-label='Lokalizacja']")
            location.send_keys(Keys.BACKSPACE * 10 + db.getL(random.randint(1,db.getNumberL())))
            location.click()
            time.sleep(1)
            location.send_keys(Keys.ARROW_DOWN + Keys.ENTER)

            # Ukryj przed znajomymi
            if hide != 0:
                hideBeforeFriends = driver.find_elements_by_xpath("//input[@aria-label='Włączone']")
                hideBeforeFriends[1].click()

            # Dalej
            next = driver.find_element_by_xpath("//div[@aria-label='Dalej']")
            next.click()

            # Opublikuj
            time.sleep(2)
            post = driver.find_element_by_xpath("//div[@aria-label='Opublikuj']")
            post.click()

            time.sleep(3)