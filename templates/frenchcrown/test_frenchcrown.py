# import csv
# import time
# from requests import Session
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin
#
# base_url = "https://frenchcrown.in/collections/boxers"
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
# }
#
# def main(base_url):
#     s = Session()
#     s.headers.update(headers)
#
#     count = 1
#     pagination = 0
#     is_base_url = True  # Флаг для базового URL
#     start_time = time.time()  # Время начала выполнения
#
#     links = []  # Список ссылок
#
#     while True:
#
#         if count > 1:
#             url = base_url + "?page=" + str(count)
#         else:
#             url = base_url
#
#         response = s.get(url)
#         soup = BeautifulSoup(response.text, "lxml")
#
#         if count == 1:
#             pagination = soup.find('div', class_="ProductListWrapper").find_all("div", class_="jQueryEqualHeight")[-2].get_text(strip=True)
#
#         cards = soup.find_all('div', class_="ProductItem__Info ProductItem__Info--left")
#
#         for card in cards:
#             link_element = card.find("a", target="_blank")
#             link = link_element.get("href")
#             full_link = urljoin(base_url, link)
#             if full_link != base_url:  # Проверка для исключения базового URL
#                 links.append(full_link)
#             else:
#                 is_base_url = False  # Установка флага в False, если текущая ссылка - базовый URL
#
#         if count == pagination and not is_base_url:
#             break
#
#         count += 1
#
#         # Проверка времени выполнения
#         elapsed_time = time.time() - start_time
#         if elapsed_time > 20:
#             print("Превышено время выполнения. Процесс остановлен.")
#             break
#
#     with open('templates/../../../urls_csv/urls_boxers.csv', 'w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerow(['url'])  # Запись заголовка
#         writer.writerows([[link] for link in links])  # Запись ссылок
#
#     print("Ссылки на товары были успешно записаны в файл 'boxers.csv'.")
#
#
# main(base_url)
#
#
#
#
#

# from requests import Session
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin
#
# base_url = "https://frenchcrown.in/collections/boxers"
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
# }
#
# def main(base_url):
#     s = Session()
#     s.headers.update(headers)
#
#     count = 1
#     pagination = 0
#     is_base_url = True  # Флаг для базового URL
#     while True:
#
#         if count > 1:
#             url = base_url + "?page=" + str(count)
#         else:
#             url = base_url
#
#         response = s.get(url)
#         soup = BeautifulSoup(response.text, "lxml")
#
#         if count == 1:
#             pagination = soup.find('div', class_="ProductListWrapper").find_all("div", class_="jQueryEqualHeight")[-2].get_text(strip=True)
#
#         cards = soup.find_all('div', class_="ProductItem__Info ProductItem__Info--left")
#
#         for card in cards:
#             link_element = card.find("a", target="_blank")
#             link = link_element.get("href")
#             full_link = urljoin(base_url, link)
#             if full_link != base_url:  # Проверка для исключения базового URL
#                 print(full_link)
#             else:
#                 is_base_url = False  # Установка флага в False, если текущая ссылка - базовый URL
#
#         if count == pagination and not is_base_url:
#             break
#
#         count += 1
#
#     with open('boxers.csv', 'w', newline='', encoding='utf-8') as file:
#         file.write(response.text)
#
#     print("Ссылки на товары были успешно записаны в файл 'boxers.html'.")
#
#
# main(base_url)
#





# import requests
# from bs4 import BeautifulSoup
# import csv
#
# base_url = "https://frenchcrown.in/collections/boxers"
#
# def main(base_url):
#     product_links = []
#     data_variants = []
#
#     response = requests.get(base_url)
#     soup = BeautifulSoup(response.text, "html.parser")
#     product_elements = soup.find_all("div", class_="ProductItem__Info")
#
#     for product_element in product_elements:
#         link_element = product_element.find("a", target="_blank")
#         link = link_element.get("href")
#         if link and "/products/" in link:
#             product_links.append(link)
#             data_variant = product_element.find("span", class_="smartwishlist").get("data-variant")
#             data_variants.append(data_variant)
#
#     with open('one_product_motoarena.csv', 'w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerow(['url', 'data-variant'])
#         for link, variant in zip(product_links, data_variants):
#             writer.writerow([link, variant])
#
#     print("Ссылки на товары и значения data-variant были успешно записаны в файл 'one_product_motoarena.csv'.")
#
# main(base_url)
