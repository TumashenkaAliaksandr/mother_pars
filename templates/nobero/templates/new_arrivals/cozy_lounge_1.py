import os
import re
import requests
from bs4 import BeautifulSoup
import csv
import hashlib

directory = 'templates/../../../done_csv'
filename = 'cozy_lounge_1.csv'
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

    category = "Luxury Summer Sets"
    print('Category: ', category)

    title_element = soup.find('h1', {'class': 'capitalize'})
    title = title_element.text.strip() if title_element and title_element.text.strip() != 'Default Title' else ''
    print('Title: ', title)
    price_element = soup.find('h2', {'id': 'variant-price'})
    price = price_element.text.replace('₹', '').strip()
    print('Price: ', price)

    desc_container = soup.find('details', {'class': 'filter-group'})
    desc = desc_container.text.strip() if desc_container else ''
    print('Description:', '\n', desc)

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

    image_elements = soup.select('img.image-placeholder-bg')
    image_urls = set()  # Set to store unique image URLs
    for img in image_elements:
        image_url = 'https:' + img['src']
        image_width = int(img['width']) if 'width' in img.attrs else 0
        if image_width != 75:  # Exclude images with width=75
            image_urls.add(image_url)
    print('Images:', image_urls)

    match = re.search(r'v=(\d+)', list(image_urls)[0])
    if match:
        id = match.group(1)
        print("ID:", id)

    size_title = "Select Size"
    print('size_title:', size_title)

    label_elements = soup.select('label[for^="size-"]')
    formatted_labels = [label.text.strip() for label in label_elements if label.text.strip()]
    labels = '|'.join(formatted_labels)


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
        'image_urls': ', '.join(image_urls),
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
    with open('templates/../../../urls_csv/cozy_lounge_1.csv', 'r', encoding='utf-8') as file:
        for line in csv.DictReader(file):
            url = line['url']
            get_data(url)


if __name__ == '__main__':
    main()
