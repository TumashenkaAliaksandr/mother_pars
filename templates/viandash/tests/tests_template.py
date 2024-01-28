import re
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
import csv
import random
import string

# Функция для генерации уникального числового ID
def generate_numeric_id(length=10):
    return ''.join(random.choices(string.digits, k=length))

# Функция для получения ID с веб-страницы
def get_product_id(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Генерация уникального числового ID для товара
    return generate_numeric_id()

# Чтение ссылок из CSV файла и обработка
input_file = '../urls_csv/urls_viandash_links.csv'
output_file = '../done_csv/viandash_done.csv'

with open(input_file, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Пропуск заголовков, если они есть

    with open(output_file, mode='w', newline='', encoding='utf-8') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(['Title', 'Cateory', 'Cost', 'Cost Variants', 'Description', 'Photos', 'Brand', 'id'])

        for row in reader:
            url = row[0]  # Получаем ссылку на товар из столбца CSV файла
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Проверяем наличие информации о товаре
            title = soup.find('h1', class_='product__title').text.strip()
            print(title)
            cost = soup.find('span', class_='price-item').text.strip().replace('Rs. ', '')
            print(cost)

            # Находим все опции внутри тега select
            options = soup.select('select.select__select option')

            # Создаем строку с элементами для удаления
            remove_elements = ['[', '- Rs.', '\n\n', '                         ', "'"]

            # Извлекаем текст каждой опции и удаляем лишние элементы с помощью replace
            cost_variants = [option.get_text(strip=True) for option in options]
            for element in remove_elements:
                cost_variants = [variant.replace(element, ' ') for variant in cost_variants]
            # Приводим варианты к строке, разделяя их запятой
            cost_variants_str = ' | '.join(cost_variants)

            product_info = soup.find('div', class_='product__info-wrapper')
            if product_info:
                p_elements = product_info.find_all('p')
                p_texts = "\n".join([p.text.strip() for p in p_elements])

                # Собираем все тексты в одну строку
                combined_text = f"{p_texts}"
                print(combined_text)

            category = soup.find('div', class_='product__info-wrapper')
            if category:
                c_elements = product_info.find('p')
                c_texts = "\n".join([p.text.strip() for p in c_elements])

                # Собираем все тексты в одну строку
                category_text = f"{c_texts}"
                print(category_text)

            brand = 'Vi & Ash'
            print(brand)

            # ... (остальной код)

            photos = []
            media_div = soup.find('div',
                                  class_='product__media media media--transparent gradient global-media-settings')

            if media_div:
                img_tag = media_div.find('img')
                if img_tag:
                    srcset_attribute = img_tag.get('srcset')
                    if srcset_attribute:
                        src_values = srcset_attribute.split(', ')
                        if src_values:
                            src_value = src_values[0].split(' ')[0]  # Берем первое значение в srcset

                            # Используем urlparse для извлечения чистого URL без параметров запроса
                            parsed_url = urlparse(src_value)
                            base_url = parsed_url.scheme + 'https://' + parsed_url.netloc + parsed_url.path

                            photos.append(base_url)
                            print(photos)
                        else:
                            print("No src values found in srcset.")
                    else:
                        print("srcset attribute not found.")
                else:
                    print("Img tag not found.")
            else:
                print("Media div not found.")

            # Прямо в writer.writerow записываем photos[0] (первую ссылку) без кавычек и двух слэшей
            section_id = get_product_id(url)  # Получаем ID продукта
            writer.writerow([title, category_text, cost, cost_variants_str, combined_text, photos[0], brand, section_id])

            # Теперь выводим cost_variants после цикла
            print("Cost Variants:", cost_variants_str)

print('Информация успешно записана в viandash_done.csv')
