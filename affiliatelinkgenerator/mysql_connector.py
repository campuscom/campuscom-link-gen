import sys
import mysql.connector
from logger import logger


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


@singleton
class Database(object):
    def __init__(self, config):
        config = config.get("database", {})
        config.update({"raise_on_warnings": True})
        try:
            conn = mysql.connector.connect(**config)
        except mysql.connector.Error as e:
            logger(e, level=40)
            sys.exit('Could not connect to database')

        self.connection = conn

    def connect(self):
        return self.connection


def update_row(config, product_id, affiliate_link):
    database = Database(config)
    connection = database.connect()
    cursor = connection.cursor()

    sql = "UPDATE products SET affiliate_link = %s WHERE product_id = %s"
    values = (affiliate_link, product_id)

    try:
        cursor.execute(sql, values)
        row_id = cursor.lastrowid
        connection.commit()

        return row_id
    except mysql.connector.Error as e:
        logger(f'Could not update row {product_id} in table products', level=40)
        logger(e, level=40)

    return None


def get_all(config, domain, newonly):
    database = Database(config)
    connection = database.connect()
    cursor = connection.cursor()

    sql = f"SELECT product_id, url FROM products"

    if newonly:
        sql = sql + f" WHERE affiliate_link IS NULL OR affiliate_link=''"

        if domain is not None:
            sql = sql + f" AND url LIKE '%{domain}%'"
    else:
        if domain is not None:
            sql = sql + f" WHERE url LIKE '%{domain}%'"

    cursor.execute(sql)
    products = cursor.fetchall()

    return products
