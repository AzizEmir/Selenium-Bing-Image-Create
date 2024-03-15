from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from bs4 import BeautifulSoup
import time
import random
import string
import requests
import subprocess
import re
import os
import shutil
import pyotp
import hashlib

# LibreWolf seçeneklerini tanımla
librewolf_options = webdriver.FirefoxOptions()

# İndirme işlemleri için tercihleri ayarla
librewolf_options.set_preference("browser.download.dir", "/home/aziz/İndirilenler/selenium_fotolar")  # İndirme dizini
librewolf_options.set_preference("browser.download.folderList", 2)  # İndirme dizini olarak belirtilen yolu kullan
librewolf_options.set_preference("browser.helperApps.neverAsk.saveToDisk", "image/jpeg")  # İndirmeleri her zaman belirli bir dosya türü olarak kaydet
librewolf_options.set_preference("browser.download.panel.shown", False)  # İndirme penceresini gösterme
librewolf_options.set_preference("dom.popup_maximum", 0)  # Pop-up'ların maksimum sayısını sıfıra ayarla

# LibreWolf'un çalıştırılabilir dosyasının yolu
librewolf_path = "/usr/bin/firefox"  # "librewolf" veya "librewolf.exe" gibi bir dosya adı

# LibreWolf'un çalıştırılabilir dosyasını belirt
librewolf_options.binary_location = librewolf_path

# Selenium WebDriver'ı başlat
driver = webdriver.Firefox(options=librewolf_options)

# ASAMA 1 
# bing image creator a giris yapilacak sayfaya git

# Bing Images sayfasını aç 
driver.get("https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=21&id=264960&wreply=https%3a%2f%2fwww.bing.com%2fsecure%2fPassport.aspx%3fedge_suppress_profile_switch%3d1%26requrl%3dhttps%253a%252f%252fwww.bing.com%252fimages%252fcreate%253fsude%253d1%26sig%3d1E29D91E7DA366510213CD2C7C5967FC%26nopa%3d2&wp=MBI_SSL&lc=1033&CSRFToken=b9dc43d5-fa58-4852-bdac-d46d1b8e994f&cobrandid=03f1ec5e-1843-43e5-a2f6-e60ab27f6b91&nopa=2")

# Bekleme süresi
time.sleep(2)

# E-posta giriş kutusunu bul ve belirtilen e-posta adresini gönder
email_kutusu = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="i0116"]')))
email_kutusu.send_keys("EMAIL")

# Enter tuşuna basarak devam et
email_kutusu.send_keys(Keys.RETURN)

# Bekleme süresi
time.sleep(2)

# parola giriş kutusunu bul ve belirtilen parola adresini gönder
parola_kutusu = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="i0118"]')))
parola_kutusu.send_keys("PASSWORD")

# Enter tuşuna basarak devam et
parola_kutusu.send_keys(Keys.RETURN)

# Bekleme süresi
time.sleep(2)

def stay_signin():
    try:
        # "acceptButton" ID'li butonu bul ve tıkla
        buton = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//button[@id="acceptButton"]')))
        buton.click()
    except:
        pass

# Bekleme süresi
time.sleep(2)

# HESAPTA TOTP VAR MI ?
# Anahtarınızı buraya girin
totp_key = ""

# Input alanını bul Yoksa TOTP yoktur
try:
    input_element =  WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, '//input[@id="idTxtBx_SAOTCC_OTC"]')))

    if input_element:
        # SHA-1 algoritması kullanarak TOTP nesnesini oluştur
        totp = pyotp.TOTP(totp_key, interval=30, digest=hashlib.sha1)

        # TOTP kodunu al
        totp_code = totp.now()

        print("TOTP Kodu:", totp_code)

        # TOTP kodunu input alanına yazdırın
        input_element =  WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//input[@id="idTxtBx_SAOTCC_OTC"]'))
            )
        input_element.send_keys(totp_code)
        input_element.send_keys(Keys.RETURN)

        stay_signin()

    # SHA-1 algoritması kullanarak TOTP nesnesini oluştur
    totp = pyotp.TOTP(totp_key, interval=30, digest=hashlib.sha1)
    
    # TOTP kodunu al
    totp_code = totp.now()
    
    print("TOTP Kodu:", totp_code)
    
    # Input alanı varsa TOTP kodunu gönder
    if input_element:
        input_element.send_keys(totp_code)
except:
    stay_signin()

try:
    # Belirli bir süre boyunca `bnp_cookie_banner` elementinin görünür olmasını bekleyin
    banner = WebDriverWait(driver, 8).until(EC.visibility_of_element_located((By.ID, 'bnp_cookie_banner')))

    # Eğer banner görünürse, bnp_btn_reject butonuna tıklayın
    if banner.is_displayed():
        reject_button = banner.find_element(By.ID, 'bnp_btn_reject')
        reject_button.click()

except Exception as e:
    pass  # Pop-up bulunamadığında yapılacak işlem yoksa, pass ifadesiyle geçebilirsiniz

# ASAMA 2 Regex deseni

def process_after_step_2(driver,siirMetni):
    # Siiri yapistir ve olusmasini bekle
    siir_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="sb_form_q"]')))
        
    # Siir metni
    siir_metni = siirMetni
    siir_input.send_keys(siir_metni)
    siir_input.send_keys(Keys.RETURN)

    # Bekleme süresi
    time.sleep(2)

    while True:
        try:
            giloader = driver.find_element(By.ID, "giloader")
            if "display: none;" in giloader.get_attribute("style"):
                # data-idx="1" içeren ilk li etiketini bul
                li_element = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//li[@data-idx="1"]')))

                link = li_element.find_element(By.TAG_NAME, 'a')

                # a etiketinin href özelliğini kopyala ve bir değişkene at
                link_href = link.get_attribute('href')
                
                driver.execute_script("window.open(arguments[0], '_self');", link_href)
                
                time.sleep(2)
                break
        except:
            pass
        time.sleep(3)  # Her bir saniyede bir kontrol et

    # Bekleme süresi
    time.sleep(4)

    try:
        # Belirli bir süre boyunca `bnp_cookie_banner` elementinin görünür olmasını bekleyin
        banner = WebDriverWait(driver, 8).until(EC.visibility_of_element_located((By.ID, 'bnp_cookie_banner')))

        # Eğer banner görünürse, bnp_btn_reject butonuna tıklayın
        if banner.is_displayed():
            reject_button = banner.find_element(By.ID, 'bnp_btn_reject')
            reject_button.click()

    except (NoSuchElementException, TimeoutException):
        pass  # Pop-up bulunamadığında yapılacak işlem yoksa, pass ifadesiyle geçebilirsiniz


    time.sleep(2)

    for _ in range(3):
        # 1. Öğenin XPath'ini belirtin
        download_button_xpath = '//div[@class="action dld nofocus" and @role="button"]'
        # 2. XPath ifadesiyle öğeyi bulun
        download_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, download_button_xpath)))
        # 3. Öğeye tıklayın
        download_button.click()

        time.sleep(3)
        # Butonun varlığını kontrol edin
        next_button = driver.find_element(By.XPATH, '//div[@id="navr"]/span[@class="icon" and @title="Bir sonraki görüntü sonucu"]')
        # Butona tıklayın
        next_button.click()

    # 4. Resim İçin
    # 1. Öğenin XPath'ini belirtin
    download_button_xpath = '//div[@aria-label="İndir" and @role="button"]'
    # 2. XPath ifadesiyle öğeyi bulun
    download_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, download_button_xpath)))
    # 3. Öğeye tıklayın
    download_button.click()

    # Büyük harfleri içeren kelimeleri bul
    buyuk_kelime = re.findall(r'\b[A-ZÇĞİÖŞÜ]+\b', siir_metni)

    # Tüm büyük harf içeren kelimeleri birleştir
    birlesik_kelime = ' '.join(buyuk_kelime)

    print(birlesik_kelime)

    # BASH ile yapılması gerekenler
    def move_images(source_dir, dest_dir):
        # Hedef dizini oluştur
        os.makedirs(dest_dir, exist_ok=True)
        
        # Kaynak dizinindeki tüm .jpeg dosyalarını hedef dizine taşı
        for filename in os.listdir(source_dir):
            if filename.endswith(".jpeg"):
                shutil.move(os.path.join(source_dir, filename), dest_dir)

    # Kaynak ve hedef dizinlerini belirle
    source_directory = "/home/aziz/İndirilenler/selenium_fotolar"
    dest_directory = "/home/aziz/Masaüstü/selenium_bing/sonuclar/"

    # Betiği çalıştır
    move_images(source_directory, os.path.join(dest_directory, birlesik_kelime))

# ASAMA 3 txt dosyalarında bulunan tüm şiirleri döngü ile ASAMA 2'yi tekrar et

# Klasör yolu
klasor_yolu = "./metinlerKlasor"

# Regex deseni
regex_deseni = r'^(\d+)-(.+)\.txt$'

# Dosyaları dolaş
for dosya_adı in os.listdir(klasor_yolu):
    # Dosya adı regex deseni ile eşleşiyorsa
    if re.match(regex_deseni, dosya_adı):
        dosya_yolu = os.path.join(klasor_yolu, dosya_adı)
        
        # Dosyayı oku
        with open(dosya_yolu, 'r') as dosya:
            icerik = dosya.read()
            print(f"{dosya_adı} dosyasının içeriği:")
            # ASAMA 2 yi çağır
            process_after_step_2(driver,icerik)

            #Sonraki Resme geçmek için alanı kapat
            # Belirtilen XPath ile div elementini bulun
            close_button = driver.find_element(By.XPATH, '//div[@data-tooltip="Görüntüyü kapat"]')

            # Elementi tıklayın
            close_button.click()

            print("-------------------------------------")
    else:
        print("eşleşmiyor")
