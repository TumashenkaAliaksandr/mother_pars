import requests
from bs4 import BeautifulSoup

base_url = 'https://azmirli-perfume.by/katalog/'
page_number = 2
visited_links = set()

while True:
    url = f'{base_url}?page={page_number}'
    response = requests.get(url)

    # Проверка наличия контента на странице
    if response.status_code != 200:
        break

    soup = BeautifulSoup(response.text, 'html.parser')

    # Найти все ссылки на товары
    card_headers = soup.find_all('div', {'class': 'card_hdr'})
    for header in card_headers:
        link = header.find('a', {'class': 'msoptionsprice-name'})
        if link:
            href = link.get('href')
            full_url = f'https://azmirli-perfume.by/{href}'
            if full_url not in visited_links:
                visited_links.add(full_url)
                print(full_url)

    # Переход к следующей странице
    page_number += 1
