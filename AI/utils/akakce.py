from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# Tarama yapılacak ürün linkleri
product_urls = [
    "https://www.akakce.com/vitamin-mineral/en-ucuz-ligone-melatonin-3-mg-90-cigneme-tableti-fiyati,166840700.html",
    "https://www.akakce.com/cep-telefonu/en-ucuz-iphone-15-fiyati,1745758198.html"
]

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)

all_data = []

for url in product_urls:
    driver.get(url)
    wait = WebDriverWait(driver, 15)

    canvas = wait.until(EC.presence_of_element_located((By.ID, "PG_C")))
    tooltip = wait.until(EC.presence_of_element_located((By.ID, "tooltip")))

    # Ürün adını al
    try:
        product_name = driver.find_element(By.TAG_NAME, "h1").text.strip()
    except:
        product_name = "Bilinmeyen Ürün"

    # Gerekli kaydırma ve seçim işlemleri
    canvas_width = canvas.size['width'] // 2
    canvas_height = canvas.size['height'] // 2
    canvas_center_y = canvas_height // 2

    start_x = -100
    end_x = canvas_width
    step = 30

    driver.execute_script(
        "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", canvas
    )
    time.sleep(1)

    try:
        element = driver.find_element(By.XPATH, "//label[@data-len='365']")
        driver.execute_script("arguments[0].click();", element)
    except:
        print("Grafik gösterimi değiştirilemedi")

    for x in range(start_x, end_x, step):
        try:
            ActionChains(driver).move_to_element_with_offset(canvas, x, canvas_center_y).perform()
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
with open("product_data.csv", mode="w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerow(["Product Name", "Date", "Price"])
    writer.writerows(all_data)

print("\n✅ Veriler 'product_data.csv' dosyasına yazıldı.")