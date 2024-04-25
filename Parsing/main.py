from bs4 import BeautifulSoup # импортируем библиотеку BeautifulSoup
import requests # импортируем библиотеку requests

def parse():
    url = 'https://snovonovo.com/?s=iphone&post_type=product' # передаем необходимы URL адрес
    page = requests.get(url) # отправляем запрос методом Get на данный адрес и получаем ответ в переменную
    print(page.status_code) # смотрим ответ
    soup = BeautifulSoup(page.text, "html.parser") # передаем страницу в bs4

    block = soup.findAll('span', class_='price') # находим  контейнер с нужным классом
    prices = []
    for data in block:
        price = int(''.join(filter(lambda x: x.isalnum(), data.get_text())))
        prices.append(price)
        print(price)
    print(f"Mean: ", sum(prices) / len(prices))
    print(f"Max: ", max(prices))
    print(f"Min: ", min(prices))

if __name__ == '__main__':
    parse()
