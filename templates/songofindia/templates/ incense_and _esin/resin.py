import time, re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import csv
import textwrap
import os

# Функция для сохранения данных в файл CSV
def save_to_csv(title, category, subcategory, price, description, description_all, main_image_url, all_image_urls, product_id):
    with open(csv_file_path, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        # Записываем данные в строку CSV файла
        writer.writerow([title, category, subcategory, price, description, description_all, main_image_url, ', '.join(all_image_urls), product_id])

# Путь к файлу CSV
csv_file_path = "../../done_csv/resin.csv"

# Проверяем, существует ли файл или пустой ли он
if not os.path.exists(csv_file_path) or os.path.getsize(csv_file_path) == 0:
    with open(csv_file_path, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        header = ["Title", "Category", "Subcategory", "Price", "Description", "Description_All", "Main_Image_URL", "All_Image_URLs", "Product_ID"]
        writer.writerow(header)

# Путь к драйверу Chrome (загрузите драйвер, совместимый с вашей версией Chrome)
chrome_driver_path = "webdrivers\chromedriver.exe"

# Создаем экземпляр объекта Service
service = ChromeService(executable_path=chrome_driver_path)

# Создаем объект ChromeOptions
chrome_options = ChromeOptions()
chrome_options.add_argument("--headless")  # Запускаем в безголовом режиме (без открытия окна браузера)

# Создаем экземпляр браузера Chrome
driver = webdriver.Chrome(service=service, options=chrome_options)

with open('../../urls_csv/urls_resin.csv', 'r', encoding='utf-8') as file:
    for line in csv.DictReader(file):
        url = line['url']

        # Загружаем страницу с помощью Selenium
        driver.get(url)

        # Ждем некоторое время, чтобы страница полностью загрузилась (при необходимости увеличьте время)
        time.sleep(2)

        # Получаем содержимое страницы после выполнения JavaScript
        page_content = driver.page_source

        # Создаем объект BeautifulSoup для парсинга HTML-контента
        soup = BeautifulSoup(page_content, "html.parser")

        # Найти заголовок товара
        title = soup.find("h1", class_="page-title").text.strip()
        print('Title: ', title)

        # Найти категорию товара
        category = 'Home Fragrance'
        print('Category: ', category)

        subcategory = 'Resin Grain'
        print('Subcategory:', subcategory)

        # Найти цену товара
        price = soup.find("span", class_="price").text.replace('₹', '').strip()
        print('Price: ', price)

        # Найти описание товара
        description_element = soup.find("div", class_="product attribute overview")
        if description_element:
            description_value = description_element.find("div", class_="value")
            if description_value:
                description = description_value.text.strip()
                wrapped_description = textwrap.fill(description, width=100, break_long_words=False)
                print('Descriptions: ', wrapped_description)
            else:
                description = ""
                print(" ")
        else:
            description = ""
            print(" ")


        # Итерироваться по строкам таблицы и собрать текст из всех ячеек в одну переменную
        table = soup.find("table", id="product-attribute-specs-table")
        description_all = ""
        if table:
            rows = table.find_all("tr")
            for row in rows:
                # Найти теги <th> и <td> внутри строки
                th_tags = row.find_all(["th", "td"])

                # Извлечь текст из тегов <th> и <td> с выполнением переноса слов
                for tag in th_tags:
                    text = tag.text.strip()
                    wrapped_text = textwrap.fill(text, width=100, break_long_words=False)
                    description_all += wrapped_text + "\n"
                    print(wrapped_text)
                print()
        else:
            print(" ")

        # Находим тег div с классом "fotorama__stage__frame" (предполагаем, что это главное фото товара)
        main_image_tag = soup.find("div", class_="fotorama__stage__frame")

        if main_image_tag:
            # Получаем ссылку на фото из атрибута "href" или "src" тега "img"
            img_tag = main_image_tag.find("img")
            if img_tag:
                main_image_url = img_tag.get("href") or img_tag.get("src")
                print("Ссылка на главное фото товара:", main_image_url)
            else:
                main_image_url = " "
        else:
            main_image_url = " "

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
                product_id = " "
        else:
            product_id = " "

        # После обработки страницы, сохраняем данные в файл CSV
        save_to_csv(title, category, subcategory, price, description, description_all, main_image_url, all_large_or_medium_image_urls, product_id)

# Закрываем браузер
driver.quit()
