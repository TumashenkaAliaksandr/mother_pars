import requests
from bs4 import BeautifulSoup
import csv
import textwrap

url = "https://www.songofindia.co.in/index.php/mysore-chandan-sandalwood-organic-ambience-diffuser-with-reeds.html"
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

# Найти заголовок товара
title = soup.find("h1", class_="page-title").text.strip()
print('Title: ', title)

# Найти категорию товара
category = 'Home Fragrance | Room Diffuser'
print('Category: ', category)

# Найти цену товара
price = soup.find("span", class_="price").text.replace('₹', '').strip()
print('Price: ', price)

# Найти контейнеры с классом "fotorama__stage__frame"
frame_containers = soup.find_all("div", {"class": "fotorama__stage__shaft"})
photos = []

# Извлечь URL-адреса фотографий из атрибутов "href"
for container in frame_containers:
    img_tag = container.find("href")
    if img_tag:
        photos.append(img_tag)

# Если список фотографий пуст, добавить значение 'N/A'
if not photos:
    photos.append('N/A')

# Вывести список URL-адресов фотографий
print('Photo URLs:', photos)


# Найти описание товара
description = soup.find("div", class_="product attribute overview").find("div", class_="value").text.strip()
wrapped_description = textwrap.fill(description, width=100, break_long_words=False)
print('Descriptions: ', wrapped_description)

# Найти таблицу с атрибутом id="product-attribute-specs-table"
table = soup.find("table", id="product-attribute-specs-table")

# Найти заголовок таблицы
caption = table.find("caption", class_="table-caption").text.strip()
print("Table Caption:", caption)

# Итерироваться по строкам таблицы и собрать текст из всех ячеек в одну переменную
description_all = ""
rows = table.find_all("tr")
for row in rows:
    # Найти теги <th> и <td> внутри строки
    th_tags = row.find_all(["th", "td"])

    # Извлечь текст из тегов <th> и <td> с выполнением переноса слов
    for tag in th_tags:
        text = tag.text.strip()
        wrapped_text = textwrap.fill(text, width=100, break_long_words=False)
        description_all += wrapped_text + "\n"
        print(wrapped_text)
    print()


# Найти ID товара (если доступно)
product_id_element = soup.find("div", class_="fotorama__caption__wrap")
product_id = product_id_element.text.strip() if product_id_element else "N/A"
print('Product id: ', product_id)

# Записать данные в файл CSV
with open("product_info.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Title", "Price", "Photo", "Description", "Description_all", "Category", "ID"])
    writer.writerow([title, price, photos, wrapped_description, description_all, category, product_id])

print("Информация о товаре успешно записана в файл product_info.csv.")
