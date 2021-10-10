import requests
from bs4 import BeautifulSoup
import sqlite3
import json

URL = 'https://tk-dm.ru/'

list_data_product = []


def collects_url():
    """Собираем URL на товары и записываем в файл"""

    list_data_chapters = []
    list_url_product = []
    chapters_request = requests.get(url=URL).text
    soup_chapters = BeautifulSoup(chapters_request, 'lxml')
    chapters_url = soup_chapters.find(class_='folders').find_all('a')
    for urls in chapters_url:
        for i in range(0, 4):
            list_data_chapters.append(URL + urls.get('href') + f'/p/{i}')

    for url in list_data_chapters:
        url_request = requests.get(url=url).text
        soup_url = BeautifulSoup(url_request, 'lxml')
        for links in soup_url.find_all('a'):
            href = links.get('href')
            if '/magazin/product/' in str(href):
                list_url_product.append(URL + href)

    new_set_url_product = set(list_url_product)
    new_list_url_product = list(new_set_url_product)

    with open('domashnie_melochi_url.txt', 'w', encoding='UTF8') as file_w:
        for i in new_list_url_product:
            file_w.write(i + '\n')


def collects_data():
    """Подготавлеваем для записи в фаил"""
    with open('domashnie_melochi_url.txt', 'r', encoding='UTF8') as file:
        for line in file:
            link = line[0:-1]
            print(link)
            goods_request = requests.get(url=link).text
            soup_goods = BeautifulSoup(goods_request, 'lxml')
            vendor_code = soup_goods.find(class_='product-card-right').find(class_='product-article').get_text()
            name_goods = soup_goods.find(class_='product-card-right').find(class_='product-name-h1').get_text()
            price_goods = soup_goods.find(class_='product-card-right').find(class_='price-current').get_text(strip=True)
            url_jpeg_soup = soup_goods.find(class_='product-image').find('img')
            try:
                url_jpeg = URL + url_jpeg_soup.get('src')
            except Exception as err:
                print(link, f'>>>нет фотографии товара>>>{err}')
            list_data_product.append({
                'vendor_code': vendor_code,
                'name_goods': name_goods,
                'price_goods': price_goods,
                'url_goods': link,
                'url_jpeg': url_jpeg
            })


def write_file():
    with open('list_data_product.json', 'w', encoding='UTF 8') as file_d:
        json.dump(list_data_product, file_d)


def recording_in_bd():
    """Создаем БД и Записываем данные"""
    conn = sqlite3.connect('goods.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS goods (
        Артикул TEXT,
        Наименование TEXT,
        Цена INTEGER,
        Ссылка на сайт TEXT,
        Картинка TEXT
        )""")
    with open('list_data_product.json', 'r', encoding='UTF 8') as read_to_file:
        data = json.load(read_to_file)
        for line in data:
            vendor_code = line['vendor_code'][8:]
            name_goods = line['name_goods']
            price_goods = line['price_goods'][:-4]
            url_goods = line['url_goods']
            url_jpeg = line['url_jpeg']
            print(vendor_code, name_goods, price_goods, url_goods, url_jpeg)
            sqlite_insert_with_param = '''INSERT INTO goods('Артикул', 'Наименование', 'Цена', 'Ссылка', 'Картинка')
            VALUES(?, ?, ?, ?, ?)'''
            data_tuple = (vendor_code, name_goods, price_goods, url_goods, url_jpeg)
            cursor.execute(sqlite_insert_with_param, data_tuple)
    conn.commit()
    cursor.close()


# collects_data()
# write_file()
recording_in_bd()
