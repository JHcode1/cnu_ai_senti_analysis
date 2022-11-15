import requests
from bs4 import BeautifulSoup
url ='https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=105'

headers = {'User-Agent':'Mozilla/5.0 (window NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, liek Gecko)/92.0.4515.131 Safari/537.36'}
result = requests.get(url, headers=headers)

doc = BeautifulSoup(result.text, 'html.prarser')
title_list = doc.select('ul.type06_headline li')
print(len(title_list))