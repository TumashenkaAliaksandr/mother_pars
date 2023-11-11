import requests
from bs4 import BeautifulSoup

# Загружаем HTML-код страницы
url = "https://www.urbanmonkey.com/collections/cargo-pants/products/adventure-cargo-pants-3?variant=47123611484441&?section_title=&?section_id=&?location_id=1"
response = requests.get(url)
html_content = response.text
soup = BeautifulSoup(html_content, "html.parser")
# Находим элемент с классом "t4s-tab-wrapper"
tab_wrappers = soup.find_all("div", class_="t4s-tab-wrapper")

# Создаем словарь для хранения текста из каждой вкладки
tab_texts = {}

# Проходим по каждому элементу вкладки
for tab_wrapper in tab_wrappers:
    # Находим заголовок вкладки
    tab_title = tab_wrapper.find("span", class_="t4s-tab__text").text.strip()

    # Находим текст вкладки
    tab_content = tab_wrapper.find("div", class_="t4s-tab-content").text.strip()

    # Добавляем заголовок и текст в словарь
    tab_texts[tab_title] = tab_content

# Теперь у вас есть доступ к тексту из каждой вкладки по заголовку
core_features_text = tab_texts.get("core features", "")
description_text = tab_texts.get("description", "")
shipping_returns_text = tab_texts.get("shipping & returns", "")
care_guide_text = tab_texts.get("care guide", "")

# Выводим текст из каждой вкладки
print("Core Features:")
print(core_features_text)

print("Description:")
print(description_text)

print("Shipping & Returns:")
print(shipping_returns_text)

print("Care Guide:")
print(care_guide_text)

# import requests
# from bs4 import BeautifulSoup
# import csv
#
# base_url = "https://www.urbanmonkey.com/collections/cargo-pants.html?variant="
# page_num = 1
# links = []
#
# while True:
#     url = base_url + str(page_num)
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, "html.parser")
#
#     product_divs = soup.find_all("div", class_="t4s-product-btns")
#
#     for div in product_divs:
#         link = div.find("a")["href"]
#         links.append('https://www.urbanmonkey.com/collections/cargo-pants' + link)
#
#     next_link = soup.find("a", class_="next")
#     if not next_link:
#         break
#
#     page_num += 1
#
# with open("urls_csv/urls_urban_monkey.csv", "w", newline="") as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(["url"])
#     for link in links:
#         writer.writerow([link])
#
# print("Ссылки на товары успешно записаны в файл urls_urban_monkey.csv.")
