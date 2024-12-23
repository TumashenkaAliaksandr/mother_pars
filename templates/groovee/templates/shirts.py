import csv
import random
import string
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.parse
import time

# Записываем заголовки столбцов в CSV файл
with open('../done_csv/groovee_oversize_shirts.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Product ID', 'Brand', 'Category', 'Designed By & Brands', 'Title', 'Price', 'Sizes', 'Description', 'Photo URLs', 'URL_Product'])

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
        title = soup.find('div', {'class': 'main-product__details-wrapper'}).find('h1', recursive=False).text.strip()
        print('Title:', title)
        price_element = soup.find('ins', class_='price__sale')
        if price_element:
            price = price_element.text.strip().replace('₹', '')
        else:
            price = 'Out of stock'
        print('Price:', price)
        # Находим контейнер с размерами
        sizes_container = soup.find('div', {'class': 'main-product__form-group'})
        if sizes_container:
            # Извлекаем все размеры из элементов <label>
            sizes = '|'.join([size.text.strip() for size in sizes_container.find_all('label')])
        else:
            sizes = 'Out of stock'
        print('Sizes:', sizes)

        # Находим все <span> внутри <div class="bdv-wrap">
        spans = soup.find('div', {'class': 'bdv-wrap'}).find_all('span')
        # Извлечение текста из каждого <span>
        for span in spans:
            print(span.text.strip())

        # Находим все <span> внутри <div class="bdv-wrap">
        spans = soup.find('div', {'class': 'bdv-wrap'}).find_all('span')

        # Извлечение текста из каждого <span>
        designed_by_brands = ' | '.join([span.get_text(strip=True) for span in spans])
        print('Dis & Brends:', designed_by_brands)

        category = 'Oversized-tshirts'
        # sub_category_element = soup.find('div', {'class': 'product-brand-wrap mb-2'})
        # if sub_category_element:
        #     sub_category = sub_category_element.find('span', recursive=False).text.strip()
        # else:
        #     sub_category = 'N/A'
        #
        # product_details = soup.find_all('div', {'class': 'table-responsive'})
        # if product_details:
        #     product_detail = ''
        #     for block in product_details:
        #         tbody = block.find('tbody')
        #         if tbody:
        #             for row in tbody.find_all('tr'):
        #                 th = row.find('th').text.strip()
        #                 if th in ['Color', 'Washcare', 'Fabric', 'Occasion']:
        #                     td = row.find('td')
        #                     if td:
        #                         td_text = td.text.strip()
        #                         product_detail += f"{th}: {td_text}\n"  # Добавляем двоеточие и значения из td
        #                     else:
        #                         product_detail += f"{th}: N/A\n"  # Если нет td, добавляем N/A
        #         else:
        #             product_detail = 'N/A'
        # else:
        #     product_detail = 'N/A'

        # Находим контейнер с описанием
        description_block = soup.find('div', class_='accordion__content')
        if description_block:
            description = description_block.text.strip()  # Извлекаем текст и убираем лишние пробелы
        else:
            description = 'No description available'

        print('Description:', description)

        # Находим div с классом 'main-product__media-wrapper'
        media_wrapper = soup.find('div', class_='main-product__media-wrapper')

        if media_wrapper:
            # Находим первое изображение внутри этого div
            photo = media_wrapper.find('img')
            if photo:
                # Извлекаем URL изображения и добавляем https: если необходимо
                photo_url = photo['src']
                if photo_url.startswith('//'):
                    photo_url = 'https:' + photo_url  # Добавляем https:
            else:
                photo_url = 'No image available'
        else:
            photo_url = 'No media wrapper available'

        print('Photo URL:', photo_url)

        # Добавляем данные в CSV файл
        with open('../done_csv/groovee_oversize_shirts.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([product_id, span, category, designed_by_brands, title, price, sizes, description, photo_url, url])

        # Закрываем браузер после использования
        driver.quit()
