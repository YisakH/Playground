
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
url_3060ti = 'https://quasarzone.com/bbs/qb_tsy?_method=post&type=&page=1&_token=cqlsp6BWdhmOi6ULyUFquj2FLkDsbhDDvbBhF3FU&popularity=&kind=subject%7C%7Ccontent&keyword=3060ti&sort=num%2C+reply&direction=DESC'
url_3070 = 'https://quasarzone.com/bbs/qb_tsy?_method=post&type=&page=1&_token=xw5MYBASLz7MNLQIhUslrgSSK6TTRzjwQiuxomgK&popularity=&kind=subject&keyword=3070&sort=num%2C+reply&direction=DESC'

ip = "192.168.30.15"
port = 1883
passwd = open("./passwd.txt", 'r').readline()

conn = pymysql.connect(host='192.168.30.15', user='root', password=passwd, db='crwaling', charset='utf8')
cur = conn.cursor()

        
def insert_data(data, gpu_name):
    
    sql = "INSERT INTO "+ gpu_name +" (text) VALUES('" + str(data) + "')"
    cur.execute(sql)
    conn.commit()
    
def get_last_notice(gpu_name):
    cur.execute("SELECT text FROM " + gpu_name + " ORDER BY num DESC LIMIT 1")

    row = cur.fetchall()
    
    if(len(row) > 0):
        value = row[0][0]
        return value
    return row

def crawling(url, gpu_name):
    driver.maximize_window()
    driver.get(url)
    
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content,"html.parser")
    titles = soup.find_all('span', class_ = 'ellipsis-with-reply-cnt')
    
    last = get_last_notice(gpu_name)
    key = 0
    
    for title in titles:
        if(title.text == last):
            break
        
        key+=1
    
    for title in reversed(titles[:key]):
        insert_data(title.text, gpu_name)

crawling(url_3060ti, 'rtx3060ti')
crawling(url_3070, 'rtx3070')
