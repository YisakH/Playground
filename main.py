from bs4 import BeautifulSoup
from selenium import webdriver
import requests

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--single-process")
chrome_options.add_argument("--disable-dev-shm-usage")

# 바로 뽐뿌 컴퓨터 게시판으로 접속한다
driver = webdriver.Chrome(chrome_options=chrome_options)
url = 'http://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu&category=4'
#r = requests.get(url)
time.sleep(2)

driver.maximize_window()
driver.get(url)

content = driver.page_source.encode('utf-8').strip()
soup = BeautifulSoup(content,"html.parser")

titles = soup.find_all('font', class_ = 'list_title')
for title in titles:
    print(title.string)

print('===========================================================================================')
