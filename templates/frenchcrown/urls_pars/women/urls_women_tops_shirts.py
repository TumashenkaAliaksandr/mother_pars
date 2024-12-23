from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv

# Опции для веб-драйвера
options = Options()
options.add_argument('--headless')  # Открытие браузера в фоновом режиме

# Инициализация веб-драйвера
driver = webdriver.Chrome(options=options)

base_url = "https://frenchcrown.in/collections/women-tops"
driver.get(base_url)

# Получение ссылок на товары
product_links = []
link_elements = driver.find_elements("css selector", "div.ProductItem__Wrapper a")
for link_element in link_elements:
    link = link_element.get_attribute("href")
    if link and "/products/" in link:
        product_links.append(link)

# Запись ссылок на товары в файл CSV
fieldnames = ['url']
with open('templates/../../../urls_csv/urls_women_tops_shirts.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for link in product_links:
        writer.writerow({'url': link})

print("Ссылки на товары были успешно записаны в файл 'urls_shirts_old.csv'.")

# Закрытие веб-драйвера
driver.quit()
