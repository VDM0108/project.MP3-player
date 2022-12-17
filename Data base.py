import os

import pandas as pd
#парсинг
import requests
import csv
from bs4 import BeautifulSoup as bs
import pandas as pd
from pathlib import Path



def create_dir():
    'Create dir Music'
    parent_path = os.getcwd()
    dir_name = 'Music'
    path = os.path.join(parent_path, dir_name)
    os.mkdir(path)

#create_dir()

def create_db(db_name):
    'Create (name).xlsx'
    all_music = pd.DataFrame({'Name':  [], 'Author': [],  'Path': []})
    #print(all_music)
    all_music.to_excel('./' + db_name + '.xlsx', index = False)
    #all_music = pd.read_excel('./all_music.xlsx')
    #print(1, all_music)

#create_db()


def delete_track(db_name, path):
    df = pd.read_excel('./' + db_name + '.xlsx')
    ind = df.index[df['Path'] == path].tolist()[0]
    new_df = df.iloc[:ind]
    new_df[ind:] = df[ind + 1:]
    df.to_excel('./' + db_name + '.xlsx', index=False)


def add_track(db_name, name, author, path):
    'Adds track to data base'
    all_music = pd.read_excel('./' + db_name + '.xlsx')
    #print(all_music)
    all_music.iloc[::] = all_music.iloc[::-1]
    all_music.loc[len(all_music.index)] = [name, author, path]
    all_music.iloc[::] = all_music.iloc[::-1]
    #new_track = {'Author':  author, 'Name': name, 'Url':  url, 'Path': path}
    #all_music = all_music.append(new_track, ignore_index=True)
    #print(all_music)
    all_music.to_excel('./' + db_name + '.xlsx', index = False)

def get_data(db_name):
    'Gives the whole data of all_music.xlsx'
    all_music = pd.read_excel('./' + db_name + '.xlsx')
    music = []
    for i in range(all_music.shape[0]):
        music.append([all_music.loc[i]['Name'], all_music.loc[i]['Author'], all_music.loc[i]['Path']])
    return music

def parcing(inp):
    'Finds the current track'
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
    'Downloads the chosen track'
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
