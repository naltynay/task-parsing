import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

from flask import Flask, render_template
import sqlite3


app = Flask(__name__)


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("products.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn


baseurl = "https://kingfisher.kz/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}


@app.route('/')
def get_product():
    conn = db_connection()
    cursor = conn.cursor()
    e = requests.get(baseurl).text
    soup_cat=BeautifulSoup(e,'html.parser')
    categorylist = soup_cat.find_all("ul",{"class":"submenu"})
    for category in categorylist:
        for subcat in category:
            link = subcat.find("a",{"class":""}).get('href')
            category_title = subcat.find("a",{"class":""}).text.replace('\n',"")
            parse_url = baseurl+link[1:]
            k = requests.get(parse_url).text
            soup_product=BeautifulSoup(k,'html.parser')
            productlist = soup_product.find_all("div",{"class":"goodsBlock"})
            for product in productlist:
                title = product.find("a",{"class":"title"}).text.replace('\n',"")
                price = product.find("span",{"class":"price"}).text.replace('\n',"")
                city_title = "(Актау,Актобе,Алматы,Атырау,Караганда,НурСултан ,Павлодар,Темиртау,Шымкент)"
                sql = """INSERT INTO product (title, price, city_title, category_title)
                            VALUES (?, ?, ?, ?)"""
                
                cursor = cursor.execute(sql, (title, price, city_title, category_title))
                conn.commit()

    return "OK"
