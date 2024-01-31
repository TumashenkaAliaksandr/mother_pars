import os
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import uuid
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

directory = '../done_csv'
filename = 'myatulya_coldpressed_oil.csv'
FILEPARAMS = os.path.join(directory, filename)

def create_csv(filename, order):
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        csv.writer(file).writerow(order)

def write_data_csv(filename, data):
    with open(filename, 'a', encoding='utf-8', newline='') as file:
        csv.DictWriter(file, fieldnames=list(data)).writerow(data)

def get_data(url):
    try:
        # Инициализация Selenium
        options = Options()
        options.headless = True  # Установите True, если вы не хотите видеть открывающееся окно браузера
        driver = webdriver.Chrome(options=options)

        try:
            driver.get(url)
            # Подождем, чтобы дать странице время на загрузку JavaScript
            driver.implicitly_wait(10)
            # Получаем HTML-код после загрузки JavaScript
            html_code = driver.page_source
        finally:
            driver.quit()

        if html_code:
            soup = BeautifulSoup(html_code, 'html.parser')

            # Генерируем случайный идентификатор UUID
            uuid_str = str(uuid.uuid4())
            # Оставляем только цифры
            digits = ''.join(filter(str.isdigit, uuid_str))
            # Ограничиваем количество символов до 8
            product_id = digits[:8]
            print('Product ID:', product_id)

            # Извлекаем заголовок товара
            title = soup.find('h1', class_='product-single__title').text.strip().capitalize()
            print('Title: ', title)

            brand = 'Atulya'
            category = 'HAIR CARE'
            subcategory = 'COLD PRESSED OIL'

            # Извлекаем цену товара, добавляем проверку наличия элемента
            price_element = soup.find('span', class_='product__price')
            price = price_element.text.strip().replace('Rs. ', '').split('.')[0] if price_element else "Цена не указана"
            print('Price: ', price)

            total_price = soup.find('span', class_='cbb-frequently-bought-total-price-sale-price')
            price_total_find = total_price.text.strip().replace('Rs. ', '').split('.')[0] if total_price else "No price"
            print('Total Price: ', price_total_find)

            # Извлекаем описание товара, добавляем проверку наличия элемента
            description_element = soup.find('div', class_='collapsible-content__inner rte')
            description = description_element.text.strip().capitalize() if description_element else "Описание отсутствует"
            print('Descriptions: ', description)

            # Извлекаем только три первые ссылки на фотографии, исключая те, которые содержат "thumbnail"
            photo_links = [urljoin(url, img['src']) for img in soup.find_all('img', class_='photoswipe__image')[:4] if
                           'thumbnail' not in img.get('src', '')]
            print('Photo url: ', photo_links)

            # Найдем все теги <p> внутри блока с классом "metafield-rich_text_field"
            p_tags = soup.select('.metafield-rich_text_field p')

            # Вывести текст каждого тега <p>
            how_to_use = '\n'.join(p_tag.text.strip() for p_tag in p_tags)
            print('Ingredients & How to use: ', how_to_use)

            # Найдем все теги <li>
            li_tags = soup.find_all('li')
            sale_prices = []

            # Извлечем значения из тегов <h3>, <s> и <span class="money"> в каждом <li>
            for li_tag in li_tags:
                h3_tag = li_tag.find('h3', class_='cbb-frequently-bought-selector-label-name')
                s_tag = li_tag.find('span', class_='cbb-frequently-bought-selector-label-sale-price')
                money_tag = li_tag.find('span', class_='money')

                if h3_tag and s_tag and money_tag:
                    label = h3_tag.text.strip().capitalize()
                    compare_at_price = s_tag.text.strip().replace('Rs. ', '').split('.')[0]
                    sale_prices.append(f'{label}\nSale price: {compare_at_price}\n')
                    print(f'{label}\nSale price: {compare_at_price}\n')

            # Собираем данные о товаре в словарь
            product_data = {
                'ID': product_id,
                'Title': title,
                'Brand': brand,
                'Price': price,
                'Category': category,
                'Subcategory': subcategory,
                'Total Price': price_total_find,
                'Sale Price': ''.join(sale_prices),
                'Description': description,
                'Ingredients & How to use': how_to_use,
                'Photo_Links': ', '.join(photo_links),
            }

            # Записываем данные в CSV файл
            write_data_csv(FILEPARAMS, product_data)

            print(f"Данные успешно записаны в файл {FILEPARAMS}")
        else:
            print("Не удалось получить HTML-код страницы.")
    except Exception as e:
        print(f"Произошла ошибка при обработке URL {url}: {e}")

# Считываем URL из файла и обрабатываем каждый из них
urls_filename = '../urls_csv/coldpressed_oil_links.csv'  # Укажите имя вашего файла с URL
with open(urls_filename, 'r', encoding='utf-8') as urls_file:
    urls = [line.strip() for line in urls_file]

# Определите порядок полей в CSV файле
order = ['ID', 'Title', 'Brand', 'Price', 'Category', 'Subcategory', 'Total Price', 'Sale Price', 'Description',
         'Ingredients & How to use', 'Photo_Links']

# Создаем CSV файл с заголовками
create_csv(FILEPARAMS, order)

# Обрабатываем каждый URL
for url in urls:
    get_data(url)
