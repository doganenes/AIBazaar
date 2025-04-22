from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)

driver.get(
    "https://www.akakce.com/vitamin-mineral/en-ucuz-ligone-melatonin-3-mg-90-cigneme-tableti-fiyati,166840700.html"
)

wait = WebDriverWait(driver, 15)

canvas = wait.until(EC.presence_of_element_located((By.ID, "PG_C")))
tooltip = wait.until(EC.presence_of_element_located((By.ID, "tooltip")))

driver.execute_script("arguments[0].scrollIntoView();", canvas)

canvas_width = canvas.size["width"]
canvas_height = canvas.size["height"]
canvas_center_y = canvas_height // 2

print(f"Canvas genişliği: {canvas_width}px")

start_x = 1  # 0 yerine 1, çünkü 0 bazen erişim hatası verebilir
end_x = canvas_width - 1
step = 10

prices = []

for x in range(start_x, end_x, step):
    try:
        ActionChains(driver).move_to_element_with_offset(
            canvas, x, canvas_center_y
        ).perform()
        time.sleep(0.5)

        tooltip_text = tooltip.get_attribute("textContent").strip()
        if tooltip_text:
            prices.append((x, tooltip_text))
            print(f"x={x}px → {tooltip_text}")
        else:
            prices.append((x, "Boş/Tooltip çıkmadı"))
            print(f"x={x}px → ⚠️ Boş tooltip")

    except Exception as e:
        print(f"x={x}px → ❌ Hata: {e}")
        prices.append((x, "Hata"))

driver.quit()

print("\n🎯 Toplanan Veriler:")
for x, p in prices:
    print(f"{x}px → {p}")
