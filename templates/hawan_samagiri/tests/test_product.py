import requests
from bs4 import BeautifulSoup
import csv
import random
import string

# Функция для получения информации о продукте по его URL
def get_product_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Находим информацию о продукте
    title = soup.find('div', class_='product__title').find('h1').text.strip()
    print(title)
    sale_price_element = soup.find('span', class_='price-item--sale')
    sale_price_text = sale_price_element.text.strip()
    # Удалить "Rs." и лишние пробелы из текста цены
    sale_price = sale_price_text.replace('Rs.', '').strip()
    print("Цена со скидкой:", sale_price)
    # Найти все теги <p>, содержащие описание
    description_tags = soup.find_all('p', {"data-mce-fragment": "1"})

    # Извлечь текст из найденных тегов
    description = '\n'.join(tag.get_text(strip=True) for tag in description_tags)
    print("Описание:")
    print(description)
    # Найти все теги <img>
    img_tags = soup.find_all('img')

    # Получить src-атрибуты изображений, добавить https: и убрать квадратные скобки
    photos = [img['src'].split(' ')[0].replace('//', 'https://').split('?')[0] for img in img_tags]
    print("Ссылки на фотографии:")
    print(photos[:3])  # Печать ссылок на три фотографии

    # Генерируем рандомный ID
    product_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    print("Product ID:", product_id)

    return {
        'Product ID': product_id,
        'Title': title,
        'Description': description,
        'Image URLs': ', '.join(photos[:3]),  # Ссылки на три фотографии в одной строке
        'Price': sale_price,
    }

# Ссылка на продукт
product_url = 'https://www.camveda.com/products/camveda-bhimseni-kapoor-500gm-jar'

# Получаем информацию о продукте
product_info = get_product_info(product_url)

# Записываем информацию о продукте в файл CSV
with open('product_info.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Product ID', 'Title', 'Price', 'Description', 'Image URLs'])
    writer.writeheader()
    writer.writerow(product_info)

print("Информация о продукте была сохранена в файл 'product_info.csv'.")
