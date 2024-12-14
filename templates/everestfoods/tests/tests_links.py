import requests
from bs4 import BeautifulSoup
import csv

# URL страницы, которую нужно парсить
url = "https://www.everestfoods.com/products/"

# Выполнение GET-запроса к странице
response = requests.get(url)

# Проверка успешности запроса
if response.status_code == 200:
    # Парсинг HTML-кода страницы
    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим все блоки с классом "d-flex spicesyoumaylike__listing"
    product_blocks = soup.find_all('div', class_='d-flex spicesyoumaylike__listing')

    # Список для хранения ссылок на товары
    product_links = []

    # Проверяем, если на странице есть товары
    if not product_blocks:
        print("Товары не найдены на странице.")
    else:
        for block in product_blocks:
            # Находим все теги <a> внутри блока
            product_link_tags = block.find_all('a', class_='spicesyoumaylike__box')
            for product_link_tag in product_link_tags:
                # Извлекаем значение атрибута "href"
                href = product_link_tag.get('href')
                if href:
                    product_links.append(href)

        print(f"Собрано {len(product_links)} товаров.")

else:
    print("Не удалось получить доступ к странице. Код состояния:", response.status_code)

# Записываем ссылки в CSV файл
with open('../urls_csv/product_links.csv', 'w', newline='') as csvfile:
    fieldnames = ['url']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for link in product_links:
        writer.writerow({'url': link})

print("Ссылки успешно записаны в файл product_links.csv")
