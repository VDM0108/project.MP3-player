#парсинг
import requests
import csv
from bs4 import BeautifulSoup as bs
import pandas as pd
from pathlib import Path
#запускать функцию, когда пользователь ввел запрос в поиск
def parcing(inp):
    global names
    global artists
    global pathes
    global urls
    names = []
    artists = []
    urls = []
    pathes = []
    song = '+'.join(inp.split())
    URL_TEMPLATE = "https://ruo.morsmusic.org/search/"+song
    r = requests.get(URL_TEMPLATE)
    soup = bs(r.text, "lxml")
    name = soup.find_all('a', class_='media-link media-name')
    artist = soup.find_all('div', class_='media-link media-artist')
    url = soup.find_all('a', class_='track-download')
    for z in url:
        z = str(z)
        e = z.find('href')
        z = z[e+6:]
        r = z.find('>')
        z = z[:r-1]
        z = "https://ruo.morsmusic.org" + z
        urls.append(z)
    for i in range(len(name)):
        for x in name[i]:
            if '\n' in x:
                x = x[21:]
                k = x.find('\n')
                x = x[:k]
                names.append(x)
    for i in range(len(names)):
        x = names[i]
        for q in x:
            if q not in 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM ':
                x = x.replace(q, "")
        x = "_".join(x.split())
        y = urls[i]
        y = y[31:]
        l = y.find('/')+1
        h = y.find('_-_'+x)
        y = y[l:h]
        y = " ".join(y.split("_"))
        artists.append(y)
    #уже можно вывести на экран name, artist, добавить в значок загрузки url
    for i in range(len(names)):
        x = names[i]
        y = artists[i]
        z = urls[i]
        x = "_".join(x.split())
        y = "_".join(y.split())
        p = Path(y+x+".mp3").resolve()
        pathes.append(p)
#как-то происходит выбор нужного url для скачивания из urls
def download(url):
    k = urls.index(url)
    r = requests.get(url, allow_redirects = True)
    x = names[k]
    y = artists[k]
    open(y+x+'.mp3', 'wb').write(r.content)
    return(k)
inp = input()
parcing(inp)
url = urls[0]
k = download(url)
#база данных
import os
import glob
import pymysql
import mysql.connector
import csv
import pymysql.cursors
from mysql.connector import Error
#подключение к бд
def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection
connection = create_server_connection("localhost", "root", 'Vadim_password1234')
#cоздание бд
def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")
create_database_query = "CREATE DATABASE IF NOT EXISTS player0"
create_database(connection, create_database_query)
#проверка подключения к бд
def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection
#выполнение команды1
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()

        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")
create_mp3player= """
CREATE TABLE IF NOT EXISTS mp3player0 (
  track VARCHAR(200) NOT NULL,
  artist VARCHAR(200),
  url VARCHAR(200),
  path VARCHAR(200)
  );
 """
connection = create_db_connection("localhost", "root", 'Vadim_password1234', 'player0')
execute_query(connection, create_mp3player)
#выполнение команды2
def execute_query(connection, sql, k):
    mydb = pymysql.connect(host='localhost', user='root', passwd='Vadim_password1234', db='player0')
    cur = mydb.cursor()
    val = []
    for i in range(len(names)):
        if i == k:
            x = names[i]
            y = artists[i]
            z = urls[i]
            t = pathes[i]
            v = (x, y, z, t)
            val.append(v)
    try:
        cur.executemany(sql,val)
        mydb.commit()
        print(cur.rowcount,"records inserted!")
    except:
        mydb.rollback()

    mydb.close()
connection = create_db_connection("localhost", "root", 'Vadim_password1234', 'player0')
sql = "INSERT INTO mp3player0(track, artist, url, path) values(%s, %s, %s, %s)"
execute_query(connection, sql, k) 