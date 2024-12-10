# import requests
# from bs4 import BeautifulSoup
# import csv
#
# # URL страницы категории, которую нужно парсить
# url_base = "https://islamicshop.in"
# url_base_page = url_base + "/men/"
# product_links = []
#
# # Начинаем с первой страницы
# page_number = 1
#
# while True:
#     # Формируем URL для текущей страницы
#     if page_number == 1:
#         url = url_base_page  # Первая страница без параметров
#     else:
#         url = f"{url_base_page}?p={page_number}"  # Параметр пагинации
#
#     # Выполнение GET-запроса к странице
#     response = requests.get(url)
#
#     # Проверка успешности запроса
#     if response.status_code == 200:
#         # Парсинг HTML-кода страницы
#         soup = BeautifulSoup(response.text, 'html.parser')
#
#         # Находим все теги <a> с классом "product-image"
#         product_link_tags = soup.find_all('a', class_='img')
#
#         # Если на странице нет товаров, выходим из цикла
#         if not product_link_tags:
#             print("Товары не найдены на странице", page_number)
#             break
#
#         for product_link_tag in product_link_tags:
#             # Извлекаем значение атрибута "href"
#             href = product_link_tag.get('href')
#
#             # Добавляем ссылку в список, если она существует
#             if href:
#                 product_links.append(href)
#
#         print(f"Собрано {len(product_link_tags)} товаров с страницы {page_number}")
#
#         # Переходим к следующей странице
#         page_number += 1
#     else:
#         print("Не удалось получить доступ к странице. Код состояния:", response.status_code)
#         break
#
# # Записываем ссылки в CSV файл
# with open('product_links.csv', 'w', newline='') as csvfile:
#     fieldnames = ['url']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()
#
#     for link in product_links:
#         writer.writerow({'url': link})
#
# print("Ссылки успешно записаны в файл product_links.csv")


import requests
from bs4 import BeautifulSoup
import csv

# Базовый URL страницы категории
url_base = "https://islamicshop.in/men/"
product_links = []

# Начинаем с первой страницы
page_number = 1

while True:
    # Формируем URL для текущей страницы
    url = f"{url_base}?p={page_number}"  # Параметр пагинации

    # Выполнение GET-запроса к странице
    response = requests.get(url)

    # Проверка успешности запроса
    if response.status_code == 200:
        # Парсинг HTML-кода страницы
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим все блоки с классом "product-block"
        image_blocks = soup.find_all('div', class_='product-block')

        # Если на странице нет изображений, выходим из цикла
        if not image_blocks:
            print("Товары не найдены на странице", page_number)
            break

        for block in image_blocks:
            # Находим тег <a> с классом "product-image" для основной ссылки на товар
            product_image_tag = block.find('a', class_='img')
            if product_image_tag:
                # Извлекаем значение атрибута "href"
                href = product_image_tag.get('href')
                if href:
                    product_links.append(href)

        print(f"Собрано {len(image_blocks)} товаров с страницы {page_number}")

        # Проверяем наличие следующей страницы
        pages_block = soup.find('div', class_='pages')
        if pages_block:
            next_page_tag = pages_block.find('a', class_='next')  # Ищем ссылку на следующую страницу
            if not next_page_tag:
                print("Следующая страница не найдена. Завершение.")
                break

            # Переходим к следующей странице по номеру из ссылки
            page_number += 1
        else:
            print("Не удалось найти блок с пагинацией. Завершение.")
            break

    else:
        print("Не удалось получить доступ к странице. Код состояния:", response.status_code)
        break

# Записываем ссылки в CSV файл
with open('../urls_csv/product_links.csv', 'w', newline='') as csvfile:
    fieldnames = ['url']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for link in product_links:
        writer.writerow({'url': link})

print("Ссылки успешно записаны в файл product_links.csv")

