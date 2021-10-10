import requests
from bs4 import BeautifulSoup
import sqlite3

URL = 'https://tk-dm.ru/'
HOST = 'https://tk-dm.ru'
list_data_chapters = []
list_data_product = []


def parser_chapters():
    """
    Собираем URLы разделов.
    """
    chapters_request = requests.get(url=URL).text
    soup_chap = BeautifulSoup(chapters_request, 'lxml')
    chapters_soup = soup_chap.find(class_='folders').find_all('a')
    for chapter in chapters_soup:
        list_data_chapters.append(HOST + chapter.get('href'))
    return list_data_chapters


def parser_product(section_number):
    """
    С помощью URLов с разделами собераем данные о таварах внутри раздела.
    """
    list_data_product.clear()
    product_request = requests.get(list_data_chapters[section_number]).text
    soup_prod = BeautifulSoup(product_request, 'lxml')
    product_data = soup_prod.find_all(class_='product-top')
    for product in product_data:
        list_data_product.append({
            'name': product.find(class_='product-name').get_text(strip=True),
            'url': HOST + product.find('a').get('href'),
        })
    product_price = soup_prod.find_all(class_='product-price')
    x = 0
    for price in product_price:
        list_data_product[x]['price'] = price.find('strong').text
        x += 1


def bot_output(selection):
    """
    Формируем строки в бот
    """
    list_data = []
    # for i in list_data_product:
    #     data = f'{i["name"]}, {i["price"]}р.\n {i["url"]}'
    #     list_data.append(data)
    # return "  \n  \n  ".join(list_data)
    connect = sqlite3.connect('goods.db')
    cursor = connect.cursor()
    cursor.execute(selection)
    goods = cursor.fetchall()

    connect.commit()
    cursor.close()

    for i in goods:
        text = i[4]
        data = f'\nАртикул: {i[0]}\n {i[1]}\n Цена: {i[2]}руб.\n{text}'
        list_data.append(data)
    return list_data





