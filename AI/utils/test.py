import csv
import time
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
q
def read_products_from_csv(filename):
    product_list = []
    with open(filename, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if row:  # Boş satır kontrolü
                product_list.append(row[0])
    return product_list

def scraping_prices_from_test_csv():
    product_list = read_products_from_csv("csv/test.csv")

    options = Options()
    #options.add_argument("--headless")  # Tarayıcıyı gizli çalıştır
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    all_data = []

    for product_name in product_list:
        print(f"Ürün aranıyor: {product_name}")
        query = urllib.parse.quote_plus(product_name)
        driver.get(f"https://www.akakce.com/arama/?q={query}")

        try:
            first_product_img = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#APL li img"))
            )
            ActionChains(driver).move_to_element(first_product_img).click().perform()
        except:
            print(f"❌ {product_name} için ürün bulunamadı.")
            continue

        try:
            name = driver.find_element(By.TAG_NAME, "h1").text.strip()
        except:
            name = product_name

        try:
            price_element = driver.find_element(By.CSS_SELECTOR, "span.pt_v8")
            price_text = price_element.text.strip()
        except:
            price_text = "Fiyat bulunamadı"

        print(f"✅ {name} → {price_text}")
        all_data.append([name, price_text])
        time.sleep(1)  # Akakçe'den ban yememek için küçük gecikme

    driver.quit()

    with open("./csv/akakce.csv", mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["Product Name", "Price"])
        writer.writerows(all_data)

# Fonksiyonu çalıştır
scraping_prices_from_test_csv()
