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

    driver.get("https://www.pricerunner.com/")  # doğru URL'yi buraya koyman lazım

    wait = WebDriverWait(driver, 10)
    time.sleep(4)
    # 1. Arama inputuna yaz ve Enter'a bas
    search_input = wait.until(EC.presence_of_element_located((By.NAME, "q")))
    search_input.clear()
    search_input.send_keys("iphone 14")
    search_input.send_keys(Keys.ENTER)
    print("Arama yapıldı.")

    # 2. Ürünler yüklenene kadar bekle ve ilk ürünü tıkla
    first_product = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".pr-13k6084-ProductList-grid > div")))
    first_product.click()
    print("İlk ürün tıklandı.")
    time.sleep(2)
    # 3. Sayfa yüklenmesini bekle
    page_height = driver.execute_script("return document.body.scrollHeight")

    # 2. Sayfayı yarıya kadar kaydır
    driver.execute_script(f"window.scrollTo(0, {page_height / 1.1});")

    time.sleep(3)
    
    try:
        # Butonu bul
        price_history_button = driver.find_element(By.CSS_SELECTOR, ".pr-wyywe-Tabs-item")

        # Tıklamayı dene
        try:
            price_history_button.click()
        except:
            try:
                driver.execute_script("arguments[0].click();", price_history_button)
            except:
                actions = ActionChains(driver)
                actions.move_to_element(price_history_button).click().perform()

        print("history btn doğru çalışıyor")
    except Exception as e:
        print(f"price history hata nedeni: {e}")

    # 4. Popularity sekmesine tıkla
    try:
        popularity_tab = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "pr-1hs0xe7-Tabs-content")))
        popularity_tab.click()
        print("Popularity sekmesine tıklandı.")
    except Exception as e:
        print(f"Popularity hatası: {e}" )

    # 5. 12 months seçimi
    month_selector = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class,'Selector-button')]")))
    month_selector.click()
    print("Ay seçimi açıldı.")

    # 12 months seçeneğini seç
    try:
        twelve_months_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "pr-o7x5sf-Selector-button")))
        twelve_months_option.click()
        print("12 months seçildi.")

    except Exception as e:
        print(f"12 ay hatası: {e}" )
  
    # 6. Chart içine mouse hareket ettirme
    time.sleep(3)  # Grafik tam yüklensin

    # Chart alanını bul
    chart_div = wait.until(EC.presence_of_element_located((By.XPATH, "//div[starts-with(@id, 'highcharts-')]")))

    # ActionChains ile mouse hareket ettir
    actions = ActionChains(driver)

    chart_width = chart_div.size['width']
    chart_height = chart_div.size['height']

    start_x = chart_div.location['x']
    start_y = chart_div.location['y'] + chart_height // 2

    # x ekseninde 10 adımda hareket ettir
    for i in range(0, chart_width, 30):  # 30 piksellik adımlarla
        actions.move_to_element_with_offset(chart_div, i, chart_height // 2).perform()
        time.sleep(0.5)  # Tooltip değişimini bekle

        try:
            price_tooltip = driver.find_element(By.CLASS_NAME, "highchart-tooltip__price")
            print(f"Tooltip Price: {price_tooltip.text}")
        except:
            print("Tooltip bulunamadı.")

    # İşlem bittiğinde tarayıcıyı kapat
    driver.quit()

    print("\n✅ Veriler 'product_data.csv' dosyasına yazıldı.")


price_runner()