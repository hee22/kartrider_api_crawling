
import scrapy
import pandas as pd
import numpy as np
import json
import requests
from cartrider.items import CartriderItem

class CartriderSpider(scrapy.Spider):
    name = "Cartrider"
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": "api-key",
    }
    
    def start_requests(self):
        # 조회할 날짜 설정
        dates = list(zip(pd.date_range("2019-06-01","2019-12-02").strftime("%Y%m%d"), pd.date_range("2019-06-02","2019-12-03").strftime("%Y%m%d")))
        # match_type : spped indi
        match_type = "7b9f0fd5377c38514dbb78ebe63ac6c3b81009d5a31dd569d1cff8f005aa881a" 
        # api 주소 -> 모든 매치 리스트 조회 api
        url_format = "https://api.nexon.co.kr/kart/v1.0/matches/all?start_date={start_date}&end_date={end_date}&offset={offset}&limit=200&match_types={match_types}"
        # 조회기간 중 모든 matchId 요청
        for start_date, end_date in dates:
            for i in list(np.linspace(0,1000,6)):
                url = url_format.format(start_date=start_date, end_date=end_date, offset=0, limit=200, match_types=match_type)
                yield scrapy.http.Request(url, headers=self.headers, callback=self.parse)
        
    def parse(self, response):
        matches = json.loads(response.body)["matches"][0]["matches"]
        for match in matches:
            # api 주소 -> 특정 매치의 상세정보 조회 api
            url_m = "https://api.nexon.co.kr/kart/v1.0/matches/{match_id}".format(match_id=match)
            resp = requests.get(url_m, headers=self.headers)
            data1 = resp.json()["players"]
            # 데이터 분석을 위해 match인원이 8명인 matchId만 호출 & 반환
            if len(data1) == 8:
                yield scrapy.http.Request(url_m, headers=self.headers, callback=self.match_parse)
            else:
                continue
            
    def match_parse(self, response):
        item = CartriderItem()
        for i in range(0,8):
            item["matches"] = json.loads(response.body)["matchId"]
            item["trackId"] = json.loads(response.body)["trackId"]
            item["kart"] = json.loads(response.body)["players"][i]["kart"]
            item["matchRank"] = json.loads(response.body)["players"][i]["matchRank"]
            item["rankinggrade2"] = json.loads(response.body)["players"][i]["rankinggrade2"]
            yield item