# 카트라이더 오픈 api 크롤링
### 1. 데이터 수집의 개요
- 19.11.22 카트라이더 오픈 api 공개
- 카트 대회에서 맵별로 다양한 카트 선택
- 맵별 카트 선택 현황에 대해 확인

### 2. 데이터 수집의 계획
- [https://developers.nexon.com/kart](https://developers.nexon.com/kart)
- 구조도

<img src="https://github.com/hee22/kartrider_api_crawling/blob/master/Flow.JPG" width="40%" height="30%" title="Flow" alt="Flow"></img>
### 3. 크롤링 방법
- Scrapy를 활용 json형식으로 수집
- [spider.py](https://github.com/hee22/kartrider_api_crawling/blob/master/crawling_project/cartrider/cartrider/spiders/spider.py)

### 4. 데이터 저장
- aws 서버 MongoDB로 저장
- [mongodb.py](https://github.com/hee22/kartrider_api_crawling/blob/master/crawling_project/cartrider/cartrider/mongodb.py)

### 5. 코드 관리
- [requirements.txt](https://github.com/hee22/kartrider_api_crawling/blob/master/requirements.txt)
- 데이터 전처리
  - [CartPre.py](https://github.com/hee22/kartrider_api_crawling/blob/master/crawling_project/CartPre.py)

### 6. 프로젝트 회고
- 오픈 api를 사용하여 크롤링에서 어려움은 없었음.
  - 다른 프로젝트 데이터 수집시 오픈 api 유무부터 확인
- 데이터 전처리 시 어려움
  - 파이썬 공부 필요
- 도메인 지식 필요
  - 카트라이더 게임 현황에 대한 지식
