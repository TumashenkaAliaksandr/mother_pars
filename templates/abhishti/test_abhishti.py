import requests
from bs4 import BeautifulSoup
import csv
import time

def get_product_links(base_url, delay=2, output_csv="urls_csv/urls_new_arrival_men.csv"):
    page_num = 1
    links = []

    while True:
        url = f"{base_url}?page={page_num}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Проверка наличия ошибок при запросе
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к {url}: {e}")
            break

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
        time.sleep(delay)  # Добавьте задержку перед следующим запросом

    with open(output_csv, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["url"])
        for link in links:
            writer.writerow([link])

    print(f"Ссылки на товары успешно записаны в файл {output_csv}.")

if __name__ == "__main__":
    base_url = "https://www.abhishti.com/collections/new-arrival-men"
    get_product_links(base_url)
