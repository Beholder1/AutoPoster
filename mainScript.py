from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import random
import os

from db import Database

db = Database("store.db")

class MainScript:
    def __init__(self):
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
        email.send_keys("kamil.limanowa@gmail.com")
        password = driver.find_element_by_id("pass")
        password.send_keys("h5k11s00")
        password.send_keys(Keys.ENTER)
        time.sleep(6)

        # Przejście do postowania ogłoszenia
        driver.get("https://www.facebook.com/marketplace/create/item")
        file = open("test.txt")
        time.sleep(2)

        # Wybranie pól tekstowych
        titles = driver.find_elements_by_css_selector(".oajrlxb2.rq0escxv.f1sip0of.hidtqoto.e70eycc3.lzcic4wl.g5ia77u1.gcieejh5.bn081pho.humdl8nn.izx4hr6d.oo9gr5id.qc3s4z1d.knj5qynh.fo6rh5oj.osnr6wyh.hv4rvrfc.dati1w0a.p0x8y401.k4urcfbm.iu8raji3.nfbje2wv")

        # Tytuł
        titles[0].send_keys(file.readline())

        # Cena
        titles[1].send_keys(file.readline())

        # Lokalizacja
        titles[3].send_keys(Keys.BACKSPACE * 10 + db.getL(random.randint(1,db.getNumberL())))
        titles[3].click()
        time.sleep(1)
        titles[3].send_keys(Keys.ARROW_DOWN + Keys.ENTER)

        # Ukryj przed znajomymi
        hideBeforeFriends = driver.find_elements_by_css_selector(".oajrlxb2.rq0escxv.f1sip0of.hidtqoto.nhd2j8a9.datstx6m.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.b5wmifdl.lzcic4wl.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.pmk7jnqg.j9ispegn.kr520xx4.k4urcfbm")
        hideBeforeFriends[1].click()

        # Opis
        desc = driver.find_element_by_css_selector(".oajrlxb2.rq0escxv.f1sip0of.hidtqoto.lzcic4wl.g5ia77u1.gcieejh5.bn081pho.humdl8nn.izx4hr6d.oo9gr5id.j83agx80.jagab5yi.knj5qynh.fo6rh5oj.oud54xpy.l9qdfxac.ni8dbmo4.stjgntxs.hv4rvrfc.dati1w0a.ieid39z1.k4urcfbm")
        desc.send_keys(file.readline())

        # Wybranie rozwijanych menu
        menu = driver.find_elements_by_css_selector(".cwj9ozl2.qbxu24ho.bxzzcbxg.lxuwth05.h2mp5456.beltcj47.p86d2i9g.aot14ch1.kzx2olss.goun2846.ccm00jje.s44p3ltw.mk2mc5f4.frvqaej8.ed0hlay0.afxsp9o4.jcgfde61.j83agx80.cbu4d94t.ni8dbmo4.stjgntxs.l9j0dhe7.du4w35lb.hw4tbnyy.nhd2j8a9.lzcic4wl")

        # Kategoria WIP
        menu[0].click()
        time.sleep(1)
        tools = driver.find_elements_by_css_selector(".oajrlxb2.gs1a9yip.g5ia77u1.mtkw9kbi.tlpljxtp.qensuy8j.ppp5ayq2.goun2846.ccm00jje.s44p3ltw.mk2mc5f4.rt8b4zig.n8ej3o3l.agehan2d.sk4xxmp2.rq0escxv.nhd2j8a9.a8c37x1j.mg4g778l.btwxx1t3.pfnyh3mw.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.tgvbjcpo.hpfvmrgz.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.l9j0dhe7.i1ao9s8h.esuyzwwr.f1sip0of.du4w35lb.lzcic4wl.ue3kfks5.pw54ja7n.uo3d90p7.l82x9zwi.abiwlrkh.p8dawk7l")
        tools[8].click()

        # Stan WIP
        menu[1].click()
        time.sleep(1)
        test = driver.find_element_by_css_selector(".oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.j83agx80.p7hjln8o.kvgmc6g5.opuu4ng7.oygrvhab.kj2yoqh6.pybr56ya.dflh9lhu.f10w8fjw.scb9dxdr.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl.n00je7tq.arfg74bv.qs9ysxi8.k77z8yql.l9j0dhe7.abiwlrkh.p8dawk7l.bp9cbjyn.dwo3fsh8.btwxx1t3.pfnyh3mw.du4w35lb")
        test.click()

        # Zdjęcia
        photos = driver.find_elements_by_css_selector(".mkhogb32")
        photos[1].send_keys(os.getcwd() + "\i1.png")

        # Dalej
        next = driver.find_elements_by_css_selector(".oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.pq6dq46d.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl.n00je7tq.arfg74bv.qs9ysxi8.k77z8yql.l9j0dhe7.abiwlrkh.p8dawk7l.cbu4d94t.taijpn5t.k4urcfbm")
        next[1].click()
        file.close()