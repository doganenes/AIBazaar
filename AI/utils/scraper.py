from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
from selenium.webdriver.common.keys import Keys
import urllib.parse
import threading
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--window-size=1920,1080")
global driver 

product_lists = [
    "Motorola Fold",
    "Google Pixel 9 Pro",
    "Xiaomi 13 256GB",
    "Iphone 15",

    # Akıllı Telefonlar
    "iPhone 16 Pro",
    "Samsung Galaxy S24 Ultra",
    "Huawei Mate XT Ultimate Design",
    "vivo X200 Pro",
    "HONOR Magic6 Pro",
    "Xiaomi 14 Pro",
    "OPPO Find X7 Pro",
    "OnePlus 12",

    # Dizüstü Bilgisayarlar
    "Apple MacBook Pro 14 inç M3 Pro",
    "ASUS Zenbook S14",
    "ASUS Zenbook S16",
    "Lenovo Şeffaf Ekranlı Laptop",
    "Dell XPS 15 2024",
    "HP Spectre x360 14",
    "Razer Blade 16 2024",
    "MSI Stealth 17 Studio",
    "Acer Swift Edge 16",
    "Samsung Galaxy Book4 Ultra",
    "Microsoft Surface Laptop 6",

    # Giyilebilir Teknolojiler
    "Samsung Galaxy Ring",
    "Apple Watch Ultra AI",
    "Fitbit AI 2",
    "Garmin AI Runners",
    "Huawei Watch GT 4",
    "Xiaomi Smart Band 8 Pro",
    "OPPO Wearable Band",
    "Withings ScanWatch 2",
    "Amazfit Balance",
    "Montblanc Summit 3",

    # Sanal ve Artırılmış Gerçeklik
    "Apple Vision XR",
    "Oculus Quest 4 Pro",
    "Sony PlayStation AR Kit",
    "Meta Quest Vision",
    "HTC Vive XR Elite",
    "Lenovo ThinkReality A3",
    "Magic Leap 2",
    "Nreal Air 2",
    "Pico 4 Enterprise",
    "Xiaomi Wireless AR Glass Discovery Edition",

    # Ses Aksesuarları
    "ANKER Space One Bluetooth Kulaklık",
    "Sennheiser Momentum 4 True Wireless",
    "JBL Tour Pro 2",
    "Sony WF-1000XM5",
    "Bose QuietComfort Ultra Earbuds",
    "Apple AirPods Pro 2",
    "Samsung Galaxy Buds 3 Pro",
    "Beats Studio Buds+",
    "Nothing Ear (2)",
    "Google Pixel Buds Pro"
]



def scraping_prices(product_list):
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.akakce.com/")
    wait = WebDriverWait(driver, 10)
    time.sleep(4)

    all_data = []

    for product_name in product_list:
        product_encoded = urllib.parse.quote_plus(product_name)
        driver.get(f"https://www.akakce.com/arama/?q={product_encoded}")
        first_product_link = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#APL li img"))
        )

        try:
        # ActionChains ile tıkla
            actions = ActionChains(driver)
            actions.move_to_element(first_product_link).click().perform()
            canvas = wait.until(EC.presence_of_element_located((By.ID, "PG_C")))
            tooltip = wait.until(EC.presence_of_element_located((By.ID, "tooltip")))
        except:
            continue
        # Ürün adını al
        try:
            product_name = driver.find_element(By.TAG_NAME, "h1").text.strip()
        except:
            product_name = "Bilinmeyen Ürün"

        # Gerekli kaydırma ve seçim işlemleri
        canvas_width = canvas.size["width"] // 2
        canvas_height = canvas.size["height"] // 2
        canvas_center_y = canvas_height // 2

        start_x = -100
        end_x = canvas_width
        step = 30

        driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
            canvas,
        )
        time.sleep(1)

        try:
            element = driver.find_element(By.XPATH, "//label[@data-len='365']")
            driver.execute_script("arguments[0].click();", element)
        except:
            pass
            print("Grafik gösterimi değiştirilemedi")

        for x in range(start_x, end_x, step):
            try:
                ActionChains(driver).move_to_element_with_offset(
                    canvas, x, canvas_center_y
                ).perform()
                time.sleep(1)

                if tooltip.text and "TL" in tooltip.text:
                    lines = tooltip.text.split("\n")
                    if len(lines) >= 2:
                        date = lines[0].strip()
                        price = lines[1].strip()
                        all_data.append([product_name, date, price])
                        print(f"{x}px → {date}\n{price}")
                else:
                    print(f"{x}px → ⚠️ Boş tooltip")
            except Exception as e:
                print(f"x={x}px → ❌ Hata: {e}")

    driver.quit()

    # CSV'ye yaz
    with open("./csv/akakce.csv", mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["Product Name", "Date", "Price"])
        writer.writerows(all_data)


# scraping_prices(product_lists)


def price_runner(product_list):
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.pricerunner.com")

    wait = WebDriverWait(driver, 10)
    time.sleep(4)

    try:
        reject_button = wait.until(
            EC.element_to_be_clickable((By.ID, "onetrust-reject-all-handler"))
        )
        reject_button.click()
        print("✅ Reject All butonuna tıklandı.")
    except Exception as e:
        print("⚠️ Reject All butonu bulunamadı veya tıklanamadı:", e)

    for product_name in product_list:
        search_input = wait.until(EC.presence_of_element_located((By.NAME, "q")))
        search_input.clear()
        search_input.send_keys(product_name)
        search_input.send_keys(Keys.ENTER)
        search_input.clear()
        print("Arama yapıldı.")

        first_product = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".pr-13k6084-ProductList-grid > div")
            )
        )
        first_product.click()
        print("İlk ürün tıklandı.")
        time.sleep(2)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 1.5);")

        try:
            time.sleep(1)
            popularity_button = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="pricegraph"]/div[3]/div/button[2]/div')
                )
            )
            time.sleep(1)
            popularity_button.click()
        except:
            try:
                driver.execute_script("window.scrollTo(0, 0);")
                # Butonu bul
                price_history_button = driver.find_element(
                    By.XPATH, '//*[@id="product-listing-navigation"]/div/div/button[3]'
                )
                price_history_button.click()
                popularity_button = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, '//*[@id="pricegraph"]/div[3]/div/button[2]')
                    )
                )
                popularity_button.click()
                print("Price history butonuna tıklandı.")
            except:
                try:
                    driver.execute_script("arguments[0].click();", price_history_button)
                    popularity_button = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, '//*[@id="pricegraph"]/div[3]/div/button[2]')
                    )
                )
                    popularity_button.click()
                except:
                    actions = ActionChains(driver)
                    actions.move_to_element(price_history_button).click().perform()
                popularity_button = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, '//*[@id="pricegraph"]/div[3]/div/button[2]')
                    )
                )
                popularity_button.click()
        try:
            month_element = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="pricegraph"]/div[6]/div/div/div/label[3]/span')
                )
            )

            month_element.click()

        except Exception as e:
            print(f"12 ay hatası: {e}")

        time.sleep(3)
    try:
        chart = driver.find_element(By.CLASS_NAME, "highcharts-series")
        actions = ActionChains(driver)
    except:
        pass
        start_x = -100
        end_x = 700
        step = 30
        fixed_y = 50
        tooltip_popularities = []

        for x_offset in range(start_x, end_x, step):
            actions.move_to_element_with_offset(chart, x_offset, fixed_y).perform()
            time.sleep(0.3)
            try:
                tooltip_popularity_element = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "highchart-tooltip__price")
                    )
                )

                tooltip_popularity = tooltip_popularity_element.text
                print(f"Offset {x_offset}: Tooltip Price = {tooltip_popularity}")
                tooltip_popularities.append((product_name, tooltip_popularity))
            except Exception as e:
                print(f"Offset {x_offset}: Tooltip bulunamadı.")
        driver.get("https://www.pricerunner.com")
    driver.quit()

    with open("./csv/price_runner.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Product Name ", "Popularity"])
        writer.writerows(tooltip_popularities)


# price_runner(product_lists)


def scraping_description_and_image(product_list):
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.trendyol.com/")
    wait = WebDriverWait(driver, 10)
    time.sleep(4)

    results = []

    for product_name in product_list:
        try:
            # Arama kutusunu temizle ve tekrar bul
            search_input = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'input[data-testid="suggestion"]')
                )
            )
            search_input.clear()
            search_input.send_keys(product_name)
            search_input.send_keys(Keys.ENTER)

            # Ürün listesini bekle
            wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".prdct-cntnr-wrppr .p-card-wrppr")
                )
            )
            time.sleep(3)

            # İlk ürüne tıkla
            first_product = driver.find_element(
                By.CSS_SELECTOR, ".prdct-cntnr-wrppr .p-card-wrppr"
            )
            main_window = driver.current_window_handle
            first_product.click()

            # Yeni sekmeye geç
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(3)

            # Ürün puanı
            try:
                rating_element = driver.find_element(
                    By.CSS_SELECTOR, ".product-rating-score .value"
                )
                rating_value = rating_element.text.strip()
            except:
                rating_value = None

            # Ürün görseli
            image_element = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".base-product-image img")
                )
            )
            image_src = image_element.get_attribute("src")

            # Ürün özellikleri
            product_details = {}
            try:
                feature_elements = driver.find_elements(
                    By.CSS_SELECTOR, ".detail-attr-container li.detail-attr-item"
                )
                for item in feature_elements:
                    try:
                        key = item.find_element(
                            By.CSS_SELECTOR, ".attr-name.attr-key-name-w"
                        ).text.strip()
                        value = item.find_element(
                            By.CSS_SELECTOR, ".attr-value-name-w"
                        ).text.strip()
                        product_details[key] = value
                        key_value_text = ' '.join(f"{key}:{value};" for key, value in product_details.items())
                        print(key_value_text)
                    except:
                        continue
                results.append((key_value_text,product_name,image_src,rating_value))

            except:
                pass

            # Ürün sekmesini kapat ve ana sekmeye dön
            driver.close()
            driver.switch_to.window(main_window)
            time.sleep(2)

        except Exception as e:
            print(f"Hata oluştu: {product_name} -> {e}")
            continue

    driver.quit()
    with open("./csv/trendyol.csv", mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["Description", "Product Name", "Image", "Rating"])
        writer.writerows(results)



# Örnek kullanım
# a = scraping_description_and_image(product_lists)
# print(a)
threads = []

import threading

threads = []

# Fonksiyonları thread'lere referans olarak ekleyip çalıştırıyoruz
threads.append(threading.Thread(target=scraping_prices, args=(product_lists,)))
threads.append(threading.Thread(target=price_runner, args=(product_lists,)))
# threads.append(
#     threading.Thread(target=scraping_description_and_image, args=(product_lists,))
# )

# Thread'leri başlat
for t in threads:
    t.start()

# Tüm thread'lerin bitmesini bekle
for t in threads:
    t.join()
