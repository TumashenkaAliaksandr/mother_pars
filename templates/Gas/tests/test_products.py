import requests
from bs4 import BeautifulSoup
import csv
import random
import string
import textwrap
import re


# Функция для форматирования описания
def format_description(description):
    # Подстановка заголовков для соответствующих частей описания
    description = description.replace('Specifications :', '\n**Specifications:**\n')
    description = description.replace(
        'Machine wash cold, Dry clean, Medium iron, Do not bleach, Do not wring, Do not tumble dry',
        '\n**Product Care:**\nMachine wash cold, Dry clean, Medium iron, Do not bleach, Do not wring, Do not tumble dry'
    )
    description = description.replace('Manufacturer Name:', '\n**Manufacturer:**\n')
    description = description.replace('Marketer Name:', '\n**Marketer:**\n')
    description = description.replace('Net Quantity:', '\n**Net Quantity:**\n')
    description = description.replace('Package Dimension:', '\n**Package Dimension:**\n')
    description = description.replace('Product Weight:', '\n**Product Weight:**\n')
    description = description.replace('Customer Care Information:', '\n**Customer Care Information:**\n')
    description = description.replace('MRP:', '\n**MRP:**\n')

    return description

# Функция для извлечения подкатегории из строки описания
def extract_subcategory(description):
    # Поиск строки, начинающейся с 'Name of the Commodity:'
    match = re.search(r'Name of the Commodity:\s*([^<]+)', description)
    if match:
        # Возвращаем только текст до первого тега <br> или окончания строки
        subcategory = match.group(1).strip()
        # Обрезаем текст до первого <br> если он есть
        subcategory = re.split(r'<br\s*/?>', subcategory, 1)[0].strip()
        # Удаляем все данные, которые следуют за основной подкатегорией
        subcategory = re.split(r'\*\*Package Dimension:', subcategory, 1)[0].strip()
        return subcategory
    return 'Unknown'


# Функция для получения информации о продукте по его URL
def get_product_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Находим название продукта
    title_element = soup.find('h1', class_='product-title')
    title = title_element.text.strip() if title_element else 'Title not found'
    print("Название продукта:", title)

    # Ищем элемент <li> с классом 'price-old' или внутри 'price-container'
    sale_price_element = soup.find('li', class_='price-old')

    # Если элемент с классом 'price-old' не найден, ищем внутри 'price-container'
    if not sale_price_element:
        price_container = soup.find('ul', class_='price-container')
        if price_container:
            sale_price_element = price_container.find('li')

    # Если нашли нужный элемент, ищем <span> или <h2> внутри него и удаляем знак рупии
    if sale_price_element:
        span_or_h2_element = sale_price_element.find(['span', 'h2'])
        sale_price = span_or_h2_element.text.strip().replace('₹', '').strip() if span_or_h2_element else 'N/A'
    else:
        sale_price = 'N/A'

    print("Цена без скидки:", sale_price)

    # Находим контейнеры с описанием
    description_container = soup.find('div', class_='tab-content')

    formatted_description = ''
    if description_container:
        description_paragraphs = description_container.find_all('div')
        for paragraph in description_paragraphs:
            paragraph_text = paragraph.get_text(strip=True)
            # Форматируем текст для лучшего отображения
            wrapped_text = textwrap.fill(paragraph_text, width=100, break_long_words=False)
            formatted_description += wrapped_text + '\n\n'

    # Применяем форматирование к описанию
    formatted_description = format_description(
        formatted_description) if formatted_description else 'No description available.'

    # Печатаем отформатированное описание для отладки
    print('Отформатированное описание:', formatted_description)

    # Извлекаем подкатегорию из форматированного описания
    subcategory = extract_subcategory(formatted_description)
    print("Подкатегория:", subcategory)

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

    # Список идентификаторов контейнеров
    size_container_ids = [
        'product',
    ]

    # Инициализируем список для хранения всех доступных размеров
    sizes = []

    # Проходим по каждому идентификатору контейнера
    for container_id in size_container_ids:
        size_container = soup.find('div', id=container_id)

        if size_container:
            # Ищем все лейблы, связанные с радиокнопками
            available_sizes = size_container.find_all('div', class_='radio radio-type-button2')

            if available_sizes:
                for size in available_sizes:
                    label = size.find('label')
                    if label:
                        size_text = label.get_text(strip=True)
                        # Добавляем размер в список только если его там нет
                        if size_text not in sizes:
                            sizes.append(size_text)
            else:
                print("Размеры не найдены в контейнере:", container_id)
        else:
            print("Контейнер размеров не найден:", container_id)

    # Выводим все доступные размеры
    sizes_output = ', '.join(sizes) if sizes else 'No sizes available'
    print("Доступные размеры:", sizes_output)

    return {
        'Product ID': product_id,
        'Title': title,
        'Description': formatted_description,
        'Image URLs': ', '.join(photos[:3]),  # Ссылки на три фотографии в одной строке
        'Price': sale_price,
        'Brand': brand,
        'Category': category,
        'Subcategory': subcategory,  # Добавляем подкатегорию
        'Size': sizes_output,
    }


# Чтение URL из файла CSV и получение информации о продукте для каждой ссылки
input_file = '../urls_csv/gas_pr_links.csv'
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
    writer = csv.DictWriter(file,
                            fieldnames=['Product ID', 'Brand', 'Category', 'Subcategory', 'Title', 'Price', 'Size',
                                        'Description',
                                        'Image URLs'])
    writer.writeheader()
    for info in product_info_list:
        writer.writerow(info)

print(f"Информация о продуктах была сохранена в файл '{output_file}'.")
