import undetected_chromedriver as uc
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

base_url = "https://www.epey.com/akilli-telefonlar/e/YTo0OntpOjE4NzA7YTozOntpOjA7czo3OiIyNTE1MDkzIjtpOjE7czo3OiIyMzg2NTQ3IjtpOjI7czo3OiIyMTk5NDE1Ijt9czo3OiJnYXJhbnRpIjthOjE6e2k6MDtzOjE6IjEiO31zOjU6ImZpeWF0IjthOjI6e2k6MDtzOjQ6IjUwMDAiO2k6MTtzOjY6IjExOTAwMCI7fWk6MTQ7YToyOntpOjA7czoxOiI0IjtpOjE7czoyOiIyNCI7fX1fTjs=/"
productIds = []

for page_num in range(1, 12):
    ua = user_agents[(page_num - 1) % len(user_agents)]

    options = uc.ChromeOptions()
    options.add_argument(f"user-agent={ua}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--headless")  # gizli çalıştırmak istersen

    driver = uc.Chrome(options=options)
    url = f"{base_url}{page_num}/"
    driver.get(url)

    time.sleep(random.randint(3, 6))

    soup = BeautifulSoup(driver.page_source, "html.parser")
    container = soup.select_one("#listele > div.listele.table")

    if container:
        ul_elements = container.find_all("ul")
        print(f"Sayfa {page_num} UL id'leri:")
        for ul in ul_elements[1:]:
            productImg = None
            ul_id = ul.get("id")
            if ul_id and ul_id not in productIds:
                productImg = ul.find("img")
                if productImg:
                    productImgLink = productImg.get("src").replace("k_", "b_")
                    
                    if "reklam" in productImgLink:
                        continue
                else:
                    productImgLink = None

                a_tag = ul.find("a", class_="urunadi")
                if a_tag:
                    productTitle = a_tag.get("title")
                    print(productTitle)
                print(productImgLink)
                productImgLink = productImgLink.replace("k_", "b_")
                productIds.append((ul_id, productImgLink, productTitle))
                print(ul_id)

        driver.quit()

df = pd.DataFrame(productIds, columns=["ProductID", "ProductImage", "ProductName"])
df.to_csv("epeyProductListid.csv", index=False)
