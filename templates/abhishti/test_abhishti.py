import requests
from bs4 import BeautifulSoup
import csv

base_url = "https://www.abhishti.com/collections/new-arrival-men"
page_num = 1
links = []

while True:
    url = f"{base_url}?page={page_num}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    product_divs = soup.find_all("div", class_="product-item__image-wrapper product-item__image-wrapper--multiple")

    for div in product_divs:
        link = div.find("a")["href"]
        # Добавьте "https://" к каждой ссылке
        full_link = "https://www.abhishti.com" + link
        links.append(full_link)

    next_link = soup.find("a", class_="next")
    if not next_link:
        break

    page_num += 1

with open("urls_csv/urls_new_arrival_men.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["url"])
    for link in links:
        writer.writerow([link])

print("Ссылки на товары успешно записаны в файл urls_new_arrival_men.csv.")
