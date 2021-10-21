from os import error
import sqlite3

# get all the products from the file products.txt for setup of db
def get_products():
    products = list()
    try:
        with open('products.txt') as f:
            for index, line in enumerate(f.readlines()):
                product = line.split()
                product[1] = int(product[1])
                product.insert(0, index+1)
                products.append(tuple(product))
    except Exception as err:
        raise err
    return products

#variable declaration
connection = None
cursor = None


# connect to database and create products as mentioned in the products.txt file
try:
    connection = sqlite3.connect('codem\ecommerceapi\db.sqlite3')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM simpleapi_product ')
    connection.commit()
    for product in get_products():
        cursor.execute("insert into simpleapi_product values (?, ?, ?)", product)
    connection.commit()
except Exception as e:
    print(e)
finally:
    cursor.close()
    connection.close()