# import requests
# from bs4 import BeautifulSoup
#
#
# def get_data(url):
#     html = requests.get(url).text
#     soup = BeautifulSoup(html, 'html.parser')
#
#     title = soup.find('h1', {'class': 'product_name'}).text.strip()
#     price = soup.find('div', {'class': 'price-ui'})
#     cost = price.find('span').text.replace('Rs.', '').strip()
#     desc = soup.find('div', {'class': 'description'}).text.strip()
#
#     lines = []
#     current_line = ''
#     for word in desc.split():
#         if len(current_line + ' ' + word) > 100:
#             lines.append(current_line)
#             current_line = word
#         else:
#             current_line += ' ' + word
#     if current_line:
#         lines.append(current_line)
#     formatted_text = '\n'.join(lines)
#
#     img_container = soup.find('div', {'class': 'image__container'})
#     img_src = "https:" + img_container.find('img')['data-src']
#
#     print(title, cost, formatted_text, img_src, sep='\n')
#
#
# def main():
#     url = 'https://renaindia.com/collections/kitchenware-all/products/3-in-1-compact-rotary-peeler'
#     get_data(url)
#
#
# if __name__ == '__main__':
#     main()


import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://renaindia.com/collections'
FILE_NAME = 'product_links.csv'
DATA_FILE_NAME = 'products.csv'


def create_csv(filename, order):
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        csv.DictWriter(file, fieldnames=order).writeheader()


def write_csv(filename, data):
    with open(filename, 'a', encoding='utf-8', newline='') as file:
        csv.DictWriter(file, fieldnames=list(data)).writerow(data)


def get_product_links():
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    product_links = []
    for link in soup.find_all('a', {'class': 'product-link'}):
        product_links.append('https://renaindia.com' + link['href'])

    return product_links


def get_product_data(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')

    product_name = soup.find('h1', {'class': 'product-title'}).text.strip()
    price = soup.find('div', {'class': 'price-ui'})
    cost = price.find('span').text.replace('Rs.', '').strip()
    new_cost = float(cost) * 1.1  # добавляем 10%
    description = soup.find('div', {'class': 'product-description'}).text.strip()
    data = {'name': product_name, 'price': cost, 'new_price': new_cost, 'description': description}
    return data


def main():
    order = ['name', 'price', 'new_price', 'description']
    create_csv(DATA_FILE_NAME, order)

    product_links = get_product_links()
    for link in product_links:
        data = get_product_data(link)
        write_csv(DATA_FILE_NAME, data)


if __name__ == '__main__':
    main()
