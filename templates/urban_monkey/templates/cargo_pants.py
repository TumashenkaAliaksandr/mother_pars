import os
import requests
from bs4 import BeautifulSoup
import csv
import re
import json
from urllib.parse import urlparse, parse_qs

def format_description(description, max_line_length=100):
    words = description.split()
    lines = []
    current_line = []

    for word in words:
        if len(' '.join(current_line + [word])) <= max_line_length:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]

    if current_line:
        lines.append(' '.join(current_line))

    formatted_description = '\n'.join(lines)
    return formatted_description

def create_csv(filename, order):
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        csv.writer(file).writerow(order)

def write_data_csv(filename, data):
    with open(filename, 'a', encoding='utf-8', newline='') as file:
        csv.DictWriter(file, fieldnames=list(data)).writerow(data)

def extract_id_from_script(html):
    script_text = re.search(r'<script type="application/json" class="pr_variants_json">(.*?)</script>', html, re.DOTALL)

    if script_text:
        script_content = script_text.group(1)
        script_data = json.loads(script_content)

        ids = [variant['id'] for variant in script_data]
        return ids
    else:
        return None

def extract_image_src(html):
    soup = BeautifulSoup(html, 'html.parser')
    img_elements = soup.find_all("div", class_="t4s-product__media")

    image_src_list = []

    for img_element in img_elements:
        img = img_element.find("img")
        if img and "src" in img.attrs:
            image_src = img["src"]
            # Удаляем первые два символа "//" перед "www" и часть "?v=1697874194&width=720"
            fixed_url = image_src[2:].split('?v=')[0]
            image_src_list.append(fixed_url)

    return image_src_list

def write_image_src_to_file(image_src_list, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for src in image_src_list:
            file.write(src + '\n')

def get_data(url, filename):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find("h1", class_="t4s-product__title").text.strip()
    print('Title:', title)

    category = "Cargo Pants"
    sub_category = 'Men’s New Blazers / Trench Coats'
    print('Category:', category)

    price = soup.find('div', class_="t4s-product-price").text.replace('Rs.', '').replace(',', '').replace('.00', '').strip()
    print('Price:', price)

    choose_color_elements = soup.find_all("h4", class_="t4s-pr-choose__title")
    choose_color_value = ""
    for element in choose_color_elements:
        if "Choose color:" in element.text:
            choose_color_value = element.text.replace("Choose color:", "").strip()
            print('Choose color:', choose_color_value)
            break

    size_elements = soup.select('script[type="application/json"].pr_options_json')[0]
    size_data = json.loads(size_elements.text)
    if size_data:
        sizes = size_data[0]["values"]
        print("Sizes:", ", ".join(sizes))

    tab_wrappers = soup.find_all("div", class_="t4s-tab-wrapper")
    tab_texts = {}

    for tab_wrapper in tab_wrappers:
        tab_title = tab_wrapper.find("span", class_="t4s-tab__text").text.strip()
        tab_content = tab_wrapper.find("div", class_="t4s-tab-content").text.strip()
        tab_texts[tab_title] = tab_content

    core_features_text = tab_texts.get("core features", "").replace(":", ":\n")
    description_text = tab_texts.get("description", "")
    shipping_returns_text = tab_texts.get("shipping & returns", "")
    care_guide_text = tab_texts.get("care guide", "")

    formatted_description = format_description(description_text)

    print("Core Features:")
    print(core_features_text)

    print("Description:")
    print(formatted_description)

    print("Shipping & Returns:")
    print(shipping_returns_text)

    print("Care Guide:")
    print(care_guide_text)

    product_id_element = soup.find("input", {"name": "product-id"})
    if product_id_element:
        product_id = product_id_element.get("value")
        print("Product ID:", product_id)
    else:
        print("Product ID not found.")


    image_src_list = extract_image_src(html)
    if image_src_list:
        print("Image Sources:")
        for src in image_src_list:
            print(src)

        write_image_src_to_file(image_src_list, "image_src.txt")


    data = {
        "Title": title,
        "Category": category,
        "Price": price,
        "Core Features": core_features_text,
        "Description": formatted_description,
        "Shipping & Returns": shipping_returns_text,
        "Care Guide": care_guide_text,
        "Photo Url": src,
        "Choose color": choose_color_value,
        "Sizes": " | ".join(sizes),
        "Product ID": product_id,
    }
    write_data_csv(filename, data)

def process_urls_csv(input_csv, output_csv):
    create_csv(output_csv, ["Title", "Category", "Price", "Core Features", "Description", "Shipping & Returns", "Care Guide", "Photo Url", "Choose color", "Sizes", "Product ID"])

    with open(input_csv, 'r', encoding='utf-8') as file:
        for line in csv.DictReader(file):
            url = line['url']
            get_data(url, output_csv)

if __name__ == "__main__":
    input_csv = 'templates/../../urls_csv/urls_urban_monkey.csv'
    output_csv = '../done_csv/cargo_pants.csv'

    process_urls_csv(input_csv, output_csv)


