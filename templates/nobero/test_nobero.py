import os
import re
import requests
from bs4 import BeautifulSoup
import csv
import hashlib

directory = 'templates/../done_csv'
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


    data = {
        'title': title,
        'price': price,
        'description': formatted_text,
        'category': category,
        'image_urls': ', '.join(image_urls),
    }
    write_data_csv(FILEPARAMS, data)


def main():
    order = ['title', 'price', 'description', 'category', 'image_urls']
    create_csv(FILEPARAMS, order)
    with open('templates/../urls_csv/test_pick_printed_t_shirts.csv', 'r', encoding='utf-8') as file:
        for line in csv.DictReader(file):
            url = line['url']
            get_data(url)


if __name__ == '__main__':
    main()
