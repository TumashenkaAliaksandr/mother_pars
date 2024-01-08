import requests
from bs4 import BeautifulSoup
import csv

# Получаем HTML-код страницы
url = 'https://bryanandcandy.com/collections/body-scrub-for-glowing-skin'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

product_link = soup.find('a', class_='ProductItem__ImageWrapper')


# Находим все ссылки на товары
product_links = []
for product in soup.find_all('a', class_='ProductItem__ImageWrapper'):
    product_link = product.get('href')
    full_link = f'https://bryanandcandy.com{product_link}'
    product_links.append(full_link)

# Выводим все найденные ссылки
for link in product_links:
    print(link)


# Записываем ссылки в CSV файл
with open('../urls_csv/body_scrub_for_glowing_skin_links.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['url'])
    for link in product_links:
        writer.writerow([link])
