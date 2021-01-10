# coding=utf-8
# pip install beautifulsoup4==4.9.3
# pip install requests==2.25.1
# pip3 install pyodbc


import requests
from bs4 import BeautifulSoup
# import pyodbc
from time import time
import json


t1 = time()
# setup database
with open('keys.json', 'r', encoding='utf-8') as f:
    keys = json.load(f)
driver = keys['driver']
server = keys['server']
database = keys['database']
username = keys['username']
password = keys['password']

# cnxn = pyodbc.connect(Driver=driver, Server=server, Database=database, Uid=username, Pwd=password)
# cursor = cnxn.cursor()

# get NCKU CSIE web announces
csie = 'http://www.csie.ncku.edu.tw'
url = csie + '/ncku_csie/announce/news/1000'
response = requests.get(url)
response.encoding = 'utf8'
soup = BeautifulSoup(response.text, "html.parser")
web_announces = soup.find_all("td")

Status = []  # 公告標籤
Title = []  # 標題
articleURL = []  # 網址

for i in range(len(web_announces)):
    # if i%2 == 0:
    #     Since.append(web_anounces[i].text)
    if i % 2 == 1:
        temp = web_announces[i].text.split('\xa0\xa0')  # ['一般', '[徵才公告]  AWS 2021校園招募']
        Status.append(temp[0])
        Title.append(temp[1])
        articleURL.append(csie + web_announces[i].find('a')['href'])

# 反轉順序
Status.reverse()
Title.reverse()
articleURL.reverse()

# 每篇公告進去抓取內容
URL = []  # 資料連結
Content = []  # 公告內容
Type = []  # 公告類型
Author = []  # 公告人員
Since = []  # 時間

# 有下載檔案才需要
FileName, UploadDate, FileURL = [], [], []
for index, uid in enumerate(articleURL):
    response = requests.get(uid)
    response.encoding = 'utf8'

    soup = BeautifulSoup(response.text, "html.parser")
    anounce_title = soup.find_all('th')

    URL.append(anounce_title[1].findNext().text if anounce_title[1].findNext().text == '無'
               else anounce_title[1].findNext().find('a').get('href'))
    Content.append(str(anounce_title[2].findNext()).replace('\xa0', ' '))
    Type.append(anounce_title[3].findNext().text)
    Author.append(anounce_title[5].findNext().text)
    Since.append(anounce_title[6].findNext().text)

    # Confirm whether the data is in the database
    check_duplicate_url_title = Title[index]
    check_duplicate_url_since = Since[index]
    check_duplicate_url = f'https://www.tuuuna.com/api/searchtitle?title={check_duplicate_url_title}&since={check_duplicate_url_since}'

    # if requests.get(check_duplicate_url).text == '[]':  # 如果資料庫中沒有 才進入
    if requests.get(check_duplicate_url).text != '[]':  # 如果資料庫中有 才進入
        myaid = 0
        # feedback_from_sql = cursor.execute('call xp_insertarticle(4, ?,?,?,?,?,?,?,?)',
        #                                    articleURL[index], Title[index], URL[index], Content[index],
        #                                    Type[index], Status[index], Author[index], Since[index])

        if soup.find_all('td')[-1].text != '未查詢到任何相關資料！！':
            FileName = [i for i in soup.find_all('th')[-1].find_next().find_next().find_next().text.split('\n') if
                        i]
            UploadDate = [s.text for i, s in
                          enumerate(soup.find_all('th')[-1].find_next().find_next().find_next().find_all('td')) if
                          i % 3 == 1]
            FileURL = [csie + i.find_all('a')[0].get('href') for i in soup.find_all('td') if i.find_all('a') and
                       'http' not in i.find_all('a')[0].get('href')[:4]]
            # print(FileName, UploadDate, FileURL)
            for i in range(len(FileName)):
                print(type(FileName[i]), FileName[i])
                print(type(UploadDate[i]), UploadDate[i])
                print(type(FileURL[i]), FileURL[i])
                print()
                # cursor.execute('call xp_insertFile(?,?,?,?)', myaid, FileName[i], UploadDate[i],
                #                FileURL[i])
                # cursor.commit()

# cursor.close()
# cnxn.close()
print(time() - t1)
