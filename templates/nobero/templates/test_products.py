import os
import re
import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urlparse, parse_qs

directory = 'templates/../../done_csv'
filename = 't_shirts.csv'
FILEPARAMS = os.path.join(directory, filename)

def create_csv(filename, order):
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        csv.writer(file).writerow(order)

def write_data_csv(filename, data):
    with open(filename, 'a', encoding='utf-8', newline='') as file:
        csv.DictWriter(file, fieldnames=list(data)).writerow(data)

def get_data(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    variant_id = query_params.get('variant', [''])[0]
    print(variant_id)

    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    title_element = soup.find('h1', {'class': 'capitalize'})
    title = title_element.text.strip() if title_element and title_element.text.strip() != 'Default Title' else ''
    price_element = soup.find('h2', {'id': 'variant-price'})
    price = price_element.text.replace('₹', '').strip()
    print(title, price)

    desc_container = soup.find('details', {'class': 'filter-group'})
    desc = desc_container.text.strip() if desc_container else ''
    print(desc)

    category = 'T-shirts'

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

    variation_elements = soup.select('select.single-option-selector option')
    size_element = soup.find('span', class_='md:text-xl')
    size_title = size_element.text.strip() if size_element else ''
    print(size_title)

    select_color_element = soup.find('div', class_='capitalize pb-4 flex justify-between items-center')
    sel_color = select_color_element.next_sibling.text.strip() if select_color_element else ''
    print(sel_color)

    selected_color_element = soup.find('span', {'id': 'selected-color-title'})
    sel_color_el = selected_color_element.text.strip() if selected_color_element else ''

    if selected_color_element:
        sel_color = selected_color_element.text.strip()
    else:
        sel_color = ''

    size_element = soup.find('input', {'class': 'size-select-input'})
    vari = size_element['value']
    print(vari, sel_color_el, variation_elements)

    variations = []
    for i, variation_element in enumerate(variation_elements):
        variation_title = ''
        if i < len(variation_elements):
            variation_title_element = variation_elements[i].find('label')
            if variation_title_element:
                variation_title = variation_title_element.text.strip()

        variation_name = re.sub(r'Rs[.,0-9\s]*|[^a-zA-Z0-9\s]', '', variation_element.text.strip())
        variation_value = variation_element['value']
        variation_price = variation_element.text.replace('Rs.', '').strip()

        variations.append({
            'title': variation_title,
            'name': variation_name,
            'value': variation_value,
            'price': variation_price
        })

        image_elements = soup.select('img.image-placeholder-bg')
        image_urls = ['http:' + img['src'] for img in image_elements]
        print(image_urls, variations)

        for variation in variations:
            data = {
                'title': title,
                'price': variation['price'],
                'description': formatted_text,
                'category': category,
                'image_urls': ', '.join(image_urls),
                'variation_titles': variation['title'],
                'name_variations': variation['name'],
                'variations_price': variation['price'],
                'id': variation['value'],
                'variant_id': variant_id
            }

            write_data_csv(FILEPARAMS, data)

    def main():
        order = ['title', 'price', 'description', 'category', 'image_urls', 'variation_titles', 'name_variations',
                 'variations_price', 'id', 'variant_id']  # Добавляем 'variant_id' в порядок полей
        create_csv(FILEPARAMS, order)
        with open('templates/../../urls_csv/test_pick_printed_t_shirts.csv', 'r', encoding='utf-8') as file:
            for line in csv.DictReader(file):
                url = line['url']
                get_data(url)

    if __name__ == '__main__':
        main()
