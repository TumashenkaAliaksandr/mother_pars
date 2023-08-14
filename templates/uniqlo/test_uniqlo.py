# https://www.uniqlo.com/in/en/
#
# import requests
# from bs4 import BeautifulSoup
# import csv
# import time
#
# base_url = "https://www.uniqlo.com/in/en/baby/newborn/birth-preparation-items?path=%2C%2C23418&page="
# page_num = 1
# links = []
#
# while True:
#     url = base_url + str(page_num)
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, "html.parser")
#
#     product_articles = soup.find_all("article", class_="fr-grid-item")
#
#     for article in product_articles:
#         link_element = article.find("a")
#         if link_element:
#             link = link_element["href"]
#             links.append(link)
#
#     next_link = soup.find("a", class_="next")
#     if not next_link:
#         break
#
#     page_num += 1
#     time.sleep(1)  # Задержка в 1 секунду между запросами
#
# with open("urls_test.csv", "w", newline="") as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(["url"])
#     for link in links:
#         writer.writerow([link])
#
# print("Ссылки на товары успешно записаны в файл urls_test.csv.")


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import csv

# Опции для веб-драйвера
options = Options()
options.add_argument('--headless')  # Открытие браузера в фоновом режиме

# Инициализация веб-драйвера
driver = webdriver.Chrome(options=options)

base_url = "https://www.uniqlo.com/in/en/baby/newborn/birth-preparation-items?path=%2C%2C23418&page="
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
link_elements = driver.find_elements(By.CSS_SELECTOR, 'article.fr-grid-item a')
for link_element in link_elements:
    link = link_element.get_attribute("href")
    if link and '/products/' in link:
        product_links.append(link)


# Запись ссылок на товары в файл CSV
fieldnames = ['url']
with open('urls_test.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for link in product_links:
        writer.writerow({'url': link})

print("Ссылки на товары были успешно записаны в файл 'urls_test.csv'.")

# Закрытие веб-драйвера
driver.quit()
