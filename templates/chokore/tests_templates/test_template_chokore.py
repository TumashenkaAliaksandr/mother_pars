import requests
from bs4 import BeautifulSoup
import csv
import random

# Функция для получения случайного товарного ID
def get_random_product_id():
    # Ваша логика для получения случайного ID товара
    return 'chokore-vintage-cowboy-hat-chocolate-brown'

# Функция для извлечения данных с карточки товара
def scrape_product_data(product_id):
    url = f'https://www.chokore.com/collections/mens-accessories/products/{product_id}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим заголовок (title)
    title = soup.find('div', {'class': 'custom-title-wishlist'}).find('h1', recursive=False).text.strip()
    print('Title:', title)

    # Находим цену (price)
    price = soup.find('span', class_='product-price__price').text.strip()

    # Находим описание (description)
    description = soup.find('div', class_='product-single__description').text.strip()

    # Находим детали (details)
    details = soup.find('div', class_='product-single__details').text.strip()

    # Находим фото (photo) - берем первые три фото
    photo_elements = soup.find_all('img', class_='product-single__photo')
    photos = [photo['src'] for photo in photo_elements[:3]]

    # Находим категорию (category) и подкатегорию (sub category)
    breadcrumbs = soup.find_all('span', class_='breadcrumb__text')
    category = breadcrumbs[-2].text.strip()
    sub_category = breadcrumbs[-1].text.strip()

    return {
        'title': title,
        'price': price,
        'description': description,
        'details': details,
        'photos': photos,
        'category': category,
        'sub_category': sub_category,
        'url': url
    }

# Получаем случайный товарный ID
product_id = get_random_product_id()

# Извлекаем данные с карточки товара
product_data = scrape_product_data(product_id)

# Записываем данные в CSV файл
with open('product_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['title', 'price', 'description', 'details', 'photo1', 'photo2', 'photo3', 'category', 'sub_category', 'url']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({
        'title': product_data['title'],
        'price': product_data['price'],
        'description': product_data['description'],
        'details': product_data['details'],
        'photo1': product_data['photos'][0] if len(product_data['photos']) > 0 else '',
        'photo2': product_data['photos'][1] if len(product_data['photos']) > 1 else '',
        'photo3': product_data['photos'][2] if len(product_data['photos']) > 2 else '',
        'category': product_data['category'],
        'sub_category': product_data['sub_category'],
        'url': product_data['url']
    })

print("Данные успешно записаны в файл 'product_data.csv'")
