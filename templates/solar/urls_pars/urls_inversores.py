import os
import requests
from bs4 import BeautifulSoup
import csv


directory = '../urls_csv'
FILENAME = 'urls_inversores.csv'
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
url = "https://autosolar.es/inversores"
response = requests.get(url)

# Проверка успешности запроса
if response.status_code == 200:
    # Инициализация объекта BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(response.content, "html.parser")

    # Нахождение всех ссылок на товары
    product_links = set()
    link_elements = soup.select('div.category-products a')
    for link_element in link_elements:
        link = link_element.get("href")
        product_links.add(link)

    # Поиск и обработка остальных страниц пагинации
    pagination = soup.find("div", {'class': 'pagination'})
    if pagination is not None:
        pages = pagination.find_all("li")
        for page in pages:
            page_link = page.find("a")
            if page_link is not None:
                page_url = page_link["href"]
                page_response = requests.get(page_url)
                if page_response.status_code == 200:
                    page_soup = BeautifulSoup(page_response.content, "html.parser")
                    page_link_elements = page_soup.select('div.category-products a')
                    for page_link_element in page_link_elements:
                        page_link = page_link_element.get("href")
                        product_links.add(page_link)

    # Запись ссылок на товары в файл
    fieldnames = ['url']
    create_csv(FILEPARAMS, fieldnames)
    for link in product_links:
        data = {'url': link}
        write_csv(FILEPARAMS, data, fieldnames)
else:
    print("Не удалось выполнить запрос к странице категории.")