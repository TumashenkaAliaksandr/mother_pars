import requests
from bs4 import BeautifulSoup

url = "https://www.abhishti.com/products/pink-striped-kurta-with-pintucks-with-straight-pants-abi-mn-st107"

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Парсинг заголовка (title)
title_element = soup.find("h1", class_="product-meta__title heading h3")
title = title_element.text.strip() if title_element else "Заголовок не найден"

# Парсинг цены
price_element = soup.find("span", class_="price")
price = price_element.text.strip() if price_element else "Цена не найдена"

price = price.replace("Sale price₹", "").strip()

print("Заголовок:", title)
print("Цена:", price)
