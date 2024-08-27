import requests
from bs4 import BeautifulSoup
import csv
import random
import string
from selenium import webdriver

# Функция для получения информации о продукте по его URL
def get_product_info(url):
    driver = webdriver.Chrome()  # или другой драйвер
    driver.set_page_load_timeout(70)
    driver.get(url)
    print(f"Парсим страницу: {url}")

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Находим название продукта
    title_element = soup.find('h1', class_='product_title')
    title = title_element.text.strip() if title_element else 'Title not found'
    print("Название продукта:", title)

    # Ищем элемент <li> с классом 'price-old' или внутри 'price-container'
    sale_price_element = soup.find('div', class_='price')

    if not sale_price_element:
        price_container = soup.find('span', class_='woocommerce-Price-currencySymbol')
        if price_container:
            sale_price_element = price_container.find('span')

    if sale_price_element:
        span_or_h2_element = sale_price_element.find(['span', 'woocommerce-Price-currencySymbol'])
        sale_price = span_or_h2_element.text.strip().replace('₹', '').strip() if span_or_h2_element else 'N/A'
    else:
        sale_price = 'N/A'

    print("Цена без скидки:", sale_price)

    # Находим контейнеры с описанием
    description_container = soup.find('div', class_='tab-content')

    description = ''
    if description_container:
        description = description_container.get_text(strip=True)

    print('Описание:', description)

    # Находим див-блок с классом "zoom nslick-slide nslick-current nslick-active"
    div_block = soup.find('div', class_='woo-single-images')

    photos = []
    if div_block:
        # Находим все теги <img> внутри див-блока
        img_tags = div_block.find_all('img')
        for img in img_tags:
            # Извлекаем значение атрибута "src"
            src = img.get('src')
            if src:
                photos.append(src)

        # Выводим все найденные ссылки на фотографии
        print("Ссылки на фотографии:", photos)
    else:
        print("Див-блок не найден.")

    # Форматируем ссылки в строку, разделённую запятыми
    if photos:
        photo_urls = ', '.join(photos[:3])
        print("Ссылки на фотографии:", photo_urls)
    else:
        photo_urls = 'No images found'
        print("Ссылки на фотографии:", photo_urls)

    # Генерируем рандомный ID
    product_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    print("Product ID:", product_id)

    brand = 'Satya'

    # Находим категорию и подкатегорию
    category_li_ancestor = soup.find('li', class_='level-3 sub item-term_ancestor')
    category_li_post_term = soup.find('li', class_='level-3 sub item-post_term')

    category = None
    if category_li_ancestor:
        category_link = category_li_ancestor.find('a')
        if category_link:
            category = category_link.text.strip()
    if not category and category_li_post_term:
        category_link = category_li_post_term.find('a')
        if category_link:
            category = category_link.text.strip()

    if not category:
        category = 'Category not found'
    print('Категория:', category)

    driver.quit()
    return {
        'Product ID': product_id,
        'Title': title,
        'Description': description,
        'Image URLs': photo_urls,
        'Price': sale_price,
        'Brand': brand,
        'Category': category if 'category' in locals() else 'Category not found',
    }

# Читаем URL-адреса из файла product_url
with open('product_url.csv', 'r', encoding='utf-8') as file:
    urls = [line.strip() for line in file.readlines()]

# Обрабатываем каждый URL-адрес и записываем результаты в файл Saya_product_info.csv
with open('Saya_product_info.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile,
                            fieldnames=['Product ID', 'Brand', 'Category', 'Title', 'Price',
                                        'Description',
                                        'Image URLs'])
    writer.writeheader()

    for url in urls:
        product_info = get_product_info(url)
        writer.writerow(product_info)

print(f"Информация о продуктах была сохранена в файл 'Saya_product_info.csv'.")
