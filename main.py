import requests
from bs4 import BeautifulSoup
from selectolax.parser import HTMLParser
import csv


def get_data(url):
    html = requests.get(url).text
    tree = HTMLParser(html)

    title = tree.css_first('h1').text().strip()
    params_cost = tree.css_first('.kit-ideal-consumption').css('div')
    params_discount = tree.css_first('.product-discount').css('div')
    params_info = tree.css_first('.padded-container-content').css('div')
    params_desc = tree.css_first('.product-intro-description').css('div')
    print(title)
    for row in params_cost:
        cost = row.css_first('div').text().strip()
        print(cost)

    for row in params_discount:
        discount = row.css_first('strong').text().strip()
        disc_cost = row.css_first('em').text().strip()
        print(discount, disc_cost)

    for row in params_info:
        info_text = row.text().strip()
        for info_line in info_text.split('\n'):
            print(info_line.lstrip())

    for row in params_desc:
        info_one = row.css_first('div').text().strip()
        lines = [info_one[i:i + 50] for i in range(0, len(info_one), 50)]
        formatted_text = '\n'.join(lines)
        print('\n', 'Description:', '\n', formatted_text)


def main():
    with open('urls_solar.csv', 'r', encoding='utf-8') as file:
        for line in csv.DictReader(file):
            url = line['url']
            get_data(url)



if __name__ == '__main__':
    main()