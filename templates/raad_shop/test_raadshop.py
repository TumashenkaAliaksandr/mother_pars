# import requests
# from bs4 import BeautifulSoup
#
# url = "https://raadshop.com/products/hightop-mandalaandroses02869"
#
# # Загрузка страницы
# response = requests.get(url)
# soup = BeautifulSoup(response.content, "html.parser")
#
# # Получение данных
# header = soup.find("header", class_="mobile-hide")
# title = header.find("h2", class_="m5 mob-h2").text.strip()
# price = soup.find("span", class_="product-price__price").text.strip()
# description = soup.find("div", class_="product-single__description rte").text.strip()
# image = soup.find("div", class_="product-single__photos").find("img")["src"]
#
# print("Title:", title)
# print("Price:", price)
# print("Description:", description)
# print("Image:", image)
import requests
from bs4 import BeautifulSoup

url = 'https://raadshop.com/products/hightop-mandalaandroses02869'
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

header = soup.find("header", class_="mobile-hide")
title = header.find("h2", class_="m5 mob-h2").text.strip()

print("Title:", title)

price_element = soup.find("p", class_="f8pr-price s1pr")
current_price = price_element.find("span", class_="cvc-money").find("span", class_="money").text.strip()

print("Current Price:", current_price)
