# https://www.uniqlo.com/in/en/
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver as wiredriver
import time
import csv

# Опции для веб-драйвера
options = Options()
options.add_argument('--headless')  # Открытие браузера в фоновом режиме

# Инициализация веб-драйвера с использованием selenium-wire
driver = wiredriver.Chrome(options=options)

base_url = "https://www.uniqlo.com/in/en/baby/toddler/bottoms?path=%2C%2C11881"
driver.get(base_url)

# Ожидание завершения всех сетевых запросов
while True:
    network_requests = driver.requests
    pending_requests = [request for request in network_requests if request.response is None]
    if not pending_requests:
        break
    time.sleep(5)

# Получение ссылок на товары
product_links = []
link_elements = driver.find_elements(By.CSS_SELECTOR, 'article.fr-grid-item a')
for link_element in link_elements:
    link = link_element.get_attribute("href")
    if link and '/products/' in link:
        product_links.append(link)

# Запись ссылок на товары в файл CSV
fieldnames = ['url']
with open('urls_csv/urls_test3.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for link in product_links:
        writer.writerow({'url': link})

print("Ссылки на товары были успешно записаны в файл 'urls_test.csv'.")

# Закрытие веб-драйвера
driver.quit()
