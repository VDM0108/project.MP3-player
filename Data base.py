import os

import pandas as pd
#парсинг
import requests
import csv
from bs4 import BeautifulSoup as bs
import pandas as pd
from pathlib import Path





def create_db():
    all_music = pd.DataFrame({'Name':  [], 'Author': [],  'Path': []})
    print(all_music)
    all_music.to_excel('./all_music.xlsx', index = False)
    all_music = pd.read_excel('./all_music.xlsx')
    print(1, all_music)

#create_db()


def add_track(name, author, path):
    all_music = pd.read_excel('./all_music.xlsx')
    print(all_music)
    all_music.loc[ len(all_music.index )] = [name, author, path]
    #new_track = {'Author':  author, 'Name': name, 'Url':  url, 'Path': path}
    #all_music = all_music.append(new_track, ignore_index=True)
    print(all_music)
    all_music.to_excel('./all_music.xlsx', index = False)

def get_data():
    all_music = pd.read_excel('./all_music.xlsx')
    music = []
    for i in range(all_music.shape[0]):
        music.append([all_music.loc[i]['Name'], all_music.loc[i]['Author'], all_music.loc[i]['Path']])
    return music

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



#как-то происходит выбор нужного url для скачивания из urls
def download(url):
    k = urls.index(url)
    r = requests.get(url, allow_redirects = True)
    x = names[k]
    y = artists[k]
    name = y+x+'.mp3'
    dir_path = os.getcwd()
    path = dir_path + '/Music/' + y + x +'.mp3'
    open(path, 'wb').write(r.content)
    #x = "_".join(x.split())
    #y = "_".join(y.split())
    #p = Path(y + x + ".mp3").resolve()

    print(x, y, path)
    #return(k)
    add_track(x, y, path)


#create_db()
inp = input()
parcing(inp)
url = urls[0]
k = download(url)


#add_track('sd', 'sd', 'sds')
