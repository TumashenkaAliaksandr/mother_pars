import requests
from bs4 import BeautifulSoup
import csv
import time

URLS = [    'https://renaindia.com/collections/kitchenware-all',    'https://renaindia.com/collections/hostware',    'https://renaindia.com/collections/bakeware-all',]
FILENAME = 'urls_rena.csv'


def create_csv(filename, fieldnames):
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()


def write_csv(filename, data, fieldnames):
    with open(filename, 'a', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(data)


def get_product_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    product_links = []
    last_page_link = soup.select('.page')[-2].a.get('href', '')  # ссылка на последнюю страницу
    last_page = int(last_page_link.split('=')[-1]) if last_page_link else 1
    for page in range(1, last_page + 1):
        page_url = url + f'?page={page}'
        response = requests.get(page_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        for link in soup.find_all('a'):
            if 'product' in link.get('href', ''):
                link_url = 'https://renaindia.com' + link['href']
                if link_url not in product_links:
                    product_links.append(link_url)
        time.sleep(1)  # добавим задержку для увеличения интервала запросов
    return product_links


def main():
    fieldnames = ['url']
    create_csv(FILENAME, fieldnames)

    for url in URLS:
        product_links = get_product_links(url)
        for link in product_links:
            data = {'url': link}
            write_csv(FILENAME, data, fieldnames)


if __name__ == '__main__':
    main()
