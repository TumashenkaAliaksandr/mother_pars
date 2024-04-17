import csv
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.parse
import time

# Задаем URL сайта
url = "https://www.chokore.com/collections/gift-sets"

# Запускаем браузер
driver = webdriver.Chrome()
driver.get(url)

# Ждем 20 секунд для загрузки страницы
time.sleep(100)

# Получаем HTML-код страницы после загрузки JavaScript
html = driver.page_source

# Используем BeautifulSoup для парсинга HTML
soup = BeautifulSoup(html, 'html.parser')

# Находим все ссылки на странице
links = soup.find_all('a', href=True)
product_links = set()
for link in links:
    href = link.get('href')
    # Проверяем, является ли ссылка на товар
    if href and '/collections/gift-sets/products/' in href:
        product_links.add(urllib.parse.urljoin(url, href))

# Записываем найденные уникальные ссылки в файл CSV
with open('../product_gift_sets.csv', 'w', newline='') as csvfile:
    fieldnames = ['Link']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for product_link in product_links:
        writer.writerow({'Link': product_link})

# Закрываем браузер после использования
driver.quit()
