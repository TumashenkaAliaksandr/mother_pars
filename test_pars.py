import requests
from bs4 import BeautifulSoup


def get_data(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find('h1', {'class': 'product_name'}).text.strip()
    price = soup.find('div', {'class': 'price-ui'})
    cost = price.find('span').text.replace('Rs.', '').strip()
    desc = soup.find('div', {'class': 'description'}).text.strip()

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

    img_container = soup.find('div', {'class': 'image__container'})
    img_src = "https:" + img_container.find('img')['data-src']

    print(title, cost, formatted_text, img_src, sep='\n')


def main():
    url = 'https://renaindia.com/collections/kitchenware-all/products/3-in-1-compact-rotary-peeler'
    get_data(url)


if __name__ == '__main__':
    main()
