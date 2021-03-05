import csv

from peewee import *

db = PostgresqlDatabase(database='test', user='postgres', password='', host='localhost')

class Coin(Model):
    code = CharField()
    model = CharField()
    price = IntegerField()
    brand = CharField()
    country = CharField()
    image = CharField()

    class Meta:
        database = db


def main():

    db.connect()
    db.create_tables([Coin])

    with open('shop.csv') as f:
        order = ['code', 'model', 'price', 'brand', 'country', 'image']
        reader = csv.DictReader(f, fieldnames=order, delimiter=';')

        coins = list(reader)

        #for row in coins:
        #    coin = Coin(code=row['code'], model=row['model'], price=row['price'], brand=row['brand'], country=row['country'], image=row['image'])
        #    coin.save()

        with db.atomic():
            #for row in coins:
                #Coin.create(**row)

            for index in range(0,len(coins), 10):
                Coin.insert_many(coins[index:index+10]).execute()

if __name__ == '__main__':
    main()