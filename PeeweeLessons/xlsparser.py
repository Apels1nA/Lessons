import xlrd # Чтение xls
import psycopg2 #Заполенние БД
import math #Округление цен


def lineProcessing(unprocessedString):
    if unprocessedString[6] == '' or unprocessedString[7] == '': #Проверка наличия цены
        return 0
    else: #Обработка строки
        unprocessedString[1] = str(unprocessedString[1])[0:-2]
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

def updateTable(processedString, cur):
    if processedString != 0:
        cur.execute(
            "INSERT into fullprice (code, barcode, nomenclature, category, product_type, packing, price, price_rrc, quantity_in_stock, disable_discount, max_discount, material, brand_name, country, manufacturer, volume, diameter, length, width, box_weight, box_volume, box_length, box_width, box_height, minimum_lot, photo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", processedString
        )

def xls_reader():
    isFirstRow = True
    rb = xlrd.open_workbook('/Users/ilyamiskelo/Projects/Work/gardenShop/backend/storage/data.xls',formatting_info=True)
    sheet = rb.sheet_by_index(0)
    con = psycopg2.connect(
            database="gardenshop", 
            user="ilyamiskelo", 
            password="", 
            host="127.0.0.1", 
            port="5432"
        )
    cur = con.cursor()
    for rownum in range(sheet.nrows):
        row = sheet.row_values(rownum)
        if isFirstRow:
            isFirstRow = False
            continue
        
        updateTable(lineProcessing(row), cur)
        #break

    con.commit()
    con.close()



xls_reader()