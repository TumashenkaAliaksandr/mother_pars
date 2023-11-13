# import os
# import re
# import textwrap
#
# import requests
# from bs4 import BeautifulSoup
# import csv
# import hashlib
#
# directory = 'templates/../../done_csv'
# filename = 'cargo_pants.csv'
# FILEPARAMS = os.path.join(directory, filename)
#
# def create_csv(filename, order):
#     with open(filename, 'w', encoding='utf-8', newline='') as file:
#         csv.writer(file).writerow(order)
#
# def write_data_csv(filename, data):
#     with open(filename, 'a', encoding='utf-8', newline='') as file:
#         csv.DictWriter(file, fieldnames=list(data)).writerow(data)
#
# def get_data(url):
#     html = requests.get(url).text
#     soup = BeautifulSoup(html, 'html.parser')
#
#     title = soup.find("h1", class_="t4s-product__title").text.strip()  # этот кусок кода для тайтла
#     print('Title: ', title)
#
#     category = "Cargo Pants"
#     sub_category = 'Men’s New Blazers / Trench Coats'
#     print('Category: ', category)
#
#     price = soup.find('div', class_="t4s-product-price").text.replace('Rs.', '').replace(',', '').replace('.00', '').strip()
#     print('Price: ', price)
#
#     # Находим элемент с классом "t4s-tab-wrapper"
#     tab_wrappers = soup.find_all("div", class_="t4s-tab-wrapper")
#
#     # Создаем словарь для хранения текста из каждой вкладки
#     tab_texts = {}
#
#     # Проходим по каждому элементу вкладки
#     for tab_wrapper in tab_wrappers:
#         # Находим заголовок вкладки
#         tab_title = tab_wrapper.find("span", class_="t4s-tab__text").text.strip()
#
#         # Находим текст вкладки
#         tab_content = tab_wrapper.find("div", class_="t4s-tab-content").text.strip()
#
#         # Добавляем заголовок и текст в словарь
#         tab_texts[tab_title] = tab_content
#
#     def format_description(description, max_line_length=100):
#         words = description.split()
#         lines = []
#         current_line = []
#
#         for word in words:
#             if len(' '.join(current_line + [word])) <= max_line_length:
#                 current_line.append(word)
#             else:
#                 lines.append(' '.join(current_line))
#                 current_line = [word]
#
#         if current_line:
#             lines.append(' '.join(current_line))
#
#         formatted_description = '\n'.join(lines)
#         return formatted_description
#
#     # Теперь у вас есть доступ к тексту из каждой вкладки по заголовку
#     core_features_text = (tab_texts.get("core features", "").replace(":", ":\n"))
#     description_text = tab_texts.get("description", "")
#     shipping_returns_text = tab_texts.get("shipping & returns", "")
#     care_guide_text = tab_texts.get("care guide", "")
#
#     # Выводим текст из каждой вкладки
#     print("Core Features:")
#     print(core_features_text)
#
#     print("Description:")
#     print(description_text)
#
#     print("Shipping & Returns:")
#     print(shipping_returns_text)
#
#     print("Care Guide:")
#     print(care_guide_text)
#
#     main_image_element = soup.find('img', class_='Image--lazyLoaded')
#
#     # Переменная для хранения найденного id
#     id = None
#
#     if main_image_element:
#         main_image_url = 'https:' + main_image_element['src']
#
#         match = re.search(r'v=(\d+)', main_image_url)
#         if match:
#             id = match.group(1)
#             print("ID:", id)
#     else:
#         print('Главное фото товара не найдено.')
#
#     # Находим <div> элемент с классом "Product__Slideshow"
#     slideshow_div = soup.find('div', class_='Product__Slideshow')
#
#     # Если найден <div> элемент с классом "Product__Slideshow"
#     if slideshow_div:
#         # Инициализируем переменную для хранения списка фото товара
#         image_urls = []
#
#         # Находим все <img> элементы внутри слайдшоу
#         img_elements = slideshow_div.find_all('img')
#
#         # Итерируемся по каждому <img> элементу
#         for img_element in img_elements:
#             # Извлекаем значение атрибута src
#             src = 'https:' + img_element['src']
#
#             # Проверяем, что значение атрибута src не содержит "data:image"
#             if 'data:image' not in src:
#                 # Добавляем значение атрибута src в список фото товара
#                 image_urls.append(src)
#                 print('Фото:', src)
#
#     else:
#         print('Слайдшоу товара не найдено.')
#
#     size_title = "Select Size"
#     print('size_title:', size_title)
#
#     label_elements = soup.find('div', class_='Popover__ValueList')
#     formatted_labels = [label.text.strip() for label in label_elements if label.text.strip()]
#     labels = '|'.join(formatted_labels)
#     print(labels)
#
#     # color_title = "Select Color"
#     # print('Title color: ', color_title)
#     #
#     # color_vars = soup.find_all('input', class_='color-select-input', attrs={'name': 'color'})
#     # values = [color_var.get('value') for color_var in color_vars if color_var.get('value')]
#     # values_str = '|'.join(values)
#     #
#     # print('Color:', values_str)
#
#
#     data = {
#         'title': title,
#         'price': price,
#         'story_description': core_features_text,
#         'category': category,
#         'sub_category': sub_category,
#         'image_urls': ', '.join(image_urls),  # Заменил переменную src на image_urls
#         'size_title': size_title,
#         'size': labels,
#         'description': description_text,
#         'id': id,
#     }
#     write_data_csv(FILEPARAMS, data)
#
#
# def main():
#     order = ['title', 'price', 'story_description', 'category', 'sub_category', 'image_urls', 'size_title', 'size', 'description', 'id']
#     create_csv(FILEPARAMS, order)
#     with open('templates/../../urls_csv/urls_urban_monkey.csv', 'r', encoding='utf-8') as file:
#         for line in csv.DictReader(file):
#             url = line['url']
#             get_data(url)
#
#
# if __name__ == '__main__':
#     main()

import os
import requests
from bs4 import BeautifulSoup
import csv
import re
import json


def format_description(description, max_line_length=100):
    words = description.split()
    lines = []
    current_line = []

    for word in words:
        if len(' '.join(current_line + [word])) <= max_line_length:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]

    if current_line:
        lines.append(' '.join(current_line))

    formatted_description = '\n'.join(lines)
    return formatted_description


def create_csv(filename, order):
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        csv.writer(file).writerow(order)


def write_data_csv(filename, data):
    with open(filename, 'a', encoding='utf-8', newline='') as file:
        csv.DictWriter(file, fieldnames=list(data)).writerow(data)


def extract_id_from_script(html):
    script_text = re.search(r'<script type="application/json" class="pr_variants_json">(.*?)</script>', html, re.DOTALL)

    if script_text:
        script_content = script_text.group(1)
        script_data = json.loads(script_content)

        ids = [variant['id'] for variant in script_data]
        return ids
    else:
        return None


def extract_image_src(html):
    soup = BeautifulSoup(html, 'html.parser')
    img_elements = soup.find_all("div", class_="t4s-product__media")

    image_src_list = []

    for img_element in img_elements:
        img = img_element.find("img")
        if img and "src" in img.attrs:
            image_src = img["src"]
            # Удаляем первые два символа "//" перед "www" и часть "?v=1697874194&width=720"
            fixed_url = image_src[2:].split('?v=')[0]
            image_src_list.append(fixed_url)

    return image_src_list


def write_image_src_to_file(image_src_list, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for src in image_src_list:
            file.write(src + '\n')


def get_data(url, filename):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find("h1", class_="t4s-product__title").text.strip()
    print('Title:', title)

    category = "Cargo Pants"
    sub_category = 'Men’s New Blazers / Trench Coats'
    print('Category:', category)

    price = soup.find('div', class_="t4s-product-price").text.replace('Rs.', '').replace(',', '').replace('.00',
                                                                                                          '').strip()
    print('Price:', price)

    tab_wrappers = soup.find_all("div", class_="t4s-tab-wrapper")
    tab_texts = {}

    for tab_wrapper in tab_wrappers:
        tab_title = tab_wrapper.find("span", class_="t4s-tab__text").text.strip()
        tab_content = tab_wrapper.find("div", class_="t4s-tab-content").text.strip()
        tab_texts[tab_title] = tab_content

    core_features_text = tab_texts.get("core features", "").replace(":", ":\n")
    description_text = tab_texts.get("description", "")
    shipping_returns_text = tab_texts.get("shipping & returns", "")
    care_guide_text = tab_texts.get("care guide", "")

    formatted_description = format_description(description_text)

    print("Core Features:")
    print(core_features_text)

    print("Description:")
    print(formatted_description)

    print("Shipping & Returns:")
    print(shipping_returns_text)

    print("Care Guide:")
    print(care_guide_text)

    ids = extract_id_from_script(html)
    if ids:
        print("IDs:")
        for variant_id in ids:
            print(variant_id)

    image_src_list = extract_image_src(html)
    if image_src_list:
        print("Image Sources:")
        for src in image_src_list:
            print(src)

        write_image_src_to_file(image_src_list, "image_src.txt")

    data = {
        "Title": title,
        "Category": category,
        "Price": price,
        "Core Features": core_features_text,
        "Description": formatted_description,
        "Shipping & Returns": shipping_returns_text,
        "Care Guide": care_guide_text,
        "Photo Url": src,
    }
    write_data_csv(filename, data)


def process_urls_csv(input_csv, output_csv):
    create_csv(output_csv,
               ["Title", "Category", "Price", "Core Features", "Description", "Shipping & Returns", "Care Guide", "Photo Url"])

    with open(input_csv, 'r', encoding='utf-8') as file:
        for line in csv.DictReader(file):
            url = line['url']
            get_data(url, output_csv)


if __name__ == "__main__":
    input_csv = 'templates/../../urls_csv/urls_urban_monkey.csv'
    output_csv = 'cargo_pants.csv'

    process_urls_csv(input_csv, output_csv)

