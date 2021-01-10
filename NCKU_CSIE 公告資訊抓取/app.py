# coding=utf-8
# pip install beautifulsoup4==4.9.3
# pip install requests==2.25.1
# pip3 install pyodbc


import requests
from bs4 import BeautifulSoup
import time
import pyodbc
import json

sleep_time = 300

# setup database
with open('keys.json', 'r', encoding='utf-8') as f:
    keys = json.load(f)
driver = keys['driver']
server = keys['server']
database = keys['database']
username = keys['username']
password = keys['password']
try:
    cnxn = pyodbc.connect(Driver=driver, Server=server, Database=database, Uid=username, Pwd=password)
    cursor = cnxn.cursor()
except Exception as e:
    assert 0, str(e) + ' \nconnect sql fail...'


# get NCKU CSIE web announces
csie = 'http://www.csie.ncku.edu.tw'
url = csie + '/ncku_csie/announce/news/1000'


count = 0
while True:
    count = count + 1
    print('#', count)

    try:
        response = requests.get(url)
        response.encoding = 'utf8'
        soup = BeautifulSoup(response.text, "html.parser")
        web_announces = soup.find_all("td")

        Status = []  # 公告標籤
        Title = []  # 標題
        articleURL = []  # 網址

        for i in range(len(web_announces)):
            # if i % 2 == 0:
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


        # 每個通知進去該網頁抓內容
        URL = []  # 資料連結
        Content = []  # 公告內容
        Type = []  # 公告類型
        Author = []  # 公告人員
        Since = []  # 時間
        FileName, UploadDate, FileURL = [], [], []  # 附加檔案

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

            # check_duplicate_url_title = Title[index]
            check_duplicate_url_since = Since[index]
            check_duplicate_url = f'https://www.tuuuna.com/api/searchtitle?since={check_duplicate_url_since}'
            # 驗證該筆資料是否存在資料庫中
            if requests.get(check_duplicate_url).text == '[]':
                myaid = 0
                print('新資料插入')
                try:
                    cursor.execute('call xp_insertarticle(4, ?,?,?,?,?,?,?,?)',
                                   str(articleURL[index]), str(Title[index]), str(URL[index]),
                                   str(Content[index]), str(Type[index]), str(Status[index]),
                                   str(Author[index]), str(Since[index]))
                    for i in cursor:
                        myaid = i[0]
                        break
                    print(myaid)
                except Exception as e:
                    print('insertarticle fail')
                    print(e)

                # 資料庫加入下載文件
                if soup.find_all('td')[-1].text != '未查詢到任何相關資料！！':
                    FileName = [i for i in soup.find_all('th')[-1].find_next().find_next().find_next().text.split('\n') if i]
                    UploadDate = [s.text for i, s in enumerate(soup.find_all('th')[-1].find_next().find_next().find_next().find_all('td')) if i % 3 == 1]
                    FileURL = [csie + i.find_all('a')[0].get('href') for i in soup.find_all('td') if i.find_all('a') and
                               'http' not in i.find_all('a')[0].get('href')[:4]]
                    print(FileName, UploadDate, FileURL)
                    
                    for i in range(len(FileName)):
                        try:
                            cursor.execute('call xp_insertFile(?,?,?,?)',
                                           int(myaid), str(FileName[i]),
                                           str(UploadDate[i]), str(FileURL[i]))
                            cursor.commit()
                        except Exception as e:
                            print('insertfile fail')
                            print(e)
                        
            else:
                print('已存在此筆資料')

        try:
            cursor.close()
            cnxn.close()
        except Exception as e:
            print('close fail')
            print(e)

    except Exception as e:
        print('something wrong')
        print(e)

    time.sleep(sleep_time)

