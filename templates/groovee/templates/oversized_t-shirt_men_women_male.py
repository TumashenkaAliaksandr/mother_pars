import csv
import random
import string
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from bs4 import BeautifulSoup

# ========================= НАСТРОЙКИ =========================
INPUT_CSV = '../urls_csv/urls_oversized_t-shirt_men_women_male.csv'
OUTPUT_CSV = '../done_csv/groovee_oversized_t-shirt_men_women_male_all.csv'

# ============================================================

def get_random_id():
    return ''.join(random.choices(string.digits, k=10))

def clean_description(html_text):
    """Очищает описание от HTML-тегов"""
    if not html_text:
        return "No description available"
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup.get_text(separator=' ').strip()

def make_full_url(url):
    """Превращает относительную ссылку в полную"""
    if not url:
        return ""
    if url.startswith('//'):
        return 'https:' + url
    if url.startswith('/'):
        return 'https://groovee.in' + url
    return url

# Создаём CSV с заголовками
with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([
        'Product ID', 'Brand', 'Category', 'Sold By', 'Product Detail',
        'Title', 'Price', 'Sizes', 'Description', 'Photo URLs', 'URL_Product'
    ])

# Настройки Chrome
chrome_options = Options()
# chrome_options.add_argument("--headless=new")   # Раскомментируй для работы без окна
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Chrome(options=chrome_options)
driver.set_page_load_timeout(35)

try:
    with open(INPUT_CSV, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)  # Пропускаем заголовок

        for row in reader:
            try:
                if not row or not row[0].strip():
                    continue

                url = row[0].strip()
                print(f'Открываю: {url}')

                product_id = get_random_id()
                driver.get(url)

                # Ждём window.product
                try:
                    WebDriverWait(driver, 20).until(
                        lambda d: d.execute_script(
                            "return typeof window.product !== 'undefined' && window.product !== null;")
                    )
                except TimeoutException:
                    print("   Warning: window.product не найден")

                # Получаем данные из JS
                try:
                    product_json = driver.execute_script("return JSON.stringify(window.product);")
                    product = json.loads(product_json)
                except:
                    product = None

                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')

                # ==================== СБОР ДАННЫХ ====================

                brand = "Groovee"
                category = "Oversized T-shirt Mens Women & Male"

                # Title
                title = product.get('title') if product else None
                if not title:
                    h1 = soup.find('h1')
                    title = h1.get_text(strip=True) if h1 else "No Title"

                # Price
                price = None
                if product and product.get('price'):
                    price = str(product['price'] / 100)
                else:
                    price_el = soup.find('del', class_='text-danger') or soup.find('span', class_='price')
                    if price_el:
                        price = price_el.get_text(strip=True).replace('₹', '').replace(',', '').strip()
                price = price or "0"

                # Sizes
                sizes = []
                if product and product.get('variants'):
                    sizes = [v['title'] for v in product['variants'] if v.get('available', False)]
                else:
                    sizes_container = soup.find('div', {'class': 'option-values d-flex flex-flow flex-wrap'})
                    if sizes_container:
                        sizes = [a.get_text(strip=True) for a in sizes_container.find_all('a', {'role': 'button'})]

                sizes_str = '|'.join(sizes) if sizes else "N/A"

                # Description — ОЧИЩЕННЫЙ ТЕКСТ
                description = product.get('description') if product else None
                if not description:
                    desc_block = soup.find('div', class_='description') or soup.find('div', {'id': 'description'})
                    description = desc_block.get_text(separator=' ') if desc_block else "No description available"
                else:
                    description = clean_description(description)

                # Photo URLs — ПОЛНЫЕ ССЫЛКИ
                photo_urls = []
                if product and product.get('images'):
                    photo_urls = [make_full_url(img) for img in product['images'][:6]]
                else:
                    # Fallback
                    for img in soup.find_all('img', class_='feature-image'):
                        src = img.get('src') or img.get('data-src')
                        if src:
                            full_url = make_full_url(src)
                            if full_url not in photo_urls:
                                photo_urls.append(full_url)
                        if len(photo_urls) >= 6:
                            break

                photo_urls_str = ', '.join(photo_urls)

                # ==================== Product Detail (УЛУЧШЕННЫЙ) ====================
                product_detail = ""

                # 1. Новый блок .product-attributes
                attributes = soup.find('div', class_='product-attributes')
                if attributes:
                    for block in attributes.find_all('div', class_='attribute-block'):
                        title_tag = block.find('span', class_='attribute-title')
                        value_tag = block.find('span', class_='attribute-value')
                        if title_tag and value_tag:
                            key = title_tag.get_text(strip=True)
                            value = value_tag.get_text(strip=True)
                            product_detail += f"{key}: {value}\n"

                # 2. Старый блок table-responsive (на всякий случай)
                for block in soup.find_all('div', {'class': 'table-responsive'}):
                    tbody = block.find('tbody')
                    if tbody:
                        for tr in tbody.find_all('tr'):
                            th = tr.find('th')
                            td = tr.find('td')
                            if th and td:
                                th_text = th.get_text(strip=True)
                                if th_text in ['Color', 'Washcare', 'Fabric', 'Occasion', 'Material', 'Fit']:
                                    product_detail += f"{th_text}: {td.get_text(strip=True)}\n"

                if not product_detail.strip():
                    product_detail = "N/A"

                sold_by = "Groovee"

                # Запись в CSV
                with open(OUTPUT_CSV, 'a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        product_id,
                        brand,
                        category,
                        sold_by,
                        product_detail.strip(),
                        title,
                        price,
                        sizes_str,
                        description,
                        photo_urls_str,
                        url
                    ])

                print(f'✓ Успешно: {title[:70]}...')

            except Exception as e:
                print(f'✗ Ошибка при обработке {url}: {e}')

except Exception as e:
    print(f'Критическая ошибка: {e}')

finally:
    driver.quit()
    print('\nПарсинг завершён!')