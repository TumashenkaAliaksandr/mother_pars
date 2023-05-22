import os
import requests
from bs4 import BeautifulSoup
import csv

directory = 'templates/../done_csv'
filename = 'butter_lamps.csv'
FILEPARAMS = os.path.join(directory, filename)


def create_csv(filename, order):
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        csv.DictWriter(file, fieldnames=order).writeheader()


def write_data_csv(filename, data):
    with open(filename, 'a', encoding='utf-8', newline='') as file:
        csv.DictWriter(file, fieldnames=list(data)).writerow(data)


def get_data(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find('h1', {'class': 'product-single__title'}).text.strip()

    price_element = soup.find('span', {'class': 'product-single__price'})
    price = round(float(price_element.text.replace('Rs.', '').replace(',', '').strip()) * 1.1, 2) if price_element else 'N/A'

    desc_container = soup.find('div', {'class': 'product-single__description'})
    desc = desc_container.text.strip() if desc_container else ''

    category = 'Butter-lamps'

    lines = []
    current_line = ''
    for word in desc.split():
        if len(current_line + ' ' + word) > 100:
            lines.append(current_line)
            current_line = word
        else:
            current_line += ' ' + word
    if current_line:
        lines.append(current_line)
    formatted_text = '\n'.join(lines)

    image_elements = soup.select('a.js-modal-open-product-modal.product__photo-wrapper-product-template')
    image_urls = ['http:' + img["href"] for img in image_elements]

    variations = []
    variation_elements = soup.select('div.selector-wrapper.js.product-form__item')
    for variation_element in variation_elements:
        variation_name = variation_element.find('label').text.strip()
        variation_options = variation_element.find_all('option')
        variation_values = [option.text.strip() for option in variation_options if option.get('value')]
        variation_data = {'name': variation_name, 'values': variation_values}
        variations.append(variation_data)

    name_variations = [variation['name'] for variation in variations]
    values_variations = [', '.join(variation['values']) for variation in variations]

    price_variations = []
    for variation_option in variation_options:
        if variation_option.get('value'):
            variation_value = variation_option.text.strip()
            price_element = variation_option.find_previous('span', {'class': 'product-single__price'})
            variation_price = round(float(price_element.text.replace('Rs.', '').replace(',', '').strip()) * 1.1, 2) if price_element else 'N/A'
            price_variations.append(f'{variation_value}: {variation_price}')

    data = {
        'title': title,
        'price': price,
        'description': formatted_text,
        'category': category,
        'image_urls': ', '.join(image_urls),
        'name_variations': ', '.join(name_variations),
        'values_variations': ', '.join(values_variations),
        'price_variations': ', '.join(price_variations)
    }

    write_data_csv(FILEPARAMS, data)


def main():
    order = ['title', 'price', 'description', 'category', 'image_urls', 'name_variations', 'values_variations',
             'price_variations']
    create_csv(FILEPARAMS, order)
    with open('templates/../urls_csv/urls_folkbazar_butter_lamps.csv', 'r', encoding='utf-8') as file:
        for line in csv.DictReader(file):
            url = line['url']
            get_data(url)


if __name__ == '__main__':
    main()
