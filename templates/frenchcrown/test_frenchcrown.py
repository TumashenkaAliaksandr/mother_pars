import requests
import csv

base_url = "https://hits.gokwik.co/api/v1/header/events/update"

def main(base_url):
    product_links = set()
    page = 1

    while True:
        url = f"{base_url}?page={page}"
        response = requests.get(url)
        json_data = response.json()

        # Проверяем, есть ли еще страницы
        if not json_data or not json_data.get("data"):
            break

        for item in json_data["data"]:
            link = item.get("url")
            if link:
                product_links.add(link)

        page += 1

    with open('urls_boxers.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['url'])
        writer.writerows([[link] for link in product_links])

    print("Ссылки на товары были успешно записаны в файл 'urls_boxers.csv'.")

main(base_url)
