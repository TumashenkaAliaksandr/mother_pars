import csv
import time
from requests import Session
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://frenchcrown.in/collections/women-sale"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    )
}


def get_product_links(soup):
    links = set()

    for a in soup.find_all("a", href=True):

        href = a["href"]

        if "/products/" not in href:
            continue

        if href.startswith("/products/"):
            full_url = urljoin("https://frenchcrown.in", href)
            links.add(full_url)

    return links


def main():

    session = Session()
    session.headers.update(HEADERS)

    all_links = set()

    page = 1

    while True:

        if page == 1:
            url = BASE_URL
        else:
            url = f"{BASE_URL}?page={page}"

        print(f"Открываю страницу {page}")

        try:
            response = session.get(url, timeout=30)
        except Exception as e:
            print(e)
            break

        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "html.parser")

        page_links = get_product_links(soup)

        print(f"Найдено ссылок: {len(page_links)}")

        if not page_links:
            break

        before_count = len(all_links)

        all_links.update(page_links)

        after_count = len(all_links)

        if before_count == after_count:
            break

        page += 1

        time.sleep(1)

    output_file = "../../urls_csv/urls_women_sale.csv"

    with open(output_file, "w", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        writer.writerow(["url"])

        for link in sorted(all_links):
            writer.writerow([link])

    print(f"\nВсего найдено товаров: {len(all_links)}")
    print(f"Файл сохранён: {output_file}")


if __name__ == "__main__":
    main()