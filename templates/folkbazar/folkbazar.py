import os
import requests
from bs4 import BeautifulSoup
import csv


directory = 'templates/../done_csv'
filename = 'folkbazar.csv'
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
    price = price_element.text.replace('Rs.', '').replace(',', '').strip() if price_element else 'N/A'

    desc_container = soup.find('div', {'class': 'product-single__description'})
    desc = desc_container.text.strip() if desc_container else ''

    category = 'religious-statues'

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

    img_container = soup.find('div', {'class': 'product-single__photo'})
    img_src = 'http' + img_container.find('img')['src'] if img_container else ''

    img_container_two = soup.find('div', {'class': 'product - single__thumbnail'})
    img_src_two = 'http' + img_container.find('img')['src'] if img_container else ''


    print(title, price, formatted_text, img_src, img_src_two, category)

    data = {'title': title, 'price': price, 'description': formatted_text,
            'img_src': img_src, 'img_src_two': img_src_two, 'category': category}
    write_data_csv(FILEPARAMS, data)


def main():
    order = ['title', 'cost', 'description',  'img_src', 'img_src_two', 'category']
    create_csv(FILEPARAMS, order)
    with open('templates/../urls_csv/urls_folkbazar.csv', 'r', encoding='utf-8') as file:
        for line in csv.DictReader(file):
            url = line['url']
            get_data(url)


if __name__ == '__main__':
    main()
