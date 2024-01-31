import csv
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

url_base = "https://myatulya.com"
url = url_base + "/collections/hair-mask"

# Настройки Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Запуск в безголовом режиме (без GUI)

# Создаем экземпляр драйвера Chrome
driver = webdriver.Chrome(options=chrome_options)

# Получаем веб-страницу с помощью Selenium
driver.get(url)

# Ожидаем полной загрузки страницы (можно настроить таймаут при необходимости)
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "grid-product__link")))

# Прокручиваем страницу с помощью JavaScript для загрузки дополнительного контента
while True:
    # Захватываем текущий исходный код страницы
    page_source = driver.page_source

    # Парсим исходный код страницы с помощью BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Извлекаем ссылки на продукты
    product_links = []
    product_link_tags = soup.find_all('a', class_='grid-product__link')
    for product_link_tag in product_link_tags:
        href = product_link_tag.get('href')
        full_url = urljoin(url_base, href)
        product_links.append(full_url)

    # Прокручиваем страницу вниз с помощью JavaScript
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Ждем некоторое время перед следующей итерацией (можно настроить время ожидания)
    time.sleep(2)

    # Захватываем новый исходный код страницы
    new_page_source = driver.page_source

    # Проверяем, загружен ли новый контент
    if new_page_source == page_source:
        break

# Записываем ссылки в CSV файл
with open('../urls_csv/hair_mask_links.csv', 'w', newline='') as csvfile:
    fieldnames = ['url']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for link in product_links:
        writer.writerow({'url': link})

print("Ссылки успешно записаны в файл hair_mask_links.csv")

# Закрываем драйвер Selenium
driver.quit()
