import csv
import random
import string
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.parse
import time

# Записываем заголовки столбцов в CSV файл
with open('../done_csv/groovee_shirts.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Product ID', 'Brand', 'Category', 'Solid By', 'Product Detail', 'Title', 'Price', 'Sizes', 'Description', 'Photo URLs', 'URL_Product'])

# Чтение URL-адреса товара из CSV файла
with open('../urls_csv/urls_shirts.csv', 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Пропускаем заголовки
    for row in reader:
        url = row[0]  # Получаем URL-адрес из первого столбца (первый столбец содержит URL)

        # Генерируем случайный ID из цифр
        product_id = ''.join(random.choices(string.digits, k=8))

        # Запускаем браузер
        driver = webdriver.Chrome()
        driver.get(url)

        # Ждем 5 секунд для загрузки страницы
        time.sleep(5)

        # Получаем HTML-код страницы после загрузки JavaScript
        html = driver.page_source

        # Используем BeautifulSoup для парсинга HTML
        soup = BeautifulSoup(html, 'html.parser')

        # Извлекаем данные о товаре
        title = soup.find('div', {'class': 'product-detail'}).find('h1', recursive=False).text.strip()
        price_element = soup.find('del', class_='text-danger')
        if price_element:
            price = price_element.text.strip().replace('₹', '')
        else:
            price = 'Out of stock'
        sizes_container = soup.find('div', {'class': 'option-values d-flex flex-flow flex-wrap'})
        if sizes_container:
            sizes = '|'.join([size.text.strip() for size in sizes_container.find_all('a', {'role': 'button'})])
        else:
            sizes = 'Out of stock'
        brand = 'Groovee'
        category = 'Shirts'
        sub_category_element = soup.find('div', {'class': 'product-brand-wrap mb-2'})
        if sub_category_element:
            sub_category = sub_category_element.find('span', recursive=False).text.strip()
        else:
            sub_category = 'N/A'

        product_details = soup.find_all('div', {'class': 'table-responsive'})
        if product_details:
            product_detail = ''
            for block in product_details:
                tbody = block.find('tbody')
                if tbody:
                    for row in tbody.find_all('tr'):
                        th = row.find('th').text.strip()
                        if th in ['Color', 'Washcare', 'Fabric', 'Occasion']:
                            td = row.find('td')
                            if td:
                                td_text = td.text.strip()
                                product_detail += f"{th}: {td_text}\n"  # Добавляем двоеточие и значения из td
                            else:
                                product_detail += f"{th}: N/A\n"  # Если нет td, добавляем N/A
                else:
                    product_detail = 'N/A'
        else:
            product_detail = 'N/A'

        # Извлекаем описание товара
        description_block = soup.find('div', class_='description')
        if description_block:
            description = description_block.text.strip()
        else:
            description = 'No description available'

        # Извлекаем URL-адреса лучших фотографий товара (размером 1800)
        photo_gallery = soup.find_all('img', class_='feature-image')
        best_photo_urls = set()
        for photo in photo_gallery:
            if '1800' in photo['src']:
                best_photo_urls.add(photo['src'])
            if len(best_photo_urls) == 2:
                break

        # Добавляем данные в CSV файл
        with open('../done_csv/groovee_shirts.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([product_id, brand, category, sub_category, product_detail, title, price, sizes, description, ', '.join(best_photo_urls), url])

        # Закрываем браузер после использования
        driver.quit()
