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

    # Находим название продукта в <h1> или в мета-теге
    title_element = soup.find('h1')
    if title_element:
        title = title_element.text.strip()
    else:
        title_meta = soup.find('meta', itemprop='name')
        title = title_meta['content'].strip() if title_meta else 'Title not found'

    print("Название продукта:", title)

    # Находим название продукта в <h1> или в мета-теге
    code_element = soup.find('product-name')
    if code_element:
        code = code_element.text.strip()
    else:
        code_meta = soup.find('meta', itemprop='sku')
        code = code_meta['content'].strip() if code_meta else 'Code not found'

    print("Code продукта:", code)

    # Ищем старую цену
    old_price_element = soup.find('div', class_='price-box')
    if old_price_element:
        old_price_span = old_price_element.find('span', class_='price')
        old_price = old_price_span.text.strip().replace('Rs.', '').strip() if old_price_span else 'N/A'
    else:
        old_price = 'N/A'

    print("Старая цена:", old_price)

    # Обработка описания
    def extract_description(soup):
        description_container = soup.find('div', class_='tab-content')
        formatted_description = ''

        if description_container:
            description_paragraphs = description_container.find_all('div')

            # Проверяем, есть ли параграфы
            if description_paragraphs:
                for paragraph in description_paragraphs:
                    paragraph_text = paragraph.get_text(strip=True)
                    # Форматируем текст для лучшего отображения
                    wrapped_text = textwrap.fill(paragraph_text, width=100, break_long_words=False)
                    formatted_description += wrapped_text + '\n\n'

        return formatted_description.strip() if formatted_description.strip() else 'No description available.'

    # Извлекаем описание
    description = extract_description(soup)
    print('Описание:', description)

    # Получаем ссылки на изображения из div с классом 'product-image'
    img_tags = soup.find_all('div', class_='image')
    photos = []

    for div in img_tags:
        img = div.find('img')  # Ищем img внутри каждого div
        if img and 'src' in img.attrs:
            src = img['src']
            clean_src = src.split('?')[0]  # Удаляем всё, что после знака вопроса
            photos.append(clean_src)

    # Форматируем ссылки в строку, разделённую запятыми
    photo_urls = ', '.join(photos[:1])
    print("Ссылки на фотографии:", photo_urls)

    # Генерируем рандомный ID
    product_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    print("Product ID:", product_id)

    category = 'MAN'
    print('Категория товара:', category)

    # Список идентификаторов контейнеров
    size_container_ids = [
        'product',
    ]

    # Инициализируем списки для хранения цветов и размеров
    colors = []
    sizes = []

    # Находим элемент <select> для цветов
    color_select = soup.find('select', id='select_13249')
    if color_select:
        color_options = color_select.find_all('option')
        for option in color_options:
            color_text = option.text.strip()
            if color_text and color_text != '-- Please Select --':
                colors.append(color_text)

    # Находим элемент <select> для размеров
    size_select = soup.find('select', id='select_13248')
    if size_select:
        size_options = size_select.find_all('option')
        for option in size_options:
            size_text = option.text.strip()
            if size_text and size_text != '-- Please Select --':
                sizes.append(size_text)

    # Выводим все доступные цвета и размеры
    print("Доступные цвета:", ', '.join(colors))
    print("Доступные размеры:", ', '.join(sizes))


    return {
        'Product ID': product_id,
        'Code Product': code,
        'Title': title,
        'Description': description,
        'Image URLs': ', '.join(photos[:3]),  # Ссылки на три фотографии в одной строке
        'Old Price': old_price,
        'Category': category,
        'Size': ', '.join(sizes),
    }

# Чтение URL из файла CSV и получение информации о продукте для каждой ссылки
input_file = '../urls_csv/test_product.csv'
output_file = '../done_csv/product_info.csv'


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
                            fieldnames=['Product ID', 'Code Product', 'Category', 'Title', 'Old Price', 'Sizes', 'Description',
                                        'Image URLs'])
    writer.writeheader()

    for info in product_info_list:
        writer.writerow(info)

print(f"Информация о продуктах была сохранена в файл '{output_file}'.")
