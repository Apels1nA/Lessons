import requests #Загрузка CSV
import urllib.request #Загрузка CSV
import os #удаление CSV файла перед загрузкой
import psycopg2 #Заполенние БД
import csv # Чтение CSV файла
import math #Округление цен


def downloadCSV():
    if os.path.isfile('/Users/ilyamiskelo/Projects/Work/gardenShop/backend/storage/data.csv'): #Проверка существования файла перед удалением
        os.remove('/Users/ilyamiskelo/Projects/Work/gardenShop/backend/storage/data.csv')

    url = 'https://arti-m.ru/pricelist/fullprice.csv'

    r = requests.get(url)

    with open("/Users/ilyamiskelo/Projects/Work/gardenShop/backend/storage/data.csv", "wb") as code:
        code.write(r.content)

    urllib.request.urlretrieve(url, "/Users/ilyamiskelo/Projects/Work/gardenShop/backend/storage/data.csv")

def lineProcessing(unprocessedString):
    if unprocessedString[6] == '' or unprocessedString[7] == '': #Проверка наличия цены
        return 0
    else: #Обработка строки
        unprocessedString[6] = str(unprocessedString[6]).replace(',', '.') #Цена
        unprocessedString[7] = str(unprocessedString[7]).replace(',', '.') #ЦенаРРЦ
        unprocessedString[6] = math.ceil(float(unprocessedString[6])) #Цена
        unprocessedString[7] = math.ceil(float(unprocessedString[7])) #ЦенаРРЦ
        unprocessedString[19] = str(unprocessedString[19]).replace(',', '.') #Вес_коробки
        unprocessedString[20] = str(unprocessedString[20]).replace(',', '.') #Объем_коробки
        unprocessedString[21] = str(unprocessedString[21]).replace(',', '.') #Длинна_коробки
        unprocessedString[22] = str(unprocessedString[22]).replace(',', '.') #Ширина_коробки
        unprocessedString[23] = str(unprocessedString[23]).replace(',', '.') #Высота_коробки

        if unprocessedString[24] == '': #Минимальая_партия
            unprocessedString[24] = 0

        processedString = unprocessedString
        return processedString

def updateTable(processedString):
    con = psycopg2.connect(
        database="gardenshop", 
        user="ilyamiskelo", 
        password="", 
        host="127.0.0.1", 
        port="5432"
    )
    cur = con.cursor()
    cur.execute(
        "INSERT into fullprice (code, barcode, nomenclature, category, product_type, packing, price, price_rrc, quantity_in_stock, disable_discount, max_discount, material, brand_name, country, manufacturer, volume, diameter, length, width, box_weight, box_volume, box_length, box_width, box_height, minimum_lot, photo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", processedString
    )
    con.commit()
    con.close()


def csv_reader(file_obj):
    reader = csv.reader(file_obj, delimiter=';')
    isFirstRow = True

    for row in reader:

        if isFirstRow:
            isFirstRow = False
            continue
        
        updateTable(lineProcessing(row))
        #break

def refreshCSV():
    csv_path = "/Users/ilyamiskelo/Projects/Work/gardenShop/backend/storage/data.csv"

    with open(csv_path, "r") as f_obj:
        csv_reader(f_obj)


downloadCSV()
refreshCSV()