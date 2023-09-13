import csv
import re
import textwrap
import requests
from bs4 import BeautifulSoup

# Открываем файл с URL-ссылками для чтения
with open('../urls_csv/urls_new_arrival_men.csv', 'r', encoding='utf-8') as file:
    # Открываем файл CSV и записываем заголовки один раз перед циклом
    with open("../done_csv/product_data.csv", "w", newline="", encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile)
        # Записываем заголовки
        csvwriter.writerow(["Title", "Price", "Colors", "Size", "Description", "URL- image", 'id'])

    # Итерируемся по строкам файла
    for line in csv.DictReader(file):
        # Получаем URL-ссылку из текущей строки
        url = line['url']

        # Загружаем страницу и создаем объект Soup для каждой URL-ссылки
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Парсинг заголовка (title)
        title_element = soup.find("h1", class_="product-meta__title heading h3")
        title = title_element.text.strip() if title_element else "Заголовок не найден"

        # Парсинг цены
        price_element = soup.find("span", class_="price")
        price = price_element.text.strip() if price_element else "Цена не найдена"
        price = price.replace("Sale price₹", "").strip()

        # Находим все элементы с классом "pl-swatches__link" и извлекаем их атрибут "aria-label"
        aria_labels = [a['aria-label'] for a in soup.find_all('a', class_='pl-swatches__link')]

        # Находим элементы <input> с классом "block-swatch__radio" и извлекаем их атрибут "value"
        input_elements = soup.find_all('input', class_='block-swatch__radio')

        # Создаем список для хранения значений атрибута "value"
        values = [input_element['value'] for input_element in input_elements]

        # Находим элемент <div> с классом "product-tabs__tab-item-content" и извлекаем его текст
        div_element = soup.find('div', class_='product-tabs__tab-item-content')

        # Извлекаем весь текст из элемента
        all_text = div_element.get_text()

        # Попытка найти элемент с id "product-7218630098992-content"
        product_content = soup.find('div', {'id': 'product-7218630098992-content'})

        # Проверяем, найден ли элемент
        if product_content:
            # Находим все текстовые элементы внутри элемента
            text_elements = product_content.find_all('div', {'class': 'product-tabs__tab-item-content'})

            # Извлекаем и печатаем текст с переносом слов
            wrapped_texts = []
            for element in text_elements:
                text = element.get_text()
                # Разбиваем текст на строки с максимальной шириной 100 символов
                wrapped_text = textwrap.fill(text, width=100)
                wrapped_texts.append(wrapped_text)
        else:
            # Если элемент не найден, устанавливаем значение по умолчанию или выполняем другие действия
            wrapped_texts = ["Текст не найден"]

        # Продолжаем обработку wrapped_texts и других данных

        # Находим все элементы с классом 'product__media-item'
        media_items = soup.find_all('div', {'class': 'product__media-item'})

        # Создаем список для хранения URL-адресов изображений
        image_urls = []

        # Итерируемся по найденным элементам и извлекаем URL-адреса изображений
        for media_item in media_items:
            image_tag = media_item.find('img')
            if image_tag:
                image_url = image_tag.get('src')
                # Убираем лишние слеши из URL-адреса
                if image_url.startswith('//'):
                    image_url = image_url[2:]
                image_urls.append(image_url)

        # Ищем элемент с атрибутом data-media-id
        img_element = soup.find(attrs={"data-media-id": True})

        # Проверяем, найден ли элемент
        if img_element:
            # Получаем значение атрибута data-media-id
            data_media_id = img_element['data-media-id']

            # Используем регулярное выражение для извлечения только цифр
            digits = re.search(r'\d+', data_media_id)

            if digits:
                digits_value = digits.group()
                print("Значение атрибута data-media-id (только цифры):", digits_value)
            else:
                print("Цифры в атрибуте data-media-id не найдены.")
        else:
            print("Элемент с атрибутом data-media-id не найден.")

        # Открываем файл CSV и записываем данные
        with open("../done_csv/product_data.csv", "a", newline="", encoding="utf-8") as csvfile:
            csvwriter = csv.writer(csvfile)
            # Записываем данные
            csvwriter.writerow(
                [title, price, ', '.join(aria_labels), ', '.join(values), all_text, '\n'.join(image_urls), digits_value])

        print("Данные сохранены в product_data.csv")
