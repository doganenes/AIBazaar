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
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from thefuzz import fuzz

phones = pd.read_csv("csv/phones_after_2023yeni.csv")

product_list = (
    phones["phone_model"] + " " + phones["storage"].astype(str) + "GB "
).tolist()


def find_best_match(product_name: str, product_titles: str, threshold=60):
    best_match = None
    best_score = 0
    all_scores = []

    print(f"🔍 Benzerlik skorları ('{product_name}' için):")

    for title in product_titles:
        score = fuzz.ratio(
            product_name.lower(), title.lower()
        )  # Benzerlik skoru hesapla

        all_scores.append((title, score))
        print(f"   📊 {score}% - {title}")

        if score >= threshold and score > best_score:
            best_match = title
            best_score = score

    print(f"🎯 En yüksek skor: {best_score}% (Eşik: {threshold}%)")
    return best_match, best_score, all_scores


def scraping_prices_from_test_csv():
    options = Options()
    driver = webdriver.Chrome(options=options)
    products = list()

    for index, product_name in enumerate(product_list):
        print(f"Ürün aranıyor ({index+1}/{len(product_list)}): {product_name}")

        # Her ürün için varsayılan değerler
        price = 0
        productIndexName = phones["phone_model"][index]

        try:
            query = urllib.parse.quote_plus(product_name)
            search_url = f"https://www.akakce.com/arama/?q={query}"
            driver.get(search_url)
            time.sleep(random.uniform(1, 2))

            # Ürün listesinin yüklenmesini bekle
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#APL > li"))
                )
                list_items = driver.find_elements(By.CSS_SELECTOR, "#APL > li")
            except TimeoutException:
                print(f"❌ Ürün listesi yüklenemedi: {product_name}")
                products.append((product_name, price, productIndexName))
                continue

            if not list_items:
                print(f"❌ Ürün bulunamadı: {product_name}")
                products.append((product_name, price, productIndexName))
                continue

            # İlk 10 ürünün başlıklarını al
            h3_texts = []
            for li in list_items[:10]:
                try:
                    h3_element = li.find_element(By.CSS_SELECTOR, "h3.pn_v8")
                    h3_texts.append(h3_element.text)
                except NoSuchElementException:
                    continue

            if not h3_texts:
                print(f"❌ Ürün başlıkları alınamadı: {product_name}")
                products.append((product_name, price, productIndexName))
                continue

            print(f"Bulunan ürünler ({len(h3_texts)} adet):")
            for i, title in enumerate(h3_texts, 1):
                print(f"  {i}. {title}")

            print()  # Boş satır
            h3_result, best_score, all_scores = find_best_match(
                product_name, h3_texts, 60
            )

            if h3_result:
                print(f"✅ En iyi eşleşme: '{h3_result}' (Skor: {best_score}%)")
            else:
                print(
                    f"❌ Eşik değeri aşan eşleşme yok (En yüksek skor: {max([s[1] for s in all_scores]) if all_scores else 0}%)"
                )

            if not h3_result:
                print(f"❌ Uygun eşleşme bulunamadı: {product_name}")
                products.append((product_name, price, productIndexName))
                continue

            # Eşleşen ürünü bul ve fiyatını al
            product_found = False
            for li in list_items[:10]:
                try:
                    time.sleep(random.uniform(0.5, 1.5))
                    h3_element = li.find_element(By.CSS_SELECTOR, "h3.pn_v8")

                    if str(h3_element.text) == str(h3_result):
                        print(f"🎯 Hedef ürün bulundu: {h3_element.text}")

                        # Ürün detay sayfasına git
                        try:
                            link_element = li.find_element(By.CLASS_NAME, "pw_v8")
                            href_value = link_element.get_attribute("href")
                            driver.get(href_value)
                            time.sleep(random.uniform(1, 2))

                            # Fiyatı al
                            try:
                                price_element = WebDriverWait(driver, 10).until(
                                    EC.presence_of_element_located(
                                        (By.CLASS_NAME, "pt_v8")
                                    )
                                )
                                price_text = price_element.text
                                price = price_text.split(",")[0].replace(".", "")
                                price = int(price) if price.isdigit() else 0

                                # Fiyat kontrolü
                                if price < 6000:
                                    print(
                                        f"⚠️ Fiyat çok düşük ({price} TL), 0 olarak ayarlandı"
                                    )
                                    price = 0
                                else:
                                    print(f"💰 Fiyat bulundu: {price} TL")

                                product_found = True
                                break

                            except (
                                TimeoutException,
                                NoSuchElementException,
                                ValueError,
                            ) as e:
                                print(f"❌ Fiyat alınamadı: {str(e)}")
                                price = 0
                                product_found = True
                                break

                        except (NoSuchElementException, TimeoutException) as e:
                            print(f"❌ Ürün detay sayfasına gidilemedi: {str(e)}")
                            continue

                except (NoSuchElementException, TimeoutException) as e:
                    print(f"❌ Ürün işlenirken hata: {str(e)}")
                    continue

            if not product_found:
                print(f"❌ Ürün işlenemedi: {product_name}")

        except Exception as e:
            print(f"❌ Genel hata: {str(e)}")
            price = 0

        # Her durumda ürünü listeye ekle
        products.append((product_name, price, productIndexName))
        print(f"📝 Kaydedildi: {product_name} - {price} TL")
        print("-" * 50)

    # CSV dosyasını kaydet
    try:
        df = pd.DataFrame(
            products, columns=["Product Name", "Price (TL)", "Product Csv name"]
        )
        df.to_csv("products3.csv", index=False, encoding="utf-8")
        print(f"✅ {len(products)} ürün products.csv dosyasına kaydedildi")
    except Exception as e:
        print(f"❌ CSV kaydetme hatası: {str(e)}")

    finally:
        driver.quit()


if __name__ == "__main__":
    scraping_prices_from_test_csv()
