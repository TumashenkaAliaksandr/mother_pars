import requests
from bs4 import BeautifulSoup
import csv

# Функция для получения информации о продукте по его URL
def get_product_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Находим информацию о продукте
    product_title = soup.find('h1', class_='product-single__title')
    product_description = soup.find('div', class_='product-single__description')
    product_image = soup.find('img', class_='product-single__photo')
    product_price = soup.find('span', class_='product-single__price')

    # Проверяем, найдены ли элементы, прежде чем извлечь информацию
    title = product_title.text.strip() if product_title else 'N/A'
    description = product_description.text.strip() if product_description else 'N/A'
    image_url = product_image['src'] if product_image and 'src' in product_image.attrs else 'N/A'
    price = product_price.text.strip() if product_price else 'N/A'

    return {
        'Title': title,
        'Description': description,
        'Image URL': image_url,
        'Price': price
    }

# Ссылка на продукт
product_url = 'https://www.camveda.com/products/camveda-bhimseni-kapoor-500gm-jar'

# Получаем информацию о продукте
product_info = get_product_info(product_url)

# Записываем информацию о продукте в файл CSV
with open('product_info.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Title', 'Description', 'Image URL', 'Price'])
    writer.writeheader()
    writer.writerow(product_info)

print("Информация о продукте была сохранена в файл 'product_info.csv'.")
