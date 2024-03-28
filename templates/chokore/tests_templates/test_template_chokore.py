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
    price_element = soup.find('s', {'class': 'product-single__sale-price'}).find('span', recursive=False).text.strip()
    if price_element:
        price = price_element.strip().replace('₹', '')
    else:
        price = 'Out of stock'
    print('Price:', price)

    # Находим описание (description)
    description = soup.find('div', class_='so-tab-content cust-tab4-content').text.strip()
    print('Description:', description)

    # Находим детали (details)
    details = soup.find('div', class_='so-tab-content cust_tab2_conTent').text.strip()
    print('Datails:', details)

    # Находим все изображения
    image_wrappers = soup.find_all('div', class_='responsive-image__wrapper')

    # Создаем список для хранения ссылок на изображения
    images = []

    # Проходим по каждому блоку с изображением
    for image_wrapper in image_wrappers:
        # Получаем ссылку на изображение
        image_src = image_wrapper.img['src'].lstrip('//')
        # Получаем размеры изображения
        image_sizes = image_wrapper.img['data-widths']
        # Разбиваем строку размеров и преобразуем в список чисел
        image_sizes = [int(size.strip()) for size in image_sizes[1:-1].split(',')]
        # Находим максимальный размер
        max_size = max(image_sizes)
        # Добавляем ссылку и максимальный размер в список
        images.append((image_src, max_size))

    # Сортируем список изображений по размеру в обратном порядке
    images.sort(key=lambda x: x[1], reverse=True)

    # Выбираем три изображения с наибольшим размером
    top_three_images = images[:3]

    # Выводим результат
    for index, (image_src, image_size) in enumerate(top_three_images, 1):
        print(f"Изображение {index}:")
        print(f"Ссылка: {image_src}")
        print(f"Размер: {image_size}")

    # Находим фото (photo) - берем первые три фото
    photo_elements = soup.find_all('img', class_='product-single__photo')
    photos = [photo['src'] for photo in photo_elements[:3]]

    # Находим категорию (category) и подкатегорию (sub category)
    breadcrumbs = soup.find('span', class_='breadcrumbs__link').text.strip()
    print('Breadcrumb:', breadcrumbs)
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
