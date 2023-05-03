import requests
from bs4 import BeautifulSoup


def get_data(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find('h1', {'class': 'title'}).text.strip()
    price = soup.find('div', {'class': 'product-price'})
    cost = price.find('span').text.strip()
    desc = soup.find('div', {'class': 'composed-description'}).text.strip()

    photo_desc = []
    desc_photo = soup.find_all('div', {'class': 'me-3'})
    for dp in desc_photo:
        photo_desc.append(dp.find('img')['src'])

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

    img_container = soup.find('div', {'class': 'product-image'})
    img_src = img_container.find('img')['src']

    photo_desc_str = '\n'.join(photo_desc)

    return title, cost, formatted_text, img_src, photo_desc_str


def main():
    url = 'https://autosolar.es/kits-solares-conexion-red/kit-solar-autoconsumo-fotovoltaico-6000w-10950kwhano-ingeteam'
    title, cost, formatted_text, img_src, photo_desc = get_data(url)
    print(title, cost, formatted_text, img_src, photo_desc, sep='\n')


if __name__ == '__main__':
    main()



# import requests
# from bs4 import BeautifulSoup
# import csv
#
# URL = 'https://renaindia.com/collections'
# FILE_NAME = 'product_links.csv'
# DATA_FILE_NAME = 'products.csv'
#
#
# def create_csv(filename, order):
#     with open(filename, 'w', encoding='utf-8', newline='') as file:
#         csv.DictWriter(file, fieldnames=order).writeheader()
#
#
# def write_csv(filename, data):
#     with open(filename, 'a', encoding='utf-8', newline='') as file:
#         csv.DictWriter(file, fieldnames=list(data)).writerow(data)
#
#
# def get_product_links():
#     response = requests.get(URL)
#     soup = BeautifulSoup(response.content, 'html.parser')
#
#     product_links = []
#     for link in soup.find_all('a', {'class': 'product-link'}):
#         product_links.append('https://renaindia.com' + link['href'])
#
#     return product_links
#
#
# def get_product_data(link):
#     response = requests.get(link)
#     soup = BeautifulSoup(response.content, 'html.parser')
#
#     product_name = soup.find('h1', {'class': 'product-title'}).text.strip()
#     price = soup.find('div', {'class': 'price-ui'})
#     cost = price.find('span').text.replace('Rs.', '').strip()
#     new_cost = float(cost) * 1.1  # добавляем 10%
#     description = soup.find('div', {'class': 'product-description'}).text.strip()
#     data = {'name': product_name, 'price': cost, 'new_price': new_cost, 'description': description}
#     return data
#
#
# def main():
#     order = ['name', 'price', 'new_price', 'description']
#     create_csv(DATA_FILE_NAME, order)
#
#     product_links = get_product_links()
#     for link in product_links:
#         data = get_product_data(link)
#         write_csv(DATA_FILE_NAME, data)
#
#
# if __name__ == '__main__':
#     main()
