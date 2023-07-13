from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import csv

# Опции для веб-драйвера
options = Options()
options.add_argument('--headless')  # Открытие браузера в фоновом режиме

# Инициализация веб-драйвера
driver = webdriver.Chrome(options=options)

base_url = "https://frenchcrown.in/collections/boxers"
driver.get(base_url)

# Скроллинг страницы вниз, чтобы загрузить все товары
while True:
    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break

# Получение ссылок на товары
product_links = set()
link_elements = driver.find_elements("css selector", "div.ProductItem__Wrapper a")
for link_element in link_elements:
    link = link_element.get_attribute("href")
    if link and "/products/" in link:
        product_links.add(link)

# Запись ссылок на товары в файл CSV
fieldnames = ['url']
with open('templates/../../../urls_csv/urls_boxers.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for link in product_links:
        writer.writerow({'url': link})

print("Ссылки на товары были успешно записаны в файл 'urls_boxers.csv'.")

# Закрытие веб-драйвера
driver.quit()
