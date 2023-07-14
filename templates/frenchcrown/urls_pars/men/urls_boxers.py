from requests import Session


base_url = "https://frenchcrown.in/collections/boxers"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def main(base_url):
    s = Session()
    s.headers.update(headers)

    response = s.get(base_url)

    with open('urls_boxers.csv', 'w', newline='', encoding='utf-8') as file:
        file.write(response.text)

    print("Ссылки на товары были успешно записаны в файл 'urls_boxers.csv'.")


main(base_url)
