import requests
from bs4 import BeautifulSoup
import csv
import json

url = 'https://raadshop.com/products/hightop-mandalaandroses02869'
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

header = soup.find("header", class_="mobile-hide")
title = header.find("h2", class_="m5 mob-h2").text.strip() if header else ''
print('Title:', title)

price_element = soup.find("p", class_="f8pr-price s1pr")
current_price = price_element.find("span", class_="cvc-money").find("span", class_="money").text.strip() if price_element else ''
print('Price:', current_price)

category = 'Shoes'
print('Category:', category)

style = "Men's High Tops"
print('Style:', style)

label_element = soup.find("span", class_="data-change-to-option-template--14771537444967__main-product-1")
color_sh = label_element.text.strip() if label_element else ''
print('Color:', color_sh)

li_element = soup.find('li', class_="hidden")

size = ''
if li_element:
    size_span = li_element.find('span')
    if size_span:
        size = size_span.text.strip()
    else:
        print('Размер не найден')
else:
    print('Элемент <li> не найден')
print(size)

select_element = soup.find("select", id="id-template--14771537444967__main-product")
option = select_element.find("option")

option_data = option.get("data-options")
if option_data:
    option_data = json.loads(option_data.replace("&quot;", '"'))
    option_id = option_data.get("id")
    print(f"ID: {option_id}")


div_tag = soup.find('div', class_='m6lm')

text = ''
if div_tag:
    p_tag = div_tag.find('p')
    if p_tag:
        text = p_tag.text.strip()
        if '•' in text:
            text = '\n'.join(line.strip() for line in text.split('•') if line.strip())
            print('Description:', text)

    # Запись параметров в CSV-файл
    with open('done_csv/product_details.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Current Price', 'Category', 'Style', 'Color', 'Size', 'Description', 'ID'])
        writer.writerow([title, current_price, category, style, color_sh, size, text if text else 'No description available', option_id])
else:
    print('Данные об ID не найдены')
