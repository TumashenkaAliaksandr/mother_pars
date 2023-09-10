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

# Находим все элементы с классом "pl-swatches__link" и извлекаем их атрибут "aria-label"
aria_labels = [a['aria-label'] for a in soup.find_all('a', class_='pl-swatches__link')]

# Выводим полученные значения "aria-label"
for label in aria_labels:
    print('Color:', label)

# Находим элементы <input> с классом "block-swatch__radio" и извлекаем их атрибут "value"
input_elements = soup.find_all('input', class_='block-swatch__radio')

# Создаем список для хранения значений атрибута "value"
values = [input_element['value'] for input_element in input_elements]

# Выводим полученные значения "value"
for value in values:
    print('Size:', value)
