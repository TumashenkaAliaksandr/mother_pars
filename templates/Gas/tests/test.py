import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin


def get_product_links(page_url):
    response = requests.get(page_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    product_links = set()  # Используем множество для автоматического удаления дубликатов

    # Находим все теги <a> с классом "single-product"
    product_link_tags = soup.find_all('a', class_='single-product')
    for product_link_tag in product_link_tags:
        # Извлекаем значение атрибута "href"
        href = product_link_tag.get('href')
        # Добавляем префикс к ссылке
        full_url = urljoin(base_url, href)
        # Добавляем ссылку в множество
        product_links.add(full_url)

    return product_links

base_url = "https://www.gasjeans.in/"
url = urljoin(base_url, "gasjeans-man")

all_product_links = set()  # Используем множество для всех ссылок
page_number = 1

while True:
    page_url = f"{url}?page={page_number}"
    product_links = get_product_links(page_url)

    if not product_links:
        break

    all_product_links.update(product_links)
    page_number += 1

# Записываем ссылки в CSV файл
with open('../urls_csv/gas_product_links.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['url']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for link in all_product_links:
        writer.writerow({'url': link})

print("Ссылки успешно записаны в файл 'product_links.csv'")
