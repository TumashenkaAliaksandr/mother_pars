# import requests
# from bs4 import BeautifulSoup
# import csv
#
# url = "https://www.songofindia.co.in/index.php/home-fragrances/reeds-diffuser.html"
# response = requests.get(url)
#
# soup = BeautifulSoup(response.content, "html.parser")
#
# product_divs = soup.find_all("div", class_="product photo product-item-photo")
#
# links = []
#
# for div in product_divs:
#     link = div.find("a")["href"]
#     links.append(link)
#
# with open("products.csv", "w", newline="") as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(["Ссылка на товар"])
#     for link in links:
#         writer.writerow([link])
#
# print("Ссылки на товары успешно записаны в файл products.csv.")


# import requests
# from bs4 import BeautifulSoup
# import csv
#
# base_url = "https://www.songofindia.co.in/index.php/home-fragrances/reeds-diffuser.html?p="
# page_num = 1
# links = []
#
# while True:
#     url = base_url + str(page_num)
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, "html.parser")
#
#     product_divs = soup.find_all("div", class_="product-item-info")
#
#     for div in product_divs:
#         link = div.find("a")["href"]
#         links.append(link)
#
#     next_link = soup.find("a", class_="next")
#     if not next_link:
#         break
#
#     page_num += 1
#
# with open("products.csv", "w", newline="") as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(["Ссылка на товар"])
#     for link in links:
#         writer.writerow([link])
#
# print("Ссылки на товары успешно записаны в файл products.csv.")
#
# from bs4 import BeautifulSoup
#
# import requests
# from bs4 import BeautifulSoup
#
# # Ссылка на страницу с товаром
# url = "https://www.songofindia.co.in/index.php/mysore-chandan-sandalwood-organic-ambience-diffuser-with-reeds.html"
#
# # Получаем HTML-код страницы
# response = requests.get(url)
# html_content = response.text
#
# # Создаем объект BeautifulSoup для парсинга HTML
# soup = BeautifulSoup(html_content, "html.parser")
#
# # Находим указанный блок
# div_block = soup.find("div", {"class": "fotorama__stage__frame"})
#
# # Проверяем, что блок найден
# if div_block is not None:
#     # Извлекаем значение атрибута href
#     href = div_block.get("href")
#
#     # Извлекаем значение атрибута id
#     div_id = div_block.find("div", {"class": "fotorama__caption__wrap"}).get("id")
#
#     # Выводим результаты
#     print("Href:", href)
#     print("ID:", div_id)
# else:
#     print("Блок не найден.")
# from bs4 import BeautifulSoup
#
# import requests
# from bs4 import BeautifulSoup
#
# # Ссылка на страницу с товаром
# url = "https://www.songofindia.co.in/index.php/mysore-chandan-sandalwood-organic-ambience-diffuser-with-reeds.html"
#
# # Получаем HTML-код страницы
# response = requests.get(url)
# html_content = response.text
#
# # Создаем объект BeautifulSoup для парсинга HTML
# soup = BeautifulSoup(html_content, "html.parser")
#
# # Найти элемент с классом "fotorama__stage__shaft"
# shaft_element = soup.find('div', class_='fotorama__stage__shaft')
#
# if shaft_element is not None:
#     # Найти все элементы с классом "fotorama__stage__frame" внутри элемента "shaft_element"
#     frame_elements = shaft_element.find_all('div', class_='fotorama__stage__frame')
#
#     # Получить значения атрибута "src" изображений внутри каждого элемента "frame_element"
#     src_values = [frame.find('img', class_='fotorama__img--full').get('src') for frame in frame_elements]
#
#     # Вывести результаты
#     print('src values:', src_values)
# else:
#     print("Элемент 'fotorama__stage__shaft' не найден.")
#
#
#
#
# import requests
# from lxml import html
#
# # Ссылка на страницу с товаром
# url = "https://www.songofindia.co.in/index.php/mysore-chandan-sandalwood-organic-ambience-diffuser-with-reeds.html"
#
# # Получаем HTML-код страницы
# response = requests.get(url)
# html_content = response.content
#
# # Создаем объект ElementTree для парсинга HTML с помощью lxml
# tree = html.fromstring(html_content)
#
# # Найти элемент с классом "fotorama__stage__shaft"
# shaft_element = tree.xpath('//div[@class="fotorama__stage__shaft"]')
#
# if shaft_element:
#     # Найти все элементы с классом "fotorama__stage__frame" внутри элемента "shaft_element"
#     frame_elements = shaft_element[0].findall('.//div[@class="fotorama__stage__frame"]')
#
#     # Получить значения атрибута "src" изображений внутри каждого элемента "frame_element"
#     src_values = [frame.find('img').get('src') for frame in frame_elements]
#
#     # Вывести результаты
#     print('src values:', src_values)
# else:
#     print("Элемент 'fotorama__stage__shaft' не найден.")
#
# import time, re
# import requests
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.chrome.options import Options as ChromeOptions
# from bs4 import BeautifulSoup
# from PIL import Image
# from io import BytesIO
#
# # Путь к драйверу Chrome (загрузите драйвер, совместимый с вашей версией Chrome)
# chrome_driver_path = "путь_к_драйверу_chrome"
#
# # Создаем экземпляр объекта Service
# service = ChromeService(executable_path=chrome_driver_path)
#
# # Создаем объект ChromeOptions
# chrome_options = ChromeOptions()
# chrome_options.add_argument("--headless")  # Запускаем в безголовом режиме (без открытия окна браузера)
#
# # Создаем экземпляр браузера Chrome
# driver = webdriver.Chrome(service=service, options=chrome_options)
#
# url = "https://www.songofindia.co.in/index.php/mysore-chandan-sandalwood-organic-ambience-diffuser-with-reeds.html"
#
# # Загружаем страницу с помощью Selenium
# driver.get(url)
#
# # Ждем некоторое время, чтобы страница полностью загрузилась (при необходимости увеличьте время)
# time.sleep(5)
#
# # Получаем содержимое страницы после выполнения JavaScript
# page_content = driver.page_source
#
# # Закрываем браузер
# driver.quit()
#
# # Создаем объект BeautifulSoup для парсинга HTML-контента
# soup = BeautifulSoup(page_content, "html.parser")
#
# # Находим тег div с классом "fotorama__stage__frame" (предполагаем, что это главное фото товара)
# main_image_tag = soup.find("div", class_="fotorama__stage__frame")
#
# if main_image_tag:
#     # Получаем ссылку на фото из атрибута "href" или "src" тега "img"
#     img_tag = main_image_tag.find("img")
#     if img_tag:
#         main_image_url = img_tag.get("href") or img_tag.get("src")
#         print("Ссылка на главное фото товара:", main_image_url)
#     else:
#         print("Ссылка на фото товара не найдена.")
# else:
#     print("Главное фото товара не найдено.")
#
# # Продолжение кода после получения главной фото
#
# # Находим все теги img с классом "fotorama__img"
# all_image_tags = soup.find_all("img", class_="fotorama__img")
#
# # Создаем список для хранения всех ссылок на фотографии большего или среднего размера
# all_large_or_medium_image_urls = []
#
# # Извлекаем ссылки на фотографии из атрибутов "data-full", "data-zoom-image", "src" или "href"
# for image_tag in all_image_tags:
#     image_url = None
#     for attr in ["data-full", "data-zoom-image", "src", "href"]:
#         image_url = image_tag.get(attr)
#         if image_url:
#             break
#     if image_url:
#         # Получаем размер изображения
#         try:
#             response = requests.get(image_url)
#             image = Image.open(BytesIO(response.content))
#             width, height = image.size
#         except Exception as e:
#             width, height = 0, 0
#
#         # Проверяем размер изображения (настройте пороговое значение по вашему усмотрению)
#         if width >= 300 and height >= 300:
#             all_large_or_medium_image_urls.append(image_url)
#
# # Выводим список ссылок на фотографии большего или среднего размера товара
# print("Ссылки на фото товара большего или среднего размера:")
# for image_url in all_large_or_medium_image_urls:
#     print(image_url)
#
# # Находим тег div с классом "fotorama__caption__wrap"
# caption_wrap_div = soup.find("div", class_="fotorama__caption__wrap")
#
# if caption_wrap_div:
#     # Получаем значение атрибута "id"
#     caption_id = caption_wrap_div.get("id")
#
#     # Используем регулярное выражение для извлечения только цифр из значения ID
#     # Если ID не содержит цифр, вернется None
#     product_id = re.findall(r'\d+', caption_id)
#     if product_id:
#         # Если нашли цифры, возьмем первое значение (так как re.findall() возвращает список найденных совпадений)
#         product_id = product_id[0]
#         print("ID товара:", product_id)
#     else:
#         print("ID товара не найден.")
# else:
#     print("Тег с классом 'fotorama__caption__wrap' не найден.")
#------------------------------------------------------------------


import time, re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import csv


# Функция для сохранения данных в файл CSV
def save_to_csv(title, main_image_url, all_image_urls, product_id):
    with open("product_info.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Title", "Main Image URL", "Other Image URLs", "ID"])

        # Записываем данные в строку CSV файла
        writer.writerow([title, main_image_url, ', '.join(all_image_urls), product_id])

    print("Информация о товаре успешно записана в файл product_info.csv.")

# Путь к драйверу Chrome (загрузите драйвер, совместимый с вашей версией Chrome)
chrome_driver_path = "путь_к_драйверу_chrome"

# Создаем экземпляр объекта Service
service = ChromeService(executable_path=chrome_driver_path)

# Создаем объект ChromeOptions
chrome_options = ChromeOptions()
chrome_options.add_argument("--headless")  # Запускаем в безголовом режиме (без открытия окна браузера)

# Создаем экземпляр браузера Chrome
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://www.songofindia.co.in/index.php/mysore-chandan-sandalwood-organic-ambience-diffuser-with-reeds.html"

# Загружаем страницу с помощью Selenium
driver.get(url)

# Ждем некоторое время, чтобы страница полностью загрузилась (при необходимости увеличьте время)
time.sleep(3)

# Получаем содержимое страницы после выполнения JavaScript
page_content = driver.page_source

# Закрываем браузер
driver.quit()

# Создаем объект BeautifulSoup для парсинга HTML-контента
soup = BeautifulSoup(page_content, "html.parser")

# Найти заголовок товара
title = soup.find("h1", class_="page-title").text.strip()
print('Title: ', title)

# Находим тег div с классом "fotorama__stage__frame" (предполагаем, что это главное фото товара)
main_image_tag = soup.find("div", class_="fotorama__stage__frame")

if main_image_tag:
    # Получаем ссылку на фото из атрибута "href" или "src" тега "img"
    img_tag = main_image_tag.find("img")
    if img_tag:
        main_image_url = img_tag.get("href") or img_tag.get("src")
        print("Ссылка на главное фото товара:", main_image_url)
    else:
        main_image_url = "Ссылка на фото товара не найдена."
else:
    main_image_url = "Главное фото товара не найдено."

# Продолжение кода после получения главного фото

# Находим все теги img с классом "fotorama__img"
all_image_tags = soup.find_all("img", class_="fotorama__img")

# Создаем список для хранения всех ссылок на фотографии большего или среднего размера
all_large_or_medium_image_urls = []

# Извлекаем ссылки на фотографии из атрибутов "data-full", "data-zoom-image", "src" или "href"
for image_tag in all_image_tags:
    image_url = None
    for attr in ["data-full", "data-zoom-image", "src", "href"]:
        image_url = image_tag.get(attr)
        if image_url:
            break
    if image_url:
        # Получаем размер изображения
        try:
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            width, height = image.size
        except Exception as e:
            width, height = 0, 0

        # Проверяем размер изображения (настройте пороговое значение по вашему усмотрению)
        if width >= 300 and height >= 300:
            all_large_or_medium_image_urls.append(image_url)

# Выводим список ссылок на фотографии большего или среднего размера товара
print("Ссылки на фото товара большего или среднего размера:")
for image_url in all_large_or_medium_image_urls:
    print(image_url)

# Находим тег div с классом "fotorama__caption__wrap"
caption_wrap_div = soup.find("div", class_="fotorama__caption__wrap")

if caption_wrap_div:
    # Получаем значение атрибута "id"
    caption_id = caption_wrap_div.get("id")

    # Используем регулярное выражение для извлечения только цифр из значения ID
    # Если ID не содержит цифр, вернется None
    product_id = re.findall(r'\d+', caption_id)
    if product_id:
        # Если нашли цифры, возьмем первое значение (так как re.findall() возвращает список найденных совпадений)
        product_id = product_id[0]
        print("ID товара:", product_id)
    else:
        product_id = "ID товара не найден."
else:
    product_id = "Тег с классом 'fotorama__caption__wrap' не найден."

# Сохраняем данные в файл CSV
save_to_csv(title, main_image_url, all_large_or_medium_image_urls, product_id)


#------------------------------------------------------------------
#
# import time
# import requests
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.chrome.options import Options as ChromeOptions
# from PIL import Image
# from io import BytesIO
# import csv
# import textwrap
# import re
#
# def extract_product_info(url):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, "html.parser")
#
#     # Найти заголовок товара
#     title = soup.find("h1", class_="page-title").text.strip()
#     print('Title: ', title)
#
#     # Найти категорию товара
#     category = 'Home Fragrance | Room Diffuser'
#     print('Category: ', category)
#
#     # Найти цену товара
#     price = soup.find("span", class_="price").text.replace('₹', '').strip()
#     print('Price: ', price)
#
#     # Найти описание товара
#     description = soup.find("div", class_="product attribute overview").find("div", class_="value").text.strip()
#     wrapped_description = textwrap.fill(description, width=100, break_long_words=False)
#     print('Descriptions: ', wrapped_description)
#
#     # Найти таблицу с атрибутом id="product-attribute-specs-table"
#     table = soup.find("table", id="product-attribute-specs-table")
#
#     # Найти заголовок таблицы
#     caption = table.find("caption", class_="table-caption").text.strip()
#     print("Table Caption:", caption)
#
#     # Итерироваться по строкам таблицы и собрать текст из всех ячеек в одну переменную
#     description_all = ""
#     rows = table.find_all("tr")
#     for row in rows:
#         # Найти теги <th> и <td> внутри строки
#         th_tags = row.find_all(["th", "td"])
#
#         # Извлечь текст из тегов <th> и <td> с выполнением переноса слов
#         for tag in th_tags:
#             text = tag.text.strip()
#             wrapped_text = textwrap.fill(text, width=100, break_long_words=False)
#             description_all += wrapped_text + "\n"
#             print(wrapped_text)
#         print()
#
#     # Находим тег div с классом "fotorama__caption__wrap"
#     caption_wrap_div = soup.find("div", class_="fotorama__caption__wrap")
#
#
#     if caption_wrap_div:
#         # Получаем значение атрибута "id"
#         caption_id = caption_wrap_div.get("id")
#
#         # Используем регулярное выражение для извлечения только цифр из значения ID
#         # Если ID не содержит цифр, вернется None
#         product_id = re.findall(r'\d+', caption_id)
#         if product_id:
#             # Если нашли цифры, возьмем первое значение (так как re.findall() возвращает список найденных совпадений)
#             product_id = product_id[0]
#             print("ID товара:", product_id)
#         else:
#             print("ID товара не найден.")
#             # Устанавливаем значение по умолчанию, если ID не найден
#             product_id = "N/A"
#     else:
#         print("Тег с классом 'fotorama__caption__wrap' не найден.")
#         # Устанавливаем значение по умолчанию, если тег не найден
#         product_id = "N/A"
#
#     return title, category, price, wrapped_description, description_all, product_id
#
# def extract_photos_and_product_id(url):
#     # Путь к драйверу Chrome (замените на путь к скаченному драйверу)
#     chrome_driver_path = "путь_к_скаченному_драйверу_chrome"
#
#     # Создаем экземпляр объекта Service
#     service = ChromeService(executable_path=chrome_driver_path)
#
#     # Создаем объект ChromeOptions
#     chrome_options = ChromeOptions()
#     chrome_options.add_argument("--headless")  # Запускаем в безголовом режиме (без открытия окна браузера)
#
#     # Создаем экземпляр браузера Chrome
#     driver = webdriver.Chrome(service=service, options=chrome_options)
#
#     # Загружаем страницу с помощью Selenium
#     driver.get(url)
#
#     # Ждем некоторое время, чтобы страница полностью загрузилась (при необходимости увеличьте время)
#     time.sleep(5)
#
#     # Получаем содержимое страницы после выполнения JavaScript
#     page_content = driver.page_source
#
#     # Закрываем браузер
#     driver.quit()
#
#
#
#     # Создаем объект BeautifulSoup для парсинга HTML-контента
#     soup = BeautifulSoup(page_content, "html.parser")
#
#
#     # Находим тег div с классом "fotorama__stage__frame" (предполагаем, что это главное фото товара)
#     main_image_tag = soup.find("div", class_="fotorama__stage__frame")
#
#     if main_image_tag:
#         # Получаем ссылку на фото из атрибута "href" или "src" тега "img"
#         img_tag = main_image_tag.find("img")
#         if img_tag:
#             main_image_url = img_tag.get("href") or img_tag.get("src")
#             print("Ссылка на главное фото товара:", main_image_url)
#         else:
#             print("Ссылка на фото товара не найдена.")
#     else:
#         print("Главное фото товара не найдено.")
#
#     # Находим все теги img с классом "fotorama__img"
#     all_image_tags = soup.find_all("img", class_="fotorama__img")
#
#     # Создаем список для хранения всех ссылок на фотографии большего или среднего размера
#     all_large_or_medium_image_urls = []
#
#     # Извлекаем ссылки на фотографии из атрибутов "data-full", "data-zoom-image", "src" или "href"
#     for image_tag in all_image_tags:
#         image_url = None
#         for attr in ["data-full", "data-zoom-image", "src", "href"]:
#             image_url = image_tag.get(attr)
#             if image_url:
#                 # Получаем размер изображения
#                 try:
#                     response = requests.get(image_url)
#                     image = Image.open(BytesIO(response.content))
#                     width, height = image.size
#                 except Exception as e:
#                     width, height = 0, 0
#
#                 # Проверяем размер изображения (настройте пороговое значение по вашему усмотрению)
#                 if width >= 300 and height >= 300:
#                     all_large_or_medium_image_urls.append(image_url)
#                 break
#     return main_image_url, all_large_or_medium_image_urls
#
#
#
# def main():
#     url = "https://www.songofindia.co.in/index.php/mysore-chandan-sandalwood-organic-ambience-diffuser-with-reeds.html"
#
#     # Извлекаем информацию о продукте (название, категория, цена, описание, идентификатор товара)
#     title, category, price, wrapped_description, description_all, product_id = extract_product_info(url)
#
#     # Извлекаем ссылку на главное фото товара и список фотографий большего или среднего размера
#     main_image_url, all_large_or_medium_image_urls = extract_photos_and_product_id(url)
#
#     # Записать данные в файл CSV
#     with open("product_info.csv", "w", newline="", encoding="utf-8") as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(["Title", "Price", "Main Image URL", "Other Image URLs", "Description", "Description_all", "Category", "Product ID"])
#
#         # Записываем данные в строку CSV файла
#         writer.writerow([title, price, main_image_url, ', '.join(all_large_or_medium_image_urls), wrapped_description, description_all, category, product_id])
#
#     print("Информация о товаре успешно записана в файл product_info.csv.")
#
# if __name__ == "__main__":
#     main()
