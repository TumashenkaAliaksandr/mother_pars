# import requests
# from bs4 import BeautifulSoup
#
# url = "https://frenchcrown.in/collections/shirts"
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
# }
#
# response = requests.get(url, headers=headers)
# soup = BeautifulSoup(response.content, "html.parser")
#
# title_element = soup.find('h1', {'class': 'Product__Title'})
# title = title_element.text.strip() if title_element and title_element.text.strip() != 'Default Title' else ''
# print('Title: ', title)
#
# category_elem = soup.find('h1', {'class': 'Heading'})
# category = category_elem.text.strip()
# print('Category: ', category)

import requests
from bs4 import BeautifulSoup

url = "https://frenchcrown.in/products/bright-white-with-tacao-peach-rose-printed-lightweight-premium-cotton-oversized-shirt-bu"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

title = soup.find("h1", class_="ProductMeta__Title").text.strip()  # этот кусок кода для тайтла
print(title)


# # Находим все контейнеры товаров
# product_containers = soup.find_all("div", class_="ProductItem__Wrapper") # аходим все теги
# print(product_containers)
#
# # Список для хранения всех ссылок
# all_links = []
#
# # Извлекаем ссылки на товары из контейнеров
# for container in product_containers:
#     link = container.find("a", class_="href")
#     if link and "href" in link.attrs:
#         all_links.append(link["href"])
#     print(container)
#
#
# # Выводим собранные ссылки
# for link in all_links:
#     print(link)


# from bs4 import BeautifulSoup
#
# html_code = '<div class="ProductItem__Wrapper"><a class="ProductItem__ImageWrapper ProductItem__ImageWrapper--withAlternateImage" href="/products/bright-white-and-waikawa-blue-striped-chambray-kurta-shirt-bu" target="_blank"><div class="AspectRatio AspectRatio--withFallback ProdctImage-wrap" style="max-width: 3600px; padding-bottom: 125.0%; --aspect-ratio: 0.8"><img alt="Bright White and Waikawa Blue Striped Chambray Kurta Shirt 9995-KS-38, 9995-KS-H-38, 9995-KS-39, 9995-KS-H-39, 9995-KS-40, 9995-KS-H-40, 9995-KS-42, 9995-KS-H-42, 9995-KS-44, 9995-KS-H-44, 9995-KS-46, 9995-KS-H-46, 9995-KS-48, 9995-KS-H-48, 9995-KS-50, 9995-KS-H-50, 9995-KS-52, 9995-KS-H-52" class="ProductItem__Image ProductItem__Image--alternate Image--lazyLoaded lazy2" data-image-id="30007669358643" data-mobsrc="//cdn.shopify.com/s/files/1/0094/6326/7379/files/9995-KS_2_720x.jpg?v=1686404110" data-sizes="auto" data-src="//cdn.shopify.com/s/files/1/0094/6326/7379/files/9995-KS_2_1080x.jpg?v=1686404110" data-widths="[200,300,400,600]" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="/><img alt="Bright White and Waikawa Blue Striped Chambray Kurta Shirt 9995-KS-38, 9995-KS-H-38, 9995-KS-39, 9995-KS-H-39, 9995-KS-40, 9995-KS-H-40, 9995-KS-42, 9995-KS-H-42, 9995-KS-44, 9995-KS-H-44, 9995-KS-46, 9995-KS-H-46, 9995-KS-48, 9995-KS-H-48, 9995-KS-50, 9995-KS-H-50, 9995-KS-52, 9995-KS-H-52" class="ProductItem__Image Image--lazyLoaded lazy2 lazy3" data-image-id="30007669293107" data-mobsrc="//cdn.shopify.com/s/files/1/0094/6326/7379/files/9995-KS_1_720x.jpg?v=1686404110" data-sizes="auto" data-src="//cdn.shopify.com/s/files/1/0094/6326/7379/files/9995-KS_1_1080x.jpg?v=1686404110" data-widths="[200,400,600]" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="/>\n<span class="Image__Loader"></span>'
#
# soup = BeautifulSoup(html_code, "html.parser")
#
#
# link = soup.find("a", class_="ProductItem__ImageWrapper")
# if link and "href" in link.attrs:
#     product_link = link["href"]
#     print('https://frenchcrown.in/' + product_link)
# else:
#     print("Ссылка не найдена.")
