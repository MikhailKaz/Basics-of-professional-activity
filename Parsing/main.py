from bs4 import BeautifulSoup # импортируем библиотеку BeautifulSoup
import requests # импортируем библиотеку requests

def parse():
    url = 'https://snovonovo.com/?s=iphone&post_type=product' # передаем необходимы URL адрес
    page = requests.get(url) # отправляем запрос методом Get на данный адрес и получаем ответ в переменную
    print(page.status_code) # смотрим ответ
    soup = BeautifulSoup(page.text, "html.parser") # передаем страницу в bs4

    block = soup.findAll('span', class_='price') # находим  контейнер с нужным классом
    for data in block: # проходим циклом по содержимому контейнера
        price = data.span.bdi.string
        print(price)

if __name__ == '__main__':
    parse()
