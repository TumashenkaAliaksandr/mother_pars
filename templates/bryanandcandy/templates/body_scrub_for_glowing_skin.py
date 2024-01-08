import re
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
input_file = '../urls_csv/body_scrub_for_glowing_skin_links.csv'
output_file = '../done_csv/body_scrub_for_glowing_skin.csv'

with open(input_file, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Пропуск заголовков, если они есть

    with open(output_file, mode='w', newline='', encoding='utf-8') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(['Title', 'Cost', 'Description', 'Photos', 'Brand', 'Сategory', 'id'])

        for row in reader:
            url = row[0]  # Получаем ссылку на товар из столбца CSV файла
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Проверяем наличие информации о товаре
            title = soup.find('h1', class_='ProductMeta__Title')
            cost = soup.find('span', class_='ProductMeta__Price')
            description = soup.find('div', class_='ProductMeta__Description')

            if title and cost and description:
                title_text = title.text.strip()
                cost_text = cost.text.strip().replace('Rs.', '')
                description_text = description.text.strip()
                brand = 'Bryan & Candy'
                category = "Body Scrub"

                photos = []
                for link in soup.find_all('a', class_='Product__SlideshowNavImage'):
                    href = link.get('href')
                    if href.startswith('//'):
                        href = 'https:' + href  # Добавляем 'https:' к ссылке, если она начинается с '//'
                    if len(photos) < 3:  # Ограничиваем количество фото тремя
                        photos.append(href)  # Добавляем только ссылку на фото

                section_id = get_product_id(url)  # Получаем ID продукта
                writer.writerow([title_text, cost_text, description_text, '\n'.join(photos), brand, category, section_id])
            else:
                writer.writerow(['', '', '', '', '', '', 'ID продукта не найден или информация о товаре отсутствует'])

print('Информация успешно записана в body_scrub_for_glowing_skin.csv')
