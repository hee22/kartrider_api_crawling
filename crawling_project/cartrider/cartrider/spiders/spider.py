
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
        "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50X2lkIjoiNDE5NDY3NjM1IiwiYXV0aF9pZCI6IjIiLCJ0b2tlbl90eXBlIjoiQWNjZXNzVG9rZW4iLCJzZXJ2aWNlX2lkIjoiNDMwMDExMzkzIiwiWC1BcHAtUmF0ZS1MaW1pdCI6IjIwMDAwOjEwIiwibmJmIjoxNTc1MzYyNzg3LCJleHAiOjE2Mzg0MzQ3ODcsImlhdCI6MTU3NTM2Mjc4N30.6lX7wrFWh1ayoXGRfIewm-Yt5AKAPHcbGjRhYytrzxQ",
    }
    
    def start_requests(self):
        dates = list(zip(pd.date_range("2019-06-01","2019-07-30").strftime("%Y%m%d"), pd.date_range("2019-06-02","2019-07-31").strftime("%Y%m%d")))
        match_type = "7b9f0fd5377c38514dbb78ebe63ac6c3b81009d5a31dd569d1cff8f005aa881a" # spped indi
        url_format = "https://api.nexon.co.kr/kart/v1.0/matches/all?start_date={start_date}&end_date={end_date}&offset={offset}&limit=200&match_types={match_types}"
        for start_date, end_date in dates:
            for i in list(np.linspace(0,1000,6)):
                url = url_format.format(start_date=start_date, end_date=end_date, offset=0, limit=200, match_types=match_type)
                yield scrapy.http.Request(url, headers=self.headers, callback=self.parse)
        
    def parse(self, response):
        matches = json.loads(response.body)["matches"][0]["matches"]
        for match in matches:
            url_m = "https://api.nexon.co.kr/kart/v1.0/matches/{match_id}".format(match_id=match)
            resp = requests.get(url_m, headers=self.headers)
            data1 = resp.json()["players"]
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
