from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv

# Опции для веб-драйвера
options = Options()
options.add_argument('--headless')  # Открытие браузера в фоновом режиме

# Инициализация веб-драйвера
driver = webdriver.Chrome(options=options)

base_url = "https://frenchcrown.in/collections/new-pants"
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
with open('templates/../../../urls_csv/urls_lounge_pants.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for link in product_links:
        writer.writerow({'url': link})

print("Ссылки на товары были успешно записаны в файл 'urls_wool_pants.csv'.")

# Закрытие веб-драйвера
driver.quit()


import csv
import time
from requests import Session
from bs4 import BeautifulSoup
from urllib.parse import urljoin


base_url = "https://frenchcrown.in/collections/new-pants"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


def main(base_url):
    s = Session()
    s.headers.update(headers)

    count = 1
    pagination = 0
    is_base_url = True  # Флаг для базового URL
    start_time = time.time()  # Время начала выполнения

    links = []  # Список ссылок

    while True:

        if count > 1:
            url = base_url + "?page=" + str(count)
        else:
            url = base_url

        response = s.get(url)
        soup = BeautifulSoup(response.text, "lxml")

        if count == 1:
            pagination = soup.find('div', class_="ProductListWrapper").find_all("div", class_="jQueryEqualHeight")[-2].get_text(strip=True)

        cards = soup.find_all('div', class_="ProductItem__Info ProductItem__Info--left")

        for card in cards:
            link_element = card.find("a", target="_blank")
            link = link_element.get("href")
            full_link = urljoin(base_url, link)
            if full_link != base_url:  # Проверка для исключения базового URL
                links.append(full_link)
            else:
                is_base_url = False  # Установка флага в False, если текущая ссылка - базовый URL

        if count == pagination and not is_base_url:
            break

        count += 1

        # Проверка времени выполнения
        elapsed_time = time.time() - start_time
        if elapsed_time > 20:
            print("Превышено время выполнения. Процесс остановлен.")
            break

    with open('templates/../../../urls_csv/urls_jeans.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['url'])  # Запись заголовка
        writer.writerows([[link] for link in links])  # Запись ссылок

    print("Ссылки на товары были успешно записаны в файл 'new-jackets.csv'.")


main(base_url)
