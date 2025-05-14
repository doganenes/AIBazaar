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
    "Apple iPhone 16 Pro Max 1TB",
    "Apple iPhone 16 Pro Max 512TB",
    "Apple iPhone 16 Plus 512GB",
    "Apple iPhone 16 Pro Max 256GB",
    "Apple iPhone 15 Pro Max 512 GB",
    "Apple iPhone 16 Pro 512GB",
    "Honor Magic V3 512 GB 12 GB Ram",
    "Apple iPhone 15 Pro 1 TB",
    "Apple iPhone 16 512GB",
    "Samsung Galaxy Z Fold6 12/256GB",
    "Samsung Galaxy S25 Ultra 1 TB Titanyum",
    "Xiaomi Mi 14 Ultra 16/512 Gb",
    "vivo X200 Pro 16/512gb",
    "Apple İphone 14 Pro 128 Gb",
    "Apple İphone 14 Pro 256 Gb",
    "Apple İphone 14 Pro 512 Gb",
    "Apple iPhone 14 Plus 512 GB",
    "Samsung Galaxy S25 Ultra 512 GB",
    "Samsung Galaxy Z Fold5 1 TB 12 GB Ram",
    "Xiaomi 15 Ultra 512 GB, Siyah",
    "Samsung Yenilenmiş Galaxy S24 Ultra 1TB",
    "Samsung Galaxy Z Fold6 512 GB",
    "Apple iPhone 14 Plus 256 GB",
    "Apple Iphone 15 Pro 256gb",
    "Honor Magic V2 512 GB 16 GB Ram",
    "Xiaomi Mix Flip 12/512 GB",
    "Samsung Galaxy S23 Ultra 512 GB",
    "Huawei Pura 70 Ultra 16 GB RAM 512 GB",
    "vivo X100 Pro 512 GB 16 GB Ram",
    "Samsung Galaxy S25+ 512 GB",
    "Samsung Galaxy S25+ 256 GB",
    "AGM Mobile AGM G2 GUARDIAN",
    "TECNO PHANTOM V2 FOLD 5G 12+512",
    "Huawei HUAWEI MATE X3 512GB",
    "Nubia Red Magic 9s Pro 16 Gb 512",
    "Honor Magic 7 Pro 512 GB 12 GB Ram",
    "Samsung Galaxy Z Fold4 256 GB 12 GB Ram",
    "Apple Yenilenmiş Iphone 13 Pro Max 256 Gb",
    "Samsung Z Fold 5 512 GB 5G",
    "Samsung Galaxy S23 Ultra 256 GB",
    "ULEFONE Armor 27t Pro",
    "Samsung Galaxy Z Flip 6 512 Gb",
    "Samsung Galaxy Z Flip 6 256 Gb",
    "Samsung Galaxy Z Flip5 512 GB",
    "Samsung Galaxy Z Flip5 256 GB",
    "Xiaomi 14t Pro 12gb/1tb",
    "Apple iPhone 12 Pro Max 512 GB",
    "SAMSUNG GALAXY S22 ULTRA 512GB"
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
            actions = ActionChains(driver)
            actions.move_to_element(first_product_link).click().perform()
            canvas = wait.until(EC.presence_of_element_located((By.ID, "PG_C")))
            tooltip = wait.until(EC.presence_of_element_located((By.ID, "tooltip")))
        except:
            continue

        try:
            product_name = driver.find_element(By.TAG_NAME, "h1").text.strip()
        except:
            product_name = "Bilinmeyen Ürün"

        canvas_width = canvas.size["width"] // 2
        canvas_height = canvas.size["height"] // 2
        canvas_center_y = canvas_height // 2

        start_x = -100
        end_x = canvas_width
        step = 1

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

    with open("./csv/akakce.csv", mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["Product Name", "Date", "Price"])
        writer.writerows(all_data)


# scraping_prices(product_lists)

def scraping_description_and_image(product_list):
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.trendyol.com/")
    wait = WebDriverWait(driver, 10)
    time.sleep(4)

    results = []

    for product_name in product_list:
        try:
            search_input = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'input[data-testid="suggestion"]')
                )
            )
            search_input.clear()
            search_input.send_keys(product_name)
            search_input.send_keys(Keys.ENTER)

            wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".prdct-cntnr-wrppr .p-card-wrppr")
                )
            )
            time.sleep(3)

            first_product = driver.find_element(
                By.CSS_SELECTOR, ".prdct-cntnr-wrppr .p-card-wrppr"
            )
            main_window = driver.current_window_handle
            first_product.click()

            driver.switch_to.window(driver.window_handles[1])
            time.sleep(3)

            try:
                rating_element = driver.find_element(
                    By.CSS_SELECTOR, ".product-rating-score .value"
                )
                rating_value = rating_element.text.strip()
                price_product = driver.find_element(By.CSS_SELECTOR,".prc-dsc")
                price_product = price_product.text.replace(" TL","")
                print(f"Product price: {price_product}")
            except:
                rating_value = None

            image_element = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".base-product-image img")
                )
            )
            image_src = image_element.get_attribute("src")

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
                    # print(key_value_text)
                    except:
                        continue
                results.append((key_value_text,product_name,image_src,rating_value,price_product))

            except:
                pass

            driver.close()
            driver.switch_to.window(main_window)
            time.sleep(2)

        except Exception as e:
            print(f"Hata oluştu: {product_name} -> {e}")
            continue

    driver.quit()
    with open("./csv/trendyol.csv", mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["Description", "Product Name", "Image", "Rating","Price"])
        writer.writerows(results)


# a = scraping_description_and_image(product_lists)
# print(a)
threads = []


# threads = []

# threads.append(threading.Thread(target=scraping_prices, args=(product_lists,)))
threads.append(
     threading.Thread(target=scraping_description_and_image, args=(product_lists,))
 )

for t in threads:
    t.start()

for t in threads:
    t.join()
