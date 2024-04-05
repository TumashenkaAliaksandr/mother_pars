import csv
import random
import string
import requests
from bs4 import BeautifulSoup
import time

# Записываем заголовки столбцов в CSV файл
with open('chokore_product_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Product ID', 'Title', 'Price', 'Description', 'Details', 'Max Image URL', 'Category', 'URL'])

# Функция для получения случайного товарного ID
def generate_product_id():
    return ''.join(random.choices(string.digits, k=8))

# Функция для извлечения данных с карточки товара
def scrape_product_data(url):
    # Генерируем случайный ID из цифр
    product_id = generate_product_id()

    # Отправляем GET-запрос на страницу товара
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим заголовок (title)
    title_element = soup.find('div', {'class': 'custom-title-wishlist'})
    title = title_element.find('h1', recursive=False).text.strip() if title_element else 'No title found'

    # Находим цену (price)
    price_element = soup.find('s', {'class': 'product-single__sale-price'})
    price = price_element.find('span', recursive=False).text.strip().replace('₹', '') if price_element else 'Out of stock'

    # Находим описание (description)
    description_block = soup.find('div', class_='so-tab-content cust-tab4-content')
    description = description_block.text.strip() if description_block else 'No description available'

    # Находим детали (details)
    details_block = soup.find('div', class_='so-tab-content cust_tab2_conTent')
    details = details_block.text.strip() if details_block else 'No details available'

    # Находим все изображения
    image_wrappers = soup.find_all('a', class_='chocolat-image')
    max_image_url = image_wrappers[0]['href'].lstrip('//') if image_wrappers else 'No image URL found'

    # Находим категорию (category)
    breadcrumbs = soup.find('li', class_='breadcrumbs__item category').text.strip() if soup.find('li', class_='breadcrumbs__item category') else 'No category found'

    return {
        'product_id': product_id,
        'title': title,
        'price': price,
        'description': description,
        'details': details,
        'max_image_url': max_image_url,
        'category': breadcrumbs,
        'url': url
    }

# Чтение URL-адреса товара из CSV файла
with open('../urls_csv/product_links.csv', 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Пропускаем заголовки
    for row in reader:
        url = row[0]  # Получаем URL-адрес из первого столбца

        # Извлекаем данные с карточки товара
        product_data = scrape_product_data(url)

        # Записываем данные в CSV файл
        with open('chokore_product_data.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                product_data['product_id'],
                product_data['title'],
                product_data['price'],
                product_data['description'],
                product_data['details'],
                product_data['max_image_url'],
                product_data['category'],
                product_data['url']
            ])

        # Задержка, чтобы не нагружать сервер
        time.sleep(3)  # Подождите 3 секунды между запросами
