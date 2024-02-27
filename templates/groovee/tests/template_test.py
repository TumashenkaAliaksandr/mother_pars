import csv
import random
import string
from selenium import webdriver
from bs4 import BeautifulSoup

# Чтение URL-адреса товара из CSV файла
with open('../urls_csv/urls_groovee_tsh.csv', 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Пропускаем заголовки
    for row in reader:
        url = row[0]  # Получаем URL-адрес из первого столбца (первый столбец содержит URL)

        # Генерируем случайный ID из цифр
        product_id = ''.join(random.choices(string.digits, k=8))

        # Запускаем браузер
        driver = webdriver.Chrome()
        driver.get(url)

        # Получаем HTML-код страницы после загрузки JavaScript
        html = driver.page_source

        # Используем BeautifulSoup для парсинга HTML
        soup = BeautifulSoup(html, 'html.parser')

        # Извлекаем данные о товаре
        title = soup.find('div', {'class': 'product-detail'}).find('h1', recursive=False).text.strip()
        price = soup.find('del', class_='text-danger').text.strip().replace('₹', '')
        sizes_container = soup.find('div', {'class': 'option-values d-flex flex-flow flex-wrap'})
        sizes = '|'.join([size.text.strip() for size in sizes_container.find_all('a', {'role': 'button'})])
        description_block = soup.find('div', class_='description')
        descriptions = '\n'.join([description.text.strip() for description in description_block.find_all('p')])
        brand = 'Groovee'
        category = 'Oversized T-shirts'
        sub_category = soup.find('div', {'class': 'product-brand-wrap mb-2'}).find('span', recursive=False).text.strip()

        # Извлекаем URL-адреса лучших фотографий товара (размером 1800)
        photo_gallery = soup.find_all('img', class_='feature-image')
        best_photo_urls = set()  # Множество для уникальных ссылок
        for photo in photo_gallery:
            if '1800' in photo['src']:
                best_photo_urls.add(photo['src'])
            if len(best_photo_urls) == 2:  # Прекращаем поиск после того, как найдены 2 уникальные ссылки
                break

        # Создаем CSV файл и записываем данные
        with open('groovee_product_details.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Product ID', 'Brand', 'Category', 'Solid By', 'Title', 'Price', 'Sizes', 'Description', 'Photo URLs', 'URL_Product'])
            writer.writerow([product_id, brand, category, sub_category, title, price, sizes, descriptions, ', '.join(best_photo_urls), url])

        # Закрываем браузер после использования
        driver.quit()
