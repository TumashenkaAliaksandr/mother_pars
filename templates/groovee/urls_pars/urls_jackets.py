import csv
import time
import urllib.parse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException


URL = "https://groovee.in/collections/fresh-drop"
OUTPUT_CSV = "../urls_csv/urls_jackets.csv"


# -----------------------------------
# Настройка Chrome
# -----------------------------------

options = Options()

# Для отладки лучше оставить браузер видимым
# options.add_argument("--headless=new")

options.add_argument("--start-maximized")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

driver.set_page_load_timeout(60)

try:

    print(f"Открываю страницу: {URL}")

    driver.get(URL)

    time.sleep(8)

    # -----------------------------------
    # Автоскролл
    # -----------------------------------

    print("Запускаю автоскролл...")

    last_height = driver.execute_script(
        "return document.body.scrollHeight"
    )

    same_height_count = 0

    while True:

        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )

        time.sleep(4)

        new_height = driver.execute_script(
            "return document.body.scrollHeight"
        )

        print(f"Высота страницы: {new_height}")

        if new_height == last_height:

            same_height_count += 1

            if same_height_count >= 3:
                print("Страница полностью загружена.")
                break

        else:

            same_height_count = 0

        last_height = new_height

    time.sleep(5)

    # -----------------------------------
    # Сбор ссылок через JS
    # -----------------------------------

    raw_links = driver.execute_script("""
        return Array.from(
            document.querySelectorAll('a.product-card__link')
        ).map(el => el.getAttribute('href'));
    """)

    print(f"Найдено элементов: {len(raw_links)}")

    product_links = set()

    for href in raw_links:

        if not href:
            continue

        href = href.strip()

        if "/products/" not in href:
            continue

        full_url = urllib.parse.urljoin(
            "https://groovee.in",
            href
        )

        product_links.add(full_url)

    print(
        f"Уникальных ссылок найдено: "
        f"{len(product_links)}"
    )

    # -----------------------------------
    # Сохранение CSV
    # -----------------------------------

    with open(
        OUTPUT_CSV,
        "w",
        newline="",
        encoding="utf-8"
    ) as csvfile:

        writer = csv.writer(csvfile)

        writer.writerow(["Link"])

        for link in sorted(product_links):

            writer.writerow([link])

    print(
        f"Сохранено ссылок: "
        f"{len(product_links)}"
    )

except TimeoutException:

    print("Таймаут загрузки страницы.")

except Exception as e:

    print(f"Ошибка: {e}")

finally:

    driver.quit()

    print("Браузер закрыт.")
    print("Парсинг завершен.")