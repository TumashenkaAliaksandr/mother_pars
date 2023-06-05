from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import csv

# Опции для веб-драйвера
options = Options()
options.add_argument('--headless')  # Открытие браузера в фоновом режиме

# Инициализация веб-драйвера
driver = webdriver.Chrome(options=options)

base_url = "https://nobero.com/collections/pick-printed-t-shirts"
driver.get(base_url)

# Прокрутка страницы для динамической загрузки контента
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Получение ссылок на товары
product_links = []
link_elements = driver.find_elements('css selector', 'a.product_link')
for link_element in link_elements:
    link = link_element.get_attribute("href")
    if link and '/products/' in link:
        product_links.append(link)

# Запись ссылок на товары в файл CSV
fieldnames = ['url']
with open('templates/../../urls_csv/test_pick_printed_t_shirts.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for link in product_links:
        writer.writerow({'url': link})

print("Ссылки на товары были успешно записаны в файл 'product_links.csv'.")

# Закрытие веб-драйвера
driver.quit()
