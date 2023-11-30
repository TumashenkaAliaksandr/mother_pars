# import requests
# from bs4 import BeautifulSoup
# import csv
#
# url = 'https://raadshop.com/products/hightop-mandalaandroses02869'
# response = requests.get(url)
#
# soup = BeautifulSoup(response.content, "html.parser")
#
# header = soup.find("header", class_="mobile-hide")
# title = header.find("h2", class_="m5 mob-h2").text.strip()
#
# price_element = soup.find("p", class_="f8pr-price s1pr")
# current_price = price_element.find("span", class_="cvc-money").find("span", class_="money").text.strip()
#
# div_tag = soup.find('div', class_='m6lm')
#
# if div_tag:
#     p_tag = div_tag.find('p')
#     if p_tag:
#         text = p_tag.text.strip()
#         if '•' in text:
#             text = '\n'.join(line.strip() for line in text.split('•') if line.strip())
#
# category = 'Shoes'
#
# # Запись параметров в CSV-файл
# with open('done_csv/product_details.csv', mode='w', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
#     writer.writerow(['Title', 'Current Price', 'Category', 'Description'])
#     writer.writerow([title, current_price, text if text else 'No description available'])
#
#
#
import requests
from bs4 import BeautifulSoup
import csv

url = 'https://raadshop.com/products/hightop-mandalaandroses02869'
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

header = soup.find("header", class_="mobile-hide")
title = header.find("h2", class_="m5 mob-h2").text.strip()

price_element = soup.find("p", class_="f8pr-price s1pr")
current_price = price_element.find("span", class_="cvc-money").find("span", class_="money").text.strip()

category = 'Shoes'

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
    writer.writerow(['Title', 'Current Price', 'Category', 'Description'])
    writer.writerow([title, current_price, category, text if text else 'No description available'])
