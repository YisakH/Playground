
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime
import pymysql

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--single-process")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(chrome_options=chrome_options)
url = 'https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu&page_num=20&category=5&search_type=subject&keyword=%BE%C6%C0%CC%C6%F9'


ip = "192.168.30.15"
passwd = open("passwd.txt", "r").readline()
port = 1883

conn = pymysql.connect(host='192.168.30.15', user='root', password=passwd, db='crwaling', charset='utf8')
cur = conn.cursor()

        
def insert_data(data):
    
    sql = "INSERT INTO iphone (text, date) VALUES('" + str(data) + "', '" + str(datetime.now()) +  "')"
    cur.execute(sql)
    conn.commit()
    
def get_last_notice():
    cur.execute("SELECT text FROM iphone ORDER BY num DESC LIMIT 1")

    row = cur.fetchall()
    
    if(len(row) > 0):
        value = row[0][0]
        return value
    return row

for i in range(2):
    driver.maximize_window()
    driver.get(url)
    
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content,"html.parser")
    titles = soup.find_all('font', class_ = 'list_title')
    
    last = get_last_notice()
    key = int()
    
    for title in titles:
        if(title.text == "뽐뿌게시판 업자신고 프로세스 개선 안내"):
            continue
        if(title.text == last):
            break
        
        key+=1
    
    for title in reversed(titles[:key]):
        if(title.text == "뽐뿌게시판 업자신고 프로세스 개선 안내"):
            continue
        
        insert_data(title.text)
    
    time.sleep(20)
