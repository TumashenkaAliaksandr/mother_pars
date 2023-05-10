import os
import requests
from bs4 import BeautifulSoup
import csv


directory = '../done_csv'
filename = 'cargador_coche_electrico.csv'
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

    title = soup.find('h1', {'class': 'title'}).text.strip()
    price = soup.find('div', {'class': 'product-price'})
    cost = price.find('span').text.strip()

    desc_container = soup.find('div', {'class': 'tab active'})
    desc = desc_container.text.strip() if desc_container else ''

    category = 'Cargador_coche_electrico'

    photo_desc = set()
    desc_photo = soup.find_all('div', {'class': 'me-3'})
    for dp in desc_photo:
        photo_desc.add(dp.find('img')['src'])

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

    print(title, cost, formatted_text, img_src, category, photo_desc_str)

    data = {'title': title, 'cost': cost, 'description': formatted_text,
            'img_src': img_src, 'photo_desc_str': photo_desc_str, 'category': category}
    write_data_csv(FILEPARAMS, data)


def main():
    order = ['title', 'cost', 'description',  'img_src', 'photo_desc_str', 'category']
    create_csv(FILEPARAMS, order)
    with open('../urls_csv/urls_coche_electrico_tab.csv', 'r', encoding='utf-8') as file:
        for line in csv.DictReader(file):
            url = line['url']
            get_data(url)


if __name__ == '__main__':
    main()
