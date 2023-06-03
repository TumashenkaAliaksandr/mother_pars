import os
import requests
from bs4 import BeautifulSoup
import csv

directory = 'templates/../../urls_csv'
FILENAME = 'urls_folkbazar_thangkas.csv'
FILEPARAMS = os.path.join(directory, FILENAME)

def create_csv(filename, fieldnames):
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

def write_csv(filename, data, fieldnames):
    with open(filename, 'a', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(data)

# Отправка запроса на страницу категории
base_url = "https://folkbazar.com/en-us/collections/thangkas?page="
response = requests.get(base_url)

# Проверка успешности запроса
if response.status_code == 200:
    # Инициализация объекта BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(response.content, "html.parser")

    # Нахождение всех ссылок на товары, исключая ссылки с ключевым словом 'incense'
    product_links = set()
    link_elements = soup.select('div.grid a')
    for link_element in link_elements:
        link = link_element.get("href")
        if link and '/collections/thangkas/products/' in link and 'incense' not in link:
            added = "https://folkbazar.com" + link
            product_links.add(added)

    # Поиск и обработка остальных страниц пагинации
    pagination = soup.find("div", class_='pagination')
    if pagination is not None:
        pages = pagination.find_all("a")
        for page in pages:
            page_link = page.get("href")
            if page_link and '/collections/thangkas?page=' in page_link:
                page_url = "https://folkbazar.com" + page_link
                page_response = requests.get(page_url)
                if page_response.status_code == 200:
                    page_soup = BeautifulSoup(page_response.content, "html.parser")
                    page_link_elements = page_soup.select('div.grid a')
                    for page_link_element in page_link_elements:
                        page_link = page_link_element.get("href")
                        if page_link and '/collections/thangkas/products/' in page_link and 'incense' not in page_link:
                            product_links.add("https://folkbazar.com" + page_link)

    # Запись ссылок на товары в файл
    fieldnames = ['url']
    create_csv(FILEPARAMS, fieldnames)
    for link in product_links:
        data = {'url': link}
        write_csv(FILEPARAMS, data, fieldnames)
else:
    print("Не удалось выполнить запрос к странице категории.")
