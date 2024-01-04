import re
import requests
from bs4 import BeautifulSoup
import csv


# Функция для получения ID с веб-страницы
def get_product_id(url):
    respon = requests.get(url)
    soup = BeautifulSoup(respon.text, 'html.parser')

    # Поиск ID на странице
    section_id = None
    result = soup.find('section', class_='Product--medium')
    if result:
        section_id_string = result.get('data-section-id')
        section_id_numbers = re.search(r'\d+', section_id_string)
        if section_id_numbers:
            section_id = section_id_numbers.group()

    return section_id if section_id else "ID продукта не найден на странице"


# Чтение ссылок из CSV файла и обработка
input_file = '../urls_csv/bryanandcandy_links.csv'
output_file = '../done_csv/product_bryanandcandy_info.csv'


with open(input_file, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Пропуск заголовков, если они есть

    with open(output_file, mode='w', newline='', encoding='utf-8') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(['Title', 'Cost', 'Description', 'Photos', 'Brand', 'id'])

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
                category = 'Gifting'

                photos = []
                for link in soup.find_all('a', class_='Product__SlideshowNavImage'):
                    href = link.get('href')
                    if href.startswith('//'):
                        href = 'https:' + href  # Добавляем 'https:' к ссылке, если она начинается с '//'
                    photos.append(href)  # Добавляем только ссылку на фото

                section_id = get_product_id(url)  # Получаем ID продукта
                writer.writerow([title_text, cost_text, description_text, '\n'.join(photos), brand, category, section_id])
            else:
                writer.writerow(['', '', '', '', '', '', 'ID продукта не найден или информация о товаре отсутствует'])

print('Информация успешно записана в product_info.csv')
