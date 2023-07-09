# import requests
# from bs4 import BeautifulSoup
# import csv
#
# url = "https://www.songofindia.co.in/index.php/home-fragrances/reeds-diffuser.html"
# response = requests.get(url)
#
# soup = BeautifulSoup(response.content, "html.parser")
#
# product_divs = soup.find_all("div", class_="product photo product-item-photo")
#
# links = []
#
# for div in product_divs:
#     link = div.find("a")["href"]
#     links.append(link)
#
# with open("products.csv", "w", newline="") as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(["Ссылка на товар"])
#     for link in links:
#         writer.writerow([link])
#
# print("Ссылки на товары успешно записаны в файл products.csv.")


# import requests
# from bs4 import BeautifulSoup
# import csv
#
# base_url = "https://www.songofindia.co.in/index.php/home-fragrances/reeds-diffuser.html?p="
# page_num = 1
# links = []
#
# while True:
#     url = base_url + str(page_num)
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, "html.parser")
#
#     product_divs = soup.find_all("div", class_="product-item-info")
#
#     for div in product_divs:
#         link = div.find("a")["href"]
#         links.append(link)
#
#     next_link = soup.find("a", class_="next")
#     if not next_link:
#         break
#
#     page_num += 1
#
# with open("products.csv", "w", newline="") as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(["Ссылка на товар"])
#     for link in links:
#         writer.writerow([link])
#
# print("Ссылки на товары успешно записаны в файл products.csv.")

from bs4 import BeautifulSoup

import requests
from bs4 import BeautifulSoup

# Ссылка на страницу с товаром
url = "https://www.songofindia.co.in/index.php/mysore-chandan-sandalwood-organic-ambience-diffuser-with-reeds.html"

# Получаем HTML-код страницы
response = requests.get(url)
html_content = response.text

# Создаем объект BeautifulSoup для парсинга HTML
soup = BeautifulSoup(html_content, "html.parser")

# Находим указанный блок
div_block = soup.find("div", {"class": "fotorama__stage__frame"})

# Проверяем, что блок найден
if div_block is not None:
    # Находим все изображения внутри блока
    images = div_block.find_all("img")

    # Получаем ссылки на изображения
    image_urls = [img.get("src") for img in images]

    # Выводим ссылки на изображения
    for url in image_urls:
        print(url)
else:
    print("Блок не найден.")







