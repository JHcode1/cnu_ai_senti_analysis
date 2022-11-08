import requests
import re
import math
from bs4 import BeautifulSoup


##################
# 1.영화 제목 수집 #
##################

# movie_code: 네이버 영화 코드(6자라 숫자)


# 제목수집
# 함수생성
# - 1.생성  2.호출
# - 함수는 생성하면 아무 동작x
# - 반드시 생성 후 호출을 통해서 사용!

def movie_title_crawler(movie_code):
    url = f'https://movie.naver.com/movie/bi/mi/point.naver?code={movie_code}'
    result = requests.get(url)
    doc = BeautifulSoup(result.text, 'html.parser')
    title = doc.select('h3.h_movie > a')[0].get_text()
    return title


# 리뷰 수집(리뷰, 평점, 작성자, 작성일자) + 제목
def movie_review_crawler(movie_code):
    title = movie_title_crawler(movie_code)  # 제목 수집

    # 리뷰를 수집하는 코드 작성!
    # set {제목, 리뷰, 평점, 작성자, 작성일자}
    print(f'>> Start collecting movies for {title}')
    url = f'https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver?code={movie_code}&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page=1'

    result = requests.get(url)
    doc = BeautifulSoup(result.text, 'html.parser')
    all_count = doc.select('strong.total > em')[0].get_text()  # 리뷰 전체 count

    # "2,480" : str type(문자열)
    # 문자열 나눗셈? (X)
    # print(type(all_count))
    # "2480" -> 2480 (O)
    # "2,480" -> 2480? 문자 포함 변환 (X)

    # 1. 숫자만 추출 : 정규식 (이메일 정규식, 숫자 정규식 - 구글링 하면 나옴)
    numbers = re.sub(r'[^0-9]', '', all_count)  # 0~9 사이의 숫자 제외하고 전부 '' 공백으로 바꿈
    pages = math.ceil(int(numbers) / 10)  # 반올림?
    print(f'The total number of pages to collect is {pages}')

    # 해당 페이지 리뷰 수집!
    count = 0  # 전체 리뷰 수를 count

    for page in range(1, pages+1):
        url = f'https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver?code={movie_code}&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&{page}'
        result = requests.get(url)
        doc = BeautifulSoup(result.text, 'html.parser')
        review_list = doc.select('div.score_result > ul > li')  # 한 page의 리뷰 10건

        for i, one in enumerate(review_list):  # review 1건씩 수집
            # 리뷰, 평점, 작성자, 작성일자
            review = one.select('div.score_reple > p > span')[-1].get_text().strip()  # -1 : 맨 마지막 값 의미, strip : 공백 지움 함수
            score = one.select('div.star_score > em')[0].get_text()

            # 전처리 : 날짜 시간 -> 날짜만 추출
            # 예 : 2022.10.19 15:28 -> 22.10.19
            # - 날짜는 항상 16글자로 구성 (01.01)
            original_date = one.select('div.score_reple dt > em')[1].get_text()

            # 문자열 추출
            # [시작:끝+1], 끝은 포함x
            # [:15] 0~14
            # [3:] 8~끝까지
            date = original_date[:10]  # 문자열 추출

            original_writer = one.select('div.score_reple dt > em')[0].get_text().strip()
            idx_end = original_writer.find('(')  # (의 인덱스 번호
            writer = original_writer[:idx_end]

            count += 1
            print(f"## 리뷰_{count} #####################################################################################")
            print(f'# Review: {review}')
            print(f'# writer: {writer}')
            print(f'# Score: {score}')
            print(f'# Date: {date}\n')

        break

        # 수집(리뷰) -> 저장(db) -> 전처리, 탐색 -> 딥러닝모델 학습 & 평가(긍부정 분석기) -> 시각화 or 실제 데이터 서비스

        # MongoDB 데이터베이스
        # 1. Local(컴퓨터) 설치
        # 2. 웹 클라우드 사용(ip, 내부 ip 사용 x)

