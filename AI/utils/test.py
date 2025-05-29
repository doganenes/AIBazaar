import time
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import random
from selenium.common.exceptions import NoSuchElementException
from thefuzz import fuzz

phones = pd.read_csv("csv/phones_after_2023yeni.csv")

product_list = (
    phones["phone_model"] + " " + phones["storage"].astype(str) + "GB "
).tolist()



def find_best_match(product_name: str, product_titles: str, threshold=60):
    best_match = None
    best_score = 0

    for title in product_titles:
        score = fuzz.ratio(
            product_name.lower(), title.lower()
        )  # Benzerlik skoru hesapla

        if score >= threshold and score > best_score:
            best_match = title
            best_score = score

    return best_match


def scraping_prices_from_test_csv():

    options = Options()
    # options.add_argument("--headless")  # Tarayıcıyı gizli çalıştır
    driver = webdriver.Chrome(options=options)

    products = list()
    index = 0
    for product_name in product_list:
        print(f"Ürün aranıyor: {product_name}")
        query = urllib.parse.quote_plus(product_name)
        search_url = f"https://www.akakce.com/arama/?q={query}"
        driver.get(search_url)
        time.sleep(random.uniform(1, 2))

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#APL > li"))
        )
        list_items = driver.find_elements(By.CSS_SELECTOR, "#APL > li")

        if not list_items:
            print(f"❌ No products found for: {product_name}")
           

        h3_elements = [
            li.find_element(By.CSS_SELECTOR, "h3.pn_v8") for li in list_items[:10]
        ]
        h3_texts = [h3.text for h3 in h3_elements]
        print(h3_texts)
        h3_result = find_best_match(product_name, h3_texts, 0.85)
        print(f"this is {h3_result}")
      
        for li in list_items[:10]:
            try:
                time.sleep(random.uniform(0.5, 1.5))
                h3_element = WebDriverWait(li, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "h3.pn_v8"))
                )

                time.sleep(random.uniform(1.3, 2))
                try:
                    if str(h3_element.text) == str(h3_result):
                        WebDriverWait(li, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "pt_v8"))
                        )
                        a_tag = li.find_element(By.TAG_NAME, "a")
                        ref = a_tag.get_attribute("href")
                        driver.get(ref)
                        price = driver.find_element(By.CLASS_NAME, "pt_v8").text
                        price = price.split(",")[0].replace(".", "")
                        if int(price) < 5000:
                            price = 0
                        print(price)
                        product_name = phones["phone_model"][index]

                        products.append((product_name, price))
                        index += 1
                        break

                    else:
                        continue
                except Exception as e:
                    price = 0
                    continue
            except Exception as e:
                print(f"❌ Error: {str(e)}")
                continue

        df = pd.DataFrame(products, columns=["Product Name", "Price (TL)"])
        df.to_csv("products.csv", index=False, encoding="utf-8")


scraping_prices_from_test_csv()
