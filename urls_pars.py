# import requests
# from bs4 import BeautifulSoup
# import csv
# import time
#
# URLS = [
#     'https://renaindia.com/collections/kitchenware-all',
#     'https://renaindia.com/collections/hostware',
#     'https://renaindia.com/collections/bakeware-all',
# ]
# FILENAME = 'urls_rena.csv'
#
#
# def create_csv(filename, fieldnames):
#     with open(filename, 'w', encoding='utf-8', newline='') as file:
#         writer = csv.DictWriter(file, fieldnames=fieldnames)
#         writer.writeheader()
#
#
# def write_csv(filename, data, fieldnames):
#     with open(filename, 'a', encoding='utf-8', newline='') as file:
#         writer = csv.DictWriter(file, fieldnames=fieldnames)
#         writer.writerow(data)
#
#
# def get_product_links(url):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     product_links = []
#     last_page_link = soup.select('.page')[-2].a.get('href', '')  # ссылка на последнюю страницу
#     last_page = int(last_page_link.split('=')[-1]) if last_page_link else 1
#     for page in range(1, last_page + 1):
#         page_url = url + f'?page={page}'
#         response = requests.get(page_url)
#         soup = BeautifulSoup(response.content, 'html.parser')
#         for link in soup.find_all('a'):
#             if 'product' in link.get('href', ''):
#                 link_url = 'https://renaindia.com' + link['href']
#                 if link_url not in product_links:
#                     product_links.append(link_url)
#         time.sleep(1)  # добавим задержку для увеличения интервала запросов
#     return product_links
#
#
# def main():
#     fieldnames = ['url']
#     create_csv(FILENAME, fieldnames)
#
#     for url in URLS:
#         product_links = get_product_links(url)
#         for link in product_links:
#             data = {'url': link}
#             write_csv(FILENAME, data, fieldnames)
#
#
# if __name__ == '__main__':
#     main()


# import requests
# import csv
# from bs4 import BeautifulSoup
#
# URLS = [
#     'https://autosolar.es/kit-solar-aislada/',
#     # 'https://autosolar.es/paneles-solares',
#     # 'https://autosolar.es/inversores',
# ]
# FILENAME = 'product_links_kits.csv'
#
#
# def create_csv(filename, fieldnames):
#     with open(filename, 'w', encoding='utf-8', newline='') as file:
#         writer = csv.DictWriter(file, fieldnames=fieldnames)
#         writer.writeheader()
#
#
# def write_csv(filename, data, fieldnames):
#     with open(filename, 'a', encoding='utf-8', newline='') as file:
#         writer = csv.DictWriter(file, fieldnames=fieldnames)
#         writer.writerow(data)
#
#
# def get_product_links(url):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     product_links = []
#     page_links = soup.select('.page-link')
#     if len(page_links) > 1:
#         last_page_link = page_links[-2].a
#         if last_page_link:
#             last_page_link = last_page_link.get('href', '')
#         last_page = int(last_page_link.split('=')[-1]) if last_page_link else 1
#         for page in range(1, last_page + 1):
#             page_url = url + f'?page={page}'
#             response = requests.get(page_url)
#             soup = BeautifulSoup(response.content, 'html.parser')
#             for link in soup.find_all('a'):
#                 if 'product' in link.get('href', ''):
#                     link_url = 'https://autosolar.es' + link['href']
#                     if link_url not in product_links:
#                         product_links.append(link_url)
#     else:
#         for link in soup.find_all('a'):
#             if 'product' in link.get('href', ''):
#                 link_url = 'https://autosolar.es' + link['href']
#                 if link_url not in product_links:
#                     product_links.append(link_url)
#     return product_links
#
#
#
# def main():
#     fieldnames = ['url']
#     create_csv(FILENAME, fieldnames)
#
#     for url in URLS:
#         product_links = get_product_links(url)
#         for link in product_links:
#             data = {'url': link}
#             write_csv(FILENAME, data, fieldnames)
#
#     print(f"Ссылки на товары записаны в файл {FILENAME}")
#
#
# if __name__ == '__main__':
#     main()

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

URL = 'https://autosolar.es/kits-solares'


def get_product_links(url):
    options = Options()
    options.add_argument('--headless')  # Запуск браузера в безголовом режиме (без открытия окна)
    service = Service('путь_к_chromedriver')  # Замените 'путь_к_chromedriver' на путь к установленному Chromedriver

    with webdriver.Chrome(service=service, options=options) as driver:
        driver.get(url)
        time.sleep(3)  # Даем странице время для полной загрузки

        # Прокрутка страницы до конца для динамической загрузки контента
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Поиск ссылок на товары
        product_links = []
        elements = driver.find_elements(By.CSS_SELECTOR, '.woocommerce-LoopProduct-link')
        for element in elements:
            product_links.append(element.get_attribute('href'))

    return product_links


# Получение ссылок на товары
product_links = get_product_links(URL)

# Вывод ссылок
for link in product_links:
    print(link)
