import csv
import random
import string
import time
import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
from bs4 import BeautifulSoup
import urllib.parse


INPUT_FILE = '../urls_csv/urls_jackets.csv'
OUTPUT_FILE = '../done_csv/groovee_jackets.csv'

BASE_URL = "https://groovee.in"


# -----------------------------
# CSV HEADER
# -----------------------------
with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([
        'Product ID',
        'Brand',
        'Category',
        'Sold By',
        'Product Detail',
        'Title',
        'Price',
        'Sizes',
        'Description',
        'Photo URLs',
        'URL_Product'
    ])


# -----------------------------
# URL FIX FUNCTION
# -----------------------------
def make_full_url(url: str) -> str:
    if not url:
        return ""

    url = url.strip()

    if url.startswith("//"):
        return "https:" + url

    if url.startswith("/"):
        return urllib.parse.urljoin(BASE_URL, url)

    return url


# -----------------------------
# RANDOM ID
# -----------------------------
def rand_id():
    return ''.join(random.choices(string.digits, k=10))


def safe(el):
    return el.text.strip() if el else 'N/A'


# -----------------------------
# CHROME
# -----------------------------
options = Options()

# options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options)
driver.set_page_load_timeout(25)


try:
    with open(INPUT_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)

        for row in reader:

            if not row or not row[0].strip():
                continue

            raw_url = row[0].strip()

            # ✅ FIX URL HERE
            url = make_full_url(raw_url)

            print(f"\n➡ {url}")

            product_id = rand_id()

            try:
                driver.get(url)

            except TimeoutException:
                print("⛔ Timeout -> stop loading")
                driver.execute_script("window.stop();")

            except WebDriverException as e:
                print(f"⛔ Driver error: {e}")
                continue

            time.sleep(5)

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # -----------------------------
            # JS PRODUCT
            # -----------------------------
            product = None
            try:
                js = driver.execute_script(
                    "return window.product ? JSON.stringify(window.product) : null;"
                )
                if js:
                    product = json.loads(js)
            except:
                product = None

            # -----------------------------
            # TITLE
            # -----------------------------
            title = 'N/A'
            if product and product.get('title'):
                title = product['title']
            else:
                h1 = soup.select_one('div.product-detail h1')
                title = safe(h1)

            # -----------------------------
            # PRICE
            # -----------------------------
            price = "Out of stock"

            if product and product.get('price'):
                price = str(product['price'] / 100)
            else:
                price_el = soup.find('del', class_='text-danger') or soup.find('span', class_='price')
                if price_el:
                    price = price_el.text.strip().replace('₹', '').replace(',', '').strip()

            # -----------------------------
            # SIZES
            # -----------------------------
            sizes = []

            if product and product.get('variants'):
                sizes = [v.get('title') for v in product['variants'] if v.get('title')]
            else:
                sizes_block = soup.find('div', class_='option-values d-flex flex-flow flex-wrap')
                if sizes_block:
                    sizes = [a.text.strip() for a in sizes_block.find_all('a', {'role': 'button'})]

            sizes_str = '|'.join(sizes) if sizes else "N/A"

            # -----------------------------
            # DESCRIPTION
            # -----------------------------
            description = "No description available"

            if product and product.get('description'):
                description = BeautifulSoup(product['description'], 'html.parser').get_text(" ").strip()
            else:
                desc = soup.find('div', class_='description')
                if desc:
                    description = desc.get_text(" ").strip()

            # -----------------------------
            # PHOTOS
            # -----------------------------
            photos = []

            if product and product.get('images'):
                photos = product['images'][:6]
            else:
                for img in soup.find_all('img', class_='feature-image'):
                    src = img.get('src') or img.get('data-src')
                    if src:
                        photos.append(src)
                    if len(photos) >= 6:
                        break

            # ✅ FIX PHOTO URLS TOO
            photos = [make_full_url(p) for p in photos]
            photos = list(dict.fromkeys(photos))
            photos_str = ', '.join(photos)

            # -----------------------------
            # PRODUCT DETAIL
            # -----------------------------
            detail = []

            for block in soup.select('.product-attributes .attribute-block'):
                t = block.select_one('.attribute-title')
                v = block.select_one('.attribute-value')
                if t and v:
                    detail.append(f"{t.text.strip()}: {v.text.strip()}")

            for tr in soup.select('table tr'):
                th = tr.find('th')
                td = tr.find('td')

                if th and td:
                    key = th.text.strip()
                    if key in ['Color', 'Washcare', 'Fabric', 'Occasion', 'Material', 'Fit']:
                        detail.append(f"{key}: {td.text.strip()}")

            product_detail = '|'.join(detail) if detail else "N/A"

            # -----------------------------
            # SAVE
            # -----------------------------
            with open(OUTPUT_FILE, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)

                writer.writerow([
                    product_id,
                    "Groovee",
                    "Jackets",
                    "Groovee",
                    product_detail,
                    title,
                    price,
                    sizes_str,
                    description,
                    photos_str,
                    url  # ✅ FULL URL NOW
                ])

            print(f"✔ {title[:60]}")

finally:
    driver.quit()
    print("\nDONE")