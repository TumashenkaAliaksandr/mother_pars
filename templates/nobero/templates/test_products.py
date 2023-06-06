import os
import re
import requests
from bs4 import BeautifulSoup
import csv
import hashlib

directory = 'templates/../../done_csv'
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

    title_element = soup.find('h1', {'class': 'md'})
    title = title_element.text.strip() if title_element and title_element.text.strip() != 'Default Title' else ''
    print(title)

    desc_container = soup.find('div', {'class': 'product-single__description'})
    desc = desc_container.text.strip() if desc_container else ''

    category = 'T-shirts'

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

    image_elements = soup.select('div.product__photo-wrapper-product-template a.js-modal-open-product-modal')
    image_urls = ['https:' + img["href"] for img in image_elements]

    variation_elements = soup.select('select#ProductSelect-product-template option')
    variation_titles = soup.select('div.selector-wrapper.js.product-form__item')

    for i, variation_element in enumerate(variation_elements):
        variation_title = ''
        if i < len(variation_titles):
            variation_title_element = variation_titles[i].find('label')
            if variation_title_element:
                variation_title = variation_title_element.text.strip()

        variation_name = re.sub(r'Rs[.,0-9\s]*|[^a-zA-Z0-9\s]', '', variation_element.text.strip())
        variation_value = variation_element['value']
        variation_price = variation_element.text.replace('Rs.', '').strip()

        # Generate a unique hash for the identifier
        identifier = hashlib.sha256(url.encode('utf-8')).hexdigest()

        data = {
            'identifier': identifier,
            'title': title,
            'price': variation_price,
            'description': formatted_text,
            'category': category,
            'image_urls': ', '.join(image_urls),
            'variation_titles': variation_title,
            'name_variations': variation_name,
            'variations_price': variation_price,
            'id': variation_value
        }

        # Исключаем товары с пометкой "Sold Out" или содержащие "incense" и "Default Title"
        if "Sold Out" not in variation_name and "incense" and "Default Title" not in variation_name:
            write_data_csv(FILEPARAMS, data)


def main():
    order = ['identifier', 'title', 'price', 'description', 'category', 'image_urls', 'variation_titles', 'name_variations',
             'variations_price', 'id']
    create_csv(FILEPARAMS, order)
    with open('templates/../../urls_csv/test_pick_printed_t_shirts.csv', 'r', encoding='utf-8') as file:
        for line in csv.DictReader(file):
            url = line['url']
            get_data(url)


if __name__ == '__main__':
    main()
