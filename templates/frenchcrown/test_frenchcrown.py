# import requests
# import csv
#
# base_url = "https://hits.gokwik.co/api/v1/header/events/update"
#
# def main(base_url):
#     product_links = set()
#     page = 1
#
#     while True:
#         url = f"{base_url}?page={page}"
#         response = requests.get(url)
#         json_data = response.json()
#
#         # Проверяем, есть ли еще страницы
#         if not json_data or not json_data.get("data"):
#             break
#
#         for item in json_data["data"]:
#             link = item.get("url")
#             if link:
#                 product_links.add(link)
#
#         page += 1
#
#     with open('urls_boxers.csv', 'w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerow(['url'])
#         writer.writerows([[link] for link in product_links])
#
#     print("Ссылки на товары были успешно записаны в файл 'urls_boxers.csv'.")
#
# main(base_url)


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv

# Опции для веб-драйвера
options = Options()
options.add_argument('--headless')  # Открытие браузера в фоновом режиме

# Инициализация веб-драйвера
driver = webdriver.Chrome(options=options)

base_url = "https://frenchcrown.in/collections/boxers"
driver.get(base_url)

# Получение ссылок на товары
product_links = []

while True:
    link_elements = driver.find_elements_by_css_selector("div.ProductItem__Info a.pr-title")
    for link_element in link_elements:
        link = link_element.get_attribute("href")
        product_links.append(link)

    next_button = driver.find_element_by_css_selector("div.Pagination__Nav a.is-active + a")
    if next_button:
        next_button.click()
    else:
        break

# Запись ссылок на товары в файл CSV
fieldnames = ['url']
with open('product_links.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for link in product_links:
        writer.writerow({'url': link})

print("Ссылки на товары были успешно записаны в файл 'product_links.csv'.")

# Закрытие веб-драйвера
driver.quit()
