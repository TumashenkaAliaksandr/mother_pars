import requests
from bs4 import BeautifulSoup
import csv

def extract_product_links(url):
    links = []
    page_num = 1
    base_url = 'https://www.honeyhut.in'
    while True:
        response = requests.get(url + f'?page={page_num}')
        if response.status_code != 200:
            break
        soup = BeautifulSoup(response.text, 'html.parser')
        products = soup.find_all('div', class_='card-wrapper')
        if not products:
            break
        for product in products:
            link = product.find('a').get('href')
            full_link = base_url + link
            links.append(full_link)
        page_num += 1
    return links

def save_to_csv(links, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['url'])
        for link in links:
            writer.writerow([link])

url = 'https://www.honeyhut.in/collections/all'
product_links = extract_product_links(url)

csv_filename = '../urls_csv/product_links.csv'
save_to_csv(product_links, csv_filename)
print(f"Ссылки успешно сохранены в файл '{csv_filename}'")
