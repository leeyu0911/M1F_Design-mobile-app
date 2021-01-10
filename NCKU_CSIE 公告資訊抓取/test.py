import requests
from bs4 import BeautifulSoup


# 單篇內容測試
csie = 'http://www.csie.ncku.edu.tw'
url = 'http://www.csie.ncku.edu.tw/ncku_csie/announce/view/1566'  # 下載連結特例

response = requests.get(url)
response.encoding = 'utf8'
soup = BeautifulSoup(response.text, "html.parser")
anounce_title = soup.find_all('th')

URL = []  # 資料連結
Content = []  # 公告內容
Type = []  # 公告類型
Author = []  # 公告人員
Since = []  # 時間

URL.append(anounce_title[1].findNext().text if anounce_title[1].findNext().text == '無'
           else anounce_title[1].findNext().find('a').get('href'))
Content.append(anounce_title[2].findNext())
Type.append(anounce_title[3].findNext().text)
Author.append(anounce_title[5].findNext().text)
Since.append(anounce_title[6].findNext().text)

if soup.find_all('td')[-1].text != '未查詢到任何相關資料！！':
    FileName = [i for i in soup.find_all('th')[-1].find_next().find_next().find_next().text.split('\n') if i]
    UploadDate = [s.text for i, s in
                  enumerate(soup.find_all('th')[-1].find_next().find_next().find_next().find_all('td')) if
                  i % 3 == 1]
    FileURL = [csie + i.find_all('a')[0].get('href') for i in soup.find_all('td') if i.find_all('a') and
               'http' not in i.find_all('a')[0].get('href')[:4]]
    for i in range(len(FileName)):
        print(type(FileName[i]), FileName[i])
        print(type(UploadDate[i]), UploadDate[i])
        print(type(FileURL[i]), FileURL[i])
        print()

