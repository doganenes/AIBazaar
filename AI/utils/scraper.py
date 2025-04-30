from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
from selenium.webdriver.common.keys import Keys

# # Tarama yapılacak ürün linkleri
# product_urls = [
#     "https://www.akakce.com/vitamin-mineral/en-ucuz-ligone-melatonin-3-mg-90-cigneme-tableti-fiyati,166840700.html",
#     "https://www.akakce.com/cep-telefonu/en-ucuz-iphone-15-fiyati,1745758198.html"
# ]

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=options)

# all_data = []

# for url in product_urls:
#     driver.get(url)
#     wait = WebDriverWait(driver, 15)

#     canvas = wait.until(EC.presence_of_element_located((By.ID, "PG_C")))
#     tooltip = wait.until(EC.presence_of_element_located((By.ID, "tooltip")))

#     # Ürün adını al
#     try:
#         product_name = driver.find_element(By.TAG_NAME, "h1").text.strip()
#     except:
#         product_name = "Bilinmeyen Ürün"

#     # Gerekli kaydırma ve seçim işlemleri
#     canvas_width = canvas.size['width'] // 2
#     canvas_height = canvas.size['height'] // 2
#     canvas_center_y = canvas_height // 2

#     start_x = -100
#     end_x = canvas_width
#     step = 30

#     driver.execute_script(
#         "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", canvas
#     )
#     time.sleep(1)

#     try:
#         element = driver.find_element(By.XPATH, "//label[@data-len='365']")
#         driver.execute_script("arguments[0].click();", element)
#     except:
#         print("Grafik gösterimi değiştirilemedi")

#     for x in range(start_x, end_x, step):
#         try:
#             ActionChains(driver).move_to_element_with_offset(canvas, x, canvas_center_y).perform()
#             time.sleep(1)

#             if tooltip.text and "TL" in tooltip.text:
#                 lines = tooltip.text.split("\n")
#                 if len(lines) >= 2:
#                     date = lines[0].strip()
#                     price = lines[1].strip()
#                     all_data.append([product_name, date, price])
#                     print(f"{x}px → {date}\n{price}")
#             else:
#                 print(f"{x}px → ⚠️ Boş tooltip")
#         except Exception as e:
#             print(f"x={x}px → ❌ Hata: {e}")

# driver.quit()

# # CSV'ye yaz
# with open("product_data.csv", mode="w", newline="", encoding="utf-8-sig") as file:
#     writer = csv.writer(file)
#     writer.writerow(["Product Name", "Date", "Price"])
#     writer.writerows(all_data)


def price_runner():

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

    
    search_input = wait.until(EC.presence_of_element_located((By.NAME, "q")))
    search_input.clear()
    search_input.send_keys("iphone 14")
    search_input.send_keys(Keys.ENTER)
    print("Arama yapıldı.")

    first_product = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".pr-13k6084-ProductList-grid > div")
        )
    )
    first_product.click()
    print("İlk ürün tıklandı.")
    time.sleep(2)
  
    time.sleep(3)

    try:
        # Butonu bul
        price_history_button = driver.find_element(
            By.XPATH, '//*[@id="product-listing-navigation"]/div/div/button[3]'
        )
        price_history_button.click()
        print("Price history butonuna tıklandı.")
    except:
        try:
            driver.execute_script("arguments[0].click();", price_history_button)
        except:
            actions = ActionChains(driver)
            actions.move_to_element(price_history_button).click().perform()
    try:
        popularity_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="pricegraph"]/div[3]/div/button[2]')
            )
        )
        popularity_button.click()
    except Exception as e:
        print(f"Popülerlik butonuna tıklanamadı: {e}")
        
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

    chart = driver.find_element(By.CLASS_NAME, "highcharts-series")
    actions = ActionChains(driver)

    start_x = -100
    end_x = 700
    step = 30
    fixed_y = 50  
    tooltip_prices = []

    for x_offset in range(start_x, end_x, step):
        actions.move_to_element_with_offset(chart, x_offset, fixed_y).perform()
        time.sleep(0.3)         
        try:
            tooltip_price_element = WebDriverWait(driver, 2).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "highchart-tooltip__price"))
            )
            tooltip_date=WebDriverWait(driver, 2).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "highchart-tooltip__date"))
            )
            tooltip_date = tooltip_date.text
            tooltip_price = tooltip_price_element.text
            print(f"Offset {x_offset}: Tooltip Price = {tooltip_price} | Date = {tooltip_date}")
            tooltip_prices.append((x_offset, tooltip_price))
        except Exception as e:
            print(f"Offset {x_offset}: Tooltip bulunamadı.")
    driver.quit()

    print("\nToplanan Tüm Tooltip Değerleri:")
    for offset, price in tooltip_prices:
        print(f"Offset {offset}: {price}")


# price_runner()

def scraping_description_and_image(product_list):
    driver.get("https://www.trendyol.com/")
    wait = WebDriverWait(driver, 10)
    time.sleep(4)

    results = []

    for product_name in product_list:
        try:
            # Arama kutusunu temizle ve tekrar bul
            search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-testid="suggestion"]')))
            search_input.clear()
            search_input.send_keys(product_name)
            search_input.send_keys(Keys.ENTER)

            # Ürün listesini bekle
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.prdct-cntnr-wrppr .p-card-wrppr')))
            time.sleep(3)

            # İlk ürüne tıkla
            first_product = driver.find_element(By.CSS_SELECTOR, '.prdct-cntnr-wrppr .p-card-wrppr')
            main_window = driver.current_window_handle
            first_product.click()

            # Yeni sekmeye geç
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(3)

            # Ürün puanı
            try:
                rating_element = driver.find_element(By.CSS_SELECTOR, '.product-rating-score .value')
                rating_value = rating_element.text.strip()
            except:
                rating_value = None

            # Ürün görseli
            image_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.base-product-image img')))
            image_src = image_element.get_attribute("src")

            # Ürün özellikleri
            product_details = {}
            try:
                feature_elements = driver.find_elements(By.CSS_SELECTOR, '.detail-attr-container li.detail-attr-item')
                for item in feature_elements:
                    try:
                        key = item.find_element(By.CSS_SELECTOR, '.attr-name.attr-key-name-w').text.strip()
                        value = item.find_element(By.CSS_SELECTOR, '.attr-value-name-w').text.strip()
                        product_details[key] = value
                    except:
                        continue
            except:
                pass

            results.append({
                "product": product_name,
                "image": image_src,
                "details": product_details,
                "rating": rating_value
            })

            # Ürün sekmesini kapat ve ana sekmeye dön
            driver.close()
            driver.switch_to.window(main_window)
            time.sleep(2)

        except Exception as e:
            print(f"Hata oluştu: {product_name} -> {e}")
            continue

    driver.quit()
    return results


# Örnek kullanım
product_lists = ["iPhone 15", "Samsung Galaxy S24", "Xiaomi 13"]
a = scraping_description_and_image(product_lists)
print(a)