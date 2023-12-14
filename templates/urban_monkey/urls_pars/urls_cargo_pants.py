import requests
from bs4 import BeautifulSoup
import csv

base_url = "https://www.urbanmonkey.com/collections/cargo-pants.html?variant="
page_num = 1
links = []

while True:
    url = base_url + str(page_num)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    product_divs = soup.find_all("div", class_="t4s-product-btns")

    for div in product_divs:
        link = div.find("a")["href"]
        links.append('https://www.urbanmonkey.com/collections/cargo-pants' + link)

    next_link = soup.find("a", class_="next")
    if not next_link:
        break

    page_num += 1

with open("../urls_csv/urls_urban_monkey.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["url"])
    for link in links:
        writer.writerow([link])

print("Ссылки на товары успешно записаны в файл urls_urban_monkey.csv.")
