# import os
# import requests
# from bs4 import BeautifulSoup
# import csv
# import random
#
# directory = '../done_csv'
# filename = 'honeyhut_products.csv'
# FILEPARAMS = os.path.join(directory, filename)
#
#
# def create_csv(filename, order):
#     with open(filename, 'w', encoding='utf-8', newline='') as file:
#         csv.DictWriter(file, fieldnames=order).writeheader()
#
#
# def write_data_csv(filename, data):
#     with open(filename, 'a', encoding='utf-8', newline='') as file:
#         csv.DictWriter(file, fieldnames=list(data)).writerow(data)
#
#
# def get_product_data(url):
#     html = requests.get(url).text
#     soup = BeautifulSoup(html, 'html.parser')
#
#     title = soup.find('h1', {'class': 'product__info-wrapper grid__iteme'}).text.strip()
#     price = soup.find('div', {'class': 'price__sale'}).text.strip()
#     print(title)
#
#     description_container = soup.find('div', {'class': 'product__description'})
#     description = description_container.text.strip() if description_container else ''
#
#     photo = soup.find('div', {'class': 'product__photo'}).find('img')['src']
#
#     product_id = ''.join(random.choices('0123456789', k=8))
#
#     return {'Title': title, 'Price': price, 'Description': description, 'Photo': photo, 'ID': product_id}
#
#
# def main():
#     order = ['Title', 'Price', 'Description', 'Photo', 'ID']
#     create_csv(FILEPARAMS, order)
#     urls = [
#         'https://www.honeyhut.in/products/acacia-honey',
#         'https://www.honeyhut.in/products/lavender-honey',
#         'https://www.honeyhut.in/products/wildflower-honey'
#     ]
#     for url in urls:
#         product_data = get_product_data(url)
#         if product_data:
#             write_data_csv(FILEPARAMS, product_data)
#             print(f"Data extracted and written for product: {product_data['Title']}")
#         else:
#             print(f"Failed to retrieve product data for URL: {url}")
#
#
# if __name__ == '__main__':
#     main()
import requests
from bs4 import BeautifulSoup

url = 'https://www.honeyhut.in/products/acacia-honey'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

regular_price = soup.find('s', class_='price-item--regular').text.strip()
sale_price = soup.find('span', class_='price-item--sale').text.strip()

print("Regular price:", regular_price)
print("Sale price:", sale_price)
