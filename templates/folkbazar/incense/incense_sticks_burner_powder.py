import os
import re
import csv
import hashlib
import requests
from bs4 import BeautifulSoup

directory = 'templates/../../done_csv'
filename = 'no_var_incense_sticks_burner_powder.csv'
FILEPARAMS = os.path.join(directory, filename)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
}


def create_csv(filename, order):
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        csv.writer(file).writerow(order)


def write_data_csv(filename, data):
    with open(filename, 'a', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=list(data.keys()))
        writer.writerow(data)


def safe_get(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        if r.status_code != 200:
            return None
        return r.text
    except:
        return None


def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip() if text else ''


def get_data(url):
    html = safe_get(url)
    if not html:
        print(f"⛔ skip (no response): {url}")
        return

    soup = BeautifulSoup(html, 'html.parser')

    # ---------------- TITLE ----------------
    title = ''
    h1 = soup.find('h1')
    if h1:
        title = clean_text(h1.get_text())

    # ---------------- DESCRIPTION ----------------
    desc_block = (
        soup.select_one('.product-single__description') or
        soup.select_one('.product__description') or
        soup.select_one('.description')
    )

    desc = clean_text(desc_block.get_text()) if desc_block else ''

    category = 'Incense Sticks'

    # ---------------- IMAGES ----------------
    images = set()

    # modern Shopify images
    for img in soup.select('img'):
        src = img.get('src') or img.get('data-src')
        if src and ('shopify' in src or 'cdn' in src):
            if src.startswith('//'):
                src = 'https:' + src
            images.add(src)

    image_urls = ', '.join(list(images)[:8])

    # ---------------- VARIATIONS ----------------
    variation_elements = soup.select('select option')
    variation_wrappers = soup.select('div.selector-wrapper')

    if not variation_elements:
        variation_elements = soup.select('[data-value] option')

    for i, variation_element in enumerate(variation_elements):

        text = clean_text(variation_element.text)

        if not text:
            continue

        variation_name = re.sub(r'Rs[.,0-9\s]*|[^a-zA-Z0-9\s]', '', text).strip()
        variation_value = variation_element.get('value', '')

        # price fallback
        price_match = re.findall(r'[\d,.]+', text)
        variation_price = price_match[0] if price_match else '0'

        variation_title = ''
        if i < len(variation_wrappers):
            label = variation_wrappers[i].find('label')
            if label:
                variation_title = clean_text(label.text)

        identifier = hashlib.sha256(url.encode('utf-8')).hexdigest()

        data = {
            'identifier': identifier,
            'title': title,
            'price': variation_price,
            'description': desc,
            'category': category,
            'image_urls': image_urls,
            'variation_titles': variation_title,
            'name_variations': variation_name,
            'variations_price': variation_price,
            'id': variation_value
        }

        write_data_csv(FILEPARAMS, data)


def main():
    order = [
        'identifier', 'title', 'price', 'description', 'category',
        'image_urls', 'variation_titles', 'name_variations',
        'variations_price', 'id'
    ]

    create_csv(FILEPARAMS, order)

    with open('templates/../../urls_csv/urls_folkbazar_novariations.csv',
              'r', encoding='utf-8') as file:

        for line in csv.DictReader(file):
            url = line.get('url')
            if url:
                print("➡", url)
                get_data(url)


if __name__ == '__main__':
    main()