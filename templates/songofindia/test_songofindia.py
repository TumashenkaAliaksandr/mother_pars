import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.songofindia.co.in/index.php/home-fragrances/reeds-diffuser.html"
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

product_divs = soup.find_all("div", class_="product photo product-item-photo")

links = []

for div in product_divs:
    link = div.find("a")["href"]
    links.append(link)

with open("products.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Ссылка на товар"])
    for link in links:
        writer.writerow([link])

print("Ссылки на товары успешно записаны в файл products.csv.")
