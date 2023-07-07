import requests
from bs4 import BeautifulSoup
import csv

# Отправляем GET-запрос к веб-странице
url = "https://www.songofindia.co.in/index.php/home-fragrances/reeds-diffuser.html"
response = requests.get(url)

# Создаем объект BeautifulSoup для парсинга HTML-кода страницы
soup = BeautifulSoup(response.content, "html.parser")

# Находим все элементы <a> с классом "product-name"
product_links = soup.find_all("a", class_="product-name")

# Создаем список для хранения ссылок на товары
links = []

# Обходим найденные элементы и извлекаем ссылки на товары
for link in product_links:
    product_url = link["href"]
    links.append(product_url)

# Записываем ссылки в файл CSV
with open("products.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Ссылка на товар"])  # Записываем заголовок столбца
    for link in links:
        writer.writerow([link])

print("Ссылки на товары успешно записаны в файл products.csv.")
