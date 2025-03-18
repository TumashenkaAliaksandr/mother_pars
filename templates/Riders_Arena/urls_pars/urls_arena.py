# import requests
# from bs4 import BeautifulSoup
# import csv
#
# def get_product_links(url):
#     """
#     Извлекает ссылки на товары со страницы, анализируя HTML-код.
#     """
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # Поднимает исключение для плохих статусов (4xx или 5xx)
#     except requests.exceptions.RequestException as e:
#         print(f"Ошибка при запросе страницы: {e}")
#         return []
#
#     soup = BeautifulSoup(response.content, 'html.parser')
#     product_links = set()  # Используем множество для хранения уникальных ссылок
#
#     # Находим все div с классом "card__information"
#     card_divs = soup.find_all('div', class_='card__information')
#
#     for card_div in card_divs:
#         # Внутри каждого div ищем ссылку (<a>) с классом "full-unstyled-link"
#         a_tag = card_div.find('a', class_='full-unstyled-link')
#         if a_tag:
#             relative_url = a_tag.get('href')
#             # Проверяем, что ссылка не None и не пустая строка
#             if relative_url:
#                 # Формируем абсолютный URL, если ссылка относительная
#                 if relative_url.startswith('/'):
#                     absolute_url = f"https://ridersarena.com{relative_url}"
#                 else:
#                     absolute_url = relative_url
#                 product_links.add(absolute_url)  # Добавляем ссылку в множество
#
#     return list(product_links)  # Возвращаем список уникальных ссылок
#
# # Список URL коллекций
# collection_urls = [
#     "https://ridersarena.com/collections/helmets",
#     # "https://ridersarena.com/collections/jackets",
#     # "https://ridersarena.com/collections/riding-pants",
#     # "https://ridersarena.com/collections/gloves",
#     # "https://ridersarena.com/collections/shoes",
#     # "https://ridersarena.com/collections/armours",
#     # "https://ridersarena.com/collections/headwear",
#     # "https://ridersarena.com/collections/backrest-handle",
#     # "https://ridersarena.com/collections/bluetooth-intercom",
#     # "https://ridersarena.com/collections/body-cover",
#     # "https://ridersarena.com/collections/horns",
#     # "https://ridersarena.com/collections/indicators",
#     # "https://ridersarena.com/collections/luggage",
#     # "https://ridersarena.com/collections/lights-ancillaries",
#     # "https://ridersarena.com/collections/mobile-holders-1",
#     # "https://ridersarena.com/collections/tyre-inflators",
#     # "https://ridersarena.com/collections/tank-pads",
#     # 'https://ridersarena.com/collections/engine-oil',
#     # "https://ridersarena.com/collections/polish",
#     # "https://ridersarena.com/collections/ceramic-brake-pads",
#     # "https://ridersarena.com/collections/chain-kits",
#     # "https://ridersarena.com/collections/chain-lube",
#     # "https://ridersarena.com/collections/engine-oil-1",
#     # "https://ridersarena.com/collections/exhausts",
#     # "https://ridersarena.com/collections/iridium-spark-plugs",
#     # "https://ridersarena.com/collections/microfibre-cloth",
#     # "https://ridersarena.com/collections/polish",
#     # "https://ridersarena.com/collections/batteries-for-superbikes",
#     # "https://ridersarena.com/collections/cable-lock",
#     # "https://ridersarena.com/collections/disc-lock",
#     # "https://ridersarena.com/collections/gps-devices",
#     # "https://ridersarena.com/collections/flashx",
#     # "https://ridersarena.com/collections/obd-scanner",
#     # "https://ridersarena.com/collections/scale-models",
#     # "https://ridersarena.com/collections/tyres",
#     # "https://ridersarena.com/collections/axor",
#     # "https://ridersarena.com/collections/amaroq",
#     # "https://ridersarena.com/collections/apollo-tyres",
#     # "https://ridersarena.com/collections/auto-engina",
#     # "https://ridersarena.com/collections/bluarmor",
#     # "https://ridersarena.com/collections/bobo",
#     # "https://ridersarena.com/collections/carbanado",
#     # "https://ridersarena.com/collections/crank1",
#     # "https://ridersarena.com/collections/flashx",
#     # "https://ridersarena.com/collections/hjg",
#     # "https://ridersarena.com/collections/ht-exhaust",
#     # "https://ridersarena.com/collections/innovv",
#     # "https://ridersarena.com/collections/lazyassbikers",
#     # "https://ridersarena.com/collections/k-n",
#     # "https://ridersarena.com/collections/korda",
#     # "https://ridersarena.com/collections/liquimoly",
#     # "https://ridersarena.com/collections/ls2-helmets",
#     # "https://ridersarena.com/collections/maddog",
#     # "https://ridersarena.com/collections/minda",
#     # "https://ridersarena.com/collections/moto-torque",
#     # "https://ridersarena.com/collections/motulzone",
#     # "https://ridersarena.com/collections/mt",
#     # "https://ridersarena.com/collections/mytvs",
#     # "https://ridersarena.com/collections/iridium-spark-plugs",
#     # "https://ridersarena.com/collections/one-lap",
#     # "https://ridersarena.com/collections/raida-1",
#     # "https://ridersarena.com/collections/orazo",
#     # "https://ridersarena.com/collections/rev-it",
#     # "https://ridersarena.com/collections/parani",
#     # "https://ridersarena.com/collections/putoline",
#     # "https://ridersarena.com/collections/reise",
#     # "https://ridersarena.com/collections/rolon-premium",
#     # "https://ridersarena.com/collections/sena",
#     # "https://ridersarena.com/collections/solace",
#     # "https://ridersarena.com/collections/steelbird",
#     # "https://ridersarena.com/collections/studds",
#     # "https://ridersarena.com/collections/smk",
#     # "https://ridersarena.com/collections/tirewell",
#     # "https://ridersarena.com/collections/vardenchi-1",
#     # "https://ridersarena.com/collections/vega",
#     # "https://ridersarena.com/collections/vesrah",
#     # "https://ridersarena.com/collections/vista",
#     # "https://ridersarena.com/collections/waxpol",
#     # "https://ridersarena.com/collections/splendor",
#     # "https://ridersarena.com/collections/xpulse",
#     # "https://ridersarena.com/collections/rc200",
#     # "https://ridersarena.com/collections/rc390",
#     # "https://ridersarena.com/collections/duke-200",
#     # "https://ridersarena.com/collections/duke-250",
#     # "https://ridersarena.com/collections/390-adventure",
#     # "https://ridersarena.com/collections/450-450-x",
#     # "https://ridersarena.com/collections/440x",
#     # "https://ridersarena.com/collections/activa",
#     # "https://ridersarena.com/collections/cb200-x",
#     # "https://ridersarena.com/collections/cb-300r",
#     # "https://ridersarena.com/collections/hiness",
#     # "https://ridersarena.com/collections/shine",
#     # "https://ridersarena.com/collections/r15-v2-v3",
#     # "https://ridersarena.com/collections/r15-v4",
#     # "https://ridersarena.com/collections/mt-15",
#     # "https://ridersarena.com/collections/fz-v3",
#     # "https://ridersarena.com/collections/fz-x",
#     # "https://ridersarena.com/collections/s1-s1-pro",
#     # "https://ridersarena.com/collections/classic-350",
#     # "https://ridersarena.com/collections/hunter-350",
#     # "https://ridersarena.com/collections/himalayam",
#     # "https://ridersarena.com/collections/himalayan-450",
#     # "https://ridersarena.com/collections/interceptor",
#     # "https://ridersarena.com/collections/meteor",
#     # "https://ridersarena.com/collections/super-meteor-650",
#     # "https://ridersarena.com/collections/apache-rtr-160-200-4v",
#     # "https://ridersarena.com/collections/iqube",
#     # "https://ridersarena.com/collections/ronin-225",
#     # "https://ridersarena.com/collections/rr-310",
#     # "https://ridersarena.com/collections/rtr-310",
#     # "https://ridersarena.com/collections/g310-gs",
#     # "https://ridersarena.com/collections/dominar",
#     # "https://ridersarena.com/collections/pulsar-220",
#     # "https://ridersarena.com/collections/tnt-300",
#     # "https://ridersarena.com/collections/speed-400",
#
# ]
#
# # Создаем пустое множество для хранения всех уникальных ссылок на товары
# all_product_links = set()
#
# # Перебираем все URL коллекций и получаем ссылки на товары с каждой страницы
# for url in collection_urls:
#     product_links = get_product_links(url)
#
#     if product_links:
#         all_product_links.update(product_links)  # Обновляем множество уникальными ссылками
#         print(f"Найдено {len(product_links)} уникальных ссылок на товары на странице {url}")
#     else:
#         print(f"Не удалось найти ссылки на товары на странице {url}")
#
# # Записываем все найденные уникальные ссылки на товары в CSV файл
# if all_product_links:
#     csv_filename = "../urls_csv/product_links.csv"
#     with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(['Ссылка на товар'])  # Записываем заголовок
#
#         for link in all_product_links:
#             writer.writerow([link])  # Записываем каждую ссылку в новую строку
#
#     print(f"\nВсего найдено {len(all_product_links)} уникальных ссылок на товары.")
#     print(f"Ссылки записаны в файл {csv_filename}")
# else:
#     print("Не удалось найти ни одной ссылки на товары.")
import requests
from bs4 import BeautifulSoup
import csv


def get_product_links_with_pagination(base_url, max_pages=10):
    """
    Извлекает ссылки на товары с учетом пагинации.

    :param base_url: Базовый URL коллекции.
    :param max_pages: Максимальное количество страниц для обхода.
    :return: Список уникальных ссылок на товары.
    """
    product_links = set()  # Используем множество для хранения уникальных ссылок

    for page_num in range(1, max_pages + 1):
        url = f"{base_url}?page={page_num}"  # Формируем URL для текущей страницы
        print(f"Обрабатываем страницу: {url}")

        try:
            response = requests.get(url)
            response.raise_for_status()  # Проверяем успешность запроса
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе страницы {url}: {e}")
            continue

        soup = BeautifulSoup(response.content, 'html.parser')

        # Находим все div с классом "card__information"
        card_divs = soup.find_all('div', class_='card__information')

        if not card_divs:
            print(f"Страница {url} пуста или достигнут конец пагинации.")
            break  # Если на странице нет товаров, выходим из цикла

        for card_div in card_divs:
            # Внутри каждого div ищем ссылку (<a>) с классом "full-unstyled-link"
            a_tag = card_div.find('a', class_='full-unstyled-link')
            if a_tag:
                relative_url = a_tag.get('href')
                if relative_url:
                    # Формируем абсолютный URL, если ссылка относительная
                    if relative_url.startswith('/'):
                        absolute_url = f"https://ridersarena.com{relative_url}"
                    else:
                        absolute_url = relative_url
                    product_links.add(absolute_url)  # Добавляем ссылку в множество

    return list(product_links)


# Список URL коллекций
collection_urls = [
    "https://ridersarena.com/collections/helmets",
    "https://ridersarena.com/collections/jackets",
    "https://ridersarena.com/collections/riding-pants",
    "https://ridersarena.com/collections/gloves",
    "https://ridersarena.com/collections/shoes",
    "https://ridersarena.com/collections/armours",
    "https://ridersarena.com/collections/headwear",
    "https://ridersarena.com/collections/backrest-handle",
    "https://ridersarena.com/collections/bluetooth-intercom",
    "https://ridersarena.com/collections/body-cover",
    "https://ridersarena.com/collections/horns",
    "https://ridersarena.com/collections/indicators",
    "https://ridersarena.com/collections/luggage",
    "https://ridersarena.com/collections/lights-ancillaries",
    "https://ridersarena.com/collections/mobile-holders-1",
    "https://ridersarena.com/collections/tyre-inflators",
    "https://ridersarena.com/collections/tank-pads",
    'https://ridersarena.com/collections/engine-oil',
    "https://ridersarena.com/collections/polish",
    "https://ridersarena.com/collections/ceramic-brake-pads",
    "https://ridersarena.com/collections/chain-kits",
    "https://ridersarena.com/collections/chain-lube",
    "https://ridersarena.com/collections/engine-oil-1",
    "https://ridersarena.com/collections/exhausts",
    "https://ridersarena.com/collections/iridium-spark-plugs",
    "https://ridersarena.com/collections/microfibre-cloth",
    "https://ridersarena.com/collections/polish",
    "https://ridersarena.com/collections/batteries-for-superbikes",
    "https://ridersarena.com/collections/cable-lock",
    "https://ridersarena.com/collections/disc-lock",
    "https://ridersarena.com/collections/gps-devices",
    "https://ridersarena.com/collections/flashx",
    "https://ridersarena.com/collections/obd-scanner",
    "https://ridersarena.com/collections/scale-models",
    "https://ridersarena.com/collections/tyres",
    "https://ridersarena.com/collections/axor",
    "https://ridersarena.com/collections/amaroq",
    "https://ridersarena.com/collections/apollo-tyres",
    "https://ridersarena.com/collections/auto-engina",
    "https://ridersarena.com/collections/bluarmor",
    "https://ridersarena.com/collections/bobo",
    "https://ridersarena.com/collections/carbanado",
    "https://ridersarena.com/collections/crank1",
    "https://ridersarena.com/collections/flashx",
    "https://ridersarena.com/collections/hjg",
    "https://ridersarena.com/collections/ht-exhaust",
    "https://ridersarena.com/collections/innovv",
    "https://ridersarena.com/collections/lazyassbikers",
    "https://ridersarena.com/collections/k-n",
    "https://ridersarena.com/collections/korda",
    "https://ridersarena.com/collections/liquimoly",
    "https://ridersarena.com/collections/ls2-helmets",
    "https://ridersarena.com/collections/maddog",
    "https://ridersarena.com/collections/minda",
    "https://ridersarena.com/collections/moto-torque",
    "https://ridersarena.com/collections/motulzone",
    "https://ridersarena.com/collections/mt",
    "https://ridersarena.com/collections/mytvs",
    "https://ridersarena.com/collections/iridium-spark-plugs",
    "https://ridersarena.com/collections/one-lap",
    "https://ridersarena.com/collections/raida-1",
    "https://ridersarena.com/collections/orazo",
    "https://ridersarena.com/collections/rev-it",
    "https://ridersarena.com/collections/parani",
    "https://ridersarena.com/collections/putoline",
    "https://ridersarena.com/collections/reise",
    "https://ridersarena.com/collections/rolon-premium",
    "https://ridersarena.com/collections/sena",
    "https://ridersarena.com/collections/solace",
    "https://ridersarena.com/collections/steelbird",
    "https://ridersarena.com/collections/studds",
    "https://ridersarena.com/collections/smk",
    "https://ridersarena.com/collections/tirewell",
    "https://ridersarena.com/collections/vardenchi-1",
    "https://ridersarena.com/collections/vega",
    "https://ridersarena.com/collections/vesrah",
    "https://ridersarena.com/collections/vista",
    "https://ridersarena.com/collections/waxpol",
    "https://ridersarena.com/collections/splendor",
    "https://ridersarena.com/collections/xpulse",
    "https://ridersarena.com/collections/rc200",
    "https://ridersarena.com/collections/rc390",
    "https://ridersarena.com/collections/duke-200",
    "https://ridersarena.com/collections/duke-250",
    "https://ridersarena.com/collections/390-adventure",
    "https://ridersarena.com/collections/450-450-x",
    "https://ridersarena.com/collections/440x",
    "https://ridersarena.com/collections/activa",
    "https://ridersarena.com/collections/cb200-x",
    "https://ridersarena.com/collections/cb-300r",
    "https://ridersarena.com/collections/hiness",
    "https://ridersarena.com/collections/shine",
    "https://ridersarena.com/collections/r15-v2-v3",
    "https://ridersarena.com/collections/r15-v4",
    "https://ridersarena.com/collections/mt-15",
    "https://ridersarena.com/collections/fz-v3",
    "https://ridersarena.com/collections/fz-x",
    "https://ridersarena.com/collections/s1-s1-pro",
    "https://ridersarena.com/collections/classic-350",
    "https://ridersarena.com/collections/hunter-350",
    "https://ridersarena.com/collections/himalayam",
    "https://ridersarena.com/collections/himalayan-450",
    "https://ridersarena.com/collections/interceptor",
    "https://ridersarena.com/collections/meteor",
    "https://ridersarena.com/collections/super-meteor-650",
    "https://ridersarena.com/collections/apache-rtr-160-200-4v",
    "https://ridersarena.com/collections/iqube",
    "https://ridersarena.com/collections/ronin-225",
    "https://ridersarena.com/collections/rr-310",
    "https://ridersarena.com/collections/rtr-310",
    "https://ridersarena.com/collections/g310-gs",
    "https://ridersarena.com/collections/dominar",
    "https://ridersarena.com/collections/pulsar-220",
    "https://ridersarena.com/collections/tnt-300",
    "https://ridersarena.com/collections/speed-400",
    # Добавьте другие URL коллекций по мере необходимости
]

# Создаем пустое множество для хранения всех уникальных ссылок на товары
all_product_links = set()

# Перебираем все URL коллекций и получаем ссылки на товары с каждой страницы
for url in collection_urls:
    product_links = get_product_links_with_pagination(url, max_pages=10)  # Укажите максимальное количество страниц

    if product_links:
        all_product_links.update(product_links)  # Обновляем множество уникальными ссылками
        print(f"Найдено {len(product_links)} уникальных ссылок на товары для коллекции {url}")
    else:
        print(f"Не удалось найти ссылки на товары для коллекции {url}")

# Записываем все найденные уникальные ссылки на товары в CSV файл
if all_product_links:
    csv_filename = "../urls_csv/product_links.csv"
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Ссылка на товар'])  # Записываем заголовок

        for link in all_product_links:
            writer.writerow([link])  # Записываем каждую ссылку в новую строку

    print(f"\nВсего найдено {len(all_product_links)} уникальных ссылок на товары.")
    print(f"Ссылки записаны в файл {csv_filename}")
else:
    print("Не удалось найти ни одной ссылки на товары.")
