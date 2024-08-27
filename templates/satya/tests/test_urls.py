import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_product_links(page_url):
    driver = webdriver.Chrome()  # или другой драйвер
    driver.get(page_url)
    print(f"Парсим страницу: {page_url}")

    product_links = set()  # Используем множество для автоматического удаления дубликатов

    while True:
        try:
            # Ждем появления кнопки "Load More"
            load_more_button = WebDriverWait(driver, 100).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.load-more'))
            )
            load_more_button.click()
            print("Нажали кнопку 'Load More'")
        except Exception as e:
            print(f"Кнопка 'Load More' не найдена или недоступна: {e}")
            break

        # Дожидаемся загрузки новых товаров
        driver.implicitly_wait(50)

    # Парсим страницу после всех кликов
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Находим все див-блоки с классом "product-wrapper"
    product_wrappers = soup.find_all('div', class_='product-wrapper')
    print(f"Найдено див-блоков: {len(product_wrappers)}")

    for product_wrapper in product_wrappers:
        # Находим теги <h3> внутри див-блока
        h3_tags = product_wrapper.find_all('h3')
        print(f"Внутри див-блока найдено тегов <h3>: {len(h3_tags)}")

        for h3_tag in h3_tags:
            # Находим теги <a> внутри тега <h3>
            a_tags = h3_tag.find_all('a')
            print(f"Внутри тега <h3> найдено тегов <a>: {len(a_tags)}")

            for a_tag in a_tags:
                # Извлекаем значение атрибута "href"
                href = a_tag.get('href')
                if href and not href.startswith('?'):
                    print(f"Найдена ссылка: {href}")
                    # Добавляем префикс к ссылке
                    full_url = urljoin(base_url, href)
                    # Добавляем ссылку в множество
                    product_links.add(full_url)
                    print(f"Добавлена ссылка в множество: {full_url}")

    driver.quit()
    print(f"Найдено ссылок на странице: {len(product_links)}")
    return product_links

base_url = "https://houseofnagchampa.com/"
url = urljoin(base_url, "shop")

product_links = get_product_links(url)

# Записываем ссылки в CSV файл
with open('product_url.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['url']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for link in product_links:
        writer.writerow({'url': link})
        print(f"Записали ссылку в CSV: {link}")

print("Ссылки успешно записаны в файл 'product_url.csv'")
