# # https://www.groovee.in/browse/oversized-tie-dye-hoodies-and-sweatshirts-for-men
#
# import csv
# from selenium import webdriver
# from bs4 import BeautifulSoup
# import urllib.parse
# import time
#
# url = "https://groovee.in/collections/oversized-tshirts"
#
# # Запускаем браузер
# driver = webdriver.Chrome()
# driver.get(url)
#
# # Ждем 20 секунд для загрузки страницы
# time.sleep(100)
#
# # Получаем HTML-код страницы после загрузки JavaScript
# html = driver.page_source
#
# # Используем BeautifulSoup для парсинга HTML
# soup = BeautifulSoup(html, 'html.parser')
#
# # Находим все ссылки на странице, которые начинаются с '/product/'
# links = soup.find_all('a', href=True)
# product_links = set()
# for link in links:
#     if link['href'].startswith('/product/'):
#         product_links.add(urllib.parse.urljoin(url, link['href']))
#
# # Записываем найденные ссылки в файл CSV
# with open('../urls_csv/urls_oversized_t-shirt_men_women_male.csv', 'w', newline='') as csvfile:
#     fieldnames = ['Link']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#
#     writer.writeheader()
#     for product_link in product_links:
#         writer.writerow({'Link': product_link})
#
# # Закрываем браузер после использования
# driver.quit()


import csv
import urllib.parse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url = "https://groovee.in/collections/oversized-tshirts"

options = Options()
options.page_load_strategy = "eager"
driver = webdriver.Chrome(options=options)
driver.set_page_load_timeout(30)

try:
    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    product_links = set()
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if "/collections/" in href and "/products/" in href:
            product_links.add(urllib.parse.urljoin(url, href))

    with open(r"../urls_csv/urls_oversized_t-shirt_men_women_male.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["Link"])
        writer.writeheader()
        for product_link in sorted(product_links):
            writer.writerow({"Link": product_link})

finally:
    driver.quit()