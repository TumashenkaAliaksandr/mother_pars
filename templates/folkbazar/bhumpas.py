import os
import requests
from bs4 import BeautifulSoup
import csv


directory = 'templates/../done_csv'
filename = 'bhumpas.csv'
FILEPARAMS = os.path.join(directory, filename)


def create_csv(filename, order):
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        csv.DictWriter(file, fieldnames=order).writeheader()


def write_data_csv(filename, data):
    with open(filename, 'a', encoding='utf-8', newline='') as file:
        csv.DictWriter(file, fieldnames=list(data)).writerow(data)


def get_data(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find('h1', {'class': 'product-single__title'}).text.strip()

    price_element = soup.find('span', {'class': 'product-single__price'})
    price = round(float(price_element.text.replace('Rs.', '').replace(',', '').strip()) * 1.1,
                  2) if price_element else 'N/A'

    desc_container = soup.find('div', {'class': 'product-single__description'})
    desc = desc_container.text.strip() if desc_container else ''

    category = 'Bhumpas'

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

    image_elements = soup.select('a.js-modal-open-product-modal.product__photo-wrapper-product-template')
    image_urls = ['http:' + img["href"] for img in image_elements]

    size_elements = soup.select('select.product-single__option[name="size"] option')
    variations = [{'variation': option.get('value'), 'price': option.get('data-price')}
                  for option in size_elements if option.get('value')]

    print(title, price, formatted_text, ', '.join(image_urls), category, variations)

    data = {'title': title, 'price': price, 'description': formatted_text, 'image_urls': ', '.join(image_urls),
            'category': category, 'variations': ', '.join([f"{v['variation']}: {v['price']}" for v in variations])}
    write_data_csv(FILEPARAMS, data)


def main():
    order = ['title', 'price', 'description', 'image_urls', 'category', 'variations']
    create_csv(FILEPARAMS, order)
    with open('templates/../urls_csv/urls_folkbazar_bhumpas.csv', 'r', encoding='utf-8') as file:
        for line in csv.DictReader(file):
            url = line['url']
            get_data(url)


if __name__ == '__main__':
    main()
