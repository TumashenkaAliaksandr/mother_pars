import requests
from bs4 import BeautifulSoup


def get_product_links(url):
    """
    Извлекает ссылки на товары со страницы, анализируя HTML-код.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Поднимает исключение для плохих статусов (4xx или 5xx)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе страницы: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    product_links = set()  # Используем множество для хранения уникальных ссылок

    # Находим все div с классом "card__information"
    card_divs = soup.find_all('div', class_='card__information')

    for card_div in card_divs:
        # Внутри каждого div ищем ссылку (<a>) с классом "full-unstyled-link"
        a_tag = card_div.find('a', class_='full-unstyled-link')
        if a_tag:
            relative_url = a_tag.get('href')
            # Проверяем, что ссылка не None и не пустая строка
            if relative_url:
                # Формируем абсолютный URL, если ссылка относительная
                if relative_url.startswith('/'):
                    absolute_url = f"https://ridersarena.com{relative_url}"
                else:
                    absolute_url = relative_url
                product_links.add(absolute_url)  # Добавляем ссылку в множество

    return list(product_links)  # Возвращаем список уникальных ссылок


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

]

# Создаем пустое множество для хранения всех уникальных ссылок на товары
all_product_links = set()

# Перебираем все URL коллекций и получаем ссылки на товары с каждой страницы
for url in collection_urls:
    product_links = get_product_links(url)

    if product_links:
        all_product_links.update(product_links)  # Обновляем множество уникальными ссылками
        print(f"Найдено {len(product_links)} уникальных ссылок на товары на странице {url}")
    else:
        print(f"Не удалось найти ссылки на товары на странице {url}")

# Выводим все найденные уникальные ссылки на товары
if all_product_links:
    print("\nВсе найденные уникальные ссылки на товары:")

    for link in all_product_links:
        print(link)

    print(f"\nВсего найдено {len(all_product_links)} уникальных ссылок на товары.")
else:
    print("Не удалось найти ни одной ссылки на товары.")
