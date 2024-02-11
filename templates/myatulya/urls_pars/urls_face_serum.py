import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

url_base = "https://myatulya.com"
url = url_base + "/collections/face-serum"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    product_links = []

    # Находим все теги <a> с классом "grid-product__title"
    product_link_tags = soup.find_all('a', class_='grid-product__link')

    for product_link_tag in product_link_tags:
        # Извлекаем значение атрибута "href"
        href = product_link_tag.get('href')

        # Добавляем префикс к ссылке
        full_url = urljoin(url_base, href)

        # Добавляем ссылку в список
        product_links.append(full_url)

    # Записываем ссылки в CSV файл
    with open('../urls_csv/face_serum_links.csv', 'w', newline='') as csvfile:
        fieldnames = ['url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for link in product_links:
            writer.writerow({'url': link})

    print("Ссылки успешно записаны в файл honeyhut_urls.csv")
else:
    print("Не удалось получить доступ к странице. Код состояния:", response.status_code)
