import requests
from bs4 import BeautifulSoup
import csv
import random
import string
import textwrap


# Функция для получения информации о продукте по его URL
def get_product_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Находим информацию о продукте
    title = soup.find('h1', class_='product-title').text.strip()
    print("Название продукта:", title)

    sale_price_element = soup.find('li', class_='price-old')
    sale_price = sale_price_element.text.strip() if sale_price_element else 'N/A'
    print("Цена без скидки:", sale_price)

    # Находим контейнеры с описанием
    description_container = soup.find('div', class_='tab-content')

    formatted_description = ''

    # Обработка описания
    if description_container:
        description_paragraphs = description_container.find_all('div')
        for paragraph in description_paragraphs:
            paragraph_text = paragraph.get_text(strip=True)
            wrapped_text = textwrap.fill(paragraph_text, width=100, break_long_words=False)
            formatted_description += wrapped_text + '\n'

    # Если описание найдено, возвращаем его, иначе возвращаем пустую строку
    description = formatted_description if formatted_description else 'No description available.'
    print('Описание:', description)

    # Получаем ссылки на изображения из div с классом 'product-image'
    img_tags = soup.find_all('div', class_='product-image')
    photos = []

    for div in img_tags:
        img = div.find('img')  # Ищем img внутри каждого div
        if img and 'src' in img.attrs:
            src = img['src']
            clean_src = src.split('?')[0]  # Удаляем всё, что после знака вопроса
            photos.append(clean_src)

    # Форматируем ссылки в строку, разделённую запятыми
    photo_urls = ', '.join(photos[:3])
    print("Ссылки на фотографии:", photo_urls)

    # Генерируем рандомный ID
    product_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    print("Product ID:", product_id)

    brand = 'GAS'
    category = 'MAN'
    print('Брэнд:', brand)
    print('Категория товара:', category)

    return {
        'Product ID': product_id,
        'Title': title,
        'Description': description,
        'Image URLs': ', '.join(photos[:3]),  # Ссылки на три фотографии в одной строке
        'Price': sale_price,
        'Brand': brand,
        'Category': category,
    }


# Чтение URL из файла CSV и получение информации о продукте для каждой ссылки
input_file = '../urls_csv/gas_product_links.csv'
output_file = '../done_csv/gas_product_info.csv'

with open(input_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Пропускаем заголовки, если они есть
    product_info_list = []
    for row in reader:
        if not row:  # Проверяем, есть ли еще строки для чтения
            break  # Прерываем цикл, если строки закончились
        url = row[0]
        product_info = get_product_info(url)
        product_info_list.append(product_info)

# Записываем информацию о продукте в файл CSV
with open(output_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Product ID', 'Brand', 'Category', 'Title', 'Price', 'Description', 'Image URLs'])
    writer.writeheader()
    for info in product_info_list:
        writer.writerow(info)

print(f"Информация о продуктах была сохранена в файл '{output_file}'.")
