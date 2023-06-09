import os
import re
import requests
from bs4 import BeautifulSoup
import csv
import hashlib

directory = 'templates/../../../done_csv'
filename = 't_shirts.csv'
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

    category = 'T-shirts'
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
    image_urls = ['https:' + img["src"] for img in image_elements]
    best_image_url = image_urls[0] if image_urls else ''
    print('Image: ', best_image_url)

    size_title = "Select Size"
    print('size_title:', size_title)

    label_elements = soup.select('label[for^="size-"]')
    formatted_labels = [label.text.strip() for label in label_elements]
    labels = ' '.join(formatted_labels)

    color_title = "Select Color"
    print('Title color: ', color_title)

    id_prod = soup.select('input[form]')
    for form_element in id_prod:
        form_id = form_element['form']
        numeric_form_id = re.sub('[^0-9]', '', form_id)
        print('Id: ', numeric_form_id)

    div_element = soup.find('div', class_='capitalize pb-4 flex justify-between items-center')
    if div_element:
        select_color = div_element.text.strip().replace('Size', 'Color')
        print('Title color: ', select_color)

    color_vars = soup.find_all('input', class_='color-select-input', attrs={'name': 'color'})
    values = []
    for color_var in color_vars:
        value = color_var.get('value')
        values.append(value)
        values_str = ', '.join(values)

    print('Color:', values_str)

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
        'id': numeric_form_id,
    }
    write_data_csv(FILEPARAMS, data)


def main():
    order = ['title', 'price', 'description', 'category', 'image_urls', 'size_title', 'size', 'color_title', 'color_value', 'id']
    create_csv(FILEPARAMS, order)
    with open('templates/../../../urls_csv/pick_printed_t_shirts.csv', 'r', encoding='utf-8') as file:
        for line in csv.DictReader(file):
            url = line['url']
            get_data(url)


if __name__ == '__main__':
    main()
