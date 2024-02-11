import requests
from bs4 import BeautifulSoup
import csv

# URL веб-сайта, с которого вы хотите собрать ссылки на товары
base_url = 'https://www.camveda.com/'

# Получаем HTML-код страницы
response = requests.get(base_url)
soup = BeautifulSoup(response.content, 'html.parser')

# Находим все ссылки на товары
product_links = []
for link in soup.find_all('a', href=True):
    href = link['href']
    if '/collections/' in href:
        if href.startswith('http'):  # Проверяем, что ссылка абсолютная
            product_links.append(href)
        else:  # Преобразуем относительную ссылку в абсолютную
            product_links.append(base_url + href.lstrip('/'))

# Записываем найденные ссылки в файл CSV
with open('product_links.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Product Links'])
    for product_link in product_links:
        writer.writerow([product_link])

print("Ссылки на товары были сохранены в файл 'honeyhut_urls.csv'.")
