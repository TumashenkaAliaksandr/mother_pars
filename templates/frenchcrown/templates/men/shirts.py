import os
import re
import requests
from bs4 import BeautifulSoup
import csv
import hashlib

directory = 'templates/../../../done_csv'
filename = 'urls_shirts.csv'
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

    category = "Men’s Shirts"
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


    main_image_element = soup.find('img', class_='Image--lazyLoaded')
    image_urls = set()

    if main_image_element:
        main_image_url = 'https:' + main_image_element['src']
        image_url = main_image_url
        image_urls.add(image_url)
        print('Главное фото товара:', main_image_url)
    else:
        print('Главное фото товара не найдено.')

    if image_urls:
        match = re.search(r'v=(\d+)', list(image_urls)[0])
        if match:
            id = match.group(1)
            print("ID:", id)


    # Находим <div> элемент с классом "Product__Slideshow"
    slideshow_div = soup.find('div', class_='Product__Slideshow')

    # Если найден <div> элемент с классом "Product__Slideshow"
    if slideshow_div:
        # Находим все <div> элементы с классом "Product__SlideItem" внутри слайдшоу
        slide_items = slideshow_div.find_all('div', class_='Product__SlideItem')

        # Итерируемся по каждому <div> элементу
        for slide_item in slide_items:
            # Находим все <img> элементы внутри текущего <div> элемента
            img_elements = slide_item.find_all('img')

            # Итерируемся по каждому <img> элементу
            for img_element in img_elements:
                # Извлекаем значение атрибута src
                src = 'https:' + img_element['src']

                # Проверяем, что значение атрибута src не содержит "data:image"
                if 'data:image' not in src:
                    # Выводим значение атрибута src
                    print('Фото товара:', src)
    else:
        print('Слайдшоу товара не найдено.')

    size_title = "Select Size"
    print('size_title:', size_title)

    label_elements = soup.find('div', class_='Popover__ValueList')
    formatted_labels = [label.text.strip() for label in label_elements if label.text.strip()]
    labels = '|'.join(formatted_labels)
    print(labels)


    color_title = "Select Color"
    print('Title color: ', color_title)

    color_vars = soup.find_all('input', class_='color-select-input', attrs={'name': 'color'})
    values = [color_var.get('value') for color_var in color_vars if color_var.get('value')]
    values_str = '|'.join(values)

    print('Color:', values_str)

    # Previous code...

    data = {
        'title': title,
        'price': price,
        'description': formatted_text,
        'category': category,
        'image_urls': src,
        'size_title': size_title,
        'size': labels,
        'color_title': color_title,
        'color_value': values_str,
        'id': id,
    }
    write_data_csv(FILEPARAMS, data)

def main():
    order = ['title', 'price', 'description', 'category', 'image_urls', 'size_title', 'size', 'color_title', 'color_value', 'id']
    create_csv(FILEPARAMS, order)
    with open('templates/../../../urls_csv/urls_shirts.csv', 'r', encoding='utf-8') as file:
        for line in csv.DictReader(file):
            url = line['url']
            get_data(url)


if __name__ == '__main__':
    main()
