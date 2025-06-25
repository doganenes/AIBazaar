from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import csv
import urllib.parse
import threading
import random
from thefuzz import fuzz
import pandas as pd

# Global list to store all scraped data
all_data = []


def find_best_match(product_name: str, product_titles: list, threshold=60):
    """Find the best matching product title using fuzzy string matching"""
    best_match = None
    best_score = 0
    all_scores = []

    print(f"🔍 Benzerlik skorları ('{product_name}' için):")
    for title in product_titles:
        score = fuzz.ratio(product_name.lower(), title.lower())
        all_scores.append((title, score))
        print(f"   📊 {score}% - {title}")
        if score >= threshold and score > best_score:
            best_match = title
            best_score = score

    print(f"🎯 En yüksek skor: {best_score}% (Eşik: {threshold}%)")
    return best_match, best_score, all_scores
import os


def write_row_to_csv_df(row_data, file_path="./csv/yeniakakce.csv"):
    df_row = pd.DataFrame(
        [row_data], columns=["Product Name", "Date", "Price", "Image"]
    )
    if not os.path.isfile(file_path):
        df_row.to_csv(
            file_path, mode="w", header=True, index=False, encoding="utf-8-sig"
        )
    else:
        df_row.to_csv(
            file_path, mode="a", header=False, index=False, encoding="utf-8-sig"
        )


def scraping_prices(product_list):
    """Scrape prices and chart history from Akakce for a list of products"""
    global all_data

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://www.akakce.com/")
        time.sleep(2)

        for product_name in product_list[223:]:
            print(f"\n🔍 Ürün aranıyor: {product_name}")
            price = 0
            image = ""

            try:
                search_query = urllib.parse.quote_plus(product_name)
                driver.get(f"https://www.akakce.com/arama/?q={search_query}")

                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located(
                            (By.CSS_SELECTOR, "#APL > li")
                        )
                    )
                    list_items = driver.find_elements(By.CSS_SELECTOR, "#APL > li")
                except TimeoutException:
                    print(f"❌ Arama sonucu alınamadı: {product_name}")
                    continue

                if not list_items:
                    print(f"❌ Ürün bulunamadı: {product_name}")
                    continue

                h3_titles = []
                for li in list_items[:10]:
                    try:
                        h3 = li.find_element(By.CSS_SELECTOR, "h3.pn_v8")
                        h3_titles.append(h3.text)
                    except NoSuchElementException:
                        continue

                if not h3_titles:
                    print("❌ H3 başlıkları bulunamadı.")
                    continue

                best_match, score, _ = find_best_match(product_name, h3_titles)

                if not best_match:
                    print("❌ Yeterli benzerlikte ürün bulunamadı.")
                    continue

                for li in list_items[:10]:
                    try:
                        h3 = li.find_element(By.CSS_SELECTOR, "h3.pn_v8")
                        if h3.text.strip() == best_match:
                            print(f"🎯 Eşleşen ürün: {h3.text}")
                            product_link = li.find_element(
                                By.CLASS_NAME, "pw_v8"
                            ).get_attribute("href")
                            driver.get(product_link)
                            time.sleep(1)

                            try:
                                product_image = driver.find_element(
                                    By.CLASS_NAME, "img_w"
                                )
                                image = product_image.get_attribute("href")
                                print(f"🖼️ Ürün görseli: {image}")
                            except:
                                image = ""

                            break
                    except Exception as e:
                        print(f"⚠️ Hata: {e}")

                # Start price graph scraping
                try:
                    wait = WebDriverWait(driver, 10)
                    canvas = wait.until(EC.presence_of_element_located((By.ID, "PG_C")))
                    tooltip = wait.until(
                        EC.presence_of_element_located((By.ID, "tooltip"))
                    )

                    try:
                        chart_toggle = driver.find_element(
                            By.XPATH, "//label[@data-len='365']"
                        )
                        driver.execute_script("arguments[0].click();", chart_toggle)
                    except:
                        print("⚠️ Grafik değiştirme başarısız")

                    canvas_width = canvas.size["width"] // 2
                    canvas_height = canvas.size["height"] // 2

                    driver.execute_script(
                        "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                        canvas,
                    )
                    time.sleep(1)

                    for x in range(-100, canvas_width, 1):
                        try:
                            ActionChains(driver).move_to_element_with_offset(
                                canvas, x, canvas_height
                            ).perform()
                            if tooltip.text and "TL" in tooltip.text:
                                lines = tooltip.text.split("\n")
                                if len(lines) >= 2:
                                    date = lines[0].strip()
                                    price = lines[1].strip()
                                    h1_title = driver.find_element(
                                        By.TAG_NAME, "h1"
                                    ).text.strip()
                                    write_row_to_csv_df([product_name, date, price, image])
                                    print(f"💾 Kaydedildi → {product_name} | {date} | {price}")
                                    print(f"{x}px → {date}: {price}")
                        except Exception as e:
                            continue

                except Exception as e:
                    print(f"❌ Grafik verisi alınamadı: {e}")

            except Exception as e:
                print(f"❌ Genel hata: {e}")
                continue

    finally:
        driver.quit()


def main():
    """Main entry point for scraping"""
    try:
        phones = pd.read_csv(r"C:\Users\pc\Desktop\AIbazaar\AIBazaar\AI\utils\newProduct.csv")
        product_list = (phones["Product Name"]).tolist()
        print(f"📦 {len(product_list)} ürün işlenecek...")

        # Threading setup
        thread = threading.Thread(target=scraping_prices, args=(product_list,))
        thread.start()
        thread.join()

        print("✅ Tüm işlemler tamamlandı!")

    except Exception as e:
        print(f"❌ Ana fonksiyon hatası: {e}")


if __name__ == "__main__":
    main()
