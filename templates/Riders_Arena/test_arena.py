import requests
from bs4 import BeautifulSoup
import re
import csv
import random


def extract_product_data(url):
    """
    Извлекает данные о продукте из HTML-кода, полученного по URL.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки HTTP
        html_content = response.text
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе страницы: {e}")
        return None

    soup = BeautifulSoup(html_content, 'html.parser')

    product_data = {
        'id': random.randint(1000000, 9999999),  # Рандомный ID
        'product_url': url,  # Ссылка на продукт
        'title': "Название не найдено",
        'price': "Цена не найдена",
        'photo_url': "Фото не найдено",
        'description': "Описание не найдено",
        'sizes': [],
        'colors': [],
        'additional_images': [],
        'brand': "Бренд не найден"
    }

    try:
        # Название товара
        title_element = soup.find('h1', class_='h1') or soup.find('h1')
        if title_element:
            product_data['title'] = title_element.text.strip()

        # Цена
        price_container = soup.find('div', class_='price__container')
        if price_container:
            regular_price_element = price_container.find('span', class_='price-item price-item--regular')
            sale_price_element = price_container.find('span', class_='price-item price-item--sale')

            if regular_price_element and regular_price_element.text.strip():
                product_data['price'] = regular_price_element.text.strip().replace("Rs.", "").replace(",", "").strip()
            elif sale_price_element and sale_price_element.text.strip():
                product_data['price'] = sale_price_element.text.strip().replace("Rs.", "").replace(",", "").strip()
            else:
                print("Цена не найдена.")
        else:
            print("Цена не найдена.")

        # Фото (основное)
        img_element = soup.find('div', class_='product__media').find('img') if soup.find('div', class_='product__media') else None
        if img_element and 'srcset' in img_element.attrs:
            srcset = img_element['srcset'].split(',')
            best_image_url = max((s.split()[0].strip() for s in srcset), default='')
            product_data['photo_url'] = "https:" + best_image_url if not best_image_url.startswith('http') and best_image_url else best_image_url
        elif img_element and 'src' in img_element.attrs:
            product_data['photo_url'] = "https:" + img_element['src'] if not img_element['src'].startswith('http') else img_element['src']

        # Описание
        description_element = soup.find('div', class_='product__description')
        if description_element:
            description_text = description_element.text.strip()

            # Удаляем слова или фразы, связанные с доставкой и заметками
            delivery_keywords = ['shipping', 'delivery', 'order confirmation', 'actuals', 'please note']
            for keyword in delivery_keywords:
                description_text = re.sub(rf'(?i){keyword}.*?(?=\.|\n|$)', '', description_text)

            product_data['description'] = description_text.strip()

            # Проверка на бренд в описании
            lines = description_text.split('\n')
            brand_found = False
            for line in lines:
                if 'Brand' in line:
                    parts = line.split(':')
                    if len(parts) > 1:
                        product_data['brand'] = parts[1].strip()
                        brand_found = True
                        break

            if not brand_found:
                # Если бренд не найден, берем все название в качестве бренда
                product_data['brand'] = product_data['title']

        # Размеры
        size_fieldset = soup.find('legend', string='Size')
        if size_fieldset:
            size_parent = size_fieldset.find_parent('fieldset')
            sizes = [input_tag['value'] for input_tag in size_parent.find_all('input', {'name': 'Size'})]
            product_data['sizes'] = sizes if sizes else []

        # Цвета
        color_fieldset = soup.find('legend', string='Color')
        if color_fieldset:
            color_parent = color_fieldset.find_parent('fieldset')
            colors = [input_tag['value'] for input_tag in color_parent.find_all('input', {'name': 'Color'})]
            product_data['colors'] = colors if colors else []

        # Дополнительные изображения
        for li in soup.find_all('li', class_='thumbnail-list__item'):
            img_element = li.find('img')
            if img_element and 'srcset' in img_element.attrs:
                srcset = img_element['srcset'].split(',')
                widths = [int(s.split()[1].replace('w', '')) for s in srcset if len(s.split()) > 1 and 'w' in s.split()[1]]
                max_width_index = widths.index(max(widths)) if widths else -1
                best_image_url = srcset[max_width_index].split()[0].strip() if max_width_index != -1 else ''
                best_image_url = re.sub(r'\?v=\d+&width=\d+', '', best_image_url)
                product_data['additional_images'].append("https:" + best_image_url if not best_image_url.startswith('http') and best_image_url else best_image_url)
            elif img_element and 'src' in img_element.attrs:
                img_src = re.sub(r'\?v=\d+&width=\d+', '', img_element['src'])
                product_data['additional_images'].append("https:" + img_src if not img_src.startswith('http') else img_src)

    except Exception as e:
        print(f"Ошибка при парсинге данных: {e}")

    return product_data


def write_to_csv(filename, data):
    """
    Записывает данные в CSV-файл.
    """
    fieldnames = ['id', 'product_url', 'title', 'price', 'photo_url', 'description', 'sizes', 'colors',
                  'additional_images', 'brand']

    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            # Преобразуем списки в строки для записи в CSV
            data['sizes'] = ', '.join(data.get('sizes', []))
            data['colors'] = ', '.join(data.get('colors', []))
            data['additional_images'] = ', '.join(data.get('additional_images', []))
            writer.writerow(data)

        print(f"Данные успешно записаны в файл {filename}")
    except Exception as e:
        print(f"Ошибка записи в CSV: {e}")


# Пример использования:
product_url = "https://ridersarena.com/products/liqui-moly-15w50-4t-street-synthetic-technology-engine-oil-1-litre-lm030-for-bikes"
product_data = extract_product_data(product_url)

if product_data:
    print("Данные о товаре:")
    print(f"ID: {product_data['id']}")
    print(f"Ссылка на продукт: {product_data['product_url']}")
    print(f"Название: {product_data['title']}")
    print(f"Цена: {product_data['price']}")
    print(f"Фото: {product_data['photo_url']}")
    print(f"Описание: {product_data['description']}")
    print(f"Бренд: {product_data['brand']}")

    # Проверяем наличие размеров и цветов
    if product_data['sizes']:
        print(f"Доступные размеры: {', '.join(product_data['sizes'])}")
    else:
        print("Размеры не найдены.")

    if product_data['colors']:
        print(f"Доступные цвета: {', '.join(product_data['colors'])}")
    else:
        print("Цвета не найдены.")

    # Проверяем наличие дополнительных изображений
    if product_data['additional_images']:
        print("Дополнительные изображения:")
        for img in product_data['additional_images']:
            print(img)
    else:
        print("Дополнительные изображения не найдены.")

    write_to_csv("one_product_motoarena.csv", product_data)
else:
    print("Не удалось извлечь данные о товаре.")

# import requests
# from bs4 import BeautifulSoup
# import csv
# import os
#
#
# def extract_product_data(url):
#     """
#     Улучшенный парсер данных товара с обработкой ошибок:
#     - Исправлены селекторы для цены
#     - Добавлена проверка URL фото
#     - Улучшена обработка описания
#     """
#     try:
#         response = requests.get(url, timeout=15)
#         response.raise_for_status()
#     except Exception as e:
#         print(f"Ошибка запроса: {e}")
#         return None
#
#     soup = BeautifulSoup(response.content, 'html.parser')
#
#     data = {
#         'title': 'Не найдено',
#         'price': 'Не найдена',
#         'photo_url': 'Не найдено',
#         'description': 'Не найдено'
#     }
#
#     try:
#         # Название товара
#         title = soup.find('h1', {'class': 'h1'}) or soup.find('h1')
#         if title:
#             data['title'] = title.get_text(strip=True)
#
#         # Цена (учитываем оба варианта отображения)
#         price = (soup.find('span', class_='price-item--sale') or
#                  soup.find('span', class_='price-item--regular'))
#         if price:
#             data['price'] = price.get_text(strip=True).replace('Rs.', '').replace(' ', '')
#
#         # Фото
#         img_container = soup.find('div', class_='product__media')
#         if img_container:
#             img = img_container.find('img', src=True)
#             if img:
#                 data['photo_url'] = img['src'] if img['src'].startswith('http') else f"https:{img['src']}"
#
#         # Описание
#         description = soup.find('div', class_='product__description')
#         if description:
#             data['description'] = ' '.join(description.stripped_strings)
#
#     except Exception as e:
#         print(f"Ошибка парсинга: {e}")
#
#     return data
#
#
# def read_links_from_file(filename):
#     """
#     Чтение ссылок из CSV файла с проверкой:
#     - Автоматическое определение кодировки
#     - Пропуск заголовка
#     - Валидация URL
#     """
#     links = []
#     try:
#         with open(filename, 'r', encoding='utf-8') as f:
#             reader = csv.reader(f)
#             next(reader, None)  # Пропускаем заголовок
#             for row in reader:
#                 if row and row[0].startswith('http'):
#                     links.append(row[0].strip())
#     except Exception as e:
#         print(f"Ошибка чтения файла: {e}")
#     return links
#
#
# def write_data_to_csv(filename, data):
#     """
#     Запись данных в CSV с:
#     - Проверкой директории
#     - Резервным сохранением при ошибках
#     """
#     try:
#         os.makedirs(os.path.dirname(filename), exist_ok=True)
#         with open(filename, 'w', newline='', encoding='utf-8') as f:
#             writer = csv.DictWriter(f, fieldnames=data[0].keys())
#             writer.writeheader()
#             writer.writerows(data)
#         print(f"Данные сохранены в {os.path.abspath(filename)}")
#     except Exception as e:
#         print(f"Ошибка сохранения: {e}")
#         # Попытка сохранить в текущую директорию при ошибке пути
#         with open('product_data_backup.csv', 'w', encoding='utf-8') as f:
#             f.write('\n'.join([str(item) for item in data]))
#
#
# if __name__ == "__main__":
#     # Конфигурационные параметры
#     INPUT_FILE = os.path.join('urls_csv', 'product_links.csv')
#     OUTPUT_FILE = os.path.join('parsed_data', 'one_product_motoarena.csv')
#
#     # Проверка существования файла
#     if not os.path.exists(INPUT_FILE):
#         print(f"Файл {os.path.abspath(INPUT_FILE)} не найден!")
#         print("Проверьте:")
#         print(f"1. Существование файла {INPUT_FILE}")
#         print(f"2. Рабочую директорию: {os.getcwd()}")
#         exit()
#
#     # Основной процесс
#     links = read_links_from_file(INPUT_FILE)
#
#     if not links:
#         print("Не найдено валидных ссылок в файле")
#         exit()
#
#     results = []
#     for idx, url in enumerate(links, 1):
#         print(f"Обработка {idx}/{len(links)}: {url}")
#         try:
#             product_data = extract_product_data(url)
#             if product_data:
#                 results.append(product_data)
#         except Exception as e:
#             print(f"Ошибка обработки {url}: {e}")
#
#     if results:
#         write_data_to_csv(OUTPUT_FILE, results)
#     else:
#         print("Нет данных для сохранения")
