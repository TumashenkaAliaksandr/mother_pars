import requests
from bs4 import BeautifulSoup
import csv


FILEPARAMS = 'tab_rena.csv'

def create_csv(filename, order):
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        csv.DictWriter(file, fieldnames=order).writeheader()


def write_csv(filename, data):
    with open(filename, 'a', encoding='utf-8', newline='') as file:
        csv.DictWriter(file, fieldnames=list(data)).writerow(data)


def get_data(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find('h1', {'class': 'product_name'}).text.strip()
    price = soup.find('div', {'class': 'price-ui'})
    cost = price.find('span').text.replace('Rs.', '').strip()
    desc = soup.find('div', {'class': 'description'}).text.strip()

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

    img_container = soup.find('div', {'class': 'image__container'})
    img_src = "https:" + img_container.find('img')['data-src']

    print(title, cost, formatted_text, img_src, sep='\n')

    data = {'title': title, 'cost': cost, 'description': formatted_text, 'img_src': img_src}
    write_csv(FILEPARAMS, data)


def main():
    order = ['title', 'cost', 'description',  'img_src']
    create_csv(FILEPARAMS,order)

    with open('urls_rena.csv', 'r', encoding='utf-8') as file:
        for line in csv.DictReader(file):
            url = line['url']
            get_data(url)


if __name__ == '__main__':
    main()
