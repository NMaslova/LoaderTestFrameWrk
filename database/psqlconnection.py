import pymysql
from config import databaseconfig as cfg


def do_connection():
    mysql = cfg.database['mysql']
    return pymysql.Connect(host=mysql['host'],
                           user=mysql['user'],
                           password=mysql['password'],
                           db=mysql['db'],
                           charset=mysql['charset'],
                           cursorclass=mysql['cursorclass'])


def retrieve_data(table, column):
    connection = do_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT " + column + " FROM " + table
            cursor.execute(sql)
            result = cursor.fetchone()
        return result[column]
    finally:
        connection.close()


def is_value_in_database(value, table, column):
    connection = do_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT " + column + " FROM " + table + " WHERE " + column + "=%s"
            cursor.execute(sql, (value,))
            result = cursor.fetchone()
        if result is None:
            return False
        return True
    finally:
        connection.close()
