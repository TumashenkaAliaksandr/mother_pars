import os
import requests
from bs4 import BeautifulSoup
import csv
import hashlib

directory = 'templates/../../done_csv'
filename = 'serkyems.csv'
FILEPARAMS = os.path.join(directory, filename)


def create_csv(filename, order):
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        csv.writer(file).writerow(order)


def write_data_csv(filename, data):
    with open(filename, 'a', encoding='utf-8', newline='') as file:
        csv.DictWriter(file, fieldnames=list(data)).writerow(data)


def calculate_percentage(amounts):
    total_amount = sum(amounts)
    percentages = [(amount / total_amount) * 100 for amount in amounts]
    return percentages


def get_data(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find('h1', {'class': 'product-single__title'}).text.strip()

    price_element = soup.find('span', {'class': 'product-single__price'})
    price = round(float(price_element.text.replace('Rs.', '').replace(',', '').strip()) * 1.1, 2) if price_element else 'N/A'

    desc_container = soup.find('div', {'class': 'product-single__description'})
    desc = desc_container.text.strip() if desc_container else ''

    category = 'Serkyems'

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
        variation_prices = []

        percent_increase = 0.7  # Процент увеличения для каждой последующей вариации

        for i, variation_option in enumerate(variation_options):
            if variation_option.get('value'):
                variation_value = variation_option.text.strip()
                price_element = variation_option.find_previous('span', {'class': 'product-single__price'})
                variation_price = round(float(price_element.text.replace('Rs.', '').replace(',', '').strip()) * 1,
                                        2) if price_element else 'N/A'

                if i == 2:  # Index of the third variation
                    variation_price *= 0.7  # 0.7% decrease for the third variation

                if i > 0:
                    previous_price = float(variation_prices[i - 1])
                    variation_price += previous_price * percent_increase

                variation_prices.append(f'{variation_price:.2f}')

        for value, price in zip(variation_values, variation_prices):
            # Generate a unique hash for the identifier
            identifier = hashlib.sha256(url.encode('utf-8')).hexdigest()

            data = {
                'title': identifier,
                'id': title,
                'price': price,
                'description': formatted_text,
                'category': category,
                'image_urls': ', '.join(image_urls),
                'name_variations': variation_name,
                'values_variations': value,
                'price_variations': price
            }
            write_data_csv(FILEPARAMS, data)

def main():
    order = ['id', 'title', 'price', 'description', 'category', 'image_urls', 'name_variations',
             'values_variations']
    create_csv(FILEPARAMS, order)
    with open('templates/../../urls_csv/urls_folkbazar_serkyems.csv', 'r', encoding='utf-8') as file:
        for line in csv.DictReader(file):
            url = line['url']
            get_data(url)

if __name__ == '__main__':
    main()
