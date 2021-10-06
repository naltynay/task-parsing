import sqlite3

conn = sqlite3.connect("products.sqlite")

cursor = conn.cursor()
sql_query = """ CREATE TABLE product (
    id integer PRIMARY KEY,
    title text NULL,
    price text NULL,
    city_title text NULL,
    category_title text NULL
)"""
cursor.execute(sql_query)