import requests
from bs4 import BeautifulSoup


url = "https://www.uniqlo.com/in/en/products/E444705-000?colorCode=COL09&sizeCode=BVI120"
html = requests.get(url).text
soup = BeautifulSoup(html, 'html.parser')

# Получение тайтла
title_element = soup.find('h1', {'class': 'product-name'})
title = title_element.text.strip() if title_element and title_element.text.strip() != 'Default Title' else ''
print('Title: ', title)


# # Получение цены
# price = soup.find("span", class_="price-original").get_text()
# print("Price:", price)
#
#
# # Получение описания
# description = soup.find("div", class_="pdp-sub-copy").get_text()
# print("Description:", description)
#
#
# # Получение фото
# image_url = soup.find("img", class_="thumb-img")["src"]
# print("Image URL:", image_url)
#
#
# # Получение ID товара
# product_id = url.split("/")[-1].split("?")[0]
# print("Product ID:", product_id)
