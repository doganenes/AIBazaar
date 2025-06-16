import time
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pandas as pd
import random
import re
from thefuzz import fuzz

phones = pd.read_csv("notebooks/drop_duplicates_product.csv")
product_list = phones["Product Name"]


def extract_camera_mp(text):
    """Metinden kamera MP değerini çıkarır"""
    if not text:
        return 0

    # MP değeri arama desenleri
    patterns = [
        r"(\d+(?:\.\d+)?)\s*MP",
        r"(\d+(?:\.\d+)?)\s*mp",
        r"(\d+(?:\.\d+)?)\s*megapiksel",
        r"(\d+(?:\.\d+)?)\s*Megapiksel",
        r"(\d+(?:\.\d+)?)\s*MegaPixel",
        r"(\d+(?:\.\d+)?)\s*megapixel",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                continue

    return 0


def find_camera_info_flexible(driver):
    """Çoklu yöntemle kamera bilgisini bulur"""
    camera_mp = 0

    # Yöntem 1: class="ppt" tablosunun 19. elemanını direkt al
    try:
        # class="ppt" tablosunu bul ve 19. tr elementini al
        ppt_table_rows = driver.find_elements(By.CSS_SELECTOR, "table.ppt tr")
        if len(ppt_table_rows) >= 19:
            camera_row = ppt_table_rows[17]  # 19. eleman (index 18)
            text = camera_row.text
            mp_value = extract_camera_mp(text)
            if mp_value > 0:
                print(
                    f"✅ Kamera MP bulundu (PPT Tablo 19. satır): {mp_value} MP - Metin: {text}"
                )
                return mp_value
            else:
                print(
                    f"🔍 PPT Tablo 19. satır bulundu ama MP değeri çıkarılamadı: {text}"
                )
        else:
            print(
                f"❌ PPT tablosunda yeterli satır yok (Bulunan: {len(ppt_table_rows)}, Gereken: 19)"
            )
    except Exception as e:
        print(f"❌ PPT tablo arama hatası: {str(e)}")

    # Yöntem 2: Alternatif XPath'ler
    xpath_patterns = [
        "//table[@class='ppt']//tr[19]",
        "//table[@class='ppt']/tbody/tr[19]",
        "//*[@id='DT_w']/div[1]/table/tbody/tr[19]",
        "/html/body/main/div[4]/section[1]/div/div[1]/table/tbody/tr[19]",
    ]

    for xpath in xpath_patterns:
        try:
            element = driver.find_element(By.XPATH, xpath)
            text = element.text
            mp_value = extract_camera_mp(text)
            if mp_value > 0:
                print(f"✅ Kamera MP bulundu (XPath): {mp_value} MP - Metin: {text}")
                return mp_value
        except Exception as e:
            continue

    # Yöntem 3: PPT tablosunda kamera kelimesi ara
    try:
        ppt_camera_rows = driver.find_elements(
            By.XPATH,
            "//table[@class='ppt']//tr[contains(., 'Kamera') or contains(., 'kamera') or contains(., 'MP')]",
        )
        for row in ppt_camera_rows:
            text = row.text
            mp_value = extract_camera_mp(text)
            if mp_value > 0:
                print(
                    f"✅ Kamera MP bulundu (PPT Kamera arama): {mp_value} MP - Metin: {text}"
                )
                return mp_value
    except Exception as e:
        print(f"❌ PPT kamera arama hatası: {str(e)}")

    # Yöntem 4: Genel tablo tarama (yedek)
    try:
        table_rows = driver.find_elements(By.XPATH, "//table//tr")
        for row in table_rows:
            text = row.text.lower()
            if any(
                keyword in text
                for keyword in ["kamera", "camera", "mp", "megapiksel", "megapixel"]
            ):
                mp_value = extract_camera_mp(row.text)
                if mp_value > 0:
                    print(
                        f"✅ Kamera MP bulundu (Genel tablo): {mp_value} MP - Metin: {row.text}"
                    )
                    return mp_value
    except Exception as e:
        print(f"❌ Genel tablo tarama hatası: {str(e)}")

    return camera_mp


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
    # Headless modda çalıştırmak isterseniz aşağıdaki satırı ekleyin
    # options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    products = list()

    for index, product_name in enumerate(product_list):
        print(f"Ürün aranıyor ({index+1}/{len(product_list)}): {product_name}")

        # Her ürün için varsayılan değerler
        camera = 0

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
                products.append((product_name, camera))
                continue

            if not list_items:
                print(f"❌ Ürün bulunamadı: {product_name}")
                products.append((product_name, camera))
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
                products.append((product_name, camera))
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
                products.append((product_name, camera))
                continue

            # Eşleşen ürünü bul ve kamera bilgisini al
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
                            time.sleep(random.uniform(2, 3))

                            # Kamera MP bilgisini al
                            print(f"🔍 Kamera bilgisi aranıyor...")
                            camera = find_camera_info_flexible(driver)

                            if camera > 0:
                                print(f"✅ Kamera MP bulundu: {camera} MP")
                            else:
                                print(f"❌ Kamera MP bulunamadı")

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
            camera = 0

        # Her durumda ürünü listeye ekle
        products.append((product_name, camera))
        print(f"📝 Kaydedildi: {product_name} - {camera} MP")
        print("-" * 50)

    # CSV dosyasını kaydet
    try:
        df = pd.DataFrame(products, columns=["Product Name", "Camera_MP"])
        df.to_csv("ProductsCamera.csv", index=False, encoding="utf-8")
        print(f"✅ {len(products)} ürün ProductsCamera.csv dosyasına kaydedildi")
    except Exception as e:
        print(f"❌ CSV kaydetme hatası: {str(e)}")

    finally:
        driver.quit()


if __name__ == "__main__":
    scraping_prices_from_test_csv()
