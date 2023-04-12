import csv
import requests
from bs4 import BeautifulSoup
from selectolax.parser import HTMLParser


def get_data(url):
    html = requests.get(url).text
    tree = HTMLParser(html)  # Передаем в парсер html код

    title = tree.css_first('h1').text()
    params_table = tree.css_first('.shopify-section-product-template').css('tr')

    for row in params_table:
        name = row.css_first('th').text().strip()
        value = row.css_first('td').text().strip()
        print(title, name, value, sep=':')


def main():
    with open('urls.csv', 'r', encoding='utf-8') as file:
        for line in csv.DictReader(file):
            url = line['url']  # ключ
            get_data(url)
            break



if __name__ == "__main__":
    main()