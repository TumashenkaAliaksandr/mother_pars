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

    # Находим название продукта в <h1>
    title_element = soup.find('h1')
    title = title_element.text.strip() if title_element else 'Title not found'
    print("Название продукта:", title)

    # Извлечение описания
    description_container = soup.find('div', class_='productdetail__description')

    if description_container:
        description_paragraphs = description_container.find_all('p')
        formatted_description = '\n\n'.join(
            textwrap.fill(paragraph.get_text(strip=True), width=100, break_long_words=False)
            for paragraph in description_paragraphs
        )
        description = formatted_description.strip() if formatted_description.strip() else 'No description available.'
    else:
        description = 'No description available.'

    print('Описание:', description)

    # Находим блок с классом "spicesyoumaylike__imgBox"
    img_box = soup.find('div', class_='spicesyoumaylike__imgBox')

    # Переменная для хранения первой ссылки на изображение
    image_link = None

    if img_box:
        # Находим тег <picture> внутри блока
        picture_tag = img_box.find('picture')
        if picture_tag:
            # Извлекаем ссылки из <source>
            source_tags = picture_tag.find_all('source')
            for source in source_tags:
                if 'srcset' in source.attrs:
                    srcset = source['srcset']
                    # Извлекаем все URL из srcset и очищаем их
                    urls = [url.split(' ')[0] for url in srcset.split(',')]
                    # Очищаем ссылки, убирая .webp и пустые строки, а также заполнители
                    for url in urls:
                        cleaned_url = url.split('.webp')[0]
                        if cleaned_url and 'data:image/svg+xml' not in cleaned_url:
                            image_link = cleaned_url  # Сохраняем первую действительную ссылку
                            break  # Выходим из цикла после нахождения первой ссылки
                if image_link:  # Если ссылка найдена, выходим из внешнего цикла
                    break

            # Обработка тега <img>, если еще не найдено изображение
            if not image_link:
                img_tag = picture_tag.find('img')
                if img_tag and 'src' in img_tag.attrs:
                    img_src = img_tag['src']
                    image_link = img_src.split('.webp')[0]  # Убираем .webp

        if image_link:
            print(f"Найдена ссылка на изображение: {image_link}")
        else:
            print("Изображение не найдено.")
    else:
        print("Блок с изображениями не найден.")


    # Генерируем рандомный ID
    product_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    print("Product ID:", product_id)

    # Находим блок с классом "spicesyoumaylike__text"
    text_box = soup.find('section', class_='spicesyoumaylike')

    # Переменная для хранения категории
    category = None

    if text_box:
        # Находим элемент с классом "categoryTitle"
        category_element = text_box.find('div', class_='categoryTitle')
        if category_element:
            category = category_element.text.strip()  # Извлекаем текст категории

    if category:
        print(f"Категория: {category}")
    else:
        print("Категория не найдена.")


    # Извлечение информации о использовании
    usage_container = soup.find('div', class_='productdetail__usage')

    if usage_container:
        usage_name = usage_container.find_all('h4', class_='productdetail__h4')
        usage_paragraphs = usage_container.find_all('p', class_='showDiv')
        usage_texts = [paragraph.get_text(strip=True) for paragraph in usage_paragraphs]
        usage = '\n'.join(usage_texts) if usage_name and usage_texts else 'No usage information available.'
        print("Использование:", usage)
    else:
        usage = 'No usage information available.'

    brand = 'Everest'
    print('Brand:', brand)

        # Извлечение информации о packaging
    packaging_container = soup.find('div', class_='productdetail__weight')

    if packaging_container:
        usage_paragraphs = packaging_container.find_all('div', class_='item')
        packaging_texts = [paragraph.get_text(strip=True) for paragraph in usage_paragraphs]
        packaging = '\n'.join(packaging_texts) if packaging_texts else 'No usage information available.'
        print("Упаковка:", packaging)
    else:
        usage = 'No packaging information available.'


    return {
        'Product ID': product_id,
        'Brand': brand,
        'Title': title,
        'Description': description,
        'Usage': usage,
        'Packaging': packaging,
        'Image URLs': image_link,
        'Category': category,
    }


# Чтение URL из файла CSV и получение информации о продукте для каждой ссылки
input_file = '../urls_csv/product_links.csv'
output_file = '../done_csv/Everest_product_info.csv'


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
                            fieldnames=['Product ID', 'Brand', 'Category',
                                        'Title',
                                        'Description',
                                        'Usage',
                                        'Packaging',
                                        'Image URLs'])

    writer.writeheader()

    for info in product_info_list:
        writer.writerow(info)

print(f"Информация о продуктах была сохранена в файл '{output_file}'.")
