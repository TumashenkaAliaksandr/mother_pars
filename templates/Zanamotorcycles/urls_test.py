import requests
from bs4 import BeautifulSoup


def get_links(url):
    try:
        # Отправляем GET-запрос на страницу
        response = requests.get(url)

        # Если страница доступна, парсим ее
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Находим все ссылки на странице
            links = soup.find_all('a')

            # Извлекаем href из каждой ссылки
            hrefs = [link.get('href') for link in links if link.get('href')]

            return hrefs
        else:
            print(f"Страница недоступна. Код ответа: {response.status_code}")
            return []
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return []


# URL страницы, с которой нужно извлечь ссылки
url = "https://www.zanamotorcycles.com"

# Получаем список ссылок
links = get_links(url)

# Выводим ссылки
for link in links:
    print(link)
