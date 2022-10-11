# 파이썬의 경로
# 1. 프로젝트(cnu_ai_senti_analysis-main)
#  2. python package(collector)
#   3. python file(test.py, DaumNewsOne.py)
# - python package : python file 들을 모아두는 폴더
#                   폴더 아이콘안에 구멍 뚫려있음

# colab : 분석, 인공지능에 많이 사용
#       - 페이지 1개를 만들고 여기에 모든 코드를 총망라
# pycharm : 분석, 인공지능, 현업개발
#       - 모듈화가 가능

# import 와 Library
#   - Python 코드를 직접 작성해서 개발할 수 도 있지만
#       다른 개발자가 이미 만들어 놓은 코드를 사요ㅏㅇ하면 편리함
#       이미 개발 되어있는 코드들의 묶음 = 라이브러리 (module)
#       1. built in library : Python 설치시 자동으로 제공
#           ex) math, sys, os 등
#       2. 일부 Library : 사용자가 직접 추가해서 사용
#           ex) requests, beautifulsoup4 등

# Library 를 사용하기 위해서는 import 작업 진행 필요
#   - import는 도서관에서 필요한 책을 빌려오는 개념

import requests # 책 전체를 빌려옴
from bs4 import BeautifulSoup # bs4 라는 책에서 BeautifulSoup 1개 파트만 빌려옴

BeautifulSoup()

# 목표 : Daum 뉴스 웹페이지의 제목과 본문 데이터를 수집
#   1. url : https://v.daum.net/v/20221006102034412
url = 'https://v.daum.net/v/20221006102034412'
#   2. requests 로 해당 url의 html
requests.get(url)

result = requests.get(url)
# print(result.text)
# alt shift 방향키로 줄 변경 가능
# ctrl / 로 주석 처리 가능
# ctrl space 로 자동완성 기능

#   3.  BeautifulSoup 를 통해서 제목과 본문만 추출
doc = BeautifulSoup(result.text, 'html.parser')
# python 은 [] : List Type
# index    0  1  2  3   4
#       - [5, 6, 9, 10, 15] : List 내에는 다양한 데이터 저장 가능

title = doc.select('h3.tit_view')[0].get_text()  # h3 태그중에 이름이 tit_view 를 갖는 select

# html -> tag + 선택자

#   - tag : 기본적으로 정의 돼있음(h3, p, div, span, ...)

contents = doc.select('section p')  # section 태그를 부모로 둔 모든 자식 p 태그를 select


print(f'뉴스제목 : {title}')

# contents = [<p1>, <p2>, <p3>, <p4>, ...] : 복수의 본문 포함
# <p1> = <p>왱알왱알1</p>
# <p2> = <p>왱알왱알2</p>
# <p3> = <p>왱알왱알3</p>
# <p4> = <p>왱알왱알4</p>

# 반복적인 작업 -> for 문

content = ''
for line in contents:  # 순서대로 <p>를 가져와서 line 에 넣고 다음 코드 실행
    content += line.get_text()
print(f'뉴스본문 : {content}')

