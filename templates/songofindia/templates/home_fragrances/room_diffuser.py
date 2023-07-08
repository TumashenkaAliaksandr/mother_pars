import requests
from bs4 import BeautifulSoup
import csv


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

# Найти ссылку на фото товара
photo = soup.find("div", class_="product media").find("img")["src"]
print('Photo urls: ', photo)

# Найти описание товара
description = soup.find("div", class_="product attribute overview").find("div", class_="value").text.strip()
print('Descriptions: ', description)

# Найти ID товара (если доступно)
product_id_element = soup.find("span", class_="sku")
product_id = product_id_element.text.strip() if product_id_element else "N/A"
print('Product id: ', product_id)

# Записать данные в файл CSV
with open("product_info.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Title", "Price", "Photo", "Description", "Category", "ID"])
    writer.writerow([title, price, photo, description, category, product_id])

print("Информация о товаре успешно записана в файл product_info.csv.")
