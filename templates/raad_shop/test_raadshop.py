import requests
from bs4 import BeautifulSoup
import csv

url = 'https://raadshop.com/products/hightop-mandalaandroses02869'
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

header = soup.find("header", class_="mobile-hide")
title = header.find("h2", class_="m5 mob-h2").text.strip() if header else ''

price_element = soup.find("p", class_="f8pr-price s1pr")
current_price = price_element.find("span", class_="cvc-money").find("span", class_="money").text.strip() if price_element else ''

category = 'Shoes'
style = "Men's High Tops"

label_element = soup.find("span", class_="data-change-to-option-template--14771537444967__main-product-1")
color_sh = label_element.text.strip() if label_element else ''

div_tag = soup.find('div', class_='m6lm')

text = ''
if div_tag:
    p_tag = div_tag.find('p')
    if p_tag:
        text = p_tag.text.strip()
        if '•' in text:
            text = '\n'.join(line.strip() for line in text.split('•') if line.strip())

# Запись параметров в CSV-файл
with open('done_csv/product_details.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Current Price', 'Category', 'Style', 'Color', 'Description'])
    writer.writerow([title, current_price, category, style, color_sh, text if text else 'No description available'])
