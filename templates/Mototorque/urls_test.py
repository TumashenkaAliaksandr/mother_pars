import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import csv


def get_pagination_links(base_url):
    page_urls = [base_url]
    page_number = 2

    while True:
        next_url = f"{base_url}?page={page_number}"
        try:
            # Проверяем существование страницы через HTML
            response = requests.get(next_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                products = soup.find_all('div', class_='card__content')
                if len(products) > 0:
                    page_urls.append(next_url)
                    page_number += 1
                else:
                    break
            else:
                break

            time.sleep(1)
        except Exception as e:
            print(f"Error: {e}")
            break

    return page_urls


def check_pagination(base_url):
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Ищем любые элементы пагинации с номером страницы
            return bool(soup.find('a', href=lambda x: x and '?page=' in x))
        return False
    except Exception as e:
        print(f"Ошибка: {e}")
        return False


def get_product_links(urls):
    all_product_links = set()  # Используем set для хранения уникальных ссылок

    for base_url in urls:
        paginated_urls = [base_url]  # Всегда обрабатываем первую страницу

        if check_pagination(base_url):
            print(f"Найдена пагинация: {base_url}")
            paginated_urls.extend(get_pagination_links(base_url))

        for url in paginated_urls:
            print(f"Обработка: {url}")
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    cards = soup.find_all('div', class_='card__content')

                    for card in cards:
                        a_tag = card.find('a', class_='full-unstyled-link')
                        if a_tag and (href := a_tag.get('href')):
                            full_url = urljoin("https://mototorque.in", href)
                            all_product_links.add(full_url)  # Добавляем в set

                    print(f"Найдено товаров: {len(cards)}")
                    time.sleep(1)

            except Exception as e:
                print(f"Ошибка: {e}")

    return list(all_product_links)  # Возвращаем список уникальных ссылок


def save_to_csv(links, filename):
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Product Links"])  # Заголовок
            for link in links:
                writer.writerow([link])
        print(f"Ссылки успешно сохранены в файл {filename}")
    except Exception as e:
        print(f"Ошибка при сохранении в файл: {e}")


# URL страниц со списком продуктов
urls = [
    "https://mototorque.in/collections/crash-guards",
    "https://mototorque.in/collections/royal-enfield-himalayan-bike-accessories-online"
]

# Получаем список ссылок на продукты
product_links = get_product_links(urls)

# Сохраняем в файл CSV
filename = "product_links.csv"
save_to_csv(product_links, filename)
