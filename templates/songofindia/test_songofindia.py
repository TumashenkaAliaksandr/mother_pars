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

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from bs4 import BeautifulSoup

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
time.sleep(5)

# Получаем содержимое страницы после выполнения JavaScript
page_content = driver.page_source

# Закрываем браузер
driver.quit()

# Создаем объект BeautifulSoup для парсинга HTML-контента
soup = BeautifulSoup(page_content, "html.parser")

# Находим тег div с классом "fotorama__stage__frame" (предполагаем, что это главное фото товара)
main_image_tag = soup.find("div", class_="fotorama__stage__frame")

if main_image_tag:
    # Получаем значение атрибута "id"
    image_id = main_image_tag.get("id")
    print("ID главного фото товара:", image_id)

    # Получаем ссылку на фото из атрибута "href" или "src" тега "img"
    img_tag = main_image_tag.find("img")
    if img_tag:
        main_image_url = img_tag.get("href") or img_tag.get("src")
        print("Ссылка на главное фото товара:", main_image_url)
    else:
        print("Ссылка на фото товара не найдена.")
else:
    print("Главное фото товара не найдено.")
