import csv
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.parse

url = "https://www.groovee.in/browse/oversized-tshirts"

# Запускаем браузер
driver = webdriver.Chrome()
driver.get(url)

# Получаем HTML-код страницы после загрузки JavaScript
html = driver.page_source

# Используем BeautifulSoup для парсинга HTML
soup = BeautifulSoup(html, 'html.parser')

# Находим все ссылки на странице, которые начинаются с '/product/'
links = soup.find_all('a', href=True)
product_links = set()
for link in links:
    if link['href'].startswith('/product/'):
        product_links.add(urllib.parse.urljoin(url, link['href']))

# Записываем найденные ссылки в файл CSV
with open('../urls_csv/urls_groovee_tsh.csv', 'w', newline='') as csvfile:
    fieldnames = ['Link']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for product_link in product_links:
        writer.writerow({'Link': product_link})

# Закрываем браузер после использования
driver.quit()
