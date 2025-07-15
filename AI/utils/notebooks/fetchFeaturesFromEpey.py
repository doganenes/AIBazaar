import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time, random
import pandas as pd

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Mobile Safari/537.36",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.49 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.124 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.79 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.98 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.125 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-A515F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.87 Mobile Safari/537.36",
    "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:110.0) Gecko/20100101 Firefox/110.0",
    "Mozilla/5.0 (Linux; Android 9; Redmi Note 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.77 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
]


base_url = "https://www.epey.com/akilli-telefonlar/e/YToyOntzOjU6Im1hcmthIjthOjE6e2k6MDtzOjE6IjIiO31pOjE4NzA7YTo1OntpOjA7czo3OiIyNTE1MDkzIjtpOjE7czo3OiIyMzg2NTQ3IjtpOjI7czo3OiIyMTk5NDE1IjtpOjM7czo3OiIyMDY3MjcxIjtpOjQ7czo3OiIxOTQyNDY3Ijt9fV9OOw==/"
feature_ids = {
    "Ekran Boyutu": "id1",
    "Ekran Teknolojisi": "id4",
    "Piksel Yoğunluğu": "id2",
    "Batarya Kapasitesi": "id7",
    "Kamera Çözünürlüğü": "id19",
    "CPU Üretim Teknolojisi": "id2033",
    "İşletim Sistemi": "id24",
    "RAM Kapasitesi": "id14",
    "Dahili Hafıza": "id21",
    "Ekran Yenileme Hızı": "id6737",
    "5G": "id5711",
    "Suya dayanıklılık": "id114",
    "Toza dayanıklılık": "id113",
}

all_phones = []
productIds = set()

for page_num in range(1, 3):
    ua = user_agents[(page_num - 1) % len(user_agents)]

    options = uc.ChromeOptions()
    options.add_argument(f"user-agent={ua}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = uc.Chrome(options=options)
    url = f"{base_url}{page_num}/"
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#listele > div.listele.table")
            )
        )
    except Exception as e:
        print(f"Sayfa {page_num} yüklenemedi: {e}")
        driver.quit()
        continue

    time.sleep(random.uniform(2, 4))
    soup = BeautifulSoup(driver.page_source, "html.parser")
    container = soup.select_one("#listele > div.listele.table")

    if container:
        ul_elements = container.find_all("ul")
        for ul in ul_elements:
            ul_id = ul.get("id")
            if ul_id and ul_id not in productIds:
                productImg = ul.find("img")
                productImgLink = (
                    productImg.get("src").replace("k_", "b_") if productImg else None
                )
                productIds.add(ul_id)
            else:
                continue

            a_tag = ul.find("a", class_="urunadi")
            if not a_tag:
                continue

            product_link = a_tag.get("href")
            if product_link.startswith("https://track.adform.net"):
                continue
            if not product_link.startswith("http"):
                product_link = "https://www.epey.com" + product_link

            try:
                driver.get(product_link)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".baslik h1"))
                )
            except Exception as e:
                print(f"Sayfa yüklenemedi: {product_link} -> {e}")
                driver.back()
                continue

            try:
                phoneModel = driver.find_element(
                    By.CSS_SELECTOR, ".baslik h1"
                ).text.split(" (")[0]
            except Exception as e:
                print(f"Model adı alınamadı: {product_link} -> {e}")
                driver.back()
                continue

            time.sleep(random.uniform(2, 4))
            detail_soup = BeautifulSoup(driver.page_source, "html.parser")

            price_tag = detail_soup.select_one(
                "#fiyatlar > div.fiyatlar > div.fiyat.fiyat-1 span.urun_fiyat"
            )
            try:
                raw_price = price_tag.get_text(strip=True)
                price_only = (
                    raw_price.split(" TL")[0].replace(".", "").replace(",", ".")
                )
                productPrice = float(price_only)
            except Exception as e:
                print(f"Fiyat alınamadı: {phoneModel} -> {e}")
                driver.back()
                continue

            print(f"Ürün: {phoneModel}, Fiyat: {productPrice} TL")

            features = [f"Model: {phoneModel}"]
            for label, id_ in feature_ids.items():
                li = detail_soup.find("li", id=id_)
                if li:
                    deger = li.find("span", class_="cell cs1")
                    if deger:
                        value = deger.get_text(strip=True)
                        features.append(f"{label}: {value}")

            features.append(f"Price: {productPrice} TL")
            description = "; ".join(features)

            all_phones.append(
                {
                    "ProductID": ul_id,
                    "Description": description,
                    "ImageUrl": productImgLink,
                    "Model": phoneModel,
                    "Price": productPrice,
                }
            )

            driver.back()
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "#listele > div.listele.table")
                    )
                )
            except Exception as e:
                print(f"Liste sayfasına geri dönemedi: {e}")
                continue
            time.sleep(random.uniform(2, 4))

    driver.quit()

df = pd.DataFrame(all_phones)
df.to_csv("LSTMProduct2.csv", index=False)
print("CSV kaydedildi: LSTMProduct1.csv")
