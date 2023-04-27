import requests
from selectolax.parser import HTMLParser
import csv


FILEPARAMS = 'params_tab.csv'

def create_csv(filename, order):
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        csv.DictWriter(file, fieldnames=order).writeheader()

def write_csv(filename, data):
    with open(filename, 'a', encoding='utf-8', newline='') as file:
        csv.DictWriter(file, fieldnames=list(data)).writerow(data)


def get_data(url):
    html = requests.get(url).text
    tree = HTMLParser(html)

    # Получаем список тегов img, игнорируя некоторые ссылки на изображения
    ignore_paths = ['https://autosolar.es/assets/images/star-email.png',
                    'https://autosolar.es/assets/images/eye-email.png',
                    'https://autosolar.es/assets/images/list-email.png',
                    'https://autosolar.es/images/paneles-solares/panel-solar-500w-deep-blue-30-ja-solar_thumb_main.jpg'
                    ]

    title = tree.css_first('h1').text().strip()
    params_cost = tree.css_first('.kit-ideal-consumption').css('div')
    params_discount = tree.css_first('.product-discount').css('div')
    params_info = tree.css_first('.padded-container-content').css('div')
    params_desc = tree.css_first('.product-intro-description').css('div')
    params_desc_compo = tree.css_first('.tab.active.composed-description').css('div')
    desc_title = tree.css_first('.product-tabs-container').css('h3')
    params_photo = tree.css_first('.product-image').css('div')
    print(title)

    for row in params_cost:
        cost = row.css_first('div').text().strip()
        print(cost)

    for row in params_photo:
        img_tag = row.css_first('img')
        if img_tag:
            img_src = img_tag.attributes.get('src')
            if img_src and img_src not in ignore_paths:
                print(img_src)

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
        words = info_one.split()
        lines = []
        current_line = ''
        for word in words:
            if len(current_line + ' ' + word) > 100:
                lines.append(current_line)
                current_line = word
            else:
                current_line += ' ' + word
        if current_line:
            lines.append(current_line)
        formatted_text = '\n'.join(lines)
        print('\nDescription:\n', formatted_text)


        for row in desc_title:
            desc_activ_title = row.css_first('h3').text().strip()
            print(desc_activ_title)

        # создаем пустое множество для хранения уникальных значений
        unique_values = set()

        for row in params_desc_compo:
            desc_activ = row.css_first('p')
            if desc_activ is not None:
                desc_activ = desc_activ.text().strip()
            else:
                desc_activ = ''

            words = desc_activ.split()
            lines = []
            current_line = ''

            for word in words:
                if len(current_line + ' ' + word) > 100:
                    lines.append(current_line)
                    current_line = word
                else:
                    current_line += ' ' + word

            formatted_compo_text = '\n'.join(lines)

            # проверяем, есть ли уже такая информация в множестве
            if formatted_compo_text.lower() not in unique_values:
                unique_values.add(formatted_compo_text.lower())

                # получаем все теги img внутри строки
                img_tags = row.css('img')
                img_srcs = []

                # добавляем ссылки на фото в список
                for img_tag in img_tags:
                    img_src = img_tag.attributes.get('src')
                    if img_src and img_src not in ignore_paths:
                        img_srcs.append(img_src)

                # выводим информацию о компоненте и его ссылки на фото
                print(f"{formatted_compo_text}: {', '.join(img_srcs)}")

        try:
            for row in params_desc:
                info_one = row.css_first('div').text().strip()
                words = info_one.split()
                lines = []
                current_line = ''
                for word in words:
                    if len(current_line + ' ' + word) > 100:
                        lines.append(current_line)
                        current_line = word
                    else:
                        current_line += ' ' + word
                if current_line:
                    lines.append(current_line)
                formatted_text = '\n'.join(lines)
                print('\nDescription:\n', formatted_text)
                data = {'title': title, 'cost': cost, 'disc_cost': disc_cost, 'img_srcs': img_srcs, 'info_line': info_line,
                        'composit': params_desc_compo, 'description_short': formatted_text,
                        'description_compo': params_desc_compo, 'url_img': img_tag}
                write_csv(FILEPARAMS, data)
        except UnboundLocalError:
            description_short = 'No description'
            print(formatted_text, sep='\n')
            data = {'title': title, 'cost': cost, 'disc_cost': disc_cost, 'img_srcs': img_srcs, 'info_line': info_line,
                    'composit': params_desc_compo, 'description_short': formatted_text,
                    'description_compo': params_desc_compo, 'url_img': img_tag}
            write_csv(FILEPARAMS, data)


def main():
    order = ['title', 'cost', 'composit', 'description_short', 'description_compo', 'url_img']
    create_csv(FILEPARAMS, order)

    with open('urls_solar.csv', 'r', encoding='utf-8') as file:
        for line in csv.DictReader(file):
            url = line['url']
            get_data(url)


if __name__ == '__main__':
    main()
