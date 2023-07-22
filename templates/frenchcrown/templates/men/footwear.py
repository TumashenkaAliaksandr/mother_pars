import os
import re
import textwrap

import requests
from bs4 import BeautifulSoup
import csv
import hashlib

directory = 'templates/../../../done_csv'
filename = 'footwear.csv'
FILEPARAMS = os.path.join(directory, filename)

def create_csv(filename, order):
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        csv.writer(file).writerow(order)

def write_data_csv(filename, data):
    with open(filename, 'a', encoding='utf-8', newline='') as file:
        csv.DictWriter(file, fieldnames=list(data)).writerow(data)

def get_data(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find("h1", class_="ProductMeta__Title").text.strip()  # этот кусок кода для тайтла
    print('Title: ', title)

    brand = 'Frenchcrown'

    category = "Men’s"
    sub_category = 'Men’s Footwear'
    print('Category: ', category)

    price = soup.find('span', class_="ProductMeta__Price").text.replace('₹', '').strip()
    print('Price: ', price)

    desc_container = soup.find('div', {'class': 'Collapsible Collapsible--large'})
    desc = desc_container.text.strip() if desc_container else ''

    lines = []
    current_line = ''
    for word in desc.split():
        if len(current_line + ' ' + word) > 100:
            lines.append(current_line)
            current_line = word
        else:
            current_line += ' ' + word
    if current_line:
        lines.append(current_line)
    formatted_text = '\n'.join(lines)
    print('Description:', '\n', formatted_text)

    desc_two = ""
    # Извлекаем текст из <div class="Rte">
    rte_div = soup.find('div', class_='Rte')
    if rte_div:
        rte_text = rte_div.get_text(strip=True)
        rte_text = textwrap.fill(rte_text, width=100)
        desc_two += rte_text

    # Извлекаем текст из <div class="product-extra-info">
    extra_info_div = soup.find('div', class_='product-extra-info')
    if extra_info_div:
        extra_info_items = extra_info_div.find_all('li')
        extra_info_text = '\n'.join([textwrap.fill(item.get_text(strip=True), width=100) for item in extra_info_items])
        desc_two += extra_info_text

    print(desc_two)

    main_image_element = soup.find('img', class_='Image--lazyLoaded')

    # Переменная для хранения найденного id
    id = None

    if main_image_element:
        main_image_url = 'https:' + main_image_element['src']

        match = re.search(r'v=(\d+)', main_image_url)
        if match:
            id = match.group(1)
            print("ID:", id)
    else:
        print('Главное фото товара не найдено.')

    # Находим <div> элемент с классом "Product__Slideshow"
    slideshow_div = soup.find('div', class_='Product__Slideshow')

    # Если найден <div> элемент с классом "Product__Slideshow"
    if slideshow_div:
        # Инициализируем переменную для хранения списка фото товара
        image_urls = []

        # Находим все <img> элементы внутри слайдшоу
        img_elements = slideshow_div.find_all('img')

        # Итерируемся по каждому <img> элементу
        for img_element in img_elements:
            # Извлекаем значение атрибута src
            src = 'https:' + img_element['src']

            # Проверяем, что значение атрибута src не содержит "data:image"
            if 'data:image' not in src:
                # Добавляем значение атрибута src в список фото товара
                image_urls.append(src)
                print('Фото:', src)

    else:
        print('Слайдшоу товара не найдено.')

    size_title = "Select Size"
    print('size_title:', size_title)

    label_elements = soup.find('div', class_='Popover__ValueList')
    formatted_labels = [label.text.strip() for label in label_elements if label.text.strip()]
    labels = '|'.join(formatted_labels)
    print(labels)

    # color_title = "Select Color"
    # print('Title color: ', color_title)
    #
    # color_vars = soup.find_all('input', class_='color-select-input', attrs={'name': 'color'})
    # values = [color_var.get('value') for color_var in color_vars if color_var.get('value')]
    # values_str = '|'.join(values)
    #
    # print('Color:', values_str)


    data = {
        'title': title,
        'price': price,
        'brand': brand,
        'story_description': formatted_text,
        'category': category,
        'sub_category': sub_category,
        'image_urls': ', '.join(image_urls),  # Заменил переменную src на image_urls
        'size_title': size_title,
        'size': labels,
        'description': desc_two,
        'id': id,
    }
    write_data_csv(FILEPARAMS, data)


def main():
    order = ['title', 'price', 'brand', 'story_description', 'category', 'sub_category', 'image_urls', 'size_title', 'size', 'description', 'id']
    create_csv(FILEPARAMS, order)
    with open('templates/../../../urls_csv/urls_footwear.csv', 'r', encoding='utf-8') as file:
        for line in csv.DictReader(file):
            url = line['url']
            get_data(url)


if __name__ == '__main__':
    main()
