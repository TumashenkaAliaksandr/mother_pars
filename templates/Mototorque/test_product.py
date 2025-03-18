import requests
from bs4 import BeautifulSoup
import csv
import uuid

# Список категорий и подкатегорий
categories = {
    'ACCESSORIES': {
        'keywords': ['accessories'],
        'subcategories': ['guard']
    },
    'GEARS': {
        'keywords': ['gears'],
        'subcategories': []
    },
    'JACKETS': {
        'keywords': ['jacket'],
        'subcategories': []
    },
    'AIRSPEED': {
        'keywords': ['airspeed'],
        'subcategories': []
    },
    'PANTS': {
        'keywords': ['pants'],
        'subcategories': []
    },
    'GLOVES': {
        'keywords': ['gloves'],
        'subcategories': []
    },
    'BOOTS': {
        'keywords': ['boots'],
        'subcategories': []
    },
    'PERFORMANCE EXHAUSTS': {
        'keywords': ['performance exhausts'],
        'subcategories': []
    },
    'BOLTS': {
        'keywords': ['bolts', 'bolt']
    },
    'OIL': {
        'keywords': ['oil']
    },
    'CRASH GUARDS': {
        'keywords': ['guard'],
        'subcategories': []
    }
}


def get_product_data(url):
    print(f"Обработка страницы: {url}")
    try:
        response = requests.get(url)
        print(f"Код ответа: {response.status_code}")
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Название
        title = soup.find('h1', class_='product__title')
        title = title.text.strip().lower() if title else "Название не найдено"
        print(f"Название: {title}")

        # Цена
        price_tag = soup.find('span', class_='price-item--regular')
        price = price_tag.text.strip().replace("Rs.", "").replace(" ", "") if price_tag else "Цена не найдена"
        print(f"Цена: {price}")

        # Описание
        description, material, tools_required, warranty, design = "", "", "", "", ""
        description_divs = soup.find_all('div', class_='product__description rte')

        for description_div in description_divs:
            if description_div:
                print("Найден блок описания.")

                # Если есть <ul>, обрабатываем как список
                if description_div.find('ul'):
                    ul = description_div.find('ul')
                    for li in ul.find_all('li'):
                        description += li.text.strip() + "\n"

                # Если есть <p> с <strong>, обрабатываем как текст с p и strong
                elif description_div.find('strong'):
                    for element in description_div.find_all(['p', 'li']):
                        strong_tag = element.find('strong')
                        if strong_tag:
                            strong_text = strong_tag.text.strip()
                            if strong_text == "DESCRIPTION":
                                next_p = element.find_next('ul')
                                if next_p:
                                    for li in next_p.find_all('li'):
                                        description += li.text.strip() + "\n"
                            elif strong_text == "Material":
                                material = element.find_next('p').text.strip() if element.find_next('p') else ""
                            elif strong_text == "TOOLS REQUIRED":
                                tools_required = element.find_next('p').text.strip() if element.find_next('p') else ""
                            elif strong_text == "WARRANTY":
                                warranty = element.find_next('p').text.strip() if element.find_next('p') else ""
                            elif strong_text == "DESIGN & PRODUCT OUTLOOK":
                                design = element.find_next('p').text.strip() if element.find_next('p') else ""
                        else:
                            description += element.text.strip() + "\n"

                # Если нет ни <ul>, ни <p> с <strong>, записываем все в описание
                else:
                    for element in description_div.find_all(['p', 'li']):
                        description += element.text.strip() + "\n"
            else:
                print("Блок описания не найден.")

        # Категория и подкатегория
        category = None
        subcategory = None

        # Сначала ищем в названии
        for cat, info in categories.items():
            if any(keyword in title for keyword in info['keywords']):
                category = cat
                if 'subcategories' in info:
                    for sub in info['subcategories']:
                        if sub in title:
                            subcategory = sub
                            break
                break

        # Если не нашли в названии, ищем в описании
        if not category:
            for cat, info in categories.items():
                if any(keyword in description.lower() for keyword in info['keywords']):
                    category = cat
                    if 'subcategories' in info:
                        for sub in info['subcategories']:
                            if sub in description.lower():
                                subcategory = sub
                                break
                    break

        if category:
            print(f"Категория: {category}")
        else:
            print("Категория не определена.")
        if subcategory:
            print(f"Подкатегория: {subcategory}")
        else:
            print("Подкатегория не определена.")

        # Размеры
        sizes = []
        variant_radios = soup.find('variant-radios')
        if variant_radios:
            labels = variant_radios.find_all('label')
            for label in labels:
                size = label.text.strip()
                sizes.append(size)
                print(f"Найден размер: {size}")
        else:
            print("Размеры не найдены.")

        # Изображения
        image_urls = set()  # Используем set для уникальных URL
        media_wrapper = soup.find('div', class_='grid__item product__media-wrapper')
        if media_wrapper:
            imgs = media_wrapper.find_all('img')
            for img in imgs:
                image_url = img.get('src')
                if image_url:
                    if '?' in image_url:
                        image_url = image_url.split('?')[0]  # Удаляем префиксы
                    if not image_url.startswith('http'):
                        image_url = 'https:' + image_url
                    if '_84x84' not in image_url:  # Исключаем изображения размером 84x84
                        # Удаляем размеры из имени файла, оставляя номера
                        filename = image_url.split('/')[-1]
                        parts = filename.split('_')
                        if len(parts) > 2 and parts[-1].endswith('.jpg'):
                            base_name = '_'.join(parts[:-1]) + '.jpg'
                            normalized_url = '/'.join(image_url.split('/')[:-1]) + '/' + base_name
                        else:
                            normalized_url = image_url
                        # Проверка на повторение
                        if normalized_url not in image_urls:
                            image_urls.add(normalized_url)  # Добавляем в set
                            print(f"Найдено изображение: {normalized_url}")
        else:
            print("Блок изображений не найден.")

        # Короткий ID
        product_id = str(uuid.uuid4())[:8]
        print(f"Случайный ID: {product_id}")

        return {
            'title': title,
            'price': price,
            'description': description,
            'material': material,
            'tools_required': tools_required,
            'warranty': warranty,
            'design': design,
            'category': category,
            'subcategory': subcategory,
            'sizes': ', '.join(sizes),  # Сохраняем размеры через запятую
            'image_urls': ', '.join(image_urls),  # Сохраняем уникальные ссылки через запятую
            'product_url': url,
            'product_id': product_id
        }

    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None
    except Exception as e:
        print(f"Ошибка при парсинге: {e}")
        return None


def save_to_csv(data, filename):
    if not data:
        print("Нет данных для записи.")
        return

    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"Данные успешно сохранены в {filename}")
    except Exception as e:
        print(f"Ошибка при записи в CSV: {e}")


# Пример использования
product_urls = [
    'https://mototorque.in/products/guardian',
    'https://mototorque.in/products/hulk',
    'https://mototorque.in/products/evo-v3-0-grey'
    # Добавьте другие URL сюда
]

all_product_data = []
for url in product_urls:
    product_data = get_product_data(url)
    if product_data:
        all_product_data.append(product_data)

save_to_csv(all_product_data, 'mototorque_product.csv')
