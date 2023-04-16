import gettext

import requests
from bs4 import BeautifulSoup
from selectolax.parser import HTMLParser
import csv



FILEPARAMS = 'params_tab2.csv'

def create_csv(filename, order):
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        csv.DictWriter(file, fieldnames=order).writeheader()

def write_csv(filename, data):
    with open(filename, 'a', encoding='utf-8', newline='') as file:
        csv.DictWriter(file, fieldnames=list(data)).writerow(data)

def get_data(url):

    html = requests.get(url).text
    tree = HTMLParser(html)

    params_table_c = tree.css_first('.content').css('div')
    print(params_table_c)
    params_discr = tree.css_first('.col-md-4').css('p')
    params_disc = tree.css_first('.pt-tabs__body').css('ul')
    params_disc3 = tree.css_first('.pt-tabs').css('li')
    params_table = tree.css_first('.pt-product-single-info .pt-add-info').css('div')
    try:
        params_table_d = tree.css_first('.pt-layout-text').css('div')
    except AttributeError:
        pass



    for row in params_table_c:

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')  # html.parser
        data = soup.find("div", class_="container-indent")
        url_img = "https:" + data.find("img", class_="zoom-product").get("src")
        title1 = tree.css_first('i').text().strip()
        title = tree.css_first('h1').text().strip()
        cost = row.css_first('span').text().replace("₹", "")
        print(title1, title, cost, url_img, sep='\n')

        for row in params_discr:
            description = row.css_first('p').text().strip()
            print(description, sep=':')

        for row in params_disc:
            description2 = row.css_first('ul').text().strip()
            print(description2, sep=':')

        for row in params_disc3:
            description3 = row.css_first('li').text().strip()
            print(description3, sep=':')


        for row in params_table:
            category = row.css_first('div').text().strip()
            print(category)

        try:
            for row in params_table_d:
                description_short = row.css_first('div').text().strip()
                print(description_short, sep='\n')
                data = {'title': title, 'cost': cost, 'category': category, 'description_short': description_short, 'description': description, 'url_img': url_img}
                write_csv(FILEPARAMS, data)
        except UnboundLocalError:
                description_short = 'No description'
                print(description_short, sep='\n')
                data = {'title': title, 'cost': cost, 'category': category, 'description_short': description_short,
                        'description': description, 'url_img': url_img}
                write_csv(FILEPARAMS, data)

def main():
    order = ['title', 'cost', 'category', 'description_short', 'description',  'url_img']
    create_csv(FILEPARAMS,order)

    with open('urls_solar.csv', 'r', encoding='utf-8') as file:
        for line in csv.DictReader(file):
            url = line['url']
            get_data(url)



if __name__ == '__main__':
    main()