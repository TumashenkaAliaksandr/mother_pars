import os
import textwrap
import requests
from bs4 import BeautifulSoup
import csv
import random

directory = '../done_csv'
filename = 'honeyhut_products.csv'
FILEPARAMS = os.path.join(directory, filename)


def create_csv(filename, order):
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        csv.DictWriter(file, fieldnames=order).writeheader()


def write_data_csv(filename, data):
    with open(filename, 'a', encoding='utf-8', newline='') as file:
        csv.DictWriter(file, fieldnames=list(data)).writerow(data)


def get_product_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    brand = 'Honey Hut'

    title_element = soup.find('div', {'class': 'product__title'}).find('h1', recursive=False)
    if title_element:
        title = title_element.text.strip()[:35]
    else:
        title = "Title not found"

    price_element = soup.find('span', {'class': 'price-item price-item--sale price-item--last'})
    if price_element:
        price = price_element.text.strip().replace('Rs. ', '').split('.')[0]
    else:
        price = "Price not found"

    mass_element = soup.find('p', {'class': 'priceweight mediumfont'})
    if mass_element:
        mass = mass_element.text.strip()
    else:
        mass = "Mass not found"

    # Получаем описание товара из контейнера
    description_container = soup.find('div', {'class': 'product__description'})
    description = description_container.text.strip() if description_container else ''

    # Разбиваем описание на строки не более 100 символов
    wrapped_description = textwrap.fill(description, width=100)

    photo = soup.find('div', {'class': 'product__media media media--transparent gradient global-media-settings'}).find('img')['src'].strip().replace('//', '')

    product_id = ''.join(random.choices('0123456789', k=8))

    base_url = 'https://www.honeyhut.in'
    urls = soup.find_all('div', class_='product__title')
    url_list = ', '.join([base_url + url.find('a').get('href') for url in urls])
    print(url_list)

    return {'Brand': brand, 'Title': title, 'Price': price, 'Mass': mass, 'Description': description, 'Photo': photo, 'ID': product_id, 'url_product': url_list}

def main():
    order = ['Brand', 'Title', 'Price', 'Description', 'Photo', 'ID', 'Url_Product']
    create_csv(FILEPARAMS, order)
    urls_filename = '../urls_csv/honeyhut_urls.csv'
    with open(urls_filename, 'r', encoding='utf-8') as urls_file:
        urls = [line.strip() for line in urls_file]
    for url in urls:
        product_data = get_product_data(url)
        if product_data:
            write_data_csv(FILEPARAMS, product_data)
            print(f"Data extracted and written for product: {product_data['Title']}")
        else:
            print(f"Failed to retrieve product data for URL: {url}")


if __name__ == '__main__':
    main()

