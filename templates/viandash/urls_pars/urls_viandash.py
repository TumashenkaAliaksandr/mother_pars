import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.viandash.com/"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    # Находим все теги <a> с классом "full-unstyled-link" и href, содержащими "/products/"
    product_links = set()  # Используем множество для автоматического исключения повторяющихся ссылок
    for link in soup.find_all('a', class_='full-unstyled-link', href=lambda x: x and '/products/' in x):
        full_link = "https://www.viandash.com" + link['href']
        product_links.add(full_link)

    # Записываем найденные ссылки в файл CSV
    with open('../urls_csv/urls_viandash_links.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Записываем заголовок
        writer.writeheader()

        # Записываем ссылки
        for full_link in product_links:
            writer.writerow({'url': full_link})

        print("Ссылки успешно записаны в файл honeyhut_urls.csv")
else:
    print(f"Ошибка {response.status_code}: Невозможно получить доступ к странице")
