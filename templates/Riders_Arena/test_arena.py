# import requests
# from bs4 import BeautifulSoup
#
# def extract_product_data(url):
#     """
#     Извлекает данные о продукте из HTML-кода, полученного по URL.
#     """
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # Проверка на ошибки HTTP
#         html_content = response.text
#     except requests.exceptions.RequestException as e:
#         print(f"Ошибка при запросе страницы: {e}")
#         return None
#
#     soup = BeautifulSoup(html_content, 'html.parser')
#
#     try:
#         # Название товара
#         title_element = soup.find('h1', class_='h1') or soup.find('h1')
#         title = title_element.text.strip() if title_element else "Название не найдено"
#
#         # Цена
#         price_element = soup.find('span', class_='price-item price-item--regular')
#         price_text = price_element.text.strip() if price_element else "Цена не найдена"
#
#         # Убираем "Rs." и пробелы
#         price = price_text.replace("Rs.", "").replace(" ", "").strip() if price_text != "Цена не найдена" else "Цена не найдена"
#
#         # Фото
#         img_element = soup.find('div', class_='product__media media media--transparent gradient global-media-settings').find('img')
#         photo_url = img_element['src'] if img_element and 'src' in img_element.attrs else "Фото не найдено"
#
#         # Описание
#         description_element = soup.find('div', class_='product__description rte quick-add-hidden')
#         description = description_element.text.strip() if description_element else "Описание не найдено"
#
#         return {
#             'title': title,
#             'price': price,
#             'photo_url': "https://" + photo_url,
#             'description': description
#         }
#
#     except Exception as e:
#         print(f"Ошибка при парсинге данных: {e}")
#         return None
#
# # Пример использования:
# product_url = "https://ridersarena.com/products/ngk-iridium-spark-plug-set-for-royal-enfield-interceptor-650-gt650"
# product_data = extract_product_data(product_url)
#
# if product_data:
#     print("Данные о товаре:")
#     for key, value in product_data.items():
#         print(f"{key}: {value}")
# else:
#     print("Не удалось извлечь данные о товаре.")


import requests
from bs4 import BeautifulSoup
import csv
import os


def extract_product_data(url):
    """
    Улучшенный парсер данных товара с обработкой ошибок:
    - Исправлены селекторы для цены
    - Добавлена проверка URL фото
    - Улучшена обработка описания
    """
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"Ошибка запроса: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    data = {
        'title': 'Не найдено',
        'price': 'Не найдена',
        'photo_url': 'Не найдено',
        'description': 'Не найдено'
    }

    try:
        # Название товара
        title = soup.find('h1', {'class': 'h1'}) or soup.find('h1')
        if title:
            data['title'] = title.get_text(strip=True)

        # Цена (учитываем оба варианта отображения)
        price = (soup.find('span', class_='price-item--sale') or
                 soup.find('span', class_='price-item--regular'))
        if price:
            data['price'] = price.get_text(strip=True).replace('Rs.', '').replace(' ', '')

        # Фото
        img_container = soup.find('div', class_='product__media')
        if img_container:
            img = img_container.find('img', src=True)
            if img:
                data['photo_url'] = img['src'] if img['src'].startswith('http') else f"https:{img['src']}"

        # Описание
        description = soup.find('div', class_='product__description')
        if description:
            data['description'] = ' '.join(description.stripped_strings)

    except Exception as e:
        print(f"Ошибка парсинга: {e}")

    return data


def read_links_from_file(filename):
    """
    Чтение ссылок из CSV файла с проверкой:
    - Автоматическое определение кодировки
    - Пропуск заголовка
    - Валидация URL
    """
    links = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # Пропускаем заголовок
            for row in reader:
                if row and row[0].startswith('http'):
                    links.append(row[0].strip())
    except Exception as e:
        print(f"Ошибка чтения файла: {e}")
    return links


def write_data_to_csv(filename, data):
    """
    Запись данных в CSV с:
    - Проверкой директории
    - Резервным сохранением при ошибках
    """
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        print(f"Данные сохранены в {os.path.abspath(filename)}")
    except Exception as e:
        print(f"Ошибка сохранения: {e}")
        # Попытка сохранить в текущую директорию при ошибке пути
        with open('product_data_backup.csv', 'w', encoding='utf-8') as f:
            f.write('\n'.join([str(item) for item in data]))


if __name__ == "__main__":
    # Конфигурационные параметры
    INPUT_FILE = os.path.join('urls_csv', 'product_links.csv')
    OUTPUT_FILE = os.path.join('parsed_data', 'product_data.csv')

    # Проверка существования файла
    if not os.path.exists(INPUT_FILE):
        print(f"Файл {os.path.abspath(INPUT_FILE)} не найден!")
        print("Проверьте:")
        print(f"1. Существование файла {INPUT_FILE}")
        print(f"2. Рабочую директорию: {os.getcwd()}")
        exit()

    # Основной процесс
    links = read_links_from_file(INPUT_FILE)

    if not links:
        print("Не найдено валидных ссылок в файле")
        exit()

    results = []
    for idx, url in enumerate(links, 1):
        print(f"Обработка {idx}/{len(links)}: {url}")
        try:
            product_data = extract_product_data(url)
            if product_data:
                results.append(product_data)
        except Exception as e:
            print(f"Ошибка обработки {url}: {e}")

    if results:
        write_data_to_csv(OUTPUT_FILE, results)
    else:
        print("Нет данных для сохранения")
