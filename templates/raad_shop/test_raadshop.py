# import requests
# from bs4 import BeautifulSoup
# import csv
#
# base_url = "https://raadshop.com/collections/high-tops?page="
# page_num = 1
# links = []
#
# while True:
#     url = base_url + str(page_num)
#     response = requests.get(url)
#
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#
#         # Находим все теги <a> с классом 'product-card'
#         product_links = soup.find_all('a', class_='product-card')
#
#         if product_links:
#             # Собираем все ссылки на товары
#             all_product_urls = ['https://raadshop.com' + link['href'] for link in product_links]
#             links.extend(all_product_urls)
#         else:
#             break
#
#         page_num += 1
#     else:
#         print(f"Не удалось получить страницу {url}")
#         break
#
# with open("product_links.csv", "w", newline="", encoding='utf-8') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(["url"])
#     for link in links:
#         writer.writerow([link])
#
# print("Ссылки на товары успешно записаны в файл product_links.csv.")


import requests
from bs4 import BeautifulSoup

product_url = 'https://raadshop.com/products/hightop-samouraiandredflowers00168'

response = requests.get(product_url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим ссылку на товар
    product_link = soup.find('link', rel='canonical')

    if product_link:
        print("Ссылка на товар:", product_link['href'])
    else:
        print("Ссылка на товар не найдена")
else:
    print("Не удалось получить страницу товара")
