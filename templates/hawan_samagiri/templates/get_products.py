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
    title = soup.find('div', class_='product__title').find('h1').text.strip()
    print(title)
    sale_price_element = soup.find('span', class_='price-item--sale')
    sale_price_text = sale_price_element.text.strip()
    # Удалить "Rs." и лишние пробелы из текста цены
    sale_price = sale_price_text.replace('Rs.', '').strip()
    print("Цена со скидкой:", sale_price)

    # Находим контейнеры с описанием
    description_divs = soup.find_all('div', style=lambda style: style and 'text-align: left;' in style)
    description_container = soup.find('div', class_='product__description rte quick-add-hidden')

    formatted_description_div = ''
    formatted_description = ''

    # Обработка первого вида описания
    for div in description_divs:
        div_text = div.get_text(strip=True)
        formatted_description_div += div_text + '\n'

    # Обработка второго вида описания
    if description_container:
        description_paragraphs = description_container.find_all('p')
        for paragraph in description_paragraphs:
            paragraph_text = paragraph.get_text(strip=True)
            wrapped_text = textwrap.fill(paragraph_text, width=100, break_long_words=False)
            formatted_description += wrapped_text + '\n'

    # Если описание найдено, возвращаем его, иначе возвращаем пустую строку
    if formatted_description_div:
        description = formatted_description_div
    elif formatted_description:
        description = formatted_description
    else:
        description = ''

    # Получаем ссылки на изображения
    img_tags = soup.find_all('img')
    photos = [img['src'].split(' ')[0].replace('//', 'https://').split('?')[0] for img in img_tags]
    print("Ссылки на фотографии:")
    print(photos[:3])

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

# Чтение URL из файла CSV и получение информации о продукте для каждой ссылки
input_file = '../urls_csv/product_links.csv'
output_file = '../done_csv/camveda_product_info.csv'

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
    writer = csv.DictWriter(file, fieldnames=['Product ID', 'Title', 'Price', 'Description', 'Image URLs'])
    writer.writeheader()
    for info in product_info_list:
        writer.writerow(info)

print(f"Информация о продуктах была сохранена в файл '{output_file}'.")
